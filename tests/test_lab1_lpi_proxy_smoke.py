import subprocess
import sys
from pathlib import Path

import pandas as pd


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


def test_derive_lab1_lpi_proxy_smoke(tmp_path):
    out_path = tmp_path / "lpi_proxy.csv"

    args = [
        sys.executable,
        "scripts/derive_lab1_lpi_border_proxy.py",
        "--input-csv",
        "labs/lab1_americas/data/raw_templates/lpi_wdi_example.csv",
        "--start-year",
        "2018",
        "--end-year",
        "2024",
        "--output-csv",
        str(out_path),
    ]
    run_cmd(args)

    assert out_path.exists(), "LPI proxy output missing"
    out = pd.read_csv(out_path)

    assert {"region", "year", "border_delay_index", "lpi_score", "proxy_source"}.issubset(out.columns)
    assert out["region"].nunique() >= 4
    assert out["year"].min() == 2018
    assert out["year"].max() == 2024
    assert out["border_delay_index"].between(0, 1).all()
    assert set(out["proxy_source"].unique()) == {"lpi"}
