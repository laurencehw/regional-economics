"""Fetch BTS Border Crossing Entry Data (keg4-3bc2) via Socrata API."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import List

import pandas as pd
import requests

BASE_URL = "https://data.bts.gov/resource/keg4-3bc2.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch BTS border crossing data")
    parser.add_argument("--start-date", default="2015-01-01T00:00:00.000")
    parser.add_argument("--limit", type=int, default=50000)
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument(
        "--where",
        default="border in ('US-Canada Border','US-Mexico Border')",
        help="Socrata where clause (without date filter)",
    )
    parser.add_argument(
        "--output-csv",
        default="data/raw/bts/bts_border_crossings_keg4_3bc2.csv",
        help="Output CSV path",
    )
    return parser.parse_args()


def fetch_page(offset: int, limit: int, where_clause: str) -> pd.DataFrame:
    session = requests.Session()
    session.trust_env = False
    params = {
        "$select": "port_name,state,port_code,border,date,measure,value,latitude,longitude",
        "$where": where_clause,
        "$order": "date ASC, port_code ASC",
        "$limit": str(limit),
        "$offset": str(offset),
    }
    response = session.get(BASE_URL, params=params, timeout=90)
    response.raise_for_status()
    text = response.text.strip()
    if not text:
        return pd.DataFrame()
    return pd.read_csv(StringIO(text))


def main() -> None:
    args = parse_args()
    where_clause = f"({args.where}) and date >= '{args.start_date}'"
    fetched_at = datetime.now(timezone.utc).isoformat()

    frames: List[pd.DataFrame] = []
    for page in range(args.max_pages):
        offset = page * args.limit
        df = fetch_page(offset=offset, limit=args.limit, where_clause=where_clause)
        if df.empty:
            break
        df["fetched_at_utc"] = fetched_at
        frames.append(df)
        if len(df) < args.limit:
            break

    if frames:
        out = pd.concat(frames, ignore_index=True)
    else:
        out = pd.DataFrame(
            columns=[
                "port_name",
                "state",
                "port_code",
                "border",
                "date",
                "measure",
                "value",
                "latitude",
                "longitude",
                "fetched_at_utc",
            ]
        )

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Rows written: {len(out)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
