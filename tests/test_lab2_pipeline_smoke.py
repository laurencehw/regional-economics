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


def test_prepare_lab2_inputs_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "prepared"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab2_asia/code/prepare_lab2_inputs.py",
        "--base-input",
        "labs/lab2_asia/data/raw_templates/tiva_base_example.csv",
        "--alt-input",
        "labs/lab2_asia/data/raw_templates/tiva_alt_example.csv",
        "--mappings",
        "labs/lab2_asia/data/source_mappings.json",
        "--output-dir",
        str(out_dir),
    ])

    panel_csv = out_dir / "panel_mapped.csv"
    assert panel_csv.exists(), "panel_mapped.csv missing"
    df = pd.read_csv(panel_csv)

    assert df.shape[0] == 12, f"Expected 12 rows (3 countries × 4 years), got {df.shape[0]}"

    expected_cols = ["country", "year", "dva_value", "fnl_value", "dva_ratio", "dva_growth", "dva_lag"]
    for col in expected_cols:
        assert col in df.columns, f"Missing canonical column: {col}"

    assert df["dva_growth"].isna().sum() == 3, "Expected 3 NaN dva_growth (first year per country)"
    assert df["dva_lag"].isna().sum() == 3, "Expected 3 NaN dva_lag (first year per country)"
    assert (df["dva_ratio"].dropna() > 1.0).all(), "DVA should exceed FNL in template data"

    summary_json = out_dir / "mapping_summary.json"
    assert summary_json.exists(), "mapping_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    assert summary["panel_rows"] == 12
    assert summary["panel_countries"] == 3


def test_convergence_scaffold_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "convergence"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab2_asia/code/lab2_asia_convergence_scaffold.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    summary_json = out_dir / "model_summary.json"
    assert summary_json.exists(), "model_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "Beta_Convergence_OLS_HC1"
    assert summary["n_obs"] >= 100, f"Expected ≥100 obs from synthetic data, got {summary['n_obs']}"
    assert -0.20 < summary["beta"] < 0.0, f"beta={summary['beta']} outside expected range (-0.20, 0)"
    assert summary["convergence_detected"] is True
    assert summary["half_life_years"] > 0

    est_csv = out_dir / "estimation_panel.csv"
    assert est_csv.exists(), "estimation_panel.csv missing"
    est_df = pd.read_csv(est_csv)
    assert not est_df.empty, "estimation_panel.csv is empty"
