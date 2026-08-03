# Lab 4 - Europe

## Objective

Estimate Cohesion Policy effects at the EU eligibility threshold using NUTS-2 outcomes and a local-linear RDD.

## Core Method

**Eligibility-threshold RDD** (income relative to the Cohesion cutoff), not a geographic boundary RDD. Sharp RDD estimates the eligibility effect; fuzzy RDD is required when eligibility instruments realized transfers. DiD-with-spillovers remains a planned extension, not the current scaffold.

## Primary Datasets

- Eurostat NUTS-2 GDP
- Eligibility / GDP-per-capita PPS relative to programming-period thresholds

## Current Data Gate Status

- NUTS-2 GDP panel pulled to `data/raw/eurostat/nama_10r_2gdp_nuts2_mio_eur_2000_2024_2026-02-22.csv`.
- NUTS 2024 geometry pulled to `data/raw/eurostat/ref-nuts-2024-20m.geojson.zip`.
- Pull metadata recorded in `data/raw/metadata/eurostat_nuts2_pull_2026-02-22.json`.
- Scaffold and smoke tests implement sharp local-linear RDD with HC1 SEs.

## Folder Layout

- `data/`: raw and interim lab data
- `code/`: scripts
- `output/`: tables, figures, and model results

## Build Checklist

1. [x] Define outcome and eligibility forcing variable.
2. [x] Sharp local-linear RDD scaffold with kernel weights and HC1 SEs.
3. [~] Real Eurostat/eligibility panel mapping.
4. [ ] Fuzzy RDD for treatment intensity.
5. [ ] Programming-period-specific thresholds and pooled designs.
6. [ ] Export reproducible real-data outputs and interpretation notes.

## Evidence Labels

- `--run-smoke-test` outputs are **synthetic demonstrations** with a known treatment effect.
- Real-data summaries should report design type (`eligibility_threshold_RDD`), period rules, and whether treatment is eligibility or transfers.
