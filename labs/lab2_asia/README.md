# Lab 2 - Asia

## Objective
Estimate value-added exposure and network dependence in Asian production systems using MRIO-style trade-in-value-added indicators.

## Core Method
MRIO and network econometrics for value chains

## Primary Datasets
- WIOD, TiVA

## Current Data Gate Status
- WIOD starter pull logged in `data/raw/metadata/wiod_2016_pull_manifest_2026-02-22.json` (files stored in `data/external/wiod/2016_release/`).
- OECD TiVA starter extract available at `data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv`.
- Next gate is expanding to full WIOTS inputs and additional TiVA measures for concordance checks.

## Folder Layout
- data/: raw and interim lab data
- code/: scripts or notebooks
- output/: tables, figures, and model results

## Build Checklist
1. Define outcome and explanatory variables.
2. Prepare and validate spatial/network objects.
3. Estimate baseline specification.
4. Run diagnostics and robustness checks.
5. Export reproducible outputs and interpretation notes.
