Utility scripts for data pipelines and automation tasks.

Current scripts:
- `fetch_wdi_lab1.py`: pulls WDI long-format indicators for selected countries.
- `fetch_bts_border_crossings.py`: pulls BTS border crossing records from dataset `keg4-3bc2`.
- `build_lab1_americas_real_raw.py`: builds broader Americas WDI + bilateral Comtrade raw inputs.
- `derive_lab1_bts_border_proxy.py`: derives a simple yearly border-friction proxy from BTS truck crossings.
- `fetch_wiod_release2016.py`: pulls selected WIOD 2016 release files from Dataverse.
- `fetch_oecd_tiva_mainlv_extract.py`: pulls constrained OECD TiVA MainLV extracts (small, query-limited).
- `fetch_eurostat_nuts2_lab3.py`: pulls Eurostat NUTS-2 GDP panel and NUTS geometry bundle.

Typical usage:
- `python scripts/fetch_wdi_lab1.py --output-csv data/raw/wdi/wdi_usmca_core_long_2026-02-20.csv`
- `python scripts/fetch_bts_border_crossings.py --start-date 2018-01-01T00:00:00.000 --output-csv data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv`
- `python scripts/build_lab1_americas_real_raw.py --year 2024 --batch-size 8 --date-stamp 2026-02-20`
- `python scripts/derive_lab1_bts_border_proxy.py --input-csv data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv --output-csv data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv`
- `python scripts/fetch_wiod_release2016.py --file-ids 199099,199337,199097 --output-dir data/external/wiod/2016_release --manifest-out data/raw/metadata/wiod_2016_pull_manifest_2026-02-22.json`
- `python scripts/fetch_oecd_tiva_mainlv_extract.py --measure EXGR_DVA --ref-areas CHN,JPN,KOR,IND,IDN,VNM,THA,MYS,PHL,SGP --counterpart-area OECD --output-csv data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv`
- `python scripts/fetch_eurostat_nuts2_lab3.py --output-csv data/raw/eurostat/nama_10r_2gdp_nuts2_mio_eur_2000_2024_2026-02-22.csv --geometry-zip data/raw/eurostat/ref-nuts-2024-20m.geojson.zip --metadata-json data/raw/metadata/eurostat_nuts2_pull_2026-02-22.json`
