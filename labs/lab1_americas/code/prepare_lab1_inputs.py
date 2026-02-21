"""Prepare canonical Lab 1 inputs from raw WDI, Comtrade, and BTS extracts.

Outputs:
- panel_mapped.csv with columns:
  region, year, gdp_growth, log_gdp_pc, manufacturing_share, border_delay_index
- trade_mapped.csv with columns:
  origin, destination, year, trade_value
- mapping_summary.json with row counts and coverage diagnostics
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


CANONICAL_PANEL_COLS = [
    "region",
    "year",
    "gdp_growth",
    "log_gdp_pc",
    "manufacturing_share",
    "border_delay_index",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Map raw data sources into Lab 1 canonical inputs")
    parser.add_argument("--wdi-input", required=True, help="Path to WDI CSV (wide or long format)")
    parser.add_argument("--comtrade-input", required=True, help="Path to Comtrade bilateral CSV")
    parser.add_argument("--bts-input", required=True, help="Path to BTS border-delay CSV")
    parser.add_argument("--mappings", default="../data/source_mappings.json", help="Path to mapping JSON")
    parser.add_argument("--output-dir", default="../data", help="Directory for mapped outputs")
    parser.add_argument("--year", type=int, default=None, help="Optional year filter for trade output")
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


def normalize_wdi(wdi_df: pd.DataFrame, cfg: Dict[str, object]) -> pd.DataFrame:
    region_col = cfg["region_col"]
    indicator_col = cfg["indicator_code_col"]
    year_col = cfg.get("year_col", "year")
    value_col = cfg.get("value_col", "value")
    indicator_map = cfg["indicator_to_feature"]

    if year_col in wdi_df.columns and value_col in wdi_df.columns:
        long_df = wdi_df[[region_col, indicator_col, year_col, value_col]].copy(deep=True)
    else:
        year_like_cols = [c for c in wdi_df.columns if re.fullmatch(r"\d{4}", str(c))]
        needed = [region_col, indicator_col]
        missing = [c for c in needed if c not in wdi_df.columns]
        if missing:
            raise ValueError(f"WDI file missing required columns: {missing}")
        if not year_like_cols:
            raise ValueError("Could not detect yearly columns in WDI file.")

        long_df = wdi_df[[region_col, indicator_col, *year_like_cols]].melt(
            id_vars=[region_col, indicator_col],
            var_name=year_col,
            value_name=value_col,
        )

    long_df = to_numeric_years(long_df, year_col)
    long_df = long_df.assign(**{value_col: pd.to_numeric(long_df[value_col], errors="coerce")})
    long_df = long_df.dropna(subset=[value_col]).copy()
    long_df = long_df.loc[long_df[indicator_col].isin(indicator_map.keys())].copy()

    if long_df.empty:
        raise ValueError("No WDI rows matched configured indicator codes.")

    long_df = long_df.assign(feature=long_df[indicator_col].map(indicator_map))
    panel = long_df.pivot_table(
        index=[region_col, year_col],
        columns="feature",
        values=value_col,
        aggfunc="first",
    ).reset_index()

    panel = panel.rename(columns={region_col: "region", year_col: "year"})

    if "gdp_per_capita_constant" in panel.columns:
        gdp_pc = pd.to_numeric(panel["gdp_per_capita_constant"], errors="coerce")
        panel = panel.assign(log_gdp_pc=np.where(gdp_pc > 0, np.log(gdp_pc), np.nan))
    elif "log_gdp_pc" not in panel.columns:
        panel = panel.assign(log_gdp_pc=np.nan)

    return panel


def normalize_bts(bts_df: pd.DataFrame, cfg: Dict[str, object]) -> pd.DataFrame:
    region_col = cfg["region_col"]
    year_col = cfg["year_col"]
    border_col = cfg["border_delay_col"]

    missing = [c for c in [region_col, year_col, border_col] if c not in bts_df.columns]
    if missing:
        raise ValueError(f"BTS file missing required columns: {missing}")

    out = bts_df[[region_col, year_col, border_col]].copy(deep=True)
    out = to_numeric_years(out, year_col)
    out = out.assign(**{border_col: pd.to_numeric(out[border_col], errors="coerce")})
    out = out.rename(columns={region_col: "region", year_col: "year", border_col: "border_delay_index"})
    out = out.dropna(subset=["region", "year"]).copy()
    return out


def build_panel(wdi_df: pd.DataFrame, bts_df: pd.DataFrame) -> pd.DataFrame:
    panel = wdi_df.merge(bts_df, on=["region", "year"], how="left")

    for col in CANONICAL_PANEL_COLS:
        if col not in panel.columns:
            panel = panel.assign(**{col: np.nan})

    panel = panel[CANONICAL_PANEL_COLS].sort_values(["region", "year"]).reset_index(drop=True)
    return panel


def normalize_comtrade(comtrade_df: pd.DataFrame, cfg: Dict[str, object], year_filter: int | None) -> pd.DataFrame:
    origin_col = cfg["origin_col"]
    destination_col = cfg["destination_col"]
    year_col = cfg["year_col"]
    value_col = cfg["trade_value_col"]

    missing = [c for c in [origin_col, destination_col, year_col, value_col] if c not in comtrade_df.columns]
    if missing:
        raise ValueError(f"Comtrade file missing required columns: {missing}")

    trade = comtrade_df[[origin_col, destination_col, year_col, value_col]].copy(deep=True)
    trade = trade.rename(
        columns={
            origin_col: "origin",
            destination_col: "destination",
            year_col: "year",
            value_col: "trade_value",
        }
    )

    trade = to_numeric_years(trade, "year")
    trade = trade.assign(trade_value=pd.to_numeric(trade["trade_value"], errors="coerce"))
    trade = trade.dropna(subset=["origin", "destination", "trade_value"]).copy()
    trade = trade.loc[trade["trade_value"] >= 0].copy()
    trade = trade.loc[trade["origin"] != trade["destination"]].copy()

    if year_filter is not None:
        trade = trade.loc[trade["year"] == year_filter].copy()

    trade = (
        trade.groupby(["origin", "destination", "year"], as_index=False)["trade_value"]
        .sum()
        .sort_values(["origin", "destination", "year"])
        .reset_index(drop=True)
    )
    return trade


def main() -> None:
    args = parse_args()

    mapping_path = Path(args.mappings)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mapping = load_mapping(mapping_path)

    wdi_raw = pd.read_csv(args.wdi_input)
    comtrade_raw = pd.read_csv(args.comtrade_input)
    bts_raw = pd.read_csv(args.bts_input)

    wdi_panel = normalize_wdi(wdi_raw, mapping["wdi"])
    bts_panel = normalize_bts(bts_raw, mapping["bts"])
    panel = build_panel(wdi_panel, bts_panel)

    trade = normalize_comtrade(comtrade_raw, mapping["comtrade"], args.year)

    panel_path = output_dir / "panel_mapped.csv"
    trade_path = output_dir / "trade_mapped.csv"
    summary_path = output_dir / "mapping_summary.json"

    panel.to_csv(panel_path, index=False)
    trade.to_csv(trade_path, index=False)

    summary = {
        "panel_rows": int(panel.shape[0]),
        "panel_regions": int(panel["region"].nunique()),
        "panel_years": sorted(int(y) for y in panel["year"].dropna().unique()),
        "trade_rows": int(trade.shape[0]),
        "trade_years": sorted(int(y) for y in trade["year"].dropna().unique()),
        "missing_border_delay_share": float(panel["border_delay_index"].isna().mean()),
    }
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote mapped panel: {panel_path}")
    print(f"Wrote mapped trade: {trade_path}")
    print(f"Wrote mapping summary: {summary_path}")


if __name__ == "__main__":
    main()
