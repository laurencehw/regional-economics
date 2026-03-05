"""Multi-year Moran's I comparison: dot/line plot across years with p-value annotations.

Smoke-test mode generates 5 synthetic summary dicts (2017-2021).
Real mode reads multiple model_summary.json files via --summaries glob.
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-year Moran's I comparison")
    parser.add_argument("--summaries", type=str, nargs="*", default=None,
                        help="Paths to model_summary.json files (supports glob patterns)")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def expand_globs(patterns: List[str]) -> List[str]:
    """Expand glob patterns into file paths."""
    paths = []
    for pat in patterns:
        matches = sorted(glob.glob(pat))
        paths.extend(matches)
    return paths


def synthetic_summaries(seed: int = 42) -> List[Dict]:
    """Generate 5 synthetic yearly summaries with declining Moran's I."""
    rng = np.random.default_rng(seed)
    years = [2017, 2018, 2019, 2020, 2021]
    base_i = 0.45
    summaries = []
    for j, yr in enumerate(years):
        i_val = base_i - 0.05 * j + rng.normal(0, 0.01)
        p_val = max(0.001, min(0.999, 0.05 + 0.02 * j + rng.normal(0, 0.01)))
        summaries.append({
            "method": "Global_Morans_I",
            "year": yr,
            "moran_i": round(float(i_val), 4),
            "p_value_two_sided": round(float(p_val), 4),
            "n_obs": 50,
        })
    return summaries


def compute_trend(years: List[int], i_values: List[float]) -> float:
    """OLS slope of Moran's I on year."""
    x = np.array(years, dtype=float)
    y = np.array(i_values, dtype=float)
    x_dm = x - np.mean(x)
    slope = float(np.dot(x_dm, y) / np.dot(x_dm, x_dm))
    return slope


def plot_multi_year(df: pd.DataFrame, output_path: Path) -> None:
    from plotnine import (
        aes, geom_line, geom_point, geom_text, ggplot, labs,
        scale_x_continuous, theme, element_text,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    df = df.copy()
    df["p_label"] = df["p_value"].apply(lambda p: f"p={p:.3f}")

    p = (
        ggplot(df, aes(x="year", y="moran_i"))
        + geom_line(color="#377eb8", size=0.9)
        + geom_point(color="#377eb8", size=3)
        + geom_text(aes(label="p_label"), nudge_y=0.012, size=7, color="#666666")
        + labs(x="Year", y="Moran's I",
               title="Spatial Autocorrelation of Night Lights Across Africa")
        + scale_x_continuous(breaks=df["year"].tolist())
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
        summaries = synthetic_summaries(seed=args.seed)
    else:
        if not args.summaries:
            raise ValueError("Provide --summaries paths or use --run-smoke-test")
        paths = expand_globs(args.summaries)
        if not paths:
            raise ValueError(f"No files found matching: {args.summaries}")
        summaries = []
        for p in paths:
            with open(p, encoding="utf-8") as f:
                summaries.append(json.load(f))

    # Sort by year
    summaries.sort(key=lambda s: s["year"])

    years = [s["year"] for s in summaries]
    i_values = [s["moran_i"] for s in summaries]
    p_values = [s["p_value_two_sided"] for s in summaries]
    trend_slope = compute_trend(years, i_values)

    output_summary = {
        "method": "Multi_Year_Moran",
        "n_years": len(years),
        "years": years,
        "i_values": [round(v, 4) for v in i_values],
        "p_values": [round(v, 4) for v in p_values],
        "trend_slope": round(trend_slope, 6),
    }

    summary_path = out_dir / "multi_year_summary.json"
    summary_path.write_text(json.dumps(output_summary, indent=2), encoding="utf-8")
    print(f"Summary: {summary_path}")

    try:
        plot_df = pd.DataFrame({
            "year": years,
            "moran_i": i_values,
            "p_value": p_values,
        })
        plot_multi_year(plot_df, out_dir / "multi_year_moran.pdf")
    except ImportError:
        print("plotnine not installed — skipping figure generation")


if __name__ == "__main__":
    main()
