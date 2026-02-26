"""Lab 4 scaffold for sharp RDD estimation of EU Cohesion Fund effects.

This script supports two modes:
1. Smoke-test mode with synthetic data (known treatment effect).
2. Real-data mode using a mapped panel CSV.

Outputs are written to the selected output directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from scipy.stats import norm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 4 Europe RDD scaffold")
    parser.add_argument("--panel", type=str, default=None, help="Path to canonical panel CSV")
    parser.add_argument("--year", type=int, default=2022, help="Cross-section year for RDD")
    parser.add_argument("--region-col", type=str, default="nuts2_code")
    parser.add_argument("--outcome-col", type=str, default="gdp_growth")
    parser.add_argument("--forcing-col", type=str, default="forcing_var")
    parser.add_argument("--treatment-col", type=str, default="treated")
    parser.add_argument("--bandwidth-frac", type=float, default=0.5,
                        help="Bandwidth as fraction of forcing variable range")
    parser.add_argument("--kernel", type=str, default="triangular",
                        choices=["triangular", "uniform"],
                        help="Kernel for local weighting")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for synthetic data")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def triangular_kernel(x: np.ndarray, bandwidth: float) -> np.ndarray:
    """Return triangular kernel weights: K(u) = (1 - |u|) for |u| <= 1, else 0."""
    u = x / bandwidth
    weights = np.maximum(1.0 - np.abs(u), 0.0)
    return weights


def uniform_kernel(x: np.ndarray, bandwidth: float) -> np.ndarray:
    """Return uniform kernel weights: 1 if |x| <= bandwidth, else 0."""
    return np.where(np.abs(x) <= bandwidth, 1.0, 0.0)


def select_bandwidth(forcing: np.ndarray, frac: float) -> float:
    """Simple rule-of-thumb bandwidth: fraction of the forcing variable range."""
    fv_range = float(np.max(forcing) - np.min(forcing))
    bw = frac * fv_range
    if bw <= 0:
        raise ValueError("Bandwidth must be positive; check forcing variable range.")
    return bw


def estimate_rdd(
    y: np.ndarray,
    x: np.ndarray,
    d: np.ndarray,
    weights: np.ndarray,
) -> Dict[str, float]:
    """Estimate sharp RDD via weighted OLS with HC1 standard errors.

    Parameters
    ----------
    y : outcome vector (n,)
    x : forcing variable, centered at cutoff (n,)
    d : treatment indicator (n,)
    weights : kernel weights (n,)

    Returns
    -------
    dict with keys: tau, se_tau, t_stat, p_value, n_obs, n_effective
    """
    mask = weights > 0
    y_w, x_w, d_w, w = y[mask], x[mask], d[mask], weights[mask]
    n = int(y_w.shape[0])
    if n < 5:
        raise ValueError("Fewer than 5 observations in RDD bandwidth window.")

    # Build design matrix: [1, D, X, D*X]
    X_mat = np.column_stack([
        np.ones(n),
        d_w,
        x_w,
        d_w * x_w,
    ])
    k = X_mat.shape[1]

    # Weighted OLS: W^{1/2} X, W^{1/2} y
    sqrt_w = np.sqrt(w)
    Xw = X_mat * sqrt_w[:, np.newaxis]
    yw = y_w * sqrt_w

    beta, _, _, _ = np.linalg.lstsq(Xw, yw, rcond=None)

    # tau is coefficient on D (index 1)
    tau = float(beta[1])

    # HC1 robust standard errors
    e = yw - Xw @ beta
    hc1_factor = n / max(n - k, 1)
    XwX = Xw.T @ Xw

    if np.linalg.matrix_rank(XwX) < k:
        raise ValueError("Design matrix is rank-deficient; check bandwidth or data.")

    XwX_inv = np.linalg.inv(XwX)
    meat = (Xw * e[:, np.newaxis]).T @ (Xw * e[:, np.newaxis])
    V = hc1_factor * XwX_inv @ meat @ XwX_inv
    se_tau = float(np.sqrt(V[1, 1]))

    t_stat = tau / se_tau if se_tau > 0 else 0.0
    p_value = float(2.0 * (1.0 - norm.cdf(abs(t_stat))))

    n_effective = float(np.sum(w))

    return {
        "tau": tau,
        "se_tau": se_tau,
        "t_stat": t_stat,
        "p_value": p_value,
        "n_obs": n,
        "n_effective": n_effective,
    }


def prepare_cross_section(
    panel_df: pd.DataFrame,
    year: int,
    region_col: str,
    outcome_col: str,
    forcing_col: str,
    treatment_col: str,
) -> pd.DataFrame:
    """Select a single-year cross section and validate columns."""
    required = [region_col, "year", outcome_col, forcing_col, treatment_col]
    missing = [c for c in required if c not in panel_df.columns]
    if missing:
        raise ValueError(f"Missing panel columns: {missing}")

    xsec = panel_df.loc[panel_df["year"] == year, required].copy()
    xsec = xsec.dropna(subset=[region_col, outcome_col, forcing_col, treatment_col])
    xsec = xsec.drop_duplicates(subset=[region_col])
    xsec = xsec.sort_values(region_col).reset_index(drop=True)

    if xsec.shape[0] < 5:
        raise ValueError("Need at least 5 regions in the selected year for RDD estimation.")
    return xsec


def synthetic_inputs(seed: int = 42) -> pd.DataFrame:
    """Generate synthetic RDD data with a known treatment effect of +2.0.

    Creates 40 regions: 20 treated (forcing_var < 0) and 20 control (forcing_var > 0).
    The forcing variable is uniformly spread around the cutoff.
    The outcome is: y = 3.0 + 2.0*D + 0.5*X + 0.3*D*X + noise
    where D=1 if X<0 (treated), X is the forcing variable.
    """
    rng = np.random.default_rng(seed)
    n = 40
    TRUE_TAU = 2.0

    forcing = np.concatenate([
        rng.uniform(-10.0, -0.5, size=n // 2),
        rng.uniform(0.5, 10.0, size=n // 2),
    ])
    treated = (forcing < 0).astype(float)

    noise = rng.normal(0.0, 0.5, size=n)
    gdp_growth = 3.0 + TRUE_TAU * treated + 0.5 * forcing + 0.3 * treated * forcing + noise

    regions = [f"XX{i:02d}" for i in range(1, n + 1)]

    panel = pd.DataFrame({
        "nuts2_code": regions,
        "year": 2022,
        "gdp_mio_eur": rng.uniform(5000, 50000, size=n),
        "gdp_growth": gdp_growth,
        "forcing_var": forcing,
        "treated": treated.astype(int),
    })
    return panel


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    if args.run_smoke_test:
        panel_df = synthetic_inputs(seed=args.seed)
    else:
        if not args.panel:
            raise ValueError("Provide --panel or use --run-smoke-test.")
        panel_df = pd.read_csv(args.panel)

    xsec = prepare_cross_section(
        panel_df, args.year, args.region_col,
        args.outcome_col, args.forcing_col, args.treatment_col,
    )

    forcing = xsec[args.forcing_col].to_numpy(dtype=float)
    outcome = xsec[args.outcome_col].to_numpy(dtype=float)
    treatment = xsec[args.treatment_col].to_numpy(dtype=float)

    bandwidth = select_bandwidth(forcing, args.bandwidth_frac)

    if args.kernel == "triangular":
        weights = triangular_kernel(forcing, bandwidth)
    else:
        weights = uniform_kernel(forcing, bandwidth)

    result = estimate_rdd(outcome, forcing, treatment, weights)

    summary = {
        "method": "Sharp_RDD_Local_Linear",
        "year": int(args.year),
        "outcome": args.outcome_col,
        "forcing": args.forcing_col,
        "tau": result["tau"],
        "se_tau": result["se_tau"],
        "t_stat": result["t_stat"],
        "p_value": result["p_value"],
        "bandwidth": float(bandwidth),
        "bandwidth_frac": float(args.bandwidth_frac),
        "kernel": args.kernel,
        "n_obs": result["n_obs"],
        "n_effective": result["n_effective"],
    }

    xsec.to_csv(output_dir / "rdd_sample.csv", index=False)
    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"RDD tau: {summary['tau']:.4f} (se={summary['se_tau']:.4f}, p={summary['p_value']:.4f})")


if __name__ == "__main__":
    main()
