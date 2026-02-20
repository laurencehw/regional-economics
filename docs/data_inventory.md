# Data Inventory

Track acquisition status, access requirements, update cadence, and intended usage for each core dataset.

| Dataset | Primary Use | Status | Access Path | Notes |
|---|---|---|---|---|
| World Development Indicators (WDI) | Cross-country macro controls and outcomes | In progress | `data/raw/wdi/wdi_usmca_core_long_2026-02-20.csv` | Extracted on 2026-02-20 via `scripts/fetch_wdi_lab1.py` for USA/CAN/MEX and 3 core indicators (`NY.GDP.MKTP.KD.ZG`, `NY.GDP.PCAP.KD`, `NV.IND.MANF.ZS`). Next: expand indicator set and harmonize with lab panel schema. |
| UN Comtrade | Trade flows for gravity and spatial interaction | In progress | `data/raw/comtrade/comtrade_usmca_total_x_2024_2026-02-20.csv` | Extracted on 2026-02-20 via `labs/lab1_americas/code/fetch_comtrade_api.py` (reporters 840/124/484, flow X, cmd TOTAL). Includes 17 normalized rows; coverage is currently a narrow pilot pull for Lab 1. |
| Bureau of Transportation Statistics (BTS) | North American corridor and border-friction context | In progress | `data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv` | Extracted on 2026-02-20 from BTS Socrata dataset `keg4-3bc2` via `scripts/fetch_bts_border_crossings.py`; 72,539 data rows plus header from 2018 onward. Next: derive a reproducible border-friction index for Lab 1. |
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
