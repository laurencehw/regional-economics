"""Lab 7 scaffold for converting STRI scores to ad-valorem tariff equivalents.

Uses the gravity model estimated in gravity_services_scaffold.py to compute
the trade-cost equivalent of STRI regulatory barriers.

Methodology:
Given a PPML gravity estimate with STRI as a regressor:
  E[trade] = exp(α + β_dist * log_dist + β_stri * stri_avg + ...)

The tariff equivalent of a one-unit STRI change is:
  τ = exp(β_stri * ΔSTRI) - 1

This can be computed for each country pair based on their bilateral
STRI difference or for each country based on their STRI level relative
to a benchmark (e.g., the sample minimum).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lab 7 STRI tariff-equivalent estimation"
    )
    parser.add_argument("--stri", type=str, default=None, help="Path to STRI CSV")
    parser.add_argument("--trade", type=str, default=None, help="Path to trade CSV")
    parser.add_argument("--gravity", type=str, default=None, help="Path to gravity CSV")
    parser.add_argument("--year", type=int, default=2019, help="Year")
    parser.add_argument(
        "--sectors",
        type=str,
        default="telecommunications,financial_services,computer_services",
        help="Comma-separated sectors to analyze",
    )
    parser.add_argument("--max-iter", type=int, default=200)
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def parse_cols(raw: str) -> List[str]:
    return [c.strip() for c in raw.split(",") if c.strip()]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ppml_estimate(
    y: np.ndarray, x: np.ndarray, x_names: List[str],
    max_iter: int = 200, tol: float = 1e-8,
) -> Dict[str, object]:
    """PPML via IRLS (duplicated from gravity scaffold for standalone use)."""
    n, k = x.shape
    beta = np.zeros(k)

    for iteration in range(max_iter):
        eta = np.clip(x @ beta, -20, 20)
        mu = np.exp(eta)
        w = mu
        z = eta + (y - mu) / np.where(mu > 1e-10, mu, 1e-10)
        w_sqrt = np.sqrt(w)
        xw = x * w_sqrt[:, None]
        zw = z * w_sqrt
        try:
            beta_new = np.linalg.lstsq(xw, zw, rcond=None)[0]
        except np.linalg.LinAlgError:
            break
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            break
        beta = beta_new

    eta = np.clip(x @ beta, -20, 20)
    mu = np.exp(eta)
    residuals = y - mu
    bread = np.linalg.pinv(x.T @ np.diag(mu) @ x)
    meat = x.T @ np.diag(residuals**2) @ x
    vcov = bread @ meat @ bread
    se = np.sqrt(np.maximum(np.diag(vcov), 0))

    return {
        "betas": [float(b) for b in beta],
        "se": [float(s) for s in se],
        "beta_names": list(x_names),
        "n_obs": int(n),
    }


def compute_tariff_equivalents(
    stri_df: pd.DataFrame,
    beta_stri: float,
    country_col: str = "country",
    score_col: str = "stri_score",
    sector_col: str = "sector",
) -> pd.DataFrame:
    """Convert STRI scores to tariff equivalents relative to the sample minimum."""
    results = []
    for sector, group in stri_df.groupby(sector_col):
        min_stri = group[score_col].min()
        for _, row in group.iterrows():
            delta = row[score_col] - min_stri
            # Tariff equivalent: exp(-β * Δ) - 1 when β < 0 gives positive cost
            tariff_eq = np.exp(-beta_stri * delta) - 1.0
            results.append({
                "country": row[country_col],
                "sector": sector,
                "stri_score": float(row[score_col]),
                "stri_delta_from_min": float(delta),
                "tariff_equivalent": float(tariff_eq),
                "tariff_equivalent_pct": float(tariff_eq * 100),
            })
    return pd.DataFrame(results)


def synthetic_inputs() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate synthetic data with STRI variation."""
    rng = np.random.default_rng(42)

    countries = ["USA", "GBR", "DEU", "FRA", "JPN", "IND", "CHN", "KOR"]
    sectors = ["telecommunications", "financial_services", "computer_services"]

    # Country-level STRI (higher = more restrictive)
    country_stri_base = {
        "USA": 0.18, "GBR": 0.14, "DEU": 0.16, "FRA": 0.22,
        "JPN": 0.28, "IND": 0.42, "CHN": 0.55, "KOR": 0.20,
    }

    stri_rows = []
    for country in countries:
        for sector in sectors:
            base = country_stri_base[country]
            stri_rows.append({
                "country": country, "year": 2019, "sector": sector,
                "stri_score": float(np.clip(base + rng.normal(0, 0.03), 0.05, 0.8)),
            })
    stri_df = pd.DataFrame(stri_rows)

    # Gravity variables
    gravity_rows = []
    for orig in countries:
        for dest in countries:
            if orig == dest:
                continue
            gravity_rows.append({
                "iso_o": orig, "iso_d": dest,
                "dist": rng.uniform(500, 15000),
                "contig": 1 if rng.random() < 0.12 else 0,
                "comlang_ethno": 1 if rng.random() < 0.18 else 0,
            })
    gravity_df = pd.DataFrame(gravity_rows)

    # Trade flows (STRI raises trade costs)
    trade_rows = []
    avg_stri = stri_df.groupby("country")["stri_score"].mean().to_dict()
    for _, row in gravity_df.iterrows():
        log_dist = np.log(max(row["dist"], 1))
        stri_o = avg_stri.get(row["iso_o"], 0.2)
        stri_d = avg_stri.get(row["iso_d"], 0.2)
        stri_avg = (stri_o + stri_d) / 2

        # True DGP: STRI reduces trade
        eta = 8.5 - 0.85 * log_dist + 0.5 * row["contig"] - 1.8 * stri_avg
        services_trade = max(0, rng.poisson(np.exp(np.clip(eta, 0, 11))))
        trade_rows.append({
            "exporter": row["iso_o"], "importer": row["iso_d"],
            "year": 2019, "services_trade": float(services_trade),
        })
    trade_df = pd.DataFrame(trade_rows)

    return trade_df, gravity_df, stri_df


def main() -> None:
    args = parse_args()
    sectors = parse_cols(args.sectors)
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    if args.run_smoke_test:
        trade_df, gravity_df, stri_df = synthetic_inputs()
    else:
        if not args.stri or not args.trade or not args.gravity:
            raise ValueError("Provide --stri, --trade, --gravity, or use --run-smoke-test.")
        trade_df = pd.read_csv(args.trade)
        gravity_df = pd.read_csv(args.gravity)
        stri_df = pd.read_csv(args.stri)

    # --- Filter ---
    if "year" in trade_df.columns:
        trade_df = trade_df.loc[trade_df["year"] == args.year].copy()
    if "year" in stri_df.columns:
        stri_df = stri_df.loc[stri_df["year"] == args.year].copy()

    # --- Compute average STRI per country ---
    avg_stri = stri_df.groupby("country")["stri_score"].mean().reset_index()
    avg_stri = avg_stri.rename(columns={"stri_score": "stri_avg"})

    # --- Merge trade + gravity + STRI ---
    # Standardize column names
    if "iso_o" in gravity_df.columns:
        gravity_df = gravity_df.rename(columns={"iso_o": "exporter", "iso_d": "importer"})

    merged = trade_df.merge(gravity_df, on=["exporter", "importer"], how="inner")
    merged = merged.merge(avg_stri.rename(columns={"country": "exporter", "stri_avg": "stri_o"}),
                          on="exporter", how="left")
    merged = merged.merge(avg_stri.rename(columns={"country": "importer", "stri_avg": "stri_d"}),
                          on="importer", how="left")
    merged = merged.assign(
        stri_avg=(merged["stri_o"].fillna(0) + merged["stri_d"].fillna(0)) / 2,
        log_dist=np.log(merged["dist"].clip(lower=1)),
    )
    merged = merged.dropna(subset=["services_trade", "log_dist", "stri_avg"]).copy()

    if merged.empty:
        raise ValueError("No observations after merging trade, gravity, and STRI.")

    # --- PPML with STRI ---
    x_names = ["intercept", "log_dist", "stri_avg"]
    x_cols = ["log_dist", "stri_avg"]
    if "contig" in merged.columns:
        x_cols.append("contig")
        x_names.append("contig")
    if "comlang_ethno" in merged.columns:
        x_cols.append("comlang_ethno")
        x_names.append("comlang_ethno")

    x = np.column_stack([
        np.ones(len(merged)),
        merged[x_cols].to_numpy(dtype=float),
    ])
    y = merged["services_trade"].to_numpy(dtype=float)

    result = ppml_estimate(y, x, x_names, args.max_iter)

    # --- Extract STRI coefficient and compute tariff equivalents ---
    stri_idx = x_names.index("stri_avg")
    beta_stri = result["betas"][stri_idx]
    se_stri = result["se"][stri_idx]

    tariff_df = compute_tariff_equivalents(
        stri_df.loc[stri_df["sector"].isin(sectors)],
        beta_stri=beta_stri,
    )

    # --- Summary ---
    summary: Dict[str, object] = {
        "method": "STRI_Tariff_Equivalent",
        "year": int(args.year),
        "n_pairs": int(len(merged)),
        "ppml_result": result,
        "stri_coefficient": float(beta_stri),
        "stri_se": float(se_stri),
        "stri_significant_5pct": abs(beta_stri / se_stri) > 1.96 if se_stri > 0 else False,
        "sectors_analyzed": sectors,
        "tariff_equivalent_summary": {
            "mean_pct": float(tariff_df["tariff_equivalent_pct"].mean()),
            "max_pct": float(tariff_df["tariff_equivalent_pct"].max()),
            "max_country": tariff_df.loc[
                tariff_df["tariff_equivalent_pct"].idxmax(), "country"
            ],
        },
    }

    # --- Write ---
    tariff_df.to_csv(output_dir / "tariff_equivalents.csv", index=False)
    merged.to_csv(output_dir / "gravity_stri_dataset.csv", index=False)
    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"STRI coefficient: {beta_stri:.4f} (SE: {se_stri:.4f})")
    print(f"Mean tariff equivalent: {summary['tariff_equivalent_summary']['mean_pct']:.1f}%")
    print(f"Most restrictive: {summary['tariff_equivalent_summary']['max_country']} "
          f"({summary['tariff_equivalent_summary']['max_pct']:.1f}%)")


if __name__ == "__main__":
    main()
