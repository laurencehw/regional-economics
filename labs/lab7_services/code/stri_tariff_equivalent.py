"""Lab 7 scaffold for converting STRI scores to ad-valorem tariff equivalents.

Identification note
-------------------
An importer-only STRI regressor is collinear with importer fixed effects.
This script therefore uses an identified sector-disaggregated design:

  E[trade_ijs] = exp(
      exporter FE_i
      + sector FE_s
      + β_dist * log_dist_ij
      + β_stri * STRI_js
      + bilateral controls
  )

Importer STRI varies across sectors within destinations, so β_stri is identified
without importer FE. The design matches the Chapter 3-B correction.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from ppml_estimator import build_fixed_effects, ppml_estimate


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
            # With β_stri < 0, exp(-β * Δ) - 1 gives a positive cost for higher STRI
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
    """Generate sector-disaggregated synthetic data with identified STRI variation."""
    rng = np.random.default_rng(42)

    countries = ["USA", "GBR", "DEU", "FRA", "JPN", "IND", "CHN", "KOR"]
    sectors = ["telecommunications", "financial_services", "computer_services"]

    country_stri_base = {
        "USA": 0.18, "GBR": 0.14, "DEU": 0.16, "FRA": 0.22,
        "JPN": 0.28, "IND": 0.42, "CHN": 0.55, "KOR": 0.20,
    }
    sector_shift = {
        "telecommunications": -0.02,
        "financial_services": 0.04,
        "computer_services": -0.05,
    }

    stri_rows = []
    for country in countries:
        for sector in sectors:
            base = country_stri_base[country] + sector_shift[sector]
            stri_rows.append({
                "country": country,
                "year": 2019,
                "sector": sector,
                "stri_score": float(np.clip(base + rng.normal(0, 0.02), 0.05, 0.8)),
            })
    stri_df = pd.DataFrame(stri_rows)

    gravity_rows = []
    for orig in countries:
        for dest in countries:
            if orig == dest:
                continue
            gravity_rows.append({
                "iso_o": orig,
                "iso_d": dest,
                "dist": rng.uniform(500, 15000),
                "contig": 1 if rng.random() < 0.12 else 0,
                "comlang_ethno": 1 if rng.random() < 0.18 else 0,
            })
    gravity_df = pd.DataFrame(gravity_rows)

    stri_lookup = {
        (row["country"], row["sector"]): row["stri_score"]
        for _, row in stri_df.iterrows()
    }

    trade_rows = []
    for _, row in gravity_df.iterrows():
        log_dist = np.log(max(row["dist"], 1))
        for sector in sectors:
            stri_d = stri_lookup[(row["iso_d"], sector)]
            eta = (
                8.0
                - 0.85 * log_dist
                + 0.45 * row["contig"]
                + 0.35 * row["comlang_ethno"]
                - 1.6 * stri_d
            )
            services_trade = max(0, rng.poisson(np.exp(np.clip(eta, 0, 11))))
            trade_rows.append({
                "exporter": row["iso_o"],
                "importer": row["iso_d"],
                "year": 2019,
                "sector": sector,
                "services_trade": float(services_trade),
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

    if "year" in trade_df.columns:
        trade_df = trade_df.loc[trade_df["year"] == args.year].copy()
    if "year" in stri_df.columns:
        stri_df = stri_df.loc[stri_df["year"] == args.year].copy()

    if "sector" not in trade_df.columns:
        raise ValueError(
            "STRI identification requires sector-disaggregated trade. "
            "Provide a sector column or use --run-smoke-test."
        )

    trade_df = trade_df.loc[trade_df["sector"].isin(sectors)].copy()
    stri_df = stri_df.loc[stri_df["sector"].isin(sectors)].copy()

    if "iso_o" in gravity_df.columns:
        gravity_df = gravity_df.rename(columns={"iso_o": "exporter", "iso_d": "importer"})

    merged = trade_df.merge(gravity_df, on=["exporter", "importer"], how="inner")
    merged = merged.merge(
        stri_df.rename(columns={
            "country": "importer",
            "stri_score": "stri_importer",
        })[["importer", "sector", "stri_importer"]],
        on=["importer", "sector"],
        how="inner",
    )
    merged = merged.assign(log_dist=np.log(merged["dist"].clip(lower=1)))
    merged = merged.dropna(
        subset=["services_trade", "log_dist", "stri_importer"]
    ).copy()

    if merged.empty:
        raise ValueError("No observations after merging trade, gravity, and STRI.")

    # Identified design: exporter FE + sector FE + importer STRI (no importer FE)
    covars = ["log_dist", "stri_importer"]
    for optional in ("contig", "comlang_ethno"):
        if optional in merged.columns:
            covars.append(optional)

    exp_fe, exp_names = build_fixed_effects(
        merged["exporter"].to_numpy(), "exporter", drop_first=True
    )
    sec_fe, sec_names = build_fixed_effects(
        merged["sector"].to_numpy(), "sector", drop_first=True
    )

    x = np.column_stack([
        merged[covars].to_numpy(dtype=float),
        exp_fe,
        sec_fe,
    ])
    x_names = covars + exp_names + sec_names
    y = merged["services_trade"].to_numpy(dtype=float)
    cluster = (
        merged["exporter"].astype(str) + "_" + merged["importer"].astype(str)
    ).to_numpy()

    result = ppml_estimate(y, x, x_names, args.max_iter, cluster=cluster)

    stri_idx = x_names.index("stri_importer")
    beta_stri = result["betas"][stri_idx]
    se_stri = result["se"][stri_idx]

    tariff_df = compute_tariff_equivalents(stri_df, beta_stri=beta_stri)

    summary: Dict[str, object] = {
        "method": "STRI_Tariff_Equivalent",
        "identification": (
            "sector-disaggregated trade; exporter FE + sector FE; "
            "importer-sector STRI (no importer FE)"
        ),
        "year": int(args.year),
        "n_pairs": int(len(merged)),
        "n_zeros": int(result["n_zeros"]),
        "zero_share": float(result["zero_share"]),
        "converged": bool(result["converged"]),
        "ppml_result": result,
        "stri_coefficient": float(beta_stri),
        "stri_se": float(se_stri),
        "stri_significant_5pct": (
            abs(beta_stri / se_stri) > 1.96 if se_stri > 0 else False
        ),
        "sectors_analyzed": sectors,
        "mode": "synthetic_smoke_test" if args.run_smoke_test else "real_data",
        "tariff_equivalent_summary": {
            "mean_pct": float(tariff_df["tariff_equivalent_pct"].mean()),
            "max_pct": float(tariff_df["tariff_equivalent_pct"].max()),
            "max_country": tariff_df.loc[
                tariff_df["tariff_equivalent_pct"].idxmax(), "country"
            ],
        },
    }

    tariff_df.to_csv(output_dir / "tariff_equivalents.csv", index=False)
    merged.to_csv(output_dir / "gravity_stri_dataset.csv", index=False)
    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"STRI coefficient: {beta_stri:.4f} (SE: {se_stri:.4f})")
    print(f"Converged: {result['converged']}; zeros: {result['zero_share']:.1%}")
    print(f"Mean tariff equivalent: {summary['tariff_equivalent_summary']['mean_pct']:.1f}%")
    print(
        f"Most restrictive: {summary['tariff_equivalent_summary']['max_country']} "
        f"({summary['tariff_equivalent_summary']['max_pct']:.1f}%)"
    )


if __name__ == "__main__":
    main()
