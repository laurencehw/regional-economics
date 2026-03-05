"""Chapter 12 figure: MENA conflict zones map.

Syria, Yemen, Libya, Iraq highlighted; refugee flow arrows.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figure_utils import (
    FIGSIZE_MAP, LAND_COLOR, WATER_COLOR, BORDER_COLOR,
    add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, setup_map_ax, load_annotations,
    annotate_cities, annotate_arrows, project_cities, project_arrows,
)


def plot_conflict_zones_map(output_dir: Path, seed: int = 42) -> dict:
    """MENA conflict zones with refugee flow arrows."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch12_map_conflict_zones")

    world = get_country_boundaries()
    mena_iso = ISO3_SETS["mena"]
    conflict_iso = {"SYR", "YEM", "LBY", "IRQ"}
    mena = world[world["iso3"].isin(mena_iso)].copy()
    context = world[world["iso3"].isin(["TUR", "PAK", "AFG", "SDN", "TCD", "ETH"])]

    def color_fn(iso):
        if iso in conflict_iso:
            return "#d62728"
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
        alpha = 0.5 if cv == "#d62728" else 0.4
        subset.plot(ax=ax, color=cv, edgecolor=BORDER_COLOR,
                    linewidth=0.5, alpha=alpha)

    setup_map_ax(ax, "MENA Conflict Zones and Refugee Displacement")

    ann = load_annotations("ch12")
    crs = PROJECTIONS["mena"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))
    if ann.get("refugee_flows"):
        annotate_arrows(ax, project_arrows(ann["refugee_flows"], crs))

    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor="#d62728", alpha=0.5, label="Active conflict zones"),
        Patch(facecolor="#d4e6f1", alpha=0.4, label="Other MENA"),
    ]
    ax.legend(handles=legend_items, fontsize=5.5, loc="lower left", frameon=False)

    add_figure_source(fig, "Natural Earth; UNHCR; ACLED conflict data.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch12_map_conflict_zones")
    plt.close(fig)
    return {"figure": "fig_ch12_map_conflict_zones", "type": "map", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 12 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_conflict_zones_map(output_dir, args.seed)]
    combined = {"chapter": 12, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch12_figures", combined)
    print("Chapter 12 figures complete.")


if __name__ == "__main__":
    main()
