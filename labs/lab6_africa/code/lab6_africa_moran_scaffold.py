"""Lab 6 scaffold for global Moran's I on African night-lights outcomes.

This script supports two modes:
1. Smoke-test mode with synthetic data.
2. Real-data mode using mapped panel and adjacency CSV inputs.

Outputs are written to the selected output directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 6 Africa Moran's I scaffold")
    parser.add_argument("--panel", type=str, default=None, help="Path to canonical panel CSV")
    parser.add_argument("--adjacency", type=str, default=None, help="Path to canonical adjacency CSV")
    parser.add_argument("--year", type=int, default=2024, help="Cross-section year")
    parser.add_argument("--region-col", type=str, default="region")
    parser.add_argument("--neighbor-col", type=str, default="neighbor")
    parser.add_argument("--weight-col", type=str, default="weight")
    parser.add_argument("--y-col", type=str, default="night_lights_mean")
    parser.add_argument(
        "--control-cols",
        type=str,
        default="governance_score",
        help="Comma-separated controls for residual Moran's I; pass empty string for none",
    )
    parser.add_argument("--permutations", type=int, default=499, help="Permutation draws for p-value")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def parse_cols(raw: str) -> List[str]:
    return [c.strip() for c in raw.split(",") if c.strip()]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_weight_matrix(
    adjacency_df: pd.DataFrame,
    regions: List[str],
    region_col: str,
    neighbor_col: str,
    weight_col: str,
) -> np.ndarray:
    idx = {region: i for i, region in enumerate(regions)}
    n = len(regions)
    mat = np.zeros((n, n), dtype=float)

    for row in adjacency_df.itertuples(index=False):
        region = str(getattr(row, region_col))
        neighbor = str(getattr(row, neighbor_col))
        if region not in idx or neighbor not in idx or region == neighbor:
            continue
        weight = float(getattr(row, weight_col))
        if weight <= 0:
            continue
        mat[idx[region], idx[neighbor]] += weight

    # Symmetrize matrix to align with standard undirected Moran's I weighting.
    mat = 0.5 * (mat + mat.T)
    return mat


def row_standardize(mat: np.ndarray) -> np.ndarray:
    row_sums = mat.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        standardized = np.zeros_like(mat, dtype=float)
        np.divide(mat, row_sums, out=standardized, where=row_sums > 0)
    return standardized


def prepare_cross_section(
    panel_df: pd.DataFrame,
    year: int,
    region_col: str,
    y_col: str,
    control_cols: List[str],
) -> pd.DataFrame:
    required = [region_col, "year", y_col, *control_cols]
    missing = [c for c in required if c not in panel_df.columns]
    if missing:
        raise ValueError(f"Missing panel columns: {missing}")

    xsec = panel_df.loc[panel_df["year"] == year, required].copy()
    xsec = xsec.dropna(subset=[region_col, y_col]).drop_duplicates(subset=[region_col])
    if control_cols:
        xsec = xsec.dropna(subset=control_cols)

    xsec = xsec.sort_values(region_col).reset_index(drop=True)
    if xsec.shape[0] < 5:
        raise ValueError("Need at least 5 regions in the selected year for Moran diagnostics.")
    return xsec


def morans_i(y: np.ndarray, w_matrix: np.ndarray) -> Tuple[float, float]:
    n = y.shape[0]
    centered = y - np.mean(y)
    denom = float(centered @ centered)
    s0 = float(w_matrix.sum())
    if denom <= 0 or s0 <= 0:
        raise ValueError("Degenerate data or weights for Moran's I.")

    i_value = float((n / s0) * ((centered @ w_matrix @ centered) / denom))
    expected_i = float(-1.0 / (n - 1))
    return i_value, expected_i


def permutation_p_value(
    y: np.ndarray,
    w_matrix: np.ndarray,
    permutations: int,
    seed: int,
) -> Tuple[float, np.ndarray]:
    if permutations < 1:
        raise ValueError("permutations must be >= 1")

    observed, _ = morans_i(y, w_matrix)
    rng = np.random.default_rng(seed)
    draws = np.empty(permutations, dtype=float)
    for i in range(permutations):
        permuted = rng.permutation(y)
        draws[i], _ = morans_i(permuted, w_matrix)

    p_two_sided = float((1 + np.count_nonzero(np.abs(draws) >= abs(observed))) / (permutations + 1))
    return p_two_sided, draws


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    x_const = np.column_stack([np.ones(x.shape[0]), x])
    beta = np.linalg.lstsq(x_const, y, rcond=None)[0]
    return y - (x_const @ beta)


def synthetic_inputs() -> Tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)

    regions = [f"R{i:02d}" for i in range(1, 16)]
    coords = {}
    i = 0
    for r in range(3):
        for c in range(5):
            coords[regions[i]] = (r, c)
            i += 1

    edges: List[Dict[str, object]] = []
    for region, (row, col) in coords.items():
        for dr, dc in [(0, 1), (1, 0)]:
            neighbor_pos = (row + dr, col + dc)
            for candidate, pos in coords.items():
                if pos == neighbor_pos:
                    edges.append({"region": region, "neighbor": candidate, "weight": 1.0})
                    break

    adjacency_df = pd.DataFrame(edges)
    w_raw = build_weight_matrix(adjacency_df, regions, "region", "neighbor", "weight")
    w = row_standardize(w_raw)

    governance = rng.normal(loc=50.0, scale=10.0, size=len(regions))
    latent = rng.normal(0.0, 0.8, size=len(regions))
    signal = 0.08 * governance + latent
    for _ in range(6):
        signal = 0.62 * signal + 0.38 * (w @ signal) + rng.normal(0.0, 0.05, size=len(regions))

    night_lights = np.exp(2.0 + 0.22 * signal)
    panel_df = pd.DataFrame(
        {
            "region": regions,
            "year": 2024,
            "night_lights_mean": night_lights,
            "governance_score": governance,
        }
    )
    return panel_df, adjacency_df


def main() -> None:
    args = parse_args()
    control_cols = parse_cols(args.control_cols)
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    if args.run_smoke_test:
        panel_df, adjacency_df = synthetic_inputs()
    else:
        if not args.panel or not args.adjacency:
            raise ValueError("Provide --panel and --adjacency, or use --run-smoke-test.")
        panel_df = pd.read_csv(args.panel)
        adjacency_df = pd.read_csv(args.adjacency)

    xsec = prepare_cross_section(panel_df, args.year, args.region_col, args.y_col, control_cols)
    regions = xsec[args.region_col].astype(str).tolist()

    adjacency_df = adjacency_df.copy()
    adjacency_df.loc[:, args.region_col] = adjacency_df[args.region_col].astype(str)
    adjacency_df.loc[:, args.neighbor_col] = adjacency_df[args.neighbor_col].astype(str)

    w_raw = build_weight_matrix(
        adjacency_df=adjacency_df,
        regions=regions,
        region_col=args.region_col,
        neighbor_col=args.neighbor_col,
        weight_col=args.weight_col,
    )
    w = row_standardize(w_raw)

    y = xsec[args.y_col].to_numpy(dtype=float)
    i_raw, i_expected = morans_i(y, w)
    p_raw, _ = permutation_p_value(y, w, permutations=args.permutations, seed=args.seed)

    summary: Dict[str, object] = {
        "method": "Global_Morans_I",
        "n_obs": int(y.shape[0]),
        "year": int(args.year),
        "outcome": args.y_col,
        "moran_i": float(i_raw),
        "expected_i_null": float(i_expected),
        "p_value_two_sided": float(p_raw),
        "permutations": int(args.permutations),
        "controls": control_cols,
        "weight_density": float(np.count_nonzero(w) / w.size),
    }

    if control_cols:
        x = xsec[control_cols].to_numpy(dtype=float)
        resid = residualize(y, x)
        i_resid, i_expected_resid = morans_i(resid, w)
        p_resid, _ = permutation_p_value(resid, w, permutations=args.permutations, seed=args.seed + 1)
        summary.update(
            {
                "residual_moran_i": float(i_resid),
                "residual_expected_i_null": float(i_expected_resid),
                "residual_p_value_two_sided": float(p_resid),
            }
        )

    xsec.to_csv(output_dir / "cross_section_used.csv", index=False)
    pd.DataFrame(w, index=regions, columns=regions).to_csv(output_dir / "weight_matrix.csv")
    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"Moran's I (raw): {summary['moran_i']:.4f}")
    if "residual_moran_i" in summary:
        print(f"Moran's I (residual): {summary['residual_moran_i']:.4f}")


if __name__ == "__main__":
    main()
