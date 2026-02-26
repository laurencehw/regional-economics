"""Prepare canonical Lab 4 inputs from Eurostat GDP and eligibility data.

Outputs:
- panel_mapped.csv with columns:
  nuts2_code, year, gdp_mio_eur, gdp_growth, forcing_var, treated
- mapping_summary.json with row counts and coverage diagnostics
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


CANONICAL_PANEL_COLS = ["nuts2_code", "year", "gdp_mio_eur", "gdp_growth", "forcing_var", "treated"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Map raw data sources into Lab 4 canonical inputs")
    parser.add_argument("--eurostat-input", required=True, help="Path to Eurostat GDP CSV")
    parser.add_argument("--eligibility-input", required=True, help="Path to eligibility CSV")
    parser.add_argument("--mappings", default="../data/source_mappings.json", help="Path to mapping JSON")
    parser.add_argument("--output-dir", default="../data", help="Directory for mapped outputs")
    parser.add_argument("--year", type=int, default=None, help="Optional year filter for panel output")
    return parser.parse_args()


def load_mapping(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def to_numeric_years(df: pd.DataFrame, year_col: str) -> pd.DataFrame:
    out = df.copy(deep=True)
    out = out.assign(**{year_col: pd.to_numeric(out[year_col], errors="coerce")})
    out = out.loc[out[year_col].notna()].copy()
    out = out.assign(**{year_col: out[year_col].astype(int)})
    return out


def normalize_eurostat_gdp(gdp_df: pd.DataFrame, cfg: Dict[str, object]) -> pd.DataFrame:
    region_col = str(cfg["region_col"])
    year_col = str(cfg["year_col"])
    gdp_col = str(cfg["gdp_col"])

    missing = [c for c in [region_col, year_col, gdp_col] if c not in gdp_df.columns]
    if missing:
        raise ValueError(f"Eurostat GDP file missing required columns: {missing}")

    out = gdp_df[[region_col, year_col, gdp_col]].copy(deep=True)
    out = to_numeric_years(out, year_col)
    out = out.assign(**{gdp_col: pd.to_numeric(out[gdp_col], errors="coerce")})
    out = out.dropna(subset=[region_col, gdp_col]).copy()

    out = out.sort_values([region_col, year_col]).reset_index(drop=True)
    out["gdp_growth"] = out.groupby(region_col)[gdp_col].pct_change() * 100

    out = out.rename(columns={region_col: "nuts2_code", year_col: "year", gdp_col: "gdp_mio_eur"})
    return out[["nuts2_code", "year", "gdp_mio_eur", "gdp_growth"]]


def normalize_eligibility(elig_df: pd.DataFrame, cfg: Dict[str, object]) -> pd.DataFrame:
    region_col = str(cfg["region_col"])
    gdp_pc_pps_col = str(cfg["gdp_pc_pps_col"])
    threshold_col = str(cfg["threshold_col"])
    eligible_col = str(cfg["eligible_col"])

    missing = [c for c in [region_col, gdp_pc_pps_col, threshold_col, eligible_col]
               if c not in elig_df.columns]
    if missing:
        raise ValueError(f"Eligibility file missing required columns: {missing}")

    out = elig_df[[region_col, gdp_pc_pps_col, threshold_col, eligible_col]].copy(deep=True)
    out = out.assign(
        **{
            gdp_pc_pps_col: pd.to_numeric(out[gdp_pc_pps_col], errors="coerce"),
            threshold_col: pd.to_numeric(out[threshold_col], errors="coerce"),
            eligible_col: pd.to_numeric(out[eligible_col], errors="coerce"),
        }
    )
    out = out.dropna(subset=[region_col, gdp_pc_pps_col, threshold_col]).copy()

    out["forcing_var"] = out[gdp_pc_pps_col] - out[threshold_col]
    out["treated"] = out[eligible_col].astype(int)

    out = out.rename(columns={region_col: "nuts2_code"})
    return out[["nuts2_code", "forcing_var", "treated"]]


def build_panel(
    gdp_panel: pd.DataFrame,
    eligibility: pd.DataFrame,
    year_filter: int | None,
) -> pd.DataFrame:
    panel = gdp_panel.merge(eligibility, on="nuts2_code", how="left")

    if year_filter is not None:
        panel = panel.loc[panel["year"] == year_filter].copy()

    for col in CANONICAL_PANEL_COLS:
        if col not in panel.columns:
            panel = panel.assign(**{col: np.nan})

    panel = panel[CANONICAL_PANEL_COLS].sort_values(["nuts2_code", "year"]).reset_index(drop=True)
    return panel


def main() -> None:
    args = parse_args()

    mapping_path = Path(args.mappings)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mapping = load_mapping(mapping_path)

    gdp_raw = pd.read_csv(args.eurostat_input)
    elig_raw = pd.read_csv(args.eligibility_input)

    gdp_panel = normalize_eurostat_gdp(gdp_raw, mapping["eurostat_gdp"])
    eligibility = normalize_eligibility(elig_raw, mapping["eligibility"])
    panel = build_panel(gdp_panel, eligibility, args.year)

    if panel.empty:
        raise ValueError("Mapped panel is empty. Check input files and year filter.")

    panel_path = output_dir / "panel_mapped.csv"
    summary_path = output_dir / "mapping_summary.json"

    panel.to_csv(panel_path, index=False)

    summary = {
        "panel_rows": int(panel.shape[0]),
        "panel_regions": int(panel["nuts2_code"].nunique()),
        "panel_years": sorted(int(y) for y in panel["year"].dropna().unique()),
        "treated_regions": int(panel.loc[panel["treated"] == 1, "nuts2_code"].nunique()),
        "control_regions": int(panel.loc[panel["treated"] == 0, "nuts2_code"].nunique()),
        "missing_gdp_growth_share": float(panel["gdp_growth"].isna().mean()),
        "forcing_var_range": [float(panel["forcing_var"].min()), float(panel["forcing_var"].max())],
    }
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote mapped panel: {panel_path}")
    print(f"Wrote mapping summary: {summary_path}")


if __name__ == "__main__":
    main()
