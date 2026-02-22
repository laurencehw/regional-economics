# Data Storage Strategy

This policy keeps the repository reproducible while preventing large-data bloat as Labs 2-5 come online.

## Scope
- Effective date: 2026-02-21
- Applies to `data/`, `labs/*/data`, and generated outputs used in CI or drafting.

## Rules
1. Keep only small, reproducible samples in git.
   - Templates, schema examples, and test fixtures stay in-repo.
   - Files committed to git should generally be below 25 MB.
2. Store full raw pulls outside the repo when large.
   - Use a mounted drive, cloud bucket, or managed artifact store.
   - Register every external file in `docs/data_inventory.md` with exact path and extraction date.
3. Use deterministic naming for snapshots.
   - Pattern: `<dataset>_<scope>_<period>_<YYYY-MM-DD>.<ext>`
   - Example: `wdi_americas_core_long_2026-02-20.csv`
4. Separate layers clearly.
   - `data/raw/`: source pulls and unmodified snapshots.
   - `data/processed/`: cleaned or merged files produced by scripts.
   - `labs/*/data/raw_templates/`: small lab fixtures for smoke tests and onboarding.
5. No manual edits to processed outputs.
   - All transformations must come from scripts in `scripts/` or `labs/*/code/`.
6. Keep output artifacts scoped to the lab.
   - Draft and gate artifacts belong in `labs/<lab_name>/output/`.
   - Cross-lab reusable files should move to `data/processed/`.

## Dataset Registry Requirement
Before using a new dataset in prose or code, add:
- Source URL or API endpoint.
- Extraction date.
- Version/release.
- Geography and time coverage.
- License/redistribution constraints.
- Script entry point that reproduces the pull.

## Upcoming Pressure Points
- Lab 2 MRIO tables (WIOD/ADB MRIO/OECD TiVA) can exceed practical git sizes.
- Lab 4 ACLED event data may have license-based redistribution limits; keep raw files external and commit only metadata/templates.
- Lab 5 VIIRS raster files are expected to be large and should remain external with scripted pulls.
