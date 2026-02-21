import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cmd(args, cwd=REPO_ROOT):
    completed = subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=True,
    )
    return completed


def test_prepare_lab1_inputs_smoke(tmp_path):
    out_dir = tmp_path / "mapped"
    out_dir.mkdir(parents=True, exist_ok=True)

    args = [
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
    ]
    run_cmd(args)

    panel = out_dir / "panel_mapped.csv"
    trade = out_dir / "trade_mapped.csv"
    summary = out_dir / "mapping_summary.json"

    assert panel.exists(), "panel_mapped.csv missing"
    assert trade.exists(), "trade_mapped.csv missing"
    assert summary.exists(), "mapping_summary.json missing"

    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["panel_rows"] > 0
    assert payload["trade_rows"] > 0


def test_sar_scaffold_smoke(tmp_path):
    out_dir = tmp_path / "sar"
    out_dir.mkdir(parents=True, exist_ok=True)

    args = [
        sys.executable,
        "labs/lab1_americas/code/lab1_americas_sar_scaffold.py",
        "--run-smoke-test",
        "--output-dir",
        str(out_dir),
    ]
    run_cmd(args)

    summary_path = out_dir / "model_summary.json"
    assert summary_path.exists(), "model_summary.json missing"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["method"] in {"SAR_ML_spreg", "SAR_manual_ML", "OLS_fallback"}
    assert summary["n_obs"] >= 5
