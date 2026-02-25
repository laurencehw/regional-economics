import json
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


def test_compare_tiva_measures_smoke(tmp_path):
    out_csv = str(tmp_path / "comparison.csv")
    out_json = str(tmp_path / "summary.json")

    args = [
        sys.executable,
        "scripts/compare_lab2_tiva_measures.py",
        "--base-csv",
        "labs/lab2_asia/data/raw_templates/tiva_base_example.csv",
        "--alt-csv",
        "labs/lab2_asia/data/raw_templates/tiva_alt_example.csv",
        "--output-csv",
        out_csv,
        "--summary-json",
        out_json,
    ]
    run_cmd(args)

    out_path = Path(out_csv)
    assert out_path.exists(), "comparison CSV missing"
    df = pd.read_csv(out_path)
    assert not df.empty, "comparison CSV is empty"

    summary_path = Path(out_json)
    assert summary_path.exists(), "summary JSON missing"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["rows_overlap"] > 0
    assert 0 < summary["global_corr_base_alt"] <= 1.0
