"""Chapter 14 figure: AfCFTA trade corridors map.

Northern, Trans-Kalahari, Maputo, Abidjan-Lagos corridors; major ports.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figure_utils import (
    FIGSIZE_MAP, FIGSIZE_WIDE, LAND_COLOR, WATER_COLOR, BORDER_COLOR,
    REGION_COLORS, QUAL_PALETTE,
    add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, setup_map_ax, load_annotations,
    annotate_cities, annotate_corridors, project_cities, project_corridors,
)


def plot_afcfta_corridors_map(output_dir: Path, seed: int = 42) -> dict:
    """SSA with AfCFTA trade corridors and major ports."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch14_map_afcfta_corridors")

    world = get_country_boundaries()
    ssa_iso = ISO3_SETS["ssa"]
    ssa = world[world["iso3"].isin(ssa_iso)]
    context = world[world["iso3"].isin(["MAR", "DZA", "LBY", "EGY", "TUN"])]

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        ssa_proj = ssa.to_crs(PROJECTIONS["africa"])
        ctx_proj = context.to_crs(PROJECTIONS["africa"])
    except Exception:
        ssa_proj, ctx_proj = ssa, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    ssa_proj.plot(ax=ax, color="#d4e6f1", edgecolor=BORDER_COLOR, linewidth=0.5)

    setup_map_ax(ax, "AfCFTA Trade Corridors and Major Ports")

    ann = load_annotations("ch14")
    crs = PROJECTIONS["africa"]
    if ann.get("cities"):
        # Port cities as anchor markers
        for city in project_cities(ann["cities"], crs):
            ax.scatter(city["lon"], city["lat"], s=40, c="#377eb8",
                       marker="s", edgecolors="#333333", linewidths=0.5, zorder=5)
            dx, dy = city.get("label_offset", [5, 3])
            ax.annotate(city["name"], (city["lon"], city["lat"]),
                        fontsize=5.5, ha="left", va="bottom",
                        xytext=(dx, dy), textcoords="offset points",
                        zorder=6)
    if ann.get("corridors"):
        annotate_corridors(ax, project_corridors(ann["corridors"], crs))

    add_figure_source(fig, "Natural Earth; AfCFTA Secretariat; UNECA corridor database.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch14_map_afcfta_corridors")
    plt.close(fig)
    return {"figure": "fig_ch14_map_afcfta_corridors", "type": "map", **paths}


# ------------------------------------------------------------------ #
#  Figure: Intra-regional trade shares by trading bloc
# ------------------------------------------------------------------ #

def plot_intra_africa_trade_bar(output_dir: Path, seed: int = 42) -> dict:
    """Bar chart of intra-regional trade shares for major blocs."""
    blocs = ["EU", "NAFTA/USMCA", "ASEAN", "Mercosur", "AfCFTA"]
    shares = [60, 40, 25, 15, 15]

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    colors = QUAL_PALETTE[:len(blocs)]
    x_pos = np.arange(len(blocs))
    bars = ax.bar(x_pos, shares, color=colors, edgecolor="white", linewidth=0.5,
                  width=0.6)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(blocs, fontsize=8)
    ax.set_ylabel("Intra-regional trade share (%)", fontsize=8)
    ax.set_title("Intra-Regional Trade Shares: Africa in Comparative Perspective",
                 fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 75)

    # Value labels on bars
    for bar, val in zip(bars, shares):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{val}%", ha="center", va="bottom", fontsize=7.5, fontweight="bold")

    add_figure_source(fig, "UNCTAD (2023); AfCFTA Secretariat; WTO Regional Trade Agreements database.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch14_chart_intra_africa_trade")
    plt.close(fig)
    return {"figure": "fig_ch14_chart_intra_africa_trade", "type": "bar", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 14 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_afcfta_corridors_map(output_dir, args.seed),
                  plot_intra_africa_trade_bar(output_dir, args.seed)]
    combined = {"chapter": 14, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch14_figures", combined)
    print("Chapter 14 figures complete.")


if __name__ == "__main__":
    main()
