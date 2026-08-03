# Lab 2 - Asia

## Objective
Estimate value-added exposure and network dependence in Asian production systems using MRIO-style trade-in-value-added indicators.

## Core Method
MRIO and network econometrics for value chains

## Primary Datasets
- WIOD, TiVA

## Evidence Labels
- `--run-smoke-test` outputs are **synthetic demonstrations**.
- Real TiVA/WIOD runs are **author calculations**. Chapter 7 may cite the reproducible share-mode pipeline and its imprecision, but must not present unsupported subgroup ceilings or electronics-specific coefficients until those extracts exist.

## Estimands
- Preferred upgrading estimand: `dva_share = EXGR_DVA / EXGR`
- Dependent variable in share mode: percentage-point change in `dva_share` (`100 * Δs`)
- Legacy diagnostic: growth in the dollar **level** of `EXGR_DVA`
- `EXGR_FNL` is a companion foreign-content measure; it is **not** the share denominator

## Current Data Gate Status
- WIOD starter pull logged in `data/raw/metadata/wiod_2016_pull_manifest_2026-02-22.json` (files stored in `data/external/wiod/2016_release/`).
- OECD TiVA MainLV extracts (ACTIVITY=`_T`, COUNTERPART=`OECD`):
  - `data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv`
  - `data/raw/tiva/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.csv`
  - `data/raw/tiva/tiva_mainlv_asia_oecd_exgr_2000_2023_2026-08-03.csv`
- Mapped panel with validated shares: `data/real_asia/panel_mapped.csv` (`230/230` valid `dva_share` rows).
- Share-mode year-FE robustness suite: `output/real_asia/specs_share/` (ASEAN-6, Northeast Asia, leave-China-out, leave-one-economy-out).
- Legacy level-mode diagnostics remain under `output/real_asia/specs/` if present; do not mix estimands.
- Electronics (C26) fetch scaffold exists (`fetch_tiva_electronics.py`); a matching real `EXGR` C26 pull is still outstanding.

## Folder Layout
- data/: raw and interim lab data
- code/: scripts or notebooks
- output/: tables, figures, and model results

## Build Checklist
1. [x] Add gross-exports denominator path (`EXGR`) in prepare + templates.
2. [x] Construct `dva_share = EXGR_DVA / EXGR` with explicit definition and diagnostics.
3. [x] Estimate year-FE share-mode baseline in the scaffold (`--outcome-mode share --year-fe`).
4. [x] Fetch real TiVA `EXGR` for the Lab 2 country/activity sample (`_T` / OECD).
5. [x] Re-run ASEAN, Northeast Asia, leave-China-out, and leave-one-economy-out checks in share mode.
6. [x] Export coefficients, uncertainty, implied half-lives, and provenance metadata (`specs_share/`).
7. [ ] Optional: electronics C26 share panel with matching `EXGR` denominator.
8. [ ] Optional: wild cluster / small-cluster inference before manuscript claims.

## Reproduce Share Specs
```bash
python scripts/fetch_oecd_tiva_mainlv_extract.py --measure EXGR \
  --ref-areas CHN,JPN,KOR,IND,IDN,VNM,THA,MYS,PHL,SGP --counterpart-area OECD \
  --output-csv data/raw/tiva/tiva_mainlv_asia_oecd_exgr_2000_2023_2026-08-03.csv \
  --metadata-json data/raw/metadata/tiva_mainlv_asia_oecd_exgr_2000_2023_2026-08-03.json

python labs/lab2_asia/code/prepare_lab2_inputs.py \
  --base-input data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv \
  --alt-input data/raw/tiva/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.csv \
  --exgr-input data/raw/tiva/tiva_mainlv_asia_oecd_exgr_2000_2023_2026-08-03.csv \
  --mappings labs/lab2_asia/data/source_mappings.json \
  --output-dir labs/lab2_asia/data/real_asia

cd labs/lab2_asia/code
python run_real_asia_specs.py --outcome-mode share --year-fe --leave-one-out \
  --output-dir ../output/real_asia/specs_share
```
