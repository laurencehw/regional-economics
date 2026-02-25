import json
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


def test_build_lab4_panel_smoke(tmp_path):
    out_dir = tmp_path / "lab4_panel"
    out_dir.mkdir(parents=True, exist_ok=True)

    acled_counts = "labs/lab4_mena/data/raw_templates/acled_counts_example.csv"
    wdi_outcome = "labs/lab4_mena/data/raw_templates/wdi_outcome_example.csv"
    unhcr_mapped = "labs/lab4_mena/data/raw_templates/unhcr_mapped_example.csv"
    dummy_events = str(tmp_path / "dummy_acled_events.csv")

    panel_output = str(out_dir / "panel_output.csv")
    acled_cy_output = str(out_dir / "acled_country_year.csv")
    metadata_output = str(out_dir / "metadata.json")

    args = [
        sys.executable,
        "scripts/build_lab4_mena_estimation_panel.py",
        "--acled-events-csv", dummy_events,
        "--acled-counts-csv", acled_counts,
        "--wdi-outcome-csv", wdi_outcome,
        "--unhcr-mapped-csv", unhcr_mapped,
        "--acled-country-year-csv", acled_cy_output,
        "--panel-output-csv", panel_output,
        "--metadata-json", metadata_output,
    ]
    run_cmd(args)

    panel_path = Path(panel_output)
    assert panel_path.exists(), "panel_output.csv missing"
    panel = pd.read_csv(panel_path)
    assert not panel.empty, "panel_output.csv is empty"

    acled_cy_path = Path(acled_cy_output)
    assert acled_cy_path.exists(), "acled_country_year.csv missing"

    meta_path = Path(metadata_output)
    assert meta_path.exists(), "metadata.json missing"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["rows_panel"] > 0
    assert meta["countries_panel"] >= 3


def test_scm_baseline_smoke(tmp_path):
    # Stage 1: build panel
    panel_dir = tmp_path / "lab4_panel"
    panel_dir.mkdir(parents=True, exist_ok=True)

    acled_counts = "labs/lab4_mena/data/raw_templates/acled_counts_example.csv"
    wdi_outcome = "labs/lab4_mena/data/raw_templates/wdi_outcome_example.csv"
    unhcr_mapped = "labs/lab4_mena/data/raw_templates/unhcr_mapped_example.csv"
    dummy_events = str(tmp_path / "dummy_acled_events.csv")

    panel_csv = str(panel_dir / "panel.csv")
    acled_cy_csv = str(panel_dir / "acled_cy.csv")
    meta_json = str(panel_dir / "meta.json")

    build_args = [
        sys.executable,
        "scripts/build_lab4_mena_estimation_panel.py",
        "--acled-events-csv", dummy_events,
        "--acled-counts-csv", acled_counts,
        "--wdi-outcome-csv", wdi_outcome,
        "--unhcr-mapped-csv", unhcr_mapped,
        "--acled-country-year-csv", acled_cy_csv,
        "--panel-output-csv", panel_csv,
        "--metadata-json", meta_json,
    ]
    run_cmd(build_args)

    # Stage 2: run SCM baseline
    scm_dir = tmp_path / "scm_output"
    scm_dir.mkdir(parents=True, exist_ok=True)

    scm_args = [
        sys.executable,
        "scripts/run_lab4_scm_baseline.py",
        "--panel-csv", panel_csv,
        "--treated-iso3", "SYR",
        "--intervention-year", "2022",
        "--output-dir", str(scm_dir),
        "--date-stamp", "smoke",
    ]
    run_cmd(scm_args)

    weights_files = list(scm_dir.glob("scm_weights_*.csv"))
    assert len(weights_files) >= 1, "scm_weights CSV missing"
    weights = pd.read_csv(weights_files[0])
    assert len(weights) >= 2, "Need at least 2 donors in weights"

    path_files = list(scm_dir.glob("scm_path_*.csv"))
    assert len(path_files) >= 1, "scm_path CSV missing"
    path_df = pd.read_csv(path_files[0])
    assert "pre" in set(path_df["period"]), "Missing pre period in SCM path"
    assert "post" in set(path_df["period"]), "Missing post period in SCM path"

    summary_files = list(scm_dir.glob("scm_summary_*.json"))
    assert len(summary_files) >= 1, "scm_summary JSON missing"
    summary = json.loads(summary_files[0].read_text(encoding="utf-8"))
    assert summary["donor_count"] >= 2
    assert summary["pre_rmspe"] is not None
