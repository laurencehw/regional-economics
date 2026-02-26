"""Run SCM placebo and robustness checks for Lab 5MENA.

Two types of placebo tests:
1. In-space: treat each donor unit as if it were the treated unit,
   using the same intervention year.  Compare RMSPE ratios to rank the
   baseline treated unit.
2. In-time: keep the same treated unit but shift the intervention year
   to check whether the baseline gap is specific to the chosen cutoff.

Outputs a consolidated robustness summary with rank-based p-values.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# Reuse core SCM functions from the baseline script.
from run_lab5_scm_baseline import rmspe, solve_scm_weights


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 5SCM placebo / robustness checks")
    parser.add_argument(
        "--panel-csv",
        required=True,
        help="Estimation-ready panel CSV path",
    )
    parser.add_argument("--treated-iso3", default="SYR")
    parser.add_argument("--intervention-year", type=int, default=2022)
    parser.add_argument("--outcome-col", default="outcome_main")
    parser.add_argument("--unit-col", default="iso3")
    parser.add_argument("--time-col", default="year")
    parser.add_argument(
        "--placebo-years",
        type=str,
        default="",
        help="Comma-separated alternate intervention years for in-time placebo",
    )
    parser.add_argument(
        "--output-dir",
        default="labs/lab5_mena/output/scm_robustness",
    )
    parser.add_argument("--date-stamp", default=datetime.now().strftime("%Y-%m-%d"))
    return parser.parse_args()


def _prepare_panel(
    df: pd.DataFrame,
    unit_col: str,
    time_col: str,
    outcome_col: str,
) -> pd.DataFrame:
    """Clean and coerce panel types."""
    df = df.copy()
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
    df = df.dropna(subset=[time_col]).copy()
    df[time_col] = df[time_col].astype(int)
    df[outcome_col] = pd.to_numeric(df[outcome_col], errors="coerce")
    return df


def run_single_scm(
    outcome_pivot: pd.DataFrame,
    treated_unit: str,
    intervention_year: int,
    min_pre_periods: int = 3,
    min_donors: int = 2,
) -> Optional[Dict[str, object]]:
    """Run SCM for one treated unit / intervention year.

    Returns a dict with pre_rmspe, post_rmspe, ratio, donor_count,
    or None if the specification is infeasible.
    """
    all_units = list(outcome_pivot.columns)
    if treated_unit not in all_units:
        return None

    pre_years = outcome_pivot.index[outcome_pivot.index < intervention_year]
    post_years = outcome_pivot.index[outcome_pivot.index >= intervention_year]

    if len(pre_years) < min_pre_periods or len(post_years) < 1:
        return None

    treated_pre = outcome_pivot.loc[pre_years, treated_unit]
    if treated_pre.isna().any():
        return None

    donor_units = [
        u for u in all_units
        if u != treated_unit and not outcome_pivot.loc[pre_years, u].isna().any()
    ]
    if len(donor_units) < min_donors:
        return None

    x1 = treated_pre.to_numpy(dtype=float)
    x0 = outcome_pivot.loc[pre_years, donor_units].to_numpy(dtype=float)

    try:
        weights = solve_scm_weights(x1=x1, x0=x0)
    except Exception:
        return None

    weight_series = pd.Series(weights, index=donor_units, name="weight")

    def synthetic_value(year: int) -> Optional[float]:
        row = outcome_pivot.loc[year, donor_units]
        available = row.notna()
        if not bool(available.any()):
            return None
        w = weight_series[available].to_numpy(dtype=float)
        total = w.sum()
        if total <= 0:
            return None
        vals = row[available].to_numpy(dtype=float)
        return float(np.dot(vals, w / total))

    treated_path = outcome_pivot[treated_unit]
    synth_path = pd.Series(
        {y: synthetic_value(int(y)) for y in outcome_pivot.index},
        name="synthetic",
    )
    gap = treated_path - synth_path

    pre_gap = gap.loc[gap.index < intervention_year]
    post_gap = gap.loc[gap.index >= intervention_year]
    pre_rmspe_val = rmspe(pre_gap)
    post_rmspe_val = rmspe(post_gap)

    if pre_rmspe_val is None or pre_rmspe_val <= 0:
        ratio = None
    elif post_rmspe_val is None:
        ratio = None
    else:
        ratio = post_rmspe_val / pre_rmspe_val

    return {
        "treated_unit": treated_unit,
        "intervention_year": intervention_year,
        "donor_count": len(donor_units),
        "pre_rmspe": pre_rmspe_val,
        "post_rmspe": post_rmspe_val,
        "post_pre_rmspe_ratio": ratio,
        "mean_post_gap": float(post_gap.dropna().mean()) if not post_gap.dropna().empty else None,
        "weights": {d: float(w) for d, w in weight_series.items()},
    }


def run_in_space_placebos(
    outcome_pivot: pd.DataFrame,
    treated_unit: str,
    intervention_year: int,
) -> List[Dict[str, object]]:
    """Run SCM treating each unit as pseudo-treated, same intervention year."""
    results = []
    for unit in sorted(outcome_pivot.columns):
        result = run_single_scm(outcome_pivot, unit, intervention_year)
        if result is not None:
            result["is_baseline"] = (unit == treated_unit)
            results.append(result)
    return results


def run_in_time_placebos(
    outcome_pivot: pd.DataFrame,
    treated_unit: str,
    placebo_years: List[int],
) -> List[Dict[str, object]]:
    """Run SCM for same treated unit at alternate intervention years."""
    results = []
    for year in sorted(placebo_years):
        result = run_single_scm(outcome_pivot, treated_unit, year)
        if result is not None:
            results.append(result)
    return results


def compute_rank_p_value(
    in_space_results: List[Dict[str, object]],
    treated_unit: str,
) -> Optional[float]:
    """Fraction of placebo units with RMSPE ratio >= treated unit's ratio."""
    ratios = []
    baseline_ratio = None
    for r in in_space_results:
        ratio = r.get("post_pre_rmspe_ratio")
        if ratio is None:
            continue
        ratios.append(ratio)
        if r["treated_unit"] == treated_unit:
            baseline_ratio = ratio

    if baseline_ratio is None or len(ratios) < 2:
        return None

    rank = sum(1 for r in ratios if r >= baseline_ratio)
    return rank / len(ratios)


def main() -> None:
    args = parse_args()
    run_at = datetime.now(timezone.utc).isoformat()

    panel_path = Path(args.panel_csv)
    if not panel_path.exists():
        raise FileNotFoundError(f"Panel CSV not found: {panel_path}")

    df = pd.read_csv(panel_path)
    df = _prepare_panel(df, args.unit_col, args.time_col, args.outcome_col)

    outcome_pivot = (
        df.pivot(index=args.time_col, columns=args.unit_col, values=args.outcome_col)
        .sort_index()
    )

    # --- In-space placebos ---
    in_space = run_in_space_placebos(outcome_pivot, args.treated_iso3, args.intervention_year)
    rank_p = compute_rank_p_value(in_space, args.treated_iso3)

    # --- In-time placebos ---
    placebo_years = [
        int(y.strip()) for y in args.placebo_years.split(",")
        if y.strip()
    ]
    in_time = run_in_time_placebos(outcome_pivot, args.treated_iso3, placebo_years)

    # --- Baseline result ---
    baseline = next((r for r in in_space if r.get("is_baseline")), None)

    # --- Write outputs ---
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{args.treated_iso3.lower()}_{args.intervention_year}_{args.date_stamp}"

    in_space_path = output_dir / f"placebo_in_space_{stem}.json"
    in_time_path = output_dir / f"placebo_in_time_{stem}.json"
    summary_path = output_dir / f"robustness_summary_{stem}.json"

    in_space_path.write_text(json.dumps(in_space, indent=2), encoding="utf-8")
    if in_time:
        in_time_path.write_text(json.dumps(in_time, indent=2), encoding="utf-8")

    summary: Dict[str, object] = {
        "run_at_utc": run_at,
        "panel_csv": str(panel_path),
        "treated_iso3": args.treated_iso3,
        "intervention_year": args.intervention_year,
        "in_space_placebo_count": len(in_space),
        "in_space_rank_p_value": rank_p,
        "baseline_post_pre_rmspe_ratio": baseline["post_pre_rmspe_ratio"] if baseline else None,
        "in_time_placebo_years": placebo_years,
        "in_time_placebo_count": len(in_time),
        "in_time_results": [
            {
                "year": r["intervention_year"],
                "post_pre_rmspe_ratio": r["post_pre_rmspe_ratio"],
            }
            for r in in_time
        ],
        "outputs": {
            "in_space_json": str(in_space_path),
            "in_time_json": str(in_time_path) if in_time else None,
            "summary_json": str(summary_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"In-space placebos: {len(in_space)} units")
    print(f"Rank-based p-value: {rank_p}")
    if baseline:
        print(f"Baseline RMSPE ratio: {baseline['post_pre_rmspe_ratio']}")
    if in_time:
        print(f"In-time placebos: {len(in_time)} years")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
