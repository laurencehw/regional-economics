# Chapter Spec: Ch.12 - Urbanization Without Industrialization

## Metadata
- Part: Part VI - Sub-Saharan Africa
- Target word count: 10,500
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-05-03

## Core Thesis
Urbanization in Sub-Saharan Africa raises productivity only where municipal service capacity and trade-corridor connectivity convert density into lower transaction costs. Where institutional capacity is weak, density primarily scales congestion and informality, producing limited agglomeration gains.

## Key Arguments (3-5)
1. The region's urban transition is outpacing formal industrial employment growth.
2. Service-capacity constraints (power, transport, permitting, local governance) determine whether density is productive.
3. Informal institutions can sustain exchange, but often at higher variance and lower scale efficiency.
4. Corridor integration mediates whether urban centers become production nodes or consumption hubs.
5. Night-lights and alternative data can recover spatial dynamics where official GDP data are sparse.
6. **Digital financial services challenge the "low-productivity services" narrative.** The M-Pesa revolution (Suri & Jack 2016) demonstrates that Africa's urban service sector is not uniformly unproductive — mobile money has reshaped spatial access to finance, with measurable long-run effects on poverty and gender equity. Nairobi, Lagos, Cape Town, and Kigali are emerging as digital services hubs with genuine agglomeration economies in fintech, BPO, and software development. This complicates the "urbanization without industrialization" thesis: some African cities may be generating productive agglomeration through service-sector clustering that bypasses the manufacturing stage entirely. The question is whether this represents a viable alternative development path or an enclave phenomenon limited to a few cities with sufficient institutional and infrastructure capacity.
7. **E-government and digital public service delivery** (Ganapati & Ravi 2023) create their own spatial patterns — digital identification systems can either reduce or reinforce spatial inequality in access to government services, depending on infrastructure and digital literacy gradients.

## Institutional Variable Operationalization
- Institutional variable: `urban_service_capacity_rt`.
- Measurement:
  - Afrobarometer local-service quality responses (electricity, roads, local government performance).
  - Utility reliability and infrastructure access proxies (WDI/enterprise surveys where available).
  - Municipal revenue capacity proxy where subnational fiscal data exist.
- Spatial interaction term: `urban_service_capacity_rt × light_intensity_neighbors_rt` and corridor-connectivity interactions.

## Required Datasets
- VIIRS night-lights annual composites.
- Afrobarometer geocoded survey modules (service delivery, trust, local institutions).
- WDI urbanization, infrastructure, and labor-structure indicators.
- Corridor shapefiles/transport network data for major trade routes.
- DHS/WorldPop or equivalent gridded population layers for density normalization.

## Anchor References (2-3)
1. Gollin, Jedwab, and Vollrath (2016), urbanization without industrialization.
2. Henderson, Storeygard, and Weil (2012), night-lights as economic proxy.
3. Duranton and Puga (2004), micro-foundations of agglomeration.
4. Suri & Jack (2016), "The Long-Run Poverty and Gender Effects of Mobile Money," *Science* — M-Pesa as a case study in digital financial services reshaping spatial access to finance.
5. Ganapati & Ravi (2023), "Digital Identification and Government Service Delivery" — how digital ID systems reshape spatial access to public services.

## Figures/Maps Needed
- VIIRS-based map of urban growth hotspots and corridor adjacency.
- Plot of density vs productivity proxy by service-capacity tercile.
- Moran's I diagnostic maps showing cross-border spillover clusters.

## Data in Depth Box
- Topic: Estimating urban productivity-congestion gradients with night-lights and service-capacity interactions.
- Dataset(s): VIIRS + Afrobarometer + population grids.
- Replication output: Spatial panel/lag results and Moran's I diagnostics separating productive vs congested urbanization regimes.

## Institutional Spotlight
- Institution/person: Corridor and customs digitization reforms in the Northern Corridor (Kenya-Uganda-Rwanda).
- Why included: Demonstrates how institutional process reform can outperform tariff-only policy in reducing effective trade costs.

## Applied Lab Linkage
- Relevant lab: Lab 5 (Africa)
- Econometric method: Agglomeration vs. congestion in low-capacity systems
- Required code artifacts:
  - `labs/lab5_africa/code/viirs_preprocess_pipeline.py` (planned)
  - `labs/lab5_africa/code/morans_i_spillover_model.py` (planned)

## Open Questions/Risks
- Geocoded governance data availability is uneven across countries and survey waves.
- Night-lights saturation and sensor changes require careful normalization.
- Corridor assignment may be endogenous to anticipated growth, requiring robustness strategies.

