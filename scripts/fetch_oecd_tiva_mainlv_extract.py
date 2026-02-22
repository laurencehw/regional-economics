"""Fetch a constrained OECD TiVA (Main indicators, levels) extract.

Dataflow:
- OECD.STI.PIE / DSD_TIVA_MAINLV@DF_MAINLV / version 1.1
- Base endpoint: https://sdmx.oecd.org/sti-public/rest
"""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests


BASE_URL = "https://sdmx.oecd.org/sti-public/rest"
FLOW_REF = "OECD.STI.PIE,DSD_TIVA_MAINLV@DF_MAINLV,1.1"
NS = {
    "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch constrained OECD TiVA MainLV extract")
    parser.add_argument("--measure", default="EXGR_DVA")
    parser.add_argument(
        "--ref-areas",
        default="CHN,JPN,KOR,IND,IDN,VNM,THA,MYS,PHL,SGP",
        help="Comma-separated REF_AREA codes",
    )
    parser.add_argument("--activity", default="_T")
    parser.add_argument("--counterpart-area", default="OECD")
    parser.add_argument("--unit-measure", default="USD")
    parser.add_argument("--freq", default="A")
    parser.add_argument("--start-period", default="2000")
    parser.add_argument("--end-period", default="2023")
    parser.add_argument(
        "--output-csv",
        default="data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--metadata-json",
        default="data/raw/metadata/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.json",
        help="Metadata JSON output path",
    )
    parser.add_argument("--timeout", type=int, default=120)
    return parser.parse_args()


def parse_csv_list(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def build_key(args: argparse.Namespace) -> str:
    ref_areas = "+".join(parse_csv_list(args.ref_areas))
    parts = [
        args.measure,
        ref_areas,
        args.activity,
        args.counterpart_area,
        args.unit_measure,
        args.freq,
    ]
    return ".".join(parts)


def fetch_xml(url: str, timeout: int) -> bytes:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def parse_generic_data(xml_bytes: bytes) -> pd.DataFrame:
    root = ET.fromstring(xml_bytes)
    rows: List[Dict[str, object]] = []

    for series in root.findall(".//generic:Series", NS):
        key_vals: Dict[str, str] = {}
        for kv in series.findall("generic:SeriesKey/generic:Value", NS):
            key_vals[kv.attrib.get("id", "")] = kv.attrib.get("value", "")

        for obs in series.findall("generic:Obs", NS):
            t = obs.find("generic:ObsDimension", NS)
            v = obs.find("generic:ObsValue", NS)
            if t is None or v is None:
                continue
            val = v.attrib.get("value")
            if val is None:
                continue
            rows.append(
                {
                    **key_vals,
                    "TIME_PERIOD": t.attrib.get("value"),
                    "OBS_VALUE": float(val),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out = out.assign(TIME_PERIOD=pd.to_numeric(out["TIME_PERIOD"], errors="coerce"))
    out = out.dropna(subset=["TIME_PERIOD"]).copy()
    out = out.assign(TIME_PERIOD=out["TIME_PERIOD"].astype(int))
    out = out.sort_values(["REF_AREA", "COUNTERPART_AREA", "TIME_PERIOD"]).reset_index(drop=True)
    return out


def main() -> None:
    args = parse_args()
    fetched_at = datetime.now(timezone.utc).isoformat()

    key = build_key(args)
    query_url = (
        f"{BASE_URL}/data/{FLOW_REF}/{key}"
        f"?startPeriod={args.start_period}&endPeriod={args.end_period}"
    )

    xml_bytes = fetch_xml(query_url, timeout=args.timeout)
    df = parse_generic_data(xml_bytes)

    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    metadata_json = Path(args.metadata_json)
    metadata_json.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "fetched_at_utc": fetched_at,
        "flow_ref": FLOW_REF,
        "query_url": query_url,
        "query_key": key,
        "rows": int(len(df)),
        "ref_areas": sorted(df["REF_AREA"].unique().tolist()) if not df.empty else [],
        "time_min": int(df["TIME_PERIOD"].min()) if not df.empty else None,
        "time_max": int(df["TIME_PERIOD"].max()) if not df.empty else None,
    }
    metadata_json.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Rows written: {len(df)}")
    print(f"Output CSV: {output_csv}")
    print(f"Metadata: {metadata_json}")


if __name__ == "__main__":
    main()
