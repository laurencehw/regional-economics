# The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods

**Target Length:** 650–800 pages
**Target Audience:** Advanced Undergraduates, Master's, and Early PhD students in Economics, Public Policy, and Economic Geography.

**Animating Vision:** This textbook bridges classical economic geography and modern causal inference, anchored in intangibles and the service economy. It rejects purely descriptive accounts in favor of rigorous spatial econometrics, institutional analysis, and applied causal inference to explain why certain regions diverge, integrate, or stagnate. A cross-cutting theme is the growing importance of services trade and the spatial paradox of intangibility — why services cluster in expensive cities despite near-zero digital transmission costs, how regulatory heterogeneity creates invisible borders in the service economy, and how the "servicification" of manufacturing blurs the boundary between goods and services trade. Every regional section pairs substantive expertise with a hands-on Applied Lab, bringing students from passive readers to active empirical researchers.

---

## Preface & Front Matter

### Pathways Through This Book

To prevent syllabus bloat, the preface includes a visual Dependency Diagram (DAG) and 5 curated tracks:

1. **Spatial Econometrics Track:** Ch 1, 3-A, 3-B → All Labs → Ch 16. Regional chapters used as case-study readings.
2. **International Trade in Services Track:** Ch 1, 2, 3-B → Services threads in Ch 4, 7, 8, 9, 14 → Lab 7 → Ch 16.
3. **Development Economics Track:** Ch 1, 2 → Ch 5 (LatAm), Ch 8 (South Asia), Parts VI & VII (MENA/Africa) → Ch 15–16.
4. **Comparative Regionalism Track:** Ch 1, 2 → Part V (Europe) → Ch 4 (USMCA) → Ch 14 (AfCFTA) → Lab 4 → Ch 16.
5. **Geoeconomics & Industrial Policy:** Ch 1, 2 → Ch 4 (CHIPS) → Ch 6–7 (Asia) → Ch 11 (Sanctions) → Ch 15–16.

Each chapter begins with a one-line "Prerequisites" note (e.g., "This chapter requires Chapter 1 and Section 3-B.5. No prior regional chapters needed.").

---

## Part I: Theoretical and Methodological Foundations

Restructured to reduce front-loading. Heavy institutional theories (path dependency, varieties of capitalism, windows of opportunity) have been distributed to the regional chapters where they come alive. Methods are split by discipline: spatial econometrics (3-A) and trade measurement (3-B).

### Chapter 1: The Micro-Foundations of Space

- **Opening Case Study:** The spatial puzzle of Bangalore vs. Kolkata — why does a global services hub emerge in one Indian city and not another?
- **Classical Roots to NEG:** Von Thünen, Weber, Christaller, Lösch → Krugman's core-periphery model. Centripetal forces (market access, thick labor markets, knowledge spillovers) versus centrifugal forces (congestion, land rents, commuting costs).
- **The Marshallian Trinity of Agglomeration:** Input-sharing, labor-market pooling (matching), and knowledge spillovers as micro-foundations for clustering.
- **Agglomeration vs. Spatial Sorting:** Do cities make workers more productive, or do highly skilled people simply self-select into rich cities? Introduction to worker fixed-effects.
- **Housing Constraints & Spatial Misallocation:** Why doesn't everyone move to Silicon Valley? Hsieh & Moretti on how zoning acts as the ultimate centrifugal force.
- **The Spatial Paradox of Intangibility:** Why services cluster in the most expensive cities despite near-zero digital transmission costs. The economics of "capitalism without capital" (Haskel & Westlake's four S's: scalability, spillovers, sunkenness, synergies) and the persistence of face-to-face contact for tacit knowledge exchange (Storper & Venables 2004).
- **Defining the Spatial Unit:** Functional vs. administrative boundaries. Introduction to Commuting Zones (CZs). Why analysis of "functional regions" (e.g., the Silicon Valley–Hsinchu corridor) often matters more than analysis bounded by national borders.
- **Preview Boxes:** Call-forward boxes in every theory chapter (e.g., "In Chapter 9, we apply these agglomeration principles to EU Cohesion Funds...").

### Chapter 2: The Institutional Toolkit & Services Architecture

Slimmed down. Path dependency, varieties of capitalism, and windows of opportunity moved to regional chapters where they come alive through cases.

- **Institutional Thickness & Related Variety:** Measuring sub-national governance quality; the Product Space (Hidalgo & Hausmann) — why regions diversify into "nearby" industries rather than leaping to unrelated sectors.
- **The Architecture of Services Trade:** How trade agreements actually handle services. The 4 GATS modes, positive vs. negative listing (GATS vs. NAFTA/CPTPP), and Mutual Recognition Agreements (MRAs) for professional services. The distinction between market access and national treatment commitments.
- **Regulatory Heterogeneity as a Services Trade Barrier:** Why institutional barriers — professional licensing, data localization, divergent regulatory standards — matter more for services trade than tariffs. The OECD STRI and World Bank STRI as tools for measuring invisible borders (Borchert, Gootiiz & Mattoo 2014). The EU Services Directive as a case study in incomplete liberalization.

### Chapter 3-A: Spatial Econometrics & Inequality Measurement

- **Measuring Spatial Inequality:** Formal definitions of unconditional/conditional β-convergence, σ-convergence, Theil indices, and spatial Gini coefficients. The Williamson hypothesis (inverted-U of regional inequality over development).
- **From OLS to Spatial Regressions:** Why ordinary regression fails when observations are spatially dependent. The Spatial Autoregressive (SAR) model, Spatial Error Model (SEM), and Spatial Durbin Model (SDM).
- **The Spatial Weight Matrix ($W$):** Construction methods — contiguity, distance-decay, k-nearest neighbors, and trade-flow weights. The consequences of $W$-specification for inference.
- **Endogeneity and the Reflection Problem:** Manski's identification challenge — separating endogenous, exogenous, and correlated effects in spatial models.
- **The Modifiable Areal Unit Problem (MAUP):** The statistical danger of drawing arbitrary geographic boundaries and how it affects inference.
- **Spatial Causal Inference & The Bartik Instrument:** Spatial Regression Discontinuity Design (RDD), Synthetic Control Methods, difference-in-differences with spatial spillovers, and using the Shift-Share (Bartik) instrument to evaluate localized trade shocks.
- **Quantitative Spatial Models (QSMs):** A conceptual introduction to structural general equilibrium counterfactuals.
- **Data in Depth Box:** Computing σ-convergence for EU NUTS-2 regions and Chinese provinces using the same code template, illustrating how the same measure reveals very different convergence patterns.

### Chapter 3-B: Trade Measurement and the Gravity Model

- **The Gravity Model Consolidated:** Structural gravity (Anderson & van Wincoop 2003), PPML estimators (Santos Silva & Tenreyro 2006), and the counterintuitive reality of distance elasticities for services (Kimura & Lee 2006; Head, Mayer & Ries 2009). All regional chapters cross-reference this treatment.
- **Measuring the Intangible:** Task trading (Grossman & Rossi-Hansberg 2008), the four GATS modes (BOP-based), the gap in Mode 3 data, and OECD TiVA for capturing "servicification." Data sources: WTO BOP-based services statistics, OECD TiVA, OECD STRI, ECIPE Digital Trade Estimates.
- **Running Gravity Results Table:** A canonical estimates table that first appears here and is reprinted/extended in Lab 7 when students add their own estimates. Cross-regional comparison of distance elasticities for services vs. goods as a throughline.
- **Data Sources and Reproducibility:** Orientation to key datasets (World Bank WDI, IMF, Penn World Tables, WIOD, Afrobarometer, VIIRS night-lights, enterprise surveys) and reproducible workflows in R/Python.

---

## Regional Pedagogical Features (Applied to Parts II through VIII)

- **Regional Diagnostics Dashboard:** A standardized 1-page visual opening each Part: convergence plots (β/σ), sub-national services GDP map, spatial Gini, night-lights composite, and top 5 GATS exports. Consistent color scheme and cartographic projection across all regional maps.
- **Spatial Data Challenge Box:** A 1-page feature in each chapter highlighting what data is missing or distorted in that specific region.
- **Climate Exposure:** Integrated into every regional Part rather than saved for the end.
- **Convergence Diagnostic:** A standardized figure or table in each regional chapter showing β-convergence and σ-convergence for that region's sub-national units over the most recent available period.

---

## Part II: The Americas — Agglomeration, Geoeconomics, and Traps

**Core Theme:** Supply chain security, extreme intra-regional spatial inequality, the tension between the integrated North American high-tech corridor and the institutional barriers facing Latin America. The Americas illustrate the full spectrum of services geography — from APS networks of New York, Toronto, and Mexico City to the digital labor platforms connecting Latin American freelancers to US clients.

### Chapter 4: North America — Resilience and Discontent

- **Geoeconomics:** USMCA friend-shoring, CHIPS Act semiconductor regionalism, and CFIUS.
- **Applying Gravity:** Using Ch 3-B's framework to calculate the "shadow costs" of the US–Mexico border — deploy as an applied tool, not re-derive.
- **International Education (Mode 2):** US university towns as massive service export clusters with deep local multipliers. Bound, Braga, Khanna & Turner (2021) on the globalization of postsecondary education. Spatial concentration of international students in specific metro areas.
- **Services Trade and the APS Geography:** The US as the world's largest services exporter. USMCA's digital trade and financial services provisions. The local multiplier (Moretti 2010). The post-pandemic remote work shock (Delventhal, Kwon & Parkhomenko 2022).
- **The Geography of Discontent:** The Rust Belt paradox — how local trade shocks (measured via Bartik instruments) translate into spatial inequality and populist political realignments.
- **Climate:** IRA green subsidies, CBAM implications for USMCA, and stranded Appalachian coal regions.
- **Spatial Data Challenge:** The Mode 3 FDI measurement gap — BEA surveys capture US MNE foreign affiliates but miss foreign affiliates operating in the US. Mismatch between BLS occupational categories and actual task content for "remoteability" estimates.

### Chapter 5: Latin America and the Middle-Income Trap

- **Path Dependency (from Ch 2):** Historical colonial, industrial, and political legacies constraining modern economic choices — and when "windows of opportunity" allow escape.
- **Commodity Dependence:** The "Resource Curse" in the 21st century — lithium (Andean Triangle), oil (Venezuela, Ecuador).
- **Tourism as Spatial Strategy (Mode 2):** Mexico's coastline and the Caribbean. Clean causal identification of tourism's local agglomeration impacts (Faber & Gaubert 2019). Airbnb's impact on hotel revenues and local housing markets (Zervas, Proserpio & Byers 2017).
- **Premature Deindustrialization:** Informal services vs. productive digital labor platforms (Montevideo, Guadalajara, Medellín). Platform-mediated digital labor (Graham, Hjorth & Lehdonvirta 2017) as a new form of service-sector integration.
- **Climate:** Green commodity frontiers (Andean lithium) and Central American climate migration as a spatial force.
- **The Institutional Gap:** Why institutional quality varies so dramatically between North and Latin America despite overlapping resource endowments.
- **Spatial Data Challenge:** Undercounting informal cross-border trade — ECLAC estimates 40–60% of Andean cross-border trade is informal and unrecorded. Measuring "premature deindustrialization" when the services sector includes everything from fintech to street vending.

### Applied Lab 1: Spatial Lag Models & Border Frictions

- **Method:** Building the Spatial Weight Matrix ($W$) using trade-flow weights. The Spatial Lag model.
- **Application:** Calculating the "shadow costs" of border security and regulatory friction between the US and Mexico.
- **Extension:** Bartik instrument — using the Shift-Share instrument to evaluate localized trade shocks.
- **Chokepoint Mapping:** Analyzing the Panama Canal as a vital trade node; case studies on the Canamex Corridor and NASCO Network.

---

## Part III-A: East Asia and ASEAN

**Core Theme:** Structural transformation via developmental-state industrial policy, semiconductor geopolitics, demographic aging, and platform economies. East Asia demonstrates the "flying geese" model of sequential manufacturing upgrading and its 21st-century extension into weaponized interdependence.

### Chapter 6: East Asia's Tech Ascendancy

- **Windows of Opportunity (from Ch 2):** How developmental states seize narrow windows — Korea/Taiwan semiconductor clusters as the canonical example.
- **The Flying Geese Model and Its Evolution:** From Japan's post-war industrial leadership to a multi-polar regional tech hub.
- **The East Asian Miracle 2.0:** Korea and Taiwan — spatial clustering policy transitioning from manufacturing to R&D-led semiconductor monopolies. The spatial economics of science parks (Hsinchu, Pangyo, Tsukuba).
- **Weaponized Interdependence:** The spatial economics of semiconductor sanctions and the severing of cross-strait supply chains.
- **Demographics:** Japan/Korea aging, Baumol's cost disease in non-tradable services as a spatial force driving automation and regional fiscal stress.
- **Spatial Data Challenge:** Japan's detailed regional GDP data availability vs. China's provincial-level statistical manipulation concerns.

### Chapter 7: China's Divergence and ASEAN Fragmentation

- **China's "Great Divergence":** Coastal SEZs versus inland provinces — the spatial consequences of sequential liberalization.
- **The Hukou System:** Administrative restrictions on spatial labor mobility creating persistent regional inequality.
- **Medical Tourism (Mode 2):** Thailand (Bumrungrad International) and Singapore as case studies in service clustering and regulatory arbitrage. The spatial economics of the Bangkok medical tourism corridor, digital intermediation through medical tourism platforms.
- **ASEAN Platforms:** Grab/Gojek reorganizing urban labor markets across borders.
- **The Belt and Road as Spatial Policy:** Chinese infrastructure investment reshaping connectivity and dependency.
- **The Digital Silk Road and Platform Geopolitics:** Alibaba, TikTok, Huawei Cloud vs. Western competitors creating competing digital service infrastructures. Data localization and digital sovereignty as new trade barriers (Ferracane 2017).
- **Climate:** Managed retreat in the Mekong Delta and Pearl River Delta; China's renewable energy industrial policy as spatial policy.
- **Spatial Data Challenge:** The Hukou distortion hiding ~300M internal migrants from official population registers.

### Applied Lab 2: Multi-Regional Input-Output (MRIO) & GVC Servicification

- **Method:** Multi-Regional Input-Output (MRIO) tables.
- **Application:** Using WIOD to map Global Value Chains across Asia, calculating domestic value-added (TiVA) of electronics manufacturing in each node.
- **Services Extension:** Using TiVA to decompose the service content embedded in manufacturing exports — the "servicification" share.
- **Extension:** Network centrality metrics — identifying "hubs" versus "spokes" in Asian production networks.

---

## Part III-B: South Asia — Services, Demographics, and Leapfrogging

**Core Theme:** India's IT services revolution as the world's most dramatic services trade success story, with spatial dynamics analytically distinct from East Asian developmental-state manufacturing. The demographic dividend, brain circulation, and the contrast between services-led and manufacturing-led growth paths.

### Chapter 8: India and the Geography of IT Services

- **The South Asian Services Track:** Bangalore, Hyderabad, Pune, Chennai as globally integrated services export hubs. STPI policy, SEZ scaffolding, and the BPO-to-KPO smile curve. Language advantage and time-zone arbitrage (Dossani & Kenney 2007). Grossman & Rossi-Hansberg (2008) task-trading framework applied to Indian IT services.
- **Brain Circulation (Mode 2):** India as both a massive source of international students and an emerging destination (IITs, ISB). The brain drain vs. brain circulation debate with explicit spatial dimensions.
- **Telemedicine Leapfrogging:** Apollo Telemedicine and eSanjeevani addressing rural-urban spatial healthcare gaps via Mode 1 services. India's telemedicine expansion as a case of leapfrogging in health services delivery.
- **Contrasts:** Bangladesh's garment GVCs as a comparator to India's services track; SAARC failures; Sri Lanka's debt crisis as a cautionary tale for services-without-institutions.
- **Demographic Dividend:** The opposite spatial force from East Asian aging — youth bulge as opportunity vs. challenge.
- **Spatial Data Challenge:** India's delayed and contested GDP methodology revisions. Measuring IT-BPO exports at the state level (RBI data vs. NASSCOM industry estimates vs. STPI zone-level data). The "missing middle" in firm-level data.

### Applied Lab 3: Mapping IT-BPO Exports

- **Method:** State-level services trade mapping using RBI/KLEMS data.
- **Application:** Mapping the spatial distribution of IT-BPO exports across Indian states. Comparing concentration indices across service sub-sectors (BPO, KPO, fintech).
- **Extension:** Constructing a services-sector "smile curve" for India — plotting value-added per worker against skill intensity for different service tiers across cities.

---

## Part IV: Europe — Integration and the Core-Periphery

**Core Theme:** Supranational integration, smart specialization, and the limits of policy-driven convergence. Europe provides the most ambitious experiment in services trade liberalization (the Single Market's "four freedoms") — and also the most instructive failures.

### Chapter 9: The Single Market and the Convergence Machine

- **Varieties of Capitalism (from Ch 2):** Hall & Soskice applied to sub-national economic governance — liberal vs. coordinated market economies and how they generate distinct spatial patterns.
- **The Economics of EU Structural and Cohesion Funds:** Does top-down spatial redistribution create β-convergence, or does it generate "agglomeration shadows"?
- **The "People vs. Places" Debate:** Does the EU subsidize agglomeration shadows? The Glaeser vs. Kline/Moretti debate applied to Cohesion Funds.
- **Smart Specialization Strategies (S3):** The EU's attempt to tailor regional industrial policy — successes, failures, and "me-too" risk.
- **Education Integration:** The Bologna Process and Erasmus as a massive Mutual Recognition Agreement (MRA) for human capital — the harmonization of higher education as intra-European services integration.
- **The Unfinished Services Market:** The limits of the 2006 Services Directive. The Digital Single Market Strategy and GDPR. London as Europe's APS command center (Faulconbridge 2008).
- **Spatial Data Challenge:** NUTS-2 boundary changes over time — the "changing geography" problem for panel studies. Measuring regulatory barriers that exist in practice but not in law.

### Chapter 10: The North-South Divide and Dis-Integration

- **The Eurozone Crisis:** Institutional mismatches between Germany/Benelux and Mediterranean periphery. Real exchange rate divergence, current account imbalances, and the absence of fiscal union.
- **Post-Socialist Integration:** Visegrád manufacturing ("Factory Germany") vs. CEE nearshore business services hubs (Warsaw, Bucharest, Prague, Budapest) — shared services centers, IT outsourcing, financial back-offices as a distinct services-track integration.
- **Brexit & The Geography of Discontent:** Dis-integration as a natural experiment in severing APS networks. How "left-behind" regions destroy trade frameworks. Relocation of clearing, trading, and advisory functions from London to Dublin, Frankfurt, Amsterdam, Paris.

### Applied Lab 4: Spatial RDD (Evaluating EU Cohesion Funds)

- **Method:** Spatial Regression Discontinuity Design (Spatial RDD).
- **Application:** Using NUTS-2 regional data to evaluate the causal impact of EU Cohesion Funds on GDP growth for regions just inside versus just outside the eligibility border.
- **Extension:** Difference-in-differences with spatial spillovers — do treated regions grow at the expense of untreated neighbors?

---

## Part V: MENA — Rentier States and Fragile Geographies

**Core Theme:** Resource economics, spatial Dutch Disease, conflict spillovers, and the challenge of engineering diversification from above.

### Chapter 11: Post-Carbon Transition and Sovereign Wealth

- **Rentier State Theory and the Resource Curse:** Why resource abundance weakens the institutional feedback loop between taxation, representation, and public goods provision.
- **State-Led Mega-Projects:** "Vision 2030"–style programs as attempts to artificially engineer agglomeration — NEOM, KAEC, Masdar City.
- **Sovereign Wealth as Regional Strategy:** How Gulf SWFs (PIF, ADIA, Mubadala) function as instruments of spatial economic policy.
- **Comparative Sidebar — Australia:** "Resource Boom Without the Curse" — comparing Gulf SWFs with Australian institutional frameworks (Future Fund, mining tax debate, strong pre-existing institutions).
- **Tourism & Connectivity:** Dubai's state-engineered tourism/aviation agglomeration (Emirates as spatial policy tool) vs. Istanbul's organic medical/cosmetic tourism cluster.
- **The Gulf as Global Services Hub:** Aviation, logistics, financial services (DIFC, QFC), cloud infrastructure (AWS, Oracle data centers), and medical tourism.
- **Climate:** Extreme water scarcity and the "green hydrogen" spatial gambit.
- **Spatial Data Challenge:** The opacity of SWF investment data (PIF, ADIA). GDP data quality in conflict zones — when does a national statistical office stop functioning?

### Chapter 12: Fragile States and Conflict Economics

- **The Collapse of Institutional Thickness:** How civil conflict destroys the institutional fabric necessary for regional trade.
- **Conflict as Spatial Shock:** Institutional collapse, refugee flows, and redrawing functional borders. Diaspora remittances as economic lifelines.
- **Human Capital and the Youth Bulge:** Spatial mismatches between education, labor demand, and economic opportunity.
- **Climate–Conflict Nexus:** Water scarcity, agricultural collapse, and climate-induced displacement.
- **Spatial Data Challenge:** GDP data quality in conflict zones — when does a statistical office stop functioning?

### Applied Lab 5: Synthetic Control Method (Counterfactual GDP)

- **Method:** Synthetic Control Method (SCM).
- **Application:** Estimating the counterfactual GDP trajectory of a conflict-affected state (Syria, Libya, Yemen) had the conflict not occurred.
- **Extension:** Event-study designs for measuring the spatial diffusion of conflict shocks to neighboring economies.

---

## Part VI: Sub-Saharan Africa — Demographics and New Structuralism

**Core Theme:** Data scarcity, informal institutions, urbanization without industrialization, and the potential of continental integration.

### Chapter 13: Urbanization Without Industrialization

- **The African Anomaly:** Congestion vs. agglomeration in Lagos, Kinshasa, Dar es Salaam — the absence of the traditional agriculture-to-manufacturing transition.
- **Leapfrogging:** M-Pesa (Suri & Jack 2016), digital hubs (Nairobi, Lagos, Kigali), and productive services without manufacturing — is the "services = low productivity" narrative too simple?
- **Agglomeration vs. Congestion:** Marshallian trinity (sharing, matching, learning) vs. "consumption cities" and "poverty traps" due to infrastructure deficits.
- **The Urban-Rural Productivity Gap:** Africa's central spatial challenge — a gap far wider than the analogous European core-periphery wage gap.
- **Climate:** The shifting Sahel agricultural belt and the climate-conflict nexus.
- **Spatial Data Challenge:** The famous "GDP revision" problem (Nigeria's 2014 rebasing doubled measured GDP overnight). Night-lights as proxy — when it works and when it doesn't. The absence of firm-level census data.

### Chapter 14: The AfCFTA and Functional Corridors

- **Continental Integration:** The AfCFTA Protocol on Trade in Services — covering business services, communications, finance, tourism, and transport — as potentially more transformative than goods liberalization.
- **Eco-Tourism Corridors:** The spatial economics of multi-country safari ecosystems (Serengeti-Mara ecosystem, Victoria Falls) as functional economic regions crossing national borders.
- **The Border Effect in African Trade:** Why it remains ~3× more expensive to move a container between African neighbors than between Africa and Europe.
- **Informal Cross-Border Trade (ICBT):** Recognizing non-state institutional frameworks with their own enforcement mechanisms.
- **Regional Hegemons as Growth Poles:** South Africa (SADC), Nigeria (ECOWAS), Kenya (EAC).
- **Functional Corridors:** The Northern Corridor (Kenya–Uganda–Rwanda) — how digital customs clearing had a larger impact than a 10% tariff reduction.

### Applied Lab 6: Raster Data & Spatial Autocorrelation

- **Method:** Raster data analysis and spatial autocorrelation (Moran's $I$).
- **Application:** Using VIIRS satellite night-lights data to proxy economic activity and measure cross-border spatial spillovers. Integration of SafeGraph high-frequency mobility data alongside night-lights to proxy cross-border spillovers.
- **Extension:** GDP nowcasting workflows; mapping the "Product Space" for SADC countries to identify nearby upgrading paths.

---

## Part VII: Global Synthesis

### Chapter 15: Climate, Stranded Regions, and the Future Map

Repurposed from a standalone climate introduction to a true capstone synthesis. Regional climate subsections now provide the empirical foundation; this chapter provides the cross-regional framework.

- **Spatial Reallocation:** Formal modeling of climate-induced capital/labor shifts across regions.
- **Comparative Sidebar — Pacific Islands:** SIDS as extreme cases of managed retreat and remittance-dependency. Where managed retreat means emigration, and remittances become the primary economic link to the former homeland.
- **Stranded Regions:** Cross-regional comparisons of adaptive capacity — which regions are most exposed? Where does adaptive capacity come from?
- **Green Industrial Policy as Spatial Policy:** Carbon border adjustments (CBAM), green subsidies (IRA), and their effects on regional comparative advantage.
- **Global Comparative Spread:** A 2-page visual compiling all regional diagnostics into a single comparative spread.

### Chapter 16: The Future of Global Regionalism & Services Trade

- **The Telemigration Hypothesis:** Baldwin's (2019) "globotics upheaval" — freelancers in developing nations performing service-sector work via digital platforms as the next great spatial restructuring. Evidence from remote work adoption (Althoff et al. 2022) and spatial GE models (Delventhal, Kwon & Parkhomenko 2022).
- **Telemedicine:** Expanding on Zeltzer et al. (2023). Does Mode 1 digital delivery reduce or reinforce geographic concentration of specialized care?
- **The Splinternet:** Cloud infrastructure geography, data localization, and US/EU/China digital borders. Three competing digital-regulatory models.
- **Global Comparative Spread:** A master matrix comparing services frameworks across USMCA, EU Single Market, AfCFTA, CPTPP, and RCEP. Columns: listing approach, Mode 1–4 coverage, e-commerce/data provisions, MRAs, dispute settlement.
- **Fortress Blocs vs. Flexible Networks:** Hyper-regionalized friend-shoring blocs or adaptive global value chains?
- **The Discipline's Frontier:** Machine learning for spatial prediction, causal inference with interference, network-based models. The emerging frontier of services trade measurement in a digital economy.

### Applied Lab 7: Gravity of Services (Augmenting Baseline Gravity with STRI Data)

- **Method:** Gravity models of services trade, augmented with OECD STRI and cultural/linguistic proximity measures.
- **Application:** Estimating the "tariff equivalent" of regulatory barriers to cross-border services trade. Decomposing the border effect into regulatory, linguistic, and geographic components (Melitz & Toubal 2014).
- **Servicification Extension:** Using TiVA data, decompose service content in manufacturing exports — connecting to Lab 2's MRIO analysis.
- **Cloud Geography Exercise:** Map global distribution of AWS, Azure, and Google Cloud data center regions; cross-reference with ECIPE data localization scores.
- **Comparative Component:** Compare services trade barriers across two contrasting region-pairs to test whether regional integration agreements reduce regulatory barriers for services as effectively as they reduce tariffs for goods.

---

## Pedagogical Architecture

Each chapter is built around a consistent pedagogical structure that reinforces the book's commitment to interdisciplinary rigor.

### Recurring Chapter Features

1. **"Data in Depth" Boxes:** Guided tutorials on using specific datasets to replicate key empirical results discussed in the text.

2. **"Institutional Spotlight" Sidebars:** Short profiles of regional institutions, policy-makers, or governance experiments — drawing on interviews and primary documents.

3. **"Spatial Data Challenge" Boxes:** A 1-page feature in each regional chapter highlighting what data is missing or distorted in that specific region — teaching students about measurement limitations alongside methodology.

4. **Comparative Maps (GIS Visualizations):** Full-color maps using GIS to visualize spatial inequality *within* regions, not just between countries. Consistent color scheme and cartographic projection across all regional maps.

5. **"Comparative Spotlight" Tables:** Structured cross-regional comparisons at the end of each Part.

6. **"Modern Empirical Questions" Sections:** End-of-chapter questions requiring a blend of econometric technique and political economy reasoning.

7. **Applied Labs (one per regional Part + synthesis):** Self-contained empirical exercises with code templates (R/Python), replication data, and step-by-step instructions. Each lab offers a "Minimum Viable Version" (2–3 hours) and an "Extended Version" (6–10 hours).

### Lab Summary Table

| Lab | Region | Method | Application |
|---|---|---|---|
| Lab 1 | Americas | Spatial Lag Model (SAR), Bartik Instrument | Shadow costs of US–Mexico border friction |
| Lab 2 | East Asia | Multi-Regional Input-Output (MRIO) | Domestic value-added in Asian electronics GVCs; servicification |
| Lab 3 | South Asia | State-level services mapping (RBI/KLEMS) | IT-BPO export geography across Indian states |
| Lab 4 | Europe | Spatial Regression Discontinuity Design | Causal impact of EU Cohesion Funds |
| Lab 5 | MENA | Synthetic Control Method (SCM) | Counterfactual GDP of conflict-affected states |
| Lab 6 | Africa | Night-lights raster data, Moran's $I$, SafeGraph | Cross-border spillovers with alternative data |
| Lab 7 | Cross-regional | Services trade gravity model, STRI | Regulatory barriers to services trade; cloud geography |

---

## Appendices

### Appendix A: Mathematical Foundations
- Matrix notation for spatial models.
- Derivation of the SAR, SEM, and SDM estimators.
- Maximum likelihood vs. GMM estimation for spatial models.

### Appendix B: Data and Software Guide
- Detailed instructions for accessing all datasets referenced in the text.
- Setup guides for R (`spdep`, `spatialreg`, `sf`) and Python (`PySAL`, `geopandas`, `libpysal`).
- Replication repositories and data dictionaries for each Applied Lab.
- Lab technical specifications: estimated time, prerequisite software, data sizes, difficulty level.

### Appendix C: Glossary of Key Terms
- Definitions of all technical terms, institutional acronyms, and spatial econometric notation used throughout the text.

---

## Chapter–Lab–Page Targets

| Component | Target Pages | Notes |
|---|---|---|
| Preface + Pathways | 15–20 | Includes dependency diagram |
| Ch. 1: Micro-Foundations | 35–40 | Core theory + opening case |
| Ch. 2: Institutions (slimmed) | 20–25 | Toolkit only; heavy material distributed |
| Ch. 3-A: Spatial Econometrics | 30–35 | SAR/SEM/SDM + causal inference |
| Ch. 3-B: Trade Measurement | 25–30 | Gravity + GATS modes + TiVA |
| Regional chapters (×12) | 30–40 each | 360–480 pp total |
| Applied Labs (×7) | 10–15 each | 70–105 pp total |
| Ch. 15: Climate Synthesis | 25–30 | Cross-regional, not standalone intro |
| Ch. 16: Future/Synthesis | 30–35 | Telemigration + comparative table |
| Appendices (A–C) | 30–40 | Math + data guide + glossary |
| **TOTAL** | **650–800** | Comparable to Combes/Mayer/Thisse |
