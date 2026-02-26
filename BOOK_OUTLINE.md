# The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods

**Target Audience:** Advanced Undergraduates, Master's, and Early PhD students in Economics, Public Policy, and Economic Geography.

**Animating Vision:** This textbook bridges classical regional geography and modern political economy. It rejects purely descriptive accounts in favor of rigorous spatial econometrics, institutional analysis, and applied causal inference to explain why certain regions diverge, integrate, or stagnate. A cross-cutting theme is the growing importance of services trade and the spatial paradox of intangibility — why services cluster in expensive cities despite near-zero digital transmission costs, how regulatory heterogeneity creates invisible borders in the service economy, and how the "servicification" of manufacturing blurs the boundary between goods and services trade. Every regional section pairs substantive expertise with a hands-on Applied Lab, bringing students from passive readers to active empirical researchers.

---

## Part I: Theoretical and Methodological Foundations

Before exploring specific geographies, this part grounds the student in the formal theories of spatial economics and the modern empirical toolkit. It establishes the analytical "language" used throughout the book.

### Chapter 1: The Micro-Foundations of Space — From Classical to New Economic Geography

- **Classical Roots:** Von Thünen, Weber, Christaller, and Lösch — the origins of location theory.
- **The NEG Revolution:** Krugman's core-periphery model; centripetal forces (market access, thick labor markets, knowledge spillovers) versus centrifugal forces (congestion, land rents, commuting costs).
- **The Marshallian Trinity of Agglomeration:** Input-sharing, labor-market pooling (matching), and knowledge spillovers as micro-foundations for clustering.
- **The Spatial Paradox of Intangibility:** Why services cluster in the most expensive cities despite near-zero digital transmission costs. The economics of "capitalism without capital" (Haskel & Westlake's four S's: scalability, spillovers, sunkenness, synergies) and the persistence of face-to-face contact for tacit knowledge exchange (Storper & Venables 2004).
- **Functional Regions vs. Administrative Boundaries:** Why analysis of "functional regions" (e.g., the Silicon Valley–Hsinchu corridor) often matters more than analysis bounded by national borders.

### Chapter 2: Evolutionary and Institutional Frameworks

- **Institutional Thickness:** Measuring the density and quality of local norms, legal frameworks, regulatory bodies, and "soft" infrastructure at the sub-national level.
- **Path Dependency:** How historical colonial, industrial, and political legacies constrain modern economic choices — and when "windows of opportunity" allow escape.
- **Related Variety and Regional Upgrading:** Why regions diversify into "nearby" industries (Hidalgo & Hausmann's Product Space) rather than leaping to unrelated sectors.
- **Regulatory Heterogeneity as a Services Trade Barrier:** Why institutional barriers — professional licensing, data localization, divergent regulatory standards — matter more for services trade than tariffs. The OECD Services Trade Restrictiveness Index (STRI) and World Bank STRI as tools for measuring invisible borders (Borchert, Gootiiz & Mattoo 2014).
- **Varieties of Capitalism at the Regional Scale:** Applying Hall & Soskice to sub-national economic governance.

### Chapter 3: The Modern Spatial Econometric Toolkit

- **From OLS to Spatial Models:** Why ordinary regression fails when observations are spatially dependent. The Spatial Autoregressive (SAR) model, Spatial Error Model (SEM), and Spatial Durbin Model (SDM).
- **The Spatial Weight Matrix ($W$):** Construction methods — contiguity, distance-decay, k-nearest neighbors, and trade-flow weights. The consequences of $W$-specification for inference.
- **Endogeneity and the Reflection Problem:** Manski's identification challenge — separating endogenous, exogenous, and correlated effects in spatial models.
- **Spatial Causal Inference:** Spatial Regression Discontinuity Design (RDD), Synthetic Control Methods, and difference-in-differences with spatial spillovers, with explicit counterfactual intuition and boundary-discontinuity logic before advanced regional applications.
- **The Gravity Model for Services Trade:** The gravity model — the workhorse of empirical trade economics — produces strikingly different results for services than for goods. Distance elasticities are often *larger* for services (counterintuitively), language and colonial ties matter more, and regulatory barriers captured by the STRI show up differently from tariffs (Kimura & Lee 2006; Head, Mayer & Ries 2009). The chapter introduces the gravity framework here so that regional chapters can deploy it. The Grossman & Rossi-Hansberg (2008) "trading tasks" framework provides the theoretical scaffolding for understanding which service tasks are tradable across borders and which resist offshoring — based on the interaction of communication costs, task routineness, and factor price differences.
- **Measuring Services Trade:** Why standard BOP-based statistics undercount services trade — the four GATS modes (cross-border, consumption abroad, commercial presence, movement of persons), the gap between Mode 1 and Mode 3 estimates, and the OECD TiVA framework for capturing "servicification" (the service content embedded in manufacturing exports). Data sources: WTO BOP-based services statistics, OECD TiVA, OECD STRI, ECIPE Digital Trade Estimates.
- **Data Sources and Reproducibility:** An orientation to key datasets (World Bank WDI, IMF, Penn World Tables, WIOD, Afrobarometer, VIIRS night-lights, enterprise surveys) and reproducible workflows in R/Python.

---

## Part II: The Americas — Agglomeration, Geoeconomics, and Traps

**Core Theme:** Supply chain security, extreme intra-regional spatial inequality, the tension between the integrated North American high-tech corridor and the institutional barriers facing Latin America. The Americas also illustrate the full spectrum of services geography — from the advanced producer services (APS) networks of New York, Toronto, and Mexico City to the digital labor platforms connecting Latin American freelancers to US clients.

### Chapter 4: The North American Core — USMCA and the Geoeconomics of Resilience

- **The Core Thesis:** Integration in North America has shifted from a "least-cost" efficiency model (NAFTA era) to a "value-added and national security" model (USMCA era). The agreement is now an institutional framework for friend-shoring and industrial base protection.
- **Value Chain Circulation:** Analyzing the transformation of North American logistics from simple cost minimization to the science of resilient circulation systems.
- **The Border Effect:** Using gravity models to calculate the "shadow costs" of increased security, regulatory standards, and Rules of Origin at the US–Mexico border.
- **Semiconductor Regionalism:** The CHIPS Act guardrails and how they incentivize a North American microelectronics ecosystem — the industrial economics of supply chain protection.
- **Institutional Levers:**
  - The Defense Production Act (Title III) as a tool for expanding regional capacity in critical materials.
  - CFIUS and FDI screening for "TID businesses" (Technology, Infrastructure, Data) across the continent.
- **The Rust Belt Paradox:** Why the hollowing out of traditional manufacturing persists alongside massive public investment in reshoring, and how that divergence mirrors the rise of superstar metro clusters versus left-behind regions.
- **Services Trade and the APS Geography of North America:** The US as the world's largest services exporter. How USMCA's digital trade and financial services provisions create a distinct regulatory geography. The local multiplier (Moretti 2010): how one high-skill APS job generates multiple local service jobs, and why tech/finance hub openings reshape surrounding service economies. The post-pandemic remote work shock and its spatial redistribution effects (Delventhal, Kwon & Parkhomenko 2022).

### Chapter 5: Latin America and the Middle-Income Trap

- **The Core Thesis:** The "Middle-Income Trap" in Latin America is driven by an inability to structurally upgrade from low- to high-value-added production. Institutional Thickness explains why proximity to the US hasn't triggered convergence.
- **Commodity Dependence:** The "Resource Curse" in the 21st century — why control over lithium (the Andean Triangle) or oil (Venezuela, Ecuador) doesn't automatically produce institutional quality or diversification.
- **Premature Deindustrialization and the Services Question:** The decline of manufacturing as a share of GDP. But not all service transitions are equal — regions with institutional capacity can transition into productive tradable services (BPO, software, fintech) rather than informal non-tradable services. The emerging geography of Latin American digital labor: Montevideo, Buenos Aires, Medellín, and Guadalajara as tech hubs. Platform-mediated digital labor (Graham, Hjorth & Lehdonvirta 2017) as a new form of service-sector integration with global markets.
- **Green Commodity Frontiers:** The Andean lithium economy and Southern Cone hydrogen ambitions — can "green" commodities break the resource curse pattern?
- **Informal Economic Coercion:** How "gray zone" tactics — sudden regulatory shifts, sanitary inspections, export bans — are used to pressure regional neighbors.
- **The Institutional Gap:** Why institutional quality varies so dramatically between North and Latin America despite overlapping resource endowments.

### Applied Lab 1: Modeling Spatial Interaction in the Americas

- **Method:** Building the Spatial Weight Matrix ($W$) using trade-flow weights rather than simple geographic proximity.
- **Model:** The Spatial Lag model: $y = \rho Wy + X\beta + \epsilon$
  - $y$: Regional GDP growth.
  - $\rho$: The spatial autoregressive coefficient (measuring spillover from neighbors).
  - $Wy$: The "spatial lag" of neighboring growth.
- **Application (R/Python):** Calculating the "shadow costs" of border security and regulatory friction between the US and Mexico.
- **Chokepoint Mapping:** Analyzing the Panama Canal as a vital trade node; case studies on the Canamex Corridor and NASCO Network as functional regional units transcending national borders.

### Student Lab: "Friend-Shoring" Simulation

Using Geoeconomic Monitor data, students design a hypothetical "Strategic Reserve" for critical minerals (Lithium/Cobalt) located in the Andean region. They calculate:
- **Transport Mode Choice:** How choosing between rail and sea impacts the optimal location of processing.
- **Regulatory Harmonization:** The impact of adopting European-style standards ("Brussels Effect") versus North American standards on regional export potential.

---

## Part III: Asia — The Developmental State and Networked Value Chains

**Core Theme:** Structural transformation, demographic shifts, multipolar production networks, and the spatial economics of state-directed industrial policy. Asia also hosts the world's most dramatic services trade story — India's IT services revolution — and the platform economies (Alibaba, Grab, Gojek) that are redefining how services are organized, delivered, and traded across borders.

### Chapter 6: The "Flying Geese" and East Asia's Tech Ascendancy

- **The Flying Geese Model and Its Evolution:** From Japan's post-war industrial leadership to a multi-polar regional tech hub.
- **The East Asian Miracle 2.0:** How South Korea and Taiwan used spatial clustering policy to transition from manufacturing to R&D-led semiconductor monopolies.
- **Smart Clustering:** The spatial economics of science parks (Hsinchu, Pangyo, Tsukuba) — why geographic concentration persists in an era of digital connectivity.
- **India's IT Services Geography — The Other Asian Miracle:** The spatial economics of Bangalore, Hyderabad, Pune, and Chennai as globally integrated services export hubs. How state coordination (STPI, SEZ policy), language advantage, and time-zone arbitrage produced a service-sector analogue to East Asia's manufacturing upgrading. The "smile curve" of services value chains: from routine BPO (data entry, call centers) to high-value KPO (analytics, R&D, product design) — and how this upgrading trajectory maps onto spatial concentration (Dossani & Kenney 2007).
- **Demographic Aging as a Spatial Force:** How Japan's and South Korea's demographic transitions reshape regional labor markets, automation incentives, and fiscal geography. Japan's "cost disease" in non-tradable services (Baumol 2012) as a spatial force driving automation and regional fiscal stress.

### Chapter 7: China's Internal Divergence and ASEAN Fragmentation

- **China's "Great Divergence":** Coastal Special Economic Zones (SEZs) versus inland provinces — the spatial consequences of sequential liberalization.
- **The Hukou System:** How administrative restrictions on spatial labor mobility create persistent regional inequality within a single national economy.
- **ASEAN: Unified Bloc or Competing Export Platforms?** The challenge of integrating Southeast Asian economies beyond "China Plus One" strategies. The rise of ASEAN digital services economies — Grab (Singapore), Gojek (Indonesia), and Sea Group as platform-mediated service providers that reorganize urban labor markets across borders.
- **The Belt and Road as Spatial Policy:** How Chinese infrastructure investment reshapes connectivity, dependency, and regional hierarchies across Asia.
- **The Digital Silk Road and Platform Geopolitics:** How Chinese platform companies (Alibaba, TikTok, Huawei Cloud) and their Western competitors create competing digital service infrastructures across Asia, and how data localization laws and digital sovereignty create new trade barriers in the service economy (Ferracane 2017).

### Applied Lab 2: Network Econometrics and Global Value Chains

- **Method:** Multi-Regional Input-Output (MRIO) tables.
- **Application:** Using the World Input-Output Database (WIOD) to map Global Value Chains across Asia, calculating the actual domestic value-added (TiVA) of electronics manufacturing in each node.
- **Services Extension:** Using TiVA to decompose the service content embedded in manufacturing exports — the "servicification" share. How large is the services value-added in a Korean semiconductor or a Japanese automobile, and where is that service value created?
- **Extension:** Network centrality metrics — identifying which regional economies are "hubs" versus "spokes" in Asian production networks.

---

## Part IV: Europe — Integration, Convergence, and the Core-Periphery

**Core Theme:** Supranational integration, smart specialization, and the limits of policy-driven convergence. Europe provides the most ambitious experiment in services trade liberalization (the Single Market's "four freedoms") — and also the most instructive failures, since the EU Services Directive's incomplete implementation reveals how regulatory heterogeneity creates persistent barriers even within a nominally unified market.

### Chapter 8: The Single Market and the Convergence Machine

- **The Economics of EU Structural and Cohesion Funds:** Does top-down spatial redistribution create $\beta$-convergence, or does it generate "agglomeration shadows" where peripheral talent drains to the core?
- **Smart Specialization Strategies (S3):** The EU's attempt to tailor regional industrial policy — successes, failures, and the risk of "me-too" strategies.
- **The Four Freedoms as Spatial Policy:** How free movement of goods, services, capital, and people reshapes Europe's economic geography.
- **The Unfinished Services Market:** Why the 2006 Services Directive failed to create a true single market for services — the "country of origin" principle vs. mutual recognition, professional licensing barriers, and the political economy of sheltered domestic services. The Digital Single Market Strategy and GDPR as competing forces: harmonization that enables cross-border digital services vs. compliance costs that favor incumbents. London as Europe's APS command center — and the spatial consequences of Brexit for financial, legal, and consulting services networks (Faulconbridge 2008).

### Chapter 9: The North-South Divide and Post-Socialist Transitions

- **The Eurozone Crisis as Institutional Mismatch:** Analyzing the North–South divide through the lens of institutional differences between Germany/Benelux and the Mediterranean periphery. Real exchange rate divergence, current account imbalances, and the absence of fiscal union.
- **Post-Socialist Convergence:** The Visegrád Group's rapid integration into "Factory Germany" — automotive supply chains, wage convergence, and the risk of "dependent development." The parallel emergence of CEE cities (Warsaw, Bucharest, Prague, Budapest) as nearshore business services hubs — shared services centers, IT outsourcing, and financial back-offices that represent a services-track integration distinct from the manufacturing-track.
- **Brexit as a Natural Experiment:** The spatial economic consequences of dis-integration — border effects, FDI reallocation, and regulatory divergence. Brexit's disproportionate impact on financial services and APS networks: the relocation of clearing, trading, and advisory functions from London to Dublin, Frankfurt, Amsterdam, and Paris as a natural experiment in how regulatory borders reshape services geography.

### Applied Lab 3: Causal Inference in Space

- **Method:** Spatial Regression Discontinuity Design (Spatial RDD).
- **Application:** Using NUTS-2 regional data to evaluate the causal impact of EU Cohesion Funds on GDP growth for towns just inside versus just outside the eligibility border.
- **Extension:** Difference-in-differences with spatial spillovers — do treated regions grow at the expense of untreated neighbors?

---

## Part V: MENA — Rentier States, Climate Risk, and Fragile Geographies

**Core Theme:** Resource economics, spatial Dutch Disease, conflict spillovers, and the challenge of engineering diversification from above.

### Chapter 10: The Post-Carbon Transition and Sovereign Wealth

- **Rentier State Theory and the Resource Curse:** Why resource abundance weakens the institutional feedback loop between taxation, representation, and public goods provision.
- **State-Led Mega-Projects:** Analyzing "Vision 2030"–style programs (Saudi Arabia, UAE, Oman) as attempts to artificially engineer agglomeration economies from scratch — NEOM, KAEC, Masdar City.
- **Sovereign Wealth as Regional Strategy:** How Gulf SWFs (PIF, ADIA, Mubadala) function as instruments of spatial economic policy beyond national borders.
- **The Gulf as Global Services Hub:** Dubai and Doha as engineered connectivity nodes — aviation (Emirates, Qatar Airways as spatial policy tools), logistics (Jebel Ali, Hamad Port), and financial services (DIFC, QFC) that function as command centers for MENA and South Asian trade flows. The spatial economics of hub-and-spoke airline networks as instruments of services trade facilitation. Abu Dhabi and Riyadh's push into cloud infrastructure (AWS, Oracle data centers) and the geography of data sovereignty in the region.
- **The Gulf's Labor Geography:** Kafala systems, spatial segmentation of labor markets, and the economic geography of migration corridors from South Asia and East Africa.

### Chapter 11: Fragile States, Conflict Economics, and the Youth Bulge

- **The Collapse of Institutional Thickness:** How civil conflict in the Levant and North Africa destroys the institutional fabric necessary for regional trade.
- **Conflict as a Spatial Shock:** Refugee flows, diaspora remittances, and the redrawing of functional economic regions across formal borders.
- **Human Capital and the Youth Bulge:** Why regional growth hasn't translated into high-quality employment for the world's youngest population — spatial mismatches between education, labor demand, and economic opportunity.
- **Climate–Conflict Nexus:** Water scarcity, agricultural collapse, and climate-induced displacement as drivers of regional instability.

### Applied Lab 4: Evaluating Regional Shocks

- **Method:** Synthetic Control Method (SCM).
- **Application:** Estimating the counterfactual GDP trajectory of a conflict-affected state (e.g., Syria, Libya, Yemen) had the conflict not occurred, constructing a synthetic control from regional peers.
- **Extension:** Event-study designs for measuring the spatial diffusion of conflict shocks to neighboring economies.

---

## Part VI: Sub-Saharan Africa — Demographics, Informality, and the New Structuralism

**Core Theme:** Data scarcity, informal institutions, urbanization without industrialization, and the potential of continental integration.

### Chapter 12: Urbanization Without Industrialization

- **The African Anomaly:** Why African megacities (Lagos, Kinshasa, Dar es Salaam) generate steep congestion costs rather than agglomeration benefits — the absence of the traditional agriculture-to-manufacturing transition.
- **The "Premature Deindustrialization" Hypothesis:** Why African regions shift directly from agriculture to low-productivity services — and whether regional trade in intermediate goods can reverse this. But is the "services = low productivity" narrative too simple? The M-Pesa revolution (Suri & Jack 2016) and the emergence of Nairobi, Lagos, and Kigali as digital services hubs suggest that some African cities are generating productive service-sector agglomeration — leapfrogging manufacturing entirely through mobile money, fintech, and BPO.
- **Agglomeration vs. Congestion:** To what extent are African cities generating the Marshallian trinity (sharing, matching, learning) versus functioning as "consumption cities" or "poverty traps" due to infrastructure deficits?
- **The Urban-Rural Productivity Gap:** Africa's central spatial challenge — a gap far wider than the analogous European core-periphery wage gap.

### Chapter 13: The AfCFTA, Regional Hegemons, and Functional Corridors

- **The African Continental Free Trade Area (AfCFTA):** Can a continental "rules-based" agreement override domestic protectionist institutions? The "Nested Institutions" model applied. The AfCFTA's Protocol on Trade in Services — covering business services, communications, finance, tourism, and transport — as potentially more transformative than goods liberalization, since Africa's service-sector share of GDP already exceeds manufacturing.
- **The Border Effect in African Trade:** Why it remains ~3x more expensive to move a container between two African neighbors than between Africa and Europe — and what institutional and infrastructural reforms can change this.
- **Informal Cross-Border Trade (ICBT):** Recognizing the trade that dominates the Sahel and Great Lakes regions not as "chaos" but as a sophisticated, non-state institutional framework with its own enforcement mechanisms.
- **Regional Hegemons as Growth Poles:** The roles of South Africa (SADC), Nigeria (ECOWAS), and Kenya (EAC) as nodes that structure their respective sub-regional economies.
- **Functional Corridors:** The Northern Corridor (Kenya–Uganda–Rwanda) as a case study — how digital customs clearing (an institutional fix) had a larger impact on regional GDP than a 10% tariff reduction.

### Applied Lab 5: Alternative Data and Machine Learning

- **Method:** Raster data analysis and spatial autocorrelation (Moran's $I$).
- **Application:** Using VIIRS satellite night-lights data to proxy economic activity and measure cross-border spatial spillovers where formal GDP statistics are thin or unreliable.
- **Extension:** Connect night-lights to GDP nowcasting workflows (high-frequency consensus estimates and spatial dashboards), then map the "Product Space" for SADC countries to identify nearby upgrading paths (e.g., from copper to electric cables).

---

## Part VII: Global Synthesis

### Applied Lab 6: The Gravity of Services — Measuring Barriers to Services Trade

- **Method:** Gravity models of services trade, augmented with the OECD Services Trade Restrictiveness Index (STRI) and cultural/linguistic proximity measures.
- **Application:** Estimating the "tariff equivalent" of regulatory barriers to cross-border services trade. Using WTO BOP-based services trade data and OECD STRI scores, students estimate a gravity model for bilateral services trade and decompose the border effect into its regulatory, linguistic, and geographic components (Melitz & Toubal 2014).
- **Servicification Extension:** Using OECD TiVA data, decompose the service content embedded in manufacturing exports for a single sector (e.g., automobiles, electronics). Compare the "servicification" share across exporting countries and identify where the service value-added is geographically located — connecting to Lab 2's MRIO analysis.
- **Cloud Geography Exercise:** Map the global distribution of AWS, Azure, and Google Cloud data center regions and cross-reference with ECIPE data localization scores. Where do regulatory borders and infrastructure geography align, and where do they diverge? What does this imply for the future geography of digital services trade?
- **Comparative Component:** Students compare services trade barriers across two contrasting region-pairs (e.g., US–Mexico vs. France–Germany, or Kenya–South Africa vs. India–Singapore) to test whether regional integration agreements reduce regulatory barriers for services as effectively as they reduce tariffs for goods.

### Chapter 14: Climate Change and the Future Economic Map

- **Spatial Reallocation of Capital and Labor:** How climate-induced physical risks, shifting agricultural belts, and stranded regional assets redraw the world's economic geography.
- **Climate-Induced Migration:** How the shifting Sahelian belt and rising sea levels redefine regional economic boundaries.
- **Green Industrial Policy as Spatial Policy:** Carbon border adjustments (CBAM), green subsidies (IRA), and their effects on regional comparative advantage.
- **Stranded Regions:** The political economy of regions whose primary assets (fossil fuels, climate-vulnerable agriculture) lose value in the transition.
- **Telemedicine and the Geography of Health Services:** The pandemic-era expansion of cross-border telehealth as a natural experiment in whether digital delivery reduces or reinforces geographic concentration of specialist care (Zeltzer et al. 2023). A contained case study of the "does digital flatten geography?" question that complements the broader remote work analysis in Chapter 15.

### Chapter 15: The Future of Global Regionalism — Services, Telemigration, and the Splinternet

- **Fortress Blocs vs. Flexible Networks:** Are we moving toward a hyper-regionalized world of friend-shoring blocs, or will global value chains adapt and reweave?
- **The Telemigration Hypothesis:** Will white-collar service jobs follow the same spatial offshoring trajectory that blue-collar manufacturing did in the 1990s? Baldwin's (2019) "globotics upheaval" — freelancers in developing nations performing service-sector work in developed nations via digital platforms — as the next great spatial restructuring. Evidence from remote work adoption (Althoff et al. 2022) and spatial general equilibrium models of city restructuring (Delventhal, Kwon & Parkhomenko 2022).
- **The Splinternet and Regulatory Borders in the Service Economy:** How data localization laws, digital service taxes, geo-blocking, and content licensing territories erect new borders that are invisible in goods trade. The geography of cloud infrastructure (AWS, Azure, Google Cloud regions) as the physical footprint of the digital service economy, cross-referenced with regulatory borders (ECIPE Digital Trade Estimates). Three competing digital-regulatory models: the US (market-led), the EU (rights-based/GDPR), and China (sovereignty-first) — and how each creates a distinct geography of services trade.
- **Comparative Synthesis:** Drawing cross-regional lessons — what the European convergence machine can teach Africa, what Asian developmental states reveal about MENA diversification, and what Latin America's traps warn about for all middle-income regions.
- **The Discipline's Frontier:** Open questions in spatial economics — machine learning for spatial prediction, causal inference with interference, network-based models of trade and growth. The emerging frontier of services trade measurement and spatial modeling in a digital economy.

---

## Pedagogical Architecture

Each chapter is built around a consistent pedagogical structure that reinforces the book's commitment to interdisciplinary rigor.

### Recurring Chapter Features

1. **"Data in Depth" Boxes:** Each chapter includes a guided tutorial on using specific datasets (World Bank WDI, IMF IFS, WIOD, Afrobarometer, VIIRS, UN Comtrade) to replicate a key empirical result or regional growth regression discussed in the text.

2. **"Institutional Spotlight" Sidebars:** Short profiles of regional institutions, policy-makers, or governance experiments — drawing on interviews and primary documents. Examples: the AfCFTA Secretariat in Accra, CFIUS review processes, the EU's DG Regio, Saudi Arabia's PIF.

3. **Comparative Maps (GIS Visualizations):** Full-color maps using GIS to visualize spatial inequality *within* regions, not just between countries. Examples: night-lights intensity across the Sahel, wage gradients across the US–Mexico border, manufacturing density in the Pearl River Delta.

4. **"Comparative Spotlight" Tables:** Structured cross-regional comparisons at the end of each Part, linking back to earlier sections. Example:

   | Feature | European Regionalism (Part IV) | New African Regionalism (Part VI) |
   |---|---|---|
   | Driver | Supranational Law (*acquis communautaire*) | Functional Infrastructure (Corridors) |
   | Main Challenge | Core-Periphery Wage Gap | Urban-Rural Productivity Gap |
   | Key Metric | Convergence of Interest Rates | Convergence of Transport Costs |

5. **"Modern Empirical Questions" Sections:** End-of-chapter questions at the advanced undergrad/early PhD level, requiring a blend of econometric technique and political economy reasoning. Designed to be assignable as problem sets or short research proposals.

6. **Applied Labs (one per regional Part):** Self-contained empirical exercises with code templates (R/Python), replication data, and step-by-step instructions. Each lab introduces a distinct spatial method tied to the region's core analytical challenge.

### Lab Summary Table

| Lab | Region | Method | Application |
|---|---|---|---|
| Lab 1 | Americas | Spatial Lag Model (SAR), Weight Matrix $W$ | Shadow costs of US–Mexico border friction |
| Lab 2 | Asia | Multi-Regional Input-Output (MRIO) | Domestic value-added in Asian electronics GVCs; servicification decomposition |
| Lab 3 | Europe | Spatial Regression Discontinuity Design | Causal impact of EU Cohesion Funds |
| Lab 4 | MENA | Synthetic Control Method (SCM) | Counterfactual GDP of conflict-affected states |
| Lab 5 | Africa | Night-lights raster data, Moran's $I$ | Cross-border spillovers with alternative data |
| Lab 6 | Cross-regional | Services trade gravity model, STRI | Regulatory barriers to services trade; cloud infrastructure geography |

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

### Appendix C: Glossary of Key Terms
- Definitions of all technical terms, institutional acronyms, and spatial econometric notation used throughout the text.
