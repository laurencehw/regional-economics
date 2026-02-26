"""Fetch UNHCR population controls for Lab 4 and map to a country-year panel.

The script pulls origin-based displacement aggregates (by year and country of origin)
from the UNHCR population API and outputs:
- Raw panel with source fields
- Mapped panel aligned with Lab 4 template columns
- Pull metadata JSON
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd
import requests


COUNTRIES_URL = "https://api.unhcr.org/population/v1/countries/"
POPULATION_URL = "https://api.unhcr.org/population/v1/population/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch UNHCR Lab 4 displacement controls")
    parser.add_argument(
        "--iso3-list",
        default="EGY,IRQ,JOR,LBN,LBY,MAR,SAU,SYR,TUN,YEM",
        help="Comma-separated ISO3 country list for Lab 4 scope",
    )
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument("--limit", type=int, default=1, help="Expected rows per (country, year) query")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--raw-output-csv",
        default="data/raw/unhcr/unhcr_lab4_origin_controls_2000_2024_2026-02-23.csv",
        help="Raw output CSV path",
    )
    parser.add_argument(
        "--mapped-output-csv",
        default="data/processed/lab4/unhcr_lab4_controls_mena_2000_2024_2026-02-23.csv",
        help="Mapped output CSV path",
    )
    parser.add_argument(
        "--metadata-json",
        default="data/raw/metadata/unhcr_lab4_pull_mena_origin_2000_2024_2026-02-23.json",
        help="Pull metadata JSON path",
    )
    return parser.parse_args()


def parse_csv_list(raw: str) -> List[str]:
    return [x.strip().upper() for x in raw.split(",") if x.strip()]


def fetch_json(url: str, params: Dict[str, object], timeout: int) -> Dict[str, object]:
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError(f"Unexpected JSON payload from {url}")
    return payload


def fetch_countries(timeout: int) -> pd.DataFrame:
    first = fetch_json(COUNTRIES_URL, params={"page": 1, "limit": 500}, timeout=timeout)
    pages = int(first.get("maxPages", 1))
    rows: List[Dict[str, object]] = list(first.get("items", []))
    for page in range(2, pages + 1):
        payload = fetch_json(COUNTRIES_URL, params={"page": page, "limit": 500}, timeout=timeout)
        rows.extend(list(payload.get("items", [])))
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("UNHCR countries endpoint returned no rows")
    needed = {"iso", "code", "name"}
    missing = sorted(needed - set(df.columns))
    if missing:
        raise RuntimeError(f"Countries payload missing expected columns: {missing}")
    df = df.assign(iso=df["iso"].astype(str).str.upper(), code=df["code"].astype(str).str.upper())
    return df


def to_float(x: object) -> float:
    if x is None:
        return 0.0
    if isinstance(x, (int, float)):
        return float(x)
    text = str(x).strip()
    if not text or text == "-":
        return 0.0
    try:
        return float(text.replace(",", ""))
    except ValueError:
        return 0.0


def build_country_code_map(countries_df: pd.DataFrame, iso3_list: List[str]) -> Dict[str, Tuple[str, str]]:
    subset = countries_df[countries_df["iso"].isin(iso3_list)][["iso", "code", "name"]].copy()
    out = {row["iso"]: (row["code"], row["name"]) for _, row in subset.iterrows()}
    missing = sorted(set(iso3_list) - set(out.keys()))
    if missing:
        raise RuntimeError(f"Missing ISO3 codes in UNHCR country mapping: {missing}")
    return out


def fetch_origin_country_year(
    code: str,
    year: int,
    limit: int,
    timeout: int,
) -> Dict[str, object]:
    payload = fetch_json(
        POPULATION_URL,
        params={"coo": code, "year": year, "limit": limit},
        timeout=timeout,
    )
    items = payload.get("items", [])
    if not items:
        return {}
    row = items[0]
    if not isinstance(row, dict):
        return {}
    return row


def main() -> None:
    args = parse_args()
    pulled_at = datetime.now(timezone.utc).isoformat()
    iso3_list = parse_csv_list(args.iso3_list)
    years = list(range(args.start_year, args.end_year + 1))

    countries_df = fetch_countries(timeout=args.timeout)
    code_map = build_country_code_map(countries_df=countries_df, iso3_list=iso3_list)

    rows: List[Dict[str, object]] = []
    for iso3 in iso3_list:
        code, country_name = code_map[iso3]
        for year in years:
            item = fetch_origin_country_year(code=code, year=year, limit=args.limit, timeout=args.timeout)
            refugees = to_float(item.get("refugees"))
            asylum_seekers = to_float(item.get("asylum_seekers"))
            idps = to_float(item.get("idps"))
            total_displaced = refugees + asylum_seekers + idps
            rows.append(
                {
                    "iso3": iso3,
                    "country_name": country_name,
                    "unhcr_code": code,
                    "year": year,
                    "refugees": refugees,
                    "asylum_seekers": asylum_seekers,
                    "idps": idps,
                    "total_displaced": total_displaced,
                    "source_short_url": item.get("short-url", ""),
                }
            )

    raw_df = pd.DataFrame(rows).sort_values(["iso3", "year"]).reset_index(drop=True)
    mapped_df = raw_df.rename(
        columns={
            "refugees": "refugees_under_mandate",
            "asylum_seekers": "asylum_seekers",
            "idps": "idps",
            "total_displaced": "total_displaced",
        }
    )[
        [
            "iso3",
            "year",
            "refugees_under_mandate",
            "asylum_seekers",
            "idps",
            "total_displaced",
        ]
    ].copy()
    mapped_df["source_note"] = "UNHCR population API (origin-based annual aggregates)"

    raw_output = Path(args.raw_output_csv)
    raw_output.parent.mkdir(parents=True, exist_ok=True)
    raw_df.to_csv(raw_output, index=False)

    mapped_output = Path(args.mapped_output_csv)
    mapped_output.parent.mkdir(parents=True, exist_ok=True)
    mapped_df.to_csv(mapped_output, index=False)

    metadata = {
        "pulled_at_utc": pulled_at,
        "countries_url": COUNTRIES_URL,
        "population_url": POPULATION_URL,
        "iso3_list": iso3_list,
        "year_start": args.start_year,
        "year_end": args.end_year,
        "rows_raw": int(len(raw_df)),
        "rows_mapped": int(len(mapped_df)),
        "countries_count": int(mapped_df["iso3"].nunique()) if not mapped_df.empty else 0,
        "raw_output_csv": str(raw_output),
        "mapped_output_csv": str(mapped_output),
    }
    metadata_path = Path(args.metadata_json)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Rows written (raw): {len(raw_df)}")
    print(f"Rows written (mapped): {len(mapped_df)}")
    print(f"Raw CSV: {raw_output}")
    print(f"Mapped CSV: {mapped_output}")
    print(f"Metadata: {metadata_path}")


if __name__ == "__main__":
    main()
