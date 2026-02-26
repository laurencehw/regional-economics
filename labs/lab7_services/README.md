# Lab 7: The Gravity of Services — Measuring Barriers to Services Trade

## Overview

Lab 7 is a cross-regional synthesis lab that accompanies Part VII (Chapters 15–16). It introduces the gravity model for services trade and applies it to measure the "tariff equivalent" of regulatory barriers using the OECD Services Trade Restrictiveness Index (STRI).

Unlike Labs 1–6, which are regionally focused, Lab 7 draws on data from all regions covered in the book, making it a natural capstone exercise that ties together the services trade threads woven through the preceding chapters.

## Method

**Gravity model of bilateral services trade**, augmented with:
- OECD STRI scores as the key policy barrier variable
- Language, colonial ties, and cultural proximity (Melitz & Toubal 2014)
- Geographic distance (CEPII)
- PPML estimation to handle the prevalence of zeros in services trade data

## Core Exercises

### Exercise 1: Services vs. Goods Gravity
Estimate parallel gravity models for bilateral goods and services trade between the same country pairs. Compare:
- Distance elasticities (typically *larger* for services — counterintuitive)
- Language and colonial-tie coefficients (typically stronger for services)
- R-squared and explanatory power

Students should interpret the results through the Grossman & Rossi-Hansberg (2008) "trading tasks" framework: why does distance matter more for services when digital transmission costs are near zero?

### Exercise 2: STRI Tariff Equivalents
Using the OECD STRI, estimate the tariff-equivalent cost of regulatory barriers for a specific service sector (e.g., financial services, telecom, professional services). Compare across regions:
- Americas (US, Canada, Mexico — USMCA digital trade provisions)
- Asia (India, Japan, Korea, Singapore — IT services vs. protected domestic markets)
- Europe (EU members — the "unfinished" services market)
- Africa (Kenya, South Africa, Nigeria — AfCFTA services protocol context)

### Exercise 3: Servicification Decomposition
Using OECD TiVA data, decompose the service content embedded in manufacturing exports for a single sector (e.g., automobiles, electronics). Compare the "servicification share" across exporting countries. Where is the service value-added geographically located? This connects to Lab 2's MRIO analysis.

### Exercise 4: Cloud Geography
Map the global distribution of AWS, Azure, and Google Cloud data center regions. Cross-reference with ECIPE data localization scores. Where do regulatory borders and infrastructure geography align, and where do they diverge? What does this imply for the future geography of digital services trade?

## Required Datasets

| Dataset | Source | Access |
|---------|--------|--------|
| Bilateral services trade | WTO BOP-based statistics | Public (WTO data portal) |
| Bilateral goods trade | UN Comtrade | Public (API) |
| STRI scores | OECD STRI database | Public (OECD.Stat) |
| Gravity variables | CEPII GeoDist | Public |
| Language/colonial ties | CEPII Language | Public |
| TiVA servicification | OECD TiVA | Public (OECD.Stat) |
| Data localization scores | ECIPE Digital Trade Estimates | Public |
| Cloud regions | AWS/Azure/Google | Public (provider websites) |

## Key References

- Kimura & Lee (2006), "The Gravity Equation in International Trade in Services," *Review of World Economics*
- Head, Mayer & Ries (2009), "How Remote Is the Offshoring Threat?," *European Economic Review*
- Grossman & Rossi-Hansberg (2008), "Trading Tasks: A Simple Theory of Offshoring," *AER*
- Borchert, Gootiiz & Mattoo (2014), "Policy Barriers to International Trade in Services," *WBER*
- Melitz & Toubal (2014), "Native Language, Spoken Language, Translation and Trade," *JIE*
- Francois & Hoekman (2010), "Services Trade and Policy," *JEL*

## Status

- [ ] Scaffold gravity model estimation pipeline
- [ ] Acquire WTO BOP services trade data
- [ ] Acquire OECD STRI panel
- [ ] Build CEPII gravity variable merge
- [ ] Implement PPML estimator
- [ ] TiVA servicification decomposition
- [ ] Cloud geography mapper
- [ ] Smoke test
