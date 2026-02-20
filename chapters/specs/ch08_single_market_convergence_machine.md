# Chapter Spec: Ch.8 - The Single Market and the Convergence Machine

## Metadata
- Part: Part IV - Europe
- Target word count: 10,500
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-04-19

## Core Thesis
EU cohesion policy promotes convergence only where regional administrative capacity and institutional quality exceed a threshold. In low-capacity regions, transfers can produce weaker productivity effects and stronger out-migration spillovers, limiting net convergence.

## Key Arguments (3-5)
1. Cohesion funding effects are heterogeneous and mediated by local implementation capacity.
2. Smart specialization strategies succeed when aligned with pre-existing capability structures.
3. The four freedoms intensify both opportunity and competitive pressure, creating agglomeration shadows.
4. Border and eligibility discontinuities provide quasi-experimental variation for causal inference.
5. Spillovers across treated and untreated neighbors are central to interpreting regional policy incidence.

## Institutional Variable Operationalization
- Institutional variable: `absorption_capacity_rt`.
- Measurement:
  - Cohesion-fund absorption rate (committed vs disbursed share).
  - QoG regional government-effectiveness indicators.
  - Procurement efficiency proxy (time-to-contract or audit findings where available).
- Spatial interaction term: `absorption_capacity_rt × treatment_rt × W*growth_rt`.

## Required Datasets
- Eurostat NUTS-2 GDP, employment, and productivity panels.
- DG REGIO cohesion allocation and disbursement data.
- QoG Regional Dataset (institutional quality).
- GISCO/NUTS shapefiles for boundary-consistent spatial analysis.
- EU Innovation Scoreboard or patent proxies for specialization outcomes.

## Anchor References (2-3)
1. Becker, Egger, and von Ehrlich (2010), EU structural funds evaluation literature.
2. Rodríguez-Pose and Fratesi (2004), cohesion-policy regional effects.
3. Anselin (1988), *Spatial Econometrics* (for spillover structure).

## Figures/Maps Needed
- Map of cohesion-eligibility cutoffs and treated/untreated border regions.
- Distribution plot of absorption capacity across NUTS-2 regions.
- Event-study chart of post-treatment growth by capacity tercile.

## Data in Depth Box
- Topic: Spatial RDD around cohesion eligibility thresholds.
- Dataset(s): NUTS-2 panel + eligibility rules + QoG indicators.
- Replication output: Treatment effects with and without spatial spillover adjustments.

## Institutional Spotlight
- Institution/person: DG REGIO implementation framework and selected managing authorities.
- Why included: Demonstrates how administrative execution quality translates transfers into (or away from) productivity gains.

## Applied Lab Linkage
- Relevant lab: Lab 3 (Europe)
- Econometric method: Convergence and smart specialization
- Required code artifacts:
  - `labs/lab3_europe/code/spatial_rdd_pipeline.py` (planned)
  - `labs/lab3_europe/code/spillover_did_diagnostics.py` (planned)

## Open Questions/Risks
- NUTS boundary revisions complicate panel consistency over long horizons.
- Funding allocations may be endogenous to unobserved regional political factors.
- Spillover definitions are sensitive to W matrix construction and migration channels.

