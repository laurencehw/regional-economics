"""Fetch WTO BOP-based bilateral services trade data.

Outputs
-------
``labs/lab7_services/data/wto_services_bilateral.csv`` (from --local-csv)
``labs/lab7_services/data/wto_services_trade_synthetic.csv`` (from --smoke-test)
  Long-format panel with columns: exporter, importer, year,
  service_category, trade_value
  Compatible with ``labs/lab7_services/data/source_mappings.json``
  (exporter_col: "exporter", importer_col: "importer", year_col: "year").

DATA SOURCE
-----------
WTO Statistics — Trade in Services (BPM6)
  - Bilateral services trade by mode of supply / service category
  - Coverage: 150+ WTO members
  - URL: https://stats.wto.org/
  - Trade values in millions of current USD

DOWNLOAD INSTRUCTIONS
---------------------
1. Go to https://stats.wto.org/ and select "Trade in services".
2. Choose "Exports" or "Imports", bilateral, by service category.
3. Select countries, partners, and years of interest.
4. Export as CSV.
5. Pass the downloaded CSV path to --local-csv.

Use --smoke-test to generate a synthetic bilateral services trade panel
for CI/testing without downloading anything.

USAGE EXAMPLES
--------------
Smoke test (no download needed):
  python scripts/fetch_wto_services_trade.py --smoke-test

Process a pre-downloaded CSV:
  python scripts/fetch_wto_services_trade.py --local-csv path/to/wto_services.csv
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Country and category definitions
# ---------------------------------------------------------------------------

MAJOR_TRADERS: List[str] = [
    "USA", "GBR", "DEU", "FRA", "JPN", "CHN", "IND", "KOR",
    "CAN", "AUS", "NLD", "IRL", "SGP", "CHE", "ITA",
    "ESP", "BRA", "RUS", "HKG", "BEL",
]

SERVICE_CATEGORIES: List[str] = [
    "total_services",
    "transport",
    "travel",
    "financial",
    "telecom",
    "other_business",
]

# Approximate total services exports (millions USD, ~2020 magnitudes).
# Calibrated from WTO/UNCTAD trade-in-services statistics.
EXPORT_SCALE: Dict[str, float] = {
    "USA": 710_000, "GBR": 390_000, "DEU": 330_000, "FRA": 280_000,
    "JPN": 200_000, "CHN": 280_000, "IND": 240_000, "KOR": 100_000,
    "CAN": 95_000, "AUS": 65_000, "NLD": 230_000, "IRL": 260_000,
    "SGP": 200_000, "CHE": 140_000, "ITA": 115_000,
    "ESP": 130_000, "BRA": 35_000, "RUS": 55_000, "HKG": 110_000,
    "BEL": 120_000,
}

# Share of each category in total services exports (approximate global averages).
CATEGORY_SHARES: Dict[str, float] = {
    "total_services": 1.00,
    "transport": 0.18,
    "travel": 0.22,
    "financial": 0.12,
    "telecom": 0.10,
    "other_business": 0.38,
}

# Partner gravity weights: trade-weighted share of exports going to each
# partner (approximate, for generating plausible bilateral flows).
# These are relative attractiveness weights, not exact shares.
GDP_WEIGHTS: Dict[str, float] = {
    "USA": 25.0, "CHN": 18.0, "JPN": 5.0, "DEU": 4.5, "GBR": 3.5,
    "IND": 3.5, "FRA": 3.2, "ITA": 2.3, "CAN": 2.2, "KOR": 2.0,
    "AUS": 1.7, "ESP": 1.6, "BRA": 1.8, "NLD": 1.2, "CHE": 0.9,
    "SGP": 0.5, "IRL": 0.6, "RUS": 2.0, "HKG": 0.5, "BEL": 0.6,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch/process WTO bilateral services trade data for Lab 7",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--local-csv",
        default=None,
        help="Path to a pre-downloaded WTO services trade CSV.",
    )
    parser.add_argument(
        "--output-dir",
        default="labs/lab7_services/data",
        help="Directory for output CSV (default: labs/lab7_services/data).",
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help=(
            "Generate synthetic bilateral services trade panel (no download). "
            "For CI and quick-start validation."
        ),
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Synthetic data (smoke-test mode)
# ---------------------------------------------------------------------------

def synthetic_bilateral_services(
    countries: List[str],
    categories: List[str],
    years: List[int],
    export_scale: Dict[str, float],
    category_shares: Dict[str, float],
    gdp_weights: Dict[str, float],
) -> pd.DataFrame:
    """Generate a plausible synthetic bilateral services trade panel.

    Strategy
    --------
    For each exporter-importer-category-year:
      1. Start with exporter's total services exports.
      2. Allocate across partners using GDP-weighted gravity shares
         (excluding self-trade).
      3. Apply category share multipliers.
      4. Add log-normal noise for realism.
      5. Apply a slight positive trend over time.

    Trade values are in millions of current USD.
    """
    rng = np.random.default_rng(seed=2024)
    rows = []

    for exporter in countries:
        total_exports = export_scale.get(exporter, 50_000)

        # Compute partner weights (exclude self)
        partners = [c for c in countries if c != exporter]
        raw_weights = np.array([gdp_weights.get(p, 1.0) for p in partners])
        partner_shares = raw_weights / raw_weights.sum()

        for year in years:
            # Slight growth trend: +2% per year from baseline
            year_factor = 1.0 + 0.02 * (year - years[0])

            for j, importer in enumerate(partners):
                bilateral_total = total_exports * partner_shares[j] * year_factor

                for category in categories:
                    share = category_shares.get(category, 0.10)
                    if category == "total_services":
                        # total_services = sum of sub-categories; generate directly
                        base_value = bilateral_total
                    else:
                        base_value = bilateral_total * share

                    # Log-normal noise (multiplicative, mean ~1.0)
                    noise = rng.lognormal(0.0, 0.15)
                    value = base_value * noise

                    # Round to nearest million (trade values in $M)
                    value = round(max(1.0, value), 1)

                    rows.append({
                        "exporter": exporter,
                        "importer": importer,
                        "year": year,
                        "service_category": category,
                        "trade_value": value,
                    })

    df = pd.DataFrame(rows)
    return df.sort_values(
        ["exporter", "importer", "year", "service_category"]
    ).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Local CSV processing
# ---------------------------------------------------------------------------

EXPORTER_COLS = [
    "Reporting Economy", "Reporter", "REPORTER", "exporter",
    "Exporter", "REF_AREA", "COUNTRY",
]
IMPORTER_COLS = [
    "Partner Economy", "Partner", "PARTNER", "importer",
    "Importer", "COUNTERPART_AREA",
]
YEAR_COLS = ["Year", "YEAR", "TIME_PERIOD", "TIME", "year"]
VALUE_COLS = ["Value", "VALUE", "OBS_VALUE", "trade_value", "TRADE_VALUE"]
CATEGORY_COLS = [
    "Service/Sector", "Sector", "SECTOR", "service_category",
    "Service_Category", "INDICATOR", "Product/Sector",
]


def _find_col(df: pd.DataFrame, candidates: List[str], label: str) -> str:
    """Find the first matching column name from a list of candidates."""
    for c in candidates:
        if c in df.columns:
            return c
    raise KeyError(
        f"Could not find {label} column. Expected one of {candidates}. "
        f"Found columns: {list(df.columns)}"
    )


def process_local_csv(csv_path: str) -> pd.DataFrame:
    """Read a pre-downloaded WTO services trade CSV and reshape to standard format.

    Returns a DataFrame with columns:
    exporter, importer, year, service_category, trade_value
    """
    print(f"Reading local CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"  Raw shape: {df.shape[0]} rows x {df.shape[1]} columns")

    # Try long-format first
    try:
        exp_col = _find_col(df, EXPORTER_COLS, "exporter")
        imp_col = _find_col(df, IMPORTER_COLS, "importer")
        year_col = _find_col(df, YEAR_COLS, "year")
        val_col = _find_col(df, VALUE_COLS, "value")

        # Category column is optional; default to "total_services"
        try:
            cat_col = _find_col(df, CATEGORY_COLS, "service_category")
        except KeyError:
            cat_col = None

        cols_to_keep = [exp_col, imp_col, year_col, val_col]
        rename_map = {
            exp_col: "exporter",
            imp_col: "importer",
            year_col: "year",
            val_col: "trade_value",
        }
        if cat_col:
            cols_to_keep.append(cat_col)
            rename_map[cat_col] = "service_category"

        out = df[cols_to_keep].copy()
        out = out.rename(columns=rename_map)

        if "service_category" not in out.columns:
            out["service_category"] = "total_services"

        out["year"] = pd.to_numeric(out["year"], errors="coerce")
        out["trade_value"] = pd.to_numeric(out["trade_value"], errors="coerce")
        out = out.dropna(subset=["year", "trade_value"]).copy()
        out["year"] = out["year"].astype(int)

        # Drop rows with non-positive trade values
        out = out[out["trade_value"] > 0].copy()

        print(f"  Parsed: {len(out)} valid observations.")
        return out.sort_values(
            ["exporter", "importer", "year", "service_category"]
        ).reset_index(drop=True)

    except KeyError as e:
        raise ValueError(
            f"Could not parse CSV as bilateral services trade data. "
            f"Missing column: {e}. "
            f"Available columns: {list(df.columns)}"
        ) from e


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_summary(df: pd.DataFrame, label: str) -> None:
    """Print summary statistics for the bilateral services trade panel."""
    print(f"\n--- WTO Services Trade Summary ({label}) ---")
    print(f"  Exporters:   {df['exporter'].nunique()}")
    print(f"  Importers:   {df['importer'].nunique()}")
    print(f"  Categories:  {sorted(df['service_category'].unique().tolist())}")
    print(f"  Years:       {sorted(df['year'].unique().tolist())}")
    print(f"  Rows:        {len(df)}")
    print(f"  Total value: ${df['trade_value'].sum():,.0f}M")
    print(f"  Min value:   ${df['trade_value'].min():,.1f}M")
    print(f"  Max value:   ${df['trade_value'].max():,.1f}M")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.smoke_test:
        print("Running in smoke-test mode (synthetic data).")
        years = [2019, 2020, 2021]
        df = synthetic_bilateral_services(
            MAJOR_TRADERS, SERVICE_CATEGORIES, years,
            EXPORT_SCALE, CATEGORY_SHARES, GDP_WEIGHTS,
        )
        out_path = output_dir / "wto_services_trade_synthetic.csv"
        label = "synthetic"

    elif args.local_csv:
        df = process_local_csv(args.local_csv)
        out_path = output_dir / "wto_services_bilateral.csv"
        label = "local CSV"

    else:
        raise SystemExit(
            "Provide --local-csv PATH (path to pre-downloaded WTO services CSV) "
            "or use --smoke-test for synthetic data."
        )

    df.to_csv(out_path, index=False)
    print(f"\nWrote: {out_path}  ({len(df)} rows)")

    # Metadata sidecar
    meta = {
        "source": "WTO BPM6 services trade" if not args.smoke_test else "synthetic",
        "smoke_test": args.smoke_test,
        "local_csv": str(args.local_csv) if args.local_csv else None,
        "n_exporters": int(df["exporter"].nunique()),
        "n_importers": int(df["importer"].nunique()),
        "n_categories": int(df["service_category"].nunique()),
        "n_years": int(df["year"].nunique()),
        "n_rows": int(len(df)),
        "total_value_millions_usd": float(df["trade_value"].sum()),
        "fetched_at_utc": fetched_at,
    }
    meta_path = out_path.with_suffix(".json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote metadata: {meta_path}")

    print_summary(df, label)


if __name__ == "__main__":
    main()
