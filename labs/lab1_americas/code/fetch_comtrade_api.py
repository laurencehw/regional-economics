"""Fetch Comtrade data and export to Lab 1 raw schema.

This script reads COMTRADE_API_KEY from either:
1. Environment variable (default: COMTRADE_API_KEY), or
2. A Claude settings JSON file at C:/Users/lwils/.claude/settings.json.

Outputs a CSV suitable for `prepare_lab1_inputs.py` under the Comtrade mapping.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import requests


DEFAULT_SETTINGS_PATH = r"C:\Users\lwils\.claude\settings.json"
BASE_URL_TEMPLATE = "https://comtradeapi.un.org/data/v1/get/{type_code}/{freq_code}/{classification}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Comtrade data for Lab 1")
    parser.add_argument("--period", required=True, help="Period list, e.g. 2024 or 2023,2024")
    parser.add_argument("--reporter-code", default="all", help="Reporter code list or all")
    parser.add_argument(
        "--partner-code",
        default="auto",
        help="Partner code list, 0 for world aggregate, or auto (mirrors reporter-code)",
    )
    parser.add_argument("--flow-code", default="X", help="Flow code(s), e.g. X, M, X,M")
    parser.add_argument("--cmd-code", default="TOTAL", help="Commodity code(s), e.g. TOTAL")
    parser.add_argument("--type-code", default="C", help="Trade type code, default C")
    parser.add_argument("--freq-code", default="A", help="Frequency code, default A")
    parser.add_argument("--classification", default="HS", help="Classification code, default HS")
    parser.add_argument("--max-records", type=int, default=50000, help="Max records requested")
    parser.add_argument("--format", default="json", choices=["json"], help="Response format")
    parser.add_argument(
        "--include-desc",
        dest="include_desc",
        action="store_true",
        default=True,
        help="Request descriptive fields (needed for reporterISO/partnerISO)",
    )
    parser.add_argument(
        "--no-include-desc",
        dest="include_desc",
        action="store_false",
        help="Disable includeDesc request parameter",
    )
    parser.add_argument(
        "--settings-path",
        default=DEFAULT_SETTINGS_PATH,
        help="Path to settings JSON containing env.COMTRADE_API_KEY",
    )
    parser.add_argument("--api-key-env", default="COMTRADE_API_KEY", help="Env var for API key")
    parser.add_argument("--timeout", type=int, default=90, help="HTTP timeout seconds")
    parser.add_argument(
        "--use-env-proxy",
        action="store_true",
        help="Use OS proxy environment variables (disabled by default)",
    )
    parser.add_argument(
        "--output-csv",
        default="../data/comtrade_api_pull.csv",
        help="Output CSV path in Lab 1 raw schema",
    )
    parser.add_argument(
        "--output-json",
        default="../data/comtrade_api_pull.json",
        help="Raw JSON response output path",
    )
    return parser.parse_args()


def resolve_partner_code(reporter_code: str, partner_code: str) -> str:
    if partner_code.lower() != "auto":
        return partner_code
    if reporter_code.lower() == "all":
        raise ValueError("partner-code=auto requires explicit reporter-code list (not 'all').")
    return reporter_code


def load_api_key(env_var: str, settings_path: str) -> Tuple[str, str]:
    from_env = os.environ.get(env_var)
    if from_env:
        return from_env, f"env:{env_var}"

    path = Path(settings_path)
    if not path.exists():
        raise FileNotFoundError(
            f"API key not found in env and settings file does not exist: {path}"
        )

    payload = json.loads(path.read_text(encoding="utf-8"))
    from_settings = payload.get("env", {}).get(env_var)
    if from_settings:
        return from_settings, f"settings:{path}"

    raise KeyError(f"{env_var} not found in env or settings file")


def normalize_rows(data_rows: List[Dict[str, object]]) -> pd.DataFrame:
    records: List[Dict[str, object]] = []
    for row in data_rows:
        records.append(
            {
                "reporter_iso": row.get("reporterISO"),
                "partner_iso": row.get("partnerISO"),
                "year": row.get("refYear", row.get("period")),
                "trade_value_usd": row.get("primaryValue"),
                "reporter_code": row.get("reporterCode"),
                "partner_code": row.get("partnerCode"),
                "flow_code": row.get("flowCode"),
                "cmd_code": row.get("cmdCode"),
                "is_reported": row.get("isReported"),
            }
        )

    out = pd.DataFrame.from_records(records)
    if out.empty:
        return out

    out = out.assign(
        year=pd.to_numeric(out["year"], errors="coerce"),
        trade_value_usd=pd.to_numeric(out["trade_value_usd"], errors="coerce"),
    )
    out = out.dropna(subset=["reporter_iso", "partner_iso", "year", "trade_value_usd"]).copy()
    out = out.assign(year=out["year"].astype(int))
    out = out.loc[out["trade_value_usd"] >= 0].copy()
    out = out.loc[out["reporter_iso"] != out["partner_iso"]].copy()
    out = out.sort_values(["reporter_iso", "partner_iso", "year"]).reset_index(drop=True)
    return out


def main() -> None:
    args = parse_args()

    api_key, key_source = load_api_key(args.api_key_env, args.settings_path)
    partner_code = resolve_partner_code(args.reporter_code, args.partner_code)

    url = BASE_URL_TEMPLATE.format(
        type_code=args.type_code,
        freq_code=args.freq_code,
        classification=args.classification,
    )

    params = {
        "cmdCode": args.cmd_code,
        "period": args.period,
        "reporterCode": args.reporter_code,
        "partnerCode": partner_code,
        "flowCode": args.flow_code,
        "maxRecords": str(args.max_records),
        "format": args.format,
        "includeDesc": "true" if args.include_desc else "false",
        "subscription-key": api_key,
    }

    session = requests.Session()
    session.trust_env = bool(args.use_env_proxy)

    response = session.get(url, params=params, timeout=args.timeout)
    if response.status_code >= 400:
        snippet = response.text[:1000]
        raise RuntimeError(
            f"Comtrade API request failed with status {response.status_code}. "
            f"Response snippet: {snippet}"
        )

    payload = response.json()
    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError(f"Comtrade API error: {payload['error']}")

    if not isinstance(payload, dict) or "data" not in payload:
        raise RuntimeError("Unexpected API response format; expected top-level 'data' list")

    data_rows = payload.get("data") or []
    normalized = normalize_rows(data_rows)

    output_csv = Path(args.output_csv)
    output_json = Path(args.output_json)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)

    normalized.to_csv(output_csv, index=False)
    output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    total_count = payload.get("count")
    print(f"Fetched {len(data_rows)} raw rows from Comtrade API")
    print(f"Normalized rows written: {len(normalized)}")
    print(f"Key source: {key_source}")
    if isinstance(total_count, int) and total_count > len(data_rows):
        print(
            f"Warning: API reports count={total_count} but returned {len(data_rows)} rows. "
            "Increase maxRecords and/or add pagination support."
        )
    print(f"CSV: {output_csv.resolve()}")
    print(f"JSON: {output_json.resolve()}")


if __name__ == "__main__":
    main()
