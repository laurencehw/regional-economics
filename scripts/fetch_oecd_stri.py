"""Fetch OECD Services Trade Restrictiveness Index (STRI) data.

Outputs
-------
``labs/lab7_services/data/stri_panel.csv`` (from --local-csv)
``labs/lab7_services/data/stri_panel_synthetic.csv`` (from --smoke-test)
  Long-format panel with columns: country, year, sector, stri_score
  Compatible with ``labs/lab7_services/data/source_mappings.json``
  (country_col: "country", year_col: "year", sector_col: "sector",
  score_col: "stri_score").

DATA SOURCE
-----------
OECD Services Trade Restrictiveness Index (STRI)
  - Coverage: 50+ countries, 22 sectors, annual since 2014
  - Range: 0 (fully open) to 1 (fully closed)
  - URL: https://www.oecd.org/en/topics/services-trade.html
  - Data Explorer: https://data-explorer.oecd.org/

DOWNLOAD INSTRUCTIONS
---------------------
1. Go to https://data-explorer.oecd.org/ and search for "STRI".
2. Select countries, sectors, and years of interest.
3. Export as CSV.
4. Pass the downloaded CSV path to --local-csv.

Use --smoke-test to generate a synthetic STRI panel for CI/testing
without downloading anything.

USAGE EXAMPLES
--------------
Smoke test (no download needed):
  python scripts/fetch_oecd_stri.py --smoke-test

Process a pre-downloaded CSV:
  python scripts/fetch_oecd_stri.py --local-csv path/to/STRI_download.csv
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Country and sector definitions
# ---------------------------------------------------------------------------

STRI_COUNTRIES: List[str] = [
    # OECD members
    "USA", "GBR", "DEU", "FRA", "JPN", "KOR", "AUS", "CAN",
    "ITA", "ESP", "NLD", "CHE", "SWE", "NOR", "DNK", "FIN",
    "BEL", "AUT", "NZL", "IRL",
    # Major developing / non-OECD
    "CHN", "IND", "BRA", "IDN", "ZAF", "RUS", "TUR", "MEX",
    "THA", "COL",
]

STRI_SECTORS: List[str] = [
    "telecommunications",
    "financial_services",
    "computer_services",
    "professional_services",
    "transport",
]

# Approximate baseline STRI scores by country (sector-averaged).
# Calibrated from published OECD STRI data (2022 vintage).
STRI_BASELINES: Dict[str, float] = {
    "USA": 0.18, "GBR": 0.14, "DEU": 0.22, "FRA": 0.24, "JPN": 0.24,
    "KOR": 0.21, "AUS": 0.17, "CAN": 0.19, "ITA": 0.25, "ESP": 0.20,
    "NLD": 0.13, "CHE": 0.23, "SWE": 0.15, "NOR": 0.19, "DNK": 0.14,
    "FIN": 0.15, "BEL": 0.17, "AUT": 0.20, "NZL": 0.16, "IRL": 0.14,
    "CHN": 0.55, "IND": 0.45, "BRA": 0.38, "IDN": 0.42, "ZAF": 0.32,
    "RUS": 0.40, "TUR": 0.35, "MEX": 0.34, "THA": 0.36, "COL": 0.28,
}

# Sector-specific multipliers relative to country baseline.
# Higher = more restrictive for that sector.
SECTOR_MULTIPLIERS: Dict[str, float] = {
    "telecommunications": 1.05,
    "financial_services": 1.10,
    "computer_services": 0.75,
    "professional_services": 1.20,
    "transport": 0.90,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch/process OECD STRI data for Lab 7",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--local-csv",
        default=None,
        help="Path to a pre-downloaded OECD STRI CSV from Data Explorer.",
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
            "Generate synthetic STRI panel (no download needed). "
            "For CI and quick-start validation."
        ),
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Synthetic data (smoke-test mode)
# ---------------------------------------------------------------------------

def synthetic_stri(
    countries: List[str],
    sectors: List[str],
    years: List[int],
    baselines: Dict[str, float],
    sector_mults: Dict[str, float],
) -> pd.DataFrame:
    """Generate a plausible synthetic STRI panel.

    For each country-sector-year, the score is derived from:
      base = country_baseline * sector_multiplier
      noise ~ N(0, 0.02)
      trend = -0.002 * (year - 2018)  (slight liberalisation trend)
      stri_score = clip(base + noise + trend, 0, 1)
    """
    rng = np.random.default_rng(seed=2024)
    rows = []
    for country in countries:
        base_country = baselines.get(country, 0.25)
        for sector in sectors:
            mult = sector_mults.get(sector, 1.0)
            for year in years:
                base = base_country * mult
                noise = rng.normal(0.0, 0.02)
                trend = -0.002 * (year - years[0])
                score = float(np.clip(base + noise + trend, 0.0, 1.0))
                rows.append({
                    "country": country,
                    "year": year,
                    "sector": sector,
                    "stri_score": round(score, 4),
                })
    return pd.DataFrame(rows).sort_values(
        ["country", "sector", "year"]
    ).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Local CSV processing
# ---------------------------------------------------------------------------

# Known column name mappings for OECD Data Explorer STRI downloads.
# The exact column names vary by download format and vintage.
COUNTRY_COLS = ["COUNTRY", "Country", "REF_AREA", "COU", "country"]
SECTOR_COLS = ["SECTOR", "Sector", "IND", "sector", "INDICATOR"]
YEAR_COLS = ["YEAR", "Year", "TIME_PERIOD", "TIME", "year"]
VALUE_COLS = ["VALUE", "Value", "OBS_VALUE", "stri_score", "STRI"]


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
    """Read a pre-downloaded OECD STRI CSV and reshape to standard format.

    Handles both long-format exports (one row per observation) and
    wide-format exports (years as columns). Returns a DataFrame with
    columns: country, year, sector, stri_score.
    """
    print(f"Reading local CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"  Raw shape: {df.shape[0]} rows x {df.shape[1]} columns")

    # Try long-format first
    try:
        country_col = _find_col(df, COUNTRY_COLS, "country")
        sector_col = _find_col(df, SECTOR_COLS, "sector")
        year_col = _find_col(df, YEAR_COLS, "year")
        value_col = _find_col(df, VALUE_COLS, "value")

        out = df[[country_col, year_col, sector_col, value_col]].copy()
        out.columns = ["country", "year", "sector", "stri_score"]
        out["year"] = pd.to_numeric(out["year"], errors="coerce")
        out["stri_score"] = pd.to_numeric(out["stri_score"], errors="coerce")
        out = out.dropna(subset=["year", "stri_score"]).copy()
        out["year"] = out["year"].astype(int)

        print(f"  Parsed as long format: {len(out)} valid observations.")
        return out.sort_values(
            ["country", "sector", "year"]
        ).reset_index(drop=True)

    except KeyError:
        pass

    # Fall back to wide format: try to melt year columns
    print("  Attempting wide-format parsing (years as columns)...")
    country_col = _find_col(df, COUNTRY_COLS, "country")
    sector_col = _find_col(df, SECTOR_COLS, "sector")

    # Identify numeric year columns
    year_cols = [c for c in df.columns if c.isdigit() and 2000 <= int(c) <= 2030]
    if not year_cols:
        raise ValueError(
            "Could not identify year columns in wide format. "
            f"Columns: {list(df.columns)}"
        )

    out = df.melt(
        id_vars=[country_col, sector_col],
        value_vars=year_cols,
        var_name="year",
        value_name="stri_score",
    )
    out = out.rename(columns={country_col: "country", sector_col: "sector"})
    out["year"] = out["year"].astype(int)
    out["stri_score"] = pd.to_numeric(out["stri_score"], errors="coerce")
    out = out.dropna(subset=["stri_score"]).copy()

    print(f"  Parsed as wide format: {len(out)} valid observations.")
    return out.sort_values(
        ["country", "sector", "year"]
    ).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_summary(df: pd.DataFrame, label: str) -> None:
    """Print summary statistics for the STRI panel."""
    print(f"\n--- STRI Summary ({label}) ---")
    print(f"  Countries: {df['country'].nunique()}")
    print(f"  Sectors:   {df['sector'].nunique()}")
    print(f"  Years:     {sorted(df['year'].unique().tolist())}")
    print(f"  Rows:      {len(df)}")
    print(f"  STRI min:  {df['stri_score'].min():.4f}")
    print(f"  STRI max:  {df['stri_score'].max():.4f}")
    print(f"  STRI mean: {df['stri_score'].mean():.4f}")


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
        years = list(range(2018, 2023))
        df = synthetic_stri(STRI_COUNTRIES, STRI_SECTORS, years,
                            STRI_BASELINES, SECTOR_MULTIPLIERS)
        out_path = output_dir / "stri_panel_synthetic.csv"
        label = "synthetic"

    elif args.local_csv:
        df = process_local_csv(args.local_csv)
        out_path = output_dir / "stri_panel.csv"
        label = "local CSV"

    else:
        raise SystemExit(
            "Provide --local-csv PATH (path to pre-downloaded OECD STRI CSV) "
            "or use --smoke-test for synthetic data."
        )

    df.to_csv(out_path, index=False)
    print(f"\nWrote: {out_path}  ({len(df)} rows)")

    # Metadata sidecar
    meta = {
        "source": "OECD STRI" if not args.smoke_test else "synthetic",
        "smoke_test": args.smoke_test,
        "local_csv": str(args.local_csv) if args.local_csv else None,
        "n_countries": int(df["country"].nunique()),
        "n_sectors": int(df["sector"].nunique()),
        "n_years": int(df["year"].nunique()),
        "n_rows": int(len(df)),
        "stri_min": float(df["stri_score"].min()),
        "stri_max": float(df["stri_score"].max()),
        "fetched_at_utc": fetched_at,
    }
    meta_path = out_path.with_suffix(".json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote metadata: {meta_path}")

    print_summary(df, label)


if __name__ == "__main__":
    main()
