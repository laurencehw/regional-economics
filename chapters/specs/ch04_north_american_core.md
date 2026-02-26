# Chapter Spec: Ch.4 - The North American Core

## Metadata
- Part: Part II - Americas
- Target word count: 10,000
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-04-05

## Core Thesis
Since USMCA implementation and the CHIPS-era policy shift, North American reshoring gains are concentrated in regions with higher regulatory-compliance capacity and border-governance quality. Trade exposure alone does not predict upgrading; the key interaction is between network position and institutional execution. A geoeconomic lens — applying the gravity framework from Ch 3-B ("Applying Gravity") — reveals that border frictions, industrial-policy subsidies, and compliance regimes reshape the effective economic distance between North American regions, while the geography of discontent shows how spatially concentrated trade shocks drive political realignment in left-behind manufacturing corridors.

## Key Arguments (3-5)
1. The NAFTA-to-USMCA transition changed the payoff structure from pure cost minimization to compliance-intensive regional production.
2. Rules-of-origin and labor-value-content provisions create heterogeneous regional adjustment costs tied to local institutional capacity.
3. Border frictions act as variable trade costs that can dampen or amplify spatial spillovers in regional growth.
4. CHIPS and related industrial-policy tools increase regional concentration where supplier ecosystems and implementation capacity already exist, reinforcing internal divergence between superstar metros and left-behind manufacturing regions.
5. Domestic value-added gains are largest where regional policy coordination reduces compliance and logistics uncertainty.
6. North America's services trade — the US is the world's largest services exporter — operates through a distinct regulatory geography: USMCA's digital trade and financial services provisions create a more liberal regime than exists between any other major trading partners, while professional licensing and regulatory divergence still fragment the continental services market.
7. **International Education (Mode 2):** US university towns function as massive service export clusters — international students consuming education on US soil constitute one of the largest Mode 2 trade flows globally. Bound, Braga, Khanna & Turner (2021) document the globalization of postsecondary education and its labor-market consequences; Hausman (2022) shows how university-driven innovation generates measurable local economic growth, making college towns a distinctive spatial unit in the services-trade geography.
8. **The Geography of Discontent:** The Rust Belt paradox — local trade shocks, identified via Bartik instruments, generate persistent spatial inequality that maps onto populist political realignment. Regions that lost manufacturing employment to import competition did not simply adjust through labor mobility; instead, concentrated job losses produced durable declines in local wages, labor-force participation, and institutional capacity, fueling the politics of economic grievance that now shapes trade-policy formation itself.

## Services Trade Dimension

The chapter's goods-focused analysis of USMCA should be complemented by a services trade section covering:

- **USMCA's digital trade provisions** (Chapter 19) as the most advanced digital trade framework in any major trade agreement: prohibition of data localization requirements, customs duty moratorium on digital products, source code protection, and cross-border data flow guarantees. These provisions create a de facto "North American digital single market" that contrasts sharply with the EU's GDPR-based approach and China's data sovereignty model.
- **Advanced Producer Services (APS) networks**: New York, Toronto, Chicago, and Mexico City as command centers in the GaWC global city network (Taylor et al. 2011). The spatial organization of financial services, legal services, and management consulting across the continent — and how USMCA provisions on financial services, temporary entry for business persons, and mutual recognition shape the geography of these networks.
- **Local multiplier effects**: How the concentration of high-skill tradable services (tech, finance, consulting) in superstar metros generates Moretti-style local multipliers in non-tradable services, and how remote work adoption is partially redistributing these multiplier effects to secondary cities and exurban locations (Althoff et al. 2022).
- **Nearshoring of services to Mexico**: Monterrey, Guadalajara, and Mexico City as emerging nearshore technology and BPO hubs for US firms — a services-track integration that operates alongside the manufacturing-track (automotive, electronics) more commonly discussed.

## Climate and Energy Transition
- **IRA green subsidies**: The Inflation Reduction Act's place-based clean energy tax credits (e.g., 48C Advanced Manufacturing, energy community bonus credits) channel green investment toward specific regions, reinforcing or reshaping existing spatial hierarchies of industrial capacity. The geographic targeting of IRA incentives creates a new layer of regional competition within North America.
- **CBAM implications for USMCA**: The EU's Carbon Border Adjustment Mechanism raises the question of whether USMCA partners will need to align carbon-pricing regimes to maintain competitiveness in third markets and avoid carbon leakage — with divergent national approaches (US subsidies vs. potential Canadian carbon pricing) creating intra-continental regulatory friction.
- **Stranded Appalachian coal regions**: Coal-dependent communities in Appalachia and the Interior Basin face compound exposure — declining global coal demand, federal regulatory tightening, and limited institutional capacity for transition — making them the sharpest case of climate-driven regional economic dislocation in North America.

## Institutional Variable Operationalization
- Institutional variable: `compliance_capacity_rt`.
- Measurement:
  - Share of regional exports in USMCA high-compliance product lines (HS mapping).
  - Border-governance proxy from BTS throughput stability and mode-specific crossing composition.
  - State/provincial implementation capacity proxy from public-sector effectiveness indicators where available.
- Spatial interaction term: `compliance_capacity_rt × W*growth_rt` and `compliance_capacity_rt × trade_centrality_rt`.

## Spatial Data Challenge
- **The Mode 3 FDI measurement gap:** BEA data capture US MNE affiliates operating abroad (outward FDI) in detail, but systematic measurement of foreign-owned affiliates operating inside the US (inward FDI) is far less granular at the sub-national level. This asymmetry means that the regional employment and output footprint of foreign direct investment in the US — a core Mode 3 services trade channel — is systematically undermeasured, complicating any spatial analysis of FDI-driven economic integration.
- **Remoteability estimation mismatch:** BLS occupational categories (SOC codes) were designed to classify jobs by industry and function, not by task content or "remoteability." Estimating which occupations can be delivered remotely — and thus which regions are exposed to or benefit from Mode 1 services trade — requires mapping SOC codes to task-content measures (e.g., Dingel & Neiman 2020), introducing measurement uncertainty that compounds at the sub-national level.

## Required Datasets
- UN Comtrade HS6 bilateral trade (US, Canada, Mexico).
- BTS Border Crossing Entry Data (`keg4-3bc2`) by port/mode/date.
- WDI macro controls (growth, inflation, exchange-rate stability proxies).
- BEA regional accounts and BLS QCEW for US subnational output/employment structure.
- USMCA product-rule mapping (annex-derived concordance).
- BEA International Services trade data (bilateral services trade by type).
- OECD STRI scores for US, Canada, Mexico (for services barrier comparison).
- GaWC firm-level APS connectivity data (for global city network analysis).

## Anchor References (2-3)
1. Hanson (2001), "U.S.-Mexico Integration and Regional Economies," *JEP*.
2. Autor, Dorn, and Hanson (2013), "The China Syndrome," *AER* (for trade-shock identification logic).
3. LeSage and Pace (2009), *Introduction to Spatial Econometrics*.
4. Moretti (2010), "Local Multipliers," *AER: P&P* (for services multiplier framework).
5. Taylor, Ni, Derudder et al. (2011), *Global Urban Analysis* (for APS network mapping).
6. Bound, Braga, Khanna & Turner (2021), "The Globalization of Postsecondary Education," *Journal of Economic Perspectives* — documents the scale and spatial concentration of international education as a Mode 2 service export.

## Figures/Maps Needed
- North American manufacturing corridor map (Great Lakes, Texas-Northern Mexico, Quebec-Ontario).
- Border-port heatmap of inbound truck and container crossings.
- Graph of estimated spillover elasticity by compliance-capacity tercile.
- "Applying Gravity" — border effect visualization showing how the Ch 3-B gravity framework maps onto North American trade flows: estimated border effects at US-Canada and US-Mexico borders, illustrating the gap between predicted frictionless trade and observed flows as a measure of effective economic distance.

## Data in Depth Box
- Topic: Building a border-friction index from port-level crossing data.
- Dataset(s): BTS crossings + Comtrade bilateral flows.
- Replication output: SAR estimates of regional growth with alternative W matrices (distance vs trade-weighted) and friction interactions.

## Institutional Spotlight
- Institution/person: USMCA Free Trade Commission and customs coordination bodies (CBP/CBSA/SAT interfaces).
- Why included: Shows how implementation institutions, not treaty text alone, determine realized regional integration.

## Applied Lab Linkage
- Relevant lab: Lab 1 (Americas) — with Bartik extension
- Econometric method: Geoeconomics and border-friction gravity logic; Bartik shift-share instrument for identifying local trade-shock exposure in the geography-of-discontent analysis
- Required code artifacts:
  - `labs/lab1_americas/code/fetch_comtrade_api.py`
  - `labs/lab1_americas/code/prepare_lab1_inputs.py`
  - `labs/lab1_americas/code/lab1_americas_sar_scaffold.py`

## Open Questions/Risks
- Subnational comparability is uneven across US/Canada/Mexico statistical systems.
- Product-level USMCA compliance coding may require manual concordance checks.
- Border-friction measures may proxy both policy and demand shocks; identification strategy must address this.

