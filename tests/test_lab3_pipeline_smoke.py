import json
import sys

import pandas as pd


def test_prepare_lab3_inputs_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "prepared"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab3_south_asia/code/prepare_lab3_inputs.py",
        "--klems-input",
        "labs/lab3_south_asia/data/raw_templates/klems_it_example.csv",
        "--mappings",
        "labs/lab3_south_asia/data/source_mappings.json",
        "--output-dir",
        str(out_dir),
    ])

    panel_csv = out_dir / "panel_mapped.csv"
    assert panel_csv.exists(), "panel_mapped.csv missing"
    df = pd.read_csv(panel_csv)

    assert df.shape[0] == 36, f"Expected 36 rows (9 states × 4 years), got {df.shape[0]}"

    expected_cols = [
        "region", "year", "it_va", "total_gdp", "it_share",
        "it_employment", "total_employment", "it_emp_share", "va_per_worker",
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing canonical column: {col}"

    # IT share should be between 0 and 1
    shares = df["it_share"].dropna()
    assert (shares >= 0).all(), "IT share should be non-negative"
    assert (shares <= 1).all(), "IT share should be <= 1"

    # VA per worker should be positive
    vpw = df["va_per_worker"].dropna()
    assert (vpw > 0).all(), "VA per worker should be positive"

    summary_json = out_dir / "mapping_summary.json"
    assert summary_json.exists(), "mapping_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    assert summary["panel_rows"] == 36
    assert summary["panel_regions"] == 9


def test_concentration_scaffold_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "concentration"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab3_south_asia/code/lab3_concentration_scaffold.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    summary_json = out_dir / "model_summary.json"
    assert summary_json.exists(), "model_summary.json missing"
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "Concentration_Analysis"
    assert summary["n_regions"] == 12, f"Expected 12 regions, got {summary['n_regions']}"

    # HHI should be between 1/n (uniform) and 1.0 (monopoly)
    hhi = summary["herfindahl_index"]
    assert 0.0 < hhi <= 1.0, f"HHI={hhi} outside valid range"
    # With strong concentration in Karnataka/Telangana, HHI should exceed uniform (1/12 ≈ 0.083)
    assert hhi > 0.10, f"HHI={hhi} too low — expected concentration above uniform"

    # Gini should be between 0 (equality) and 1 (inequality)
    gini = summary["gini_coefficient"]
    assert 0.0 < gini < 1.0, f"Gini={gini} outside valid range"
    # With highly skewed IT-sector data, Gini should be substantial
    assert gini > 0.3, f"Gini={gini} too low for concentrated IT sector"

    # Top LQ regions should be the IT hubs
    top_lq = summary["top_3_regions_by_lq"]
    assert len(top_lq) == 3, "Should report top 3 LQ regions"
    top_names = [r["region"] for r in top_lq]
    assert "Karnataka" in top_names, "Karnataka should be in top 3 by LQ"
    assert "Telangana" in top_names, "Telangana should be in top 3 by LQ"

    # LQ > 1 means above-national-average specialization
    for entry in top_lq:
        assert entry["lq"] > 1.0, f"{entry['region']} LQ should exceed 1.0"

    # HHI time series should exist and show multiple years
    hhi_ts = summary["hhi_time_series"]
    assert len(hhi_ts) == 4, f"Expected 4 years in HHI time series, got {len(hhi_ts)}"

    # Results CSV should exist with concentration data
    results_csv = out_dir / "concentration_results.csv"
    assert results_csv.exists(), "concentration_results.csv missing"
    results_df = pd.read_csv(results_csv)
    assert "location_quotient" in results_df.columns


def test_prepare_then_concentration_integration(tmp_path, run_cmd):
    """Integration test: prepare inputs → run concentration analysis."""
    prepared_dir = tmp_path / "prepared"
    prepared_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab3_south_asia/code/prepare_lab3_inputs.py",
        "--klems-input",
        "labs/lab3_south_asia/data/raw_templates/klems_it_example.csv",
        "--mappings",
        "labs/lab3_south_asia/data/source_mappings.json",
        "--output-dir",
        str(prepared_dir),
    ])

    panel_csv = prepared_dir / "panel_mapped.csv"
    assert panel_csv.exists()

    est_dir = tmp_path / "concentration"
    est_dir.mkdir()

    run_cmd([
        sys.executable,
        "labs/lab3_south_asia/code/lab3_concentration_scaffold.py",
        "--panel",
        str(panel_csv),
        "--year",
        "2018",
        "--output-dir",
        str(est_dir),
    ])

    summary_json = est_dir / "model_summary.json"
    assert summary_json.exists()
    summary = json.loads(summary_json.read_text(encoding="utf-8"))

    assert summary["method"] == "Concentration_Analysis"
    assert summary["n_regions"] == 9, f"Expected 9 regions from template, got {summary['n_regions']}"
    assert summary["year"] == 2018
    assert summary["herfindahl_index"] > 0
    assert summary["gini_coefficient"] > 0
