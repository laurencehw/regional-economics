import json
import math
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

    # Statistical validity checks
    assert summary["se_beta"] > 0, "Standard error must be positive"
    assert 0.0 <= summary["p_value"] <= 1.0, f"p_value={summary['p_value']} outside [0, 1]"
    assert 0.0 <= summary["r_squared"] <= 1.0, f"r_squared={summary['r_squared']} outside [0, 1]"
    assert summary["p_value"] < 0.05, "Synthetic β=-0.10 should be significant at 5%"

    # Panel dimension checks (synthetic: 30 countries × 20 years)
    assert summary["n_countries"] == 30, f"Expected 30 countries, got {summary['n_countries']}"
    assert summary["year_range"][0] == 2001, f"Expected first estimation year 2001, got {summary['year_range'][0]}"
    assert summary["year_range"][1] == 2019, f"Expected last year 2019, got {summary['year_range'][1]}"

    # Half-life should be economically plausible (not near-zero or centuries)
    assert 1.0 < summary["half_life_years"] < 100.0, (
        f"half_life={summary['half_life_years']} outside plausible range"
    )

    est_csv = out_dir / "estimation_panel.csv"
    assert est_csv.exists(), "estimation_panel.csv missing"
    est_df = pd.read_csv(est_csv)
    assert not est_df.empty, "estimation_panel.csv is empty"
    assert "log_dva_lag" in est_df.columns, "Estimation panel should contain log_dva_lag"


def test_prepare_then_convergence_integration(tmp_path, run_cmd):
    prepared_dir = tmp_path / "prepared"
    prepared_dir.mkdir()

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
        str(prepared_dir),
    ])

    panel_csv = prepared_dir / "panel_mapped.csv"
    assert panel_csv.exists(), "panel_mapped.csv missing after prepare step"

    est_dir = tmp_path / "convergence"
    est_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab2_asia/code/lab2_asia_convergence_scaffold.py",
        "--panel",
        str(panel_csv),
        "--output-dir",
        str(est_dir),
    ])

    summary_json = est_dir / "model_summary.json"
    assert summary_json.exists(), "model_summary.json missing after convergence step"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "Beta_Convergence_OLS_HC1"
    assert summary["n_obs"] >= 3, f"Expected >= 3 obs from template data, got {summary['n_obs']}"
    assert math.isfinite(summary["beta"]), f"beta should be finite, got {summary['beta']}"
    assert summary["n_countries"] == 3, f"Expected 3 countries, got {summary['n_countries']}"
