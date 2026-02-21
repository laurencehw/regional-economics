"""Build real raw inputs for Lab 1 across Americas countries.

Outputs:
- data/raw/metadata/americas_iso_m49_<date>.csv
- data/raw/wdi/wdi_americas_core_long_<date>.csv
- data/raw/comtrade/comtrade_americas_total_x_<year>_<date>.csv
- data/raw/comtrade/comtrade_americas_pull_summary_<year>_<date>.json
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd
import pycountry
import requests

WB_COUNTRY_URL = "https://api.worldbank.org/v2/country"
WB_INDICATOR_URL = "https://api.worldbank.org/v2/country/all/indicator/{indicator}"
COMTRADE_URL = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
DEFAULT_SETTINGS_PATH = str(Path.home() / ".claude" / "settings.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Lab 1 real raw inputs (Americas)")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument(
        "--indicators",
        default="NY.GDP.MKTP.KD.ZG,NY.GDP.PCAP.KD,NV.IND.MANF.ZS",
        help="WDI indicators comma-separated",
    )
    parser.add_argument("--settings-path", default=DEFAULT_SETTINGS_PATH)
    parser.add_argument("--api-key-env", default="COMTRADE_API_KEY")
    parser.add_argument("--output-root", default="data/raw")
    parser.add_argument("--date-stamp", default=datetime.now().strftime("%Y-%m-%d"))
    return parser.parse_args()


def parse_csv_list(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def load_api_key(settings_path: str, env_name: str) -> str:
    import os

    env_val = os.environ.get(env_name)
    if env_val:
        return env_val

    payload = json.loads(Path(settings_path).read_text(encoding="utf-8"))
    key = payload.get("env", {}).get(env_name)
    if not key:
        raise KeyError(f"{env_name} not found in env or {settings_path}")
    return key


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


def iso3_to_m49(iso3: str) -> str | None:
    c = pycountry.countries.get(alpha_3=iso3)
    if not c or not getattr(c, "numeric", None):
        return None
    return str(int(c.numeric))


def build_country_code_map(iso_list: List[str]) -> pd.DataFrame:
    rows = []
    for iso in iso_list:
        m49 = iso3_to_m49(iso)
        rows.append({"iso3": iso, "m49_code": m49})
    out = pd.DataFrame(rows)
    return out


def fetch_wdi_for_indicators(
    session: requests.Session,
    iso_filter: set[str],
    indicators: List[str],
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    fetched_at = datetime.now(timezone.utc).isoformat()
    rows: List[Dict[str, object]] = []

    for indicator in indicators:
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
            data = payload[1] if isinstance(payload[1], list) else []

            for row in data:
                iso3 = row.get("countryiso3code")
                if iso3 not in iso_filter:
                    continue

                year_raw = row.get("date")
                try:
                    year = int(year_raw)
                except Exception:
                    continue
                if year < start_year or year > end_year:
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
                        "indicator_code": indicator_meta.get("id", indicator),
                        "indicator_name": indicator_meta.get("value"),
                        "year": year,
                        "value": value,
                        "fetched_at_utc": fetched_at,
                    }
                )

            page += 1

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out = out.sort_values(["country_iso3", "indicator_code", "year"]).reset_index(drop=True)
    return out


def batched(values: List[str], size: int) -> List[List[str]]:
    return [values[i : i + size] for i in range(0, len(values), size)]


def fetch_comtrade_bilateral(
    session: requests.Session,
    api_key: str,
    reporter_codes: List[str],
    year: int,
    batch_size: int,
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    fetched_at = datetime.now(timezone.utc).isoformat()
    rep_batches = batched(reporter_codes, batch_size)
    par_batches = batched(reporter_codes, batch_size)

    raw_rows: List[Dict[str, object]] = []
    failures: List[Dict[str, object]] = []

    def request_with_retry(params: Dict[str, str], max_attempts: int = 6) -> requests.Response:
        for attempt in range(max_attempts):
            response = session.get(COMTRADE_URL, params=params, timeout=90)
            if response.status_code != 429:
                return response
            sleep_seconds = min(8.0, 1.0 * (2 ** attempt))
            time.sleep(sleep_seconds)
        return response

    for rep in rep_batches:
        for par in par_batches:
            params = {
                "cmdCode": "TOTAL",
                "period": str(year),
                "reporterCode": ",".join(rep),
                "partnerCode": ",".join(par),
                "flowCode": "X",
                "maxRecords": "50000",
                "format": "json",
                "includeDesc": "true",
                "subscription-key": api_key,
            }

            response = request_with_retry(params=params)
            if response.status_code >= 400:
                failures.append(
                    {
                        "status": response.status_code,
                        "reporter_batch": params["reporterCode"],
                        "partner_batch": params["partnerCode"],
                        "response_snippet": response.text[:500],
                    }
                )
                continue

            payload = response.json()
            if isinstance(payload, dict) and payload.get("error"):
                failures.append(
                    {
                        "status": "api_error",
                        "reporter_batch": params["reporterCode"],
                        "partner_batch": params["partnerCode"],
                        "response_snippet": str(payload.get("error"))[:500],
                    }
                )
                continue

            data = payload.get("data") if isinstance(payload, dict) else None
            if not isinstance(data, list):
                continue

            for row in data:
                raw_rows.append(
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
                        "fetched_at_utc": fetched_at,
                    }
                )

    out = pd.DataFrame(raw_rows)
    if out.empty:
        summary = {
            "raw_rows": 0,
            "normalized_rows": 0,
            "failed_batches": failures,
            "year": year,
        }
        return out, summary

    out = out.assign(
        year=pd.to_numeric(out["year"], errors="coerce"),
        trade_value_usd=pd.to_numeric(out["trade_value_usd"], errors="coerce"),
    )
    out = out.dropna(subset=["reporter_iso", "partner_iso", "year", "trade_value_usd"]).copy()
    out = out.assign(year=out["year"].astype(int))
    out = out.loc[out["trade_value_usd"] >= 0].copy()
    out = out.loc[out["reporter_iso"] != out["partner_iso"]].copy()

    normalized = (
        out.groupby(["reporter_iso", "partner_iso", "year"], as_index=False)["trade_value_usd"]
        .sum()
        .sort_values(["reporter_iso", "partner_iso", "year"])
        .reset_index(drop=True)
    )

    summary = {
        "raw_rows": int(len(out)),
        "normalized_rows": int(len(normalized)),
        "failed_batches": failures,
        "year": year,
    }
    return normalized, summary


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.trust_env = False

    countries = fetch_world_bank_countries(session)
    americas_iso3 = get_americas_iso3(countries)
    iso_set = set(americas_iso3)

    code_map = build_country_code_map(americas_iso3)
    code_map = code_map.loc[code_map["m49_code"].notna()].copy()
    reporter_codes = code_map["m49_code"].astype(str).tolist()

    wdi = fetch_wdi_for_indicators(
        session=session,
        iso_filter=iso_set,
        indicators=parse_csv_list(args.indicators),
        start_year=args.start_year,
        end_year=args.end_year,
    )

    api_key = load_api_key(args.settings_path, args.api_key_env)
    comtrade, comtrade_summary = fetch_comtrade_bilateral(
        session=session,
        api_key=api_key,
        reporter_codes=reporter_codes,
        year=args.year,
        batch_size=args.batch_size,
    )

    date_stamp = args.date_stamp
    metadata_dir = output_root / "metadata"
    wdi_dir = output_root / "wdi"
    comtrade_dir = output_root / "comtrade"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    wdi_dir.mkdir(parents=True, exist_ok=True)
    comtrade_dir.mkdir(parents=True, exist_ok=True)

    map_path = metadata_dir / f"americas_iso_m49_{date_stamp}.csv"
    wdi_path = wdi_dir / f"wdi_americas_core_long_{date_stamp}.csv"
    comtrade_path = comtrade_dir / f"comtrade_americas_total_x_{args.year}_{date_stamp}.csv"
    summary_path = comtrade_dir / f"comtrade_americas_pull_summary_{args.year}_{date_stamp}.json"

    code_map.to_csv(map_path, index=False)
    wdi.to_csv(wdi_path, index=False)
    comtrade.to_csv(comtrade_path, index=False)
    summary_path.write_text(json.dumps(comtrade_summary, indent=2), encoding="utf-8")

    print(f"Americas ISO count: {len(americas_iso3)}")
    print(f"Reporter code count: {len(reporter_codes)}")
    print(f"WDI rows: {len(wdi)}")
    print(f"Comtrade rows: {len(comtrade)}")
    print(f"Code map: {map_path}")
    print(f"WDI: {wdi_path}")
    print(f"Comtrade: {comtrade_path}")
    print(f"Comtrade summary: {summary_path}")


if __name__ == "__main__":
    main()
