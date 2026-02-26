"""Run a baseline Synthetic Control for Lab 5 MENA panel.

Default baseline:
- treated unit: SYR
- intervention year: 2018
- outcome: outcome_main (WDI GDP-per-capita growth)
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Lab 5 SCM baseline")
    parser.add_argument(
        "--panel-csv",
        default="data/processed/lab5/lab5_mena_estimation_panel_2000_2024_2026-02-23.csv",
        help="Estimation-ready panel CSV path",
    )
    parser.add_argument("--treated-iso3", default="SYR")
    parser.add_argument("--intervention-year", type=int, default=2018)
    parser.add_argument("--outcome-col", default="outcome_main")
    parser.add_argument("--unit-col", default="iso3")
    parser.add_argument("--time-col", default="year")
    parser.add_argument(
        "--output-dir",
        default="labs/lab5_mena/output/scm_baseline",
        help="Directory for baseline outputs",
    )
    parser.add_argument("--date-stamp", default=datetime.now().strftime("%Y-%m-%d"))
    return parser.parse_args()


def solve_scm_weights(x1: np.ndarray, x0: np.ndarray) -> np.ndarray:
    donor_count = x0.shape[1]
    if donor_count < 1:
        raise ValueError("Need at least one donor unit")

    def objective(w: np.ndarray) -> float:
        residual = x1 - x0 @ w
        return float(np.dot(residual, residual))

    w0 = np.full(donor_count, 1.0 / donor_count)
    bounds = [(0.0, 1.0)] * donor_count
    constraints = [{"type": "eq", "fun": lambda w: float(np.sum(w) - 1.0)}]
    result = minimize(
        objective,
        w0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 2000, "ftol": 1e-12},
    )
    if result.success:
        weights = np.asarray(result.x, dtype=float)
        weights = np.clip(weights, 0.0, None)
        total = weights.sum()
        if total > 0:
            return weights / total

    # Fallback: projected gradient descent on probability simplex.
    def project_simplex(v: np.ndarray) -> np.ndarray:
        u = np.sort(v)[::-1]
        cssv = np.cumsum(u) - 1.0
        idx = np.arange(1, len(v) + 1)
        cond = u - cssv / idx > 0
        rho = idx[cond][-1]
        theta = cssv[cond][-1] / rho
        return np.maximum(v - theta, 0.0)

    gram = x0.T @ x0
    lipschitz = 2.0 * float(np.linalg.norm(gram, ord=2))
    step = 1.0 / max(lipschitz, 1e-8)
    w = w0.copy()
    prev_obj = objective(w)
    for _ in range(20000):
        grad = 2.0 * (x0.T @ (x0 @ w - x1))
        w_new = project_simplex(w - step * grad)
        obj = objective(w_new)
        if abs(prev_obj - obj) < 1e-12:
            w = w_new
            break
        w, prev_obj = w_new, obj

    weights = np.asarray(w, dtype=float)
    weights = np.clip(weights, 0.0, None)
    total = weights.sum()
    if total <= 0:
        raise RuntimeError("SCM optimization returned non-positive weight sum (fallback)")
    return weights / total


def rmspe(values: pd.Series) -> float | None:
    clean = values.dropna()
    if clean.empty:
        return None
    return float(np.sqrt(np.mean(np.square(clean.to_numpy(dtype=float)))))


def main() -> None:
    args = parse_args()
    run_at = datetime.now(timezone.utc).isoformat()

    panel_path = Path(args.panel_csv)
    if not panel_path.exists():
        raise FileNotFoundError(f"Panel CSV not found: {panel_path}")

    df = pd.read_csv(panel_path)
    required_cols = {args.unit_col, args.time_col, args.outcome_col, "treatment_event", "acled_event_count"}
    missing_cols = sorted(required_cols - set(df.columns))
    if missing_cols:
        raise ValueError(f"Panel CSV missing required columns: {missing_cols}")

    df = df.copy()
    df = df.assign(**{args.time_col: pd.to_numeric(df[args.time_col], errors="coerce")})
    df = df.dropna(subset=[args.time_col]).copy()
    df = df.assign(
        **{
            args.time_col: df[args.time_col].astype(int),
            args.outcome_col: pd.to_numeric(df[args.outcome_col], errors="coerce"),
        }
    )

    units = sorted(df[args.unit_col].dropna().astype(str).unique().tolist())
    if args.treated_iso3 not in units:
        raise ValueError(f"Treated unit not found in panel: {args.treated_iso3}")
    donor_units_all = [u for u in units if u != args.treated_iso3]

    outcome_pivot = df.pivot(index=args.time_col, columns=args.unit_col, values=args.outcome_col).sort_index()
    pre_years = outcome_pivot.index[outcome_pivot.index < args.intervention_year]
    post_years = outcome_pivot.index[outcome_pivot.index >= args.intervention_year]
    if len(pre_years) < 3:
        raise ValueError("Need at least three pre-intervention periods for SCM")

    treated_pre = outcome_pivot.loc[pre_years, args.treated_iso3]
    if treated_pre.isna().any():
        raise ValueError("Treated unit has missing pre-intervention outcomes")

    donor_units = [
        d for d in donor_units_all if not outcome_pivot.loc[pre_years, d].isna().any()
    ]
    if len(donor_units) < 2:
        raise ValueError("Need at least two donor units with complete pre-intervention outcomes")

    x1 = treated_pre.to_numpy(dtype=float)
    x0 = outcome_pivot.loc[pre_years, donor_units].to_numpy(dtype=float)
    weights = solve_scm_weights(x1=x1, x0=x0)
    weight_series = pd.Series(weights, index=donor_units, name="weight").sort_values(ascending=False)

    def synthetic_value(year: int) -> float | None:
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

    treated_path = outcome_pivot[args.treated_iso3].rename("treated_outcome")
    synth_path = pd.Series({y: synthetic_value(int(y)) for y in outcome_pivot.index}, name="synthetic_outcome")
    gap = (treated_path - synth_path).rename("gap_treated_minus_synth")

    path = pd.concat([treated_path, synth_path, gap], axis=1).rename_axis("year").reset_index()

    treated_controls = (
        df[df[args.unit_col].eq(args.treated_iso3)][[args.time_col, "treatment_event", "acled_event_count", "acled_period_flag"]]
        .drop_duplicates(subset=[args.time_col], keep="last")
        .rename(columns={args.time_col: "year"})
    )
    path = path.merge(treated_controls, on="year", how="left")
    path = path.assign(period=np.where(path["year"] < args.intervention_year, "pre", "post"))

    pre_gap = path.loc[path["period"].eq("pre"), "gap_treated_minus_synth"]
    post_gap = path.loc[path["period"].eq("post"), "gap_treated_minus_synth"]
    pre_rmspe = rmspe(pre_gap)
    post_rmspe = rmspe(post_gap)
    ratio = (post_rmspe / pre_rmspe) if pre_rmspe and pre_rmspe > 0 and post_rmspe is not None else None

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{args.treated_iso3.lower()}_{args.intervention_year}_{args.date_stamp}"

    weights_path = output_dir / f"scm_weights_{stem}.csv"
    path_path = output_dir / f"scm_path_{stem}.csv"
    summary_path = output_dir / f"scm_summary_{stem}.json"

    weight_df = (
        weight_series.reset_index()
        .rename(columns={"index": "donor_iso3"})
        .assign(rank=lambda d: np.arange(1, len(d) + 1))
    )
    weight_df.to_csv(weights_path, index=False)
    path.to_csv(path_path, index=False)

    summary: Dict[str, object] = {
        "run_at_utc": run_at,
        "panel_csv": str(panel_path),
        "treated_iso3": args.treated_iso3,
        "intervention_year": args.intervention_year,
        "outcome_col": args.outcome_col,
        "donor_count": int(len(donor_units)),
        "donors_used": donor_units,
        "pre_year_count": int(len(pre_years)),
        "post_year_count": int(len(post_years)),
        "pre_rmspe": pre_rmspe,
        "post_rmspe": post_rmspe,
        "post_pre_rmspe_ratio": ratio,
        "mean_post_gap": float(post_gap.dropna().mean()) if not post_gap.dropna().empty else None,
        "median_post_gap": float(post_gap.dropna().median()) if not post_gap.dropna().empty else None,
        "outputs": {
            "weights_csv": str(weights_path),
            "path_csv": str(path_path),
            "summary_json": str(summary_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Donors used: {len(donor_units)}")
    print(f"Pre RMSPE: {pre_rmspe}")
    print(f"Post RMSPE: {post_rmspe}")
    print(f"Post/Pre RMSPE ratio: {ratio}")
    print(f"Weights CSV: {weights_path}")
    print(f"Path CSV: {path_path}")
    print(f"Summary JSON: {summary_path}")


if __name__ == "__main__":
    main()
