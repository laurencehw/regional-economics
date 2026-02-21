Utility scripts for data pipelines and automation tasks.

Current scripts:
- `fetch_wdi_lab1.py`: pulls WDI long-format indicators for selected countries.
- `fetch_bts_border_crossings.py`: pulls BTS border crossing records from dataset `keg4-3bc2`.
- `build_lab1_americas_real_raw.py`: builds broader Americas WDI + bilateral Comtrade raw inputs.
- `derive_lab1_bts_border_proxy.py`: derives a simple yearly border-friction proxy from BTS truck crossings.

Typical usage:
- `C:\Python314\python.exe scripts/fetch_wdi_lab1.py --output-csv data/raw/wdi/wdi_usmca_core_long_2026-02-20.csv`
- `C:\Python314\python.exe scripts/fetch_bts_border_crossings.py --start-date 2018-01-01T00:00:00.000 --output-csv data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv`
- `C:\Python314\python.exe scripts/build_lab1_americas_real_raw.py --year 2024 --batch-size 8 --date-stamp 2026-02-20`
- `C:\Python314\python.exe scripts/derive_lab1_bts_border_proxy.py --input-csv data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv --output-csv data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv`
