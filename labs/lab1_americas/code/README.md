# Lab 1 Code

## Main Entry Points
- `fetch_comtrade_api.py` (pulls UN Comtrade data using API key)
- `prepare_lab1_inputs.py` (maps raw WDI/Comtrade/BTS to canonical files)
- `lab1_americas_sar_scaffold.py` (estimates SAR on canonical files)
- `run_real_americas_specs.py` (runs multi-spec robustness comparisons on real-Americas inputs)
- `run_real_americas_interaction_specs.py` (runs institution-interaction SAR specs on blended inputs)
- `../../../scripts/fetch_wdi_lpi_americas.py` (pulls LPI indicator for broad Americas friction coverage)
- `../../../scripts/derive_lab1_lpi_border_proxy.py` (builds LPI-based border friction proxy; optionally blends BTS)

## Quick Start
1. Install base dependencies:
   `pip install -r requirements.txt`
2. Optionally install PySAL spatial packages:
   `pip install -r requirements-optional-spatial.txt`
3. Pull Comtrade rows (uses `COMTRADE_API_KEY` from env or `~/.claude/settings.json`):
   `python fetch_comtrade_api.py --period 2024 --reporter-code 840,124,484 --flow-code X --cmd-code TOTAL --output-csv ../data/comtrade_api_pull.csv --output-json ../data/comtrade_api_pull.json`
4. Map raw source files:
   `python prepare_lab1_inputs.py --wdi-input ../data/raw_templates/wdi_bulk_example.csv --comtrade-input ../data/comtrade_api_pull.csv --bts-input ../data/raw_templates/bts_border_delay_example.csv --mappings ../data/source_mappings.json --output-dir ../data --year 2024`
5. Run SAR on mapped files:
   `python lab1_americas_sar_scaffold.py --panel ../data/panel_mapped.csv --trade ../data/trade_mapped.csv --year 2024 --y-col gdp_growth --x-cols log_gdp_pc,manufacturing_share,border_delay_index --output-dir ../output`

## Real Americas Pipeline (Current Gate)
1. Build broader raw inputs:
   `python ../../../scripts/build_lab1_americas_real_raw.py --year 2024 --batch-size 8 --date-stamp 2026-02-20`
2. Build BTS border proxy:
   `python ../../../scripts/derive_lab1_bts_border_proxy.py --input-csv ../../../data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv --output-csv ../../../data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv`
3. Build broader LPI border proxy (and optionally blend BTS coverage):
   `python ../../../scripts/fetch_wdi_lpi_americas.py --output-csv ../../../data/raw/wdi/wdi_lpi_americas_long_2026-02-21.csv`
   `python ../../../scripts/derive_lab1_lpi_border_proxy.py --input-csv ../../../data/raw/wdi/wdi_lpi_americas_long_2026-02-21.csv --bts-input-csv ../../../data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv --start-year 2018 --end-year 2025 --output-csv ../../../data/processed/lab1/border_delay_proxy_americas_lpi_blend_2018_2025_2026-02-21.csv`
4. Map to canonical files:
   `python prepare_lab1_inputs.py --wdi-input ../../../data/raw/wdi/wdi_americas_core_long_2026-02-20.csv --comtrade-input ../../../data/raw/comtrade/comtrade_americas_total_x_2024_2026-02-20.csv --bts-input ../../../data/processed/lab1/border_delay_proxy_americas_lpi_blend_2018_2025_2026-02-21.csv --mappings ../data/source_mappings_americas_real.json --output-dir ../data/real_americas --year 2024`
5. Run real-sample SAR gate:
   `python lab1_americas_sar_scaffold.py --panel ../data/real_americas/panel_mapped.csv --trade ../data/real_americas/trade_mapped.csv --year 2024 --y-col gdp_growth --x-cols log_gdp_pc,manufacturing_share --output-dir ../output/real_americas_2024`
6. Run robustness spec bundle:
   `python run_real_americas_specs.py --panel ../data/real_americas/panel_mapped.csv --trade ../data/real_americas/trade_mapped.csv --year 2024 --output-dir ../output/real_americas_2024/specs`
7. Run institution-interaction spec bundle:
   `python run_real_americas_interaction_specs.py --panel ../data/real_americas_lpi_blend/panel_mapped.csv --trade ../data/real_americas_lpi_blend/trade_mapped.csv --year 2024 --output-dir ../output/real_americas_2024_lpi_blend/interaction_specs`

## Canonical Input Schemas
- Panel file columns: `region`, `year`, `gdp_growth`, `log_gdp_pc`, `manufacturing_share`, `border_delay_index`
- Trade raw file columns expected by mapping: `reporter_iso`, `partner_iso`, `year`, `trade_value_usd`
- Trade mapped file columns for SAR: `origin`, `destination`, `year`, `trade_value`

## Notes
- `fetch_comtrade_api.py` defaults `partner-code` to `auto` (uses the same code list as reporters).
- If `libpysal` and `spreg` are installed, SAR uses those libraries.
- Otherwise, the SAR script runs a built-in ML estimator and still reports `rho`.
