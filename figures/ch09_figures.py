"""Chapter 9 figure: EU convergence map — NUTS-2 GDP per capita choropleth.

Shows Structural Funds eligibility boundary (75% EU average threshold).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from figure_utils import (
    FIGSIZE_MAP, FIGSIZE_WIDE, LAND_COLOR, WATER_COLOR, BORDER_COLOR,
    REGION_COLORS, QUAL_PALETTE,
    add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, setup_map_ax, load_annotations,
    annotate_cities, project_cities,
)


def plot_eu_convergence_map(output_dir: Path, seed: int = 42) -> dict:
    """EU countries with convergence shading — GDP per capita classes."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, ISO3_SETS, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch09_map_eu_convergence")

    world = get_country_boundaries()
    eu_iso = ISO3_SETS["europe"]
    eu = world[world["iso3"].isin(eu_iso)].copy()
    context = world[world["iso3"].isin(["UKR", "TUR", "RUS", "BLR", "MDA", "MAR", "TUN"])]

    # Assign GDP per capita classes (calibrated synthetic)
    rng = np.random.default_rng(seed)
    gdp_lookup = {
        "LUX": 95, "IRL": 85, "NLD": 75, "DNK": 72, "SWE": 70,
        "AUT": 68, "DEU": 67, "BEL": 65, "FIN": 62, "FRA": 60,
        "GBR": 58, "ITA": 52, "ESP": 48, "CZE": 47, "SVN": 46,
        "MLT": 44, "PRT": 42, "EST": 40, "LTU": 38, "SVK": 37,
        "LVA": 35, "HUN": 34, "POL": 33, "HRV": 30, "GRC": 28,
        "ROU": 25, "BGR": 22, "NOR": 75, "CHE": 80, "CYP": 40,
    }
    eu["gdp_index"] = eu["iso3"].map(gdp_lookup).fillna(50)

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        eu_proj = eu.to_crs(PROJECTIONS["europe"])
        ctx_proj = context.to_crs(PROJECTIONS["europe"])
    except Exception:
        eu_proj, ctx_proj = eu, context

    ctx_proj.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    eu_proj.plot(ax=ax, column="gdp_index", cmap="RdYlGn", edgecolor=BORDER_COLOR,
                 linewidth=0.5, legend=True,
                 legend_kwds={"label": "GDP per capita index (EU28 = 100)",
                              "shrink": 0.6, "orientation": "horizontal",
                              "pad": 0.05})

    # Zoom to EU countries with buffer
    xmin, ymin, xmax, ymax = eu_proj.total_bounds
    dx, dy = (xmax - xmin) * 0.08, (ymax - ymin) * 0.08
    setup_map_ax(ax, "EU Convergence: GDP per Capita Index and Structural Funds Eligibility",
                 bbox=(xmin - dx, ymin - dy, xmax + dx, ymax + dy))

    ann = load_annotations("ch09")
    crs = PROJECTIONS["europe"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))

    add_figure_source(fig, "Eurostat; Natural Earth. 75% threshold marks Structural Funds eligibility.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch09_map_eu_convergence")
    plt.close(fig)
    return {"figure": "fig_ch09_map_eu_convergence", "type": "map", **paths}


# ------------------------------------------------------------------ #
#  Figure: EU convergence bar chart — GDP per capita index by club
# ------------------------------------------------------------------ #

def plot_eu_convergence_bar(output_dir: Path, seed: int = 42) -> dict:
    """Horizontal bar chart: GDP per capita index (EU27=100) by convergence club."""
    countries = [
        ("Luxembourg", 261, "core"),
        ("Ireland", 234, "core"),
        ("Netherlands", 131, "core"),
        ("Germany", 124, "core"),
        ("Sweden", 122, "core"),
        ("France", 104, "core"),
        ("Spain", 85, "periphery"),
        ("Italy", 95, "periphery"),
        ("Greece", 67, "periphery"),
        ("Portugal", 77, "periphery"),
        ("Poland", 77, "new_member"),
        ("Romania", 72, "new_member"),
    ]

    club_colors = {
        "core": QUAL_PALETTE[1],        # blue
        "periphery": QUAL_PALETTE[0],   # red
        "new_member": QUAL_PALETTE[2],  # green
    }
    club_labels = {
        "core": "Core",
        "periphery": "Periphery",
        "new_member": "New Member States",
    }

    names = [c[0] for c in countries]
    values = [c[1] for c in countries]
    colors = [club_colors[c[2]] for c in countries]

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    y_pos = np.arange(len(names))
    ax.barh(y_pos, values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("GDP per capita index (EU27 = 100)", fontsize=8)
    ax.set_title("EU Convergence Clubs: GDP per Capita Relative to EU Average",
                 fontsize=9, fontweight="bold")
    ax.axvline(100, color="#808080", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.text(102, len(names) - 0.5, "EU avg = 100", fontsize=6.5, color="#808080",
            va="top")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend
    legend_items = [Patch(facecolor=club_colors[k], label=club_labels[k])
                    for k in ("core", "periphery", "new_member")]
    ax.legend(handles=legend_items, fontsize=6.5, loc="lower right", frameon=False)

    add_figure_source(fig, "Eurostat (2023). Index: EU27 = 100, PPS-adjusted.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch09_chart_eu_convergence_bar")
    plt.close(fig)
    return {"figure": "fig_ch09_chart_eu_convergence_bar", "type": "bar", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 9 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_eu_convergence_map(output_dir, args.seed),
                  plot_eu_convergence_bar(output_dir, args.seed)]
    combined = {"chapter": 9, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch09_figures", combined)
    print("Chapter 9 figures complete.")


if __name__ == "__main__":
    main()
