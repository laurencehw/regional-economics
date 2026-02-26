# Chapter Spec: Ch.8 - India and the Geography of IT Services

## Metadata
- Part: Part III-B - South Asia
- Target word count: 9,000–11,000
- Target pages: 30–40
- Status: Spec drafted
- Owner: Laurence (lead)
- Draft due: 2026-05-30

## Core Thesis
India's IT services revolution represents an alternative upgrading path to East Asian developmental-state manufacturing — from routine BPO to high-value knowledge process outsourcing — that is spatially concentrated, institutionally shaped, and analytically distinct. The spatial dynamics (Bangalore vs. Hyderabad vs. tier-2 cities, STPI/SEZ policy, BPO-to-KPO upgrading, language advantage, time-zone arbitrage) warrant their own chapter rather than a paragraph in an East Asia chapter. India's demographic dividend creates the opposite spatial force from East Asian aging, and the subcontinent's mix of services success, garment-sector GVC integration (Bangladesh), and institutional fragility (Sri Lanka, SAARC failures) demands a dedicated analytical treatment.

## Key Arguments (3-5)
1. **India's IT services geography is a full spatial-economic case study.** Bangalore, Hyderabad, Pune, Chennai as globally integrated nodes; STPI/SEZ policy as institutional scaffolding; the smile curve from BPO to KPO; language advantage and time-zone arbitrage (Dossani & Kenney 2007).
2. **The Grossman & Rossi-Hansberg (2008) task-trading framework explains India's services offshoring pattern.** Offshoring decisions depend on the interaction of communication costs, task routineness, and factor price differences — and India's position in this space is changing as it moves up the value chain.
3. **Brain circulation creates two-way spatial flows.** India is simultaneously a massive source of international students (outbound Mode 2 consumption) and an emerging destination (IITs, ISB). The brain drain vs. brain circulation debate has explicit spatial dimensions.
4. **Telemedicine leapfrogging demonstrates Mode 1 services in action.** Apollo Telemedicine and eSanjeevani address rural-urban spatial healthcare gaps, making India a test case for whether digital delivery reduces or reinforces geographic concentration (connecting to Zeltzer et al. 2023 in Ch. 16).
5. **Bangladesh's garment GVCs provide a manufacturing-track comparator.** The contrast between India's services-led and Bangladesh's manufacturing-led integration illuminates the distinct spatial and institutional requirements of each path. SAARC failures and Sri Lanka's debt crisis illustrate services-without-institutions risks.

## Required Datasets
- RBI state-level services trade data.
- KLEMS India productivity data by sector and state.
- NASSCOM industry reports on IT-BPO export geography (city-level where available).
- STPI zone-level export data.
- WTO BOP-based services trade statistics for India, Bangladesh, Sri Lanka.
- WDI and IMF macro controls.

## Anchor References (2-3)
1. Dossani & Kenney (2007), "The Next Wave of Globalization: Relocating Service Provision to India," *World Development*.
2. Grossman & Rossi-Hansberg (2008), "Trading Tasks: A Simple Theory of Offshoring," *AER*.
3. Bound, Braga, Khanna & Turner (2021), "The Globalization of Postsecondary Education," *JEP* — for brain circulation dimension.

## Figures/Maps Needed
- India IT services cluster map: Bangalore, Hyderabad, Pune, Chennai, NCR — showing STPI/SEZ zones, university linkages, and BPO-to-KPO upgrading.
- Services value chain "smile curve" for India: plotting value-added per worker against skill intensity for BPO/KPO/fintech tiers across cities.
- Comparative chart: India (services-led) vs. Bangladesh (manufacturing-led) export composition trajectories.
- Brain circulation flow diagram: outbound student flows vs. return migration vs. diaspora remittances.

## Data in Depth Box
- Topic: Mapping IT-BPO exports at the state level using RBI/KLEMS data.
- Dataset(s): RBI state-level services exports + KLEMS productivity + STPI zone data.
- Replication output: Concentration indices for IT-BPO exports across Indian states; comparison with manufacturing export concentration.

## Institutional Spotlight
- Institution/person: Software Technology Parks of India (STPI) — how a special-purpose institutional framework scaffolded an entire services export sector.
- Why included: STPI/SEZ policy demonstrates how targeted institutional design can create globally competitive service clusters in a developing-country context, paralleling but differing from East Asian science park models.

## Spatial Data Challenge
- India's delayed and contested GDP methodology revisions.
- Measuring IT-BPO exports at the state level: RBI data vs. NASSCOM industry estimates vs. STPI zone-level data produce different geographies.
- The "missing middle" in firm-level data — large firms are captured by NASSCOM, informal firms by surveys, but mid-sized services firms are systematically undercounted.

## Applied Lab Linkage
- Relevant lab: Lab 3 (South Asia — IT-BPO Mapping)
- Econometric method: State-level services trade mapping and concentration analysis
- Required code artifacts:
  - `labs/lab3_south_asia/code/it_bpo_mapping.py` (planned)
  - `labs/lab3_south_asia/code/smile_curve_analysis.py` (planned)

## Open Questions/Risks
- State-level services trade data from RBI is available at lower frequency and granularity than manufacturing trade data.
- NASSCOM data is industry-reported and may have upward bias.
- The BPO-to-KPO upgrading narrative may oversimplify — some cities are simultaneously doing both.
- Sri Lanka's crisis is fast-moving — careful dating of analysis needed.
