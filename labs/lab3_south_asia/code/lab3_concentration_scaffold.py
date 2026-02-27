"""Lab 3 scaffold for IT-BPO spatial concentration analysis.

This script supports two modes:
1. Smoke test mode with synthetic data.
2. Real-data mode using a canonical panel CSV.

Computes Location Quotients, Herfindahl index, and Gini coefficient
for IT-sector concentration across Indian states.

Outputs are written to the selected output directory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lab 3 South Asia IT-BPO concentration scaffold"
    )
    parser.add_argument(
        "--panel", type=str, default=None, help="Path to canonical panel CSV"
    )
    parser.add_argument(
        "--year", type=int, default=2018, help="Cross-section year"
    )
    parser.add_argument(
        "--region-col", type=str, default="region"
    )
    parser.add_argument(
        "--it-va-col", type=str, default="it_va",
        help="Column with IT-sector value-added",
    )
    parser.add_argument(
        "--total-gdp-col", type=str, default="total_gdp",
        help="Column with total GDP",
    )
    parser.add_argument(
        "--va-per-worker-col", type=str, default="va_per_worker",
        help="Column with value-added per IT worker (for smile curve)",
    )
    parser.add_argument(
        "--it-emp-share-col", type=str, default="it_emp_share",
        help="Column with IT employment share (skill intensity proxy)",
    )
    parser.add_argument("--output-dir", type=str, default="../output")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def prepare_cross_section(
    panel_df: pd.DataFrame,
    year: int,
    region_col: str,
    it_va_col: str,
    total_gdp_col: str,
) -> pd.DataFrame:
    required = [region_col, "year", it_va_col, total_gdp_col]
    missing = [c for c in required if c not in panel_df.columns]
    if missing:
        raise ValueError(f"Missing panel columns: {missing}")

    xsec = panel_df.loc[panel_df["year"] == year].copy()
    xsec = xsec.dropna(subset=[region_col, it_va_col, total_gdp_col])
    xsec = xsec.drop_duplicates(subset=[region_col])
    xsec = xsec.sort_values(region_col).reset_index(drop=True)

    if xsec.shape[0] < 3:
        raise ValueError(
            "Need at least 3 regions in the selected year for concentration analysis."
        )
    return xsec


def compute_location_quotients(
    it_va: np.ndarray, total_gdp: np.ndarray
) -> np.ndarray:
    """Compute Location Quotients: (IT_s / GDP_s) / (sum(IT) / sum(GDP))."""
    national_it_share = it_va.sum() / total_gdp.sum()
    state_it_shares = np.where(total_gdp > 0, it_va / total_gdp, 0.0)
    lq = np.where(national_it_share > 0, state_it_shares / national_it_share, 0.0)
    return lq


def compute_herfindahl(it_va: np.ndarray) -> float:
    """Compute Herfindahl-Hirschman Index for IT-sector concentration."""
    total = it_va.sum()
    if total <= 0:
        return 0.0
    shares = it_va / total
    return float(np.sum(shares ** 2))


def compute_gini(values: np.ndarray) -> float:
    """Compute Gini coefficient for a distribution of non-negative values."""
    v = np.sort(values[values >= 0])
    n = len(v)
    if n < 2 or v.sum() <= 0:
        return 0.0
    cumulative = np.cumsum(v)
    numerator = 2.0 * np.sum((np.arange(1, n + 1)) * v) - (n + 1) * v.sum()
    return float(numerator / (n * v.sum()))


def compute_time_series_hhi(
    panel_df: pd.DataFrame,
    region_col: str,
    it_va_col: str,
) -> List[Dict[str, object]]:
    """Compute HHI for each year in the panel."""
    results = []
    for year, group in panel_df.groupby("year"):
        it_va = group[it_va_col].to_numpy(dtype=float)
        hhi = compute_herfindahl(it_va)
        results.append({"year": int(year), "hhi": hhi, "n_regions": len(group)})
    return sorted(results, key=lambda x: x["year"])


def synthetic_inputs() -> pd.DataFrame:
    """Generate synthetic Indian state IT-sector data for smoke testing."""
    rng = np.random.default_rng(42)

    states = [
        "Karnataka",
        "Telangana",
        "Maharashtra",
        "Tamil Nadu",
        "Delhi NCR",
        "Uttar Pradesh",
        "West Bengal",
        "Kerala",
        "Rajasthan",
        "Gujarat",
        "Madhya Pradesh",
        "Bihar",
    ]

    # IT intensity varies dramatically by state (mimicking real concentration)
    it_intensity = np.array([
        0.20, 0.17, 0.05, 0.04, 0.06, 0.004, 0.013, 0.03, 0.005, 0.015, 0.003, 0.001
    ])
    total_gdp_base = np.array([
        5000, 4000, 18000, 10000, 6000, 12000, 7000, 4500, 6500, 9000, 5500, 3500
    ])

    rows = []
    for yr in range(2015, 2019):
        growth = 1.0 + 0.08 * (yr - 2015) + rng.normal(0, 0.01, len(states))
        it_growth = 1.0 + 0.12 * (yr - 2015) + rng.normal(0, 0.02, len(states))
        gdp = total_gdp_base * growth
        it_va = gdp * it_intensity * it_growth

        # Employment: IT has higher VA per worker in top clusters
        va_per_worker_base = np.array([
            0.72, 0.68, 0.75, 0.60, 0.65, 0.40, 0.45, 0.55, 0.38, 0.50, 0.35, 0.30
        ])
        va_per_worker = va_per_worker_base * (1 + rng.normal(0, 0.02, len(states)))
        it_emp = np.where(va_per_worker > 0, it_va / va_per_worker, 0)
        total_emp = gdp / (0.08 + rng.normal(0, 0.005, len(states)))
        it_emp_share = np.where(total_emp > 0, it_emp / total_emp, 0)

        for i, state in enumerate(states):
            rows.append({
                "region": state,
                "year": yr,
                "it_va": float(it_va[i]),
                "total_gdp": float(gdp[i]),
                "it_share": float(it_va[i] / gdp[i]),
                "it_employment": float(it_emp[i]),
                "total_employment": float(total_emp[i]),
                "it_emp_share": float(it_emp_share[i]),
                "va_per_worker": float(va_per_worker[i]),
            })

    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    if args.run_smoke_test:
        panel_df = synthetic_inputs()
    else:
        if not args.panel:
            raise ValueError("Provide --panel or use --run-smoke-test.")
        panel_df = pd.read_csv(args.panel)

    # --- Cross-section analysis ---
    xsec = prepare_cross_section(
        panel_df, args.year, args.region_col, args.it_va_col, args.total_gdp_col
    )
    regions = xsec[args.region_col].tolist()
    it_va = xsec[args.it_va_col].to_numpy(dtype=float)
    total_gdp = xsec[args.total_gdp_col].to_numpy(dtype=float)

    # Location Quotients
    lq = compute_location_quotients(it_va, total_gdp)

    # HHI and Gini
    hhi = compute_herfindahl(it_va)
    gini = compute_gini(it_va)

    # --- Time series HHI ---
    hhi_series = compute_time_series_hhi(panel_df, args.region_col, args.it_va_col)

    # --- Build results dataframe ---
    results_df = pd.DataFrame({
        "region": regions,
        "it_va": it_va,
        "total_gdp": total_gdp,
        "it_share": np.where(total_gdp > 0, it_va / total_gdp, 0.0),
        "location_quotient": lq,
    })

    if args.va_per_worker_col in xsec.columns and args.it_emp_share_col in xsec.columns:
        results_df = results_df.assign(
            va_per_worker=xsec[args.va_per_worker_col].to_numpy(dtype=float),
            it_emp_share=xsec[args.it_emp_share_col].to_numpy(dtype=float),
        )

    # --- Summary ---
    summary: Dict[str, object] = {
        "method": "Concentration_Analysis",
        "year": int(args.year),
        "n_regions": int(len(regions)),
        "herfindahl_index": hhi,
        "gini_coefficient": gini,
        "top_3_regions_by_lq": [
            {"region": r, "lq": float(l)}
            for r, l in sorted(
                zip(regions, lq), key=lambda x: x[1], reverse=True
            )[:3]
        ],
        "top_3_regions_by_it_share": [
            {"region": r, "share": float(s)}
            for r, s in sorted(
                zip(regions, it_va / it_va.sum()),
                key=lambda x: x[1],
                reverse=True,
            )[:3]
        ],
        "hhi_time_series": hhi_series,
    }

    # --- Write outputs ---
    results_df.to_csv(output_dir / "concentration_results.csv", index=False)
    with (output_dir / "model_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"HHI: {hhi:.4f}")
    print(f"Gini: {gini:.4f}")
    print(f"Top LQ: {summary['top_3_regions_by_lq'][0]['region']} "
          f"({summary['top_3_regions_by_lq'][0]['lq']:.2f})")


if __name__ == "__main__":
    main()
