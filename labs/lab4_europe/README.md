# Lab 4 - Europe

## Objective
Estimate policy effects at European regional boundaries using NUTS-2 panel outcomes and spatial RDD logic.

## Core Method
Spatial RDD and DiD with spillovers

## Primary Datasets
- Eurostat NUTS-2

## Current Data Gate Status
- NUTS-2 GDP panel pulled to `data/raw/eurostat/nama_10r_2gdp_nuts2_mio_eur_2000_2024_2026-02-22.csv`.
- NUTS 2024 geometry pulled to `data/raw/eurostat/ref-nuts-2024-20m.geojson.zip`.
- Pull metadata recorded in `data/raw/metadata/eurostat_nuts2_pull_2026-02-22.json`.

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
