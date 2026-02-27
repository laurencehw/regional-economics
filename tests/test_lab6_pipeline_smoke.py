import json
import sys

import numpy as np
import pandas as pd


def test_fetch_viirs_africa_smoke(tmp_path, run_cmd):
    """Smoke test: fetch_viirs_africa.py --smoke-test produces valid CSV + adjacency."""
    viirs_dir = tmp_path / "viirs"
    adj_dir = tmp_path / "adjacency"
    viirs_dir.mkdir(parents=True, exist_ok=True)
    adj_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "scripts/fetch_viirs_africa.py",
        "--smoke-test",
        "--year", "2020",
        "--output-dir", str(viirs_dir),
        "--write-adjacency",
        "--adjacency-output-dir", str(adj_dir),
    ])

    radiance_csv = viirs_dir / "viirs_africa_2020.csv"
    meta_json = viirs_dir / "viirs_africa_2020_meta.json"
    adjacency_csv = adj_dir / "adjacency_africa.csv"

    assert radiance_csv.exists(), "viirs_africa_2020.csv missing"
    assert meta_json.exists(), "viirs_africa_2020_meta.json missing"
    assert adjacency_csv.exists(), "adjacency_africa.csv missing"

    rad = pd.read_csv(radiance_csv)
    assert set(rad.columns) >= {"iso3", "year", "avg_radiance"}, (
        f"Unexpected columns: {rad.columns.tolist()}"
    )
    assert len(rad) >= 50, f"Expected >= 50 African countries, got {len(rad)}"
    assert (rad["year"] == 2020).all(), "Year column mismatch"
    assert rad["avg_radiance"].notna().all(), "Unexpected NaN in synthetic radiance"
    assert (rad["avg_radiance"] > 0).all(), "All radiance values should be positive"

    meta = json.loads(meta_json.read_text(encoding="utf-8"))
    assert meta["smoke_test"] is True
    assert meta["year"] == 2020
    assert meta["n_valid_radiance"] == meta["n_countries"]

    adj = pd.read_csv(adjacency_csv)
    assert set(adj.columns) >= {"iso3", "neighbor_iso3", "shared_border_km"}, (
        f"Unexpected adjacency columns: {adj.columns.tolist()}"
    )
    assert len(adj) > 100, f"Expected > 100 adjacency pairs, got {len(adj)}"
    assert (adj["shared_border_km"] > 0).all(), "Border lengths should be positive"
    # Check symmetry: every (A, B) pair should have a (B, A) pair
    pairs = set(zip(adj["iso3"], adj["neighbor_iso3"]))
    for a, b in list(pairs)[:20]:  # spot-check first 20
        assert (b, a) in pairs, f"Missing reverse pair ({b}, {a})"


def test_viirs_output_feeds_prepare_inputs(tmp_path, run_cmd):
    """Integration: fetch_viirs_africa.py smoke output feeds prepare_lab6_inputs.py."""
    viirs_dir = tmp_path / "viirs"
    adj_dir = tmp_path / "adjacency"
    mapped_dir = tmp_path / "mapped"
    for d in [viirs_dir, adj_dir, mapped_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Step 1: generate synthetic VIIRS + adjacency
    run_cmd([
        sys.executable,
        "scripts/fetch_viirs_africa.py",
        "--smoke-test",
        "--year", "2021",
        "--output-dir", str(viirs_dir),
        "--write-adjacency",
        "--adjacency-output-dir", str(adj_dir),
    ])

    # Step 2: run prepare_lab6_inputs with the generated files
    run_cmd([
        sys.executable,
        "labs/lab6_africa/code/prepare_lab6_inputs.py",
        "--viirs-input", str(viirs_dir / "viirs_africa_2021.csv"),
        "--afrobarometer-input", "labs/lab6_africa/data/raw_templates/afrobarometer_example.csv",
        "--adjacency-input", str(adj_dir / "adjacency_africa.csv"),
        "--mappings", "labs/lab6_africa/data/source_mappings.json",
        "--output-dir", str(mapped_dir),
        "--year", "2021",
    ])

    summary = json.loads((mapped_dir / "mapping_summary.json").read_text(encoding="utf-8"))
    assert summary["panel_rows"] > 0, "Panel should have rows"
    assert summary["adjacency_rows"] > 0, "Adjacency should have rows"
    assert summary["panel_regions"] >= 50, (
        f"Expected >= 50 African countries, got {summary['panel_regions']}"
    )


def test_prepare_lab6_inputs_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "mapped"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab6_africa/code/prepare_lab6_inputs.py",
        "--viirs-input",
        "labs/lab6_africa/data/raw_templates/viirs_example.csv",
        "--afrobarometer-input",
        "labs/lab6_africa/data/raw_templates/afrobarometer_example.csv",
        "--adjacency-input",
        "labs/lab6_africa/data/raw_templates/adjacency_example.csv",
        "--mappings",
        "labs/lab6_africa/data/source_mappings.json",
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
        "labs/lab6_africa/code/lab6_africa_moran_scaffold.py",
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
