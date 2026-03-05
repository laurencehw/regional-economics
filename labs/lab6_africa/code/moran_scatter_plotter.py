"""Moran scatter plot: outcome y vs spatial lag Wy with OLS fit line.

Smoke-test mode generates synthetic data via the scaffold.
Real mode reads cross-section + weight matrix CSVs from a scaffold run.
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
    parser = argparse.ArgumentParser(description="Moran scatter plot for Lab 6")
    parser.add_argument("--cross-section", type=str, default=None,
                        help="Path to cross_section_used.csv from scaffold")
    parser.add_argument("--weight-matrix", type=str, default=None,
                        help="Path to weight_matrix.csv from scaffold")
    parser.add_argument("--y-col", type=str, default="night_lights_mean")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def compute_scatter_data(y: np.ndarray, w: np.ndarray) -> Dict:
    """Compute Moran scatter components: standardised y, spatial lag, slope."""
    y_mean = np.mean(y)
    y_std = np.std(y, ddof=0)
    if y_std <= 0:
        raise ValueError("Zero variance in y — cannot compute Moran scatter.")
    z = (y - y_mean) / y_std
    wz = w @ z

    # OLS slope of Wz on z (= Moran's I)
    slope = float(np.dot(z, wz) / np.dot(z, z))

    # Quadrant counts (HH, LH, LL, HL)
    hh = int(np.sum((z > 0) & (wz > 0)))
    lh = int(np.sum((z < 0) & (wz > 0)))
    ll = int(np.sum((z < 0) & (wz < 0)))
    hl = int(np.sum((z > 0) & (wz < 0)))

    return {
        "z": z,
        "wz": wz,
        "slope": slope,
        "quadrant_counts": {"HH": hh, "LH": lh, "LL": ll, "HL": hl},
    }


def plot_scatter(z: np.ndarray, wz: np.ndarray, slope: float,
                 year: int, output_path: Path) -> None:
    from plotnine import (
        aes, geom_abline, geom_hline, geom_point, geom_vline,
        ggplot, labs, theme, element_text,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    df = pd.DataFrame({"z": z, "wz": wz})
    p = (
        ggplot(df, aes(x="z", y="wz"))
        + geom_point(color="#377eb8", alpha=0.7, size=2.5)
        + geom_abline(intercept=0, slope=slope, color="#e41a1c", size=0.9)
        + geom_hline(yintercept=0, linetype="dashed", color="#808080", size=0.4)
        + geom_vline(xintercept=0, linetype="dashed", color="#808080", size=0.4)
        + labs(x="Standardised Night Lights (z)",
               y="Spatial Lag (Wz)",
               title=f"Moran Scatter Plot ({year}), I = {slope:.3f}")
        + base_theme
        + theme(figure_size=(6, 5), plot_title=element_text(size=11))
    )
    p.save(str(output_path), dpi=300)
    print(f"Figure saved: {output_path}")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.run_smoke_test:
        # Import synthetic data generator from scaffold
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
        year = args.year
    else:
        if not args.cross_section or not args.weight_matrix:
            raise ValueError("Provide --cross-section and --weight-matrix, or --run-smoke-test")
        xsec = pd.read_csv(args.cross_section)
        y = xsec[args.y_col].to_numpy(dtype=float)
        wm = pd.read_csv(args.weight_matrix, index_col=0)
        w = wm.to_numpy(dtype=float)
        year = args.year

    result = compute_scatter_data(y, w)

    summary = {
        "method": "Moran_Scatter",
        "n_obs": int(len(y)),
        "moran_i_slope": result["slope"],
        "quadrant_counts": result["quadrant_counts"],
        "year": year,
    }

    summary_path = out_dir / "moran_scatter_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary: {summary_path}")

    try:
        plot_scatter(result["z"], result["wz"], result["slope"],
                     year, out_dir / "moran_scatter.pdf")
    except ImportError:
        print("plotnine not installed — skipping figure generation")


if __name__ == "__main__":
    main()
