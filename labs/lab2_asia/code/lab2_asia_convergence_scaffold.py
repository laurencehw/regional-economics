"""Lab 2 scaffold for β-convergence estimation of GVC participation.

Two estimands are supported:

1. Level mode (legacy / diagnostic):
       growth in EXGR_DVA dollars
2. Share mode (preferred for Chapter 6–7 upgrading narrative):
       percentage-point growth in EXGR_DVA / EXGR

Model:
    y_{i,t} = α + β × log(x_{i,t-1}) + [year FE] + ε_{i,t}

    β < 0  → convergence (laggards catch up)
    β ≥ 0  → no convergence

Modes:
1. Smoke-test mode with synthetic data.
2. Real-data mode using a mapped panel CSV.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd
from scipy.stats import norm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lab 2 Asia β-convergence scaffold")
    parser.add_argument("--panel", type=str, default=None, help="Path to canonical panel CSV")
    parser.add_argument("--country-col", type=str, default="country")
    parser.add_argument("--year-col", type=str, default="year")
    parser.add_argument(
        "--outcome-mode",
        type=str,
        default="level",
        choices=["level", "share"],
        help="level = DVA dollar growth; share = DVA/EXGR percentage-point growth",
    )
    parser.add_argument("--dva-col", type=str, default="dva_value")
    parser.add_argument("--growth-col", type=str, default=None)
    parser.add_argument("--lag-col", type=str, default=None)
    parser.add_argument(
        "--year-fe",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Absorb year fixed effects via within-year demeaning",
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for synthetic data")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def estimate_convergence(
    growth: np.ndarray,
    log_lag: np.ndarray,
) -> Dict[str, float]:
    """Estimate β-convergence via OLS with HC1 standard errors.

    Parameters
    ----------
    growth : annual growth in percentage points (n,)
    log_lag : log of lagged level or share (n,)
    """
    n = len(growth)
    if n < 3:
        raise ValueError("Need at least 3 observations for convergence estimation.")

    X_mat = np.column_stack([np.ones(n), log_lag])
    k = X_mat.shape[1]

    beta_vec, _, _, _ = np.linalg.lstsq(X_mat, growth, rcond=None)
    alpha = float(beta_vec[0])
    beta = float(beta_vec[1])

    fitted = X_mat @ beta_vec
    e = growth - fitted
    ss_res = float(np.sum(e ** 2))
    ss_tot = float(np.sum((growth - np.mean(growth)) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    hc1_factor = n / max(n - k, 1)
    XtX = X_mat.T @ X_mat

    if np.linalg.matrix_rank(XtX) < k:
        raise ValueError("Design matrix is rank-deficient; check data.")

    XtX_inv = np.linalg.inv(XtX)
    meat = (X_mat * e[:, np.newaxis]).T @ (X_mat * e[:, np.newaxis])
    V = hc1_factor * XtX_inv @ meat @ XtX_inv
    se_beta = float(np.sqrt(V[1, 1]))

    t_stat = beta / se_beta if se_beta > 0 else 0.0
    p_value = float(2.0 * (1.0 - norm.cdf(abs(t_stat))))

    if -100.0 < beta < 0.0:
        convergence_speed = float(-np.log1p(beta / 100.0))
        half_life = float(np.log(2) / convergence_speed)
    else:
        convergence_speed = float("nan")
        half_life = float("nan")

    return {
        "alpha": alpha,
        "beta": beta,
        "se_beta": se_beta,
        "t_stat": t_stat,
        "p_value": p_value,
        "n_obs": n,
        "r_squared": r_squared,
        "convergence_speed": convergence_speed,
        "half_life_years": half_life,
    }


def demean_by_group(values: np.ndarray, groups: np.ndarray) -> np.ndarray:
    out = values.astype(float).copy()
    for g in np.unique(groups):
        mask = groups == g
        out[mask] = out[mask] - np.mean(out[mask])
    return out


def prepare_panel(
    panel_df: pd.DataFrame,
    country_col: str,
    year_col: str,
    growth_col: str,
    lag_col: str,
    year_fe: bool,
) -> pd.DataFrame:
    """Validate columns, drop NaN rows, compute log lag, optionally demean."""
    required = [country_col, year_col, growth_col, lag_col]
    missing = [c for c in required if c not in panel_df.columns]
    if missing:
        raise ValueError(f"Missing panel columns: {missing}")

    est = panel_df[[country_col, year_col, growth_col, lag_col]].copy()
    est = est.dropna(subset=[growth_col, lag_col])
    est = est.loc[est[lag_col] > 0].copy()
    est["log_lag"] = np.log(est[lag_col].astype(float))
    # Backward-compatible alias used by existing tests/plots
    est["log_dva_lag"] = est["log_lag"]

    if year_fe:
        years = est[year_col].to_numpy()
        est[growth_col] = demean_by_group(est[growth_col].to_numpy(dtype=float), years)
        est["log_lag"] = demean_by_group(est["log_lag"].to_numpy(dtype=float), years)
        est["log_dva_lag"] = est["log_lag"]

    est = est.sort_values([country_col, year_col]).reset_index(drop=True)

    if est.shape[0] < 3:
        raise ValueError("Need at least 3 observations for convergence estimation.")
    return est


def synthetic_inputs(seed: int = 42, outcome_mode: str = "level") -> pd.DataFrame:
    """Generate synthetic β-convergence data with known β = -3.0."""
    rng = np.random.default_rng(seed)
    TRUE_BETA = -3.0
    n_countries = 30
    n_years = 20
    countries = [f"C{i:02d}" for i in range(1, n_countries + 1)]

    if outcome_mode == "level":
        initial = rng.uniform(10000, 1000000, size=n_countries)
        rows = []
        for i, country in enumerate(countries):
            dva = initial[i]
            for t in range(n_years):
                year = 2000 + t
                noise = rng.normal(0.0, 0.5)
                growth_pct = 3.0 + TRUE_BETA * (np.log(dva) - np.log(100_000.0)) + noise
                rows.append({"country": country, "year": year, "dva_value": dva})
                dva = dva * (1.0 + growth_pct / 100.0)
        panel = pd.DataFrame(rows)
        panel = panel.sort_values(["country", "year"]).reset_index(drop=True)
        panel["dva_growth"] = panel.groupby("country")["dva_value"].pct_change() * 100
        panel["dva_lag"] = panel.groupby("country")["dva_value"].shift(1)
        return panel

    # Share mode: DVA/EXGR shares in (0.2, 0.9)
    initial = rng.uniform(0.25, 0.85, size=n_countries)
    rows = []
    for i, country in enumerate(countries):
        share = initial[i]
        for t in range(n_years):
            year = 2000 + t
            noise = rng.normal(0.0, 0.4)
            growth_pp = 1.5 + TRUE_BETA * (np.log(share) - np.log(0.50)) + noise
            rows.append({
                "country": country,
                "year": year,
                "dva_share": share,
                "exgr_value": 100000.0,
                "dva_value": share * 100000.0,
            })
            share = float(np.clip(share + growth_pp / 100.0, 0.05, 0.95))
    panel = pd.DataFrame(rows)
    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)
    panel["dva_share_growth"] = panel.groupby("country")["dva_share"].diff() * 100
    panel["dva_share_lag"] = panel.groupby("country")["dva_share"].shift(1)
    return panel


def resolve_columns(args: argparse.Namespace) -> tuple[str, str]:
    if args.outcome_mode == "share":
        growth = args.growth_col or "dva_share_growth"
        lag = args.lag_col or "dva_share_lag"
    else:
        growth = args.growth_col or "dva_growth"
        lag = args.lag_col or "dva_lag"
    return growth, lag


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)
    growth_col, lag_col = resolve_columns(args)

    if args.run_smoke_test:
        panel_df = synthetic_inputs(seed=args.seed, outcome_mode=args.outcome_mode)
        country_col = "country"
        year_col = "year"
    else:
        if not args.panel:
            raise ValueError("Provide --panel or use --run-smoke-test.")
        panel_df = pd.read_csv(args.panel)
        country_col = args.country_col
        year_col = args.year_col

    est_panel = prepare_panel(
        panel_df, country_col, year_col, growth_col, lag_col, year_fe=args.year_fe
    )

    growth = est_panel[growth_col].to_numpy(dtype=float)
    log_lag = est_panel["log_lag"].to_numpy(dtype=float)
    result = estimate_convergence(growth, log_lag)

    countries_in_panel = est_panel[country_col].unique().tolist()
    years_in_panel = sorted(int(y) for y in est_panel[year_col].unique())

    summary = {
        "method": "Beta_Convergence_OLS_HC1",
        "outcome_mode": args.outcome_mode,
        "estimand": (
            "percentage-point growth in EXGR_DVA/EXGR"
            if args.outcome_mode == "share"
            else "percent growth in EXGR_DVA level"
        ),
        "outcome": growth_col,
        "regressor": f"log({lag_col})",
        "year_fe": bool(args.year_fe),
        "beta": result["beta"],
        "se_beta": result["se_beta"],
        "t_stat": result["t_stat"],
        "p_value": result["p_value"],
        "r_squared": result["r_squared"],
        "half_life_years": result["half_life_years"],
        "beta_negative": result["beta"] < 0,
        # Require conventional significance; a negative point estimate alone is not "detected" convergence.
        "convergence_detected": bool(result["beta"] < 0 and result["p_value"] < 0.05),
        "n_obs": result["n_obs"],
        "n_countries": len(countries_in_panel),
        "year_range": [years_in_panel[0], years_in_panel[-1]] if years_in_panel else [],
        "mode": "synthetic_smoke_test" if args.run_smoke_test else "real_data",
    }

    est_panel.to_csv(output_dir / "estimation_panel.csv", index=False)
    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"Estimand: {summary['estimand']}")
    convergence_str = "YES" if summary["convergence_detected"] else "NO"
    print(f"Convergence: {convergence_str}")
    print(f"  beta: {summary['beta']:.4f} (se={summary['se_beta']:.4f}, p={summary['p_value']:.4f})")
    if summary["convergence_detected"] and np.isfinite(summary["half_life_years"]):
        print(f"  half-life: {summary['half_life_years']:.1f} years")


if __name__ == "__main__":
    main()
