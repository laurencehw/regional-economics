"""Fetch electronics-sector (C26) TiVA EXGR_DVA for 10 Asian economies.

Smoke-test mode generates a calibrated synthetic panel.
Real mode hits the OECD SDMX API with ACTIVITY=C26.
"""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import requests

ECONOMIES = ["CHN", "JPN", "KOR", "IND", "IDN", "VNM", "THA", "MYS", "PHL", "SGP"]
BASE_URL = "https://sdmx.oecd.org/sti-public/rest"
FLOW_REF = "OECD.STI.PIE,DSD_TIVA_MAINLV@DF_MAINLV,1.1"
NS = {
    "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch electronics-sector TiVA DVA for Asian economies"
    )
    parser.add_argument("--run-smoke-test", action="store_true")
    parser.add_argument("--start-period", default="2005")
    parser.add_argument("--end-period", default="2022")
    parser.add_argument("--output-dir", type=str, default="../data")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def synthetic_electronics(seed: int = 42) -> pd.DataFrame:
    """Calibrated synthetic C26 electronics DVA panel.

    Japan/Korea high base, Vietnam/Philippines low but rising fast.
    """
    rng = np.random.default_rng(seed)
    years = list(range(2005, 2023))
    base_dva = {
        "JPN": 120_000, "KOR": 95_000, "CHN": 80_000,
        "SGP": 45_000, "MYS": 22_000, "THA": 18_000,
        "IND": 12_000, "IDN": 10_000, "VNM": 5_000, "PHL": 4_000,
    }
    growth_rates = {
        "JPN": 0.01, "KOR": 0.03, "CHN": 0.08,
        "SGP": 0.04, "MYS": 0.05, "THA": 0.04,
        "IND": 0.06, "IDN": 0.05, "VNM": 0.12, "PHL": 0.07,
    }
    rows: List[Dict] = []
    for eco in ECONOMIES:
        val = base_dva[eco]
        for yr in years:
            noise = rng.normal(0, 0.03)
            val *= 1.0 + growth_rates[eco] + noise
            rows.append({
                "MEASURE": "EXGR_DVA",
                "REF_AREA": eco,
                "ACTIVITY": "C26",
                "COUNTERPART_AREA": "WLD",
                "UNIT_MEASURE": "USD",
                "FREQ": "A",
                "TIME_PERIOD": yr,
                "OBS_VALUE": round(val, 3),
            })
    return pd.DataFrame(rows)


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
            rows.append({
                **key_vals,
                "TIME_PERIOD": t.attrib.get("value"),
                "OBS_VALUE": float(val),
            })
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out = out.assign(TIME_PERIOD=pd.to_numeric(out["TIME_PERIOD"], errors="coerce"))
    out = out.dropna(subset=["TIME_PERIOD"]).copy()
    out = out.assign(TIME_PERIOD=out["TIME_PERIOD"].astype(int))
    out = out.sort_values(["REF_AREA", "TIME_PERIOD"]).reset_index(drop=True)
    return out


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.run_smoke_test:
        df = synthetic_electronics(seed=args.seed)
    else:
        ref_areas = "+".join(ECONOMIES)
        key = f"EXGR_DVA.{ref_areas}.C26.WLD.USD.A"
        query_url = (
            f"{BASE_URL}/data/{FLOW_REF}/{key}"
            f"?startPeriod={args.start_period}&endPeriod={args.end_period}"
        )
        xml_bytes = fetch_xml(query_url, timeout=args.timeout)
        df = parse_generic_data(xml_bytes)

    csv_path = out_dir / "tiva_electronics_dva.csv"
    df.to_csv(csv_path, index=False)

    metadata = {
        "measure": "EXGR_DVA",
        "activity": "C26",
        "description": "Electronics sector (ISIC Rev.4 C26) DVA in gross exports",
        "n_rows": int(len(df)),
        "n_economies": int(df["REF_AREA"].nunique()) if not df.empty else 0,
        "economies": sorted(df["REF_AREA"].unique().tolist()) if not df.empty else [],
        "year_range": [int(df["TIME_PERIOD"].min()), int(df["TIME_PERIOD"].max())]
        if not df.empty else [],
        "smoke_test": args.run_smoke_test,
    }
    meta_path = out_dir / "tiva_electronics_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Rows: {len(df)}")
    print(f"CSV: {csv_path}")
    print(f"Metadata: {meta_path}")


if __name__ == "__main__":
    main()
