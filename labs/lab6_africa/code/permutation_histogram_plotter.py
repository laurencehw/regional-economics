"""Permutation histogram: distribution of Moran's I under random permutations.

Marks the observed I as a vertical line.
Smoke-test mode uses scaffold's synthetic data.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Permutation histogram for Moran's I")
    parser.add_argument("--cross-section", type=str, default=None)
    parser.add_argument("--weight-matrix", type=str, default=None)
    parser.add_argument("--y-col", type=str, default="night_lights_mean")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--permutations", type=int, default=499)
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def compute_permutation_distribution(
    y: np.ndarray, w: np.ndarray, permutations: int, seed: int,
) -> Dict:
    """Run permutation test and return distribution statistics."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lab6_africa_moran_scaffold import morans_i, permutation_p_value

    observed_i, expected_i = morans_i(y, w)
    p_value, draws = permutation_p_value(y, w, permutations=permutations, seed=seed)

    mean_perm = float(np.mean(draws))
    std_perm = float(np.std(draws, ddof=1))
    z_score = float((observed_i - mean_perm) / std_perm) if std_perm > 0 else 0.0

    return {
        "observed_i": float(observed_i),
        "expected_i": float(expected_i),
        "mean_perm_i": mean_perm,
        "std_perm_i": std_perm,
        "p_value": p_value,
        "z_score": z_score,
        "draws": draws,
    }


def plot_histogram(draws: np.ndarray, observed_i: float,
                   year: int, output_path: Path) -> None:
    from plotnine import (
        aes, geom_histogram, geom_vline, ggplot, labs, theme,
        element_text, annotate,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    df = pd.DataFrame({"permuted_i": draws})
    p = (
        ggplot(df, aes(x="permuted_i"))
        + geom_histogram(bins=30, fill="#377eb8", alpha=0.7, color="#333333")
        + geom_vline(xintercept=observed_i, color="#e41a1c", size=1.0, linetype="solid")
        + annotate("text", x=observed_i, y=0, label=f" I = {observed_i:.3f}",
                   ha="left", va="bottom", color="#e41a1c", size=9)
        + labs(x="Moran's I (permuted)", y="Count",
               title=f"Permutation Distribution ({year})")
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
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from lab6_africa_moran_scaffold import (
            synthetic_inputs, build_weight_matrix, row_standardize,
        )
        panel_df, adjacency_df = synthetic_inputs()
        regions = panel_df["region"].tolist()
        w = row_standardize(
            build_weight_matrix(adjacency_df, regions, "region", "neighbor", "weight")
        )
        y = panel_df[args.y_col].to_numpy(dtype=float)
    else:
        if not args.cross_section or not args.weight_matrix:
            raise ValueError("Provide --cross-section and --weight-matrix, or --run-smoke-test")
        xsec = pd.read_csv(args.cross_section)
        y = xsec[args.y_col].to_numpy(dtype=float)
        wm = pd.read_csv(args.weight_matrix, index_col=0)
        w = wm.to_numpy(dtype=float)

    result = compute_permutation_distribution(
        y, w, permutations=args.permutations, seed=args.seed,
    )

    summary = {
        "method": "Permutation_Histogram",
        "observed_i": result["observed_i"],
        "mean_perm_i": result["mean_perm_i"],
        "std_perm_i": result["std_perm_i"],
        "p_value": result["p_value"],
        "n_permutations": args.permutations,
        "z_score": result["z_score"],
        "year": args.year,
    }

    summary_path = out_dir / "permutation_hist_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary: {summary_path}")

    try:
        plot_histogram(result["draws"], result["observed_i"],
                       args.year, out_dir / "permutation_histogram.pdf")
    except ImportError:
        print("plotnine not installed — skipping figure generation")


if __name__ == "__main__":
    main()
