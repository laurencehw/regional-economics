"""Chapter 16 figure: Global APS city connectivity network.

GaWC-style hub hierarchy diagram — services network visualization.
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
    add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir, load_annotations,
)


def plot_services_network(output_dir: Path, seed: int = 42) -> dict:
    """Global APS city connectivity network (GaWC-style hub hierarchy)."""
    rng = np.random.default_rng(seed)
    ann = load_annotations("ch16")
    cities = ann.get("aps_cities", [])

    if not cities:
        # Fallback embedded data
        cities = [
            {"name": "London", "lat": 51.51, "lon": -0.13, "tier": 1},
            {"name": "New York", "lat": 40.71, "lon": -74.01, "tier": 1},
            {"name": "Singapore", "lat": 1.35, "lon": 103.82, "tier": 1},
            {"name": "Hong Kong", "lat": 22.32, "lon": 114.17, "tier": 1},
            {"name": "Tokyo", "lat": 35.68, "lon": 139.69, "tier": 2},
            {"name": "Paris", "lat": 48.86, "lon": 2.35, "tier": 2},
            {"name": "Sydney", "lat": -33.87, "lon": 151.21, "tier": 2},
            {"name": "Dubai", "lat": 25.20, "lon": 55.27, "tier": 2},
            {"name": "Shanghai", "lat": 31.23, "lon": 121.47, "tier": 2},
            {"name": "Mumbai", "lat": 19.08, "lon": 72.88, "tier": 3},
            {"name": "São Paulo", "lat": -23.55, "lon": -46.63, "tier": 3},
            {"name": "Nairobi", "lat": -1.29, "lon": 36.82, "tier": 3},
        ]

    try:
        import geopandas as gpd
        from figure_utils import get_country_boundaries
        world = get_country_boundaries()
        has_geo = True
    except ImportError:
        has_geo = False

    fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

    if has_geo:
        world.plot(ax=ax, color=LAND_COLOR, edgecolor=BORDER_COLOR, linewidth=0.15)

    # Draw connections between tier-1 cities (strong) and tier-1 to tier-2 (medium)
    tier1 = [c for c in cities if c["tier"] == 1]
    tier2 = [c for c in cities if c["tier"] == 2]
    tier3 = [c for c in cities if c["tier"] == 3]

    # Tier-1 to tier-1: strong links
    for i, c1 in enumerate(tier1):
        for c2 in tier1[i+1:]:
            ax.plot([c1["lon"], c2["lon"]], [c1["lat"], c2["lat"]],
                    color="#e41a1c", linewidth=1.2, alpha=0.4, zorder=3)

    # Tier-1 to tier-2: medium links
    for c1 in tier1:
        for c2 in tier2:
            ax.plot([c1["lon"], c2["lon"]], [c1["lat"], c2["lat"]],
                    color="#377eb8", linewidth=0.6, alpha=0.25, zorder=2)

    # Tier-2 to tier-3: weak links
    for c2 in tier2:
        for c3 in tier3:
            dist = np.sqrt((c2["lon"]-c3["lon"])**2 + (c2["lat"]-c3["lat"])**2)
            if dist < 80:  # only nearby connections
                ax.plot([c2["lon"], c3["lon"]], [c2["lat"], c3["lat"]],
                        color="#808080", linewidth=0.3, alpha=0.2, zorder=1)

    # Draw city nodes
    tier_config = {
        1: {"size": 80, "color": "#e41a1c", "label": "Alpha++ (Tier 1)"},
        2: {"size": 45, "color": "#377eb8", "label": "Alpha+ (Tier 2)"},
        3: {"size": 25, "color": "#4daf4a", "label": "Alpha (Tier 3)"},
    }
    for tier_val, cfg in tier_config.items():
        tier_cities = [c for c in cities if c["tier"] == tier_val]
        for c in tier_cities:
            ax.scatter(c["lon"], c["lat"], s=cfg["size"], c=cfg["color"],
                       edgecolors="white", linewidths=0.5, zorder=5)
            ax.annotate(c["name"], (c["lon"], c["lat"]),
                        fontsize=5 if tier_val < 3 else 4.5,
                        ha="left", va="bottom",
                        xytext=(4, 4), textcoords="offset points",
                        fontweight="bold" if tier_val == 1 else "normal",
                        zorder=6)

    ax.set_title("Global Advanced Producer Services Network (GaWC Hierarchy)",
                 fontsize=9, fontweight="bold")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-60, 75)
    ax.axis("off")

    # Legend
    from matplotlib.lines import Line2D
    legend_items = [
        Line2D([0], [0], marker="o", color=cfg["color"], linestyle="",
               markersize=np.sqrt(cfg["size"])/2, label=cfg["label"])
        for cfg in tier_config.values()
    ]
    ax.legend(handles=legend_items, fontsize=5.5, loc="lower left", frameon=False)

    add_figure_source(fig, "GaWC Research Network; Taylor & Derudder (2016).")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch16_thematic_services_network")
    plt.close(fig)
    return {"figure": "fig_ch16_thematic_services_network", "type": "thematic", **paths}


def main():
    parser = argparse.ArgumentParser(description="Chapter 16 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_services_network(output_dir, args.seed)]
    combined = {"chapter": 16, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch16_figures", combined)
    print("Chapter 16 figures complete.")


if __name__ == "__main__":
    main()
