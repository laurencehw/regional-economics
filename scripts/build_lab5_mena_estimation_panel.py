"""Build Lab 5 estimation-ready panel by merging ACLED, UNHCR, and WDI.

Inputs:
- ACLED event-level extract (external storage recommended)
- UNHCR mapped country-year controls
- WDI outcome series

Outputs:
- ACLED country-year aggregates
- Lab 5 estimation-ready panel
- Build metadata JSON
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import pandas as pd


COUNTRY_TO_ISO3 = {
    "Egypt": "EGY",
    "Iraq": "IRQ",
    "Jordan": "JOR",
    "Lebanon": "LBN",
    "Libya": "LBY",
    "Morocco": "MAR",
    "Saudi Arabia": "SAU",
    "Syria": "SYR",
    "Tunisia": "TUN",
    "Yemen": "YEM",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Lab 5 MENA estimation-ready panel")
    parser.add_argument(
        "--acled-events-csv",
        default="data/external/acled/acled_lab4_mena_2018_2025_2026-02-23.csv",
        help="ACLED event-level CSV path",
    )
    parser.add_argument(
        "--acled-counts-csv",
        default="data/processed/lab5/acled_lab4_country_year_counts_2018_2025_2026-02-23.csv",
        help="Optional ACLED country-year counts CSV path (used if present)",
    )
    parser.add_argument(
        "--wdi-outcome-csv",
        default="data/raw/wdi/wdi_lab4_mena_outcome_long_2000_2024_2026-02-23.csv",
        help="WDI long-format outcome CSV path",
    )
    parser.add_argument(
        "--unhcr-mapped-csv",
        default="data/processed/lab5/unhcr_lab4_controls_mena_2000_2024_2026-02-23.csv",
        help="UNHCR mapped control CSV path",
    )
    parser.add_argument(
        "--acled-country-year-csv",
        default="data/processed/lab5/acled_lab4_country_year_2018_2025_2026-02-23.csv",
        help="Output path for ACLED country-year aggregates",
    )
    parser.add_argument(
        "--panel-output-csv",
        default="data/processed/lab5/lab4_mena_estimation_panel_2000_2024_2026-02-23.csv",
        help="Output path for estimation-ready panel",
    )
    parser.add_argument(
        "--metadata-json",
        default="data/raw/metadata/lab4_mena_panel_build_2026-02-23.json",
        help="Build metadata JSON path",
    )
    return parser.parse_args()


def to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def build_acled_country_year(acled_events_csv: Path) -> pd.DataFrame:
    try:
        acled = pd.read_csv(acled_events_csv)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["iso3", "year", "acled_event_count", "acled_fatalities_sum", "treatment_event"])

    if acled.empty or len(acled.columns) == 0:
        return pd.DataFrame(columns=["iso3", "year", "acled_event_count", "acled_fatalities_sum", "treatment_event"])

    if "country" not in acled.columns or "event_date" not in acled.columns:
        raise ValueError("ACLED events CSV missing required columns: country/event_date")

    acled = acled.assign(
        iso3=acled["country"].map(COUNTRY_TO_ISO3),
        year=pd.to_datetime(acled["event_date"], errors="coerce").dt.year,
        fatalities=to_numeric(acled["fatalities"]) if "fatalities" in acled.columns else 0.0,
    )
    acled = acled.dropna(subset=["iso3", "year"]).copy()
    acled["year"] = acled["year"].astype(int)

    grouped = (
        acled.groupby(["iso3", "year"], as_index=False)
        .agg(
            acled_event_count=("event_id_cnty", "count"),
            acled_fatalities_sum=("fatalities", "sum"),
        )
        .sort_values(["iso3", "year"])
        .reset_index(drop=True)
    )
    grouped["treatment_event"] = grouped["acled_fatalities_sum"]
    return grouped


def load_acled_counts(acled_counts_csv: Path) -> pd.DataFrame:
    counts = pd.read_csv(acled_counts_csv)
    required = {"iso3", "year", "acled_event_count"}
    missing = sorted(required - set(counts.columns))
    if missing:
        raise ValueError(f"ACLED counts CSV missing columns: {missing}")
    counts = counts.copy()
    counts = counts.assign(year=pd.to_numeric(counts["year"], errors="coerce"))
    counts = counts.dropna(subset=["year"]).copy()
    counts = counts.assign(
        year=counts["year"].astype(int),
        acled_event_count=pd.to_numeric(counts["acled_event_count"], errors="coerce").fillna(0.0),
    )
    if "acled_fatalities_sum" not in counts.columns:
        counts = counts.assign(acled_fatalities_sum=0.0)
    else:
        counts = counts.assign(
            acled_fatalities_sum=pd.to_numeric(counts["acled_fatalities_sum"], errors="coerce").fillna(0.0)
        )
    if "treatment_event" not in counts.columns:
        counts = counts.assign(treatment_event=counts["acled_event_count"])
    else:
        counts = counts.assign(treatment_event=pd.to_numeric(counts["treatment_event"], errors="coerce").fillna(0.0))
    counts = counts[
        ["iso3", "year", "acled_event_count", "acled_fatalities_sum", "treatment_event"]
    ].drop_duplicates(subset=["iso3", "year"], keep="last")
    return counts.reset_index(drop=True).copy()


def build_panel(unhcr_mapped_csv: Path, wdi_outcome_csv: Path, acled_country_year: pd.DataFrame) -> pd.DataFrame:
    unhcr = pd.read_csv(unhcr_mapped_csv)
    wdi = pd.read_csv(wdi_outcome_csv)

    required_unhcr = {"iso3", "year", "refugees_under_mandate", "asylum_seekers", "idps", "total_displaced"}
    missing_unhcr = sorted(required_unhcr - set(unhcr.columns))
    if missing_unhcr:
        raise ValueError(f"UNHCR mapped CSV missing columns: {missing_unhcr}")

    required_wdi = {"country_iso3", "indicator_code", "year", "value"}
    missing_wdi = sorted(required_wdi - set(wdi.columns))
    if missing_wdi:
        raise ValueError(f"WDI CSV missing columns: {missing_wdi}")

    wdi = wdi[wdi["indicator_code"].eq("NY.GDP.PCAP.KD.ZG")].copy()
    wdi = wdi.rename(columns={"country_iso3": "iso3", "value": "outcome_main"})
    wdi = wdi.assign(year=pd.to_numeric(wdi["year"], errors="coerce"))
    wdi = wdi.dropna(subset=["year"]).copy()
    wdi = wdi.assign(
        year=wdi["year"].astype(int),
        outcome_main=pd.to_numeric(wdi["outcome_main"], errors="coerce"),
    )

    panel = unhcr.copy()
    panel = panel.assign(year=pd.to_numeric(panel["year"], errors="coerce"))
    panel = panel.dropna(subset=["year"]).copy()
    panel = panel.assign(year=panel["year"].astype(int))

    panel = panel.merge(
        wdi[["iso3", "year", "outcome_main"]],
        on=["iso3", "year"],
        how="left",
        validate="one_to_one",
    )
    panel = panel.merge(
        acled_country_year,
        on=["iso3", "year"],
        how="left",
        validate="one_to_one",
    )
    panel = panel.assign(
        acled_event_count=to_numeric(panel.get("acled_event_count", pd.Series(dtype=float))),
        acled_fatalities_sum=to_numeric(panel.get("acled_fatalities_sum", pd.Series(dtype=float))),
        treatment_event=to_numeric(panel.get("treatment_event", pd.Series(dtype=float))),
    )

    if not acled_country_year.empty:
        acled_min = int(acled_country_year["year"].min())
        acled_max = int(acled_country_year["year"].max())
        panel = panel.assign(acled_period_flag=panel["year"].between(acled_min, acled_max))
    else:
        panel = panel.assign(acled_period_flag=False)

    cols = [
        "iso3",
        "year",
        "outcome_main",
        "treatment_event",
        "acled_event_count",
        "acled_fatalities_sum",
        "refugees_under_mandate",
        "asylum_seekers",
        "idps",
        "total_displaced",
        "acled_period_flag",
        "source_note",
    ]
    return panel[cols].sort_values(["iso3", "year"]).reset_index(drop=True)


def main() -> None:
    args = parse_args()
    built_at = datetime.now(timezone.utc).isoformat()

    acled_events_path = Path(args.acled_events_csv)
    acled_counts_path = Path(args.acled_counts_csv)
    wdi_path = Path(args.wdi_outcome_csv)
    unhcr_path = Path(args.unhcr_mapped_csv)
    for p in [wdi_path, unhcr_path]:
        if not p.exists():
            raise FileNotFoundError(f"Required input not found: {p}")

    if acled_counts_path.exists():
        acled_country_year = load_acled_counts(acled_counts_path)
        acled_source = str(acled_counts_path)
    elif acled_events_path.exists():
        acled_country_year = build_acled_country_year(acled_events_path)
        acled_source = str(acled_events_path)
    else:
        raise FileNotFoundError(
            f"Neither ACLED counts CSV nor event-level CSV exists: {acled_counts_path} / {acled_events_path}"
        )

    acled_country_year_out = Path(args.acled_country_year_csv)
    acled_country_year_out.parent.mkdir(parents=True, exist_ok=True)
    acled_country_year.to_csv(acled_country_year_out, index=False)

    panel = build_panel(
        unhcr_mapped_csv=unhcr_path,
        wdi_outcome_csv=wdi_path,
        acled_country_year=acled_country_year,
    )
    panel_out = Path(args.panel_output_csv)
    panel_out.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(panel_out, index=False)

    metadata = {
        "built_at_utc": built_at,
        "inputs": {
            "acled_source": acled_source,
            "acled_events_csv": str(acled_events_path),
            "acled_counts_csv": str(acled_counts_path),
            "wdi_outcome_csv": str(wdi_path),
            "unhcr_mapped_csv": str(unhcr_path),
        },
        "outputs": {
            "acled_country_year_csv": str(acled_country_year_out),
            "panel_output_csv": str(panel_out),
        },
        "rows_acled_country_year": int(len(acled_country_year)),
        "rows_panel": int(len(panel)),
        "countries_panel": int(panel["iso3"].nunique()) if not panel.empty else 0,
        "year_min_panel": int(panel["year"].min()) if not panel.empty else None,
        "year_max_panel": int(panel["year"].max()) if not panel.empty else None,
        "missing_outcome_main_rows": int(panel["outcome_main"].isna().sum()) if not panel.empty else 0,
    }
    metadata_path = Path(args.metadata_json)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Rows ACLED country-year: {len(acled_country_year)}")
    print(f"Rows panel: {len(panel)}")
    print(f"ACLED country-year CSV: {acled_country_year_out}")
    print(f"Panel CSV: {panel_out}")
    print(f"Metadata: {metadata_path}")


if __name__ == "__main__":
    main()
