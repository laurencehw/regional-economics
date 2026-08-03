"""Prepare canonical Lab 2 inputs from TiVA DVA, FNL, and gross-export extracts.

Canonical DVA share:
    dva_share = EXGR_DVA / EXGR

EXGR_FNL is retained as a companion foreign-content indicator. It is **not**
the gross-export denominator and must not be used to invent a share when
EXGR is missing.

Outputs:
- panel_mapped.csv with columns:
  country, year, dva_value, fnl_value, exgr_value, dva_share, dva_ratio,
  dva_growth, dva_lag, dva_share_growth, dva_share_lag
- mapping_summary.json with coverage and denominator diagnostics
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd


CANONICAL_PANEL_COLS = [
    "country",
    "year",
    "dva_value",
    "fnl_value",
    "exgr_value",
    "dva_share",
    "dva_ratio",
    "dva_growth",
    "dva_lag",
    "dva_share_growth",
    "dva_share_lag",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Map raw TiVA sources into Lab 2 canonical inputs")
    parser.add_argument("--base-input", required=True, help="Path to TiVA base CSV (EXGR_DVA)")
    parser.add_argument("--alt-input", required=True, help="Path to TiVA alt CSV (EXGR_FNL)")
    parser.add_argument(
        "--exgr-input",
        default=None,
        help="Path to TiVA gross-exports CSV (EXGR). Required for validated dva_share.",
    )
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


def normalize_tiva(tiva_df: pd.DataFrame, cfg: Dict[str, object], value_name: str) -> pd.DataFrame:
    """Normalize a TiVA extract to [country, year, <value_name>]."""
    ref_area_col = str(cfg["ref_area_col"])
    time_period_col = str(cfg["time_period_col"])
    obs_value_col = str(cfg["obs_value_col"])

    missing = [c for c in [ref_area_col, time_period_col, obs_value_col] if c not in tiva_df.columns]
    if missing:
        raise ValueError(f"TiVA file missing required columns: {missing}")

    out = tiva_df[[ref_area_col, time_period_col, obs_value_col]].copy(deep=True)
    out = to_numeric_years(out, time_period_col)
    out = out.assign(**{obs_value_col: pd.to_numeric(out[obs_value_col], errors="coerce")})
    out = out.dropna(subset=[ref_area_col, obs_value_col]).copy()

    out = (
        out.groupby([ref_area_col, time_period_col], as_index=False)[obs_value_col]
        .sum()
    )

    out = out.rename(
        columns={ref_area_col: "country", time_period_col: "year", obs_value_col: value_name}
    )
    return out[["country", "year", value_name]]


def build_panel(
    base_df: pd.DataFrame,
    alt_df: pd.DataFrame,
    exgr_df: Optional[pd.DataFrame],
    year_filter: int | None,
) -> pd.DataFrame:
    panel = base_df.merge(alt_df, on=["country", "year"], how="left")
    if exgr_df is not None:
        panel = panel.merge(exgr_df, on=["country", "year"], how="left")
    else:
        panel["exgr_value"] = np.nan

    panel = panel.copy()
    fnl_safe = panel["fnl_value"].replace(0, np.nan)
    panel.loc[:, "dva_ratio"] = panel["dva_value"] / fnl_safe

    exgr_safe = panel["exgr_value"].replace(0, np.nan)
    panel.loc[:, "dva_share"] = panel["dva_value"] / exgr_safe
    # Shares outside [0, 1] indicate denominator/vintage mismatch; keep NaN rather than clip.
    invalid = (panel["dva_share"] < 0) | (panel["dva_share"] > 1)
    panel.loc[invalid, "dva_share"] = np.nan

    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)
    panel.loc[:, "dva_growth"] = panel.groupby("country")["dva_value"].pct_change() * 100
    panel.loc[:, "dva_lag"] = panel.groupby("country")["dva_value"].shift(1)
    # Percentage-point change in the share (scaled by 100)
    panel.loc[:, "dva_share_growth"] = panel.groupby("country")["dva_share"].diff() * 100
    panel.loc[:, "dva_share_lag"] = panel.groupby("country")["dva_share"].shift(1)

    if year_filter is not None:
        panel = panel.loc[panel["year"] == year_filter].copy()

    panel = (
        panel.reindex(columns=CANONICAL_PANEL_COLS)
        .sort_values(["country", "year"])
        .reset_index(drop=True)
    )
    return panel


def main() -> None:
    args = parse_args()

    mapping_path = Path(args.mappings)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mapping = load_mapping(mapping_path)

    base_raw = pd.read_csv(args.base_input)
    alt_raw = pd.read_csv(args.alt_input)
    exgr_raw = pd.read_csv(args.exgr_input) if args.exgr_input else None

    base_norm = normalize_tiva(base_raw, mapping["tiva"], "dva_value")
    alt_norm = normalize_tiva(alt_raw, mapping["tiva"], "fnl_value")
    exgr_norm = (
        normalize_tiva(exgr_raw, mapping["tiva"], "exgr_value") if exgr_raw is not None else None
    )
    panel = build_panel(base_norm, alt_norm, exgr_norm, args.year)

    if panel.empty:
        raise ValueError("Mapped panel is empty. Check input files and year filter.")

    panel_path = output_dir / "panel_mapped.csv"
    summary_path = output_dir / "mapping_summary.json"

    panel.to_csv(panel_path, index=False)

    share_valid = panel["dva_share"].notna()
    summary = {
        "panel_rows": int(panel.shape[0]),
        "panel_countries": int(panel["country"].nunique()),
        "panel_years": sorted(int(y) for y in panel["year"].dropna().unique()),
        "denominator": "EXGR" if exgr_norm is not None else None,
        "dva_share_definition": "EXGR_DVA / EXGR",
        "exgr_provided": bool(exgr_norm is not None),
        "missing_fnl_share": float(panel["fnl_value"].isna().mean()),
        "missing_exgr_share": float(panel["exgr_value"].isna().mean()),
        "missing_dva_share": float(panel["dva_share"].isna().mean()),
        "missing_dva_growth_share": float(panel["dva_growth"].isna().mean()),
        "valid_dva_share_rows": int(share_valid.sum()),
        "dva_share_range": (
            [float(panel.loc[share_valid, "dva_share"].min()),
             float(panel.loc[share_valid, "dva_share"].max())]
            if share_valid.any()
            else None
        ),
        "dva_ratio_note": (
            "dva_ratio = EXGR_DVA / EXGR_FNL is retained for diagnostics only; "
            "it is not a domestic-content share."
        ),
    }
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote mapped panel: {panel_path}")
    print(f"Wrote mapping summary: {summary_path}")
    if exgr_norm is None:
        print("WARNING: No --exgr-input provided; dva_share is missing.")
    else:
        print(
            f"Valid dva_share rows: {summary['valid_dva_share_rows']} / {summary['panel_rows']}"
        )


if __name__ == "__main__":
    main()
