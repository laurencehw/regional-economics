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
    FIGSIZE_MAP, LAND_COLOR, WATER_COLOR, BORDER_COLOR, REGION_COLORS,
    add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, setup_map_ax, load_annotations,
    annotate_cities,
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
            return "#66a61e"
        return "#d4e6f1"

    mena["_color"] = mena["iso3"].map(color_fn)

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        mena_proj = mena.to_crs(PROJECTIONS["mena"])
        ctx_proj = context.to_crs(PROJECTIONS["mena"])
    except Exception:
        mena_proj, ctx_proj = mena, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    for cv in mena_proj["_color"].unique():
        subset = mena_proj[mena_proj["_color"] == cv]
        subset.plot(ax=ax, color=cv, edgecolor=BORDER_COLOR, linewidth=0.5, alpha=0.6)

    setup_map_ax(ax, "MENA: GCC Energy Economies and Diversification Hubs")

    ann = load_annotations("ch11")
    if ann.get("cities"):
        annotate_cities(ax, ann["cities"])

    # Energy field markers
    for field in ann.get("energy_zones", []):
        ax.plot(field["lon"], field["lat"], "^", color="#d62728",
                markersize=8, zorder=5, alpha=0.8)
        ax.annotate(field["name"], (field["lon"], field["lat"]),
                    fontsize=4.5, ha="left", va="bottom",
                    xytext=(3, 3), textcoords="offset points",
                    color="#d62728")

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_items = [
        Patch(facecolor="#66a61e", alpha=0.6, label="GCC states"),
        Patch(facecolor="#d4e6f1", alpha=0.6, label="Other MENA"),
        Line2D([0], [0], marker="^", color="#d62728", linestyle="",
               markersize=6, label="Major oil/gas fields"),
    ]
    ax.legend(handles=legend_items, fontsize=5.5, loc="lower left", frameon=False)

    add_figure_source(fig, "Natural Earth; EIA International Energy Statistics.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch11_map_mena_energy")
    plt.close(fig)
    return {"figure": "fig_ch11_map_mena_energy", "type": "map", **paths}


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

    summaries = [plot_mena_energy_map(output_dir, args.seed)]
    combined = {"chapter": 11, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch11_figures", combined)
    print("Chapter 11 figures complete.")


if __name__ == "__main__":
    main()
