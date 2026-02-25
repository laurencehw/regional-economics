import json
import sys

import pandas as pd


def test_compare_tiva_measures_smoke(tmp_path, run_cmd):
    out_csv = tmp_path / "comparison.csv"
    out_json = tmp_path / "summary.json"

    run_cmd([
        sys.executable,
        "scripts/compare_lab2_tiva_measures.py",
        "--base-csv",
        "labs/lab2_asia/data/raw_templates/tiva_base_example.csv",
        "--alt-csv",
        "labs/lab2_asia/data/raw_templates/tiva_alt_example.csv",
        "--output-csv",
        str(out_csv),
        "--summary-json",
        str(out_json),
    ])

    assert out_csv.exists(), "comparison CSV missing"
    df = pd.read_csv(out_csv)
    assert not df.empty, "comparison CSV is empty"

    assert out_json.exists(), "summary JSON missing"
    summary = json.loads(out_json.read_text(encoding="utf-8"))
    assert summary["rows_overlap"] > 0
    assert 0 < summary["global_corr_base_alt"] <= 1.0
