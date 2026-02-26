# Chapter Spec: Ch.7 - China's Internal Divergence and ASEAN Fragmentation

## Metadata
- Part: Part III-A - East Asia and ASEAN
- Target word count: 10,500
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-04-19

## Core Thesis
China's Great Divergence — the widening productivity and income gap between coastal mega-regions and interior provinces — is institutionally produced by the Hukou system, fiscal decentralization, and selective SOE reform that channel investment toward export-oriented coastal zones. Simultaneously, ASEAN's economic geography is fragmented by sovereignty boundaries, divergent regulatory regimes, and incomplete integration, yet connected by emergent platform economies and the Belt & Road Initiative's infrastructure corridors. Together, these dynamics illustrate how institutional barriers to factor mobility within and between states generate persistent spatial inequality even amid rapid aggregate growth.

## Key Arguments (3-5)
1. **China's Coastal-Inland Divergence.** The interaction of Hukou restrictions, fiscal federalism, and export-processing zone policies concentrates high-productivity manufacturing and services in coastal mega-regions (Pearl River Delta, Yangtze River Delta, Jing-Jin-Ji), while interior provinces remain dependent on resource extraction and transfer payments. Internal migration flows are massive but institutionally incomplete — migrants lack full access to urban public goods, suppressing human-capital accumulation and consumption spillovers.
2. **Medical Tourism as Mode 2 Services Trade.** Thailand (Bumrungrad International Hospital) and Singapore illustrate how health services can become spatially concentrated export industries under GATS Mode 2 (consumption abroad). Institutional enablers include JCI accreditation, visa facilitation, and deliberate positioning by national tourism/health agencies. These medical tourism corridors create specialized agglomeration economies distinct from traditional manufacturing clusters.
3. **ASEAN Platform Economies (Grab/Gojek).** Regional digital platforms demonstrate how network effects can partially overcome ASEAN's regulatory fragmentation, creating de facto economic integration ahead of de jure harmonization. Platform firms' spatial expansion strategies — city-by-city, country-by-country — reveal the binding constraints of divergent licensing, payments regulation, and data-localization rules across ASEAN member states.
4. **Digital Silk Road and Belt & Road Infrastructure.** China's BRI reshapes ASEAN economic geography through transport corridors (China-Laos Railway, ECRL in Malaysia), special economic zones, and digital infrastructure (Huawei/ZTE telecommunications networks, cloud data centers). The spatial economics of BRI projects raise questions about debt sustainability, sovereignty, and whether infrastructure connectivity translates into genuine economic integration or reinforces hub-spoke dependency on China.
5. **Climate Vulnerability and Managed Retreat.** The Mekong Delta and Pearl River Delta face existential climate risks (sea-level rise, saltwater intrusion, intensifying typhoons) that will force managed retreat and reshape economic geography. Climate adaptation is not spatially neutral — it will redistribute population, capital, and economic activity, with institutional capacity determining whether retreat is orderly or chaotic.

## Spatial Data Challenge
- **Hukou distortion hiding ~300M internal migrants.** China's official population statistics assign individuals to their Hukou registration location, not their actual place of residence and work. This creates a systematic mismeasurement of approximately 300 million internal migrants who live and work in coastal cities but are statistically counted in their rural home provinces. Researchers must use census micro-data, mobile phone location data, or Baidu migration indices to approximate actual population distributions. The distortion cascades into per-capita GDP calculations, urbanization rates, and fiscal burden estimates — making sub-national panel econometrics in China significantly more treacherous than headline data availability suggests.

## Institutional Variable Operationalization
- Institutional variable: `integration_barrier_rt`.
- Measurement:
  - Hukou restrictiveness index (by city tier and province).
  - ASEAN regulatory divergence score (NTBs, licensing requirements, data-localization rules by sector and member state).
  - BRI connectivity index (transport infrastructure, digital infrastructure, SEZ proximity).
- Spatial interaction term: `integration_barrier_rt × connectivity_rt` in migration and trade regressions.

## Required Datasets
- China National Bureau of Statistics (NBS) provincial and prefectural panels (GDP, employment, fixed-asset investment, migration).
- ASEAN Statistical Yearbook and ASEANstats database.
- WTO Tourism Satellite Account and UNWTO tourism statistics (for Mode 2 medical tourism flows).
- AidData Global Chinese Development Finance Dataset (for BRI project-level data).
- Baidu Migration Index or equivalent mobile-phone-based migration proxies.
- Nighttime lights and satellite imagery for cross-validating Chinese provincial GDP.

## Anchor References (2-3)
1. Lu and Wan (2014), or Fan, Kanbur, and Zhang (2011) — China regional inequality and internal migration literature.
2. Yeung (2016), *Strategic Coupling: East Asian Industrial Transformation in the New Global Economy* — GPN framework applied to ASEAN integration.
3. Hillman (2021), *The Digital Silk Road: China's Quest to Wire the World* — BRI digital infrastructure and geopolitical implications.

## Figures/Maps Needed
- **China coastal-inland divergence map**: Choropleth of per-capita GDP or total factor productivity at the prefectural level, highlighting the coastal-inland gradient and the role of mega-regions (PRD, YRD, Jing-Jin-Ji).
- **Medical tourism corridor visualization**: Flow map showing patient flows from source countries to Thailand (Bangkok/Bumrungrad) and Singapore, with annotations on institutional enablers (JCI accreditation, visa policies, insurance partnerships).
- ASEAN regulatory fragmentation dashboard: comparative heatmap of NTBs, data-localization rules, and licensing regimes across member states and key service sectors.
- BRI infrastructure corridor map: transport and digital infrastructure overlaid on ASEAN economic geography.

## Data in Depth Box
- Topic: Cross-validating Chinese provincial GDP with nighttime lights and alternative indicators.
- Dataset(s): China NBS provincial GDP + DMSP-OLS/VIIRS nighttime lights + electricity consumption + tax revenue.
- Replication output: Adjusted provincial GDP estimates using luminosity-based calibration; comparison of official vs. adjusted growth trajectories for coastal and inland provinces.

## Institutional Spotlight
- Institution/person: Bumrungrad International Hospital (Bangkok) as a case study in institutional design for medical tourism — JCI accreditation, dedicated international patient departments, insurance partnerships, and Thai government visa/regulatory facilitation.
- Why included: Illustrates how deliberate institutional coordination between private hospitals, accreditation bodies, and government agencies creates a spatially concentrated services export cluster — a concrete example of Mode 2 services trade geography.

## Applied Lab Linkage
- Relevant lab: Lab 2 (Asia)
- Econometric method: Sequential liberalization and network integration
- Required code artifacts:
  - `labs/lab2_asia/code/hukou_migration_panel.py` (planned)
  - `labs/lab2_asia/code/bri_connectivity_index.py` (planned)
  - `labs/lab2_asia/code/nightlights_gdp_validation.py` (planned)

## Open Questions/Risks
- Chinese sub-national data quality remains a fundamental constraint; nighttime-lights cross-validation helps but is imperfect.
- ASEAN regulatory data is unevenly available and frequently outdated; NTB inventories require manual coding.
- BRI project-level data is improving (AidData) but coverage gaps remain, especially for digital infrastructure.
- Medical tourism statistics are notoriously inconsistent across source agencies (UNWTO vs. national tourism boards vs. hospital self-reports).
- Climate adaptation section requires careful handling of uncertainty in sea-level-rise projections and policy response timelines.
