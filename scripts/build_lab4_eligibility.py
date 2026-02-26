"""Construct a proxy EU Cohesion Policy eligibility file from Eurostat GDP data.

The real EU rule uses GDP per capita in PPS; we approximate with total
regional GDP levels. Regions whose average GDP over a reference period
falls below 75 % of the cross-regional median are classified as eligible
("less developed"). This produces a valid sharp-RDD forcing variable.

Outputs
-------
- eligibility CSV: nuts2_code, programming_period, gdp_pc_pps,
  eu_threshold_75pct, eligible
- construction summary JSON with region counts and threshold
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build proxy eligibility from Eurostat GDP data"
    )
    parser.add_argument("--gdp-input", required=True, help="Path to Eurostat GDP CSV")
    parser.add_argument("--ref-start", type=int, default=2014,
                        help="Start of reference period (inclusive)")
    parser.add_argument("--ref-end", type=int, default=2016,
                        help="End of reference period (inclusive)")
    parser.add_argument("--threshold-pct", type=float, default=0.75,
                        help="Threshold as fraction of EU-wide median")
    parser.add_argument("--min-ref-years", type=int, default=2,
                        help="Minimum reference-period years required per region")
    parser.add_argument(
        "--output",
        default="labs/lab4_europe/data/real_europe/eligibility_constructed.csv",
        help="Output eligibility CSV path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    gdp = pd.read_csv(args.gdp_input)

    for col in ["nuts2_code", "year", "gdp_value"]:
        if col not in gdp.columns:
            raise ValueError(f"GDP file missing required column: {col}")

    gdp = gdp.assign(
        year=pd.to_numeric(gdp["year"], errors="coerce"),
        gdp_value=pd.to_numeric(gdp["gdp_value"], errors="coerce"),
    )
    gdp = gdp.dropna(subset=["nuts2_code", "year", "gdp_value"])
    gdp = gdp.assign(year=gdp["year"].astype(int))

    ref = gdp.loc[
        (gdp["year"] >= args.ref_start) & (gdp["year"] <= args.ref_end)
    ].copy()

    if ref.empty:
        raise ValueError(
            f"No data in reference period {args.ref_start}-{args.ref_end}. "
            "Check --ref-start / --ref-end."
        )

    year_counts = ref.groupby("nuts2_code")["year"].nunique()
    valid_regions = year_counts[year_counts >= args.min_ref_years].index
    ref = ref.loc[ref["nuts2_code"].isin(valid_regions)].copy()

    region_avg = (
        ref.groupby("nuts2_code", as_index=False)["gdp_value"]
        .mean()
        .rename(columns={"gdp_value": "gdp_pc_pps"})
    )

    eu_median = float(np.median(region_avg["gdp_pc_pps"]))
    threshold = args.threshold_pct * eu_median

    region_avg["eu_threshold_75pct"] = threshold
    region_avg["eligible"] = (region_avg["gdp_pc_pps"] < threshold).astype(int)
    region_avg["programming_period"] = f"{args.ref_start}-{args.ref_end + 4}"

    out_cols = [
        "nuts2_code", "programming_period", "gdp_pc_pps",
        "eu_threshold_75pct", "eligible",
    ]
    region_avg = region_avg[out_cols].sort_values("nuts2_code").reset_index(drop=True)

    region_avg.to_csv(output_path, index=False)

    n_treated = int((region_avg["eligible"] == 1).sum())
    n_control = int((region_avg["eligible"] == 0).sum())

    summary = {
        "ref_period": [args.ref_start, args.ref_end],
        "threshold_pct": args.threshold_pct,
        "eu_median_gdp": eu_median,
        "threshold_value": threshold,
        "total_regions": int(region_avg.shape[0]),
        "treated_regions": n_treated,
        "control_regions": n_control,
        "treated_share": float(n_treated / region_avg.shape[0]) if region_avg.shape[0] > 0 else 0.0,
    }

    summary_path = output_path.parent / "eligibility_construction_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote eligibility: {output_path}")
    print(f"Wrote summary: {summary_path}")
    print(f"  Threshold: {threshold:.2f} (75% of median {eu_median:.2f})")
    print(f"  Treated: {n_treated}, Control: {n_control}")


if __name__ == "__main__":
    main()
