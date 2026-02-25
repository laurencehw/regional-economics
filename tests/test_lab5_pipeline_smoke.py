import json
import sys


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
