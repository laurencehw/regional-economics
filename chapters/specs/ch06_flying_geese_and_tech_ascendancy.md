# Chapter Spec: Ch.6 - The Flying Geese and East Asia's Tech Ascendancy

## Metadata
- Part: Part III - Asia
- Target word count: 10,500
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-04-12

## Core Thesis
East Asia's technology upgrading is not an automatic flying-geese sequence; it is institutionally engineered. Regions with stronger state-coordination capacity (directed credit, mission-oriented R&D, and science-park governance) move to higher domestic value-added positions in electronics value chains faster than similarly exposed regions.

## Key Arguments (3-5)
1. The original flying-geese pattern persists only where institutions coordinate capability accumulation.
2. Science-park governance quality shapes innovation productivity beyond simple cluster size effects.
3. Upgrading depends on moving from assembly to design/process control, measurable through domestic value-added shares.
4. Network centrality in MRIO tables mediates how policy support translates into upgrading outcomes.
5. Demographic aging alters labor-cost dynamics, increasing incentives for automation-intensive spatial concentration.

## Institutional Variable Operationalization
- Institutional variable: `state_coordination_intensity_rt`.
- Measurement:
  - Public R&D expenditure share in strategic sectors.
  - Policy-bank or directed-credit intensity to high-tech manufacturing.
  - Science-park governance proxy (tenancy composition, incubator/public-lab linkage indicators).
- Spatial interaction term: `state_coordination_intensity_rt × network_centrality_rt` in value-added regressions.

## Required Datasets
- WIOD/MRIO tables for electronics and related sectors.
- OECD STAN/ANBERD and national R&D accounts (Japan, Korea, Taiwan where available).
- TiVA indicators for domestic vs foreign value-added shares.
- WDI and IMF macro controls.
- Patent output proxies (WIPO or national IP office aggregates).

## Anchor References (2-3)
1. Amsden (1989), *Asia's Next Giant*.
2. Wade (1990), *Governing the Market*.
3. Baldwin and Okubo (2019), GVC/network restructuring literature.

## Figures/Maps Needed
- East Asia electronics value-chain network graph (hub-spoke vs multi-hub evolution).
- Timeline figure: policy regime shifts and technology-upgrading milestones.
- Domestic value-added share trajectories by economy/region.

## Data in Depth Box
- Topic: MRIO-based decomposition of domestic value-added in electronics exports.
- Dataset(s): WIOD + TiVA + policy coordination proxies.
- Replication output: Panel model linking coordination intensity and network centrality to upgrading outcomes.

## Institutional Spotlight
- Institution/person: Hsinchu Science Park governance model and Korea's MOTIE/KDB coordination architecture.
- Why included: Illustrates concrete mechanisms of state-market coordination in spatial industrial upgrading.

## Applied Lab Linkage
- Relevant lab: Lab 2 (Asia)
- Econometric method: Developmental state and cluster transitions
- Required code artifacts:
  - `labs/lab2_asia/code/mrio_pipeline.py` (planned)
  - `labs/lab2_asia/code/network_centrality_estimator.py` (planned)

## Open Questions/Risks
- Subnational policy-intensity measures are unevenly available across Asian economies.
- MRIO concordances across versions can alter estimated value-added shares.
- Separating institutional effects from geopolitical demand shifts requires robustness checks.

