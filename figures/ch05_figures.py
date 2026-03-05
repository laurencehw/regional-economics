"""Chapter 5 figures: Latin America map + middle-income trap scatter.

Map: Mercosur, Pacific Alliance, CAFTA-DR groupings; commodity zones; cities.
Thematic: GDP per capita vs growth scatter — middle-income trap visualization.
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
    annotate_cities,
)


def plot_latin_america_map(output_dir: Path, seed: int = 42) -> dict:
    """Latin America with trade bloc shading and key cities."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch05_map_latin_america")

    world = get_country_boundaries()
    ann = load_annotations("ch05")
    blocs = ann.get("trade_blocs", {})

    la_iso = set()
    bloc_colors = {}
    for key, bloc in blocs.items():
        la_iso.update(bloc["iso3"])
        for iso in bloc["iso3"]:
            bloc_colors[iso] = bloc["color"]

    # Add other LA countries
    other_la = ["BRA", "ARG", "CHL", "COL", "PER", "MEX", "VEN", "ECU",
                "BOL", "PRY", "URY", "GUY", "SUR", "GTM", "HND", "SLV",
                "NIC", "CRI", "PAN", "CUB", "DOM", "HTI", "JAM", "TTO"]
    la_iso.update(other_la)
    la = world[world["iso3"].isin(la_iso)]

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        la_proj = la.to_crs(PROJECTIONS["latin_america"])
    except Exception:
        la_proj = la

    # Color by bloc membership
    def _get_color(iso):
        return bloc_colors.get(iso, LAND_COLOR)

    la_proj = la_proj.copy()
    la_proj["_color"] = la_proj["iso3"].map(_get_color)
    for color_val in la_proj["_color"].unique():
        subset = la_proj[la_proj["_color"] == color_val]
        subset.plot(ax=ax, color=color_val, edgecolor=BORDER_COLOR, linewidth=0.5,
                    alpha=0.6)

    setup_map_ax(ax, "Latin America: Trade Blocs and Key Economies")

    if ann.get("cities"):
        annotate_cities(ax, ann["cities"])

    # Legend
    from matplotlib.patches import Patch
    legend_items = [Patch(facecolor=b["color"], alpha=0.6, label=b["label"])
                    for b in blocs.values()]
    ax.legend(handles=legend_items, fontsize=6, loc="lower left", frameon=False)

    add_figure_source(fig, "Natural Earth; WTO trade agreements database.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch05_map_latin_america")
    plt.close(fig)
    return {"figure": "fig_ch05_map_latin_america", "type": "map", **paths}


def plot_middle_income_trap(output_dir: Path, seed: int = 42) -> dict:
    """GDP per capita vs. growth rate scatter — middle-income trap."""
    rng = np.random.default_rng(seed)

    countries = [
        ("BRA", 14064, 0.8, "Latin America"),
        ("MEX", 18833, 1.2, "Latin America"),
        ("ARG", 22064, 0.5, "Latin America"),
        ("CHL", 25155, 2.5, "Latin America"),
        ("COL", 14522, 1.8, "Latin America"),
        ("PER", 12794, 3.0, "Latin America"),
        ("CRI", 20683, 2.2, "Latin America"),
        ("DOM", 18600, 3.5, "Latin America"),
        ("VEN", 7045, -3.0, "Latin America"),
        ("KOR", 44292, 3.0, "East Asia"),
        ("CHN", 17192, 6.0, "East Asia"),
        ("MYS", 28364, 4.5, "East Asia"),
        ("THA", 18236, 3.5, "East Asia"),
        ("VNM", 10583, 5.5, "East Asia"),
        ("IND", 7333, 5.0, "South Asia"),
        ("POL", 35651, 3.8, "Europe"),
        ("TUR", 30253, 3.0, "MENA"),
    ]

    fig, ax = plt.subplots(figsize=FIGSIZE_THEMATIC)

    region_colors = {
        "Latin America": "#1b9e77",
        "East Asia": "#d95f02",
        "South Asia": "#7570b3",
        "Europe": "#e7298a",
        "MENA": "#66a61e",
    }

    for iso, gdppc, growth, region in countries:
        noise_g = rng.normal(0, 0.15)
        noise_y = rng.normal(0, 200)
        ax.scatter(gdppc + noise_y, growth + noise_g,
                   color=region_colors[region], s=40, alpha=0.8,
                   edgecolors="white", linewidths=0.5, zorder=5)
        ax.annotate(iso, (gdppc + noise_y, growth + noise_g),
                    fontsize=5, ha="left", va="bottom",
                    xytext=(3, 2), textcoords="offset points")

    # Middle-income trap zone
    ax.axvspan(5000, 20000, alpha=0.08, color="#e41a1c")
    ax.text(12000, -2.5, "Middle-Income\nTrap Zone", fontsize=7,
            ha="center", color="#e41a1c", alpha=0.7, fontstyle="italic")

    from matplotlib.patches import Patch
    legend_items = [Patch(facecolor=c, label=r, alpha=0.8)
                    for r, c in region_colors.items()]
    ax.legend(handles=legend_items, fontsize=6, loc="upper right", frameon=False)

    ax.set_xlabel("GDP per capita (PPP, 2020 USD)", fontsize=8)
    ax.set_ylabel("Average growth rate (%)", fontsize=8)
    ax.set_title("Middle-Income Trap: GDP per Capita vs. Growth",
                 fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axhline(0, color="#808080", linestyle="--", linewidth=0.5)

    add_figure_source(fig, "World Bank WDI; Penn World Table 10.0.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch05_thematic_middle_income")
    plt.close(fig)
    return {"figure": "fig_ch05_thematic_middle_income", "type": "thematic", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 5 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = []
    summaries.append(plot_latin_america_map(output_dir, args.seed))
    summaries.append(plot_middle_income_trap(output_dir, args.seed))

    combined = {"chapter": 5, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch05_figures", combined)
    print("Chapter 5 figures complete.")


if __name__ == "__main__":
    main()
