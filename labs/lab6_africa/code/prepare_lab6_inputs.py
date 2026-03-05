"""Prepare canonical Lab 6 inputs from VIIRS, Afrobarometer, and adjacency extracts.

Outputs:
- panel_mapped.csv with columns:
  region, year, night_lights_mean, governance_score
- adjacency_mapped.csv with columns:
  region, neighbor, weight
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


CANONICAL_PANEL_COLS = ["region", "year", "night_lights_mean", "governance_score"]
CANONICAL_ADJ_COLS = ["region", "neighbor", "weight"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Map raw data sources into Lab 6 canonical inputs")
    parser.add_argument("--viirs-input", required=True, help="Path to VIIRS CSV (wide or long format)")
    parser.add_argument("--afrobarometer-input", default=None, help="Path to Afrobarometer governance CSV (optional; omit to skip governance merge)")
    parser.add_argument("--adjacency-input", required=True, help="Path to adjacency edge-list CSV")
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


def normalize_viirs(viirs_df: pd.DataFrame, cfg: Dict[str, object]) -> pd.DataFrame:
    region_col = str(cfg["region_col"])
    year_col = str(cfg.get("year_col", "year"))
    value_col = str(cfg["radiance_col"])

    if year_col in viirs_df.columns and value_col in viirs_df.columns:
        long_df = viirs_df[[region_col, year_col, value_col]].copy(deep=True)
    else:
        year_like_cols = [c for c in viirs_df.columns if re.fullmatch(r"\d{4}", str(c))]
        needed = [region_col]
        missing = [c for c in needed if c not in viirs_df.columns]
        if missing:
            raise ValueError(f"VIIRS file missing required columns: {missing}")
        if not year_like_cols:
            raise ValueError("Could not detect yearly columns in VIIRS file.")

        long_df = viirs_df[[region_col, *year_like_cols]].melt(
            id_vars=[region_col],
            var_name=year_col,
            value_name=value_col,
        )

    long_df = to_numeric_years(long_df, year_col)
    long_df = long_df.assign(**{value_col: pd.to_numeric(long_df[value_col], errors="coerce")})
    long_df = long_df.dropna(subset=[region_col, value_col]).copy()
    long_df = long_df.loc[long_df[value_col] >= 0].copy()

    panel = (
        long_df.groupby([region_col, year_col], as_index=False)[value_col]
        .mean()
        .rename(columns={region_col: "region", year_col: "year", value_col: "night_lights_mean"})
    )
    panel = panel.sort_values(["region", "year"]).reset_index(drop=True)
    return panel


def normalize_afrobarometer(afro_df: pd.DataFrame, cfg: Dict[str, object]) -> pd.DataFrame:
    region_col = str(cfg["region_col"])
    year_col = str(cfg["year_col"])
    value_col = str(cfg["governance_col"])

    missing = [c for c in [region_col, year_col, value_col] if c not in afro_df.columns]
    if missing:
        raise ValueError(f"Afrobarometer file missing required columns: {missing}")

    out = afro_df[[region_col, year_col, value_col]].copy(deep=True)
    out = to_numeric_years(out, year_col)
    out = out.assign(**{value_col: pd.to_numeric(out[value_col], errors="coerce")})
    out = out.dropna(subset=[region_col, value_col]).copy()

    out = (
        out.groupby([region_col, year_col], as_index=False)[value_col]
        .mean()
        .rename(columns={region_col: "region", year_col: "year", value_col: "governance_score"})
    )
    out = out.sort_values(["region", "year"]).reset_index(drop=True)
    return out


def normalize_adjacency(adjacency_df: pd.DataFrame, cfg: Dict[str, object]) -> pd.DataFrame:
    region_col = str(cfg["region_col"])
    neighbor_col = str(cfg["neighbor_col"])
    weight_col = str(cfg.get("weight_col", "weight"))

    needed = [region_col, neighbor_col]
    missing = [c for c in needed if c not in adjacency_df.columns]
    if missing:
        raise ValueError(f"Adjacency file missing required columns: {missing}")

    out = adjacency_df.copy(deep=True)
    if weight_col not in out.columns:
        out = out.assign(**{weight_col: 1.0})

    out = out[[region_col, neighbor_col, weight_col]].copy()
    out = out.rename(columns={region_col: "region", neighbor_col: "neighbor", weight_col: "weight"})
    out = out.assign(
        region=out["region"].astype(str).str.strip().str.upper(),
        neighbor=out["neighbor"].astype(str).str.strip().str.upper(),
        weight=pd.to_numeric(out["weight"], errors="coerce"),
    )
    out = out.dropna(subset=["region", "neighbor", "weight"]).copy()
    out = out.loc[(out["weight"] > 0) & (out["region"] != out["neighbor"])].copy()

    if out.empty:
        raise ValueError("Adjacency normalization produced zero usable links.")

    # Symmetrize links to enforce an undirected neighborhood structure.
    reverse = out.rename(columns={"region": "neighbor", "neighbor": "region"})
    out = (
        pd.concat([out, reverse], ignore_index=True)
        .groupby(["region", "neighbor"], as_index=False)["weight"]
        .sum()
        .sort_values(["region", "neighbor"])
        .reset_index(drop=True)
    )
    return out


def build_panel(viirs_panel: pd.DataFrame, afro_panel: pd.DataFrame, year_filter: int | None) -> pd.DataFrame:
    panel = viirs_panel.merge(afro_panel, on=["region", "year"], how="left")
    if year_filter is not None:
        panel = panel.loc[panel["year"] == year_filter].copy()

    for col in CANONICAL_PANEL_COLS:
        if col not in panel.columns:
            panel = panel.assign(**{col: np.nan})

    panel = panel[CANONICAL_PANEL_COLS].sort_values(["region", "year"]).reset_index(drop=True)
    return panel


def main() -> None:
    args = parse_args()

    mapping_path = Path(args.mappings)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mapping = load_mapping(mapping_path)

    viirs_raw = pd.read_csv(args.viirs_input)
    adjacency_raw = pd.read_csv(args.adjacency_input)

    viirs_panel = normalize_viirs(viirs_raw, mapping["viirs"])

    if args.afrobarometer_input is not None:
        afro_raw = pd.read_csv(args.afrobarometer_input)
        afro_panel = normalize_afrobarometer(afro_raw, mapping["afrobarometer"])
    else:
        afro_panel = pd.DataFrame(columns=["region", "year", "governance_score"])

    adjacency = normalize_adjacency(adjacency_raw, mapping["adjacency"])
    panel = build_panel(viirs_panel, afro_panel, args.year)

    if panel.empty:
        raise ValueError("Mapped panel is empty. Check input files and year filter.")

    panel_path = output_dir / "panel_mapped.csv"
    adjacency_path = output_dir / "adjacency_mapped.csv"
    summary_path = output_dir / "mapping_summary.json"

    panel.to_csv(panel_path, index=False)
    adjacency.to_csv(adjacency_path, index=False)

    summary = {
        "panel_rows": int(panel.shape[0]),
        "panel_regions": int(panel["region"].nunique()),
        "panel_years": sorted(int(y) for y in panel["year"].dropna().unique()),
        "adjacency_rows": int(adjacency.shape[0]),
        "adjacency_regions": int(
            pd.Index(adjacency["region"]).union(pd.Index(adjacency["neighbor"])).nunique()
        ),
        "missing_governance_share": float(panel["governance_score"].isna().mean()),
    }
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote mapped panel: {panel_path}")
    print(f"Wrote mapped adjacency: {adjacency_path}")
    print(f"Wrote mapping summary: {summary_path}")


if __name__ == "__main__":
    main()
