# Lab 6 - Africa

## Objective
Estimate spatial clustering in economic activity across African economies using night-lights intensity, then test whether governance-adjusted residuals remain spatially autocorrelated.

## Core Method
Night-lights raster analysis and Moran's I

## Primary Datasets
- VIIRS, Afrobarometer

## Variable Mapping (Wired)
- `night_lights_mean` <- VIIRS annual mean radiance (`avg_radiance` in template files)
- `governance_score` <- Afrobarometer governance/trust index (`trust_local_gov` in template files)
- Spatial links <- adjacency edge list (`shared_border_km` in template files)

Mappings are configured in `data/source_mappings.json` and transformed via `code/prepare_lab5_inputs.py`.

## Research Question
To what extent are national night-lights levels spatially clustered across African economies, and how much clustering remains after conditioning on governance quality?

## Folder Layout
- `data/`: raw and mapped lab data
- `code/`: scripts
- `output/`: tables, figures, and model results

## Build Checklist
1. Map VIIRS and Afrobarometer extracts into canonical panel inputs.
2. Build and row-standardize the adjacency matrix from edge-list links.
3. Estimate global Moran's I for night-lights levels.
4. Re-estimate Moran's I on governance-adjusted residuals.
5. Export reproducible outputs and interpretation notes.

## Minimum Deliverables
- Baseline Moran summary (`output/model_summary.json`).
- Weight matrix artifact (`output/weight_matrix.csv`).
- Estimation-ready cross-section (`output/cross_section_used.csv`).

## Current Gate Status
- Minimum reproducible scaffold is implemented with template data and smoke tests.
- Real-data gate is pending final VIIRS preprocessing decisions and Afrobarometer licensing constraints.
