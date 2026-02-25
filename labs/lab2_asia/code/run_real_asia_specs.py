"""Run reproducible robustness specs for the real-Asia Lab 2 dataset.

This script orchestrates multiple β-convergence runs using
`lab2_asia_convergence_scaffold.py`, collects model summaries,
and writes a compact comparison table.
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
    parser = argparse.ArgumentParser(description="Run real-Asia Lab 2 robustness specs")
    parser.add_argument(
        "--panel",
        default="../data/real_asia/panel_mapped.csv",
        help="Path to mapped panel file",
    )
    parser.add_argument(
        "--scaffold-script",
        default="lab2_asia_convergence_scaffold.py",
        help="Path to convergence scaffold script",
    )
    parser.add_argument(
        "--output-dir",
        default="../output/real_asia/specs",
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
    return {
        "total_rows": int(len(panel)),
        "countries": sorted(panel["country"].unique().tolist()),
        "n_countries": int(panel["country"].nunique()),
        "year_range": [int(panel["year"].min()), int(panel["year"].max())],
        "n_years": int(panel["year"].nunique()),
        "nonmissing_dva_value": int(panel["dva_value"].notna().sum()),
        "nonmissing_fnl_value": int(panel["fnl_value"].notna().sum()),
        "nonmissing_dva_growth": int(panel["dva_growth"].notna().sum()),
        "nonmissing_dva_lag": int(panel["dva_lag"].notna().sum()),
        "missing_dva_growth_share": float(panel["dva_growth"].isna().mean()),
        "missing_dva_lag_share": float(panel["dva_lag"].isna().mean()),
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
                "n_countries",
                "beta",
                "se_beta",
                "p_value",
                "convergence",
                "half_life",
                "notes",
                "output_subdir",
            ]
        ]
    df.to_csv(output_csv, index=False)

    lines = [
        "# Real-Asia Lab 2 Spec Comparison",
        "",
        "| Spec | Status | n_obs | Countries | beta | se | p-value | Converge? | Half-life | Notes |",
        "|---|---|---:|---:|---:|---:|---:|---|---:|---|",
    ]

    if df.empty:
        lines.append("| (none) | skipped | 0 | 0 | - | - | - | - | - | No records |")
    else:
        for _, r in df.iterrows():
            beta_str = f"{r['beta']:.6f}" if pd.notna(r["beta"]) else ""
            se_str = f"{r['se_beta']:.6f}" if pd.notna(r["se_beta"]) else ""
            pv_str = f"{r['p_value']:.4f}" if pd.notna(r["p_value"]) else ""
            hl_str = f"{r['half_life']:.1f}" if pd.notna(r["half_life"]) else ""
            lines.append(
                f"| {r['spec_id']} | {r['status']} | {int(r['n_obs']) if pd.notna(r['n_obs']) else 0} | "
                f"{int(r['n_countries']) if pd.notna(r['n_countries']) else 0} | "
                f"{beta_str} | {se_str} | {pv_str} | {r['convergence']} | {hl_str} | {r['notes'] or ''} |"
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
    (output_dir / "input_coverage.json").write_text(json.dumps(coverage, indent=2), encoding="utf-8")

    specs = [
        {
            "spec_id": "full_panel",
            "country_filter": None,
            "notes": "All 10 Asian economies, full time range.",
        },
        {
            "spec_id": "asean_6",
            "country_filter": ["IDN", "MYS", "PHL", "SGP", "THA", "VNM"],
            "notes": "ASEAN subset — flying-geese within Southeast Asia.",
        },
        {
            "spec_id": "east_asia_core",
            "country_filter": ["CHN", "JPN", "KOR"],
            "notes": "Northeast Asia core — highest-DVA economies.",
        },
        {
            "spec_id": "ex_china",
            "country_filter": [
                "IDN", "IND", "JPN", "KOR", "MYS", "PHL", "SGP", "THA", "VNM",
            ],
            "notes": "All except CHN — tests whether China drives the result.",
        },
    ]

    records: List[Dict[str, object]] = []
    tmp_dir = output_dir / "_tmp_panels"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        spec_id = spec["spec_id"]
        country_filter = spec["country_filter"]

        spec_panel = panel.copy()
        if country_filter:
            spec_panel = spec_panel.loc[spec_panel["country"].isin(country_filter)].copy()

        n_countries = int(spec_panel["country"].nunique())
        usable = spec_panel.dropna(subset=["dva_growth", "dva_lag"])
        n_obs = int(usable.shape[0])

        if n_obs < 3:
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "skipped",
                    "n_obs": n_obs,
                    "n_countries": n_countries,
                    "beta": None,
                    "se_beta": None,
                    "p_value": None,
                    "convergence": "",
                    "half_life": None,
                    "notes": f"Insufficient observations (n={n_obs})",
                    "output_subdir": "",
                }
            )
            continue

        panel_tmp = tmp_dir / f"{spec_id}_panel.csv"
        spec_panel.to_csv(panel_tmp, index=False)

        out_subdir = output_dir / spec_id
        out_subdir.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            str(scaffold_script),
            "--panel",
            str(panel_tmp),
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
                    "n_countries": summary.get("n_countries", n_countries),
                    "beta": summary.get("beta"),
                    "se_beta": summary.get("se_beta"),
                    "p_value": summary.get("p_value"),
                    "convergence": "YES" if summary.get("convergence_detected") else "NO",
                    "half_life": summary.get("half_life_years"),
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
                    "n_countries": n_countries,
                    "beta": None,
                    "se_beta": None,
                    "p_value": None,
                    "convergence": "",
                    "half_life": None,
                    "notes": f"Command failed: {exc.stderr[-300:]}",
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
