"""Lab 7 scaffold for PPML gravity estimation of services vs. goods trade.

This script supports two modes:
1. Smoke test mode with synthetic data.
2. Real-data mode using trade, gravity, and STRI CSV inputs.

Estimates parallel gravity models for services and goods trade via
Poisson Pseudo-Maximum Likelihood (PPML), then compares distance
elasticities and institutional-barrier coefficients.

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
    parser = argparse.ArgumentParser(
        description="Lab 7 Services Gravity PPML scaffold"
    )
    parser.add_argument("--trade", type=str, default=None, help="Path to trade CSV")
    parser.add_argument("--gravity", type=str, default=None, help="Path to gravity variables CSV")
    parser.add_argument("--stri", type=str, default=None, help="Path to STRI CSV (optional)")
    parser.add_argument("--year", type=int, default=2019, help="Cross-section year")
    parser.add_argument(
        "--gravity-vars",
        type=str,
        default="log_dist,contig,comlang_ethno,colony",
        help="Comma-separated gravity regressors",
    )
    parser.add_argument("--max-iter", type=int, default=200, help="PPML max iterations")
    parser.add_argument("--tol", type=float, default=1e-8, help="PPML convergence tolerance")
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def parse_cols(raw: str) -> List[str]:
    return [c.strip() for c in raw.split(",") if c.strip()]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ppml_estimate(
    y: np.ndarray,
    x: np.ndarray,
    x_names: List[str],
    max_iter: int = 200,
    tol: float = 1e-8,
) -> Dict[str, object]:
    """Poisson Pseudo-Maximum Likelihood estimation via IRLS.

    Estimates: E[y | x] = exp(x @ beta)
    Uses iteratively reweighted least squares (IRLS) following
    Santos Silva and Tenreyro (2006).
    """
    n, k = x.shape
    beta = np.zeros(k)

    for iteration in range(max_iter):
        eta = x @ beta
        eta = np.clip(eta, -20, 20)  # prevent overflow
        mu = np.exp(eta)

        # IRLS weight and working variable
        w = mu
        z = eta + (y - mu) / np.where(mu > 1e-10, mu, 1e-10)

        # Weighted least squares step
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

    # Final fitted values and diagnostics
    eta = x @ beta
    eta = np.clip(eta, -20, 20)
    mu = np.exp(eta)

    # Pseudo R-squared (deviance-based)
    y_safe = np.where(y > 0, y, 1e-10)
    deviance = 2 * np.sum(
        np.where(y > 0, y * np.log(y_safe / np.where(mu > 1e-10, mu, 1e-10)), 0)
        - (y - mu)
    )
    null_mu = np.mean(y)
    null_deviance = 2 * np.sum(
        np.where(y > 0, y * np.log(y_safe / null_mu), 0) - (y - null_mu)
    )
    pseudo_r2 = 1.0 - (deviance / null_deviance) if null_deviance > 0 else 0.0

    # Robust (sandwich) standard errors
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
        "pseudo_r2": float(pseudo_r2),
        "iterations": iteration + 1 if iteration < max_iter else max_iter,
        "converged": iteration < max_iter - 1,
    }


def merge_gravity_data(
    trade_df: pd.DataFrame,
    gravity_df: pd.DataFrame,
    trade_cfg: Dict,
    gravity_cfg: Dict,
) -> pd.DataFrame:
    """Merge trade flows with gravity variables."""
    trade = trade_df.rename(columns={
        trade_cfg["exporter_col"]: "exporter",
        trade_cfg["importer_col"]: "importer",
        trade_cfg["year_col"]: "year",
        trade_cfg["services_col"]: "services_trade",
    })
    if trade_cfg.get("goods_col") and trade_cfg["goods_col"] in trade_df.columns:
        trade = trade.rename(columns={trade_cfg["goods_col"]: "goods_trade"})

    gravity = gravity_df.rename(columns={
        gravity_cfg["origin_col"]: "exporter",
        gravity_cfg["destination_col"]: "importer",
        gravity_cfg["dist_col"]: "dist",
    })

    # Rename remaining gravity columns
    rename_map = {}
    for key in ["contiguity_col", "language_col", "colony_col", "legal_col"]:
        if key in gravity_cfg and gravity_cfg[key] in gravity_df.columns:
            target = key.replace("_col", "")
            target = {
                "contiguity": "contig",
                "language": "comlang_ethno",
                "colony": "colony",
                "legal": "comleg_posttrans",
            }.get(target, target)
            rename_map[gravity_cfg[key]] = target
    gravity = gravity.rename(columns=rename_map)

    merged = trade.merge(gravity, on=["exporter", "importer"], how="inner")
    merged = merged.assign(log_dist=np.log(merged["dist"].clip(lower=1)))

    return merged


def synthetic_inputs() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate synthetic trade, gravity, and STRI data for smoke testing."""
    rng = np.random.default_rng(42)

    countries = ["USA", "GBR", "DEU", "FRA", "JPN", "IND", "CHN", "KOR", "CAN", "BRA"]
    n = len(countries)

    # Synthetic gravity variables
    gravity_rows = []
    for i, orig in enumerate(countries):
        for j, dest in enumerate(countries):
            if orig == dest:
                continue
            dist = rng.uniform(500, 15000)
            contig = 1 if rng.random() < 0.15 else 0
            comlang = 1 if rng.random() < 0.2 else 0
            colony = 1 if rng.random() < 0.1 else 0
            gravity_rows.append({
                "iso_o": orig, "iso_d": dest,
                "dist": dist, "contig": contig,
                "comlang_ethno": comlang, "colony": colony,
                "comleg_posttrans": 1 if rng.random() < 0.3 else 0,
            })
    gravity_df = pd.DataFrame(gravity_rows)

    # Synthetic trade (generated from gravity model with known parameters)
    trade_rows = []
    for _, row in gravity_df.iterrows():
        log_dist = np.log(max(row["dist"], 1))
        # True DGP: services more distance-sensitive than goods
        services_eta = 8.0 - 0.9 * log_dist + 0.5 * row["contig"] + 0.4 * row["comlang_ethno"]
        goods_eta = 9.0 - 0.65 * log_dist + 0.8 * row["contig"] + 0.2 * row["comlang_ethno"]

        services_trade = max(0, rng.poisson(np.exp(np.clip(services_eta, 0, 12))))
        goods_trade = max(0, rng.poisson(np.exp(np.clip(goods_eta, 0, 12))))

        trade_rows.append({
            "exporter": row["iso_o"],
            "importer": row["iso_d"],
            "year": 2019,
            "services_trade": float(services_trade),
            "goods_trade": float(goods_trade),
        })
    trade_df = pd.DataFrame(trade_rows)

    # Synthetic STRI
    stri_rows = []
    sectors = ["telecommunications", "financial_services", "computer_services"]
    for country in countries:
        base = rng.uniform(0.1, 0.5)
        for sector in sectors:
            stri_rows.append({
                "country": country, "year": 2019,
                "sector": sector,
                "stri_score": float(np.clip(base + rng.normal(0, 0.05), 0, 1)),
            })
    stri_df = pd.DataFrame(stri_rows)

    return trade_df, gravity_df, stri_df


def main() -> None:
    args = parse_args()
    gravity_vars = parse_cols(args.gravity_vars)
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    if args.run_smoke_test:
        trade_df, gravity_df, stri_df = synthetic_inputs()
        trade_cfg = {
            "exporter_col": "exporter", "importer_col": "importer",
            "year_col": "year", "services_col": "services_trade",
            "goods_col": "goods_trade",
        }
        gravity_cfg = {
            "origin_col": "iso_o", "destination_col": "iso_d",
            "dist_col": "dist", "contiguity_col": "contig",
            "language_col": "comlang_ethno", "colony_col": "colony",
            "legal_col": "comleg_posttrans",
        }
    else:
        if not args.trade or not args.gravity:
            raise ValueError("Provide --trade and --gravity, or use --run-smoke-test.")
        trade_df = pd.read_csv(args.trade)
        gravity_df = pd.read_csv(args.gravity)

        mappings_path = Path(args.trade).parent / "source_mappings.json"
        if not mappings_path.exists():
            mappings_path = Path("labs/lab7_services/data/source_mappings.json")
        with mappings_path.open("r") as fp:
            mappings = json.load(fp)
        trade_cfg = mappings["trade"]
        gravity_cfg = mappings["gravity"]

        stri_df = pd.read_csv(args.stri) if args.stri else None

    # --- Merge and filter ---
    merged = merge_gravity_data(trade_df, gravity_df, trade_cfg, gravity_cfg)
    if "year" in merged.columns:
        merged = merged.loc[merged["year"] == args.year].copy()

    merged = merged.dropna(subset=["services_trade", "log_dist"]).copy()

    # --- Estimate services gravity ---
    available_vars = [v for v in gravity_vars if v in merged.columns]
    x_names = ["intercept"] + available_vars
    x = np.column_stack([
        np.ones(len(merged)),
        merged[available_vars].to_numpy(dtype=float),
    ])

    services_y = merged["services_trade"].to_numpy(dtype=float)
    services_result = ppml_estimate(services_y, x, x_names, args.max_iter, args.tol)
    services_result["dependent_var"] = "services_trade"
    services_result["method"] = "PPML_Gravity"

    # --- Estimate goods gravity (if available) ---
    goods_result = None
    if "goods_trade" in merged.columns:
        goods_y = merged["goods_trade"].to_numpy(dtype=float)
        goods_result = ppml_estimate(goods_y, x, x_names, args.max_iter, args.tol)
        goods_result["dependent_var"] = "goods_trade"
        goods_result["method"] = "PPML_Gravity"

    # --- Compare distance elasticities ---
    dist_idx = x_names.index("log_dist") if "log_dist" in x_names else None
    comparison = {}
    if dist_idx is not None:
        comparison["services_distance_elasticity"] = services_result["betas"][dist_idx]
        comparison["services_distance_se"] = services_result["se"][dist_idx]
        if goods_result:
            comparison["goods_distance_elasticity"] = goods_result["betas"][dist_idx]
            comparison["goods_distance_se"] = goods_result["se"][dist_idx]
            comparison["services_more_distance_sensitive"] = (
                abs(services_result["betas"][dist_idx])
                > abs(goods_result["betas"][dist_idx])
            )

    # --- Build summary ---
    summary: Dict[str, object] = {
        "method": "PPML_Gravity_Comparison",
        "year": int(args.year),
        "n_pairs": int(len(merged)),
        "services_model": services_result,
        "distance_comparison": comparison,
    }
    if goods_result:
        summary["goods_model"] = goods_result

    # --- Write outputs ---
    merged.to_csv(output_dir / "gravity_dataset.csv", index=False)
    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"Services model: n={services_result['n_obs']}, "
          f"pseudo-R²={services_result['pseudo_r2']:.4f}")
    if goods_result:
        print(f"Goods model:    n={goods_result['n_obs']}, "
              f"pseudo-R²={goods_result['pseudo_r2']:.4f}")
    if comparison.get("services_more_distance_sensitive") is not None:
        print(f"Services more distance-sensitive: "
              f"{comparison['services_more_distance_sensitive']}")


if __name__ == "__main__":
    main()
