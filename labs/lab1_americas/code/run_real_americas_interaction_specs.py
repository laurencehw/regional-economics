"""Run institution-interaction SAR specs for real-Americas Lab 1 data.

This script extends the baseline robustness bundle by introducing interaction
terms between border-governance quality and core macro controls.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run real-Americas Lab 1 interaction specs")
    parser.add_argument(
        "--panel",
        default="../data/real_americas_lpi_blend/panel_mapped.csv",
        help="Path to mapped panel file",
    )
    parser.add_argument(
        "--trade",
        default="../data/real_americas_lpi_blend/trade_mapped.csv",
        help="Path to mapped trade file",
    )
    parser.add_argument(
        "--sar-script",
        default="lab1_americas_sar_scaffold.py",
        help="Path to SAR scaffold script (relative to this script directory by default)",
    )
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument(
        "--output-dir",
        default="../output/real_americas_2024_lpi_blend/interaction_specs",
        help="Output directory for interaction-spec results",
    )
    return parser.parse_args()


def ensure_path(base: Path, maybe_relative: str, allow_parent_exists: bool = False) -> Path:
    p = Path(maybe_relative)
    if p.is_absolute():
        return p

    cwd_candidate = (Path.cwd() / p)
    if cwd_candidate.exists():
        return cwd_candidate.resolve()
    if allow_parent_exists and cwd_candidate.parent.exists():
        return cwd_candidate.resolve()

    return (base / p).resolve()


def run_command(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=True)


def zscore(s: pd.Series) -> pd.Series:
    std = float(s.std(ddof=0))
    if not np.isfinite(std) or std <= 0:
        return pd.Series(np.zeros(len(s), dtype=float), index=s.index)
    return (s - float(s.mean())) / std


def prepare_panel(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy(deep=True)

    # Fill missing border friction by year, then convert to quality index.
    out = out.assign(
        border_delay_index_filled=out.groupby("year")["border_delay_index"].transform(
            lambda s: s.fillna(s.mean())
        )
    )
    out = out.assign(border_quality_index=1.0 - out["border_delay_index_filled"])

    # Standardized controls reduce scale issues in interaction terms.
    out = out.assign(
        log_gdp_pc_z=out.groupby("year")["log_gdp_pc"].transform(zscore),
        manufacturing_share_z=out.groupby("year")["manufacturing_share"].transform(zscore),
        border_quality_index_z=out.groupby("year")["border_quality_index"].transform(zscore),
    )
    out = out.assign(
        quality_x_log_gdp=out["border_quality_index_z"] * out["log_gdp_pc_z"],
        quality_x_manufacturing=out["border_quality_index_z"] * out["manufacturing_share_z"],
    )
    return out


def compute_coverage(panel: pd.DataFrame, year: int) -> Dict[str, int]:
    y = panel.loc[panel["year"] == year].copy()
    return {
        "year": int(year),
        "rows_year": int(len(y)),
        "regions_year": int(y["region"].nunique()),
        "nonmissing_gdp_growth": int(y["gdp_growth"].notna().sum()),
        "nonmissing_log_gdp_pc": int(y["log_gdp_pc"].notna().sum()),
        "nonmissing_manufacturing_share": int(y["manufacturing_share"].notna().sum()),
        "nonmissing_border_quality_index": int(y["border_quality_index"].notna().sum()),
        "nonmissing_quality_x_log_gdp": int(y["quality_x_log_gdp"].notna().sum()),
        "nonmissing_quality_x_manufacturing": int(y["quality_x_manufacturing"].notna().sum()),
    }


def extract_beta(summary: Dict[str, object], target_name: str) -> float | None:
    beta_names = summary.get("beta_names")
    betas = summary.get("betas")
    if not isinstance(beta_names, list) or not isinstance(betas, list):
        return None
    if target_name not in beta_names:
        return None
    idx = beta_names.index(target_name)
    if idx >= len(betas):
        return None
    try:
        return float(betas[idx])
    except Exception:
        return None


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
                "beta_quality_x_log_gdp",
                "beta_quality_x_manufacturing",
                "x_cols",
                "notes",
                "output_subdir",
            ]
        ]
    df.to_csv(output_csv, index=False)

    lines = [
        "# Real-Americas Lab 1 Institution-Interaction Spec Comparison",
        "",
        "| Spec | Status | n_obs | Method | rho | beta(q x log_gdp) | beta(q x manuf) | X cols | Notes |",
        "|---|---|---:|---|---:|---:|---:|---|---|",
    ]

    if df.empty:
        lines.append("| (none) | skipped | 0 | - | - | - | - | - | No records |")
    else:
        for _, r in df.iterrows():
            rho = r["rho"]
            b1 = r["beta_quality_x_log_gdp"]
            b2 = r["beta_quality_x_manufacturing"]
            rho_s = f"{rho:.6f}" if pd.notna(rho) else ""
            b1_s = f"{b1:.6f}" if pd.notna(b1) else ""
            b2_s = f"{b2:.6f}" if pd.notna(b2) else ""
            lines.append(
                f"| {r['spec_id']} | {r['status']} | {int(r['n_obs']) if pd.notna(r['n_obs']) else 0} | "
                f"{r['method'] or ''} | {rho_s} | {b1_s} | {b2_s} | {r['x_cols']} | {r['notes'] or ''} |"
            )

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    panel_path = ensure_path(script_dir, args.panel)
    trade_path = ensure_path(script_dir, args.trade)
    sar_script = ensure_path(script_dir, args.sar_script)
    output_dir = ensure_path(script_dir, args.output_dir, allow_parent_exists=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(panel_path)
    panel = prepare_panel(panel)

    coverage = compute_coverage(panel=panel, year=args.year)
    (output_dir / "input_coverage.json").write_text(json.dumps(coverage, indent=2), encoding="utf-8")

    specs = [
        {
            "spec_id": "quality_levels",
            "x_cols": ["log_gdp_pc", "manufacturing_share", "border_quality_index"],
            "notes": "Adds filled border-quality level (1 - friction).",
        },
        {
            "spec_id": "quality_x_log_gdp",
            "x_cols": ["log_gdp_pc", "manufacturing_share", "border_quality_index", "quality_x_log_gdp"],
            "notes": "Tests whether GDP-level effect varies by border quality.",
        },
        {
            "spec_id": "quality_x_manufacturing",
            "x_cols": [
                "log_gdp_pc",
                "manufacturing_share",
                "border_quality_index",
                "quality_x_manufacturing",
            ],
            "notes": "Tests whether manufacturing share effect varies by border quality.",
        },
        {
            "spec_id": "quality_full_interactions",
            "x_cols": [
                "log_gdp_pc",
                "manufacturing_share",
                "border_quality_index",
                "quality_x_log_gdp",
                "quality_x_manufacturing",
            ],
            "notes": "Joint interaction model for conditional spillovers narrative.",
        },
        {
            "spec_id": "quality_macro_interaction",
            "x_cols": ["log_gdp_pc", "border_quality_index", "quality_x_log_gdp"],
            "notes": "Macro-only interaction spec with broader sample requirement.",
        },
    ]

    records: List[Dict[str, object]] = []
    tmp_dir = output_dir / "_tmp_panels"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        spec_id = spec["spec_id"]
        x_cols = spec["x_cols"]

        required = ["region", "year", "gdp_growth", *x_cols]
        year_slice = panel.loc[panel["year"] == args.year, required].dropna().copy()
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
                    "beta_quality_x_log_gdp": None,
                    "beta_quality_x_manufacturing": None,
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
                    "beta_quality_x_log_gdp": extract_beta(summary, "quality_x_log_gdp"),
                    "beta_quality_x_manufacturing": extract_beta(summary, "quality_x_manufacturing"),
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
                    "beta_quality_x_log_gdp": None,
                    "beta_quality_x_manufacturing": None,
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

    print(f"Wrote spec results: {output_dir / 'spec_results.csv'}")
    print(f"Wrote markdown summary: {output_dir / 'spec_results.md'}")
    print(f"Wrote input coverage: {output_dir / 'input_coverage.json'}")


if __name__ == "__main__":
    main()
