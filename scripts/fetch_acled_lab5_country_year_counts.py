"""Fetch ACLED country-year event counts for Lab 5 using OAuth credentials.

This path is resilient when account permissions expose counts but restrict row-level data.
Credentials must be provided via environment variables:
- ACLED_USERNAME
- ACLED_PASSWORD
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests


TOKEN_URL = "https://acleddata.com/oauth/token"
DATA_URL = "https://acleddata.com/api/acled/read"

COUNTRY_TO_ISO3 = {
    "Egypt": "EGY",
    "Iraq": "IRQ",
    "Jordan": "JOR",
    "Lebanon": "LBN",
    "Libya": "LBY",
    "Morocco": "MAR",
    "Saudi Arabia": "SAU",
    "Syria": "SYR",
    "Tunisia": "TUN",
    "Yemen": "YEM",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch ACLED country-year event counts for Lab 5")
    parser.add_argument(
        "--countries",
        default="Egypt,Iraq,Jordan,Lebanon,Libya,Morocco,Saudi Arabia,Syria,Tunisia,Yemen",
        help="Comma-separated country names",
    )
    parser.add_argument("--start-year", type=int, default=2018)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--username-env", default="ACLED_USERNAME")
    parser.add_argument("--password-env", default="ACLED_PASSWORD")
    parser.add_argument(
        "--output-csv",
        default="data/processed/lab5/acled_lab5_country_year_counts_2018_2025_2026-02-23.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--metadata-json",
        default="data/raw/metadata/acled_lab5_country_year_counts_2018_2025_2026-02-23.json",
        help="Metadata JSON path",
    )
    return parser.parse_args()


def parse_csv_list(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def get_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value


def fetch_token(username: str, password: str, timeout: int) -> str:
    payload = {
        "grant_type": "password",
        "client_id": "acled",
        "username": username,
        "password": password,
    }
    resp = requests.post(TOKEN_URL, data=payload, timeout=timeout)
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError("ACLED token response missing access_token")
    return token


def query_count(access_token: str, country: str, year: int, timeout: int) -> Dict[str, object]:
    params = {
        "country": country,
        "event_date": f"{year}-01-01|{year}-12-31",
        "event_date_where": "BETWEEN",
        "limit": "1",
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(DATA_URL, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()
    if not isinstance(payload, dict):
        raise RuntimeError("Unexpected ACLED count response payload")
    return payload


def main() -> None:
    args = parse_args()
    pulled_at = datetime.now(timezone.utc).isoformat()

    username = get_env(args.username_env)
    password = get_env(args.password_env)
    countries = parse_csv_list(args.countries)

    missing_iso = sorted([c for c in countries if c not in COUNTRY_TO_ISO3])
    if missing_iso:
        raise ValueError(f"Country-to-ISO mapping missing for: {missing_iso}")

    token = fetch_token(username=username, password=password, timeout=args.timeout)
    rows: List[Dict[str, object]] = []
    restriction_samples: List[Dict[str, object]] = []
    for country in countries:
        iso3 = COUNTRY_TO_ISO3[country]
        for year in range(args.start_year, args.end_year + 1):
            payload = query_count(access_token=token, country=country, year=year, timeout=args.timeout)
            total_count = payload.get("total_count", payload.get("count", 0))
            try:
                total_count_int = int(total_count)
            except Exception:
                total_count_int = 0

            restrictions = payload.get("data_query_restrictions", {})
            if isinstance(restrictions, dict):
                restriction_samples.append(restrictions)

            rows.append(
                {
                    "iso3": iso3,
                    "country": country,
                    "year": year,
                    "acled_event_count": total_count_int,
                }
            )

    df = pd.DataFrame(rows).sort_values(["iso3", "year"]).reset_index(drop=True)
    df = df.assign(treatment_event=df["acled_event_count"].astype(float))

    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    metadata = {
        "pulled_at_utc": pulled_at,
        "token_url": TOKEN_URL,
        "data_url": DATA_URL,
        "countries": countries,
        "start_year": args.start_year,
        "end_year": args.end_year,
        "rows": int(len(df)),
        "output_csv": str(output_csv),
        "credential_env_vars": {
            "username_env": args.username_env,
            "password_env": args.password_env,
        },
        "restriction_samples": restriction_samples[:3],
    }
    metadata_path = Path(args.metadata_json)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Rows written: {len(df)}")
    print(f"Output CSV: {output_csv}")
    print(f"Metadata: {metadata_path}")


if __name__ == "__main__":
    main()
