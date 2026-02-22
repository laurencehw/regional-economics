"""Build Lab 2 country/activity concordance templates from WIOD + TiVA metadata.

Outputs in `data/processed/lab2/`:
- wiod_niots_country_codes_<date>.csv
- tiva_ref_area_allowed_<date>.csv
- wiod_tiva_country_concordance_<date>.csv
- tiva_activity_codebook_<date>.csv
- wiod_tiva_concordance_summary_<date>.json
"""

from __future__ import annotations

import argparse
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set
import xml.etree.ElementTree as ET

import pandas as pd
import requests


NS = {
    "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}

TIVA_CONSTRAINT_URL = (
    "https://sdmx.oecd.org/sti-public/rest/availableconstraint/"
    "OECD.STI.PIE,DSD_TIVA_MAINLV@DF_MAINLV,1.1"
)
AREA_CODELIST_URL = "https://sdmx.oecd.org/sti-public/rest/codelist/all/CL_AREA/latest"
ACTIVITY_CODELIST_URL = "https://sdmx.oecd.org/sti-public/rest/codelist/all/CL_ACTIVITY_ISIC4/latest"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build WIOD-TiVA concordance templates for Lab 2")
    parser.add_argument(
        "--niots-zip",
        default="data/external/wiod/2016_release/NIOTS.zip",
        help="Path to WIOD NIOTS zip file",
    )
    parser.add_argument(
        "--tiva-csv",
        default="data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv",
        help="Path to constrained TiVA extract CSV",
    )
    parser.add_argument(
        "--out-dir",
        default="data/processed/lab2",
        help="Output directory for concordance artifacts",
    )
    parser.add_argument("--date-stamp", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--timeout", type=int, default=120)
    return parser.parse_args()


def niots_country_codes(niots_zip: Path) -> List[str]:
    with zipfile.ZipFile(niots_zip) as zf:
        names = zf.namelist()

    out: Set[str] = set()
    for name in names:
        base = Path(name).name
        if not base.endswith("_NIOT_nov16.xlsx"):
            continue
        code = base.split("_", 1)[0].strip().upper()
        if len(code) == 3 and code.isalnum():
            out.add(code)
    return sorted(out)


def parse_code_list(xml_bytes: bytes) -> Dict[str, str]:
    root = ET.fromstring(xml_bytes)
    codes: Dict[str, str] = {}
    for code in root.findall(".//structure:Codelist/structure:Code", NS):
        cid = code.attrib.get("id")
        if not cid:
            continue
        name_el = code.find("common:Name", NS)
        name = name_el.text.strip() if name_el is not None and name_el.text else ""
        codes[cid] = name
    return codes


def parse_constraint_values(xml_bytes: bytes, key_id: str) -> List[str]:
    root = ET.fromstring(xml_bytes)
    for kv in root.findall(".//common:KeyValue", NS):
        if kv.attrib.get("id") != key_id:
            continue
        vals = [v.text.strip() for v in kv.findall("common:Value", NS) if v.text]
        return sorted(set(vals))
    return []


def fetch_xml(url: str, timeout: int) -> bytes:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def main() -> None:
    args = parse_args()
    niots_zip = Path(args.niots_zip)
    tiva_csv = Path(args.tiva_csv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not niots_zip.exists():
        raise FileNotFoundError(f"NIOTS zip not found: {niots_zip}")
    if not tiva_csv.exists():
        raise FileNotFoundError(f"TiVA CSV not found: {tiva_csv}")

    # Local inputs
    wiod_codes = niots_country_codes(niots_zip)
    tiva_extract = pd.read_csv(tiva_csv)
    if "REF_AREA" not in tiva_extract.columns:
        raise ValueError(f"TiVA extract missing required REF_AREA column: {tiva_csv}")
    tiva_extract_ref = sorted(set(tiva_extract["REF_AREA"].astype(str).str.upper()))

    # OECD metadata
    constraint_xml = fetch_xml(TIVA_CONSTRAINT_URL, timeout=args.timeout)
    area_xml = fetch_xml(AREA_CODELIST_URL, timeout=args.timeout)
    activity_xml = fetch_xml(ACTIVITY_CODELIST_URL, timeout=args.timeout)

    allowed_ref_areas = parse_constraint_values(constraint_xml, "REF_AREA")
    allowed_activities = parse_constraint_values(constraint_xml, "ACTIVITY")
    area_names = parse_code_list(area_xml)
    activity_names = parse_code_list(activity_xml)

    # Output 1: WIOD country code list
    wiod_df = pd.DataFrame({"wiod_iso3": wiod_codes})
    wiod_path = out_dir / f"wiod_niots_country_codes_{args.date_stamp}.csv"
    wiod_df.to_csv(wiod_path, index=False)

    # Output 2: TiVA allowed ref areas
    tiva_allowed_df = pd.DataFrame({"ref_area": allowed_ref_areas})
    tiva_allowed_df = tiva_allowed_df.assign(
        area_name=tiva_allowed_df["ref_area"].map(area_names).fillna(""),
        in_tiva_extract=tiva_allowed_df["ref_area"].isin(tiva_extract_ref),
    )
    tiva_allowed_path = out_dir / f"tiva_ref_area_allowed_{args.date_stamp}.csv"
    tiva_allowed_df.to_csv(tiva_allowed_path, index=False)

    # Output 3: country concordance template
    all_codes = sorted(set(wiod_codes) | set(allowed_ref_areas))
    concordance = pd.DataFrame({"iso3": all_codes})
    concordance = concordance.assign(
        area_name=concordance["iso3"].map(area_names).fillna(""),
        in_wiod_niots=concordance["iso3"].isin(wiod_codes),
        in_tiva_allowed=concordance["iso3"].isin(allowed_ref_areas),
        in_tiva_extract=concordance["iso3"].isin(tiva_extract_ref),
        include_lab2=False,
        notes="",
    )
    # Default include marker for countries present in constrained extract.
    concordance.loc[concordance["in_tiva_extract"], "include_lab2"] = True
    concordance_path = out_dir / f"wiod_tiva_country_concordance_{args.date_stamp}.csv"
    concordance.to_csv(concordance_path, index=False)

    # Output 4: activity codebook
    activity_df = pd.DataFrame({"activity_code": allowed_activities})
    activity_df = activity_df.assign(
        activity_name=activity_df["activity_code"].map(activity_names).fillna(""),
        is_total_activity=activity_df["activity_code"].eq("_T"),
        include_lab2=activity_df["activity_code"].eq("_T"),
        notes="",
    )
    activity_path = out_dir / f"tiva_activity_codebook_{args.date_stamp}.csv"
    activity_df.to_csv(activity_path, index=False)

    summary = {
        "date_stamp": args.date_stamp,
        "niots_zip": str(niots_zip),
        "tiva_csv": str(tiva_csv),
        "wiod_country_count": int(len(wiod_codes)),
        "tiva_allowed_ref_area_count": int(len(allowed_ref_areas)),
        "tiva_extract_ref_area_count": int(len(tiva_extract_ref)),
        "country_overlap_count": int(len(set(wiod_codes) & set(allowed_ref_areas))),
        "activity_code_count": int(len(allowed_activities)),
        "outputs": {
            "wiod_country_codes": str(wiod_path),
            "tiva_ref_area_allowed": str(tiva_allowed_path),
            "country_concordance": str(concordance_path),
            "activity_codebook": str(activity_path),
        },
    }
    summary_path = out_dir / f"wiod_tiva_concordance_summary_{args.date_stamp}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"WIOD country codes: {len(wiod_codes)}")
    print(f"TiVA allowed REF_AREA codes: {len(allowed_ref_areas)}")
    print(f"Country overlap: {summary['country_overlap_count']}")
    print(f"Activity codes: {len(allowed_activities)}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
