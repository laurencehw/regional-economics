# Chapter Spec: Ch.3-B - Trade Measurement and the Gravity Model

## Metadata
- Part: Part I - Foundations
- Target word count: 7,000–9,000
- Target pages: 25–30
- Status: Spec drafted
- Owner: Laurence (lead)
- Draft due: 2026-04-05

## Core Thesis
The gravity model is the workhorse of empirical trade economics, but it produces strikingly different results for services than for goods. Understanding these differences — and the measurement challenges underlying services trade data — is essential before any regional chapter can meaningfully discuss services geography. This chapter provides the reference treatment that all regional chapters cross-reference.

## Key Arguments (3-5)
1. Structural gravity (Anderson & van Wincoop 2003) provides the theoretical foundation; PPML (Santos Silva & Tenreyro 2006) is the preferred estimator for handling zeros and heteroskedasticity.
2. Distance elasticities are often *larger* for services than goods (counterintuitively) — language, colonial ties, and regulatory barriers matter more for services trade.
3. The Grossman & Rossi-Hansberg (2008) "trading tasks" framework explains which service tasks offshore based on communication costs, routineness, and factor price differences.
4. Standard BOP statistics undercount services trade — Mode 3 (commercial presence/FDI) is poorly captured, and "servicification" (service content embedded in manufacturing exports) is invisible without TiVA decomposition.
5. The GATS four-mode framework provides the institutional grammar: Mode 1 (cross-border), Mode 2 (consumption abroad), Mode 3 (commercial presence), Mode 4 (movement of persons). Each regional chapter should identify which modes are most relevant.

## Required Datasets
- WTO BOP-based bilateral services trade statistics.
- OECD TiVA indicators for servicification decomposition.
- OECD STRI scores by country and sector.
- ECIPE Digital Trade Estimates.
- CEPII distance/language/colonial-tie gravity variables.

## Anchor References (2-3)
1. Anderson & van Wincoop (2003), "Gravity with Gravitas," *AER*.
2. Santos Silva & Tenreyro (2006), "The Log of Gravity," *ReStat*.
3. Grossman & Rossi-Hansberg (2008), "Trading Tasks: A Simple Theory of Offshoring," *AER*.
4. Kimura & Lee (2006), "The Gravity Equation in International Trade in Services," *RIEB*.
5. Head, Mayer & Ries (2009), "How Remote Is the Offshoring Threat?" *EER*.

## Figures/Maps Needed
- Distance elasticity comparison chart: goods vs. services across multiple gravity studies.
- Running Gravity Results Table: canonical estimates from the literature (reprinted and extended in Lab 7).
- Schematic of GATS four modes with real-world examples from regional chapters.
- Servicification chart: service value-added share in manufacturing exports for selected countries (from TiVA).

## Data in Depth Box
- Topic: Estimating a baseline PPML gravity model for bilateral services trade.
- Dataset(s): WTO BOP services + CEPII gravity variables + OECD STRI.
- Replication output: Coefficient table comparing distance, language, and STRI effects for goods vs. services.

## Institutional Spotlight
- Institution/person: WTO Trade in Services Division — the challenges of collecting Mode 3 data across countries.
- Why included: Demonstrates why services trade measurement is a frontier problem, not a solved one.

## Applied Lab Linkage
- Relevant lab: Lab 7 (Services Gravity)
- Econometric method: PPML gravity with STRI augmentation
- Required code artifacts: Baseline gravity estimation script that Lab 7 extends with institutional variables.

## Running Gravity Results Table
First appears in this chapter with canonical estimates. Reprinted and extended in Lab 7 when students add their own STRI-augmented estimates. Cross-regional comparison of distance elasticities for services vs. goods as a throughline.

## Open Questions/Risks
- Mode 3 data remains sparse; students should understand the FDI-services trade data gap.
- STRI comparability across countries is imperfect — different regulatory traditions may produce similar scores with very different effects.
- Servicification measures depend on MRIO table vintage and sector concordances.
