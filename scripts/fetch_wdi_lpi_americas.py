"""Fetch World Bank LPI indicator for Americas economies in long format.

Outputs columns aligned with other WDI pulls:
- country_iso3
- country_name
- indicator_code
- indicator_name
- year
- value
- fetched_at_utc
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
import requests

WB_COUNTRY_URL = "https://api.worldbank.org/v2/country"
WB_INDICATOR_URL = "https://api.worldbank.org/v2/country/all/indicator/{indicator}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch WDI LPI indicator for Americas economies")
    parser.add_argument("--indicator", default="LP.LPI.OVRL.XQ", help="WDI indicator code")
    parser.add_argument("--start-year", type=int, default=2007)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument(
        "--output-csv",
        default="data/raw/wdi/wdi_lpi_americas_long.csv",
        help="Output CSV path",
    )
    return parser.parse_args()


def fetch_world_bank_countries(session: requests.Session) -> List[Dict[str, object]]:
    response = session.get(WB_COUNTRY_URL, params={"format": "json", "per_page": 400}, timeout=90)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        return []
    return payload[1]


def get_americas_iso3(country_rows: Iterable[Dict[str, object]]) -> List[str]:
    iso3 = []
    for row in country_rows:
        region_id = (row.get("region") or {}).get("id")
        income_id = (row.get("incomeLevel") or {}).get("id")
        code = row.get("id")
        iso2 = row.get("iso2Code")
        if region_id not in {"LCN", "NAC"}:
            continue
        if income_id == "NA":
            continue
        if not isinstance(code, str) or len(code) != 3:
            continue
        if iso2 == "NA":
            continue
        iso3.append(code)
    return sorted(set(iso3))


def fetch_indicator_rows(session: requests.Session, indicator: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    page = 1
    pages = 1
    while page <= pages:
        response = session.get(
            WB_INDICATOR_URL.format(indicator=indicator),
            params={"format": "json", "per_page": 20000, "page": page},
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list) or len(payload) < 2:
            break

        meta = payload[0] if isinstance(payload[0], dict) else {}
        pages = int(meta.get("pages", 1) or 1)
        page_rows = payload[1] if isinstance(payload[1], list) else []
        rows.extend(page_rows)
        page += 1
    return rows


def main() -> None:
    args = parse_args()
    fetched_at = datetime.now(timezone.utc).isoformat()

    session = requests.Session()
    session.trust_env = False

    countries = fetch_world_bank_countries(session)
    americas_iso = set(get_americas_iso3(countries))
    raw_rows = fetch_indicator_rows(session, args.indicator)

    rows = []
    for row in raw_rows:
        iso3 = row.get("countryiso3code")
        if iso3 not in americas_iso:
            continue

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
                "country_iso3": iso3,
                "country_name": country.get("value"),
                "indicator_code": indicator_meta.get("id", args.indicator),
                "indicator_name": indicator_meta.get("value"),
                "year": year,
                "value": value,
                "fetched_at_utc": fetched_at,
            }
        )

    out = pd.DataFrame(rows)
    out = out.sort_values(["country_iso3", "year"]).reset_index(drop=True)

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Countries in scope: {len(americas_iso)}")
    print(f"Rows written: {len(out)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
