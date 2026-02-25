import json
import sys

import pandas as pd


def test_build_lab4_panel_smoke(lab4_panel):
    panel_csv = lab4_panel["panel_csv"]
    assert panel_csv.exists(), "panel_output.csv missing"
    panel = pd.read_csv(panel_csv)
    assert not panel.empty, "panel_output.csv is empty"

    acled_cy_csv = lab4_panel["acled_cy_csv"]
    assert acled_cy_csv.exists(), "acled_country_year.csv missing"

    meta_json = lab4_panel["meta_json"]
    assert meta_json.exists(), "metadata.json missing"
    meta = json.loads(meta_json.read_text(encoding="utf-8"))
    assert meta["rows_panel"] > 0
    assert meta["countries_panel"] >= 3


def test_scm_baseline_smoke(tmp_path, run_cmd, lab4_panel):
    scm_dir = tmp_path / "scm_output"
    scm_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "scripts/run_lab4_scm_baseline.py",
        "--panel-csv", str(lab4_panel["panel_csv"]),
        "--treated-iso3", "SYR",
        "--intervention-year", "2022",
        "--output-dir", str(scm_dir),
        "--date-stamp", "smoke",
    ])

    weights_files = list(scm_dir.glob("scm_weights_*.csv"))
    assert len(weights_files) >= 1, "scm_weights CSV missing"
    weights = pd.read_csv(weights_files[0])
    assert len(weights) >= 2, "Need at least 2 donors in weights"

    path_files = list(scm_dir.glob("scm_path_*.csv"))
    assert len(path_files) >= 1, "scm_path CSV missing"
    path_df = pd.read_csv(path_files[0])
    assert "pre" in set(path_df["period"]), "Missing pre period in SCM path"
    assert "post" in set(path_df["period"]), "Missing post period in SCM path"

    summary_files = list(scm_dir.glob("scm_summary_*.json"))
    assert len(summary_files) >= 1, "scm_summary JSON missing"
    summary = json.loads(summary_files[0].read_text(encoding="utf-8"))
    assert summary["donor_count"] >= 2
    assert summary["pre_rmspe"] is not None
