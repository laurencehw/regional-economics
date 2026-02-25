import json
import sys

import numpy as np
import pandas as pd


def test_prepare_lab1_inputs_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "mapped"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab1_americas/code/prepare_lab1_inputs.py",
        "--wdi-input",
        "labs/lab1_americas/data/raw_templates/wdi_bulk_example.csv",
        "--comtrade-input",
        "labs/lab1_americas/data/raw_templates/comtrade_example.csv",
        "--bts-input",
        "labs/lab1_americas/data/raw_templates/bts_border_delay_example.csv",
        "--mappings",
        "labs/lab1_americas/data/source_mappings.json",
        "--output-dir",
        str(out_dir),
        "--year",
        "2024",
    ])

    panel = out_dir / "panel_mapped.csv"
    trade = out_dir / "trade_mapped.csv"
    summary = out_dir / "mapping_summary.json"

    assert panel.exists(), "panel_mapped.csv missing"
    assert trade.exists(), "trade_mapped.csv missing"
    assert summary.exists(), "mapping_summary.json missing"

    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["panel_rows"] > 0
    assert payload["trade_rows"] > 0


def test_sar_scaffold_smoke(tmp_path, run_cmd):
    out_dir = tmp_path / "sar"
    out_dir.mkdir(parents=True, exist_ok=True)

    run_cmd([
        sys.executable,
        "labs/lab1_americas/code/lab1_americas_sar_scaffold.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ])

    summary_path = out_dir / "model_summary.json"
    assert summary_path.exists(), "model_summary.json missing"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["method"] in {"SAR_ML_spreg", "SAR_manual_ML", "OLS_fallback"}
    assert summary["n_obs"] >= 5

    # Betas list is non-empty
    assert len(summary["betas"]) >= 2, "Need at least intercept + one covariate"

    # Rho is finite and bounded for spatial methods
    if summary["method"] in {"SAR_ML_spreg", "SAR_manual_ML"}:
        assert "rho" in summary
        assert np.isfinite(summary["rho"]), "rho must be finite"
        assert -1.0 <= summary["rho"] <= 1.0, f"rho={summary['rho']} out of [-1, 1]"

    # Weight matrix: square, zero diagonal, rows sum to ~1
    wm_path = out_dir / "weight_matrix.csv"
    assert wm_path.exists(), "weight_matrix.csv missing"
    wm = pd.read_csv(wm_path, index_col=0)
    assert wm.shape[0] == wm.shape[1], "Weight matrix not square"
    diag = np.diag(wm.to_numpy(dtype=float))
    assert np.allclose(diag, 0.0), "Weight matrix diagonal should be zero"
    row_sums = wm.to_numpy(dtype=float).sum(axis=1)
    nonzero_rows = row_sums[row_sums > 0]
    assert np.allclose(nonzero_rows, 1.0, atol=1e-8), "Non-zero rows should sum to 1 (row-standardized)"
