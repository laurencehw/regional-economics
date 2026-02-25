import json
import sys

import numpy as np
import pandas as pd


def test_prepare_lab5_inputs_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "mapped"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab5_africa/code/prepare_lab5_inputs.py",
        "--viirs-input",
        "labs/lab5_africa/data/raw_templates/viirs_example.csv",
        "--afrobarometer-input",
        "labs/lab5_africa/data/raw_templates/afrobarometer_example.csv",
        "--adjacency-input",
        "labs/lab5_africa/data/raw_templates/adjacency_example.csv",
        "--mappings",
        "labs/lab5_africa/data/source_mappings.json",
        "--output-dir",
        str(out_dir),
        "--year",
        "2024",
    ])

    panel = out_dir / "panel_mapped.csv"
    adjacency = out_dir / "adjacency_mapped.csv"
    summary = out_dir / "mapping_summary.json"

    assert panel.exists(), "panel_mapped.csv missing"
    assert adjacency.exists(), "adjacency_mapped.csv missing"
    assert summary.exists(), "mapping_summary.json missing"

    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["panel_rows"] > 0
    assert payload["adjacency_rows"] > 0


def test_moran_scaffold_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "moran"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab5_africa/code/lab5_africa_moran_scaffold.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    summary_path = out_dir / "model_summary.json"
    assert summary_path.exists(), "model_summary.json missing"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["method"] == "Global_Morans_I"
    assert summary["n_obs"] >= 5
    assert abs(float(summary["moran_i"])) <= 1.5

    # Synthetic data has positive spatial autocorrelation
    assert summary["moran_i"] > 0, "Synthetic grid data should exhibit positive Moran's I"
    assert summary["moran_i"] > summary["expected_i_null"], (
        "Moran's I should exceed null expectation for spatially autocorrelated data"
    )

    # p-value validity
    assert 0.0 <= summary["p_value_two_sided"] <= 1.0, (
        f"p_value={summary['p_value_two_sided']} outside [0, 1]"
    )

    # Residualized Moran's I: governance should explain some spatial clustering
    assert "residual_moran_i" in summary, "Residual Moran's I missing from summary"
    assert summary["residual_moran_i"] < summary["moran_i"], (
        "Residual Moran's I should be smaller after partialing out governance"
    )
    assert 0.0 <= summary["residual_p_value_two_sided"] <= 1.0

    # Weight density should be positive (grid has neighbors)
    assert summary["weight_density"] > 0, "Weight density should be positive"

    # Weight matrix: symmetric, zero diagonal
    wm_path = out_dir / "weight_matrix.csv"
    assert wm_path.exists(), "weight_matrix.csv missing"
    wm = pd.read_csv(wm_path, index_col=0).to_numpy(dtype=float)
    assert wm.shape[0] == wm.shape[1], "Weight matrix not square"
    assert np.allclose(np.diag(wm), 0.0), "Weight matrix diagonal should be zero"
    row_sums = wm.sum(axis=1)
    nonzero_rows = row_sums[row_sums > 0]
    assert np.allclose(nonzero_rows, 1.0, atol=1e-8), "Non-zero rows should sum to 1"
