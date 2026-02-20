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

