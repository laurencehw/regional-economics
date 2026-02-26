"""Run reproducible robustness specs for the real-Europe Lab 4 RDD dataset.

This script orchestrates multiple Sharp RDD runs using
`lab4_europe_rdd_scaffold.py`, varying bandwidth, kernel, and
cross-section year, then writes a compact comparison table.
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
    parser = argparse.ArgumentParser(description="Run real-Europe Lab 4 RDD robustness specs")
    parser.add_argument(
        "--panel",
        default="../data/real_europe/panel_mapped.csv",
        help="Path to mapped panel file",
    )
    parser.add_argument(
        "--scaffold-script",
        default="lab4_europe_rdd_scaffold.py",
        help="Path to RDD scaffold script",
    )
    parser.add_argument(
        "--output-dir",
        default="../output/real_europe/specs",
        help="Output directory for robustness results",
    )
    return parser.parse_args()


def ensure_path(base: Path, maybe_relative: str, allow_parent_exists: bool = False) -> Path:
    p = Path(maybe_relative)
    if p.is_absolute():
        return p

    cwd_candidate = Path.cwd() / p
    if cwd_candidate.exists():
        return cwd_candidate.resolve()
    if allow_parent_exists and cwd_candidate.parent.exists():
        return cwd_candidate.resolve()

    return (base / p).resolve()


def compute_coverage(panel: pd.DataFrame) -> Dict[str, object]:
    """Compute coverage diagnostics across the entire panel."""
    treated_mask = panel["treated"] == 1
    return {
        "total_rows": int(len(panel)),
        "n_regions": int(panel["nuts2_code"].nunique()),
        "year_range": [int(panel["year"].min()), int(panel["year"].max())],
        "n_years": int(panel["year"].nunique()),
        "treated_regions": int(panel.loc[treated_mask, "nuts2_code"].nunique()),
        "control_regions": int(panel.loc[~treated_mask, "nuts2_code"].nunique()),
        "missing_gdp_growth_share": float(panel["gdp_growth"].isna().mean()),
        "missing_forcing_var_share": float(panel["forcing_var"].isna().mean()),
    }


def run_command(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=True)


def write_summary_table(records: List[Dict[str, object]], output_csv: Path, output_md: Path) -> None:
    df = pd.DataFrame(records)
    col_order = [
        "spec_id", "status", "year", "n_obs", "n_effective",
        "tau", "se_tau", "p_value", "bandwidth", "kernel", "notes",
        "output_subdir",
    ]
    if not df.empty:
        df = df[[c for c in col_order if c in df.columns]]
    df.to_csv(output_csv, index=False)

    lines = [
        "# Real-Europe Lab 4 RDD Spec Comparison",
        "",
        "| Spec | Status | Year | n_obs | n_eff | tau | se | p-value | BW | Kernel | Notes |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]

    if df.empty:
        lines.append("| (none) | skipped | - | 0 | 0 | - | - | - | - | - | No records |")
    else:
        for _, r in df.iterrows():
            tau_s = f"{r['tau']:.4f}" if pd.notna(r.get("tau")) else ""
            se_s = f"{r['se_tau']:.4f}" if pd.notna(r.get("se_tau")) else ""
            pv_s = f"{r['p_value']:.4f}" if pd.notna(r.get("p_value")) else ""
            bw_s = f"{r['bandwidth']:.1f}" if pd.notna(r.get("bandwidth")) else ""
            neff_s = f"{r['n_effective']:.1f}" if pd.notna(r.get("n_effective")) else ""
            lines.append(
                f"| {r['spec_id']} | {r['status']} | {int(r['year'])} | "
                f"{int(r['n_obs']) if pd.notna(r.get('n_obs')) else 0} | "
                f"{neff_s} | {tau_s} | {se_s} | {pv_s} | {bw_s} | "
                f"{r.get('kernel', '')} | {r.get('notes', '') or ''} |"
            )

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    panel_path = ensure_path(script_dir, args.panel)
    scaffold_script = ensure_path(script_dir, args.scaffold_script)
    output_dir = ensure_path(script_dir, args.output_dir, allow_parent_exists=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(panel_path)

    coverage = compute_coverage(panel)
    (output_dir / "input_coverage.json").write_text(
        json.dumps(coverage, indent=2), encoding="utf-8"
    )

    specs = [
        {
            "spec_id": "baseline_2022",
            "year": 2022,
            "bandwidth_frac": 0.50,
            "kernel": "triangular",
            "notes": "Primary specification.",
        },
        {
            "spec_id": "narrow_bw_2022",
            "year": 2022,
            "bandwidth_frac": 0.25,
            "kernel": "triangular",
            "notes": "Tighter bandwidth — less bias, more variance.",
        },
        {
            "spec_id": "wide_bw_2022",
            "year": 2022,
            "bandwidth_frac": 0.75,
            "kernel": "triangular",
            "notes": "Wider bandwidth — more precision, more bias.",
        },
        {
            "spec_id": "uniform_2022",
            "year": 2022,
            "bandwidth_frac": 0.50,
            "kernel": "uniform",
            "notes": "Kernel sensitivity check.",
        },
        {
            "spec_id": "baseline_2019",
            "year": 2019,
            "bandwidth_frac": 0.50,
            "kernel": "triangular",
            "notes": "Pre-COVID cross-section.",
        },
        {
            "spec_id": "baseline_2020",
            "year": 2020,
            "bandwidth_frac": 0.50,
            "kernel": "triangular",
            "notes": "COVID year — structural break check.",
        },
    ]

    records: List[Dict[str, object]] = []

    for spec in specs:
        spec_id = spec["spec_id"]
        out_subdir = output_dir / spec_id
        out_subdir.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            str(scaffold_script),
            "--panel", str(panel_path),
            "--year", str(spec["year"]),
            "--bandwidth-frac", str(spec["bandwidth_frac"]),
            "--kernel", spec["kernel"],
            "--output-dir", str(out_subdir),
        ]

        try:
            run_command(cmd=cmd, cwd=script_dir)
            summary_path = out_subdir / "model_summary.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "ok",
                    "year": spec["year"],
                    "n_obs": summary.get("n_obs"),
                    "n_effective": summary.get("n_effective"),
                    "tau": summary.get("tau"),
                    "se_tau": summary.get("se_tau"),
                    "p_value": summary.get("p_value"),
                    "bandwidth": summary.get("bandwidth"),
                    "kernel": spec["kernel"],
                    "notes": spec["notes"],
                    "output_subdir": str(out_subdir),
                }
            )
        except subprocess.CalledProcessError as exc:
            stderr_tail = (exc.stderr or "")[-300:]
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "error",
                    "year": spec["year"],
                    "n_obs": None,
                    "n_effective": None,
                    "tau": None,
                    "se_tau": None,
                    "p_value": None,
                    "bandwidth": None,
                    "kernel": spec["kernel"],
                    "notes": f"Failed: {stderr_tail}",
                    "output_subdir": str(out_subdir),
                }
            )

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
