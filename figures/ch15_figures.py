"""Chapter 15 figure: Climate vulnerability global map.

Coastal flood zones, stranded-asset regions, climate migration arrows.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figure_utils import (
    FIGSIZE_WIDE, LAND_COLOR, WATER_COLOR, BORDER_COLOR,
    QUAL_PALETTE,
    add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, setup_map_ax, load_annotations,
    annotate_arrows, project_arrows,
)


def plot_climate_vulnerability_map(output_dir: Path, seed: int = 42) -> dict:
    """Global map with climate vulnerability zones and migration arrows."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries
    except ImportError:
        return _placeholder(output_dir, "fig_ch15_map_climate_vulnerability")

    world = get_country_boundaries()

    # Climate vulnerability index (calibrated synthetic)
    rng = np.random.default_rng(seed)
    high_vuln = {"BGD", "MMR", "VNM", "PHL", "IDN", "IND", "NGA", "MOZ",
                 "MDG", "HTI", "SLB", "VUT", "TUV", "KIR", "YEM", "SOM",
                 "SDN", "TCD", "NER", "MLI", "ETH", "KEN", "SEN"}
    stranded = {"SAU", "ARE", "KWT", "QAT", "IRQ", "RUS", "VEN", "NGA",
                "AGO", "LBY", "DZA"}

    world_copy = world.copy()
    def vuln_color(iso):
        if iso in high_vuln:
            return "#d62728"
        elif iso in stranded:
            return "#ff7f00"
        return LAND_COLOR

    world_copy["_color"] = world_copy["iso3"].map(vuln_color)

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

    for cv in world_copy["_color"].unique():
        subset = world_copy[world_copy["_color"] == cv]
        alpha = 0.6 if cv != LAND_COLOR else 0.3
        subset.plot(ax=ax, color=cv, edgecolor=BORDER_COLOR,
                    linewidth=0.2, alpha=alpha)

    setup_map_ax(ax, "Global Climate Vulnerability: Exposure, Stranded Assets, and Migration")

    ann = load_annotations("ch15")
    if ann.get("arrows"):
        annotate_arrows(ax, ann["arrows"])

    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor="#d62728", alpha=0.6, label="High climate vulnerability"),
        Patch(facecolor="#ff7f00", alpha=0.6, label="Stranded fossil-fuel assets"),
        Patch(facecolor=LAND_COLOR, alpha=0.3, label="Lower vulnerability"),
    ]
    ax.legend(handles=legend_items, fontsize=5.5, loc="lower left", frameon=False)

    add_figure_source(fig, "ND-GAIN Index; IEA stranded assets data; IPCC AR6.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch15_map_climate_vulnerability")
    plt.close(fig)
    return {"figure": "fig_ch15_map_climate_vulnerability", "type": "map", **paths}


# ------------------------------------------------------------------ #
#  Figure: Stranded fossil-fuel assets — top 10 countries
# ------------------------------------------------------------------ #

def plot_stranded_assets_bar(output_dir: Path, seed: int = 42) -> dict:
    """Horizontal bar chart of estimated stranded fossil-fuel asset value."""
    data = [
        ("Saudi Arabia", 1800),
        ("Russia",       1500),
        ("Iraq",          700),
        ("Iran",          650),
        ("UAE",           600),
        ("Kuwait",        450),
        ("Qatar",         400),
        ("Nigeria",       350),
        ("Venezuela",     320),
        ("Canada",        280),
    ]
    # Sort ascending for horizontal bar
    data.sort(key=lambda x: x[1])

    names = [d[0] for d in data]
    values = [d[1] for d in data]

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    y_pos = np.arange(len(names))
    ax.barh(y_pos, values, color=QUAL_PALETTE[4], edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=7)
    ax.set_xlabel("Estimated stranded asset value (billions USD)", fontsize=8)
    ax.set_title("Stranded Fossil-Fuel Assets: Top 10 Countries at Risk",
                 fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Value labels
    for i, val in enumerate(values):
        ax.text(val + 20, i, f"${val}B", va="center", fontsize=6.5, color="#333333")

    add_figure_source(fig, "Carbon Tracker Initiative (2023); IEA World Energy Outlook (2023). Illustrative estimates.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch15_chart_stranded_assets")
    plt.close(fig)
    return {"figure": "fig_ch15_chart_stranded_assets", "type": "bar", **paths}


def _placeholder(output_dir, stem):
    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
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
    parser = argparse.ArgumentParser(description="Chapter 15 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_climate_vulnerability_map(output_dir, args.seed),
                  plot_stranded_assets_bar(output_dir, args.seed)]
    combined = {"chapter": 15, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch15_figures", combined)
    print("Chapter 15 figures complete.")


if __name__ == "__main__":
    main()
