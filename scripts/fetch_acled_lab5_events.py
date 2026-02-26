"""Fetch ACLED event records for Lab 4 using OAuth credentials from environment variables.

Credentials are never read from CLI args; set them in the shell environment:
- ACLED_USERNAME
- ACLED_PASSWORD
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import requests


TOKEN_URL = "https://acleddata.com/oauth/token"
DATA_URL = "https://acleddata.com/api/acled/read"

DEFAULT_FIELDS = ",".join(
    [
        "event_id_cnty",
        "event_date",
        "year",
        "country",
        "admin1",
        "admin2",
        "event_type",
        "sub_event_type",
        "fatalities",
        "latitude",
        "longitude",
        "source",
    ]
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch ACLED records for Lab 4 MENA intake")
    parser.add_argument(
        "--countries",
        default="Egypt",
        help="Comma-separated country names (ACLED country labels)",
    )
    parser.add_argument("--start-date", default="2024-01-01", help="Inclusive start date (YYYY-MM-DD)")
    parser.add_argument(
        "--end-date",
        default=str(date.today()),
        help="Inclusive end date (YYYY-MM-DD)",
    )
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help="Comma-separated ACLED fields")
    parser.add_argument("--limit", type=int, default=5000, help="Max records to fetch in one request")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--username-env",
        default="ACLED_USERNAME",
        help="Environment variable name holding ACLED username/email",
    )
    parser.add_argument(
        "--password-env",
        default="ACLED_PASSWORD",
        help="Environment variable name holding ACLED password/key",
    )
    parser.add_argument(
        "--output-csv",
        default="data/raw/acled/acled_lab4_events_sample_2026-02-23.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--metadata-json",
        default="data/raw/metadata/acled_lab4_pull_sample_2026-02-23.json",
        help="Metadata JSON path",
    )
    return parser.parse_args()


def parse_csv_list(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def to_country_or_clause(countries: List[str]) -> str:
    if not countries:
        raise ValueError("At least one country is required")
    head, *tail = countries
    suffix = "".join(f":OR:country={c}" for c in tail)
    return f"{head}{suffix}"


def get_env_credential(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value


def fetch_access_token(username: str, password: str, timeout: int) -> str:
    payload = {
        "grant_type": "password",
        "client_id": "acled",
        "username": username,
        "password": password,
    }
    response = requests.post(TOKEN_URL, data=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError("ACLED token response missing access_token")
    return token


def fetch_events(access_token: str, params: Dict[str, str], timeout: int) -> Tuple[List[object], Dict[str, object]]:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(DATA_URL, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict) and "data" in payload:
        rows = payload["data"]
    elif isinstance(payload, list):
        rows = payload
        payload = {"status": 200, "data": rows}
    else:
        rows = []
    if not isinstance(rows, list) or not isinstance(payload, dict):
        raise RuntimeError("Unexpected ACLED response structure for data rows")
    return rows, payload


def main() -> None:
    args = parse_args()
    pulled_at = datetime.now(timezone.utc).isoformat()

    username = get_env_credential(args.username_env)
    password = get_env_credential(args.password_env)

    countries = parse_csv_list(args.countries)
    params = {
        "country": to_country_or_clause(countries),
        "event_date": f"{args.start_date}|{args.end_date}",
        "event_date_where": "BETWEEN",
        "fields": args.fields,
        "limit": str(args.limit),
    }

    token = fetch_access_token(username=username, password=password, timeout=args.timeout)
    rows, payload = fetch_events(access_token=token, params=params, timeout=args.timeout)
    row_level_redacted = False
    if rows and isinstance(rows[0], dict):
        df = pd.DataFrame(rows)
    elif rows and isinstance(rows[0], list):
        field_names = parse_csv_list(args.fields)
        if rows[0] and len(rows[0]) == len(field_names):
            df = pd.DataFrame(rows, columns=field_names)
        else:
            # Some access levels expose counts but redact row-level values.
            row_level_redacted = True
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()

    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    api_count = payload.get("total_count", payload.get("count", len(rows)))
    try:
        api_count_int = int(api_count)
    except Exception:
        api_count_int = int(len(rows))

    metadata = {
        "pulled_at_utc": pulled_at,
        "token_url": TOKEN_URL,
        "data_url": DATA_URL,
        "query_params": params,
        "rows": int(len(df)),
        "api_reported_total_count": api_count_int,
        "row_level_redacted": row_level_redacted,
        "country_filter_count": int(len(countries)),
        "countries": countries,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "output_csv": str(output_csv),
        "data_query_restrictions": payload.get("data_query_restrictions", {}),
        "credential_env_vars": {
            "username_env": args.username_env,
            "password_env": args.password_env,
        },
    }
    metadata_json = Path(args.metadata_json)
    metadata_json.parent.mkdir(parents=True, exist_ok=True)
    metadata_json.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Rows written: {len(df)}")
    print(f"API reported total count: {api_count_int}")
    print(f"Row-level redacted: {row_level_redacted}")
    print(f"Output CSV: {output_csv}")
    print(f"Metadata: {metadata_json}")


if __name__ == "__main__":
    main()
