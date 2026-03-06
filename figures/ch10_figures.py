"""Chapter 10 figure: EU North-South divide map.

Shows North-South divide; Brexit geography; key financial/policy cities.
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


def plot_north_south_map(output_dir: Path, seed: int = 42) -> dict:
    """EU North-South economic divide + Brexit geography."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch10_map_north_south")

    world = get_country_boundaries()
    eu_iso = ISO3_SETS["europe"]
    eu = world[world["iso3"].isin(eu_iso)].copy()
    context = world[world["iso3"].isin(["UKR", "TUR", "RUS", "BLR", "MDA", "MAR", "TUN"])]

    # North-South classification
    north = {"DEU", "NLD", "BEL", "AUT", "FIN", "SWE", "DNK", "IRL", "LUX",
             "NOR", "CHE", "EST", "LVA", "LTU", "FRA"}
    south = {"ITA", "ESP", "PRT", "GRC", "CYP", "MLT", "HRV", "SVN"}
    east_new = {"POL", "CZE", "SVK", "HUN", "ROU", "BGR"}

    def classify(iso):
        if iso == "GBR":
            return "#b3cde3"  # Brexit blue
        elif iso in north:
            return "#2ca02c"
        elif iso in south:
            return "#d62728"
        elif iso in east_new:
            return "#ff7f00"
        return LAND_COLOR

    eu["_color"] = eu["iso3"].map(classify)

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        eu_proj = eu.to_crs(PROJECTIONS["europe"])
        ctx_proj = context.to_crs(PROJECTIONS["europe"])
    except Exception:
        eu_proj, ctx_proj = eu, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    for color_val in eu_proj["_color"].unique():
        subset = eu_proj[eu_proj["_color"] == color_val]
        subset.plot(ax=ax, color=color_val, edgecolor=BORDER_COLOR,
                    linewidth=0.5, alpha=0.6)

    # Zoom to EU countries with buffer
    xmin, ymin, xmax, ymax = eu_proj.total_bounds
    dx, dy = (xmax - xmin) * 0.08, (ymax - ymin) * 0.08
    setup_map_ax(ax, "EU North-South Divide and Brexit Geography",
                 bbox=(xmin - dx, ymin - dy, xmax + dx, ymax + dy))

    ann = load_annotations("ch10")
    crs = PROJECTIONS["europe"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))

    # Legend
    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor="#2ca02c", alpha=0.6, label="Core North"),
        Patch(facecolor="#d62728", alpha=0.6, label="South/Periphery"),
        Patch(facecolor="#ff7f00", alpha=0.6, label="New Member States (East)"),
        Patch(facecolor="#b3cde3", alpha=0.6, label="UK (post-Brexit)"),
    ]
    ax.legend(handles=legend_items, fontsize=5.5, loc="lower left", frameon=False)

    add_figure_source(fig, "Natural Earth; Eurostat regional accounts.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch10_map_north_south")
    plt.close(fig)
    return {"figure": "fig_ch10_map_north_south", "type": "map", **paths}


# ------------------------------------------------------------------ #
#  Figure: Youth unemployment — North vs South, 2008 vs 2023
# ------------------------------------------------------------------ #

def plot_youth_unemployment_bar(output_dir: Path, seed: int = 42) -> dict:
    """Grouped bar chart: youth unemployment rates 2008 vs 2023 for 8 EU countries."""
    countries = ["Germany", "Netherlands", "France", "Ireland",
                 "Spain", "Greece", "Italy", "Portugal"]
    rates_2008 = [10.4, 5.3, 18.6, 12.7, 24.5, 21.9, 21.2, 16.7]
    rates_2023 = [5.8, 8.2, 17.2, 10.0, 28.4, 26.1, 22.7, 20.2]

    x = np.arange(len(countries))
    width = 0.35

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    ax.bar(x - width / 2, rates_2008, width, label="2008",
           color=QUAL_PALETTE[1], edgecolor="white", linewidth=0.5)
    ax.bar(x + width / 2, rates_2023, width, label="2023",
           color=QUAL_PALETTE[0], edgecolor="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(countries, fontsize=7, rotation=25, ha="right")
    ax.set_ylabel("Youth unemployment rate (%, age 15–24)", fontsize=8)
    ax.set_title("Youth Unemployment: Europe's North-South Divergence",
                 fontsize=9, fontweight="bold")
    ax.legend(fontsize=7, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Divider between North and South groups
    ax.axvline(3.5, color="#808080", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.text(1.5, max(rates_2023) + 2, "North / Core", fontsize=6.5,
            color="#808080", ha="center")
    ax.text(5.5, max(rates_2023) + 2, "South / Periphery", fontsize=6.5,
            color="#808080", ha="center")

    add_figure_source(fig, "Eurostat Labour Force Survey (2008, 2023). Age 15\u201324.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch10_chart_youth_unemployment")
    plt.close(fig)
    return {"figure": "fig_ch10_chart_youth_unemployment", "type": "bar", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 10 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_north_south_map(output_dir, args.seed),
                  plot_youth_unemployment_bar(output_dir, args.seed)]
    combined = {"chapter": 10, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch10_figures", combined)
    print("Chapter 10 figures complete.")


if __name__ == "__main__":
    main()
