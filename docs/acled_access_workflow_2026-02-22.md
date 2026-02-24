# ACLED Access Workflow (Opened 2026-02-22)

This runbook opens the ACLED licensing track for Lab 4 (MENA) so data intake can proceed without blocking the chapter/lab build.

## Current Status
- Workflow opened: 2026-02-22
- Request submitted: No
- Request draft prepared: Yes (`docs/acled_request_draft_2026-02-23.md`)
- API credentials received and validation pull completed (`data/raw/metadata/acled_lab4_pull_validation_egypt_2024_2026-02-23.json`).
- Production-scope pull executed; count metadata available but row-level fields are restricted under current access window.
- Country-year count proxy generated at `data/processed/lab4/acled_lab4_country_year_counts_2018_2025_2026-02-23.csv`.
- Approval received: No
- Tracker file: `data/raw/metadata/acled_access_tracker_2026-02-22.json`
- Lab checklist: `labs/lab4_mena/data/acled_intake_checklist_2026-02-22.md`

## Submission Steps
1. Confirm project scope statement for educational/research use in Lab 4.
2. Register or confirm ACLED account holder and institutional email.
3. Submit access request covering required countries/years for MENA scope.
4. Record request ID, timestamp, and approved terms in tracker JSON.
5. Add approval date and permitted redistribution constraints to `docs/data_inventory.md`.

## License and Storage Controls
1. Keep full ACLED pulls out of git (external storage only).
2. Commit only small schema templates, metadata logs, and reproducible scripts.
3. Do not publish row-level ACLED extracts if terms prohibit redistribution.
4. When sharing outputs, aggregate to country-year or higher as required by license terms.

## Intake Readiness (Post-Approval)
1. Pull event-level records to external storage using approved credentials.
2. Validate schema against `labs/lab4_mena/data/raw_templates/acled_events_template.csv`.
3. Produce a mapped country-year panel keyed by `iso3`, `year`.
4. Log extraction date, endpoint, and filter scope in tracker JSON.

## Scripted Pull Path
1. Export credentials in shell env vars (`ACLED_USERNAME`, `ACLED_PASSWORD`).
2. Run `scripts/fetch_acled_lab4_events.py` with Lab 4 country/date scope.
3. Save metadata JSON in `data/raw/metadata/` and register output in `docs/data_inventory.md`.
