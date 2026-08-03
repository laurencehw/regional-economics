"""Run reproducible robustness specs for the real-Asia Lab 2 dataset.

This script orchestrates multiple β-convergence runs using
`lab2_asia_convergence_scaffold.py`, collects model summaries,
and writes a compact comparison table.

Default estimand is share mode (`EXGR_DVA / EXGR`) with year FE.
Pass `--outcome-mode level` for the legacy DVA-level diagnostic.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

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
        default="../output/real_asia/specs_share",
        help="Output directory for robustness results",
    )
    parser.add_argument(
        "--outcome-mode",
        choices=["level", "share"],
        default="share",
        help="level = DVA dollar growth; share = DVA/EXGR percentage-point growth",
    )
    parser.add_argument(
        "--year-fe",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Pass --year-fe to the scaffold (default: on for share mode)",
    )
    parser.add_argument(
        "--leave-one-out",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Add leave-one-economy-out specs",
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


def compute_coverage(panel: pd.DataFrame, outcome_mode: str) -> Dict[str, object]:
    """Compute coverage diagnostics across the entire panel."""
    growth_col = "dva_share_growth" if outcome_mode == "share" else "dva_growth"
    lag_col = "dva_share_lag" if outcome_mode == "share" else "dva_lag"
    coverage: Dict[str, object] = {
        "outcome_mode": outcome_mode,
        "total_rows": int(len(panel)),
        "countries": sorted(panel["country"].unique().tolist()),
        "n_countries": int(panel["country"].nunique()),
        "year_range": [int(panel["year"].min()), int(panel["year"].max())],
        "n_years": int(panel["year"].nunique()),
        "nonmissing_dva_value": int(panel["dva_value"].notna().sum()),
        "nonmissing_fnl_value": int(panel["fnl_value"].notna().sum()),
        "nonmissing_exgr_value": int(panel["exgr_value"].notna().sum())
        if "exgr_value" in panel.columns
        else 0,
        "nonmissing_dva_share": int(panel["dva_share"].notna().sum())
        if "dva_share" in panel.columns
        else 0,
        "nonmissing_growth": int(panel[growth_col].notna().sum())
        if growth_col in panel.columns
        else 0,
        "nonmissing_lag": int(panel[lag_col].notna().sum()) if lag_col in panel.columns else 0,
        "missing_growth_share": float(panel[growth_col].isna().mean())
        if growth_col in panel.columns
        else 1.0,
        "missing_lag_share": float(panel[lag_col].isna().mean())
        if lag_col in panel.columns
        else 1.0,
        "growth_col": growth_col,
        "lag_col": lag_col,
    }
    return coverage


def run_command(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=True)


def build_specs(panel: pd.DataFrame, leave_one_out: bool) -> List[Dict[str, object]]:
    economies = sorted(panel["country"].unique().tolist())
    specs: List[Dict[str, object]] = [
        {
            "spec_id": "full_panel",
            "country_filter": None,
            "notes": "All Asian economies in the mapped panel, full time range.",
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
            "country_filter": [c for c in economies if c != "CHN"],
            "notes": "All except CHN — tests whether China drives the result.",
        },
    ]
    if leave_one_out:
        for eco in economies:
            specs.append(
                {
                    "spec_id": f"loo_{eco.lower()}",
                    "country_filter": [c for c in economies if c != eco],
                    "notes": f"Leave-one-economy-out: drop {eco}.",
                }
            )
    return specs


def write_summary_table(
    records: List[Dict[str, object]],
    output_csv: Path,
    output_md: Path,
    outcome_mode: str,
    year_fe: bool,
) -> None:
    df = pd.DataFrame(records)
    cols = [
        "spec_id",
        "status",
        "outcome_mode",
        "year_fe",
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
    if not df.empty:
        df = df[cols]
    df.to_csv(output_csv, index=False)

    lines = [
        "# Real-Asia Lab 2 Spec Comparison",
        "",
        f"Estimand mode: `{outcome_mode}`"
        + (" with year FE" if year_fe else " without year FE"),
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


def required_cols(outcome_mode: str) -> List[str]:
    if outcome_mode == "share":
        return ["dva_share_growth", "dva_share_lag"]
    return ["dva_growth", "dva_lag"]


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent

    panel_path = ensure_path(script_dir, args.panel)
    scaffold_script = ensure_path(script_dir, args.scaffold_script)
    output_dir = ensure_path(script_dir, args.output_dir, allow_parent_exists=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    panel = pd.read_csv(panel_path)
    needed = required_cols(args.outcome_mode)
    missing_cols = [c for c in needed if c not in panel.columns]
    if missing_cols:
        raise ValueError(
            f"Panel missing columns required for outcome-mode={args.outcome_mode}: {missing_cols}. "
            "Rebuild with prepare_lab2_inputs.py --exgr-input ..."
        )

    coverage = compute_coverage(panel, args.outcome_mode)
    coverage["year_fe"] = bool(args.year_fe)
    (output_dir / "input_coverage.json").write_text(json.dumps(coverage, indent=2), encoding="utf-8")

    specs = build_specs(panel, leave_one_out=bool(args.leave_one_out))
    records: List[Dict[str, object]] = []
    tmp_dir = output_dir / "_tmp_panels"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        spec_id = str(spec["spec_id"])
        country_filter: Optional[List[str]] = spec["country_filter"]  # type: ignore[assignment]

        spec_panel = panel.copy()
        if country_filter:
            spec_panel = spec_panel.loc[spec_panel["country"].isin(country_filter)].copy()

        n_countries = int(spec_panel["country"].nunique())
        usable = spec_panel.dropna(subset=needed)
        n_obs = int(usable.shape[0])

        if n_obs < 3:
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "skipped",
                    "outcome_mode": args.outcome_mode,
                    "year_fe": bool(args.year_fe),
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
            "--outcome-mode",
            args.outcome_mode,
            "--output-dir",
            str(out_subdir),
        ]
        if args.year_fe:
            cmd.append("--year-fe")
        else:
            cmd.append("--no-year-fe")

        try:
            run_command(cmd=cmd, cwd=script_dir)
            summary_path = out_subdir / "model_summary.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            records.append(
                {
                    "spec_id": spec_id,
                    "status": "ok",
                    "outcome_mode": args.outcome_mode,
                    "year_fe": bool(args.year_fe),
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
                    "outcome_mode": args.outcome_mode,
                    "year_fe": bool(args.year_fe),
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
        outcome_mode=args.outcome_mode,
        year_fe=bool(args.year_fe),
    )

    run_meta = {
        "outcome_mode": args.outcome_mode,
        "year_fe": bool(args.year_fe),
        "leave_one_out": bool(args.leave_one_out),
        "panel": str(panel_path),
        "n_specs": len(records),
        "n_ok": sum(1 for r in records if r["status"] == "ok"),
        "n_skipped": sum(1 for r in records if r["status"] == "skipped"),
        "n_error": sum(1 for r in records if r["status"] == "error"),
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    print(f"Wrote spec results: {output_dir / 'spec_results.csv'}")
    print(f"Wrote markdown summary: {output_dir / 'spec_results.md'}")
    print(f"Wrote input coverage: {output_dir / 'input_coverage.json'}")
    print(f"Wrote run metadata: {output_dir / 'run_metadata.json'}")


if __name__ == "__main__":
    main()
