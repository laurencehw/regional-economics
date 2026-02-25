import sys

import pandas as pd


def test_derive_lab1_lpi_proxy_smoke(tmp_path, run_cmd):
    out_path = tmp_path / "lpi_proxy.csv"

    run_cmd([
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
    ])

    assert out_path.exists(), "LPI proxy output missing"
    out = pd.read_csv(out_path)

    assert {"region", "year", "border_delay_index", "lpi_score", "proxy_source"}.issubset(out.columns)
    assert out["region"].nunique() >= 4
    assert out["year"].min() == 2018
    assert out["year"].max() == 2024
    assert out["border_delay_index"].between(0, 1).all()
    assert set(out["proxy_source"].unique()) == {"lpi"}
