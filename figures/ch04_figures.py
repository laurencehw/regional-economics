"""Chapter 4 figures: North America map + manufacturing shift thematic.

Map: USMCA countries, Rust Belt/Sun Belt shading, maquiladora zones, corridors.
Thematic: Manufacturing employment share — Rust Belt vs Sun Belt over time.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figure_utils import (
    FIGSIZE_MAP, FIGSIZE_THEMATIC, LAND_COLOR, WATER_COLOR, BORDER_COLOR,
    REGION_COLORS, add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, setup_map_ax, load_annotations,
    annotate_cities, annotate_corridors, project_cities, project_corridors,
)


# ------------------------------------------------------------------ #
#  Figure 7: North America map
# ------------------------------------------------------------------ #

def plot_north_america_map(output_dir: Path, seed: int = 42) -> dict:
    """USMCA countries with Rust Belt / Sun Belt shading and trade corridors."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _synthetic_map(output_dir, "fig_ch04_map_north_america")

    world = get_country_boundaries()
    na_iso = ["USA", "CAN", "MEX"]
    na = world[world["iso3"].isin(na_iso)]
    context = world[world["iso3"].isin(
        ["GTM", "BLZ", "HND", "CUB", "JAM", "HTI", "DOM"]
    )]

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        na_proj = na.to_crs(PROJECTIONS["americas"])
        ctx_proj = context.to_crs(PROJECTIONS["americas"])
    except Exception:
        na_proj, ctx_proj = na, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    na_proj.plot(ax=ax, color="#d4e6f1", edgecolor=BORDER_COLOR, linewidth=0.5)

    setup_map_ax(ax, "North America: USMCA, Industrial Belts & Trade Corridors")

    ann = load_annotations("ch04")
    crs = PROJECTIONS["americas"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))
    if ann.get("corridors"):
        annotate_corridors(ax, project_corridors(ann["corridors"], crs))

    add_figure_source(fig, "Natural Earth; BTS cross-border flow data.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch04_map_north_america")
    plt.close(fig)
    return {"figure": "fig_ch04_map_north_america", "type": "map", **paths}


# ------------------------------------------------------------------ #
#  Figure 8: Manufacturing employment shift — Rust Belt vs Sun Belt
# ------------------------------------------------------------------ #

def plot_manufacturing_shift(output_dir: Path, seed: int = 42) -> dict:
    """Line chart: manufacturing employment share, Rust Belt vs Sun Belt."""
    rng = np.random.default_rng(seed)
    years = np.arange(1970, 2025, 5)

    # Calibrated synthetic series
    rust_belt = np.array([28, 25, 21, 17, 14, 12, 10, 9, 8, 7.5, 7.2])
    sun_belt = np.array([12, 13, 14, 15, 14.5, 14, 13.5, 13, 12.5, 12, 11.5])
    rust_belt += rng.normal(0, 0.3, len(years))
    sun_belt += rng.normal(0, 0.2, len(years))

    fig, ax = plt.subplots(figsize=FIGSIZE_THEMATIC)
    ax.plot(years, rust_belt, "o-", color="#d62728", linewidth=1.8,
            markersize=4, label="Rust Belt")
    ax.plot(years, sun_belt, "s-", color="#ff7f0e", linewidth=1.8,
            markersize=4, label="Sun Belt")

    ax.fill_between(years, rust_belt, sun_belt, alpha=0.08, color="#808080")
    ax.axvline(1994, color="#808080", linestyle=":", linewidth=0.8, alpha=0.6)
    ax.text(1994.5, 26, "NAFTA\n(1994)", fontsize=6, color="#808080")

    ax.set_xlabel("Year", fontsize=8)
    ax.set_ylabel("Manufacturing employment share (%)", fontsize=8)
    ax.set_title("Manufacturing Shift: Rust Belt vs. Sun Belt",
                 fontsize=9, fontweight="bold")
    ax.legend(fontsize=7, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(1968, 2026)

    add_figure_source(fig, "BLS Current Employment Statistics; calibrated illustration.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch04_thematic_manufacturing_shift")
    plt.close(fig)
    return {"figure": "fig_ch04_thematic_manufacturing_shift", "type": "thematic", **paths}


def _synthetic_map(output_dir, stem):
    """Fallback: text-only placeholder if geopandas unavailable."""
    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    ax.set_facecolor(WATER_COLOR)
    ax.text(0.5, 0.5, f"[{stem}]\ngeopandas required for map rendering",
            ha="center", va="center", fontsize=9, color="#808080",
            transform=ax.transAxes)
    ax.axis("off")
    fig.tight_layout()
    paths = save_figure(fig, output_dir, stem)
    plt.close(fig)
    return {"figure": stem, "type": "map_placeholder", **paths}


def main():
    parser = argparse.ArgumentParser(description="Chapter 4 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = []
    summaries.append(plot_north_america_map(output_dir, args.seed))
    summaries.append(plot_manufacturing_shift(output_dir, args.seed))

    combined = {"chapter": 4, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch04_figures", combined)
    print("Chapter 4 figures complete.")


if __name__ == "__main__":
    main()
