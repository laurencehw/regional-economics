"""Run reproducible robustness specs for the South Asia IT concentration analysis.

This script orchestrates multiple concentration-analysis runs using
`lab3_concentration_scaffold.py`, collects model summaries, and writes
a compact comparison table of HHI, Gini, and top-LQ results across specs.

Smoke-test mode generates a synthetic 12-state panel with known concentration
patterns, mirroring the real Indian IT-sector geography.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run South-Asia Lab 3 concentration robustness specs"
    )
    parser.add_argument(
        "--panel",
        default="../data/panel_mapped.csv",
        help="Path to mapped panel file (panel_mapped.csv format)",
    )
    parser.add_argument(
        "--scaffold-script",
        default="lab3_concentration_scaffold.py",
        help="Path to concentration scaffold script",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2018,
        help="Cross-section year for concentration analysis",
    )
    parser.add_argument(
        "--output-dir",
        default="../output/south_asia_specs",
        help="Output directory for robustness results",
    )
    parser.add_argument(
        "--run-smoke-test",
        action="store_true",
        help="Run with synthetic data instead of real panel",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def ensure_path(base: Path, maybe_relative: str, allow_parent_exists: bool = False) -> Path:
    """Resolve a path that may be relative to *base* or to cwd."""
    p = Path(maybe_relative)
    if p.is_absolute():
        return p

    cwd_candidate = Path.cwd() / p
    if cwd_candidate.exists():
        return cwd_candidate.resolve()
    if allow_parent_exists and cwd_candidate.parent.exists():
        return cwd_candidate.resolve()

    return (base / p).resolve()


# ---------------------------------------------------------------------------
# Synthetic data for smoke testing
# ---------------------------------------------------------------------------

def synthetic_panel(seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic 12-state IT-sector panel for smoke testing.

    Includes Andhra Pradesh (needed by the southern_states spec) and spans
    2012-2018 so that the early_period spec can select a distinct year.
    """
    rng = np.random.default_rng(seed)

    states = [
        "Karnataka", "Telangana", "Maharashtra", "Tamil Nadu",
        "Delhi NCR", "Uttar Pradesh", "West Bengal", "Kerala",
        "Rajasthan", "Gujarat", "Madhya Pradesh", "Andhra Pradesh",
    ]

    # IT intensity varies dramatically by state (mimicking real concentration)
    it_intensity = np.array([
        0.20, 0.17, 0.05, 0.04, 0.06, 0.004, 0.013, 0.03,
        0.005, 0.015, 0.003, 0.025,
    ])
    total_gdp_base = np.array([
        5000, 4000, 18000, 10000, 6000, 12000, 7000, 4500,
        6500, 9000, 5500, 5000,
    ])

    rows: List[Dict] = []
    for yr in range(2012, 2019):
        growth = 1.0 + 0.08 * (yr - 2012) + rng.normal(0, 0.01, len(states))
        it_growth = 1.0 + 0.12 * (yr - 2012) + rng.normal(0, 0.02, len(states))
        gdp = total_gdp_base * growth
        it_va = gdp * it_intensity * it_growth

        for i, state in enumerate(states):
            rows.append({
                "region": state,
                "year": yr,
                "it_va": float(it_va[i]),
                "total_gdp": float(gdp[i]),
                "it_share": float(it_va[i] / gdp[i]),
            })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Coverage diagnostics
# ---------------------------------------------------------------------------

def compute_coverage(panel: pd.DataFrame, year: int) -> Dict[str, object]:
    """Compute coverage diagnostics for the input panel at a given year."""
    y = panel.loc[panel["year"] == year].copy()
    return {
        "year": year,
        "rows_year": int(len(y)),
        "regions_year": int(y["region"].nunique()),
        "nonmissing_it_va": int(y["it_va"].notna().sum()),
        "nonmissing_total_gdp": int(y["total_gdp"].notna().sum()),
        "nonmissing_it_share": (
            int(y["it_share"].notna().sum()) if "it_share" in y.columns else 0
        ),
    }


# ---------------------------------------------------------------------------
# Subprocess runner
# ---------------------------------------------------------------------------

def run_command(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    """Execute a subprocess command and return the result."""
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=True)


# ---------------------------------------------------------------------------
# Spec definitions
# ---------------------------------------------------------------------------

TIER1_HUBS = ["Karnataka", "Telangana", "Maharashtra", "Tamil Nadu"]
SOUTHERN_STATES = ["Karnataka", "Telangana", "Tamil Nadu", "Kerala", "Andhra Pradesh"]


def build_specs(year: int, panel: pd.DataFrame) -> List[Dict[str, object]]:
    """Define the five robustness specifications for concentration analysis.

    Specs:
    1. baseline_all       -- All states, latest year
    2. tier1_hubs         -- Only top-4 IT states
    3. exclude_karnataka  -- All states except Karnataka (HHI sensitivity)
    4. southern_states    -- Southern IT corridor
    5. early_period       -- All states, earlier year from panel
    """
    all_years = sorted(int(y) for y in panel["year"].dropna().unique())
    # Pick midpoint year for the early-period spec
    midpoint = all_years[len(all_years) // 2] if len(all_years) > 1 else all_years[0]
    # Ensure early_period year is strictly before the main year when possible
    if midpoint >= year and len(all_years) > 1:
        candidates = [y for y in all_years if y < year]
        midpoint = candidates[len(candidates) // 2] if candidates else all_years[0]

    all_regions = sorted(panel["region"].unique().tolist())
    exclude_karnataka = [r for r in all_regions if r != "Karnataka"]

    return [
        {
            "spec_id": "baseline_all",
            "region_filter": None,
            "region_exclude": None,
            "year_override": None,
            "notes": "All states, latest year — primary baseline.",
        },
        {
            "spec_id": "tier1_hubs",
            "region_filter": TIER1_HUBS,
            "region_exclude": None,
            "year_override": None,
            "notes": "Top-4 IT states only (Karnataka, Telangana, Maharashtra, Tamil Nadu).",
        },
        {
            "spec_id": "exclude_karnataka",
            "region_filter": exclude_karnataka,
            "region_exclude": None,
            "year_override": None,
            "notes": "All states except Karnataka — HHI sensitivity check.",
        },
        {
            "spec_id": "southern_states",
            "region_filter": SOUTHERN_STATES,
            "region_exclude": None,
            "year_override": None,
            "notes": "Southern IT corridor states.",
        },
        {
            "spec_id": "early_period",
            "region_filter": None,
            "region_exclude": None,
            "year_override": int(midpoint),
            "notes": f"All states, earlier period (year={int(midpoint)}).",
        },
    ]


# ---------------------------------------------------------------------------
# Output table
# ---------------------------------------------------------------------------

def write_summary_table(
    records: List[Dict[str, object]], output_csv: Path, output_md: Path
) -> None:
    """Write spec comparison results to CSV and a formatted markdown table."""
    df = pd.DataFrame(records)
    col_order = [
        "spec_id", "status", "year", "n_regions", "hhi", "gini",
        "top3_lq_regions", "notes", "output_subdir",
    ]
    if not df.empty:
        for c in col_order:
            if c not in df.columns:
                df[c] = ""
        df = df[col_order]
    df.to_csv(output_csv, index=False)

    lines = [
        "# South-Asia Lab 3 Concentration Spec Comparison",
        "",
        "| Spec | Status | Year | Regions | HHI | Gini | Top-3 LQ Regions | Notes |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]

    if df.empty:
        lines.append("| (none) | skipped | - | 0 | - | - | - | No records |")
    else:
        for _, r in df.iterrows():
            hhi_str = f"{r['hhi']:.4f}" if pd.notna(r["hhi"]) else ""
            gini_str = f"{r['gini']:.4f}" if pd.notna(r["gini"]) else ""
            n_reg = int(r["n_regions"]) if pd.notna(r["n_regions"]) else 0
            lines.append(
                f"| {r['spec_id']} | {r['status']} | {r['year']} | "
                f"{n_reg} | {hhi_str} | {gini_str} | "
                f"{r['top3_lq_regions']} | {r['notes'] or ''} |"
            )

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    scaffold_script = ensure_path(script_dir, args.scaffold_script)
    output_dir = ensure_path(script_dir, args.output_dir, allow_parent_exists=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load or generate panel data
    if args.run_smoke_test:
        panel = synthetic_panel()
        print("Running in smoke-test mode with synthetic 12-state panel.")
    else:
        panel_path = ensure_path(script_dir, args.panel)
        panel = pd.read_csv(panel_path)

    # Ensure it_share column exists
    if "it_share" not in panel.columns and "it_va" in panel.columns and "total_gdp" in panel.columns:
        panel = panel.assign(
            it_share=np.where(
                panel["total_gdp"] > 0, panel["it_va"] / panel["total_gdp"], 0.0
            )
        )

    # Coverage diagnostics
    coverage = compute_coverage(panel=panel, year=args.year)
    (output_dir / "input_coverage.json").write_text(
        json.dumps(coverage, indent=2), encoding="utf-8"
    )

    specs = build_specs(year=args.year, panel=panel)

    records: List[Dict[str, object]] = []
    tmp_dir = output_dir / "_tmp_panels"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        spec_id = spec["spec_id"]
        region_filter = spec["region_filter"]
        year_override = spec["year_override"]
        effective_year = year_override if year_override is not None else args.year

        # Apply region filter
        spec_panel = panel.copy()
        if region_filter is not None:
            spec_panel = spec_panel.loc[spec_panel["region"].isin(region_filter)].copy()

        # Check we have enough data for the target year
        year_slice = spec_panel.loc[spec_panel["year"] == effective_year].dropna(
            subset=["region", "it_va", "total_gdp"]
        )
        year_slice = year_slice.drop_duplicates(subset=["region"]).sort_values("region")
        n_regions = int(year_slice.shape[0])

        if n_regions < 3:
            records.append({
                "spec_id": spec_id,
                "status": "skipped",
                "year": effective_year,
                "n_regions": n_regions,
                "hhi": None,
                "gini": None,
                "top3_lq_regions": "",
                "notes": f"Insufficient regions (n={n_regions})",
                "output_subdir": "",
            })
            continue

        # Write filtered panel to temp CSV (include all years for time-series HHI)
        panel_tmp = tmp_dir / f"{spec_id}_panel.csv"
        spec_panel.to_csv(panel_tmp, index=False)

        out_subdir = output_dir / spec_id
        out_subdir.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            str(scaffold_script),
            "--panel", str(panel_tmp),
            "--year", str(effective_year),
            "--output-dir", str(out_subdir),
        ]

        try:
            run_command(cmd=cmd, cwd=script_dir)
            summary_path = out_subdir / "model_summary.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))

            top3_lq = summary.get("top_3_regions_by_lq", [])
            top3_str = ", ".join(
                f"{entry['region']} ({entry['lq']:.2f})" for entry in top3_lq
            )

            records.append({
                "spec_id": spec_id,
                "status": "ok",
                "year": effective_year,
                "n_regions": summary.get("n_regions", n_regions),
                "hhi": summary.get("herfindahl_index"),
                "gini": summary.get("gini_coefficient"),
                "top3_lq_regions": top3_str,
                "notes": spec["notes"],
                "output_subdir": str(out_subdir),
            })
        except subprocess.CalledProcessError as exc:
            stderr_tail = (exc.stderr or "")[-300:]
            records.append({
                "spec_id": spec_id,
                "status": "error",
                "year": effective_year,
                "n_regions": n_regions,
                "hhi": None,
                "gini": None,
                "top3_lq_regions": "",
                "notes": f"Command failed: {stderr_tail}",
                "output_subdir": str(out_subdir),
            })

    write_summary_table(
        records=records,
        output_csv=output_dir / "spec_results.csv",
        output_md=output_dir / "spec_results.md",
    )

    print(f"Wrote spec results: {output_dir / 'spec_results.csv'}")
    print(f"Wrote markdown summary: {output_dir / 'spec_results.md'}")
    print(f"Wrote input coverage: {output_dir / 'input_coverage.json'}")


if __name__ == "__main__":
    main()
