"""Derive a simple border-friction proxy for Lab 1 from BTS border crossings.

Proxy logic:
- Use monthly truck crossings by border.
- Compute yearly coefficient of variation (std/mean) by border.
- Min-max scale within year across the two borders.
- Map to CAN and MEX directly; USA gets weighted average across borders.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Derive BTS border proxy for Lab 1")
    parser.add_argument(
        "--input-csv",
        default="data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv",
    )
    parser.add_argument(
        "--output-csv",
        default="data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv",
    )
    return parser.parse_args()


def scale_within_year(df: pd.DataFrame) -> pd.DataFrame:
    out = df.sort_values(["year", "border"]).reset_index(drop=True).copy()

    def _scale_values(s: pd.Series) -> np.ndarray:
        v = s.to_numpy(dtype=float)
        v_min = np.nanmin(v)
        v_max = np.nanmax(v)
        if np.isnan(v_min) or np.isnan(v_max):
            scaled = np.full_like(v, np.nan, dtype=float)
        elif abs(v_max - v_min) < 1e-12:
            scaled = np.full_like(v, 0.5, dtype=float)
        else:
            scaled = (v - v_min) / (v_max - v_min)
        return scaled

    out = out.assign(border_delay_index=out.groupby("year")["cv"].transform(_scale_values))
    return out


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input_csv)

    if df.empty:
        raise ValueError("Input BTS file is empty")

    df = df.copy(deep=True)
    df = df.assign(
        date=pd.to_datetime(df["date"], errors="coerce"),
        value=pd.to_numeric(df["value"], errors="coerce"),
    )

    df = df.loc[
        df["date"].notna()
        & df["value"].notna()
        & (df["measure"] == "Trucks")
        & df["border"].isin(["US-Canada Border", "US-Mexico Border"])
    ].copy()

    if df.empty:
        raise ValueError("No usable rows after filtering BTS data")

    df = df.assign(year=df["date"].dt.year, month=df["date"].dt.month)

    monthly = (
        df.groupby(["border", "year", "month"], as_index=False)["value"]
        .sum()
        .sort_values(["border", "year", "month"])
        .reset_index(drop=True)
    )

    yearly = (
        monthly.groupby(["border", "year"], as_index=False)
        .agg(mean_trucks=("value", "mean"), std_trucks=("value", "std"), annual_trucks=("value", "sum"))
    )
    yearly = yearly.assign(std_trucks=yearly["std_trucks"].fillna(0.0))
    yearly = yearly.assign(
        cv=np.where(yearly["mean_trucks"] > 0, yearly["std_trucks"] / yearly["mean_trucks"], np.nan)
    )

    scaled = scale_within_year(yearly[["border", "year", "cv", "annual_trucks"]])

    can = scaled.loc[
        scaled["border"] == "US-Canada Border", ["year", "border_delay_index", "annual_trucks"]
    ].copy()
    can = can.assign(region="CAN")

    mex = scaled.loc[
        scaled["border"] == "US-Mexico Border", ["year", "border_delay_index", "annual_trucks"]
    ].copy()
    mex = mex.assign(region="MEX")

    usa_join = can.merge(mex, on="year", how="inner", suffixes=("_can", "_mex"))
    total = usa_join["annual_trucks_can"] + usa_join["annual_trucks_mex"]
    usa = pd.DataFrame(
        {
            "region": "USA",
            "year": usa_join["year"],
            "border_delay_index": np.where(
                total > 0,
                (usa_join["border_delay_index_can"] * usa_join["annual_trucks_can"]
                 + usa_join["border_delay_index_mex"] * usa_join["annual_trucks_mex"]) / total,
                np.nan,
            ),
        }
    )

    out = pd.concat(
        [
            can[["region", "year", "border_delay_index"]],
            mex[["region", "year", "border_delay_index"]],
            usa[["region", "year", "border_delay_index"]],
        ],
        ignore_index=True,
    )
    out = out.sort_values(["region", "year"]).reset_index(drop=True)

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Rows written: {len(out)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
