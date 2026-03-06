"""Chapter 6 figures: East Asia map + DVA trajectory thematic.

Map: Japan–Korea–Taiwan–ASEAN; tech corridors, SEZs.
Thematic: DVA trajectory by economy (Lab 2 output pattern).
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
    REGION_COLORS, QUAL_PALETTE, add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, setup_map_ax, load_annotations,
    annotate_cities, annotate_corridors, project_cities, project_corridors,
)


def plot_east_asia_map(output_dir: Path, seed: int = 42) -> dict:
    """East Asia and ASEAN: tech corridors, SEZs, key cities."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch06_map_east_asia")

    world = get_country_boundaries()
    ea_iso = ISO3_SETS["east_asia"]
    ea = world[world["iso3"].isin(ea_iso)]
    context = world[world["iso3"].isin(["IND", "BGD", "RUS"])]

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        ea_proj = ea.to_crs(PROJECTIONS["east_asia"])
        ctx_proj = context.to_crs(PROJECTIONS["east_asia"])
    except Exception:
        ea_proj, ctx_proj = ea, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    ea_proj.plot(ax=ax, color="#fde0c5", edgecolor=BORDER_COLOR, linewidth=0.5)

    # Zoom to focus countries with buffer
    xmin, ymin, xmax, ymax = ea_proj.total_bounds
    dx, dy = (xmax - xmin) * 0.08, (ymax - ymin) * 0.08
    setup_map_ax(ax, "East Asia & ASEAN: Technology Corridors and SEZs",
                 bbox=(xmin - dx, ymin - dy, xmax + dx, ymax + dy))

    ann = load_annotations("ch06")
    crs = PROJECTIONS["east_asia"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))
    if ann.get("corridors"):
        annotate_corridors(ax, project_corridors(ann["corridors"], crs))

    add_figure_source(fig, "Natural Earth; ASEAN Secretariat; national SEZ databases.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch06_map_east_asia")
    plt.close(fig)
    return {"figure": "fig_ch06_map_east_asia", "type": "map", **paths}


def plot_dva_trajectory(output_dir: Path, seed: int = 42) -> dict:
    """DVA (domestic value added) share trajectory by economy."""
    rng = np.random.default_rng(seed)
    years = np.arange(2000, 2021)

    economies = {
        "China":     (55, 72, 0.8),
        "Japan":     (82, 85, 0.3),
        "Korea":     (58, 68, 0.5),
        "Vietnam":   (35, 50, 0.7),
        "Thailand":  (52, 60, 0.4),
        "Malaysia":  (45, 55, 0.5),
    }

    fig, ax = plt.subplots(figsize=FIGSIZE_THEMATIC)
    for i, (eco, (start, end, noise)) in enumerate(economies.items()):
        dva = np.linspace(start, end, len(years)) + rng.normal(0, noise, len(years))
        ax.plot(years, dva, color=QUAL_PALETTE[i], linewidth=1.5, label=eco)

    ax.set_xlabel("Year", fontsize=8)
    ax.set_ylabel("DVA share of gross exports (%)", fontsize=8)
    ax.set_title("Domestic Value Added in Exports: East Asian Economies",
                 fontsize=9, fontweight="bold")
    ax.legend(fontsize=6.5, ncol=2, loc="lower right", frameon=False)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(1999, 2021)
    ax.set_ylim(30, 95)

    add_figure_source(fig, "OECD TiVA database. Illustrative; based on patterns in OECD TiVA data, not exact reproduction.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch06_thematic_dva_trajectory")
    plt.close(fig)
    return {"figure": "fig_ch06_thematic_dva_trajectory", "type": "thematic", **paths}


def _placeholder(output_dir, stem):
    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    ax.set_facecolor(WATER_COLOR)
    ax.text(0.5, 0.5, f"[{stem}]\ngeopandas required",
            ha="center", va="center", fontsize=9, color="#808080",
            transform=ax.transAxes)
    ax.axis("off")
    fig.tight_layout()
    paths = save_figure(fig, output_dir, stem)
    plt.close(fig)
    return {"figure": stem, "type": "map_placeholder", **paths}


def main():
    parser = argparse.ArgumentParser(description="Chapter 6 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = []
    summaries.append(plot_east_asia_map(output_dir, args.seed))
    summaries.append(plot_dva_trajectory(output_dir, args.seed))

    combined = {"chapter": 6, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch06_figures", combined)
    print("Chapter 6 figures complete.")


if __name__ == "__main__":
    main()
