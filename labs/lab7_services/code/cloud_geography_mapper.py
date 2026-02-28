"""Lab 7 mapper for cloud infrastructure geography vs. data localization regimes.

This script supports two modes:
1. Smoke test mode with synthetic data for ~15 countries.
2. Real-data mode using cloud-provider and localization CSV inputs.

Computes cloud presence metrics, concentration indices, and the
correlation between data localization restrictiveness and cloud
infrastructure density.

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
        description="Lab 7 Cloud Geography vs. Data Localization Mapper"
    )
    parser.add_argument("--cloud", type=str, default=None, help="Path to cloud CSV")
    parser.add_argument(
        "--localization", type=str, default=None, help="Path to localization CSV"
    )
    parser.add_argument("--output-dir", type=str, default="../data")
    parser.add_argument("--run-smoke-test", action="store_true")
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Synthetic data
# ---------------------------------------------------------------------------

def synthetic_cloud_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate synthetic cloud-provider and localization data for smoke testing.

    Returns (cloud_df, localization_df) where:
        cloud_df columns: country, provider, n_regions
        localization_df columns: country, localization_score, digital_openness, gdp_trillion, pop_million
    """
    # Cloud region counts: (country, AWS, Azure, GCP)
    cloud_spec: List[Tuple[str, int, int, int]] = [
        ("United States", 8, 6, 5),
        ("Germany", 2, 2, 2),
        ("China", 3, 2, 1),
        ("India", 2, 2, 1),
        ("Brazil", 1, 1, 1),
        ("Singapore", 1, 1, 1),
        ("Japan", 2, 2, 1),
        ("Australia", 1, 1, 1),
        ("South Korea", 1, 1, 1),
        ("United Kingdom", 2, 2, 1),
        ("Nigeria", 1, 0, 0),
        ("Kenya", 1, 0, 0),
        ("Indonesia", 1, 1, 0),
        ("Russia", 0, 0, 0),
        ("South Africa", 1, 1, 0),
    ]

    cloud_rows = []
    for country, aws, azure, gcp in cloud_spec:
        for provider, n_regions in [("AWS", aws), ("Azure", azure), ("GCP", gcp)]:
            cloud_rows.append({
                "country": country,
                "provider": provider,
                "n_regions": n_regions,
            })
    cloud_df = pd.DataFrame(cloud_rows)

    # Localization scores and auxiliary indicators
    loc_spec: Dict[str, Dict[str, float]] = {
        "United States":  {"localization_score": 0.10, "digital_openness": 0.90, "gdp_trillion": 25.5, "pop_million": 332.0},
        "Germany":        {"localization_score": 0.30, "digital_openness": 0.70, "gdp_trillion": 4.1,  "pop_million": 83.2},
        "China":          {"localization_score": 0.80, "digital_openness": 0.20, "gdp_trillion": 18.3, "pop_million": 1412.0},
        "India":          {"localization_score": 0.50, "digital_openness": 0.50, "gdp_trillion": 3.4,  "pop_million": 1417.0},
        "Brazil":         {"localization_score": 0.40, "digital_openness": 0.55, "gdp_trillion": 1.9,  "pop_million": 214.0},
        "Singapore":      {"localization_score": 0.15, "digital_openness": 0.88, "gdp_trillion": 0.4,  "pop_million": 5.7},
        "Japan":          {"localization_score": 0.20, "digital_openness": 0.78, "gdp_trillion": 4.2,  "pop_million": 125.0},
        "Australia":      {"localization_score": 0.25, "digital_openness": 0.80, "gdp_trillion": 1.7,  "pop_million": 26.0},
        "South Korea":    {"localization_score": 0.30, "digital_openness": 0.72, "gdp_trillion": 1.7,  "pop_million": 51.7},
        "United Kingdom": {"localization_score": 0.25, "digital_openness": 0.82, "gdp_trillion": 3.1,  "pop_million": 67.5},
        "Nigeria":        {"localization_score": 0.60, "digital_openness": 0.35, "gdp_trillion": 0.5,  "pop_million": 218.0},
        "Kenya":          {"localization_score": 0.35, "digital_openness": 0.55, "gdp_trillion": 0.1,  "pop_million": 54.0},
        "Indonesia":      {"localization_score": 0.55, "digital_openness": 0.40, "gdp_trillion": 1.3,  "pop_million": 275.0},
        "Russia":         {"localization_score": 0.90, "digital_openness": 0.10, "gdp_trillion": 2.2,  "pop_million": 144.0},
        "South Africa":   {"localization_score": 0.30, "digital_openness": 0.60, "gdp_trillion": 0.4,  "pop_million": 60.0},
    }

    loc_rows = []
    for country, vals in loc_spec.items():
        row = {"country": country, "year": 2024}
        row.update(vals)
        loc_rows.append(row)
    localization_df = pd.DataFrame(loc_rows)

    return cloud_df, localization_df


# ---------------------------------------------------------------------------
# Core computations
# ---------------------------------------------------------------------------

def build_country_panel(
    cloud_df: pd.DataFrame,
    localization_df: pd.DataFrame,
) -> pd.DataFrame:
    """Pivot cloud data wide, merge with localization, compute derived metrics."""

    # Pivot: one row per country, one column per provider
    pivot = (
        cloud_df
        .pivot_table(index="country", columns="provider", values="n_regions",
                     aggfunc="sum", fill_value=0)
        .reset_index()
    )
    # Ensure standard provider columns exist
    for prov in ["AWS", "Azure", "GCP"]:
        if prov not in pivot.columns:
            pivot[prov] = 0

    pivot["total_cloud_regions"] = pivot[["AWS", "Azure", "GCP"]].sum(axis=1)

    # Merge localization
    panel = pivot.merge(localization_df, on="country", how="outer")

    # Fill missing region counts with 0
    for col in ["AWS", "Azure", "GCP", "total_cloud_regions"]:
        panel[col] = panel[col].fillna(0).astype(int)

    # Per-capita and per-GDP intensity (avoid div-by-zero)
    panel["regions_per_million_pop"] = np.where(
        panel["pop_million"] > 0,
        panel["total_cloud_regions"] / panel["pop_million"],
        np.nan,
    )
    panel["regions_per_trillion_gdp"] = np.where(
        panel["gdp_trillion"] > 0,
        panel["total_cloud_regions"] / panel["gdp_trillion"],
        np.nan,
    )

    return panel


def compute_summary(panel: pd.DataFrame) -> Dict:
    """Compute concentration, correlation, and summary statistics."""

    total_regions_global = int(panel["total_cloud_regions"].sum())

    # Concentration: share of top-3 countries
    top3 = panel.nlargest(3, "total_cloud_regions")
    top3_share = (
        float(top3["total_cloud_regions"].sum() / total_regions_global)
        if total_regions_global > 0
        else 0.0
    )
    top3_countries = top3["country"].tolist()

    # Herfindahl-Hirschman Index of cloud region distribution
    shares = panel["total_cloud_regions"] / total_regions_global if total_regions_global > 0 else panel["total_cloud_regions"]
    hhi = float((shares ** 2).sum())

    # Correlation: localization_score vs. total_cloud_regions
    valid = panel.dropna(subset=["localization_score", "total_cloud_regions"])
    if len(valid) >= 3:
        corr = float(valid["localization_score"].corr(valid["total_cloud_regions"]))
    else:
        corr = None

    # Countries with zero cloud presence
    zero_cloud = panel.loc[panel["total_cloud_regions"] == 0, "country"].tolist()

    # Provider-level global totals
    provider_totals = {}
    for prov in ["AWS", "Azure", "GCP"]:
        if prov in panel.columns:
            provider_totals[prov] = int(panel[prov].sum())

    summary: Dict = {
        "method": "Cloud_Geography_Mapping",
        "n_countries": int(len(panel)),
        "total_cloud_regions_global": total_regions_global,
        "cloud_concentration": {
            "top3_countries": top3_countries,
            "top3_share": round(top3_share, 4),
            "hhi": round(hhi, 4),
        },
        "correlation_localization_cloud": (
            round(corr, 4) if corr is not None else None
        ),
        "provider_totals": provider_totals,
        "countries_zero_cloud": zero_cloud,
        "localization_score_stats": {
            "mean": round(float(valid["localization_score"].mean()), 4),
            "std": round(float(valid["localization_score"].std()), 4),
            "min": round(float(valid["localization_score"].min()), 4),
            "max": round(float(valid["localization_score"].max()), 4),
        },
        "regions_per_million_pop": {
            "mean": round(float(panel["regions_per_million_pop"].mean()), 4),
            "max_country": panel.loc[
                panel["regions_per_million_pop"].idxmax(), "country"
            ] if panel["regions_per_million_pop"].notna().any() else None,
        },
    }

    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    if args.run_smoke_test:
        cloud_df, localization_df = synthetic_cloud_data()
    else:
        if not args.cloud or not args.localization:
            raise ValueError(
                "Provide --cloud and --localization CSVs, or use --run-smoke-test."
            )
        cloud_df = pd.read_csv(args.cloud)
        localization_df = pd.read_csv(args.localization)

    # --- Build panel ---
    panel = build_country_panel(cloud_df, localization_df)

    # --- Compute summary ---
    summary = compute_summary(panel)

    # --- Write outputs ---
    panel.to_csv(output_dir / "cloud_geography.csv", index=False)
    with (output_dir / "cloud_summary.json").open("w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2)

    print(f"Wrote outputs to: {output_dir}")
    print(f"Countries: {summary['n_countries']}")
    print(f"Global cloud regions: {summary['total_cloud_regions_global']}")
    print(f"Top-3 concentration: {summary['cloud_concentration']['top3_share']:.1%}")
    corr = summary["correlation_localization_cloud"]
    print(f"Localization-cloud correlation: {corr}")
    if summary["countries_zero_cloud"]:
        print(f"Zero cloud presence: {', '.join(summary['countries_zero_cloud'])}")


if __name__ == "__main__":
    main()
