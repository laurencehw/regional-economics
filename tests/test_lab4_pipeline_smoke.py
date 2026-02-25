import json
import sys

import numpy as np
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

    # SCM weights must be non-negative and sum to ~1
    w_vals = weights["weight"].to_numpy(dtype=float)
    assert (w_vals >= -1e-10).all(), "SCM weights must be non-negative"
    assert np.isclose(w_vals.sum(), 1.0, atol=1e-6), f"SCM weights sum to {w_vals.sum()}, expected ~1.0"

    path_files = list(scm_dir.glob("scm_path_*.csv"))
    assert len(path_files) >= 1, "scm_path CSV missing"
    path_df = pd.read_csv(path_files[0])
    assert "pre" in set(path_df["period"]), "Missing pre period in SCM path"
    assert "post" in set(path_df["period"]), "Missing post period in SCM path"

    # Path values should be finite where available
    for col in ["treated_outcome", "synthetic_outcome"]:
        vals = path_df[col].dropna()
        assert len(vals) > 0, f"{col} has no non-null values"
        assert np.all(np.isfinite(vals.to_numpy(dtype=float))), f"{col} contains non-finite values"

    summary_files = list(scm_dir.glob("scm_summary_*.json"))
    assert len(summary_files) >= 1, "scm_summary JSON missing"
    summary = json.loads(summary_files[0].read_text(encoding="utf-8"))
    assert summary["donor_count"] >= 2
    assert summary["pre_rmspe"] is not None
    assert summary["pre_rmspe"] > 0, "Pre-RMSPE should be positive"
    assert summary["pre_year_count"] >= 3, "Need at least 3 pre-intervention years"
    assert summary["post_year_count"] >= 1, "Need at least 1 post-intervention year"


def test_scm_robustness_smoke(tmp_path, run_cmd, lab4_panel):
    """Run in-space and in-time placebos on template data."""
    rob_dir = tmp_path / "scm_robustness"
    rob_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "scripts/run_lab4_scm_robustness.py",
        "--panel-csv", str(lab4_panel["panel_csv"]),
        "--treated-iso3", "SYR",
        "--intervention-year", "2022",
        "--placebo-years", "2021,2023",
        "--output-dir", str(rob_dir),
        "--date-stamp", "smoke",
    ])

    # --- In-space placebo checks ---
    in_space_files = list(rob_dir.glob("placebo_in_space_*.json"))
    assert len(in_space_files) >= 1, "placebo_in_space JSON missing"
    in_space = json.loads(in_space_files[0].read_text(encoding="utf-8"))

    # Template has 4 units; all should be feasible at year 2022
    assert len(in_space) >= 3, f"Expected >= 3 in-space placebos, got {len(in_space)}"

    # Exactly one entry should be the baseline
    baseline_entries = [r for r in in_space if r.get("is_baseline")]
    assert len(baseline_entries) == 1, "Exactly one baseline entry expected"

    # All RMSPE ratios should be positive where available
    for r in in_space:
        ratio = r.get("post_pre_rmspe_ratio")
        if ratio is not None:
            assert ratio > 0, f"RMSPE ratio for {r['treated_unit']} should be positive"

    # Weights for each placebo should be non-negative and sum to ~1
    for r in in_space:
        w_dict = r.get("weights", {})
        w_vals = np.array(list(w_dict.values()), dtype=float)
        if len(w_vals) > 0:
            assert (w_vals >= -1e-10).all(), f"Placebo weights negative for {r['treated_unit']}"
            assert np.isclose(w_vals.sum(), 1.0, atol=1e-6), (
                f"Placebo weights sum to {w_vals.sum()} for {r['treated_unit']}"
            )

    # --- In-time placebo checks ---
    in_time_files = list(rob_dir.glob("placebo_in_time_*.json"))
    assert len(in_time_files) >= 1, "placebo_in_time JSON missing"
    in_time = json.loads(in_time_files[0].read_text(encoding="utf-8"))
    assert len(in_time) >= 1, "Expected at least 1 in-time placebo result"

    for r in in_time:
        assert r["treated_unit"] == "SYR"
        assert r["intervention_year"] in [2021, 2023]

    # --- Robustness summary checks ---
    summary_files = list(rob_dir.glob("robustness_summary_*.json"))
    assert len(summary_files) >= 1, "robustness_summary JSON missing"
    summary = json.loads(summary_files[0].read_text(encoding="utf-8"))

    assert summary["treated_iso3"] == "SYR"
    assert summary["intervention_year"] == 2022
    assert summary["in_space_placebo_count"] >= 3

    # Rank-based p-value should be in (0, 1]
    rank_p = summary["in_space_rank_p_value"]
    if rank_p is not None:
        assert 0.0 < rank_p <= 1.0, f"Rank p-value={rank_p} outside (0, 1]"

    assert summary["in_time_placebo_count"] >= 1
    assert summary["in_time_placebo_years"] == [2021, 2023]
