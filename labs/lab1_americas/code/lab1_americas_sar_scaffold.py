"""Lab 1 scaffold for trade-weighted spatial lag estimation.

This script supports two modes:
1. Smoke test mode with synthetic data.
2. Real-data mode using panel and trade CSV inputs.

Outputs are written to the selected output directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

try:
    from libpysal.weights import full2W
    from spreg import ML_Lag
except Exception:  # pragma: no cover
    full2W = None
    ML_Lag = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 1 Americas SAR scaffold")
    parser.add_argument("--panel", type=str, default=None, help="Path to panel CSV")
    parser.add_argument("--trade", type=str, default=None, help="Path to trade CSV")
    parser.add_argument("--year", type=int, default=2024, help="Cross-section year")
    parser.add_argument("--region-col", type=str, default="region")
    parser.add_argument("--origin-col", type=str, default="origin")
    parser.add_argument("--destination-col", type=str, default="destination")
    parser.add_argument("--weight-col", type=str, default="trade_value")
    parser.add_argument("--y-col", type=str, default="gdp_growth")
    parser.add_argument(
        "--x-cols",
        type=str,
        default="log_gdp_pc,manufacturing_share,border_delay_index",
        help="Comma-separated covariate names",
    )
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def parse_x_cols(raw: str) -> List[str]:
    return [c.strip() for c in raw.split(",") if c.strip()]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_trade_matrix(
    trade_df: pd.DataFrame,
    regions: List[str],
    origin_col: str,
    destination_col: str,
    weight_col: str,
) -> np.ndarray:
    idx = {region: i for i, region in enumerate(regions)}
    n = len(regions)
    mat = np.zeros((n, n), dtype=float)

    for row in trade_df.itertuples(index=False):
        origin = getattr(row, origin_col)
        destination = getattr(row, destination_col)
        if origin not in idx or destination not in idx:
            continue
        if origin == destination:
            continue
        value = float(getattr(row, weight_col))
        if value < 0:
            continue
        mat[idx[origin], idx[destination]] += value

    return mat


def row_standardize(mat: np.ndarray) -> np.ndarray:
    row_sums = mat.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        standardized = np.divide(mat, row_sums, where=row_sums > 0)
    standardized[np.isnan(standardized)] = 0.0
    return standardized


def prepare_cross_section(
    panel_df: pd.DataFrame,
    year: int,
    region_col: str,
    y_col: str,
    x_cols: List[str],
) -> pd.DataFrame:
    required = [region_col, "year", y_col, *x_cols]
    missing = [c for c in required if c not in panel_df.columns]
    if missing:
        raise ValueError(f"Missing panel columns: {missing}")

    xsec = panel_df.loc[panel_df["year"] == year, required].copy()
    xsec = xsec.dropna().drop_duplicates(subset=[region_col])
    xsec = xsec.sort_values(region_col).reset_index(drop=True)

    if xsec.shape[0] < 5:
        raise ValueError("Need at least 5 regions in the selected year to estimate SAR reliably.")

    return xsec


def estimate_sar_manual(y: np.ndarray, x: np.ndarray, w_matrix: np.ndarray, x_names: List[str]) -> Dict[str, object]:
    n = y.shape[0]
    x_const = np.column_stack([np.ones(n), x])
    i_n = np.eye(n)

    eigvals = np.linalg.eigvals(w_matrix)
    max_abs = float(np.max(np.abs(np.real(eigvals)))) if eigvals.size else 0.0
    bound = 0.98 / max_abs if max_abs > 0 else 0.98
    bound = float(min(0.98, max(0.2, bound)))

    def neg_concentrated_loglike(rho: float) -> float:
        a = i_n - rho * w_matrix
        sign, logdet = np.linalg.slogdet(a)
        if sign <= 0:
            return np.inf

        ay = a @ y
        beta = np.linalg.lstsq(x_const, ay, rcond=None)[0]
        resid = ay - x_const @ beta
        sigma2 = float((resid @ resid) / n)
        if sigma2 <= 0 or not np.isfinite(sigma2):
            return np.inf

        ll = logdet - 0.5 * n * (np.log(2 * np.pi) + 1.0 + np.log(sigma2))
        return -float(ll)

    opt = minimize_scalar(
        neg_concentrated_loglike,
        bounds=(-bound, bound),
        method="bounded",
        options={"xatol": 1e-5, "maxiter": 500},
    )
    if not opt.success:
        raise RuntimeError(f"Manual SAR optimizer failed: {opt.message}")

    rho = float(opt.x)
    a = i_n - rho * w_matrix
    ay = a @ y
    beta = np.linalg.lstsq(x_const, ay, rcond=None)[0]
    resid = ay - x_const @ beta
    sigma2 = float((resid @ resid) / n)
    sign, logdet = np.linalg.slogdet(a)
    ll = float(logdet - 0.5 * n * (np.log(2 * np.pi) + 1.0 + np.log(sigma2)))

    return {
        "method": "SAR_manual_ML",
        "rho": rho,
        "betas": [float(v) for v in beta],
        "beta_names": ["intercept", *x_names],
        "sigma2": sigma2,
        "log_likelihood": ll,
        "n_obs": int(n),
    }


def run_spatial_or_fallback(
    y: np.ndarray,
    x: np.ndarray,
    w_matrix: np.ndarray,
    x_names: List[str],
) -> Dict[str, object]:
    if ML_Lag is not None and full2W is not None:
        w = full2W(w_matrix)
        model = ML_Lag(y.reshape(-1, 1), x, w=w, name_y="gdp_growth", name_x=x_names)
        return {
            "method": "SAR_ML_spreg",
            "rho": float(model.rho),
            "betas": [float(v) for v in np.asarray(model.betas).reshape(-1)],
            "n_obs": int(y.shape[0]),
        }

    try:
        return estimate_sar_manual(y=y, x=x, w_matrix=w_matrix, x_names=x_names)
    except Exception as exc:
        x_const = np.column_stack([np.ones(x.shape[0]), x])
        beta = np.linalg.lstsq(x_const, y, rcond=None)[0]
        y_hat = x_const @ beta
        rss = float(np.sum((y - y_hat) ** 2))
        tss = float(np.sum((y - y.mean()) ** 2))
        r2 = 1.0 - (rss / tss) if tss > 0 else 0.0
        return {
            "method": "OLS_fallback",
            "reason": f"SAR estimation unavailable: {exc}",
            "betas": [float(v) for v in beta],
            "beta_names": ["intercept", *x_names],
            "r_squared": r2,
            "n_obs": int(y.shape[0]),
        }


def synthetic_inputs() -> Tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    regions = [f"R{i:02d}" for i in range(1, 13)]

    trade_rows = []
    for origin in regions:
        for destination in regions:
            if origin == destination:
                continue
            trade_rows.append(
                {
                    "origin": origin,
                    "destination": destination,
                    "trade_value": float(rng.uniform(10, 200)),
                }
            )
    trade_df = pd.DataFrame(trade_rows)

    log_gdp_pc = rng.normal(10.2, 0.35, size=len(regions))
    manufacturing_share = rng.uniform(0.12, 0.38, size=len(regions))
    border_delay_index = rng.uniform(0.0, 1.0, size=len(regions))

    base_growth = (
        0.8 * (log_gdp_pc - log_gdp_pc.mean())
        + 2.2 * manufacturing_share
        - 1.1 * border_delay_index
        + rng.normal(0.0, 0.2, size=len(regions))
    )

    panel_df = pd.DataFrame(
        {
            "region": regions,
            "year": 2024,
            "gdp_growth": base_growth,
            "log_gdp_pc": log_gdp_pc,
            "manufacturing_share": manufacturing_share,
            "border_delay_index": border_delay_index,
        }
    )

    return panel_df, trade_df


def main() -> None:
    args = parse_args()
    x_cols = parse_x_cols(args.x_cols)
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    if args.run_smoke_test:
        panel_df, trade_df = synthetic_inputs()
    else:
        if not args.panel or not args.trade:
            raise ValueError("Provide --panel and --trade, or use --run-smoke-test.")
        panel_df = pd.read_csv(args.panel)
        trade_df = pd.read_csv(args.trade)

    xsec = prepare_cross_section(panel_df, args.year, args.region_col, args.y_col, x_cols)
    regions = xsec[args.region_col].astype(str).tolist()

    trade_df = trade_df.copy()
    trade_df.loc[:, args.origin_col] = trade_df[args.origin_col].astype(str)
    trade_df.loc[:, args.destination_col] = trade_df[args.destination_col].astype(str)

    w_raw = build_trade_matrix(
        trade_df=trade_df,
        regions=regions,
        origin_col=args.origin_col,
        destination_col=args.destination_col,
        weight_col=args.weight_col,
    )
    w = row_standardize(w_raw)

    y = xsec[args.y_col].to_numpy(dtype=float)
    x = xsec[x_cols].to_numpy(dtype=float)
    summary = run_spatial_or_fallback(y=y, x=x, w_matrix=w, x_names=x_cols)

    xsec.to_csv(output_dir / "cross_section_used.csv", index=False)
    pd.DataFrame(w, index=regions, columns=regions).to_csv(output_dir / "weight_matrix.csv")

    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"Estimation method: {summary['method']}")


if __name__ == "__main__":
    main()
