# Chapter Spec: Ch.14 - The AfCFTA, Regional Hegemons, and Functional Corridors

## Metadata
- Part: Part VI - Sub-Saharan Africa
- Target word count: 10,000
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-05-17

## Core Thesis
The African Continental Free Trade Area can reduce the continent's extreme border effect only if it is embedded in functional trade corridors with digitized customs, harmonized standards, and effective dispute resolution. Tariff reduction alone is insufficient because Africa's intra-continental trade barriers are primarily institutional (customs delays, non-tariff barriers, informal payments) and infrastructural (transport costs, port congestion, road quality), not tariff-based. Regional hegemons — South Africa, Nigeria, Kenya — structure their sub-regional economies as growth poles, but their institutional spillovers are asymmetric and often extractive rather than developmental.

## Key Arguments (3-5)
1. **Africa's border effect is institutional, not tariff-based.** Intra-African trade is roughly 15% of total African trade — the lowest continental share globally. The binding constraint is not tariffs (already low under existing RECs) but non-tariff barriers: customs delays averaging 5–7 days at major borders, informal payments ("facilitation fees") adding 10–30% to transport costs, and divergent regulatory standards that require separate certification for each national market. The AfCFTA's Protocol on Trade in Goods addresses tariffs; its Protocols on Investment, Competition, and Digital Trade address the institutional barriers — but implementation depends on national institutional capacity that varies enormously.
2. **Informal cross-border trade (ICBT) is an institutional system, not a residual.** In the Great Lakes region (DRC-Rwanda-Uganda-Burundi) and the Sahel (Nigeria-Niger-Cameroon-Chad), ICBT accounts for an estimated 30–70% of cross-border economic exchange. These flows operate through non-state institutional frameworks — ethnic networks, clan-based credit systems, trader associations — that provide contract enforcement, information, and dispute resolution where formal institutions are absent. Policy that criminalizes or ignores ICBT destroys institutional capital without replacing it.
3. **Regional hegemons generate asymmetric spillovers.** South Africa's role in SADC, Nigeria's in ECOWAS, and Kenya's in the EAC create hub-spoke trade structures where the hegemon captures disproportionate gains from regional integration. South African retailers (Shoprite, Pick n Pay) and banks (Standard Bank, FirstRand) dominate regional markets, but backward linkages to local suppliers are weak — replicating the enclave dynamics that Chapter 5 documented for resource extraction in Latin America.
4. **Functional corridors outperform tariff liberalization.** The Northern Corridor (Mombasa–Nairobi–Kampala–Kigali) demonstrates that institutional process reform — single-window customs declarations, electronic cargo tracking, coordinated border management — can reduce effective trade costs by more than any plausible tariff reduction. The Trans-Caprivi Corridor (Walvis Bay–Zambia) and the Maputo Development Corridor (Johannesburg–Maputo) provide further evidence.
5. **Lab 6's spatial autocorrelation analysis connects Chapter 13's urbanization thesis to the trade-corridor question.** If economic activity (night-lights) clusters along trade corridors and dissipates away from them, the corridor — not the city or the country — may be the right unit of analysis for African economic geography. Governance quality (Afrobarometer) conditions whether corridor proximity translates into productive clustering or merely transit-related congestion.
6. **The AfCFTA's Protocol on Trade in Services may be more transformative than goods liberalization.** Services already account for a larger share of African GDP than manufacturing, and the Protocol covers five priority sectors: business services, communications, financial services, tourism, and transport. Given that Africa's border effect operates primarily through institutional and regulatory barriers rather than tariffs, services liberalization — which requires mutual recognition of professional qualifications, regulatory harmonization, and rights of establishment — directly addresses the binding constraints. South African banks and telecoms (MTN, Safaricom/M-Pesa, Standard Bank) already operate as de facto regional services integrators, but their expansion depends on the Protocol's implementation. The services dimension also connects to Chapter 13's digital financial services narrative: mobile money interoperability across borders is a services trade question that the AfCFTA framework can either enable or impede.

## Eco-Tourism Corridors
Spatial economics of multi-country safari ecosystems (Serengeti-Mara, Victoria Falls) as functional economic regions crossing national borders. The Serengeti-Mara ecosystem spans Tanzania and Kenya; Victoria Falls straddles Zambia and Zimbabwe; the Kavango-Zambezi Transfrontier Conservation Area (KAZA) links five countries. These eco-tourism corridors function as cross-border economic regions where the "product" — wildlife migration, landscape, biodiversity — is inherently transnational and non-excludable at the national level. Revenue sharing, visa harmonization (KAZA UniVisa), anti-poaching coordination, and infrastructure investment require institutional cooperation that mirrors the trade-corridor governance challenges analyzed elsewhere in this chapter. The spatial economics differ from goods corridors: tourism revenue concentrates at gateway towns and lodges, creating enclave economies with limited backward linkages unless deliberate community-benefit arrangements (conservancies, community trusts) are institutionalized. The comparison between Kenya's conservancy model and Tanzania's more centralized national-park model illustrates how institutional design shapes the spatial distribution of tourism rents.

## Institutional Variable Operationalization
- Institutional variable: `corridor_governance_index_rt`.
- Measurement:
  - Afrobarometer trust-in-local-government and service-delivery quality responses, aggregated to country-year.
  - Logistics Performance Index (LPI) customs sub-score for formal border-crossing efficiency.
  - UNCTAD Digital and Sustainable Trade Facilitation survey indicators for digital customs, single-window implementation, and transit facilitation.
  - Corridor-specific dwell-time data (TradeMark Africa/TMEA) where available.
- Spatial interaction term: `corridor_governance_index_rt × W*night_lights_rt` to test whether governance quality conditions the spatial clustering of economic activity along trade corridors.

## Required Datasets
- VIIRS night-lights annual composites (same source as Lab 6 / Ch. 13).
- Afrobarometer survey rounds 7–9 (governance, service delivery, cross-border trade perceptions).
- WDI trade openness, infrastructure quality, and governance indicators.
- UN Comtrade bilateral trade flows for intra-African trade analysis.
- UNCTAD Trade Facilitation indicators for AfCFTA member states.
- TradeMark Africa (TMEA) corridor performance data where available (Northern Corridor, Central Corridor, Trans-Kalahari).
- GADM administrative boundary shapefiles for adjacency/border-weight matrix construction.

## Anchor References (2-3)
1. Brenton and Isik (2012), *De-Fragmenting Africa: Deepening Regional Trade Integration in Goods and Services*, World Bank — comprehensive analysis of intra-African trade barriers and corridor economics.
2. Aker, Klein, O'Connell, and Yang (2014), "Borders, Ethnicity, and Trade," *Journal of Development Economics* — documents the role of ethnic networks in cross-border trade in West Africa.
3. Arvis, Raballand, and Marteau (2010), *The Cost of Being Landlocked: Logistics Costs and Supply Chain Reliability*, World Bank — quantifies the transport-cost premium for landlocked African countries and the role of transit corridors.

## Figures/Maps Needed
- Map of major African trade corridors (Northern, Central, Trans-Kalahari, Maputo, Abidjan-Lagos) overlaid with VIIRS night-lights radiance showing corridor-adjacent economic clustering.
- Border-effect comparison chart: cost of shipping a container between African neighbors vs. Africa-to-Europe ($ per TEU).
- Bar chart of ICBT estimated share of total cross-border trade by REC (ECOWAS, EAC, SADC, COMESA).
- Scatter plot: corridor governance index vs. Moran's I for corridor-adjacent regions.

## Data in Depth Box
- Topic: Estimating the "real" border effect in African trade using gravity models with corridor-specific fixed effects.
- Dataset(s): UN Comtrade intra-African bilateral trade + WDI GDP + CEPII distance data + LPI customs scores + UNCTAD facilitation indicators.
- Replication output: Gravity model estimates comparing tariff-equivalent border costs across (a) corridor-connected pairs, (b) non-corridor but contiguous pairs, and (c) non-contiguous pairs. The difference between (a) and (b) measures the corridor-governance dividend.

## Institutional Spotlight
- Institution/person: TradeMark Africa (TMEA) and the Northern Corridor Transit and Transport Coordination Authority (NCTTCA).
- Why included: TMEA's electronic cargo tracking system (ECTS) and the NCTTCA's single customs territory pilot reduced transit times on the Mombasa-Kigali route from 22 days (2010) to 6 days (2023). This is the most documented case of an institutional intervention outperforming tariff liberalization in Africa. The spotlight examines how the reform was designed, what political economy obstacles it faced, and what spatial effects it produced (increased trade volumes, new warehousing investment at border posts, measurable night-lights growth along the corridor).

## Applied Lab Linkage
- Relevant lab: Lab 6 (Africa)
- Econometric method: Spatial autocorrelation (Moran's I) and governance-residualized clustering
- Cross-reference: Lab 6's two-step Moran's I procedure (raw night-lights clustering → governance-residualized clustering) can be extended to test whether corridor proximity conditions the governance effect. If governance quality matters more for economic clustering along corridors than away from them, this supports the functional-corridor thesis.
- Required code artifacts:
  - `labs/lab6_africa/code/prepare_lab6_inputs.py` (existing)
  - `labs/lab6_africa/code/lab6_africa_moran_scaffold.py` (existing)
  - `labs/lab6_africa/code/run_real_africa_specs.py` (planned — robustness runner following Lab 1 pattern)

## Open Questions/Risks
- Intra-African bilateral trade data quality is poor; mirror statistics (exports reported by A vs. imports reported by B) diverge significantly, reflecting customs under-reporting and ICBT.
- ICBT estimation relies on indirect methods (survey-based, border-post observation studies) with large confidence intervals.
- Corridor governance data from TMEA is not publicly available for all corridors; the Northern Corridor has the best coverage, others are sparser.
- Afrobarometer coverage is limited to countries that participate in the survey program; several large economies (DRC, Angola, Sudan) have incomplete or no coverage.
- The AfCFTA is in early implementation (tariff reduction schedules began January 2021); it is too early to measure trade-creation effects econometrically. The chapter should distinguish institutional analysis (what the agreement requires) from impact evaluation (what the agreement has achieved).
