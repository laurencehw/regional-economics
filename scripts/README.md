Utility scripts for data pipelines and automation tasks.

Current scripts:
- `fetch_wdi_lab1.py`: pulls WDI long-format indicators for selected countries.
- `fetch_bts_border_crossings.py`: pulls BTS border crossing records from dataset `keg4-3bc2`.

Typical usage:
- `C:\Python314\python.exe scripts/fetch_wdi_lab1.py --output-csv data/raw/wdi/wdi_usmca_core_long_2026-02-20.csv`
- `C:\Python314\python.exe scripts/fetch_bts_border_crossings.py --start-date 2018-01-01T00:00:00.000 --output-csv data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv`
