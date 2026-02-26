# Lab 5 Code

## Main Entry Points
- `prepare_lab6_inputs.py` (maps VIIRS/Afrobarometer/adjacency extracts into canonical files)
- `lab6_africa_moran_scaffold.py` (estimates global Moran's I on levels and governance-adjusted residuals)

## Quick Start
1. Install dependencies:
   `pip install numpy pandas`
2. Map template raw files:
   `python prepare_lab6_inputs.py --viirs-input ../data/raw_templates/viirs_example.csv --afrobarometer-input ../data/raw_templates/afrobarometer_example.csv --adjacency-input ../data/raw_templates/adjacency_example.csv --mappings ../data/source_mappings.json --output-dir ../data --year 2024`
3. Run Moran scaffold on mapped files:
   `python lab6_africa_moran_scaffold.py --panel ../data/panel_mapped.csv --adjacency ../data/adjacency_mapped.csv --year 2024 --y-col night_lights_mean --control-cols governance_score --output-dir ../output`
4. Smoke-test the estimator with synthetic data:
   `python lab6_africa_moran_scaffold.py --run-smoke-test --output-dir ../output`

## Canonical Input Schemas
- Panel file columns: `region`, `year`, `night_lights_mean`, `governance_score`
- Adjacency file columns: `region`, `neighbor`, `weight`

## Notes
- Moran permutation p-values are two-sided and reproducible via `--seed`.
- If `--control-cols` is non-empty, the script reports Moran's I on OLS residuals in addition to raw levels.
