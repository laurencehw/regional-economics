# Chapter Spec: Ch.10 - The North-South Divide and Post-Socialist Transitions

## Metadata
- Part: Part IV - Europe
- Target word count: 11,000
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-05-03

## Core Thesis
The Eurozone's institutional architecture — a monetary union without fiscal union — produces systematic real exchange rate divergence between Northern core and Southern periphery that cohesion transfers cannot offset. Post-socialist Central and Eastern European economies exploit this mismatch through dependent-market-economy integration strategies, while Brexit demonstrates that regulatory dis-integration severs advanced producer services networks with spatially concentrated costs.

## Key Arguments (3-5)
1. The Eurozone eliminates nominal exchange rate adjustment while preserving divergent wage-setting and productivity institutions, generating persistent current account imbalances between Northern surplus and Southern deficit economies.
2. The absence of fiscal union means that asymmetric shocks produce pro-cyclical austerity in periphery regions rather than automatic stabilization, deepening spatial inequality during crises.
3. Post-socialist Visegrád economies (Poland, Czechia, Hungary, Slovakia) have integrated into European value chains as "Factory Germany" — dependent market economies whose FDI-driven manufacturing growth is institutionally distinct from both the CME core and the Mediterranean periphery (Nölke & Vliegenthart, 2009).
4. CEE cities (Warsaw, Bucharest, Prague, Budapest) have simultaneously developed as nearshore business process outsourcing and shared services hubs, creating a dual integration pathway where manufacturing and tradable services coexist but serve different spatial logics.
5. Brexit functions as a natural experiment in regulatory dis-integration: the severance of UK-EU advanced producer services networks reveals how institutional frameworks (passporting, mutual recognition, labor mobility) underpin spatial patterns of financial and professional services trade.
6. **The geography of discontent is spatially structured by services access.** Leave-voting areas in the UK exhibited systematically lower access to advanced producer services, higher dependence on non-tradable local services, and weaker connectivity to global city networks. This suggests that dis-integration preferences are endogenous to prior exclusion from the gains of services-led agglomeration (Los et al., 2017).
7. **Financial services relocation after Brexit reveals the stickiness and fragility of APS agglomeration.** The post-referendum migration of euro-clearing, banking licenses, and fund management from London to Frankfurt, Dublin, Amsterdam, and Paris provides a live case study of how regulatory shocks redistribute services employment — but also demonstrates agglomeration persistence, as London retains dominance in many APS sub-sectors despite loss of passporting rights.

## Institutional Variable Operationalization
- Institutional variable: `institutional_mismatch_rt`.
- Measurement:
  - Real effective exchange rate divergence from Eurozone mean (ECB data).
  - Composite index of wage-bargaining coordination and labor market rigidity (OECD/ILO indicators).
  - QoG Regional Dataset government-effectiveness scores at NUTS-2 level.
- Spatial interaction term: `institutional_mismatch_rt × eurozone_membership_rt × W*gdp_growth_rt`.

## Required Datasets
- Eurostat NUTS-2 GDP, employment, productivity, and trade panels.
- QoG Regional Dataset (institutional quality indicators at regional level).
- ECB real effective exchange rate and current account balance series.
- GISCO/NUTS shapefiles (2013 and 2016 vintages for panel consistency).
- ONS regional GVA and trade data (UK, pre- and post-Brexit).
- GaWC APS firm network data for European cities.
- FDI flow data from Eurostat and national central banks (for CEE manufacturing integration).
- OECD STRI scores for financial and professional services (for measuring Brexit regulatory divergence).

## Anchor References (3-5)
1. Baldwin (2006), "The Euro's Trade Effects," *ECB Working Paper Series* — foundational estimate of currency union trade effects with implications for spatial integration.
2. Nölke and Vliegenthart (2009), "Enlarging the Varieties of Capitalism: The Emergence of Dependent Market Economies in East Central Europe," *World Politics* — institutional framework for CEE integration as dependent market economies.
3. Los, McCann, Springford, and Thissen (2017), "The Mismatch Between Local Voting and the Local Economic Consequences of Brexit," *Regional Studies* — spatial analysis of Brexit vote patterns and regional economic exposure.
4. Farole, Goga, and Ionescu-Heroiu (2018), "Rethinking Lagging Regions: Using Cohesion Policy to Deliver on the Potential of Europe's Regions," *World Bank* — EU convergence policy effectiveness and spatial heterogeneity.
5. Becker and Jäger (2012), "From an Economic Crisis to a Sovereign Debt Crisis and Beyond," in *Apeldoorn et al. eds.* — institutional analysis of the Eurozone crisis transmission from banking to sovereign debt across European space.

## Figures/Maps Needed
- Bivariate choropleth map of NUTS-2 regions showing real exchange rate deviation vs. GDP growth (pre- and post-crisis).
- Network diagram of GaWC APS connectivity changes in European cities post-Brexit (London vs. continental rivals).
- Map of CEE manufacturing FDI clusters (automotive, electronics) overlaid with nearshore BPO/shared-services hub locations.
- Event-study plot of financial services employment in London, Frankfurt, Dublin, and Amsterdam around Article 50 notification.
- Current account balance divergence fan chart for Eurozone North vs. South, 1999-2024.

## Spatial Data Challenge
- **Reconciling NUTS-2 boundaries with functional economic geographies across EU enlargement waves.** The EU's NUTS classification is an administrative geography that imperfectly captures functional labor markets and commuting zones, particularly in post-socialist states where administrative boundaries were redesigned during EU accession. Cross-border functional regions (e.g., the Vienna-Bratislava corridor, the Øresund region) are split across national NUTS hierarchies, complicating spatial econometric analysis. Additionally, measuring Brexit's spatial impact requires linking UK ONS geographies (ITL regions, formerly NUTS) with Eurostat NUTS for consistent cross-Channel comparison — a concordance that has degraded since the UK's departure from the Eurostat reporting framework.

## Data in Depth Box
- Topic: Spatial RDD around the Eurozone periphery-core boundary using current account and growth discontinuities.
- Dataset(s): Eurostat NUTS-2 panel + ECB macro series + QoG institutional quality indicators.
- Replication output: Estimated treatment effects of Eurozone membership on periphery growth trajectories, with institutional quality as effect modifier.

## Institutional Spotlight
- Institution/person: The European Stability Mechanism (ESM) and Troika conditionality programs (Greece, Portugal, Ireland).
- Why included: The ESM/Troika interventions represent the starkest institutional response to North-South divergence — demonstrating how the absence of fiscal union forces crisis resolution through conditionality that deepens spatial inequality in the short run while attempting institutional convergence in the long run.

## Applied Lab Linkage
- Relevant lab: Lab 4 (Europe)
- Econometric method: Spatial RDD exploiting Eurozone membership and cohesion eligibility discontinuities; difference-in-differences for Brexit APS relocation
- Required code artifacts:
  - `labs/lab4_europe/code/spatial_rdd_pipeline.py` (planned)
  - `labs/lab4_europe/code/brexit_did_aps_relocation.py` (planned)

## Open Questions/Risks
- Eurozone membership is not randomly assigned; selection into the Euro correlates with institutional quality, complicating causal identification of monetary union effects.
- CEE dependent-market-economy integration may be transitional rather than stable — convergence toward Western wage levels could erode the FDI-attraction model.
- Brexit's APS relocation effects are still unfolding; sufficient post-treatment data for robust event-study designs may not be available until 2026-2027.
- The "geography of discontent" framing risks ecological fallacy — regional-level correlations between services access and Leave voting may not hold at the individual level.
