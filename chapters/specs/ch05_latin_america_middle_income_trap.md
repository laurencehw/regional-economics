# Chapter Spec: Ch.5 - Latin America and the Middle-Income Trap

## Metadata
- Part: Part II - Americas
- Target word count: 10,000
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-05-03

## Core Thesis
Latin America's persistent middle-income stagnation is not primarily a trade-access problem but an institutional-fragmentation problem. Sub-national variation in regulatory quality, formalization capacity, and fiscal governance explains why proximity to the world's largest consumer market has not triggered convergence: regions with thicker institutional endowments upgrade into higher-value-added production, while institutionally thin regions cycle between commodity booms and premature deindustrialization.

## Key Arguments (3-5)
1. **Premature deindustrialization is spatially uneven — but the services transition is not uniformly negative.** Manufacturing's share of GDP declined across LAC from the 1980s, but the timing and depth vary dramatically across sub-national regions. Metro areas with stronger regulatory environments and formal labor markets retained manufacturing longer and transitioned into higher-productivity tradable services (IT, BPO, fintech), while secondary cities deindustrialized into low-productivity non-tradable informality. The distinction between productive service-sector upgrading and informal service-sector absorption is the key spatial outcome variable.
2. **The resource curse operates through institutional channels, not commodity prices alone.** Resource-rich sub-national regions (e.g., mining corridors in Chile, Peru, Colombia; oil zones in Venezuela, Ecuador) show weaker institutional diversification not because of Dutch Disease per se, but because rent capture weakens the fiscal bargain that drives public goods provision and regulatory upgrading.
3. **Informality is an institutional equilibrium, not a residual.** Informal economic activity — dominant in LAC's urban peripheries — reflects rational responses to extractive formal institutions (high compliance costs, weak contract enforcement, regressive taxation). Regions that reduce formalization frictions show measurably faster structural upgrading.
4. **Green commodity frontiers (lithium, hydrogen, critical minerals) risk reproducing the resource curse pattern unless paired with institutional upgrading.** The Andean lithium triangle and Southern Cone hydrogen ambitions face the same governance challenges as earlier commodity booms; spatial analysis of prior boom-bust cycles identifies which institutional preconditions distinguish upgrading from enclave extraction.
5. **LAC's institutional gap with North America is sub-national, not just national.** Cross-border institutional gradients (e.g., US-Mexico border regions, Colombian-Ecuadorian corridors) show that convergence occurs at the regional level where institutional quality is locally sufficient, even when national-level indicators remain poor.
6. **Digital labor platforms and BPO create a new services-trade channel for LAC integration.** Platform-mediated digital labor (Upwork, Freelancer, Rappi, MercadoLibre) connects LAC freelancers and service workers to US and European clients, creating a form of "telemigration" (Baldwin 2019) that operates through Mode 1 (cross-border supply). Language proximity (Spanish-speaking US market), time-zone alignment, and lower wage costs create a natural comparative advantage for LAC in nearshore services — but institutional barriers (contract enforcement, payment infrastructure, intellectual property protection) determine which regions capture this opportunity. Medical tourism (Connell 2013) inverts the offshoring logic — consumers moving to the service — with Mexico, Costa Rica, and Colombia emerging as destination clusters. Tourism more broadly operates as the Mode 2 case study for how a tradable service generates non-tradable employment multipliers (Faber & Gaubert 2019).

## Institutional Variable Operationalization
- Institutional variable: `formalization_capacity_rt`.
- Measurement:
  - Sub-national formal employment share (ILO/national labor surveys) as a proxy for regulatory reach and institutional thickness.
  - Sub-national fiscal autonomy index: own-source revenue as a share of total sub-national government revenue (OECD/ECLAC fiscal decentralization data).
  - Ease-of-doing-business sub-national scores where available (World Bank sub-national Doing Business surveys for Mexico, Colombia, Peru).
- Spatial interaction term: `formalization_capacity_rt x manufacturing_share_rt` to test whether institutional quality mediates the relationship between structural composition and growth.

## Required Datasets
- ECLAC CEPALSTAT sub-national GDP and sectoral composition panels (available for Brazil, Mexico, Colombia, Chile, Peru, Argentina).
- ILO ILOSTAT labor market indicators: informal employment share by country (national; sub-national where available from household surveys).
- World Bank WDI: GDP per capita growth, manufacturing value-added share, commodity export concentration (HHI).
- OECD Revenue Statistics for LAC: sub-national fiscal autonomy indicators.
- UN Comtrade: commodity export composition for resource-curse analysis.
- USGS/British Geological Survey: lithium, copper, and critical mineral production and reserve data for green commodity frontier analysis.
- World Bank Sub-national Doing Business (Mexico 2016, Colombia 2017, Peru 2015) for formalization cost gradients.

## Anchor References (2-3)
1. Rodrik (2016), "Premature Deindustrialization," *Journal of Economic Growth* — establishes the empirical pattern and its deviation from the East Asian upgrading path.
2. Perry et al. (2007), *Informality: Exit and Exclusion*, World Bank — the foundational framework treating informality as an institutional equilibrium with both voluntary (exit) and involuntary (exclusion) components.
3. Frankel (2010), "The Natural Resource Curse: A Survey," *NBER Working Paper* — synthesizes channels through which resource abundance undermines institutional quality, with LAC case evidence.
4. Graham, Hjorth & Lehdonvirta (2017), "Digital Labour and Development," *Transfer* — how platform-mediated digital labor in the Global South complicates traditional offshoring narratives.
5. Faber & Gaubert (2019), "Tourism and Economic Development: Evidence from Mexico's Coastline," *AER* — rigorous spatial identification of tourism's local development effects, directly applicable to LAC services geography.

## Figures/Maps Needed
- Sub-national manufacturing share heat map for Brazil and Mexico (2000 vs. 2020) showing spatial patterns of deindustrialization.
- Scatter plot: sub-national formal employment share vs. GDP per capita growth across LAC regions, with regression line and institutional-quality color coding.
- Commodity-dependence map: Andean lithium triangle overlaid with sub-national governance indicators.
- Timeline figure: LAC commodity super-cycle (2003-2014) with annotations of institutional reform attempts vs. resource-rent capture episodes.

## Data in Depth Box
- Topic: Measuring premature deindustrialization at the sub-national level.
- Dataset(s): ECLAC CEPALSTAT sub-national GDP by sector + ILO informal employment shares.
- Replication output: Panel regression of sub-national manufacturing share on income level, institutional quality, and commodity exposure — testing whether LAC regions deindustrialize "earlier" (at lower income) than East Asian comparators, conditional on institutional thickness.

## Institutional Spotlight
- Institution/person: CORFO (Chile's Production Development Corporation) and its evolving mandate from import-substitution vehicle to innovation-ecosystem builder.
- Why included: Illustrates the rare LAC case where a state institution successfully transitioned from commodity-era industrial policy to knowledge-economy cluster support (salmon, wine, solar), demonstrating that institutional upgrading — not just resource endowment — determines whether regions escape the middle-income trap. Provides a direct contrast with enclave-extraction governance models elsewhere in LAC.

## Applied Lab Linkage
- Relevant lab: Lab 1 (Americas)
- Econometric method: Structural upgrading and institutional quality
- Cross-reference: Ch. 4's SAR framework with trade-weighted W can be extended to test whether LAC regions with higher formalization capacity exhibit stronger spatial spillovers from US demand shocks.
- Required code artifacts:
  - `labs/lab1_americas/code/prepare_lab1_inputs.py` (extended with LAC panel data)
  - `labs/lab1_americas/code/lab1_americas_sar_scaffold.py` (reusable for LAC cross-section)

## Open Questions/Risks
- Sub-national data availability is highly uneven across LAC: Brazil and Mexico have rich panels; Central American and Caribbean states have sparse coverage. Chapter must be transparent about which results generalize and which are conditional on data-rich cases.
- The formalization-capacity variable conflates regulatory quality with enforcement intensity; regions with "high formality" may simply have more coercive states rather than better institutions. The chapter should discuss this identification challenge explicitly.
- Green commodity frontier analysis is forward-looking and relies partly on projected production; the chapter should distinguish established empirical patterns from informed extrapolation.
- Separating premature deindustrialization from trade-liberalization effects (1980s-90s structural adjustment) requires careful temporal identification — the chapter should engage Rodrik's critique of import-competition versus technology-driven deindustrialization.
