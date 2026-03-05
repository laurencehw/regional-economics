"""Chapter 3B conceptual diagram: Gravity model distance-decay curve.

Pure matplotlib — no geodata required.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from figure_utils import (
    FIGSIZE_CONCEPT, add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir,
)


def plot_gravity_decay(output_dir: Path, seed: int = 42) -> dict:
    """Distance-decay curve with annotated trade zones."""
    fig, ax = plt.subplots(figsize=FIGSIZE_CONCEPT)

    # Gravity model: Trade_ij = G * (GDP_i * GDP_j) / distance^beta
    # Normalize: flow = A / d^beta
    d = np.linspace(100, 20000, 500)  # km

    # Multiple distance elasticities
    betas = [
        (0.7, "Manufactures (β ≈ 0.7)", "#e41a1c"),
        (1.0, "All goods (β ≈ 1.0)", "#377eb8"),
        (1.5, "Agriculture (β ≈ 1.5)", "#4daf4a"),
    ]

    A = 1e6  # normalizing constant
    for beta, label, color in betas:
        flow = A / (d ** beta)
        flow_norm = flow / flow[0]  # normalize to 1 at minimum distance
        ax.plot(d, flow_norm, color=color, linewidth=1.8, label=label)

    # Annotated distance zones
    zones = [
        (500,   "Border\ntrade",   "#ffeda0"),
        (2000,  "Regional\n(EU, NAFTA)", "#d4e6f1"),
        (8000,  "Inter-\ncontinental", "#f0f0f0"),
    ]
    prev_d = 100
    for zone_d, label, color in zones:
        ax.axvspan(prev_d, zone_d, alpha=0.2, color=color)
        ax.text((prev_d + zone_d) / 2, 0.85, label, fontsize=6,
                ha="center", va="top", color="#555555",
                transform=ax.get_xaxis_transform())
        prev_d = zone_d

    ax.set_xlabel("Distance (km)", fontsize=8)
    ax.set_ylabel("Normalized trade flow", fontsize=8)
    ax.set_title("Gravity Model: Distance Decay of Trade",
                 fontsize=9, fontweight="bold")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(100, 20000)
    ax.set_ylim(1e-4, 1.2)
    ax.legend(fontsize=6, loc="upper right", frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Key distances annotated
    for dist, city_pair in [(900, "NY–Chicago"), (5500, "NY–London"),
                            (13000, "NY–Tokyo")]:
        ax.axvline(dist, color="#cccccc", linestyle=":", linewidth=0.5)
        ax.text(dist, 1e-4 * 2, city_pair, fontsize=5, rotation=90,
                va="bottom", ha="right", color="#808080")

    add_figure_source(fig, "Tinbergen (1962); Head & Mayer (2014).")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch03b_concept_gravity_decay")
    plt.close(fig)

    return {"figure": "fig_ch03b_concept_gravity_decay", "type": "concept", **paths}


def main():
    parser = argparse.ArgumentParser(description="Chapter 3B figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_gravity_decay(output_dir, args.seed)]
    combined = {"chapter": "3B", "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch03b_figures", combined)
    print("Chapter 3B figures complete.")


if __name__ == "__main__":
    main()
