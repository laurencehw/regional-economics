"""Chapter 8 figures: India IT cluster map + concentration choropleth.

Map: India admin-1 with IT cluster markers, SEZ locations.
Thematic: IT-BPO export intensity by state (HHI / location quotient).
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
    annotate_cities, project_cities,
)


def plot_india_it_map(output_dir: Path, seed: int = 42) -> dict:
    """India with IT cluster markers and SEZ locations."""
    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries, PROJECTIONS
    except ImportError:
        return _placeholder(output_dir, "fig_ch08_map_india_it")

    world = get_country_boundaries()
    sa = world[world["iso3"].isin(["IND", "PAK", "BGD", "LKA", "NPL", "BTN", "MMR"])]

    fig, ax = plt.subplots(figsize=FIGSIZE_MAP)
    try:
        sa_proj = sa.to_crs(PROJECTIONS["south_asia"])
    except Exception:
        sa_proj = sa

    india = sa_proj[sa_proj["iso3"] == "IND"]
    others = sa_proj[sa_proj["iso3"] != "IND"]
    others.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.3)
    india.plot(ax=ax, color="#d4e6f1", edgecolor=BORDER_COLOR, linewidth=0.5)

    setup_map_ax(ax, "India: IT-BPO Clusters and Special Economic Zones")

    ann = load_annotations("ch08")
    crs = PROJECTIONS["south_asia"]
    if ann.get("cities"):
        annotate_cities(ax, project_cities(ann["cities"], crs))

    add_figure_source(fig, "Natural Earth; NASSCOM; Indian SEZ Board.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch08_map_india_it")
    plt.close(fig)
    return {"figure": "fig_ch08_map_india_it", "type": "map", **paths}


def plot_it_concentration(output_dir: Path, seed: int = 42) -> dict:
    """IT-BPO export intensity by Indian state — horizontal bar chart."""
    rng = np.random.default_rng(seed)

    states = [
        ("Karnataka", 3.8),
        ("Telangana", 3.2),
        ("Maharashtra", 2.6),
        ("Tamil Nadu", 2.4),
        ("NCT Delhi", 2.1),
        ("West Bengal", 1.3),
        ("Uttar Pradesh", 0.6),
        ("Gujarat", 0.9),
        ("Kerala", 1.5),
        ("Rajasthan", 0.4),
    ]
    names = [s[0] for s in reversed(states)]
    lqs = [s[1] + rng.normal(0, 0.05) for s in reversed(states)]

    fig, ax = plt.subplots(figsize=FIGSIZE_THEMATIC)
    colors = ["#e41a1c" if lq > 1.0 else "#377eb8" for lq in lqs]
    ax.barh(range(len(names)), lqs, color=colors, height=0.6, alpha=0.8)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=7)
    ax.axvline(1.0, color="#808080", linestyle="--", linewidth=0.8,
               label="LQ = 1.0 (national average)")
    ax.set_xlabel("Location Quotient (IT-BPO employment)", fontsize=8)
    ax.set_title("IT-BPO Concentration by Indian State",
                 fontsize=9, fontweight="bold")
    ax.legend(fontsize=6, loc="lower right", frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    add_figure_source(fig, "NASSCOM; RBI state GDP data. Illustrative; based on patterns in NASSCOM and RBI data, not exact reproduction.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch08_thematic_it_concentration")
    plt.close(fig)
    return {"figure": "fig_ch08_thematic_it_concentration", "type": "thematic", **paths}


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
    parser = argparse.ArgumentParser(description="Chapter 8 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = []
    summaries.append(plot_india_it_map(output_dir, args.seed))
    summaries.append(plot_it_concentration(output_dir, args.seed))

    combined = {"chapter": 8, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch08_figures", combined)
    print("Chapter 8 figures complete.")


if __name__ == "__main__":
    main()
