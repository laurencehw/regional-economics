"""Governance residual comparison: raw vs residualised Moran's I.

Shows how much spatial clustering governance explains by comparing
raw Moran's I with Moran's I after partialing out governance scores.

Smoke-test mode generates synthetic comparison data.
Real mode reads model_summary.json files containing both raw and residual I.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Governance residual comparison for Lab 6"
    )
    parser.add_argument("--summary", type=str, default=None,
                        help="Path to model_summary.json with raw + residual Moran's I")
    parser.add_argument("--raw-summary", type=str, default=None,
                        help="Path to raw (no controls) model_summary.json")
    parser.add_argument("--residual-summary", type=str, default=None,
                        help="Path to residualised model_summary.json")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_comparison(seed: int = 42) -> Dict:
    """Generate synthetic raw vs residual comparison."""
    rng = np.random.default_rng(seed)
    raw_i = 0.45 + rng.normal(0, 0.02)
    residual_i = 0.20 + rng.normal(0, 0.02)
    return {
        "raw_i": round(float(raw_i), 4),
        "residual_i": round(float(residual_i), 4),
        "raw_p": round(float(max(0.001, 0.03 + rng.normal(0, 0.01))), 4),
        "residual_p": round(float(max(0.001, 0.12 + rng.normal(0, 0.02))), 4),
        "year": 2024,
    }


def load_comparison(args) -> Dict:
    """Load raw and residual I from summary file(s)."""
    if args.summary:
        with open(args.summary, encoding="utf-8") as f:
            s = json.load(f)
        return {
            "raw_i": s["moran_i"],
            "residual_i": s["residual_moran_i"],
            "raw_p": s["p_value_two_sided"],
            "residual_p": s["residual_p_value_two_sided"],
            "year": s.get("year", None),
        }
    elif args.raw_summary and args.residual_summary:
        with open(args.raw_summary, encoding="utf-8") as f:
            raw = json.load(f)
        with open(args.residual_summary, encoding="utf-8") as f:
            res = json.load(f)
        return {
            "raw_i": raw["moran_i"],
            "residual_i": res["moran_i"],
            "raw_p": raw["p_value_two_sided"],
            "residual_p": res["p_value_two_sided"],
            "year": raw.get("year", res.get("year", None)),
        }
    else:
        raise ValueError("Provide --summary or both --raw-summary and --residual-summary")


def plot_comparison(comparison: Dict, output_path: Path) -> None:
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

    df = pd.DataFrame({
        "Specification": ["Raw", "Residual\n(governance\npartialed out)"],
        "moran_i": [comparison["raw_i"], comparison["residual_i"]],
        "p_label": [f'p={comparison["raw_p"]:.3f}', f'p={comparison["residual_p"]:.3f}'],
    })

    p = (
        ggplot(df, aes(x="Specification", y="moran_i", fill="Specification"))
        + geom_col(width=0.5, show_legend=False)
        + geom_text(aes(label="p_label"), nudge_y=0.015, size=8, color="#666666")
        + scale_fill_manual(values=["#377eb8", "#e41a1c"])
        + labs(x="", y="Moran's I",
               title="Spatial Autocorrelation: Raw vs. Governance-Residualised")
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
        comparison = synthetic_comparison(seed=args.seed)
    else:
        comparison = load_comparison(args)

    pct_explained = 100.0 * (1.0 - comparison["residual_i"] / comparison["raw_i"])

    summary = {
        "method": "Governance_Residual_Comparison",
        "raw_i": comparison["raw_i"],
        "residual_i": comparison["residual_i"],
        "pct_explained": round(float(pct_explained), 2),
        "raw_p": comparison["raw_p"],
        "residual_p": comparison["residual_p"],
        "year": comparison["year"],
    }

    summary_path = out_dir / "governance_comparison_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary: {summary_path}")

    try:
        plot_comparison(comparison, out_dir / "governance_comparison.pdf")
    except ImportError:
        print("plotnine not installed — skipping figure generation")


if __name__ == "__main__":
    main()
