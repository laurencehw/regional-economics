"""Chapter 2 conceptual diagram: Institutional quality spectrum.

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

from figure_utils import (
    FIGSIZE_CONCEPT, add_figure_source, save_figure, save_summary,
    add_common_args, get_output_dir,
)


def plot_institutional_spectrum(output_dir: Path, seed: int = 42) -> dict:
    """Institutional quality spectrum: extractive → inclusive, with examples."""
    fig, ax = plt.subplots(figsize=(FIGSIZE_CONCEPT[0], 3.5))

    # Spectrum bar
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(gradient, aspect="auto", cmap="RdYlGn",
              extent=[0, 10, 0.3, 0.7])

    # Labels at poles
    ax.text(0.3, 0.5, "Extractive", fontsize=9, fontweight="bold",
            va="center", ha="left", color="white")
    ax.text(9.7, 0.5, "Inclusive", fontsize=9, fontweight="bold",
            va="center", ha="right", color="#1a5e1a")

    # Example countries along the spectrum
    examples = [
        (0.8,  "DRC\n(colonial legacy)"),
        (2.5,  "Nigeria\n(resource curse)"),
        (4.0,  "Egypt\n(state-directed)"),
        (5.5,  "India\n(federal mixed)"),
        (7.0,  "Chile\n(market reforms)"),
        (8.5,  "Denmark\n(coordinated)"),
        (9.5,  "Singapore\n(developmental)"),
    ]

    for x, label in examples:
        ax.plot(x, 0.3, "v", color="#333333", markersize=8, clip_on=False)
        ax.text(x, 0.12, label, fontsize=5.5, ha="center", va="top",
                color="#333333")

    # Dimension labels above
    dimensions = [
        (1.5,  "Weak property\nrights"),
        (3.5,  "Limited\ncontract enforcement"),
        (5.0,  "Moderate\nregulatory quality"),
        (6.5,  "Strong rule\nof law"),
        (8.5,  "High voice &\naccountability"),
    ]
    for x, label in dimensions:
        ax.text(x, 0.85, label, fontsize=5, ha="center", va="bottom",
                color="#555555", fontstyle="italic")

    # Arrow showing direction
    ax.annotate("", xy=(9.8, 0.95), xytext=(0.2, 0.95),
                arrowprops=dict(arrowstyle="->", color="#808080", lw=1.2))
    ax.text(5.0, 1.02, "Institutional Quality →", fontsize=7,
            ha="center", va="bottom", color="#808080")

    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.1, 1.15)
    ax.axis("off")
    ax.set_title("Institutional Quality Spectrum: Extractive to Inclusive",
                 fontsize=9, fontweight="bold", pad=12)

    add_figure_source(fig, "Acemoglu & Robinson (2012); World Governance Indicators.")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    paths = save_figure(fig, output_dir, "fig_ch02_concept_institutional_spectrum")
    plt.close(fig)

    return {"figure": "fig_ch02_concept_institutional_spectrum", "type": "concept", **paths}


def main():
    parser = argparse.ArgumentParser(description="Chapter 2 figures")
    add_common_args(parser)
    args = parser.parse_args()
    output_dir = get_output_dir(args)

    summaries = [plot_institutional_spectrum(output_dir, args.seed)]
    combined = {"chapter": 2, "figures": summaries, "smoke_test": args.run_smoke_test}
    save_summary(output_dir, "ch02_figures", combined)
    print("Chapter 2 figures complete.")


if __name__ == "__main__":
    main()
