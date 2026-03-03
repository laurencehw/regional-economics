"""Pre/post event study for displacement shocks around conflict onset.

Smoke-test mode generates a synthetic 8-country x 15-year panel.
Real mode reads the Lab 5 estimation panel CSV.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conflict event study for MENA displacement")
    parser.add_argument("--panel-csv", type=str, default=None,
                        help="Panel CSV with iso3, year, outcome_main, total_displaced")
    parser.add_argument("--treated-iso3", type=str, default="YEM")
    parser.add_argument("--event-year", type=int, default=2015,
                        help="Year of conflict onset (t=0)")
    parser.add_argument("--pre-periods", type=int, default=3,
                        help="Number of pre-event periods")
    parser.add_argument("--post-periods", type=int, default=5,
                        help="Number of post-event periods")
    parser.add_argument("--n-bootstrap", type=int, default=200,
                        help="Bootstrap draws for CIs")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_panel(seed: int = 42) -> pd.DataFrame:
    """Synthetic 8-country x 15-year panel. Treated unit drops ~10pp at t=0."""
    rng = np.random.default_rng(seed)
    countries = ["YEM", "EGY", "JOR", "LBN", "MAR", "SAU", "TUN", "IRQ"]
    years = list(range(2008, 2023))
    event_year = 2015

    rows: List[Dict] = []
    for iso3 in countries:
        for yr in years:
            base = 2.0 + rng.normal(0, 1.5)
            if iso3 == "YEM" and yr >= event_year:
                base -= 10.0 + rng.normal(0, 1.0)
            displaced = 0.0
            if iso3 == "YEM" and yr >= event_year:
                displaced = rng.uniform(500_000, 4_000_000)
            rows.append({
                "iso3": iso3,
                "year": yr,
                "outcome_main": round(base, 4),
                "total_displaced": round(displaced, 0),
            })
    return pd.DataFrame(rows)


def compute_event_study(
    df: pd.DataFrame,
    treated_iso3: str,
    event_year: int,
    pre_periods: int,
    post_periods: int,
    n_bootstrap: int,
    seed: int,
) -> pd.DataFrame:
    """Compute period-specific treatment effects relative to t=-1."""
    rng = np.random.default_rng(seed)

    # Center time around event year
    df = df.copy()
    df["rel_year"] = df["year"] - event_year

    # Window
    window = list(range(-pre_periods, post_periods + 1))
    df = df[df["rel_year"].isin(window)].copy()

    treated = df[df["iso3"] == treated_iso3].set_index("rel_year")["outcome_main"]
    control_units = [u for u in df["iso3"].unique() if u != treated_iso3]

    # Control group mean by relative year
    control_means = (
        df[df["iso3"].isin(control_units)]
        .groupby("rel_year")["outcome_main"]
        .mean()
    )

    # Difference: treated - control mean
    diff = treated - control_means

    # Normalize to t=-1 baseline
    if -1 in diff.index:
        baseline = diff.loc[-1]
        diff = diff - baseline
    else:
        baseline = 0.0

    # Bootstrap CIs
    ci_lower = {}
    ci_upper = {}
    for t in window:
        if t not in treated.index:
            continue
        boot_diffs = []
        control_t = df[(df["iso3"].isin(control_units)) & (df["rel_year"] == t)]["outcome_main"]
        if control_t.empty:
            continue
        for _ in range(n_bootstrap):
            boot_control = rng.choice(control_t.values, size=len(control_t), replace=True)
            boot_diff = treated.get(t, np.nan) - np.mean(boot_control)
            # Normalize to baseline
            if -1 in treated.index:
                control_base = df[(df["iso3"].isin(control_units)) & (df["rel_year"] == -1)]["outcome_main"]
                boot_base_diff = treated.get(-1, np.nan) - np.mean(
                    rng.choice(control_base.values, size=len(control_base), replace=True)
                )
                boot_diff = boot_diff - boot_base_diff
            boot_diffs.append(boot_diff)
        boot_arr = np.array(boot_diffs)
        ci_lower[t] = float(np.percentile(boot_arr, 2.5))
        ci_upper[t] = float(np.percentile(boot_arr, 97.5))

    results = []
    for t in sorted(window):
        if t in diff.index:
            results.append({
                "rel_year": t,
                "effect": float(diff.loc[t]),
                "ci_lower": ci_lower.get(t, np.nan),
                "ci_upper": ci_upper.get(t, np.nan),
                "period": "pre" if t < 0 else "post",
            })
    return pd.DataFrame(results)


def plot_event_study(es_df: pd.DataFrame, treated_iso3: str,
                     event_year: int, output_path: Path) -> None:
    from plotnine import (
        aes, geom_errorbar, geom_hline, geom_point, geom_vline,
        ggplot, labs, theme, element_text,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    p = (
        ggplot(es_df, aes(x="rel_year", y="effect"))
        + geom_hline(yintercept=0, linetype="dashed", color="#808080", size=0.5)
        + geom_vline(xintercept=-0.5, linetype="dashed", color="#666666", size=0.6)
        + geom_errorbar(aes(ymin="ci_lower", ymax="ci_upper"),
                        width=0.2, color="#377eb8", size=0.5)
        + geom_point(color="#e41a1c", size=2.5)
        + labs(x=f"Years Relative to Conflict Onset ({event_year})",
               y="Effect on GDP Growth (pp)",
               title=f"Event Study: Conflict Displacement in {treated_iso3}")
        + base_theme
        + theme(figure_size=(6, 4), plot_title=element_text(size=11))
    )
    p.save(str(output_path), dpi=300)
    print(f"Figure saved: {output_path}")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.run_smoke_test:
        df = synthetic_panel(seed=args.seed)
    else:
        if not args.panel_csv:
            raise ValueError("Provide --panel-csv or use --run-smoke-test")
        df = pd.read_csv(args.panel_csv)

    es_df = compute_event_study(
        df,
        treated_iso3=args.treated_iso3,
        event_year=args.event_year,
        pre_periods=args.pre_periods,
        post_periods=args.post_periods,
        n_bootstrap=args.n_bootstrap,
        seed=args.seed,
    )

    # Save CSV
    csv_path = out_dir / "event_study.csv"
    es_df.to_csv(csv_path, index=False)

    # Plot
    plot_event_study(es_df, args.treated_iso3, args.event_year,
                     out_dir / "event_study.pdf")

    # Summary
    pre_effects = es_df.loc[es_df["period"] == "pre", "effect"]
    post_effects = es_df.loc[es_df["period"] == "post", "effect"]

    summary = {
        "method": "Conflict_Event_Study",
        "treated_iso3": args.treated_iso3,
        "event_year": args.event_year,
        "n_pre_periods": int(len(pre_effects)),
        "n_post_periods": int(len(post_effects)),
        "mean_pre_diff": float(pre_effects.mean()) if len(pre_effects) > 0 else None,
        "mean_post_diff": float(post_effects.mean()) if len(post_effects) > 0 else None,
        "estimated_effect": float(post_effects.mean()) if len(post_effects) > 0 else None,
        "smoke_test": args.run_smoke_test,
    }

    summary_path = out_dir / "event_study_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Summary: {summary_path}")
    print(f"CSV: {csv_path}")
    print(f"Estimated effect: {summary['estimated_effect']}")


if __name__ == "__main__":
    main()
