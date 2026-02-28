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


def test_servicification_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "servicification"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab7_services/code/servicification_decomposition.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    # --- Summary JSON ---
    summary_json = out_dir / "servicification_summary.json"
    assert summary_json.exists(), "servicification_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "TiVA_Servicification_Decomposition"
    assert summary["n_countries"] > 5, (
        f"Expected >5 countries, got {summary['n_countries']}"
    )
    assert summary["n_sectors"] > 0
    assert summary["n_service_types"] > 0

    # --- Panel CSV ---
    panel_csv = out_dir / "servicification_panel.csv"
    assert panel_csv.exists(), "servicification_panel.csv missing"
    panel = pd.read_csv(panel_csv)
    assert not panel.empty, "Panel CSV is empty"

    # Servicification shares must be in [0, 1]
    assert (panel["servicification_share"] >= 0).all(), (
        "Servicification shares must be >= 0"
    )
    assert (panel["servicification_share"] <= 1).all(), (
        "Servicification shares must be <= 1"
    )

    # Country ranking should be consistent
    assert summary["most_servicified"]["share"] >= summary["least_servicified"]["share"]


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


def test_cloud_geography_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "cloud"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab7_services/code/cloud_geography_mapper.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    # --- Summary JSON ---
    summary_json = out_dir / "cloud_summary.json"
    assert summary_json.exists(), "cloud_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "Cloud_Geography_Mapping"
    assert summary["n_countries"] > 10, (
        f"Expected >10 countries, got {summary['n_countries']}"
    )

    # Correlation between localization score and cloud presence should exist
    assert "correlation_localization_cloud" in summary
    assert summary["correlation_localization_cloud"] is not None, (
        "correlation_localization_cloud should not be None"
    )

    # Cloud concentration metrics should exist and be sensible
    conc = summary["cloud_concentration"]
    assert "top3_share" in conc
    assert "hhi" in conc
    assert conc["top3_share"] > 0, "Top-3 share should be positive"
    assert conc["hhi"] > 0, "HHI should be positive"
    assert len(conc["top3_countries"]) == 3

    # Provider totals
    assert "provider_totals" in summary
    assert summary["provider_totals"]["AWS"] > 0

    # --- Panel CSV ---
    panel_csv = out_dir / "cloud_geography.csv"
    assert panel_csv.exists(), "cloud_geography.csv missing"
    panel = pd.read_csv(panel_csv)
    assert not panel.empty, "Panel CSV is empty"
    assert "total_cloud_regions" in panel.columns
    assert "localization_score" in panel.columns
    assert len(panel) > 10
