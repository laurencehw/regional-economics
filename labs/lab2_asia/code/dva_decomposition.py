"""Simplified DVA decomposition using TiVA pre-computed indicators.

DVA_share = dva_value / (dva_value + fnl_value)
Ranks economies, computes trends, identifies upgraders/downgraders.

Smoke-test mode generates a calibrated synthetic cross section.
Real mode reads existing DVA and FNL CSVs from data/raw/tiva/.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

ECONOMIES = ["CHN", "JPN", "KOR", "IND", "IDN", "VNM", "THA", "MYS", "PHL", "SGP"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DVA/FVA decomposition from TiVA")
    parser.add_argument("--dva-csv", type=str, default=None, help="TiVA DVA extract CSV")
    parser.add_argument("--fnl-csv", type=str, default=None, help="TiVA FNL extract CSV")
    parser.add_argument("--panel", type=str, default=None, help="Pre-built panel_mapped.csv (alternative)")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_decomposition(seed: int = 42) -> pd.DataFrame:
    """Calibrated synthetic DVA/FVA shares for 10 Asian economies."""
    rng = np.random.default_rng(seed)
    years = [2005, 2010, 2015, 2020]
    # Base DVA shares: Japan/Korea high domestic content, Vietnam/PHL more foreign content
    base_shares = {
        "JPN": 0.82, "KOR": 0.68, "CHN": 0.72,
        "IND": 0.78, "IDN": 0.70, "SGP": 0.52,
        "MYS": 0.55, "THA": 0.58, "VNM": 0.42, "PHL": 0.48,
    }
    trend = {
        "JPN": -0.002, "KOR": 0.003, "CHN": 0.005,
        "IND": 0.003, "IDN": 0.002, "SGP": 0.001,
        "MYS": 0.004, "THA": 0.003, "VNM": 0.008, "PHL": 0.003,
    }
    rows: List[Dict] = []
    for eco in ECONOMIES:
        for yr in years:
            dt = yr - 2005
            share = np.clip(
                base_shares[eco] + trend[eco] * dt + rng.normal(0, 0.01),
                0.1, 0.95,
            )
            total = rng.uniform(50_000, 500_000)
            dva_val = total * share
            fnl_val = total * (1 - share)
            rows.append({
                "country": eco, "year": yr,
                "dva_value": round(dva_val, 2),
                "fnl_value": round(fnl_val, 2),
            })
    return pd.DataFrame(rows)


def load_from_raw_tiva(dva_path: str, fnl_path: str) -> pd.DataFrame:
    """Load and merge raw TiVA DVA and FNL extracts into a panel."""
    dva = pd.read_csv(dva_path)
    fnl = pd.read_csv(fnl_path)

    dva = dva.rename(columns={"REF_AREA": "country", "TIME_PERIOD": "year", "OBS_VALUE": "dva_value"})
    fnl = fnl.rename(columns={"REF_AREA": "country", "TIME_PERIOD": "year", "OBS_VALUE": "fnl_value"})

    dva = dva[["country", "year", "dva_value"]].copy()
    fnl = fnl[["country", "year", "fnl_value"]].copy()

    # Aggregate if multiple activities/counterparts
    dva = dva.groupby(["country", "year"], as_index=False)["dva_value"].sum()
    fnl = fnl.groupby(["country", "year"], as_index=False)["fnl_value"].sum()

    panel = dva.merge(fnl, on=["country", "year"], how="inner")
    return panel


def compute_decomposition(df: pd.DataFrame) -> pd.DataFrame:
    """Compute DVA share, rankings, and trends."""
    df = df.copy()
    total = df["dva_value"] + df["fnl_value"]
    df["dva_share"] = np.where(total > 0, df["dva_value"] / total, np.nan)
    df["fva_share"] = 1.0 - df["dva_share"]
    df["dva_share"] = df["dva_share"].clip(0, 1)
    df["fva_share"] = df["fva_share"].clip(0, 1)

    # Rank within each year
    df["rank_in_year"] = df.groupby("year")["dva_share"].rank(ascending=False, method="min").astype(int)
    return df


def compute_trends(df: pd.DataFrame) -> Dict[str, Dict]:
    """OLS slope of dva_share on year for each economy."""
    results = {}
    for eco, grp in df.groupby("country"):
        x = grp["year"].values.astype(float)
        y = grp["dva_share"].values.astype(float)
        mask = np.isfinite(x) & np.isfinite(y)
        if mask.sum() < 2:
            continue
        x, y = x[mask], y[mask]
        x_dm = x - x.mean()
        slope = float(np.dot(x_dm, y) / np.dot(x_dm, x_dm))
        mean_share = float(y.mean())
        results[eco] = {"slope": round(slope, 6), "mean_dva_share": round(mean_share, 4)}
    return results


def plot_decomposition(df: pd.DataFrame, output_path: Path, year: int | None = None) -> None:
    from plotnine import (
        aes, geom_col, ggplot, labs, coord_flip,
        scale_fill_manual, theme, element_text, position_stack,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    if year is not None:
        plot_df = df[df["year"] == year].copy()
    else:
        latest = df["year"].max()
        plot_df = df[df["year"] == latest].copy()

    plot_df = plot_df.sort_values("dva_share", ascending=True)
    plot_df["country"] = pd.Categorical(plot_df["country"], categories=plot_df["country"].tolist(), ordered=True)

    long = plot_df.melt(
        id_vars=["country", "year"],
        value_vars=["dva_share", "fva_share"],
        var_name="component",
        value_name="share",
    )
    long["component"] = long["component"].map({"dva_share": "DVA", "fva_share": "FVA"})

    p = (
        ggplot(long, aes(x="country", y="share", fill="component"))
        + geom_col(position=position_stack(), width=0.7)
        + coord_flip()
        + scale_fill_manual(values={"DVA": "#2166ac", "FVA": "#b2182b"})
        + labs(
            x="", y="Share of Gross Exports",
            title=f"DVA vs FVA Decomposition ({int(plot_df['year'].iloc[0])})",
            fill="Component",
        )
        + base_theme
        + theme(
            figure_size=(6, 4),
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
        df = synthetic_decomposition(seed=args.seed)
    elif args.panel:
        df = pd.read_csv(args.panel)
    elif args.dva_csv and args.fnl_csv:
        df = load_from_raw_tiva(args.dva_csv, args.fnl_csv)
    else:
        raise ValueError("Provide --panel, --dva-csv + --fnl-csv, or use --run-smoke-test")

    df = compute_decomposition(df)
    trends = compute_trends(df)

    upgraders = [e for e, t in trends.items() if t["slope"] > 0.001]
    downgraders = [e for e, t in trends.items() if t["slope"] < -0.001]
    stable = [e for e, t in trends.items() if -0.001 <= t["slope"] <= 0.001]

    summary = {
        "method": "TiVA_DVA_Decomposition",
        "n_countries": int(df["country"].nunique()),
        "n_years": int(df["year"].nunique()),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "economy_trends": {k: v for k, v in sorted(trends.items())},
        "upgraders": sorted(upgraders),
        "downgraders": sorted(downgraders),
        "stable": sorted(stable),
        "dva_share_range": [round(float(df["dva_share"].min()), 4),
                           round(float(df["dva_share"].max()), 4)],
        "smoke_test": args.run_smoke_test,
    }

    csv_path = out_dir / "dva_decomposition.csv"
    df.to_csv(csv_path, index=False)

    summary_path = out_dir / "decomposition_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    try:
        plot_decomposition(df, out_dir / "dva_decomposition.pdf")
    except ImportError:
        print("plotnine not installed — skipping decomposition figure")

    print(f"CSV: {csv_path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
