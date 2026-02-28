"""Lab 7 servicification decomposition of manufacturing exports.

Decomposes the service value-added content embedded in manufacturing
exports using OECD TiVA-style data.  For each country-sector pair the
servicification share is defined as:

    servicification_share = service_va / total_va

where *service_va* is the value added by a specific service category
(finance, logistics, R&D, etc.) embodied in a manufacturing sector's
gross exports, and *total_va* is the total domestic value added in
that sector.

Supports two modes:
1. Smoke test with synthetic TiVA-style data for 10 countries.
2. Real-data mode using a TiVA CSV with columns:
   country, year, sector, service_type, service_va, total_va
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lab 7 TiVA servicification decomposition"
    )
    parser.add_argument("--tiva", type=str, default=None, help="Path to TiVA CSV")
    parser.add_argument("--year", type=int, default=2018, help="Cross-section year")
    parser.add_argument("--output-dir", type=str, default="../data")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------ #
#  Synthetic data generation
# ------------------------------------------------------------------ #

COUNTRIES = ["USA", "DEU", "JPN", "KOR", "CHN", "IND", "MEX", "VNM", "BRA", "GBR"]
MFG_SECTORS = ["automobiles", "electronics", "chemicals", "textiles", "machinery"]
SERVICE_TYPES = ["finance", "logistics", "R&D", "marketing", "ICT", "management"]

# Calibrated servicification shares (service VA / total VA) --
# high-income diversified economies have higher embedded service content.
_BASE_SHARES: Dict[str, Dict[str, float]] = {
    "USA":  {"automobiles": 0.40, "electronics": 0.50, "chemicals": 0.35,
             "textiles": 0.25, "machinery": 0.38},
    "DEU":  {"automobiles": 0.45, "electronics": 0.38, "chemicals": 0.33,
             "textiles": 0.22, "machinery": 0.42},
    "JPN":  {"automobiles": 0.38, "electronics": 0.42, "chemicals": 0.30,
             "textiles": 0.20, "machinery": 0.40},
    "KOR":  {"automobiles": 0.32, "electronics": 0.35, "chemicals": 0.28,
             "textiles": 0.18, "machinery": 0.33},
    "CHN":  {"automobiles": 0.22, "electronics": 0.25, "chemicals": 0.20,
             "textiles": 0.16, "machinery": 0.23},
    "IND":  {"automobiles": 0.20, "electronics": 0.22, "chemicals": 0.18,
             "textiles": 0.14, "machinery": 0.19},
    "MEX":  {"automobiles": 0.20, "electronics": 0.23, "chemicals": 0.17,
             "textiles": 0.13, "machinery": 0.18},
    "VNM":  {"automobiles": 0.16, "electronics": 0.20, "chemicals": 0.14,
             "textiles": 0.15, "machinery": 0.16},
    "BRA":  {"automobiles": 0.24, "electronics": 0.22, "chemicals": 0.20,
             "textiles": 0.15, "machinery": 0.21},
    "GBR":  {"automobiles": 0.42, "electronics": 0.46, "chemicals": 0.34,
             "textiles": 0.24, "machinery": 0.37},
}

# How the aggregate service share distributes across service types.
# Shares are approximate and sum to 1.
_SERVICE_MIX: Dict[str, float] = {
    "finance":    0.22,
    "logistics":  0.20,
    "R&D":        0.18,
    "marketing":  0.14,
    "ICT":        0.16,
    "management": 0.10,
}


def synthetic_tiva(year: int = 2018) -> pd.DataFrame:
    """Generate a synthetic TiVA-style panel for smoke testing."""
    rng = np.random.default_rng(42)
    rows: List[Dict] = []

    for country in COUNTRIES:
        for sector in MFG_SECTORS:
            base_share = _BASE_SHARES[country][sector]
            # Total VA drawn from a plausible range (billions USD)
            total_va = float(rng.uniform(5, 80))

            for svc_type in SERVICE_TYPES:
                mix_weight = _SERVICE_MIX[svc_type]
                # Small noise so rows are not perfectly deterministic
                noise = rng.normal(0, 0.015)
                share = float(np.clip(base_share * mix_weight + noise, 0.005, 0.95))
                service_va = float(total_va * share)

                rows.append({
                    "country": country,
                    "year": year,
                    "sector": sector,
                    "service_type": svc_type,
                    "service_va": round(service_va, 4),
                    "total_va": round(total_va, 4),
                })

    return pd.DataFrame(rows)


# ------------------------------------------------------------------ #
#  Decomposition logic
# ------------------------------------------------------------------ #

def compute_servicification(df: pd.DataFrame) -> pd.DataFrame:
    """Add servicification_share = service_va / total_va."""
    out = df.copy()
    out = out.assign(
        servicification_share=(df["service_va"] / df["total_va"]).clip(0, 1)
    )
    return out


def aggregate_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """Weighted-average servicification share by country."""
    grouped = df.groupby("country").apply(
        lambda g: pd.Series({
            "total_service_va": g["service_va"].sum(),
            "total_va": g["total_va"].sum(),
            "servicification_share": g["service_va"].sum() / g["total_va"].sum(),
        }),
        include_groups=False,
    ).reset_index()
    return grouped.sort_values("servicification_share", ascending=False)


def aggregate_by_sector(df: pd.DataFrame) -> pd.DataFrame:
    """Weighted-average servicification share by manufacturing sector."""
    grouped = df.groupby("sector").apply(
        lambda g: pd.Series({
            "total_service_va": g["service_va"].sum(),
            "total_va": g["total_va"].sum(),
            "servicification_share": g["service_va"].sum() / g["total_va"].sum(),
        }),
        include_groups=False,
    ).reset_index()
    return grouped.sort_values("servicification_share", ascending=False)


def aggregate_by_service_type(df: pd.DataFrame) -> pd.DataFrame:
    """Total VA contribution by service category."""
    grouped = df.groupby("service_type").apply(
        lambda g: pd.Series({
            "total_service_va": g["service_va"].sum(),
            "total_va": g["total_va"].sum(),
            "servicification_share": g["service_va"].sum() / g["total_va"].sum(),
        }),
        include_groups=False,
    ).reset_index()
    return grouped.sort_values("servicification_share", ascending=False)


def build_summary(
    panel: pd.DataFrame,
    by_country: pd.DataFrame,
    by_sector: pd.DataFrame,
    by_service: pd.DataFrame,
    year: int,
) -> Dict:
    """Build JSON-serializable summary dictionary."""
    countries = sorted(panel["country"].unique().tolist())
    sectors = sorted(panel["sector"].unique().tolist())
    service_types = sorted(panel["service_type"].unique().tolist())

    # Cross-country ranking
    ranking = (
        by_country[["country", "servicification_share"]]
        .sort_values("servicification_share", ascending=False)
    )
    top = ranking.iloc[0]
    bottom = ranking.iloc[-1]

    return {
        "method": "TiVA_Servicification_Decomposition",
        "year": int(year),
        "n_countries": len(countries),
        "n_sectors": len(sectors),
        "n_service_types": len(service_types),
        "n_obs": int(len(panel)),
        "countries": countries,
        "sectors": sectors,
        "service_types": service_types,
        "overall_servicification_share": float(
            panel["service_va"].sum() / panel["total_va"].sum()
        ),
        "country_ranking": ranking.to_dict(orient="records"),
        "most_servicified": {
            "country": str(top["country"]),
            "share": float(top["servicification_share"]),
        },
        "least_servicified": {
            "country": str(bottom["country"]),
            "share": float(bottom["servicification_share"]),
        },
        "sector_summary": by_sector[["sector", "servicification_share"]].to_dict(
            orient="records"
        ),
        "service_type_summary": by_service[
            ["service_type", "servicification_share"]
        ].to_dict(orient="records"),
    }


# ------------------------------------------------------------------ #
#  Main
# ------------------------------------------------------------------ #

def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    # --- Load data ---
    if args.run_smoke_test:
        raw = synthetic_tiva(year=args.year)
    else:
        if not args.tiva:
            raise ValueError("Provide --tiva path to a TiVA CSV, or use --run-smoke-test.")
        raw = pd.read_csv(args.tiva)

    # --- Filter to requested year ---
    if "year" in raw.columns:
        raw = raw.loc[raw["year"] == args.year].copy()

    if raw.empty:
        raise ValueError(f"No observations for year {args.year}.")

    # --- Compute servicification shares ---
    panel = compute_servicification(raw)
    by_country = aggregate_by_country(panel)
    by_sector = aggregate_by_sector(panel)
    by_service = aggregate_by_service_type(panel)

    summary = build_summary(panel, by_country, by_sector, by_service, args.year)

    # --- Write outputs ---
    panel.to_csv(output_dir / "servicification_panel.csv", index=False)
    with (output_dir / "servicification_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    # --- Print human-readable summary ---
    print(f"Wrote outputs to: {output_dir}")
    print(f"Year: {args.year}  |  Countries: {summary['n_countries']}  |  "
          f"Sectors: {summary['n_sectors']}  |  Service types: {summary['n_service_types']}")
    print(f"Overall servicification share: {summary['overall_servicification_share']:.3f}")
    print(f"Most servicified:  {summary['most_servicified']['country']} "
          f"({summary['most_servicified']['share']:.3f})")
    print(f"Least servicified: {summary['least_servicified']['country']} "
          f"({summary['least_servicified']['share']:.3f})")
    print("\n--- Country ranking ---")
    for row in summary["country_ranking"]:
        print(f"  {row['country']:5s}  {row['servicification_share']:.3f}")
    print("\n--- Sector summary ---")
    for row in summary["sector_summary"]:
        print(f"  {row['sector']:15s}  {row['servicification_share']:.3f}")


if __name__ == "__main__":
    main()
