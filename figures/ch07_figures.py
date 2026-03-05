"""Chapter 7 figures: China-ASEAN map + provincial divergence thematic.

Map: China provinces (coastal vs inland), ASEAN corridors, BRI nodes.
Thematic: Coastal vs inland GDP per capita divergence.
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


def plot_china_asean_map(output_dir: Path, seed: int = 42) -> dict:
    """China provinces + ASEAN economic corridors + BRI nodes."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch07_map_china_asean")

    world = get_country_boundaries()
    asean = ["IDN", "MYS", "THA", "VNM", "PHL", "MMR", "KHM", "LAO", "BRN", "SGP"]
    focus = world[world["iso3"].isin(["CHN"] + asean)]
    context = world[world["iso3"].isin(["IND", "JPN", "KOR", "TWN", "RUS"])]

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        focus_proj = focus.to_crs(PROJECTIONS["east_asia"])
        ctx_proj = context.to_crs(PROJECTIONS["east_asia"])
    except Exception:
        focus_proj, ctx_proj = focus, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    # China in a distinct shade
    china = focus_proj[focus_proj["iso3"] == "CHN"]
    others = focus_proj[focus_proj["iso3"] != "CHN"]
    china.plot(ax=ax, color="#fbb4ae", edgecolor=BORDER_COLOR, linewidth=0.5)
    others.plot(ax=ax, color="#b3cde3", edgecolor=BORDER_COLOR, linewidth=0.5)

    # Zoom to focus countries with buffer
    xmin, ymin, xmax, ymax = focus_proj.total_bounds
    dx, dy = (xmax - xmin) * 0.08, (ymax - ymin) * 0.08
    setup_map_ax(ax, "China & ASEAN: BRI Corridors and Economic Integration",
                 bbox=(xmin - dx, ymin - dy, xmax + dx, ymax + dy))

    ann = load_annotations("ch07")
    crs = PROJECTIONS["east_asia"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))
    if ann.get("corridors"):
        annotate_corridors(ax, project_corridors(ann["corridors"], crs))

    add_figure_source(fig, "Natural Earth; BRI official project list.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch07_map_china_asean")
    plt.close(fig)
    return {"figure": "fig_ch07_map_china_asean", "type": "map", **paths}


def plot_provincial_divergence(output_dir: Path, seed: int = 42) -> dict:
    """Coastal vs inland GDP per capita divergence (slope chart)."""
    rng = np.random.default_rng(seed)

    years = [2000, 2005, 2010, 2015, 2020]
    coastal = [12500, 19000, 32000, 48000, 68000]
    inland = [5000, 7500, 13000, 20000, 30000]
    # Add small noise
    coastal = [v + rng.normal(0, 300) for v in coastal]
    inland = [v + rng.normal(0, 200) for v in inland]

    fig, ax = plt.subplots(figsize=FIGSIZE_THEMATIC)
    ax.plot(years, coastal, "o-", color="#e41a1c", linewidth=2, markersize=5,
            label="Coastal provinces")
    ax.plot(years, inland, "s-", color="#377eb8", linewidth=2, markersize=5,
            label="Inland provinces")

    ax.fill_between(years, coastal, inland, alpha=0.08, color="#808080")

    # Ratio annotation
    for i, yr in enumerate(years):
        ratio = coastal[i] / inland[i]
        ax.text(yr, coastal[i] + 1500, f"{ratio:.1f}×", fontsize=5.5,
                ha="center", color="#808080")

    ax.set_xlabel("Year", fontsize=8)
    ax.set_ylabel("GDP per capita (CNY)", fontsize=8)
    ax.set_title("China Provincial Divergence: Coastal vs. Inland",
                 fontsize=9, fontweight="bold")
    ax.legend(fontsize=7, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    add_figure_source(fig, "NBS China Statistical Yearbook; calibrated illustration.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch07_thematic_provincial_divergence")
    plt.close(fig)
    return {"figure": "fig_ch07_thematic_provincial_divergence", "type": "thematic", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 7 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = []
    summaries.append(plot_china_asean_map(output_dir, args.seed))
    summaries.append(plot_provincial_divergence(output_dir, args.seed))

    combined = {"chapter": 7, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch07_figures", combined)
    print("Chapter 7 figures complete.")


if __name__ == "__main__":
    main()
