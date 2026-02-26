# Chapter Spec: Ch.6 - The Flying Geese and East Asia's Tech Ascendancy

## Metadata
- Part: Part III-A - East Asia and ASEAN
- Target word count: 10,500
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-04-12

## Core Thesis
East Asia's technology upgrading is not an automatic flying-geese sequence; it is institutionally engineered. Regions with stronger state-coordination capacity (directed credit, mission-oriented R&D, and science-park governance) move to higher domestic value-added positions in electronics value chains faster than similarly exposed regions. The semiconductor industry is the canonical case: Korea and Taiwan's ascent from assembly to frontier fabrication illustrates how "windows of opportunity" opened by technological paradigm shifts are seized only where institutional coordination is in place. Today, the geopolitics of semiconductor supply chains — export controls, fab subsidies, and cross-strait interdependence — make the spatial economics of chip fabrication a first-order policy question.

## Key Arguments (3-5)
1. The original flying-geese pattern persists only where institutions coordinate capability accumulation.
2. Science-park governance quality shapes innovation productivity beyond simple cluster size effects.
3. Upgrading depends on moving from assembly to design/process control, measurable through domestic value-added shares.
4. Network centrality in MRIO tables mediates how policy support translates into upgrading outcomes.
5. Demographic aging alters labor-cost dynamics, increasing incentives for automation-intensive spatial concentration. Japan's non-tradable services sector illustrates Baumol's "cost disease" (2012) as a spatial force — low-productivity personal services in aging regions absorb fiscal resources while generating limited agglomeration returns.
6. **Windows of Opportunity (moved from Ch 2).** Korea and Taiwan's semiconductor clusters are the canonical example of how technological paradigm shifts create windows that latecomer regions can exploit — but only when institutional coordination (directed credit, IP policy, talent pipelines) is present. The transition from memory chips to logic/foundry illustrates successive windows: DRAM (Korea), foundry (Taiwan/TSMC), and the emerging contest over advanced packaging and EUV lithography.
7. **Weaponized Interdependence.** The spatial economics of semiconductor sanctions and the severing of cross-strait supply chains. US export controls on advanced chip equipment to China, TSMC's geographic concentration risk in Taiwan, and the CHIPS Act/EU Chips Act subsidy race represent a new regime where security considerations reshape the economic geography of high-tech production. The concept of "weaponized interdependence" (Farrell & Newman 2019) explains how chokepoints in global production networks become instruments of geopolitical leverage.

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
- SIA (Semiconductor Industry Association) and SEMI data on global fab capacity and equipment flows.

## Anchor References (2-3)
1. Amsden (1989), *Asia's Next Giant*.
2. Wade (1990), *Governing the Market*.
3. Baldwin and Okubo (2019), GVC/network restructuring literature.
4. Farrell & Newman (2019), "Weaponized Interdependence: How Global Economic Networks Shape State Coercion," *International Security* — theoretical framework for chokepoint leverage in semiconductor supply chains.

## Figures/Maps Needed
- East Asia electronics value-chain network graph (hub-spoke vs multi-hub evolution).
- Timeline figure: policy regime shifts and technology-upgrading milestones.
- Domestic value-added share trajectories by economy/region.
- Semiconductor supply chain map: geographic concentration of fab capacity (Taiwan, Korea, Japan) with chokepoint annotations (EUV lithography equipment, advanced packaging).
- Windows of opportunity timeline: successive technological paradigm shifts and latecomer entry points (DRAM, foundry, advanced packaging).

## Spatial Data Challenge
- Japan's detailed regional GDP accounts (prefectural SNA) contrast sharply with China's provincial statistics, where GDP figures are widely suspected of manipulation (the sum of provincial GDPs routinely exceeds the national total). Researchers must navigate this asymmetry: Japan offers granular, reliable sub-national data suitable for panel econometrics, while China requires cross-validation against alternative indicators (nighttime lights, electricity consumption, tax revenue) to assess regional economic performance credibly.

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

