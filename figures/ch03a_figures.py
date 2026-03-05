"""Chapter 3A conceptual diagrams: Spatial weight matrix heatmap + Moran scatter.

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


# ------------------------------------------------------------------ #
#  Figure 4: Spatial weight matrix heatmap (stylized 8-region example)
# ------------------------------------------------------------------ #

def plot_weight_matrix(output_dir: Path, seed: int = 42) -> dict:
    """8×8 spatial weight matrix heatmap with row-standardization."""
    rng = np.random.default_rng(seed)
    regions = ["A", "B", "C", "D", "E", "F", "G", "H"]
    n = len(regions)

    # Build a contiguity-style W: each region neighbors 2–3 others
    neighbors = {
        0: [1, 3],     1: [0, 2, 4],   2: [1, 5],     3: [0, 4, 6],
        4: [1, 3, 5, 7], 5: [2, 4, 7], 6: [3, 7],     7: [4, 5, 6],
    }
    W = np.zeros((n, n))
    for i, nbrs in neighbors.items():
        for j in nbrs:
            W[i, j] = 1.0

    # Row-standardize
    row_sums = W.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    W_std = W / row_sums

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FIGSIZE_CONCEPT[0], 3))

    # Binary contiguity
    im1 = ax1.imshow(W, cmap="Blues", vmin=0, vmax=1)
    ax1.set_xticks(range(n))
    ax1.set_yticks(range(n))
    ax1.set_xticklabels(regions, fontsize=7)
    ax1.set_yticklabels(regions, fontsize=7)
    ax1.set_title("Binary Contiguity (W)", fontsize=8, fontweight="bold")
    for i in range(n):
        for j in range(n):
            ax1.text(j, i, f"{W[i,j]:.0f}", ha="center", va="center",
                     fontsize=5, color="white" if W[i, j] > 0.5 else "#333333")

    # Row-standardized
    im2 = ax2.imshow(W_std, cmap="YlOrRd", vmin=0, vmax=0.6)
    ax2.set_xticks(range(n))
    ax2.set_yticks(range(n))
    ax2.set_xticklabels(regions, fontsize=7)
    ax2.set_yticklabels(regions, fontsize=7)
    ax2.set_title("Row-Standardized (W*)", fontsize=8, fontweight="bold")
    for i in range(n):
        for j in range(n):
            val = W_std[i, j]
            ax2.text(j, i, f"{val:.2f}" if val > 0 else "0",
                     ha="center", va="center", fontsize=5,
                     color="white" if val > 0.35 else "#333333")

    add_figure_source(fig, "Stylized 8-region spatial weight matrix illustration.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch03a_concept_weight_matrix")
    plt.close(fig)

    return {"figure": "fig_ch03a_concept_weight_matrix", "type": "concept", **paths}


# ------------------------------------------------------------------ #
#  Figure 5: Moran's I scatter plot with quadrant labels
# ------------------------------------------------------------------ #

def plot_moran_scatter(output_dir: Path, seed: int = 42) -> dict:
    """Moran's I scatter plot with labeled quadrants (HH, HL, LH, LL)."""
    rng = np.random.default_rng(seed)

    n = 60
    # Simulate spatially correlated data
    z = rng.normal(0, 1, n)
    wz = 0.45 * z + rng.normal(0, 0.5, n)  # Moran's I ≈ 0.45

    fig, ax = plt.subplots(figsize=FIGSIZE_CONCEPT)

    # Color by quadrant
    colors = []
    for xi, yi in zip(z, wz):
        if xi > 0 and yi > 0:
            colors.append("#e41a1c")   # HH
        elif xi < 0 and yi < 0:
            colors.append("#377eb8")   # LL
        elif xi > 0 and yi < 0:
            colors.append("#ff7f00")   # HL
        else:
            colors.append("#984ea3")   # LH

    ax.scatter(z, wz, c=colors, s=25, alpha=0.7, edgecolors="white",
               linewidths=0.3)

    # Reference lines
    ax.axhline(0, color="#808080", linestyle="--", linewidth=0.7)
    ax.axvline(0, color="#808080", linestyle="--", linewidth=0.7)

    # OLS fit line
    slope = np.polyfit(z, wz, 1)[0]
    xfit = np.linspace(z.min(), z.max(), 50)
    ax.plot(xfit, slope * xfit, color="#333333", linewidth=1.5,
            label=f"Moran's I ≈ {slope:.2f}")

    # Quadrant labels
    lim = max(abs(z).max(), abs(wz).max()) * 1.15
    ax.text(lim * 0.6, lim * 0.7, "HH\n(Hot spot)", fontsize=8,
            color="#e41a1c", fontweight="bold", ha="center")
    ax.text(-lim * 0.6, -lim * 0.7, "LL\n(Cold spot)", fontsize=8,
            color="#377eb8", fontweight="bold", ha="center")
    ax.text(lim * 0.6, -lim * 0.7, "HL\n(Spatial outlier)", fontsize=7,
            color="#ff7f00", ha="center")
    ax.text(-lim * 0.6, lim * 0.7, "LH\n(Spatial outlier)", fontsize=7,
            color="#984ea3", ha="center")

    ax.set_xlabel("Standardized value (z)", fontsize=8)
    ax.set_ylabel("Spatial lag (Wz)", fontsize=8)
    ax.set_title("Moran Scatter Plot", fontsize=9, fontweight="bold")
    ax.legend(fontsize=7, loc="lower right", frameon=False)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    add_figure_source(fig, "Anselin (1995); stylized illustration with simulated data.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch03a_concept_moran_scatter")
    plt.close(fig)

    return {"figure": "fig_ch03a_concept_moran_scatter", "type": "concept",
            "moran_i_approx": round(slope, 3), **paths}


def main():
    parser = argparse.ArgumentParser(description="Chapter 3A figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = []
    summaries.append(plot_weight_matrix(output_dir, args.seed))
    summaries.append(plot_moran_scatter(output_dir, args.seed))

    combined = {"chapter": "3A", "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch03a_figures", combined)
    print("Chapter 3A figures complete.")


if __name__ == "__main__":
    main()
