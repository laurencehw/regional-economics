"""Run reproducible robustness specs for the real-Americas Lab 1 dataset.

This script orchestrates multiple SAR runs using `lab1_americas_sar_scaffold.py`,
collects model summaries, and writes a compact comparison table.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run real-Americas Lab 1 robustness specs")
    parser.add_argument(
        "--panel",
        default="../data/real_americas/panel_mapped.csv",
        help="Path to mapped panel file",
    )
    parser.add_argument(
        "--trade",
        default="../data/real_americas/trade_mapped.csv",
        help="Path to mapped trade file",
    )
    parser.add_argument(
        "--sar-script",
        default="lab1_americas_sar_scaffold.py",
        help="Path to SAR scaffold script (relative to this script's directory by default)",
    )
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument(
        "--output-dir",
        default="../output/real_americas_2024/specs",
        help="Output directory for robustness results",
    )
    return parser.parse_args()


def ensure_path(base: Path, maybe_relative: str) -> Path:
    p = Path(maybe_relative)
    return p if p.is_absolute() else (base / p).resolve()


def compute_coverage(panel: pd.DataFrame, year: int) -> Dict[str, int]:
    y = panel.loc[panel["year"] == year].copy()
    return {
        "year": year,
        "rows_year": int(len(y)),
        "regions_year": int(y["region"].nunique()),
        "nonmissing_gdp_growth": int(y["gdp_growth"].notna().sum()),
        "nonmissing_log_gdp_pc": int(y["log_gdp_pc"].notna().sum()),
        "nonmissing_manufacturing_share": int(y["manufacturing_share"].notna().sum()),
        "nonmissing_border_delay_index": int(y["border_delay_index"].notna().sum()),
    }


def run_command(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=True)


def write_summary_table(records: List[Dict[str, object]], output_csv: Path, output_md: Path) -> None:
    df = pd.DataFrame(records)
    if not df.empty:
        df = df[
            [
                "spec_id",
                "status",
                "n_obs",
                "method",
                "rho",
                "x_cols",
                "notes",
                "output_subdir",
            ]
        ]
    df.to_csv(output_csv, index=False)

    lines = [
        "# Real-Americas Lab 1 Spec Comparison",
        "",
        "| Spec | Status | n_obs | Method | rho | X cols | Notes |",
        "|---|---|---:|---|---:|---|---|",
    ]

    if df.empty:
        lines.append("| (none) | skipped | 0 | - | - | - | No records |")
    else:
        for _, r in df.iterrows():
            rho = r["rho"]
            rho_str = f"{rho:.6f}" if pd.notna(rho) else ""
            lines.append(
                f"| {r['spec_id']} | {r['status']} | {int(r['n_obs']) if pd.notna(r['n_obs']) else 0} | "
                f"{r['method'] or ''} | {rho_str} | {r['x_cols']} | {r['notes'] or ''} |"
            )

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    panel_path = ensure_path(script_dir, args.panel)
    trade_path = ensure_path(script_dir, args.trade)
    sar_script = ensure_path(script_dir, args.sar_script)
    output_dir = ensure_path(script_dir, args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(panel_path)
    panel = panel.copy()

    # Mean-imputed border proxy by year for all regions (documented robustness only).
    panel = panel.assign(
        border_delay_index_filled=panel.groupby("year")["border_delay_index"].transform(
            lambda s: s.fillna(s.mean())
        )
    )

    coverage = compute_coverage(panel=panel, year=args.year)
    (output_dir / "input_coverage.json").write_text(json.dumps(coverage, indent=2), encoding="utf-8")

    specs = [
        {
            "spec_id": "baseline_all",
            "x_cols": ["log_gdp_pc", "manufacturing_share"],
            "region_filter": None,
            "notes": "Primary all-Americas baseline.",
        },
        {
            "spec_id": "macro_only_all",
            "x_cols": ["log_gdp_pc"],
            "region_filter": None,
            "notes": "Less restrictive sample requirement.",
        },
        {
            "spec_id": "border_imputed_all",
            "x_cols": ["log_gdp_pc", "manufacturing_share", "border_delay_index_filled"],
            "region_filter": None,
            "notes": "Border proxy mean-imputed outside USA/CAN/MEX (robustness only).",
        },
        {
            "spec_id": "usmca_border_raw",
            "x_cols": ["log_gdp_pc", "manufacturing_share", "border_delay_index"],
            "region_filter": ["USA", "CAN", "MEX"],
            "notes": "Tri-country subset; often too few observations.",
        },
    ]

    records: List[Dict[str, object]] = []
    tmp_dir = output_dir / "_tmp_panels"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        spec_id = spec["spec_id"]
        x_cols = spec["x_cols"]
        region_filter = spec["region_filter"]

        spec_panel = panel.copy()
        if region_filter:
            spec_panel = spec_panel.loc[spec_panel["region"].isin(region_filter)].copy()

        required = ["region", "year", "gdp_growth", *x_cols]
        year_slice = spec_panel.loc[spec_panel["year"] == args.year, required].dropna().copy()
        year_slice = year_slice.drop_duplicates(subset=["region"]).sort_values("region")
        n_obs = int(year_slice.shape[0])

        if n_obs < 5:
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "skipped",
                    "n_obs": n_obs,
                    "method": "",
                    "rho": None,
                    "x_cols": ",".join(x_cols),
                    "notes": f"Insufficient observations (n={n_obs})",
                    "output_subdir": "",
                }
            )
            continue

        panel_tmp = tmp_dir / f"{spec_id}_panel.csv"
        year_slice.to_csv(panel_tmp, index=False)

        out_subdir = output_dir / spec_id
        out_subdir.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            str(sar_script),
            "--panel",
            str(panel_tmp),
            "--trade",
            str(trade_path),
            "--year",
            str(args.year),
            "--y-col",
            "gdp_growth",
            "--x-cols",
            ",".join(x_cols),
            "--output-dir",
            str(out_subdir),
        ]

        try:
            run_command(cmd=cmd, cwd=script_dir)
            summary_path = out_subdir / "model_summary.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "ok",
                    "n_obs": summary.get("n_obs", n_obs),
                    "method": summary.get("method", ""),
                    "rho": summary.get("rho"),
                    "x_cols": ",".join(x_cols),
                    "notes": spec["notes"],
                    "output_subdir": str(out_subdir),
                }
            )
        except subprocess.CalledProcessError as exc:
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "error",
                    "n_obs": n_obs,
                    "method": "",
                    "rho": None,
                    "x_cols": ",".join(x_cols),
                    "notes": f"Command failed: {exc.stderr[-300:]}",
                    "output_subdir": str(out_subdir),
                }
            )

    write_summary_table(
        records=records,
        output_csv=output_dir / "spec_results.csv",
        output_md=output_dir / "spec_results.md",
    )

    print(f"Wrote spec results: {(output_dir / 'spec_results.csv').resolve()}")
    print(f"Wrote markdown summary: {(output_dir / 'spec_results.md').resolve()}")
    print(f"Wrote input coverage: {(output_dir / 'input_coverage.json').resolve()}")


if __name__ == "__main__":
    main()
