"""Directed trade network graph + eigenvector centrality.

Teaches concepts from Ch. 6 Section 6.4: network structure of Asian GVCs.
Uses a calibrated synthetic 10x10 bilateral trade matrix (real bilateral
TiVA deferred). Eigenvector centrality via numpy power iteration (no networkx).

Smoke-test and real modes both use calibrated synthetic data by default.
A --trade-matrix flag accepts a real bilateral CSV if available.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


ECONOMIES = ["CHN", "JPN", "KOR", "IND", "IDN", "VNM", "THA", "MYS", "PHL", "SGP"]

# Calibrated bilateral trade weights (row=exporter, col=importer)
# Reflects stylized facts: CHN hub, JPN/KOR high bilateral, ASEAN integration
TRADE_TEMPLATE = {
    ("CHN", "JPN"): 140, ("CHN", "KOR"): 120, ("CHN", "VNM"): 90,
    ("CHN", "THA"): 60, ("CHN", "MYS"): 55, ("CHN", "IND"): 70,
    ("CHN", "IDN"): 50, ("CHN", "SGP"): 65, ("CHN", "PHL"): 35,
    ("JPN", "CHN"): 130, ("JPN", "KOR"): 50, ("JPN", "THA"): 45,
    ("JPN", "VNM"): 30, ("JPN", "IDN"): 25, ("JPN", "MYS"): 20,
    ("JPN", "SGP"): 18, ("JPN", "IND"): 15, ("JPN", "PHL"): 10,
    ("KOR", "CHN"): 150, ("KOR", "JPN"): 30, ("KOR", "VNM"): 55,
    ("KOR", "IND"): 15, ("KOR", "IDN"): 12, ("KOR", "MYS"): 10,
    ("KOR", "SGP"): 12, ("KOR", "THA"): 10, ("KOR", "PHL"): 8,
    ("IND", "CHN"): 20, ("IND", "SGP"): 12, ("IND", "JPN"): 8,
    ("IND", "KOR"): 10, ("IND", "VNM"): 5, ("IND", "THA"): 6,
    ("IND", "MYS"): 8, ("IND", "IDN"): 7, ("IND", "PHL"): 3,
    ("IDN", "CHN"): 30, ("IDN", "JPN"): 20, ("IDN", "SGP"): 18,
    ("IDN", "KOR"): 10, ("IDN", "IND"): 12, ("IDN", "MYS"): 9,
    ("IDN", "THA"): 7, ("IDN", "VNM"): 5, ("IDN", "PHL"): 4,
    ("VNM", "CHN"): 40, ("VNM", "JPN"): 20, ("VNM", "KOR"): 25,
    ("VNM", "THA"): 8, ("VNM", "IDN"): 5, ("VNM", "MYS"): 6,
    ("VNM", "SGP"): 4, ("VNM", "IND"): 3, ("VNM", "PHL"): 2,
    ("THA", "CHN"): 35, ("THA", "JPN"): 25, ("THA", "VNM"): 10,
    ("THA", "MYS"): 12, ("THA", "IDN"): 8, ("THA", "SGP"): 9,
    ("THA", "KOR"): 6, ("THA", "IND"): 7, ("THA", "PHL"): 5,
    ("MYS", "CHN"): 30, ("MYS", "SGP"): 25, ("MYS", "JPN"): 15,
    ("MYS", "THA"): 10, ("MYS", "IDN"): 8, ("MYS", "KOR"): 7,
    ("MYS", "VNM"): 5, ("MYS", "IND"): 6, ("MYS", "PHL"): 3,
    ("PHL", "CHN"): 15, ("PHL", "JPN"): 12, ("PHL", "SGP"): 6,
    ("PHL", "KOR"): 5, ("PHL", "THA"): 3, ("PHL", "MYS"): 3,
    ("PHL", "VNM"): 2, ("PHL", "IDN"): 2, ("PHL", "IND"): 2,
    ("SGP", "CHN"): 50, ("SGP", "MYS"): 30, ("SGP", "IDN"): 20,
    ("SGP", "JPN"): 12, ("SGP", "KOR"): 10, ("SGP", "THA"): 10,
    ("SGP", "VNM"): 8, ("SGP", "IND"): 12, ("SGP", "PHL"): 5,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trade network graph + centrality")
    parser.add_argument("--trade-matrix", type=str, default=None,
                        help="CSV with columns: exporter, importer, value")
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def build_adjacency(economies: List[str], trade_dict: Dict[Tuple[str, str], float],
                    seed: int = 42) -> np.ndarray:
    """Build adjacency matrix from trade template with small noise."""
    rng = np.random.default_rng(seed)
    n = len(economies)
    idx = {e: i for i, e in enumerate(economies)}
    A = np.zeros((n, n))
    for (exp, imp), val in trade_dict.items():
        if exp in idx and imp in idx:
            A[idx[exp], idx[imp]] = val * (1 + rng.normal(0, 0.05))
    A = np.maximum(A, 0)
    return A


def load_trade_csv(path: str, economies: List[str]) -> np.ndarray:
    """Load a bilateral trade CSV (exporter, importer, value) into adjacency matrix."""
    df = pd.read_csv(path)
    required = {"exporter", "importer", "value"}
    if not required.issubset(df.columns):
        raise ValueError(f"Trade CSV must have columns: {required}")
    idx = {e: i for i, e in enumerate(economies)}
    n = len(economies)
    A = np.zeros((n, n))
    for _, row in df.iterrows():
        e, m = row["exporter"], row["importer"]
        if e in idx and m in idx:
            A[idx[e], idx[m]] = row["value"]
    return A


def eigenvector_centrality(A: np.ndarray, max_iter: int = 1000,
                            tol: float = 1e-8) -> np.ndarray:
    """Power iteration for eigenvector centrality of a directed graph.

    Uses row-sum normalization (out-degree weighted).
    """
    n = A.shape[0]
    # Use column sums (in-degree authority) for centrality
    B = A.T  # transpose so columns of A become rows
    row_sums = B.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums > 0, row_sums, 1)
    M = B / row_sums

    v = np.ones(n) / n
    for _ in range(max_iter):
        v_new = M.T @ v
        norm = np.linalg.norm(v_new, ord=1)
        if norm > 0:
            v_new /= norm
        if np.linalg.norm(v_new - v) < tol:
            break
        v = v_new

    # Normalize to [0, 1]
    v_max = v.max()
    if v_max > 0:
        v /= v_max
    return v


def network_stats(A: np.ndarray, economies: List[str],
                  centrality: np.ndarray) -> Dict:
    """Compute network summary statistics."""
    n = len(economies)
    n_edges = int(np.count_nonzero(A))
    density = n_edges / (n * (n - 1)) if n > 1 else 0
    total_flow = float(A.sum())

    out_degree = (A > 0).sum(axis=1)
    in_degree = (A > 0).sum(axis=0)

    rankings = sorted(
        [(economies[i], float(centrality[i])) for i in range(n)],
        key=lambda x: x[1],
        reverse=True,
    )

    return {
        "n_nodes": n,
        "n_edges": n_edges,
        "density": round(density, 4),
        "total_flow": round(total_flow, 1),
        "centrality_ranking": [{"economy": e, "centrality": round(c, 4)} for e, c in rankings],
        "mean_out_degree": round(float(out_degree.mean()), 2),
        "mean_in_degree": round(float(in_degree.mean()), 2),
    }


def plot_network(A: np.ndarray, economies: List[str], centrality: np.ndarray,
                 output_path: Path) -> None:
    """Circular layout network graph with edge widths proportional to flow."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch

    n = len(economies)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radius = 3.0
    pos = {economies[i]: (radius * np.cos(angles[i]), radius * np.sin(angles[i]))
           for i in range(n)}

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)
    ax.axis("off")
    ax.set_title("Intra-Asian Trade Network\n(Edge width ∝ bilateral flow)", fontsize=11)

    # Draw edges
    max_flow = A.max() if A.max() > 0 else 1
    for i in range(n):
        for j in range(n):
            if i == j or A[i, j] <= 0:
                continue
            x0, y0 = pos[economies[i]]
            x1, y1 = pos[economies[j]]
            width = 0.3 + 2.5 * (A[i, j] / max_flow)
            alpha = 0.15 + 0.5 * (A[i, j] / max_flow)
            # Shorten arrow to avoid overlapping node
            dx, dy = x1 - x0, y1 - y0
            dist = np.sqrt(dx**2 + dy**2)
            if dist > 0:
                shrink = 0.35 / dist
                x0s = x0 + dx * shrink
                y0s = y0 + dy * shrink
                x1s = x1 - dx * shrink
                y1s = y1 - dy * shrink
            else:
                x0s, y0s, x1s, y1s = x0, y0, x1, y1
            ax.annotate(
                "", xy=(x1s, y1s), xytext=(x0s, y0s),
                arrowprops=dict(
                    arrowstyle="->,head_width=0.15,head_length=0.1",
                    lw=width, color="#4a4a4a", alpha=alpha,
                    connectionstyle="arc3,rad=0.1",
                ),
            )

    # Draw nodes
    node_sizes = 200 + 800 * centrality
    colors = ["#e41a1c" if e in ("CHN", "JPN", "KOR")
              else "#377eb8" if e in ("IDN", "MYS", "PHL", "SGP", "THA", "VNM")
              else "#4daf4a"
              for e in economies]

    for i, eco in enumerate(economies):
        x, y = pos[eco]
        ax.scatter(x, y, s=node_sizes[i], c=colors[i], zorder=5,
                   edgecolors="white", linewidths=1.5)
        ax.text(x, y - 0.5, eco, ha="center", va="top", fontsize=8, fontweight="bold")

    fig.tight_layout()
    fig.savefig(str(output_path), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Network figure saved: {output_path}")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    economies = ECONOMIES

    if args.trade_matrix:
        A = load_trade_csv(args.trade_matrix, economies)
    else:
        A = build_adjacency(economies, TRADE_TEMPLATE, seed=args.seed)

    centrality = eigenvector_centrality(A)
    stats = network_stats(A, economies, centrality)
    stats["method"] = "Trade_Network_Eigenvector_Centrality"
    stats["smoke_test"] = args.run_smoke_test or (args.trade_matrix is None)

    # Save centrality CSV
    cent_df = pd.DataFrame({
        "economy": economies,
        "eigenvector_centrality": [round(float(centrality[i]), 6) for i in range(len(economies))],
        "out_flow": [round(float(A[i, :].sum()), 1) for i in range(len(economies))],
        "in_flow": [round(float(A[:, i].sum()), 1) for i in range(len(economies))],
    })
    cent_df = cent_df.sort_values("eigenvector_centrality", ascending=False)
    cent_path = out_dir / "network_centrality.csv"
    cent_df.to_csv(cent_path, index=False)

    # Save summary JSON
    summary_path = out_dir / "network_summary.json"
    summary_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    # Plot
    try:
        plot_network(A, economies, centrality, out_dir / "trade_network.pdf")
    except ImportError:
        print("matplotlib not installed — skipping network figure")

    print(f"Centrality CSV: {cent_path}")
    print(f"Summary: {summary_path}")
    print(f"Top 3: {stats['centrality_ranking'][:3]}")


if __name__ == "__main__":
    main()
