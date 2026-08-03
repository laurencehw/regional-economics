# Lab 6 - Africa

## Objective

Estimate spatial clustering in economic activity across African economies using night-lights intensity, then test whether governance-adjusted residuals remain spatially autocorrelated.

## Core Method

Night-lights analysis and Moran's I, with a residualized sensitivity check that conditions on governance scores.

## Primary Datasets

- VIIRS night lights
- Afrobarometer governance / trust indicators
- Adjacency / shared-border spatial links

## Variable Mapping (Wired)

- `night_lights_mean` <- VIIRS annual mean radiance (`avg_radiance` in template files)
- `governance_score` <- Afrobarometer governance/trust index (`trust_local_gov` in template files)
- Spatial links <- adjacency edge list (`shared_border_km` in template files)

Mappings are configured in `data/source_mappings.json` and transformed via `code/prepare_lab6_inputs.py`.

## Research Question

To what extent are national night-lights levels spatially clustered across African economies, and how does measured clustering change after residualizing on governance quality?

## Interpretation Rule

The change from raw Moran's I to residual Moran's I is a **sensitivity statistic**, not a causal share of autocorrelation attributable to governance. Do not report `pct_change_in_i` / legacy `pct_explained` as “percent explained by governance.”

## Folder Layout

- `data/`: raw and mapped lab data
- `code/`: scripts
- `output/`: tables, figures, and model results

## Build Checklist

1. [x] Map VIIRS and Afrobarometer extracts into canonical panel inputs (template path).
2. [x] Build and row-standardize the adjacency matrix from edge-list links.
3. [x] Estimate global Moran's I for night-lights levels.
4. [x] Re-estimate Moran's I on governance-adjusted residuals (sensitivity analysis).
5. [x] Smoke tests for synthetic pipelines.
6. [ ] Real-data gate: final VIIRS preprocessing and Afrobarometer licensing.

## Minimum Deliverables

- Baseline Moran summary (`output/model_summary.json`).
- Weight matrix artifact (`output/weight_matrix.csv`).
- Estimation-ready cross-section (`output/cross_section_used.csv`).

## Evidence Labels

- `--run-smoke-test` outputs are **synthetic demonstrations**.
- Real-data gate remains pending; do not treat template or synthetic Moran estimates as published Africa findings.
