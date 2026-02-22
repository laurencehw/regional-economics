import subprocess
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cmd(args, cwd=REPO_ROOT):
    completed = subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=True,
    )
    return completed


def test_run_interaction_specs_smoke(tmp_path):
    mapped_dir = tmp_path / "mapped"
    mapped_dir.mkdir(parents=True, exist_ok=True)

    map_args = [
        sys.executable,
        "labs/lab1_americas/code/prepare_lab1_inputs.py",
        "--wdi-input",
        "labs/lab1_americas/data/raw_templates/wdi_bulk_example.csv",
        "--comtrade-input",
        "labs/lab1_americas/data/raw_templates/comtrade_example.csv",
        "--bts-input",
        "labs/lab1_americas/data/raw_templates/bts_border_delay_example.csv",
        "--mappings",
        "labs/lab1_americas/data/source_mappings.json",
        "--output-dir",
        str(mapped_dir),
        "--year",
        "2024",
    ]
    run_cmd(map_args)

    out_dir = tmp_path / "interaction_specs"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_args = [
        sys.executable,
        "labs/lab1_americas/code/run_real_americas_interaction_specs.py",
        "--panel",
        str(mapped_dir / "panel_mapped.csv"),
        "--trade",
        str(mapped_dir / "trade_mapped.csv"),
        "--output-dir",
        str(out_dir),
        "--year",
        "2024",
    ]
    run_cmd(run_args)

    summary_csv = out_dir / "spec_results.csv"
    coverage_json = out_dir / "input_coverage.json"
    assert summary_csv.exists(), "spec_results.csv missing"
    assert coverage_json.exists(), "input_coverage.json missing"

    df = pd.read_csv(summary_csv)
    assert not df.empty
    assert "quality_full_interactions" in set(df["spec_id"])
    ok_rows = df.loc[df["status"] == "ok"]
    assert len(ok_rows) >= 1
