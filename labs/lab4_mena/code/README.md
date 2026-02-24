Place notebooks/scripts here.

ACLED pull entry point:
- `scripts/fetch_acled_lab4_events.py` (uses OAuth credentials from env vars).
- `scripts/fetch_acled_lab4_country_year_counts.py` (country-year count proxy when row-level data are restricted).
- `scripts/fetch_unhcr_lab4_controls.py` (pulls and maps UNHCR country-year displacement controls).
- `scripts/build_lab4_mena_estimation_panel.py` (builds merged estimation-ready panel).
- `scripts/run_lab4_scm_baseline.py` (runs first SCM baseline and writes weights/path/summary outputs).

Environment variables required:
- `ACLED_USERNAME`
- `ACLED_PASSWORD`
