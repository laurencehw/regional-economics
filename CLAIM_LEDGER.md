# Claim Ledger (F1)

Working ledger for precise factual claims. Status values: `verified`, `qualified`, `needs-source`, `scenario`.
Manuscript information cutoff: **July 1, 2026** (see preface).

| ID | Chapter | Claim (compressed) | Source | Year/vintage | Unit / geography | Status | Notes |
|---|---|---|---|---|---|---|---|
| F1-04-01 | 4 | USMCA steel/aluminum: 70% NA purchase; steel melt-and-pour from July 2027; no equivalent Al smelt-and-cast rule as of cutoff | USTR 2026 automotive report; USTR USMCA text | 2020 agreement; 2026/2027 phase-ins | North America | verified | Corrected from earlier “70% melt-and-pour” shorthand |
| F1-04-02 | 4 | COVID US–Canada/Mexico land-border restrictions lasted through Nov 2021 | CBP / DHS public notices | 2020–2021 | US land borders | verified | Not “through 2022” |
| F1-07-01 | 7 | Shenzhen 1979 baseline: town ~25k; Bao'an County ~314k; do not equate town to today’s municipality | UN-Habitat 2019 | 1978/1979 | Shenzhen / Bao'an | verified | |
| F1-07-02 | 7 | 2018 Shenzhen–HK comparison is total GDP, not GDP per capita | NBS China; HK C&SD (via chapter sources) | 2018 | city-level | verified | |
| F1-07-03 | 7 | Hukou vs resident-population distinction required for migrant statistics | Au and Henderson 2006; Combes et al. 2014 | various | Chinese cities | verified | |
| F1-08-01 | 8 | Indian students abroad / IIT migration rates require dated sources | chapter sources | dated in text | India | verified | Softened absolute rates |
| F1-09-01 | 9 | Basque R&D intensity ~2.15% of GDP, not ~9% | Eustat | recent vintage in text | Basque Country | verified | |
| F1-09-02 | 9 | EU had collective borrowing instruments before NGEU | European Commission | historical | EU | verified | |
| F1-11-01 | 11 | Pre-2018 GCC corporate taxation was not uniformly zero | IMF / national tax summaries | pre-2018 | GCC | verified | |
| F1-12-01 | 12 | Mohamed Bouazizi was not a university graduate | Al Jazeera 2011; contemporaneous reporting | 2010–2011 | Tunisia | verified | |
| F1-14-01 | 14 | AfCFTA Secretariat is in Accra, not Kigali | AfCFTA Secretariat | ongoing | Ghana | verified | |
| F1-14-02 | 14 | South Africa ~47% of SADC GDP; SACU revenue-sharing is formulaic, not pure size | SADC; SACU | dated in text | SADC/SACU | verified | |
| F1-15-01 | 15 | Groundswell migration figures are SSP–RCP scenarios with upper bounds, not forecasts | Clement et al. 2021; World Bank Groundswell Part 2 | scenario horizons in text | global/regions | verified | |
| F1-06-01 | 6 | Japan/Korea/Taiwan/ASEAN/China electronics DVA share bands | OECD TiVA 2023 (illustrative bands) | TiVA release vintage | East Asia electronics | qualified | Aggregate bands; Lab 2 `_T`/OECD panel is a different estimand |
| F1-14-03 | 14 | AfCFTA ROO coverage 92.3% of tariff lines | tralac 2024; Naumann 2024 | as of 2024 (text); cutoff July 1, 2026 | continental | qualified | Re-check if Secretariat publishes a later share |
| F1-07-04 | 7 | Lab 2 ASEAN/Northeast Asia share-mode β coefficients | `labs/lab2_asia/output/real_asia/specs_share/` | author calculation | 10 Asian economies, `_T`/OECD | qualified | Negative point estimates, not significant; not manuscript findings |

## Extraction backlog (needs-source pass)

Priority chapters for the next quantitative sweep: Ch. 4 (IRA/CHIPS plant announcements), Ch. 6 (foundry cost and market-share figures), Ch. 8 (NASSCOM export totals), Ch. 11 (SWF AUM), Ch. 14 (corridor transit-time claims), Ch. 16 (platform/AI subscriber counts).

## How to extend

1. Add one row per precise number, proper noun date, or legal-status claim.
2. Prefer primary official sources over secondary summaries.
3. Mark scenarios and author calculations explicitly.
4. Re-run `python scripts/audit_citations.py` after adding new author-year cites.
