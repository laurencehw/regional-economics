"""Chapter 13 figure: Sub-Saharan Africa urbanization map.

Primate cities sized by population; urbanization corridors.
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


def plot_ssa_urbanization_map(output_dir: Path, seed: int = 42) -> dict:
    """SSA with primate cities and urbanization corridors."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch13_map_ssa_urbanization")

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
    ssa_proj.plot(ax=ax, color="#fff7bc", edgecolor=BORDER_COLOR, linewidth=0.5)

    setup_map_ax(ax, "Sub-Saharan Africa: Primate Cities and Urbanization Corridors")

    ann = load_annotations("ch13")
    crs = PROJECTIONS["africa"]
    if ann.get("cities"):
        # Plot cities with size proportional to importance
        for city in project_cities(ann["cities"], crs):
            ax.scatter(city["lon"], city["lat"], s=50, c="#e6ab02",
                       edgecolors="#333333", linewidths=0.5, zorder=5)
            dx, dy = city.get("label_offset", [5, 3])
            ax.annotate(city["name"], (city["lon"], city["lat"]),
                        fontsize=6, ha="left", va="bottom",
                        xytext=(dx, dy), textcoords="offset points",
                        zorder=6)
    if ann.get("corridors"):
        annotate_corridors(ax, project_corridors(ann["corridors"], crs))

    add_figure_source(fig, "Natural Earth; UN World Urbanization Prospects.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch13_map_ssa_urbanization")
    plt.close(fig)
    return {"figure": "fig_ch13_map_ssa_urbanization", "type": "map", **paths}


# ------------------------------------------------------------------ #
#  Figure: Urbanization vs manufacturing — SSA + reference countries
# ------------------------------------------------------------------ #

def plot_urbanization_scatter(output_dir: Path, seed: int = 42) -> dict:
    """Scatter: urbanization rate vs manufacturing share of GDP."""
    # (country, urbanization_%, manufacturing_%_gdp, group)
    data = [
        # SSA countries
        ("Nigeria",      54, 9.0,  "SSA"),
        ("Ethiopia",     23, 6.0,  "SSA"),
        ("Kenya",        29, 7.5,  "SSA"),
        ("Tanzania",     37, 8.0,  "SSA"),
        ("Ghana",        59, 10.0, "SSA"),
        ("Senegal",      49, 14.0, "SSA"),
        ("Côte d'Ivoire",53, 12.0, "SSA"),
        ("Uganda",       26, 8.5,  "SSA"),
        ("Rwanda",       17, 7.0,  "SSA"),
        ("Mozambique",   38, 9.0,  "SSA"),
        ("Zambia",       46, 8.0,  "SSA"),
        ("Cameroon",     59, 13.0, "SSA"),
        ("DRC",          46, 5.0,  "SSA"),
        ("Angola",       69, 5.5,  "SSA"),
        ("South Africa", 68, 12.0, "SSA"),
        # Reference countries
        ("China",        65, 27.0, "Reference"),
        ("Vietnam",      39, 25.0, "Reference"),
        ("Indonesia",    58, 19.0, "Reference"),
        ("Bangladesh",   40, 21.0, "Reference"),
    ]

    group_colors = {"SSA": QUAL_PALETTE[4], "Reference": QUAL_PALETTE[1]}

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    for group, color in group_colors.items():
        subset = [d for d in data if d[3] == group]
        xs = [d[1] for d in subset]
        ys = [d[2] for d in subset]
        marker = "o" if group == "SSA" else "D"
        ax.scatter(xs, ys, c=color, marker=marker, s=50, alpha=0.75,
                   edgecolors="white", linewidths=0.5, label=group, zorder=3)
        for d in subset:
            ax.annotate(d[0], (d[1], d[2]), fontsize=5.5, ha="left", va="bottom",
                        xytext=(4, 3), textcoords="offset points")

    ax.set_xlabel("Urbanization rate (%)", fontsize=8)
    ax.set_ylabel("Manufacturing share of GDP (%)", fontsize=8)
    ax.set_title("Urbanization Without Industrialization: SSA vs. Asian Comparators",
                 fontsize=9, fontweight="bold")
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(10, 80)
    ax.set_ylim(0, 32)

    add_figure_source(fig, "World Bank WDI (2023); UN World Urbanization Prospects (2022).")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch13_chart_urbanization_scatter")
    plt.close(fig)
    return {"figure": "fig_ch13_chart_urbanization_scatter", "type": "scatter", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 13 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_ssa_urbanization_map(output_dir, args.seed),
                  plot_urbanization_scatter(output_dir, args.seed)]
    combined = {"chapter": 13, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch13_figures", combined)
    print("Chapter 13 figures complete.")


if __name__ == "__main__":
    main()
