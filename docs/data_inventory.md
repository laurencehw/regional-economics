# Data Inventory

Track acquisition status, access requirements, update cadence, and intended usage for each core dataset.

| Dataset | Primary Use | Status | Access Path | Notes |
|---|---|---|---|---|
| World Development Indicators (WDI) | Cross-country macro controls and outcomes | Ready | `data/raw/wdi/wdi_americas_core_long_2026-02-20.csv` | Ready for Lab 1 Americas scope (45 Americas economies; indicators `NY.GDP.MKTP.KD.ZG`, `NY.GDP.PCAP.KD`, `NV.IND.MANF.ZS`). |
| UN Comtrade | Trade flows for gravity and spatial interaction | Ready | `data/raw/comtrade/comtrade_americas_total_x_2024_2026-02-20.csv` | Ready for Lab 1 Americas scope; post-process patch applied from `data/raw/comtrade/comtrade_patch_batch_2024_2026-02-20.csv`; final normalized rows: 895. |
| Bureau of Transportation Statistics (BTS) | North American corridor and border-friction context | Ready | `data/raw/bts/bts_border_crossings_keg4_3bc2_2018_2026-02-20.csv` | Ready for Lab 1 border proxy derivation; processed proxy in `data/processed/lab1/bts_border_delay_proxy_americas_2018_2025_2026-02-20.csv`. Coverage is strongest for USA/CAN/MEX. |
| WIOD / TiVA | MRIO and value-added decomposition in Asia | Not started | TBD | Next low-friction acquisition target after Lab 5 scaffold; validate latest release and concordances. Keep ADB MRIO and OECD TiVA as backup sources if WIOD currency is insufficient. |
| Eurostat NUTS-2 | Regional GDP and treatment boundaries for Spatial RDD | Not started | TBD | Next low-friction acquisition target; record exact NUTS revision used. |
| VIIRS Night Lights | Alternative proxy for economic activity in Africa | In progress | `labs/lab5_africa/data/raw_templates/viirs_example.csv` | Lab 5 scaffold is wired with template inputs; real pull still needs cloud masking and annual compositing decisions. |
| Afrobarometer | Institutional and governance proxies | In progress | `labs/lab5_africa/data/raw_templates/afrobarometer_example.csv` | Lab 5 scaffold is wired with template inputs; real-wave selection and redistribution constraints still pending. |
| ACLED | Conflict event timing/intensity for MENA SCM | Not started | TBD | Start licensing/access request before MENA wave to avoid blocking SCM build-out. |
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

## Near-Term Acquisition Queue (as of 2026-02-21)
1. WIOD / TiVA (Asia Lab 2 readiness; low-friction public download path).
2. Eurostat NUTS-2 (Europe Lab 3 readiness; low-friction public download path).
3. ACLED access/licensing confirmation (MENA Lab 4 critical path item).
