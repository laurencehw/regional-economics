# Chapter Spec: Ch.6 - The Flying Geese and East Asia's Tech Ascendancy

## Metadata
- Part: Part III - Asia
- Target word count: 10,500
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-04-12

## Core Thesis
East Asia's technology upgrading is not an automatic flying-geese sequence; it is institutionally engineered. Regions with stronger state-coordination capacity (directed credit, mission-oriented R&D, and science-park governance) move to higher domestic value-added positions in electronics value chains faster than similarly exposed regions. But the "Asian miracle" has a services chapter that the manufacturing narrative often obscures: India's IT services revolution represents an alternative upgrading path — from routine BPO to high-value knowledge process outsourcing — that is spatially concentrated, institutionally shaped, and analytically distinct from the East Asian manufacturing model. The Grossman & Rossi-Hansberg (2008) framework of "trading tasks" provides the theoretical scaffolding for understanding why some service tasks offshore and others do not.

## Key Arguments (3-5)
1. The original flying-geese pattern persists only where institutions coordinate capability accumulation.
2. Science-park governance quality shapes innovation productivity beyond simple cluster size effects.
3. Upgrading depends on moving from assembly to design/process control, measurable through domestic value-added shares.
4. Network centrality in MRIO tables mediates how policy support translates into upgrading outcomes.
5. Demographic aging alters labor-cost dynamics, increasing incentives for automation-intensive spatial concentration. Japan's non-tradable services sector illustrates Baumol's "cost disease" (2012) as a spatial force — low-productivity personal services in aging regions absorb fiscal resources while generating limited agglomeration returns.
6. **India's IT services geography represents a parallel upgrading path to East Asian manufacturing.** The spatial economics of Bangalore, Hyderabad, Pune, and Chennai as globally integrated services export hubs — driven by STPI/SEZ policy, language advantage, time-zone arbitrage, and university-industry linkages (Dossani & Kenney 2007). The "smile curve" of the services value chain applies: upgrading from routine BPO (data entry, call centers) to KPO (analytics, R&D, product design) maps onto spatial concentration, with higher-value work clustering in Tier 1 cities. This is the Grossman & Rossi-Hansberg (2008) "trading tasks" framework in action — offshoring decisions depend on the interaction of communication costs, task routineness, and factor price differences.
7. **The "servicification" of Asian manufacturing blurs the boundary between goods and services trade.** TiVA data reveals that 30–40% of the value-added in Asian electronics exports consists of embedded services (design, logistics, marketing, finance). This has implications for how we measure upgrading: a country's position in services value chains may matter as much as its position in manufacturing value chains.

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
- TiVA indicators for domestic vs foreign value-added shares (including services value-added embedded in manufacturing exports).
- WDI and IMF macro controls.
- Patent output proxies (WIPO or national IP office aggregates).
- WTO BOP-based services trade statistics (for India, Philippines, Singapore IT/BPO exports).
- NASSCOM/RBI data on India's IT-BPO export geography (city-level where available).

## Anchor References (2-3)
1. Amsden (1989), *Asia's Next Giant*.
2. Wade (1990), *Governing the Market*.
3. Baldwin and Okubo (2019), GVC/network restructuring literature.
4. Grossman & Rossi-Hansberg (2008), "Trading Tasks: A Simple Theory of Offshoring," *AER* — foundational framework for understanding which service tasks offshore based on communication costs, routineness, and factor prices.
5. Dossani & Kenney (2007), "The Next Wave of Globalization: Relocating Service Provision to India," *World Development* — spatial economics of India's BPO/IT services revolution.

## Figures/Maps Needed
- East Asia electronics value-chain network graph (hub-spoke vs multi-hub evolution).
- Timeline figure: policy regime shifts and technology-upgrading milestones.
- Domestic value-added share trajectories by economy/region.
- India IT services cluster map: Bangalore, Hyderabad, Pune, Chennai, NCR — showing concentration of STPI/SEZ zones, university linkages, and BPO-to-KPO upgrading trajectory.
- Servicification bar chart: share of service value-added embedded in manufacturing exports for key Asian economies (from TiVA decomposition).

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

