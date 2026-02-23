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
- Access workflow is initialized; ACLED request submission is pending.
- Intake template and checklist are in place so pull/validation can start immediately after approval.
