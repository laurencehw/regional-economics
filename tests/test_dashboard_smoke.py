import json
import sys


def _run_dashboard(tmp_path, run_cmd, region):
    """Helper: run dashboard for a single region, return parsed summary."""
    out_dir = tmp_path / f"dash_{region}"
    out_dir.mkdir()

    run_cmd([
        sys.executable,
        "scripts/generate_regional_dashboard.py",
        "--run-smoke-test",
        "--region", region,
        "--output-dir", str(out_dir),
    ])

    summary_json = out_dir / "dashboard_summary.json"
    assert summary_json.exists(), f"dashboard_summary.json missing for {region}"
    return json.loads(summary_json.read_text(encoding="utf-8"))


def _validate_summary(summary, region):
    """Common assertions for every region."""
    assert summary["method"] == "Regional_Diagnostics_Dashboard"
    assert summary["region"] == region
    assert summary["smoke_test"] is True

    # Convergence
    conv = summary["convergence"]
    assert conv["beta"] < 0, f"beta should be negative, got {conv['beta']}"
    assert conv["half_life_years"] > 0
    assert conv["sigma_direction"] in ("declining", "flat", "rising")

    # Inequality
    ineq = summary["inequality"]
    assert 0 < ineq["spatial_gini"] < 1, f"Gini out of range: {ineq['spatial_gini']}"

    # Activity ranking
    act = summary["activity_ranking"]
    assert len(act["top_5"]) == 5, f"Expected 5 top units, got {len(act['top_5'])}"
    assert len(act["bottom_5"]) == 5, f"Expected 5 bottom units, got {len(act['bottom_5'])}"

    # Services
    assert len(summary["services_top5"]) == 5, (
        f"Expected 5 service categories, got {len(summary['services_top5'])}"
    )

    # Headline exists
    assert "headline" in summary
    assert "label" in summary["headline"]


def test_dashboard_americas_smoke(tmp_path, run_cmd):
    s = _run_dashboard(tmp_path, run_cmd, "americas")
    _validate_summary(s, "americas")
    assert s["lab_number"] == 1
    assert s["headline"]["type"] == "sar_rho"


def test_dashboard_east_asia_smoke(tmp_path, run_cmd):
    s = _run_dashboard(tmp_path, run_cmd, "east_asia")
    _validate_summary(s, "east_asia")
    assert s["lab_number"] == 2
    assert s["headline"]["type"] == "convergence_scatter"


def test_dashboard_south_asia_smoke(tmp_path, run_cmd):
    s = _run_dashboard(tmp_path, run_cmd, "south_asia")
    _validate_summary(s, "south_asia")
    assert s["lab_number"] == 3
    assert s["headline"]["type"] == "hhi_lq"


def test_dashboard_europe_smoke(tmp_path, run_cmd):
    s = _run_dashboard(tmp_path, run_cmd, "europe")
    _validate_summary(s, "europe")
    assert s["lab_number"] == 4
    assert s["headline"]["type"] == "rdd_tau"


def test_dashboard_mena_smoke(tmp_path, run_cmd):
    s = _run_dashboard(tmp_path, run_cmd, "mena")
    _validate_summary(s, "mena")
    assert s["lab_number"] == 5
    assert s["headline"]["type"] == "scm_gap"


def test_dashboard_africa_smoke(tmp_path, run_cmd):
    s = _run_dashboard(tmp_path, run_cmd, "africa")
    _validate_summary(s, "africa")
    assert s["lab_number"] == 6
    assert s["headline"]["type"] == "moran_i"


def test_dashboard_all_regions_consistent(tmp_path, run_cmd):
    """All 6 regions should produce identical top-level JSON keys."""
    regions = ["americas", "east_asia", "south_asia", "europe", "mena", "africa"]
    key_sets = []
    for region in regions:
        s = _run_dashboard(tmp_path, run_cmd, region)
        key_sets.append(set(s.keys()))

    # All regions should have identical top-level keys
    first = key_sets[0]
    for i, ks in enumerate(key_sets[1:], 1):
        assert ks == first, (
            f"Region {regions[i]} has different keys: "
            f"extra={ks - first}, missing={first - ks}"
        )
