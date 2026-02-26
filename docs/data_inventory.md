# Data Inventory

Track acquisition status, access requirements, update cadence, and intended usage for each core dataset.

| Dataset | Primary Use | Status | Access Path | Notes |
|---|---|---|---|---|
| World Development Indicators (WDI) | Cross-country macro controls and outcomes | Ready | `data/raw/wdi/wdi_americas_core_long_2026-02-20.csv`, `data/raw/wdi/wdi_lab4_mena_outcome_long_2000_2024_2026-02-23.csv` | Ready for Lab 1 Americas scope and Lab 5 MENA outcome pull (`NY.GDP.PCAP.KD.ZG`; 241 rows for 10 countries, 2000-2024 window). |
| UN Comtrade | Trade flows for gravity and spatial interaction | Ready | `data/raw/comtrade/comtrade_americas_total_x_2024_2026-02-20.csv` | Ready for Lab 1 Americas scope; post-process patch applied from `data/raw/comtrade/comtrade_patch_batch_2024_2026-02-20.csv`; final normalized rows: 895. |
| Bureau of Transportation Statistics (BTS) | North American corridor and border-friction context | Ready | `data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv` | Ready for Lab 1 border proxy derivation; processed proxy in `data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv`. Coverage is strongest for USA/CAN/MEX. |
| World Bank LPI (WDI `LP.LPI.OVRL.XQ`) | Broad Americas logistics-friction proxy for Lab 1 robustness | Ready | `data/raw/wdi/wdi_lpi_americas_long_2026-02-22.csv` | Fetched via `scripts/fetch_wdi_lpi_americas.py`; transformed/blended via `scripts/derive_lab1_lpi_border_proxy.py` to `data/processed/lab1/border_delay_proxy_americas_lpi_blend_2018_2025_2026-02-22.csv`. 2024 non-missing border coverage increased from 3 to 28 regions. |
| WIOD / TiVA | MRIO and value-added decomposition in Asia | In progress | `data/raw/metadata/wiod_2016_pull_manifest_full_wiots_2026-02-22.json`, `data/raw/tiva/tiva_mainlv_asia_oecd_exgr_dva_2000_2023_2026-02-22.csv`, `data/raw/tiva/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.csv`, `data/raw/metadata/tiva_mainlv_asia_oecd_exgr_fnl_2000_2023_2026-02-23.json`, `data/processed/lab2/wiod_tiva_concordance_summary_2026-02-22.json`, `data/processed/lab2/tiva_measure_comparison_summary_exgr_dva_vs_exgr_fnl_2026-02-23.json` | WIOD 2016 pull expanded to full WIOTS package set (`WIOTS_in_R.zip`, `WIOTS_in_EXCEL.zip`) plus NIOTS/docs with size-validated manifest logging. OECD TiVA constrained extracts now include `EXGR_DVA` and `EXGR_FNL` for 10 core Asian economies (`OECD` counterpart, annual USD, 230 rows each, 2000-2022 observed). `EXGR_FVA` is available in TiVA but constrained to world counterpart (`W`) in MainLV. Lab 2 concordance and measure-comparison templates are generated in `data/processed/lab2/`. |
| Eurostat NUTS-2 | Regional GDP and treatment boundaries for Spatial RDD | Ready | `data/raw/eurostat/nama_10r_2gdp_nuts2_mio_eur_2000_2024_2026-02-22.csv`, `data/raw/eurostat/ref-nuts-2024-20m.geojson.zip` | Eurostat API pull completed (`nama_10r_2gdp`, `MIO_EUR`, NUTS-2 filter, 7,498 rows / 309 regions). NUTS 2024 geometry bundle (20m geojson) pulled from GISCO. Metadata log: `data/raw/metadata/eurostat_nuts2_pull_2026-02-22.json`. |
| VIIRS Night Lights | Alternative proxy for economic activity in Africa | In progress | `labs/lab6_africa/data/raw_templates/viirs_example.csv` | Lab 6 scaffold is wired with template inputs; real pull still needs cloud masking and annual compositing decisions. |
| Afrobarometer | Institutional and governance proxies | In progress | `labs/lab6_africa/data/raw_templates/afrobarometer_example.csv` | Lab 6 scaffold is wired with template inputs; real-wave selection and redistribution constraints still pending. |
| ACLED | Conflict event timing/intensity for MENA SCM | In progress | `docs/acled_access_workflow_2026-02-22.md`, `docs/acled_request_draft_2026-02-23.md`, `data/raw/metadata/acled_access_tracker_2026-02-22.json`, `data/raw/metadata/acled_lab4_pull_validation_egypt_2024_2026-02-23.json`, `data/raw/metadata/acled_lab4_pull_mena_2018_2025_2026-02-23.json`, `data/raw/metadata/acled_lab4_country_year_counts_2018_2025_2026-02-23.json`, `data/processed/lab5/acled_lab4_country_year_counts_2018_2025_2026-02-23.csv`, `scripts/fetch_acled_lab5_events.py`, `scripts/fetch_acled_lab5_country_year_counts.py` | Credentials are active and production-scope queries run; current access exposes reliable country-year counts but redacts row-level historical fields under date-recency restrictions. Count-based treatment proxy is available; pending formal request/approval metadata and expanded row-level scope confirmation. |
| UNHCR Population Statistics | Refugee/displacement spillovers | Ready | `data/raw/unhcr/unhcr_lab4_origin_controls_2000_2024_2026-02-23.csv`, `data/processed/lab5/unhcr_lab4_controls_mena_2000_2024_2026-02-23.csv`, `data/raw/metadata/unhcr_lab4_pull_mena_origin_2000_2024_2026-02-23.json` | First real pull completed for 10 Lab 5 MENA countries (2000-2024) with mapped country-year controls (`iso3`, `year`, displacement fields). |

## Status Legend
- `Not started`: dataset not yet downloaded or validated.
- `In progress`: access and/or acquisition started; cleaning/validation ongoing.
- `Ready`: validated and documented for chapter/lab use.

## Minimum Metadata to Add Per Dataset
- Download or API endpoint.
- Extraction date.
- Version/release identifier.
- Geographic unit.
- Time coverage.
- Core variables used.
- Known caveats.

## Near-Term Acquisition Queue (as of 2026-02-24)
1. Capture ACLED request/approval reference metadata and confirm historical row-level access scope.
2. Validate count-based ACLED proxy sensitivity once row-level fields are available.
3. Run Lab 5 placebo/robustness SCM checks on top of `labs/lab5_mena/output/scm_baseline/`.
