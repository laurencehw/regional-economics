# Lab 4 - MENA

## Objective
Estimate conflict-shock impacts on economic outcomes across MENA countries using synthetic control, then assess robustness with spatial spillover diagnostics.

## Core Method
Synthetic Control and event-study diagnostics

## Primary Datasets
- WDI, ACLED, UNHCR

## Variable Mapping (Initialized)
- `outcome_main` <- WDI GDP-per-capita growth (`NY.GDP.PCAP.KD.ZG`)
- `treatment_event` <- ACLED conflict-event intensity (country-year aggregate)
- `displacement_control` <- UNHCR displaced-population indicator

Mappings and intake requirements are tracked in:
- `labs/lab4_mena/data/source_mappings.json`
- `labs/lab4_mena/data/acled_intake_checklist_2026-02-22.md`
- `labs/lab4_mena/data/unhcr_intake_checklist_2026-02-23.md`
- `docs/acled_access_workflow_2026-02-22.md`

## Folder Layout
- data/: raw and interim lab data
- code/: scripts or notebooks
- output/: tables, figures, and model results

## Build Checklist
1. Confirm ACLED licensing/access approval and record metadata in tracker.
2. Normalize WDI, ACLED, and UNHCR extracts to a country-year panel.
3. Define donor pool and treatment timing for each intervention case.
4. Estimate baseline synthetic-control paths and treatment effects.
5. Run placebo/event-study diagnostics and spatial robustness checks.
6. Export reproducible outputs and interpretation notes.

## Current Gate Status
- ACLED credential validation pull completed (Egypt 2024 sample; API-reported count 129, row-level fields currently redacted) with metadata logged in `data/raw/metadata/acled_lab4_pull_validation_egypt_2024_2026-02-23.json`.
- ACLED production query executed for Lab 4 scope; row-level historical fields are currently restricted, so country-year event-count proxy is used (`data/processed/lab4/acled_lab4_country_year_counts_2018_2025_2026-02-23.csv`).
- UNHCR first real pull completed for Lab 4 scope (10 countries, 2000-2024) and mapped controls exported to `data/processed/lab4/unhcr_lab4_controls_mena_2000_2024_2026-02-23.csv`.
- First estimation-ready panel is built: `data/processed/lab4/lab4_mena_estimation_panel_2000_2024_2026-02-23.csv`.
- First SCM baseline run completed (treated `SYR`, intervention year `2018`): `labs/lab4_mena/output/scm_baseline/scm_summary_syr_2018_2026-02-24.json`.
- Remaining blocker: capture ACLED request/approval reference metadata and confirm expanded row-level access terms.
