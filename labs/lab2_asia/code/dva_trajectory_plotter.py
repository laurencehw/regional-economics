"""Plot DVA ratio time series by economy (the figure Ch. 6 promises).

Smoke-test mode generates a synthetic 6-country panel with known trajectories.
Real mode reads the existing panel_mapped.csv.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

SUBGROUPS = {
    "NE Asia Core": ["CHN", "JPN", "KOR"],
    "ASEAN-6": ["IDN", "MYS", "PHL", "SGP", "THA", "VNM"],
    "South Asia": ["IND"],
}
SUBGROUP_COLORS = {
    "NE Asia Core": "#e41a1c",
    "ASEAN-6": "#377eb8",
    "South Asia": "#4daf4a",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot DVA ratio trajectories")
    parser.add_argument("--panel", type=str, default=None, help="Path to panel_mapped.csv")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def assign_subgroup(country: str) -> str:
    for group, members in SUBGROUPS.items():
        if country in members:
            return group
    return "Other"


def synthetic_panel(seed: int = 42) -> pd.DataFrame:
    """Synthetic 6-country panel with rising/flat/declining trajectories."""
    rng = np.random.default_rng(seed)
    years = list(range(2005, 2023))
    configs = {
        "VNM": {"base": 1.0, "trend": 0.04},   # rising
        "CHN": {"base": 1.5, "trend": 0.02},   # rising
        "KOR": {"base": 2.0, "trend": 0.005},  # flat
        "JPN": {"base": 2.2, "trend": -0.005}, # flat/declining
        "THA": {"base": 1.3, "trend": 0.03},   # rising
        "IND": {"base": 0.9, "trend": 0.025},  # rising
    }
    rows: List[Dict] = []
    for eco, cfg in configs.items():
        val = cfg["base"]
        for yr in years:
            noise = rng.normal(0, 0.02)
            val *= 1.0 + cfg["trend"] + noise
            rows.append({"country": eco, "year": yr, "dva_ratio": round(val, 4)})
    return pd.DataFrame(rows)


def compute_trend_slopes(df: pd.DataFrame) -> Dict[str, float]:
    """OLS slope of dva_ratio on year for each economy."""
    slopes = {}
    for eco, grp in df.groupby("country"):
        x = grp["year"].values.astype(float)
        y = grp["dva_ratio"].values.astype(float)
        mask = np.isfinite(x) & np.isfinite(y)
        if mask.sum() < 2:
            continue
        x, y = x[mask], y[mask]
        x_dm = x - x.mean()
        slopes[eco] = float(np.dot(x_dm, y) / np.dot(x_dm, x_dm))
    return slopes


def plot_trajectories(df: pd.DataFrame, output_path: Path) -> None:
    from plotnine import (
        aes, geom_line, ggplot, labs, scale_color_manual,
        theme, element_text, element_blank,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    df = df.copy()
    df["subgroup"] = df["country"].apply(assign_subgroup)

    p = (
        ggplot(df, aes(x="year", y="dva_ratio", color="subgroup", group="country"))
        + geom_line(size=0.8, alpha=0.85)
        + scale_color_manual(values=SUBGROUP_COLORS)
        + labs(
            x="Year",
            y="DVA / FNL Ratio",
            title="Domestic Value-Added Trajectories in Asia",
            color="Subgroup",
        )
        + base_theme
        + theme(
            figure_size=(6, 4),
            legend_position="bottom",
            plot_title=element_text(size=11),
        )
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
        if not args.panel:
            raise ValueError("Provide --panel or use --run-smoke-test")
        df = pd.read_csv(args.panel)
        if "dva_ratio" not in df.columns:
            raise ValueError("Panel must contain 'dva_ratio' column")

    slopes = compute_trend_slopes(df)

    # Classify trajectories
    upgraders = [e for e, s in slopes.items() if s > 0.01]
    stable = [e for e, s in slopes.items() if -0.01 <= s <= 0.01]
    decliners = [e for e, s in slopes.items() if s < -0.01]

    summary = {
        "method": "DVA_Trajectory_Analysis",
        "n_countries": int(df["country"].nunique()),
        "n_years": int(df["year"].nunique()),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "trend_slopes": {k: round(v, 6) for k, v in sorted(slopes.items())},
        "upgraders": sorted(upgraders),
        "stable": sorted(stable),
        "decliners": sorted(decliners),
        "smoke_test": args.run_smoke_test,
    }
    summary_path = out_dir / "trajectory_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    try:
        plot_trajectories(df, out_dir / "dva_trajectories.pdf")
    except ImportError:
        print("plotnine not installed — skipping trajectory figure")

    print(f"Summary: {summary_path}")
    print(f"Economies: {list(slopes.keys())}")


if __name__ == "__main__":
    main()
