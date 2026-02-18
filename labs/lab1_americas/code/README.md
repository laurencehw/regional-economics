# Lab 1 Code

## Main Entry Points
- `fetch_comtrade_api.py` (pulls UN Comtrade data using API key)
- `prepare_lab1_inputs.py` (maps raw WDI/Comtrade/BTS to canonical files)
- `lab1_americas_sar_scaffold.py` (estimates SAR on canonical files)

## Quick Start
1. Install base dependencies:
   `pip install -r requirements.txt`
2. Optionally install PySAL spatial packages:
   `pip install -r requirements-optional-spatial.txt`
3. Pull Comtrade rows (uses `COMTRADE_API_KEY` from env or `C:\Users\lwils\.claude\settings.json`):
   `C:\Python314\python.exe fetch_comtrade_api.py --period 2024 --reporter-code 840,124,484 --flow-code X --cmd-code TOTAL --output-csv ../data/comtrade_api_pull.csv --output-json ../data/comtrade_api_pull.json`
4. Map raw source files:
   `python prepare_lab1_inputs.py --wdi-input ../data/raw_templates/wdi_bulk_example.csv --comtrade-input ../data/comtrade_api_pull.csv --bts-input ../data/raw_templates/bts_border_delay_example.csv --mappings ../data/source_mappings.json --output-dir ../data --year 2024`
5. Run SAR on mapped files:
   `python lab1_americas_sar_scaffold.py --panel ../data/panel_mapped.csv --trade ../data/trade_mapped.csv --year 2024 --y-col gdp_growth --x-cols log_gdp_pc,manufacturing_share,border_delay_index --output-dir ../output`

## Canonical Input Schemas
- Panel file columns: `region`, `year`, `gdp_growth`, `log_gdp_pc`, `manufacturing_share`, `border_delay_index`
- Trade raw file columns expected by mapping: `reporter_iso`, `partner_iso`, `year`, `trade_value_usd`
- Trade mapped file columns for SAR: `origin`, `destination`, `year`, `trade_value`

## Notes
- `fetch_comtrade_api.py` defaults `partner-code` to `auto` (uses the same code list as reporters).
- If `libpysal` and `spreg` are installed, SAR uses those libraries.
- Otherwise, the SAR script runs a built-in ML estimator and still reports `rho`.
