Utility scripts for data pipelines and automation tasks.

Current scripts:
- `fetch_wdi_lab1.py`: pulls WDI long-format indicators for selected countries.
- `fetch_bts_border_crossings.py`: pulls BTS border crossing records from dataset `keg4-3bc2`.
- `build_lab1_americas_real_raw.py`: builds broader Americas WDI + bilateral Comtrade raw inputs.
- `derive_lab1_bts_border_proxy.py`: derives a simple yearly border-friction proxy from BTS truck crossings.
- `fetch_wiod_release2016.py`: pulls selected WIOD 2016 release files from Dataverse.
- `fetch_oecd_tiva_mainlv_extract.py`: pulls constrained OECD TiVA MainLV extracts (small, query-limited).
- `build_lab2_wiod_tiva_concordance.py`: builds WIOD-country and TiVA-code concordance templates for Lab 2.
- `compare_lab2_tiva_measures.py`: compares two TiVA extracts (same scope keys) and writes overlap diagnostics.
- `fetch_eurostat_nuts2_lab4.py`: pulls Eurostat NUTS-2 GDP panel and NUTS geometry bundle.
- `fetch_acled_lab5_events.py`: pulls ACLED event records via OAuth using env-var credentials.
- `fetch_unhcr_lab5_controls.py`: pulls UNHCR origin-based displacement controls and maps Lab 5 country-year panel fields.
- `fetch_acled_lab5_country_year_counts.py`: pulls ACLED country-year event counts (works when row-level fields are restricted).
- `build_lab5_mena_estimation_panel.py`: merges ACLED, UNHCR, and WDI into Lab 5 estimation-ready panel outputs.
- `run_lab5_scm_baseline.py`: runs first Lab 5 synthetic-control baseline and exports weights/path/summary artifacts.

Typical usage:
- `python scripts/fetch_wdi_lab1.py --output-csv data/raw/wdi/wdi_usmca_core_long_2026-02-20.csv`
- `python scripts/fetch_bts_border_crossings.py --start-date 2018-01-01T00:00:00.000 --output-csv data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv`
- `python scripts/build_lab1_americas_real_raw.py --year 2024 --batch-size 8 --date-stamp 2026-02-20`
- `python scripts/derive_lab1_bts_border_proxy.py --input-csv data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv --output-csv data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv`
- `python scripts/fetch_wiod_release2016.py --file-ids 199097,199099,199101,199104,199337 --output-dir data/external/wiod/2016_release --manifest-out data/raw/metadata/wiod_2016_pull_manifest_full_wiots_2026-02-22.json --skip-existing`
- `python scripts/fetch_oecd_tiva_mainlv_extract.py --measure EXGR_DVA --ref-areas CHN,JPN,KOR,IND,IDN,VNM,THA,MYS,PHL,SGP --counterpart-area OECD --output-csv data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv`
- `python scripts/fetch_oecd_tiva_mainlv_extract.py --measure EXGR_FNL --ref-areas CHN,JPN,KOR,IND,IDN,VNM,THA,MYS,PHL,SGP --counterpart-area OECD --output-csv data/raw/tiva/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.csv --metadata-json data/raw/metadata/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.json`
- `python scripts/build_lab2_wiod_tiva_concordance.py --date-stamp 2026-02-22`
- `python scripts/compare_lab2_tiva_measures.py --base-csv data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv --alt-csv data/raw/tiva/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.csv --output-csv data/processed/lab2/tiva_measure_comparison_exgr_dva_vs_exgr_fnl_2026-02-23.csv --summary-json data/processed/lab2/tiva_measure_comparison_summary_exgr_dva_vs_exgr_fnl_2026-02-23.json`
- `python scripts/fetch_eurostat_nuts2_lab4.py --output-csv data/raw/eurostat/nama_10r_2gdp_nuts2_mio_eur_2000_2024_2026-02-22.csv --geometry-zip data/raw/eurostat/ref-nuts-2024-20m.geojson.zip --metadata-json data/raw/metadata/eurostat_nuts2_pull_2026-02-22.json`
- `python scripts/fetch_acled_lab5_events.py --countries Egypt,Iraq,Jordan,Lebanon,Libya,Morocco,Saudi Arabia,Syria,Tunisia,Yemen --start-date 2018-01-01 --end-date 2025-12-31 --output-csv data/external/acled/acled_lab4_mena_2018_2025_2026-02-23.csv --metadata-json data/raw/metadata/acled_lab4_pull_mena_2018_2025_2026-02-23.json`
- `python scripts/fetch_unhcr_lab5_controls.py --iso3-list EGY,IRQ,JOR,LBN,LBY,MAR,SAU,SYR,TUN,YEM --start-year 2000 --end-year 2024 --raw-output-csv data/raw/unhcr/unhcr_lab4_origin_controls_2000_2024_2026-02-23.csv --mapped-output-csv data/processed/lab5/unhcr_lab4_controls_mena_2000_2024_2026-02-23.csv --metadata-json data/raw/metadata/unhcr_lab4_pull_mena_origin_2000_2024_2026-02-23.json`
- `python scripts/fetch_acled_lab5_country_year_counts.py --countries \"Egypt,Iraq,Jordan,Lebanon,Libya,Morocco,Saudi Arabia,Syria,Tunisia,Yemen\" --start-year 2018 --end-year 2025 --output-csv data/processed/lab5/acled_lab4_country_year_counts_2018_2025_2026-02-23.csv --metadata-json data/raw/metadata/acled_lab4_country_year_counts_2018_2025_2026-02-23.json`
- `python scripts/build_lab5_mena_estimation_panel.py --acled-country-year-csv data/processed/lab5/acled_lab4_country_year_2018_2025_2026-02-23.csv --panel-output-csv data/processed/lab5/lab4_mena_estimation_panel_2000_2024_2026-02-23.csv --metadata-json data/raw/metadata/lab4_mena_panel_build_2026-02-23.json`
- `python scripts/run_lab5_scm_baseline.py --treated-iso3 SYR --intervention-year 2018 --date-stamp 2026-02-24`

TiVA note:
- `EXGR_FVA` is valid in MainLV but constrained to `COUNTERPART_AREA=W`; use measures like `EXGR_FNL` when `COUNTERPART_AREA=OECD` is required for comparability with existing pulls.

ACLED credential note:
- Set `ACLED_USERNAME` and `ACLED_PASSWORD` in the shell environment before running the ACLED fetch script.
- If row-level responses are redacted, use `fetch_acled_lab5_country_year_counts.py` and proceed with count-based treatment intensity.
