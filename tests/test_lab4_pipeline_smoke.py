import json
import sys

import pandas as pd


def test_prepare_lab4_inputs_smoke(tmp_path, run_cmd):
    """Test that the preparation script produces a valid panel from template data."""
    out_dir = tmp_path / "mapped"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab4_europe/code/prepare_lab4_inputs.py",
        "--eurostat-input",
        "labs/lab4_europe/data/raw_templates/eurostat_gdp_example.csv",
        "--eligibility-input",
        "labs/lab4_europe/data/raw_templates/eligibility_example.csv",
        "--mappings",
        "labs/lab4_europe/data/source_mappings.json",
        "--output-dir",
        str(out_dir),
    ])

    panel = out_dir / "panel_mapped.csv"
    summary = out_dir / "mapping_summary.json"

    assert panel.exists(), "panel_mapped.csv missing"
    assert summary.exists(), "mapping_summary.json missing"

    df = pd.read_csv(panel)
    assert not df.empty, "panel_mapped.csv is empty"

    expected_cols = {"nuts2_code", "year", "gdp_mio_eur", "gdp_growth", "forcing_var", "treated"}
    assert expected_cols.issubset(set(df.columns)), f"Missing columns: {expected_cols - set(df.columns)}"

    assert df["treated"].isin([0, 1]).all(), "treated column must be binary"
    assert df["treated"].sum() > 0, "No treated regions in panel"
    assert (df["treated"] == 0).sum() > 0, "No control regions in panel"

    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["panel_rows"] > 0
    assert payload["treated_regions"] > 0
    assert payload["control_regions"] > 0


def test_rdd_scaffold_smoke(tmp_path, run_cmd):
    """Test that the RDD scaffold runs in smoke-test mode and recovers a plausible estimate."""
    out_dir = tmp_path / "rdd"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab4_europe/code/lab4_europe_rdd_scaffold.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    summary_path = out_dir / "model_summary.json"
    assert summary_path.exists(), "model_summary.json missing"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["method"] == "Sharp_RDD_Local_Linear"
    assert summary["n_obs"] >= 5

    tau = float(summary["tau"])
    assert 0.5 < tau < 4.0, f"Estimated tau={tau} outside plausible range for synthetic data"

    # Statistical validity checks
    assert summary["se_tau"] > 0, "Standard error must be positive"
    assert 0.0 <= summary["p_value"] <= 1.0, f"p_value={summary['p_value']} outside [0, 1]"
    assert summary["p_value"] < 0.05, "Synthetic tau=2.0 should be significant at 5%"
    assert summary["bandwidth"] > 0, "Bandwidth must be positive"
    assert summary["n_effective"] > 0, "Effective sample size must be positive"

    # t-stat sign should match tau
    assert (summary["t_stat"] > 0) == (tau > 0), "t_stat sign should match tau sign"

    sample_path = out_dir / "rdd_sample.csv"
    assert sample_path.exists(), "rdd_sample.csv missing"
    sample = pd.read_csv(sample_path)
    assert not sample.empty, "rdd_sample.csv is empty"
    assert {"nuts2_code", "gdp_growth", "forcing_var", "treated"}.issubset(
        set(sample.columns)
    ), "RDD sample missing expected columns"


def test_prepare_then_rdd_integration(tmp_path, run_cmd):
    """End-to-end: prepare panel from templates, then run RDD on it."""
    panel_dir = tmp_path / "panel"
    panel_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab4_europe/code/prepare_lab4_inputs.py",
        "--eurostat-input",
        "labs/lab4_europe/data/raw_templates/eurostat_gdp_example.csv",
        "--eligibility-input",
        "labs/lab4_europe/data/raw_templates/eligibility_example.csv",
        "--mappings",
        "labs/lab4_europe/data/source_mappings.json",
        "--output-dir",
        str(panel_dir),
        "--year",
        "2022",
    ])

    rdd_dir = tmp_path / "rdd_integration"
    rdd_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab4_europe/code/lab4_europe_rdd_scaffold.py",
        "--panel",
        str(panel_dir / "panel_mapped.csv"),
        "--year",
        "2022",
        "--output-dir",
        str(rdd_dir),
    ])

    summary_path = rdd_dir / "model_summary.json"
    assert summary_path.exists(), "model_summary.json missing"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["method"] == "Sharp_RDD_Local_Linear"
    assert summary["n_obs"] >= 4


def test_build_eligibility_smoke(tmp_path, run_cmd):
    """Test that the eligibility builder produces valid output from template GDP data."""
    out_csv = tmp_path / "eligibility.csv"

    run_cmd([
        sys.executable,
        "scripts/build_lab4_eligibility.py",
        "--gdp-input",
        "labs/lab4_europe/data/raw_templates/eurostat_gdp_example.csv",
        "--ref-start", "2018",
        "--ref-end", "2020",
        "--min-ref-years", "2",
        "--output",
        str(out_csv),
    ])

    assert out_csv.exists(), "eligibility CSV missing"
    df = pd.read_csv(out_csv)
    assert not df.empty, "eligibility CSV is empty"

    expected_cols = {"nuts2_code", "programming_period", "gdp_pc_pps", "eu_threshold_75pct", "eligible"}
    assert expected_cols.issubset(set(df.columns)), f"Missing columns: {expected_cols - set(df.columns)}"

    assert df["eligible"].isin([0, 1]).all(), "eligible column must be binary"
    assert df["eligible"].sum() > 0, "No treated regions"
    assert (df["eligible"] == 0).sum() > 0, "No control regions"
    assert (df["eu_threshold_75pct"] > 0).all(), "Threshold must be positive"

    summary_path = out_csv.parent / "eligibility_construction_summary.json"
    assert summary_path.exists(), "construction summary JSON missing"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["treated_regions"] > 0
    assert summary["control_regions"] > 0
    assert summary["threshold_value"] > 0
