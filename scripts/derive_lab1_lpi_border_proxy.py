"""Derive a Lab 1 border-friction proxy from World Bank LPI series.

Proxy logic:
- Start from WDI long-format LPI indicator values by country-year.
- Interpolate each country onto a full yearly panel.
- Convert LPI quality to friction via within-year inversion:
  border_delay_index = 1 - minmax(lpi_score)
- Optionally blend with BTS proxy where available (BTS wins by default).

Output schema is compatible with Lab 1 mapping:
- region
- year
- border_delay_index
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Derive LPI-based border proxy for Lab 1")
    parser.add_argument(
        "--input-csv",
        default="data/raw/wdi/wdi_lpi_americas_long.csv",
        help="Input WDI long CSV with LPI rows",
    )
    parser.add_argument(
        "--indicator-code",
        default="LP.LPI.OVRL.XQ",
        help="LPI indicator code to filter",
    )
    parser.add_argument("--start-year", type=int, default=2018)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument(
        "--bts-input-csv",
        default=None,
        help="Optional BTS proxy CSV with columns region,year,border_delay_index",
    )
    parser.add_argument("--prefer-bts", dest="prefer_bts", action="store_true")
    parser.add_argument("--no-prefer-bts", dest="prefer_bts", action="store_false")
    parser.set_defaults(prefer_bts=True)
    parser.add_argument(
        "--output-csv",
        default="data/processed/lab1/border_delay_proxy_americas_lpi_2018_2025.csv",
        help="Output CSV path",
    )
    return parser.parse_args()


def interpolate_country_years(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    years = np.arange(start_year, end_year + 1, dtype=int)
    parts: List[pd.DataFrame] = []
    for region, grp in df.groupby("region", sort=True):
        series = grp.set_index("year")["lpi_score"].sort_index()
        frame = pd.DataFrame({"year": years})
        frame = frame.assign(region=region)
        frame = frame.merge(
            series.rename("lpi_score").reset_index(),
            on="year",
            how="left",
        )
        frame = frame.assign(
            lpi_score=frame["lpi_score"].interpolate(method="linear", limit_direction="both")
        )
        parts.append(frame)

    panel = pd.concat(parts, ignore_index=True)
    panel = panel.dropna(subset=["lpi_score"]).copy()
    return panel


def scale_to_friction(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy(deep=True)

    def _to_friction(s: pd.Series) -> np.ndarray:
        v = s.to_numpy(dtype=float)
        v_min = np.nanmin(v)
        v_max = np.nanmax(v)
        if np.isnan(v_min) or np.isnan(v_max):
            return np.full_like(v, np.nan, dtype=float)
        if abs(v_max - v_min) < 1e-12:
            return np.full_like(v, 0.5, dtype=float)
        scaled = (v - v_min) / (v_max - v_min)
        return 1.0 - scaled

    out = out.assign(border_delay_index=out.groupby("year")["lpi_score"].transform(_to_friction))
    return out


def load_bts(path: str) -> pd.DataFrame:
    bts = pd.read_csv(path)
    needed = {"region", "year", "border_delay_index"}
    missing = needed - set(bts.columns)
    if missing:
        raise ValueError(f"BTS proxy missing required columns: {sorted(missing)}")
    bts = bts[["region", "year", "border_delay_index"]].copy()
    bts = bts.assign(
        region=bts["region"].astype(str).str.upper().str.strip(),
        year=pd.to_numeric(bts["year"], errors="coerce"),
        border_delay_index=pd.to_numeric(bts["border_delay_index"], errors="coerce"),
    )
    bts = bts.dropna(subset=["region", "year", "border_delay_index"]).copy()
    bts = bts.assign(year=bts["year"].astype(int))
    return bts


def main() -> None:
    args = parse_args()
    raw = pd.read_csv(args.input_csv)

    needed = {"country_iso3", "indicator_code", "year", "value"}
    missing = needed - set(raw.columns)
    if missing:
        raise ValueError(f"Input CSV missing required columns: {sorted(missing)}")

    lpi = raw.loc[raw["indicator_code"] == args.indicator_code, ["country_iso3", "year", "value"]].copy()
    lpi = lpi.assign(
        region=lpi["country_iso3"].astype(str).str.upper().str.strip(),
        year=pd.to_numeric(lpi["year"], errors="coerce"),
        lpi_score=pd.to_numeric(lpi["value"], errors="coerce"),
    )
    lpi = lpi.dropna(subset=["region", "year", "lpi_score"]).copy()
    lpi = lpi.assign(year=lpi["year"].astype(int))
    lpi = lpi.loc[(lpi["year"] >= args.start_year) & (lpi["year"] <= args.end_year)].copy()

    if lpi.empty:
        raise ValueError("No usable LPI rows found for selected year range and indicator code.")

    panel = interpolate_country_years(lpi[["region", "year", "lpi_score"]], args.start_year, args.end_year)
    panel = scale_to_friction(panel)
    panel = panel.assign(proxy_source="lpi")

    if args.bts_input_csv:
        bts = load_bts(args.bts_input_csv).assign(proxy_source="bts")
        merged = panel.merge(
            bts.rename(columns={"border_delay_index": "border_delay_index_bts", "proxy_source": "proxy_source_bts"}),
            on=["region", "year"],
            how="left",
        )
        if args.prefer_bts:
            merged = merged.assign(
                border_delay_index=np.where(
                    merged["border_delay_index_bts"].notna(),
                    merged["border_delay_index_bts"],
                    merged["border_delay_index"],
                ),
                proxy_source=np.where(
                    merged["border_delay_index_bts"].notna(),
                    "bts",
                    "lpi",
                ),
            )
        panel = merged.drop(columns=["border_delay_index_bts", "proxy_source_bts"])

    out = panel[["region", "year", "border_delay_index", "lpi_score", "proxy_source"]].copy()
    out = out.sort_values(["region", "year"]).reset_index(drop=True)

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    print(f"Rows written: {len(out)}")
    print(f"Regions: {out['region'].nunique()}")
    print(f"Years: {out['year'].min()}-{out['year'].max()}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
