"""Fetch WDI indicators for selected countries and export long-format CSV."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pandas as pd
import requests

BASE_URL = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch WDI indicators for Lab 1")
    parser.add_argument("--countries", default="USA,CAN,MEX", help="ISO3 codes, comma-separated")
    parser.add_argument(
        "--indicators",
        default="NY.GDP.MKTP.KD.ZG,NY.GDP.PCAP.KD,NV.IND.MANF.ZS",
        help="WDI indicator codes, comma-separated",
    )
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--per-page", type=int, default=20000)
    parser.add_argument(
        "--output-csv",
        default="data/raw/wdi/wdi_usmca_core_long.csv",
        help="Output CSV path",
    )
    return parser.parse_args()


def parse_csv_list(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def fetch_indicator(countries: str, indicator: str, per_page: int) -> list:
    session = requests.Session()
    session.trust_env = False
    response = session.get(
        BASE_URL.format(countries=countries, indicator=indicator),
        params={"format": "json", "per_page": per_page},
        timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2:
        return []
    data = payload[1]
    return data if isinstance(data, list) else []


def main() -> None:
    args = parse_args()
    countries = ";".join(parse_csv_list(args.countries))
    indicators = parse_csv_list(args.indicators)
    fetched_at = datetime.now(timezone.utc).isoformat()

    rows = []
    for ind in indicators:
        data = fetch_indicator(countries=countries, indicator=ind, per_page=args.per_page)
        for row in data:
            year_raw = row.get("date")
            try:
                year = int(year_raw)
            except Exception:
                continue
            if year < args.start_year or year > args.end_year:
                continue

            value = row.get("value")
            if value is None:
                continue

            country = row.get("country") or {}
            indicator_meta = row.get("indicator") or {}

            rows.append(
                {
                    "country_iso3": row.get("countryiso3code"),
                    "country_name": country.get("value"),
                    "indicator_code": indicator_meta.get("id", ind),
                    "indicator_name": indicator_meta.get("value"),
                    "year": year,
                    "value": value,
                    "fetched_at_utc": fetched_at,
                }
            )

    out = pd.DataFrame(rows)
    out = out.sort_values(["country_iso3", "indicator_code", "year"]).reset_index(drop=True)

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Rows written: {len(out)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
