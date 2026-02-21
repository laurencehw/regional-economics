# Data Inventory

Track acquisition status, access requirements, update cadence, and intended usage for each core dataset.

| Dataset | Primary Use | Status | Access Path | Notes |
|---|---|---|---|---|
| World Development Indicators (WDI) | Cross-country macro controls and outcomes | Ready | `data/raw/wdi/wdi_americas_core_long_2026-02-20.csv` | Ready for Lab 1 Americas scope (45 Americas economies; indicators `NY.GDP.MKTP.KD.ZG`, `NY.GDP.PCAP.KD`, `NV.IND.MANF.ZS`). |
| UN Comtrade | Trade flows for gravity and spatial interaction | Ready | `data/raw/comtrade/comtrade_americas_total_x_2024_2026-02-20.csv` | Ready for Lab 1 Americas scope; post-process patch applied from `data/raw/comtrade/comtrade_patch_batch_2024_2026-02-20.csv`; final normalized rows: 895. |
| Bureau of Transportation Statistics (BTS) | North American corridor and border-friction context | Ready | `data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv` | Ready for Lab 1 border proxy derivation; processed proxy in `data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv`. Coverage is strongest for USA/CAN/MEX. |
| WIOD / TiVA | MRIO and value-added decomposition in Asia | Not started | TBD | Validate latest available release and concordances. |
| Eurostat NUTS-2 | Regional GDP and treatment boundaries for Spatial RDD | Not started | TBD | Record exact NUTS revision used. |
| VIIRS Night Lights | Alternative proxy for economic activity in Africa | Not started | TBD | Define cloud masking and annual compositing method. |
| Afrobarometer | Institutional and governance proxies | Not started | TBD | Track survey waves and geocoding constraints; confirm licensing terms for redistribution. |
| ACLED | Conflict event timing/intensity for MENA SCM | Not started | TBD | Verify licensing and usage limits for publication/distribution. |
| UNHCR Population Statistics | Refugee/displacement spillovers | Not started | TBD | Align temporal frequency with GDP series. |

## Status Legend
- `Not started`: dataset not yet downloaded or validated.
- `In progress`: acquisition complete, cleaning/validation ongoing.
- `Ready`: validated and documented for chapter/lab use.

## Minimum Metadata to Add Per Dataset
- Download or API endpoint.
- Extraction date.
- Version/release identifier.
- Geographic unit.
- Time coverage.
- Core variables used.
- Known caveats.
