"""Fetch Eurostat NUTS-2 GDP panel and NUTS 2024 geometry for Lab 3.

GDP dataset:
- nama_10r_2gdp (regional GDP)
- API endpoint: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/

Geometry source (GISCO):
- https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests


EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
GDP_CODE = "nama_10r_2gdp"
NUTS_GEOJSON_2024_20M = (
    "https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/"
    "ref-nuts-2024-20m.geojson.zip"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Eurostat NUTS-2 GDP + NUTS reference geometry")
    parser.add_argument("--dataset-code", default=GDP_CODE)
    parser.add_argument("--unit", default="MIO_EUR", help="GDP unit to keep")
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument(
        "--output-csv",
        default="data/raw/eurostat/nama_10r_2gdp_nuts2_mio_eur_2000_2024_2026-02-22.csv",
    )
    parser.add_argument(
        "--geometry-zip",
        default="data/raw/eurostat/ref-nuts-2024-20m.geojson.zip",
    )
    parser.add_argument(
        "--metadata-json",
        default="data/raw/metadata/eurostat_nuts2_pull_2026-02-22.json",
    )
    parser.add_argument("--skip-geometry", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    return parser.parse_args()


def decode_index(flat_idx: int, sizes: List[int]) -> List[int]:
    # Eurostat JSON uses a flattened index over dimensions in order of `id`.
    out = [0] * len(sizes)
    rem = flat_idx
    for i in range(len(sizes) - 1, -1, -1):
        s = sizes[i]
        out[i] = rem % s
        rem //= s
    return out


def invert_category_index(mapping: Dict[str, int]) -> List[str]:
    out = [None] * len(mapping)
    for code, idx in mapping.items():
        out[idx] = code
    return [x for x in out if x is not None]


def is_nuts2_code(code: str) -> bool:
    # NUTS2 region codes are typically 4 characters (e.g., DE11, FR10, ES61).
    if not isinstance(code, str) or len(code) != 4:
        return False
    if not code[:2].isalpha():
        return False
    return all(ch.isalnum() for ch in code)


def fetch_gdp_json(dataset_code: str, timeout: int) -> Dict[str, object]:
    url = f"{EUROSTAT_BASE}/{dataset_code}"
    params = {"format": "JSON", "lang": "EN"}
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def tidy_gdp_payload(payload: Dict[str, object]) -> pd.DataFrame:
    dim_ids = payload["id"]
    sizes = payload["size"]
    dim_code_lists: Dict[str, List[str]] = {}
    for dim in dim_ids:
        mapping = payload["dimension"][dim]["category"]["index"]
        dim_code_lists[dim] = invert_category_index(mapping)

    rows = []
    values = payload.get("value", {})
    status = payload.get("status", {})
    for key_str, value in values.items():
        flat_idx = int(key_str)
        coords = decode_index(flat_idx, sizes)
        record = {}
        for d, c in zip(dim_ids, coords):
            record[d] = dim_code_lists[d][c]
        record["value"] = float(value)
        record["status"] = status.get(key_str)
        rows.append(record)

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out = out.assign(time=pd.to_numeric(out["time"], errors="coerce"))
    out = out.dropna(subset=["time"]).copy()
    out = out.assign(time=out["time"].astype(int))
    out = out.sort_values(["geo", "time"]).reset_index(drop=True)
    return out


def main() -> None:
    args = parse_args()
    fetched_at = datetime.now(timezone.utc).isoformat()

    payload = fetch_gdp_json(args.dataset_code, timeout=args.timeout)
    tidy = tidy_gdp_payload(payload)

    # Filter to NUTS-2 + chosen unit + year window.
    tidy = tidy.loc[
        (tidy["unit"] == args.unit)
        & tidy["geo"].map(is_nuts2_code)
        & (tidy["time"] >= args.start_year)
        & (tidy["time"] <= args.end_year)
    ].copy()
    tidy = tidy.rename(
        columns={
            "freq": "frequency",
            "unit": "unit",
            "geo": "nuts2_code",
            "time": "year",
            "value": "gdp_value",
        }
    )
    tidy = tidy[["frequency", "unit", "nuts2_code", "year", "gdp_value", "status"]]

    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    tidy.to_csv(output_csv, index=False)

    geometry_written = None
    if not args.skip_geometry:
        geometry_zip = Path(args.geometry_zip)
        geometry_zip.parent.mkdir(parents=True, exist_ok=True)
        with requests.get(NUTS_GEOJSON_2024_20M, stream=True, timeout=args.timeout) as response:
            response.raise_for_status()
            with geometry_zip.open("wb") as fp:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        fp.write(chunk)
        geometry_written = str(geometry_zip)

    metadata_json = Path(args.metadata_json)
    metadata_json.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "fetched_at_utc": fetched_at,
        "dataset_code": args.dataset_code,
        "source_url": f"{EUROSTAT_BASE}/{args.dataset_code}",
        "source_updated": payload.get("updated"),
        "unit_filter": args.unit,
        "year_range": [args.start_year, args.end_year],
        "rows_written": int(len(tidy)),
        "nuts2_regions": int(tidy["nuts2_code"].nunique()) if not tidy.empty else 0,
        "output_csv": str(output_csv),
        "geometry_url": NUTS_GEOJSON_2024_20M if not args.skip_geometry else None,
        "geometry_zip": geometry_written,
    }
    metadata_json.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Rows written: {len(tidy)}")
    print(f"NUTS-2 regions: {metadata['nuts2_regions']}")
    print(f"Output CSV: {output_csv}")
    if geometry_written:
        print(f"Geometry ZIP: {geometry_written}")
    print(f"Metadata: {metadata_json}")


if __name__ == "__main__":
    main()
