"""Compare two Lab 2 TiVA MainLV extracts with identical scope keys.

Outputs:
- country-year comparison CSV
- compact summary JSON with overlap and scale diagnostics
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pandas as pd


KEY_COLS = [
    "REF_AREA",
    "ACTIVITY",
    "COUNTERPART_AREA",
    "UNIT_MEASURE",
    "FREQ",
    "TIME_PERIOD",
]
VALUE_COL = "OBS_VALUE"
MEASURE_COL = "MEASURE"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two Lab 2 TiVA measure extracts")
    parser.add_argument(
        "--base-csv",
        default="data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv",
        help="Baseline TiVA extract CSV",
    )
    parser.add_argument(
        "--alt-csv",
        default="data/raw/tiva/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.csv",
        help="Alternative TiVA extract CSV",
    )
    parser.add_argument(
        "--output-csv",
        default="data/processed/lab2/tiva_measure_comparison_exgr_dva_vs_exgr_fnl_2026-02-23.csv",
        help="Output CSV path for merged comparisons",
    )
    parser.add_argument(
        "--summary-json",
        default="data/processed/lab2/tiva_measure_comparison_summary_exgr_dva_vs_exgr_fnl_2026-02-23.json",
        help="Output summary JSON path",
    )
    return parser.parse_args()


def read_required(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = set(KEY_COLS + [VALUE_COL, MEASURE_COL])
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns in {path}: {missing}")
    return df


def main() -> None:
    args = parse_args()
    fetched_at = datetime.now(timezone.utc).isoformat()

    base_path = Path(args.base_csv)
    alt_path = Path(args.alt_csv)
    if not base_path.exists():
        raise FileNotFoundError(f"Base CSV not found: {base_path}")
    if not alt_path.exists():
        raise FileNotFoundError(f"Alternative CSV not found: {alt_path}")

    base = read_required(base_path).copy()
    alt = read_required(alt_path).copy()

    base_measure = (
        base[MEASURE_COL].dropna().astype(str).unique().tolist()
    )
    alt_measure = (
        alt[MEASURE_COL].dropna().astype(str).unique().tolist()
    )

    base = base[KEY_COLS + [VALUE_COL]].rename(columns={VALUE_COL: "obs_base"})
    alt = alt[KEY_COLS + [VALUE_COL]].rename(columns={VALUE_COL: "obs_alt"})

    merged = base.merge(alt, on=KEY_COLS, how="inner", validate="one_to_one").copy()
    base_nonzero = merged["obs_base"].where(merged["obs_base"] != 0)
    merged = merged.assign(
        gap_alt_minus_base=merged["obs_alt"] - merged["obs_base"],
        ratio_alt_to_base=merged["obs_alt"] / base_nonzero,
    )
    merged = merged.assign(
        pct_gap_alt_vs_base=100.0 * merged["gap_alt_minus_base"] / base_nonzero
    )

    out_csv = Path(args.output_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out_csv, index=False)

    corr = merged["obs_base"].corr(merged["obs_alt"]) if not merged.empty else None
    summary = {
        "generated_at_utc": fetched_at,
        "base_csv": str(base_path),
        "alt_csv": str(alt_path),
        "base_measure_codes": base_measure,
        "alt_measure_codes": alt_measure,
        "rows_base": int(len(base)),
        "rows_alt": int(len(alt)),
        "rows_overlap": int(len(merged)),
        "ref_area_count": int(merged["REF_AREA"].nunique()) if not merged.empty else 0,
        "time_min": int(merged["TIME_PERIOD"].min()) if not merged.empty else None,
        "time_max": int(merged["TIME_PERIOD"].max()) if not merged.empty else None,
        "global_corr_base_alt": float(corr) if corr is not None else None,
        "mean_ratio_alt_to_base": float(merged["ratio_alt_to_base"].mean()) if not merged.empty else None,
        "median_ratio_alt_to_base": float(merged["ratio_alt_to_base"].median()) if not merged.empty else None,
        "mean_pct_gap_alt_vs_base": float(merged["pct_gap_alt_vs_base"].mean()) if not merged.empty else None,
        "output_csv": str(out_csv),
    }

    summary_json = Path(args.summary_json)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Rows (base): {len(base)}")
    print(f"Rows (alt): {len(alt)}")
    print(f"Rows (overlap): {len(merged)}")
    print(f"Summary: {summary_json}")
    print(f"Comparison CSV: {out_csv}")


if __name__ == "__main__":
    main()
