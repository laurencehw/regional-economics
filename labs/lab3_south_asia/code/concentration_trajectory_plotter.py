"""Plot IT-share concentration trajectories by Indian state over time.

Smoke-test mode generates a synthetic 12-state panel with known trends.
Real mode reads the existing panel_mapped.csv.

Outputs:
- concentration_trajectories.pdf  (line plot, one line per region, colored by tier)
- trajectory_summary.json         (trend slopes, tier assignments, metadata)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Tier definitions (for colour coding)
# ---------------------------------------------------------------------------

TIER_MEMBERS = {
    "Tier 1": ["Karnataka", "Maharashtra", "Telangana"],
    "Tier 2": ["Tamil Nadu", "Delhi NCR", "Gujarat"],
}
TIER_COLORS = {
    "Tier 1": "#e41a1c",   # red
    "Tier 2": "#377eb8",   # blue
    "Other": "#999999",    # gray
}


def assign_tier(region: str) -> str:
    """Assign a region to its display tier."""
    for tier, members in TIER_MEMBERS.items():
        if region in members:
            return tier
    return "Other"


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot IT-share concentration trajectories for South Asia"
    )
    parser.add_argument(
        "--panel", type=str, default=None, help="Path to panel_mapped.csv"
    )
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Synthetic panel for smoke testing
# ---------------------------------------------------------------------------

def synthetic_panel(seed: int = 42) -> pd.DataFrame:
    """Synthetic 12-state panel with rising/flat/declining IT-share trajectories."""
    rng = np.random.default_rng(seed)
    years = list(range(2010, 2019))

    configs = {
        "Karnataka":      {"base_share": 0.20, "trend": 0.012},
        "Telangana":      {"base_share": 0.17, "trend": 0.010},
        "Maharashtra":    {"base_share": 0.05, "trend": 0.003},
        "Tamil Nadu":     {"base_share": 0.04, "trend": 0.004},
        "Delhi NCR":      {"base_share": 0.06, "trend": 0.002},
        "Gujarat":        {"base_share": 0.015, "trend": 0.001},
        "Kerala":         {"base_share": 0.03, "trend": 0.002},
        "Andhra Pradesh": {"base_share": 0.025, "trend": 0.001},
        "Uttar Pradesh":  {"base_share": 0.004, "trend": 0.0005},
        "West Bengal":    {"base_share": 0.013, "trend": 0.001},
        "Rajasthan":      {"base_share": 0.005, "trend": -0.0002},
        "Bihar":          {"base_share": 0.001, "trend": 0.0001},
    }

    rows: List[Dict] = []
    for region, cfg in configs.items():
        share = cfg["base_share"]
        for yr in years:
            noise = rng.normal(0, 0.001)
            share = max(share + cfg["trend"] + noise, 0.0)
            total_gdp = rng.uniform(3000, 18000)
            it_va = share * total_gdp
            rows.append({
                "region": region,
                "year": yr,
                "it_va": round(it_va, 2),
                "total_gdp": round(total_gdp, 2),
                "it_share": round(share, 6),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# HHI computation (national-level concentration by year)
# ---------------------------------------------------------------------------

def compute_hhi_by_year(df: pd.DataFrame) -> List[Dict[str, object]]:
    """Compute national HHI of IT value-added across regions, per year."""
    results = []
    for year, grp in df.groupby("year"):
        it_va = grp["it_va"].to_numpy(dtype=float)
        total = it_va.sum()
        if total > 0:
            shares = it_va / total
            hhi = float(np.sum(shares ** 2))
        else:
            hhi = 0.0
        results.append({"year": int(year), "hhi": round(hhi, 6), "n_regions": len(grp)})
    return sorted(results, key=lambda x: x["year"])


# ---------------------------------------------------------------------------
# Trend slopes (OLS of metric on year)
# ---------------------------------------------------------------------------

def compute_trend_slopes(df: pd.DataFrame) -> Dict[str, float]:
    """OLS slope of it_share on year for each region."""
    slopes: Dict[str, float] = {}
    for region, grp in df.groupby("region"):
        x = grp["year"].values.astype(float)
        y = grp["it_share"].values.astype(float)
        mask = np.isfinite(x) & np.isfinite(y)
        if mask.sum() < 2:
            continue
        x, y = x[mask], y[mask]
        x_dm = x - x.mean()
        denom = np.dot(x_dm, x_dm)
        if denom > 0:
            slopes[str(region)] = float(np.dot(x_dm, y) / denom)
    return slopes


# ---------------------------------------------------------------------------
# Plotting — plotnine with matplotlib fallback (Lab 2 pattern)
# ---------------------------------------------------------------------------

def plot_trajectories_plotnine(df: pd.DataFrame, output_path: Path) -> None:
    """Plot using plotnine (ggplot2 style), matching Lab 2 pattern."""
    from plotnine import (
        aes, geom_line, ggplot, labs, scale_color_manual,
        theme, element_text,
    )
    try:
        from hrbrthemes import theme_ipsum
        base_theme = theme_ipsum()
    except ImportError:
        from plotnine import theme_minimal
        base_theme = theme_minimal()

    plot_df = df.copy()
    plot_df["tier"] = plot_df["region"].apply(assign_tier)
    plot_df["it_share_pct"] = plot_df["it_share"] * 100.0

    p = (
        ggplot(plot_df, aes(x="year", y="it_share_pct", color="tier", group="region"))
        + geom_line(size=0.8, alpha=0.85)
        + scale_color_manual(values=TIER_COLORS)
        + labs(
            x="Year",
            y="IT Share of GDP (%)",
            title="IT-Sector Concentration Trajectories across Indian States",
            color="Tier",
        )
        + base_theme
        + theme(
            figure_size=(8, 5),
            legend_position="bottom",
            plot_title=element_text(size=11),
        )
    )
    p.save(str(output_path), dpi=300)
    print(f"Figure saved (plotnine): {output_path}")


def plot_trajectories_matplotlib(df: pd.DataFrame, output_path: Path) -> None:
    """Fallback: plot using matplotlib directly."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plot_df = df.copy()
    plot_df["tier"] = plot_df["region"].apply(assign_tier)
    plot_df["it_share_pct"] = plot_df["it_share"] * 100.0

    fig, ax = plt.subplots(figsize=(8, 5))

    # Draw Other tier first (background), then Tier 2, then Tier 1
    for tier_name in ["Other", "Tier 2", "Tier 1"]:
        tier_df = plot_df.loc[plot_df["tier"] == tier_name]
        color = TIER_COLORS[tier_name]
        for region, grp in tier_df.groupby("region"):
            grp = grp.sort_values("year")
            alpha = 0.4 if tier_name == "Other" else 0.85
            lw = 1.0 if tier_name == "Other" else 1.5
            ax.plot(
                grp["year"], grp["it_share_pct"],
                color=color, alpha=alpha, linewidth=lw, label=None,
            )

    # Legend: one entry per tier
    from matplotlib.lines import Line2D
    legend_handles = [
        Line2D([0], [0], color=TIER_COLORS["Tier 1"], lw=1.5, label="Tier 1"),
        Line2D([0], [0], color=TIER_COLORS["Tier 2"], lw=1.5, label="Tier 2"),
        Line2D([0], [0], color=TIER_COLORS["Other"], lw=1.0, alpha=0.4, label="Other"),
    ]
    ax.legend(handles=legend_handles, loc="upper left", frameon=False)

    ax.set_xlabel("Year")
    ax.set_ylabel("IT Share of GDP (%)")
    ax.set_title("IT-Sector Concentration Trajectories across Indian States", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(str(output_path), dpi=300)
    plt.close(fig)
    print(f"Figure saved (matplotlib): {output_path}")


def plot_trajectories(df: pd.DataFrame, output_path: Path) -> None:
    """Try plotnine; fall back to matplotlib if unavailable."""
    try:
        plot_trajectories_plotnine(df, output_path)
    except ImportError:
        print("plotnine not installed — falling back to matplotlib")
        plot_trajectories_matplotlib(df, output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load or generate panel
    if args.run_smoke_test:
        df = synthetic_panel(seed=args.seed)
        print("Running in smoke-test mode with synthetic 12-state panel.")
    else:
        if not args.panel:
            raise ValueError("Provide --panel or use --run-smoke-test")
        df = pd.read_csv(args.panel)
        # Ensure required columns exist
        for col in ("region", "year", "it_va", "total_gdp"):
            if col not in df.columns:
                raise ValueError(f"Panel must contain '{col}' column")
        # Derive it_share if missing
        if "it_share" not in df.columns:
            df = df.assign(
                it_share=np.where(
                    df["total_gdp"] > 0, df["it_va"] / df["total_gdp"], 0.0
                )
            )

    # Compute national-level HHI by year
    hhi_series = compute_hhi_by_year(df)

    # Compute trend slopes per region
    slopes = compute_trend_slopes(df)

    # Classify trajectories
    rising = [r for r, s in slopes.items() if s > 0.001]
    stable = [r for r, s in slopes.items() if -0.001 <= s <= 0.001]
    declining = [r for r, s in slopes.items() if s < -0.001]

    summary = {
        "method": "IT_Concentration_Trajectory_Analysis",
        "n_regions": int(df["region"].nunique()),
        "n_years": int(df["year"].nunique()),
        "year_range": [int(df["year"].min()), int(df["year"].max())],
        "trend_slopes": {k: round(v, 6) for k, v in sorted(slopes.items())},
        "rising": sorted(rising),
        "stable": sorted(stable),
        "declining": sorted(declining),
        "hhi_by_year": hhi_series,
        "tier_assignments": {
            region: assign_tier(region) for region in sorted(df["region"].unique())
        },
        "smoke_test": args.run_smoke_test,
    }
    summary_path = out_dir / "trajectory_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Generate figure
    try:
        plot_trajectories(df, out_dir / "concentration_trajectories.pdf")
    except Exception as exc:
        print(f"Could not generate figure: {exc}")

    print(f"Summary: {summary_path}")
    print(f"Regions: {sorted(slopes.keys())}")


if __name__ == "__main__":
    main()
