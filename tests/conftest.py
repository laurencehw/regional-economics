import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def run_cmd():
    """Return a callable that runs a subprocess from the repo root."""
    def _run(args, cwd=REPO_ROOT):
        return subprocess.run(
            args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=True,
        )
    return _run


@pytest.fixture
def lab5_panel(tmp_path, run_cmd):
    """Build the Lab 5 estimation panel from raw templates and return output paths."""
    out_dir = tmp_path / "lab5_panel"
    out_dir.mkdir(parents=True, exist_ok=True)

    panel_csv = out_dir / "panel.csv"
    acled_cy_csv = out_dir / "acled_cy.csv"
    meta_json = out_dir / "meta.json"
    dummy_events = tmp_path / "dummy_acled_events.csv"
    dummy_events.touch()

    run_cmd([
        sys.executable,
        "scripts/build_lab5_mena_estimation_panel.py",
        "--acled-events-csv", str(dummy_events),
        "--acled-counts-csv", "labs/lab5_mena/data/raw_templates/acled_counts_example.csv",
        "--wdi-outcome-csv", "labs/lab5_mena/data/raw_templates/wdi_outcome_example.csv",
        "--unhcr-mapped-csv", "labs/lab5_mena/data/raw_templates/unhcr_mapped_example.csv",
        "--acled-country-year-csv", str(acled_cy_csv),
        "--panel-output-csv", str(panel_csv),
        "--metadata-json", str(meta_json),
    ])

    return {
        "panel_csv": panel_csv,
        "acled_cy_csv": acled_cy_csv,
        "meta_json": meta_json,
    }
