"""Classic Abadie-style SCM gap figure: treated vs synthetic + gap panel.

Smoke-test mode generates a synthetic 20-year path.
Real mode reads an SCM path CSV produced by run_lab5_scm_baseline.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot SCM treated vs synthetic gap")
    parser.add_argument("--path-csv", type=str, default=None,
                        help="SCM path CSV (year, treated_outcome, synthetic_outcome, ...)")
    parser.add_argument("--intervention-year", type=int, default=None,
                        help="Override intervention year (otherwise inferred from period column)")
    parser.add_argument("--treated-iso3", type=str, default="YEM",
                        help="Treated unit ISO3 code (for labels)")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_path(seed: int = 42) -> pd.DataFrame:
    """Synthetic 20-year SCM path: 15 pre + 5 post, treated drops ~5pp post."""
    rng = np.random.default_rng(seed)
    years = list(range(2000, 2020))
    intervention_year = 2015

    rows: List[Dict] = []
    for yr in years:
        synth = 2.0 + rng.normal(0, 0.5)
        if yr < intervention_year:
            treated = synth + rng.normal(0, 0.3)
        else:
            treated = synth - 5.0 + rng.normal(0, 0.4)
        gap = treated - synth
        period = "pre" if yr < intervention_year else "post"
        rows.append({
            "year": yr,
            "treated_outcome": round(treated, 4),
            "synthetic_outcome": round(synth, 4),
            "gap_treated_minus_synth": round(gap, 4),
            "period": period,
        })
    return pd.DataFrame(rows)


def infer_intervention_year(df: pd.DataFrame, override: int | None) -> int:
    """Get intervention year from arg or first post-period year."""
    if override is not None:
        return override
    if "period" in df.columns:
        post = df.loc[df["period"] == "post", "year"]
        if not post.empty:
            return int(post.min())
    raise ValueError("Cannot infer intervention year; provide --intervention-year")


def plot_gap(df: pd.DataFrame, intervention_year: int,
             treated_iso3: str, output_path: Path) -> None:
    from plotnine import (
        aes, annotate, geom_hline, geom_line, geom_rect, geom_vline,
        ggplot, labs, scale_x_continuous, theme, element_text,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    # Filter to rows with both treated and synthetic values
    plot_df = df.dropna(subset=["treated_outcome", "synthetic_outcome"]).copy()
    plot_df["gap"] = plot_df["gap_treated_minus_synth"]

    # Melt for two-line panel 1
    lines_df = plot_df.melt(
        id_vars=["year"],
        value_vars=["treated_outcome", "synthetic_outcome"],
        var_name="series",
        value_name="outcome",
    )
    lines_df["series"] = lines_df["series"].map({
        "treated_outcome": f"{treated_iso3} (Treated)",
        "synthetic_outcome": f"Synthetic {treated_iso3}",
    })

    from plotnine import facet_wrap, geom_ribbon

    # Build two-panel data
    panel1 = lines_df.copy()
    panel1["panel"] = "Treated vs. Synthetic"

    panel2 = plot_df[["year", "gap"]].copy()
    panel2["panel"] = "Gap (Treated \u2212 Synthetic)"

    # Panel 1: lines
    p1 = (
        ggplot(panel1, aes(x="year", y="outcome", color="series", linetype="series"))
        + geom_line(size=0.9)
        + geom_vline(xintercept=intervention_year - 0.5, linetype="dashed",
                     color="#666666", size=0.6)
        + labs(x="Year", y="GDP per capita growth (%)",
               title=f"SCM: {treated_iso3} vs. Synthetic Counterfactual",
               color="", linetype="")
        + base_theme
        + theme(figure_size=(6, 3.5), legend_position="bottom",
                plot_title=element_text(size=11))
    )

    # Panel 2: gap with zero line
    p2 = (
        ggplot(plot_df, aes(x="year", y="gap"))
        + geom_line(size=0.9, color="#e41a1c")
        + geom_hline(yintercept=0, linetype="dashed", color="#808080", size=0.5)
        + geom_vline(xintercept=intervention_year - 0.5, linetype="dashed",
                     color="#666666", size=0.6)
        + labs(x="Year", y="Gap (pp)",
               title=f"Treatment Effect Gap: {treated_iso3}")
        + base_theme
        + theme(figure_size=(6, 3), plot_title=element_text(size=11))
    )

    # Save both panels
    p1.save(str(output_path), dpi=300)
    gap_path = output_path.parent / output_path.name.replace(".pdf", "_gap_only.pdf")
    p2.save(str(gap_path), dpi=300)
    print(f"Figure saved: {output_path}")
    print(f"Gap panel saved: {gap_path}")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.run_smoke_test:
        df = synthetic_path(seed=args.seed)
        treated_iso3 = "SYN"
    else:
        if not args.path_csv:
            raise ValueError("Provide --path-csv or use --run-smoke-test")
        df = pd.read_csv(args.path_csv)
        treated_iso3 = args.treated_iso3

    intervention_year = infer_intervention_year(df, args.intervention_year)

    # Compute summary stats
    pre = df.loc[df["period"] == "pre"]
    post = df.loc[df["period"] == "post"]
    pre_gap = pre["gap_treated_minus_synth"].dropna()
    post_gap = post["gap_treated_minus_synth"].dropna()

    pre_rmspe = float(np.sqrt(np.mean(np.square(pre_gap.to_numpy(dtype=float))))) if len(pre_gap) > 0 else None
    mean_post_gap = float(post_gap.mean()) if len(post_gap) > 0 else None

    summary = {
        "method": "SCM_Gap_Plot",
        "treated_iso3": treated_iso3,
        "intervention_year": int(intervention_year),
        "n_pre_years": int(len(pre)),
        "n_post_years": int(len(post)),
        "mean_post_gap": mean_post_gap,
        "pre_rmspe": pre_rmspe,
        "smoke_test": args.run_smoke_test,
    }

    summary_path = out_dir / "gap_plot_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    plot_gap(df, intervention_year, treated_iso3, out_dir / "scm_gap_plot.pdf")

    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
