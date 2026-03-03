"""Horizontal bar chart of SCM donor weights.

Smoke-test mode generates a synthetic 9-donor weight vector.
Real mode reads one or more SCM weights CSVs from run_lab5_scm_baseline.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize SCM donor weights")
    parser.add_argument("--weights-csv", type=str, nargs="+", default=None,
                        help="One or more SCM weights CSV paths")
    parser.add_argument("--spec-label", type=str, nargs="+", default=None,
                        help="Label for each spec (must match --weights-csv length)")
    parser.add_argument("--treated-iso3", type=str, default="YEM")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_weights(seed: int = 42) -> pd.DataFrame:
    """Synthetic 9-donor weight vector (TUN dominant)."""
    donors = ["TUN", "SYR", "EGY", "LBY", "IRQ", "LBN", "JOR", "SAU", "MAR"]
    weights = [0.64, 0.17, 0.12, 0.07, 0.0, 0.0, 0.0, 0.0, 0.0]
    return pd.DataFrame({
        "donor_iso3": donors,
        "weight": weights,
        "rank": list(range(1, len(donors) + 1)),
    })


def plot_weights(df: pd.DataFrame, treated_iso3: str,
                 spec_label: str | None, output_path: Path) -> None:
    from plotnine import (
        aes, geom_col, geom_text, ggplot, labs,
        scale_fill_manual, theme, element_text, coord_flip,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    df = df.sort_values("weight", ascending=True).copy()
    df["donor_iso3"] = pd.Categorical(df["donor_iso3"],
                                       categories=df["donor_iso3"].tolist(),
                                       ordered=True)
    df["highlight"] = df["weight"].apply(lambda w: "Active" if w > 0.01 else "Negligible")

    title = f"SCM Donor Weights: {treated_iso3}"
    if spec_label:
        title += f" ({spec_label})"

    p = (
        ggplot(df, aes(x="donor_iso3", y="weight", fill="highlight"))
        + geom_col(width=0.7)
        + geom_text(aes(label="weight"), ha="left", nudge_y=0.01, size=7,
                    format_string="{:.3f}")
        + coord_flip()
        + scale_fill_manual(values={"Active": "#377eb8", "Negligible": "#bdbdbd"})
        + labs(x="", y="Weight", title=title, fill="")
        + base_theme
        + theme(figure_size=(6, 4), legend_position="none",
                plot_title=element_text(size=11))
    )
    p.save(str(output_path), dpi=300)
    print(f"Figure saved: {output_path}")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.run_smoke_test:
        all_weights = [synthetic_weights(seed=args.seed)]
        labels = ["smoke"]
    else:
        if not args.weights_csv:
            raise ValueError("Provide --weights-csv or use --run-smoke-test")
        all_weights = [pd.read_csv(p) for p in args.weights_csv]
        labels = args.spec_label or [None] * len(all_weights)

    # Use first spec for main figure and summary
    df = all_weights[0]
    top_row = df.loc[df["weight"].idxmax()]

    summary = {
        "method": "Donor_Weight_Visualization",
        "treated_iso3": args.treated_iso3,
        "n_donors": int(len(df)),
        "top_donor": str(top_row["donor_iso3"]),
        "top_weight": float(top_row["weight"]),
        "effective_donors": int((df["weight"] > 0.01).sum()),
        "smoke_test": args.run_smoke_test,
    }

    summary_path = out_dir / "donor_weights_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    plot_weights(df, args.treated_iso3, labels[0] if labels else None,
                 out_dir / "donor_weights.pdf")

    # If multiple specs, generate one figure per spec
    if len(all_weights) > 1:
        for i, (wdf, lab) in enumerate(zip(all_weights, labels)):
            fname = f"donor_weights_{i}.pdf"
            plot_weights(wdf, args.treated_iso3, lab, out_dir / fname)

    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
