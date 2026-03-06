"""Chapter 11 figure: MENA energy map.

GCC states, oil/gas field zones, SWF headquarters, diversification hubs.
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
    annotate_cities, project_cities,
)


def plot_mena_energy_map(output_dir: Path, seed: int = 42) -> dict:
    """MENA with GCC highlighted, energy fields, diversification hubs."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch11_map_mena_energy")

    world = get_country_boundaries()
    mena_iso = ISO3_SETS["mena"]
    gcc_iso = ISO3_SETS["gcc"]
    mena = world[world["iso3"].isin(mena_iso)].copy()
    context = world[world["iso3"].isin(["TUR", "PAK", "AFG", "SDN", "TCD", "ETH"])]

    def color_fn(iso):
        if iso in gcc_iso:
            return "#7dab6e"
        return "#d4e6f1"

    mena["_color"] = mena["iso3"].map(color_fn)

    fig, ax = plt.subplots(figsize=(8, 6))  # wider than default for Gulf label density
    try:
        mena_proj = mena.to_crs(PROJECTIONS["mena"])
        ctx_proj = context.to_crs(PROJECTIONS["mena"])
    except Exception:
        mena_proj, ctx_proj = mena, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    for cv in mena_proj["_color"].unique():
        subset = mena_proj[mena_proj["_color"] == cv]
        subset.plot(ax=ax, color=cv, edgecolor=BORDER_COLOR, linewidth=0.5, alpha=0.6)

    # Zoom to MENA countries with buffer
    xmin, ymin, xmax, ymax = mena_proj.total_bounds
    dx, dy = (xmax - xmin) * 0.08, (ymax - ymin) * 0.08
    setup_map_ax(ax, "MENA: GCC Energy Economies and Diversification Hubs",
                 bbox=(xmin - dx, ymin - dy, xmax + dx, ymax + dy))

    ann = load_annotations("ch11")
    crs = PROJECTIONS["mena"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))

    # Energy field markers (project to map CRS) — alternate offsets to reduce overlap
    energy_zones = ann.get("energy_zones", [])
    if energy_zones:
        proj_zones = project_cities(energy_zones, crs)  # same lon/lat structure
        offset_cycle = [(5, 5), (-5, 8), (5, -8), (-5, -5), (8, 3), (-8, 3)]
        for idx, field in enumerate(proj_zones):
            ax.plot(field["lon"], field["lat"], "^", color="#c44e52",
                    markersize=7, zorder=5, alpha=0.8)
            dx, dy = offset_cycle[idx % len(offset_cycle)]
            ax.annotate(field["name"], (field["lon"], field["lat"]),
                        fontsize=6, ha="left", va="bottom",
                        xytext=(dx, dy), textcoords="offset points",
                        color="#c44e52",
                        bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=1))

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_items = [
        Patch(facecolor="#7dab6e", alpha=0.6, label="GCC states"),
        Patch(facecolor="#d4e6f1", alpha=0.6, label="Other MENA"),
        Line2D([0], [0], marker="^", color="#c44e52", linestyle="",
               markersize=6, label="Major oil/gas fields"),
    ]
    ax.legend(handles=legend_items, fontsize=5.5, loc="lower left", frameon=False)

    add_figure_source(fig, "Natural Earth; EIA International Energy Statistics.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch11_map_mena_energy")
    plt.close(fig)
    return {"figure": "fig_ch11_map_mena_energy", "type": "map", **paths}


# ------------------------------------------------------------------ #
#  Figure: GCC diversification scatter — oil rents vs non-oil GDP
# ------------------------------------------------------------------ #

def plot_gdp_diversification_scatter(output_dir: Path, seed: int = 42) -> dict:
    """Scatter plot of GCC states: oil rents vs non-oil GDP share."""
    # Data: (country, oil_rents_%_gdp, non_oil_gdp_share_%, population_millions)
    gcc_data = [
        ("Saudi Arabia", 23.0, 57.0, 36.0),
        ("UAE",           8.0, 74.0, 10.0),
        ("Qatar",        15.0, 60.0,  2.9),
        ("Kuwait",       42.0, 40.0,  4.3),
        ("Oman",         27.0, 54.0,  4.6),
        ("Bahrain",      10.0, 78.0,  1.5),
    ]

    names = [d[0] for d in gcc_data]
    oil_rents = [d[1] for d in gcc_data]
    non_oil = [d[2] for d in gcc_data]
    pop = [d[3] for d in gcc_data]

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    scatter = ax.scatter(oil_rents, non_oil,
                         s=[p * 25 for p in pop],
                         c=QUAL_PALETTE[:len(names)],
                         alpha=0.75, edgecolors="white", linewidths=0.8,
                         zorder=3)

    for i, name in enumerate(names):
        ax.annotate(name, (oil_rents[i], non_oil[i]),
                    fontsize=7, ha="left", va="bottom",
                    xytext=(6, 4), textcoords="offset points")

    ax.set_xlabel("Oil rents (% of GDP)", fontsize=8)
    ax.set_ylabel("Non-oil GDP share (%)", fontsize=8)
    ax.set_title("GCC Diversification Progress: Oil Dependence vs. Non-Oil Economy",
                 fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(0, 50)
    ax.set_ylim(30, 90)

    # Size legend
    for sz_val, sz_label in [(5, "5M"), (20, "20M"), (35, "35M")]:
        ax.scatter([], [], s=sz_val * 25, c="#808080", alpha=0.4,
                   edgecolors="white", label=f"Pop. {sz_label}")
    ax.legend(fontsize=6.5, loc="upper right", frameon=False, title="Population",
              title_fontsize=7)

    add_figure_source(fig, "World Bank WDI (2023); national statistical offices. Bubble size = population.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch11_chart_gdp_diversification")
    plt.close(fig)
    return {"figure": "fig_ch11_chart_gdp_diversification", "type": "scatter", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 11 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_mena_energy_map(output_dir, args.seed),
                  plot_gdp_diversification_scatter(output_dir, args.seed)]
    combined = {"chapter": 11, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch11_figures", combined)
    print("Chapter 11 figures complete.")


if __name__ == "__main__":
    main()
