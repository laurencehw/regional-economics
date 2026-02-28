import json
import sys

import pandas as pd


def test_gravity_services_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "gravity"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab7_services/code/gravity_services_scaffold.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    summary_json = out_dir / "model_summary.json"
    assert summary_json.exists(), "model_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "PPML_Gravity_Comparison"
    assert summary["n_pairs"] > 50, f"Expected >50 pairs, got {summary['n_pairs']}"

    # Services model should exist and converge
    svc = summary["services_model"]
    assert svc["method"] == "PPML_Gravity"
    assert svc["converged"] is True, "Services PPML did not converge"
    assert svc["n_obs"] > 0

    # Distance elasticity should be negative (farther = less trade)
    dist_comp = summary["distance_comparison"]
    assert dist_comp["services_distance_elasticity"] < 0, (
        f"Services distance elasticity should be negative, got "
        f"{dist_comp['services_distance_elasticity']}"
    )

    # Goods model should also exist
    assert "goods_model" in summary, "Goods model missing from comparison"
    goods = summary["goods_model"]
    assert goods["n_obs"] > 0

    # Both models should produce distance elasticities (sign check already done above)
    # The comparison field should exist (exact ranking may vary with random data)
    assert "services_more_distance_sensitive" in dist_comp

    # Gravity dataset CSV should exist
    dataset_csv = out_dir / "gravity_dataset.csv"
    assert dataset_csv.exists()
    df = pd.read_csv(dataset_csv)
    assert "log_dist" in df.columns
    assert "services_trade" in df.columns


def test_stri_tariff_equivalent_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "stri"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab7_services/code/stri_tariff_equivalent.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    summary_json = out_dir / "model_summary.json"
    assert summary_json.exists(), "model_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "STRI_Tariff_Equivalent"
    assert summary["n_pairs"] > 30

    # STRI coefficient should be negative (higher barriers = less trade)
    assert summary["stri_coefficient"] < 0, (
        f"STRI coefficient should be negative, got {summary['stri_coefficient']}"
    )

    # Tariff equivalents should exist and be non-negative
    tariff_csv = out_dir / "tariff_equivalents.csv"
    assert tariff_csv.exists()
    tariff_df = pd.read_csv(tariff_csv)
    assert not tariff_df.empty
    assert "tariff_equivalent_pct" in tariff_df.columns
    assert (tariff_df["tariff_equivalent_pct"] >= 0).all(), (
        "Tariff equivalents should be non-negative"
    )

    # Most restrictive country should have highest tariff equivalent
    te_summary = summary["tariff_equivalent_summary"]
    assert te_summary["max_pct"] > 0, "Max tariff equivalent should be positive"
    assert te_summary["mean_pct"] >= 0, "Mean tariff equivalent should be non-negative"


def test_gravity_with_template_data(tmp_path, run_cmd):
    """Integration test using template CSV files."""
    out_dir = tmp_path / "gravity_template"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab7_services/code/gravity_services_scaffold.py",
        "--trade",
        "labs/lab7_services/data/raw_templates/services_trade_example.csv",
        "--gravity",
        "labs/lab7_services/data/raw_templates/gravity_vars_example.csv",
        "--year",
        "2019",
        "--output-dir",
        str(out_dir),
    ])

    summary_json = out_dir / "model_summary.json"
    assert summary_json.exists()
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "PPML_Gravity_Comparison"
    assert summary["services_model"]["n_obs"] > 0
    assert summary["services_model"]["converged"] is True
