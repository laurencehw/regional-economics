"""Prepare canonical Lab 3 inputs from KLEMS India IT-sector data.

Outputs:
- panel_mapped.csv with columns:
  region, year, it_va, total_gdp, it_share, it_employment, total_employment,
  it_emp_share, va_per_worker
- mapping_summary.json with row counts and coverage diagnostics
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


CANONICAL_PANEL_COLS = [
    "region",
    "year",
    "it_va",
    "total_gdp",
    "it_share",
    "it_employment",
    "total_employment",
    "it_emp_share",
    "va_per_worker",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map raw KLEMS data into Lab 3 canonical inputs"
    )
    parser.add_argument(
        "--klems-input", required=True, help="Path to KLEMS IT-sector CSV"
    )
    parser.add_argument(
        "--mappings",
        default="../data/source_mappings.json",
        help="Path to mapping JSON",
    )
    parser.add_argument(
        "--output-dir", default="../data", help="Directory for mapped outputs"
    )
    parser.add_argument(
        "--year", type=int, default=None, help="Optional year filter"
    )
    return parser.parse_args()


def load_mapping(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def normalize_klems(
    klems_df: pd.DataFrame, cfg: Dict[str, object]
) -> pd.DataFrame:
    region_col = str(cfg["region_col"])
    year_col = str(cfg["year_col"])
    it_va_col = str(cfg["it_va_col"])
    total_gdp_col = str(cfg["total_gdp_col"])
    it_emp_col = str(cfg["it_employment_col"])
    total_emp_col = str(cfg["total_employment_col"])

    required = [region_col, year_col, it_va_col, total_gdp_col]
    missing = [c for c in required if c not in klems_df.columns]
    if missing:
        raise ValueError(f"KLEMS file missing required columns: {missing}")

    out = klems_df.copy(deep=True)
    out = out.assign(
        **{year_col: pd.to_numeric(out[year_col], errors="coerce")}
    )
    out = out.loc[out[year_col].notna()].copy()
    out = out.assign(**{year_col: out[year_col].astype(int)})

    for col in [it_va_col, total_gdp_col]:
        out = out.assign(**{col: pd.to_numeric(out[col], errors="coerce")})

    out = out.dropna(subset=[region_col, it_va_col, total_gdp_col]).copy()

    rename_map = {
        region_col: "region",
        year_col: "year",
        it_va_col: "it_va",
        total_gdp_col: "total_gdp",
    }

    if it_emp_col in out.columns:
        out = out.assign(
            **{it_emp_col: pd.to_numeric(out[it_emp_col], errors="coerce")}
        )
        rename_map[it_emp_col] = "it_employment"
    if total_emp_col in out.columns:
        out = out.assign(
            **{total_emp_col: pd.to_numeric(out[total_emp_col], errors="coerce")}
        )
        rename_map[total_emp_col] = "total_employment"

    out = out.rename(columns=rename_map)

    # Derived columns
    out = out.assign(
        it_share=np.where(
            out["total_gdp"] > 0, out["it_va"] / out["total_gdp"], np.nan
        )
    )

    if "it_employment" in out.columns and "total_employment" in out.columns:
        out = out.assign(
            it_emp_share=np.where(
                out["total_employment"] > 0,
                out["it_employment"] / out["total_employment"],
                np.nan,
            ),
            va_per_worker=np.where(
                out["it_employment"] > 0,
                out["it_va"] / out["it_employment"],
                np.nan,
            ),
        )
    else:
        out = out.assign(it_emp_share=np.nan, va_per_worker=np.nan)

    for col in CANONICAL_PANEL_COLS:
        if col not in out.columns:
            out = out.assign(**{col: np.nan})

    out = out[CANONICAL_PANEL_COLS].sort_values(["region", "year"]).reset_index(
        drop=True
    )
    return out


def main() -> None:
    args = parse_args()

    mapping_path = Path(args.mappings)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mapping = load_mapping(mapping_path)
    klems_raw = pd.read_csv(args.klems_input)

    panel = normalize_klems(klems_raw, mapping["klems"])

    if args.year is not None:
        panel = panel.loc[panel["year"] == args.year].copy()

    if panel.empty:
        raise ValueError("Mapped panel is empty. Check input file and year filter.")

    panel_path = output_dir / "panel_mapped.csv"
    summary_path = output_dir / "mapping_summary.json"

    panel.to_csv(panel_path, index=False)

    summary = {
        "panel_rows": int(panel.shape[0]),
        "panel_regions": int(panel["region"].nunique()),
        "panel_years": sorted(int(y) for y in panel["year"].dropna().unique()),
        "regions": sorted(panel["region"].unique().tolist()),
        "missing_employment_share": float(panel["it_emp_share"].isna().mean()),
    }
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote mapped panel: {panel_path}")
    print(f"Wrote mapping summary: {summary_path}")


if __name__ == "__main__":
    main()
