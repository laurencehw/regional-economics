"""Smoke tests for all 16+2 chapter figure scripts.

Each test runs a chapter figure script with --run-smoke-test, verifies:
  1. Exit code 0
  2. JSON summary file produced
  3. At least one PNG output file
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = REPO_ROOT / "figures"

# Map of chapter key → script name
CHAPTER_SCRIPTS = {
    "ch01": "ch01_figures.py",
    "ch02": "ch02_figures.py",
    "ch03a": "ch03a_figures.py",
    "ch03b": "ch03b_figures.py",
    "ch04": "ch04_figures.py",
    "ch05": "ch05_figures.py",
    "ch06": "ch06_figures.py",
    "ch07": "ch07_figures.py",
    "ch08": "ch08_figures.py",
    "ch09": "ch09_figures.py",
    "ch10": "ch10_figures.py",
    "ch11": "ch11_figures.py",
    "ch12": "ch12_figures.py",
    "ch13": "ch13_figures.py",
    "ch14": "ch14_figures.py",
    "ch15": "ch15_figures.py",
    "ch16": "ch16_figures.py",
}


def _run_figure_script(tmp_path, run_cmd, chapter_key):
    """Helper: run a chapter figure script, return parsed summary."""
    script = CHAPTER_SCRIPTS[chapter_key]
    out_dir = tmp_path / f"fig_{chapter_key}"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        str(FIGURES_DIR / script),
        "--run-smoke-test",
        "--output-dir", str(out_dir),
    ])

    # Find summary JSON
    summaries = list(out_dir.glob("*_summary.json"))
    assert len(summaries) >= 1, f"No summary JSON found for {chapter_key}"
    summary = json.loads(summaries[0].read_text(encoding="utf-8"))

    # Find PNG files
    pngs = list(out_dir.glob("*.png"))
    assert len(pngs) >= 1, f"No PNG files found for {chapter_key}"

    return summary, pngs


# ------------------------------------------------------------------ #
#  Part I: Conceptual diagrams (no geopandas needed)
# ------------------------------------------------------------------ #

def test_ch01_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch01")
    assert len(summary["figures"]) == 2
    assert any("von_thunen" in p.name for p in pngs)
    assert any("core_periphery" in p.name for p in pngs)


def test_ch02_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch02")
    assert len(summary["figures"]) == 1
    assert any("institutional" in p.name for p in pngs)


def test_ch03a_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch03a")
    assert len(summary["figures"]) == 2
    assert any("weight_matrix" in p.name for p in pngs)
    assert any("moran" in p.name for p in pngs)


def test_ch03b_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch03b")
    assert len(summary["figures"]) == 1
    assert any("gravity" in p.name for p in pngs)


# ------------------------------------------------------------------ #
#  Part II–VII: Regional chapters (maps degrade gracefully w/o geopandas)
# ------------------------------------------------------------------ #

def test_ch04_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch04")
    assert len(summary["figures"]) == 2
    assert any("manufacturing" in p.name for p in pngs)


def test_ch05_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch05")
    assert len(summary["figures"]) == 2
    assert any("middle_income" in p.name for p in pngs)


def test_ch06_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch06")
    assert len(summary["figures"]) == 2
    assert any("dva" in p.name for p in pngs)


def test_ch07_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch07")
    assert len(summary["figures"]) == 2
    assert any("provincial" in p.name for p in pngs)


def test_ch08_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch08")
    assert len(summary["figures"]) == 2
    assert any("concentration" in p.name or "it_" in p.name for p in pngs)


def test_ch09_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch09")
    assert len(summary["figures"]) == 2


def test_ch10_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch10")
    assert len(summary["figures"]) == 2


def test_ch11_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch11")
    assert len(summary["figures"]) == 2


def test_ch12_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch12")
    assert len(summary["figures"]) == 2


def test_ch13_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch13")
    assert len(summary["figures"]) == 2


def test_ch14_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch14")
    assert len(summary["figures"]) == 2


def test_ch15_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch15")
    assert len(summary["figures"]) == 2


def test_ch16_figures_smoke(tmp_path, run_cmd):
    summary, pngs = _run_figure_script(tmp_path, run_cmd, "ch16")
    assert len(summary["figures"]) == 2


# ------------------------------------------------------------------ #
#  Cross-script validation
# ------------------------------------------------------------------ #

def test_all_figure_scripts_exist():
    """Verify all expected figure scripts exist in the figures/ directory."""
    for key, script in CHAPTER_SCRIPTS.items():
        path = FIGURES_DIR / script
        assert path.exists(), f"Missing figure script: {path}"


def test_figure_utils_importable():
    """Verify figure_utils.py can be imported without errors."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("figure_utils",
                                                    FIGURES_DIR / "figure_utils.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "FIGURE_WIDTH")
    assert hasattr(mod, "save_figure")
    assert hasattr(mod, "REGION_COLORS")
