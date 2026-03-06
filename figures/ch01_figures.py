"""Chapter 1 conceptual diagrams: Von Thünen rings + Krugman core-periphery.

Pure matplotlib — no geodata required.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from figure_utils import (
    FIGSIZE_CONCEPT, DPI, add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir,
)


# ------------------------------------------------------------------ #
#  Figure 1: Von Thünen concentric land-use rings with bid-rent curves
# ------------------------------------------------------------------ #

def plot_von_thunen(output_dir: Path, seed: int = 42) -> dict:
    """Concentric land-use rings (left) + bid-rent curves (right)."""
    fig, (ax_map, ax_rent) = plt.subplots(1, 2, figsize=(8, 4))

    # Ring parameters: (label, inner_r, outer_r, color)
    rings = [
        ("Dairy / Market\ngardening", 0.0, 1.0, "#7dab6e"),
        ("Timber &\nfirewood",       1.0, 1.8, "#8c7bba"),
        ("Intensive\narable",        1.8, 2.8, "#dd8452"),
        ("Extensive\narable",        2.8, 3.8, "#c44e52"),
        ("Ranching /\npasture",      3.8, 5.0, "#d4b44a"),
    ]

    # Left panel: concentric rings
    for label, r_in, r_out, color in reversed(rings):
        circle = plt.Circle((0, 0), r_out, color=color, alpha=0.5)
        ax_map.add_patch(circle)
    # City marker
    ax_map.plot(0, 0, "ko", markersize=8, zorder=5)
    ax_map.text(0, 0.55, "City", ha="center", va="bottom", fontsize=7,
                fontweight="bold",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1))
    # Labels on rings — alternate left/right to prevent overlap
    label_positions = [(0, -0.5), (1.5, -1.4), (0, -2.3), (-1.8, -3.3), (0, -4.4)]
    for (label, _, _, _), (lx, ly) in zip(rings, label_positions):
        ax_map.text(lx, ly, label, ha="center", va="center", fontsize=6.5,
                    fontweight="bold",
                    bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", pad=1))

    ax_map.set_xlim(-5.5, 5.5)
    ax_map.set_ylim(-5.5, 5.5)
    ax_map.set_aspect("equal")
    ax_map.axis("off")
    ax_map.set_title("Von Thünen Land-Use Rings", fontsize=9, fontweight="bold")

    # Right panel: bid-rent curves
    d = np.linspace(0, 5.5, 200)
    curves = [
        ("Dairy",    10.0, 2.2, "#7dab6e"),
        ("Timber",    6.0, 1.0, "#8c7bba"),
        ("Intensive", 5.0, 0.7, "#dd8452"),
        ("Extensive", 3.5, 0.4, "#c44e52"),
        ("Pasture",   2.0, 0.2, "#d4b44a"),
    ]
    for label, intercept, slope, color in curves:
        rent = np.maximum(intercept - slope * d, 0)
        ax_rent.plot(d, rent, color=color, linewidth=1.5, label=label)

    ax_rent.set_xlabel("Distance from city", fontsize=8)
    ax_rent.set_ylabel("Land rent", fontsize=8)
    ax_rent.set_title("Bid-Rent Curves", fontsize=9, fontweight="bold")
    ax_rent.legend(fontsize=6, loc="upper right", frameon=False)
    ax_rent.set_xlim(0, 5.5)
    ax_rent.set_ylim(0, 11)
    ax_rent.spines["top"].set_visible(False)
    ax_rent.spines["right"].set_visible(False)

    add_figure_source(fig, "Von Thünen (1826); stylized illustration.")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch01_concept_von_thunen")
    plt.close(fig)

    return {"figure": "fig_ch01_concept_von_thunen", "type": "concept", **paths}


# ------------------------------------------------------------------ #
#  Figure 2: Krugman tomahawk bifurcation diagram
# ------------------------------------------------------------------ #

def plot_core_periphery(output_dir: Path, seed: int = 42) -> dict:
    """Krugman core-periphery tomahawk bifurcation diagram."""
    fig, ax = plt.subplots(figsize=FIGSIZE_CONCEPT)

    # Trade cost parameter (phi = trade freeness, 0..1)
    phi = np.linspace(0.01, 0.99, 500)

    # Symmetric equilibrium (lambda = 0.5)
    ax.plot(phi, np.full_like(phi, 0.5), color="#377eb8", linewidth=2,
            label="Symmetric equilibrium")

    # Agglomeration equilibria (lambda = 0 and lambda = 1)
    # Stable for high phi (low trade costs)
    phi_break = 0.45  # sustain point
    phi_sustain = 0.30  # break point

    # Upper branch: lambda=1 (stable past sustain point)
    mask_upper = phi >= phi_sustain
    ax.plot(phi[mask_upper], np.ones_like(phi[mask_upper]),
            color="#e41a1c", linewidth=2, label="Core-periphery equilibrium")

    # Lower branch: lambda=0 (stable past sustain point)
    ax.plot(phi[mask_upper], np.zeros_like(phi[mask_upper]),
            color="#e41a1c", linewidth=2)

    # Unstable branches (dashed) — connecting tomahawk arms
    phi_arm = np.linspace(phi_sustain, phi_break, 100)
    # Upper unstable branch
    lam_upper = 0.5 + 0.5 * ((phi_arm - phi_sustain) / (phi_break - phi_sustain))
    ax.plot(phi_arm, lam_upper, color="#e41a1c", linewidth=1.5, linestyle="--",
            alpha=0.6)
    # Lower unstable branch
    ax.plot(phi_arm, 1 - lam_upper, color="#e41a1c", linewidth=1.5,
            linestyle="--", alpha=0.6)

    # Symmetric becomes unstable past break point
    mask_unstable = phi >= phi_break
    ax.plot(phi[mask_unstable], np.full(mask_unstable.sum(), 0.5),
            color="#377eb8", linewidth=2, linestyle="--", alpha=0.6)

    # Annotations
    ax.axvline(phi_break, color="#808080", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axvline(phi_sustain, color="#808080", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.text(phi_break, -0.08, "Break\npoint", ha="center", fontsize=6,
            color="#808080")
    ax.text(phi_sustain, -0.08, "Sustain\npoint", ha="center", fontsize=6,
            color="#808080")

    ax.annotate("Agglomeration\n(all industry in region 1)",
                xy=(0.85, 1.0), fontsize=6, ha="center", va="bottom",
                color="#e41a1c")
    ax.annotate("Symmetric\ndispersion",
                xy=(0.15, 0.5), fontsize=6, ha="center", va="bottom",
                color="#377eb8")

    ax.set_xlabel("Trade freeness (φ) →", fontsize=8)
    ax.set_ylabel("Share of industry in region 1 (λ)", fontsize=8)
    ax.set_title("Core–Periphery Model: Tomahawk Bifurcation",
                 fontsize=9, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=6, loc="upper left", frameon=False)

    add_figure_source(fig, "Krugman (1991); Fujita, Krugman & Venables (1999).")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch01_concept_core_periphery")
    plt.close(fig)

    return {"figure": "fig_ch01_concept_core_periphery", "type": "concept", **paths}


# ------------------------------------------------------------------ #
#  CLI
# ------------------------------------------------------------------ #

def main():
    parser = argparse.ArgumentParser(description="Chapter 1 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = []
    summaries.append(plot_von_thunen(output_dir, args.seed))
    summaries.append(plot_core_periphery(output_dir, args.seed))

    combined = {"chapter": 1, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch01_figures", combined)
    print("Chapter 1 figures complete.")


if __name__ == "__main__":
    main()
