# Lab 3: Mapping IT-BPO Exports Across Indian States

## Overview

This lab maps the spatial distribution of India's IT and Business Process Outsourcing (BPO) exports at the state level, connecting Chapter 8's analysis of India's services geography to hands-on empirical work.

## Learning Objectives

1. Construct state-level services export profiles using RBI balance of payments and KLEMS productivity data.
2. Compute spatial concentration indices (Herfindahl, Location Quotients) for IT-BPO exports across Indian states.
3. Build a services value chain "smile curve" — plotting value-added per worker against skill intensity for different service tiers (BPO, KPO, fintech) across cities.
4. Compare India's services-led spatial concentration with Bangladesh's manufacturing-led pattern.

## Exercises

### Exercise 1: State-Level IT-BPO Export Mapping
Using RBI services trade data and STPI zone-level exports, construct a choropleth map of IT-BPO export intensity across Indian states. Compute Herfindahl indices and Location Quotients to measure spatial concentration.

### Exercise 2: The Services Smile Curve
Using KLEMS productivity data by sector, plot value-added per worker against skill intensity for BPO, KPO, and fintech tiers across major Indian cities. Test whether higher-value services are more spatially concentrated than routine services.

### Exercise 3: Comparative Concentration — Services vs. Manufacturing
Compare the spatial concentration of India's IT-BPO exports with Bangladesh's garment exports. Compute Gini coefficients for both and discuss the institutional drivers of concentration.

## Datasets

| Dataset | Source | Access |
|---|---|---|
| State-level services exports | RBI | Public (annual reports) |
| KLEMS India productivity | KLEMS India project | Public |
| STPI zone-level data | STPI annual reports | Public |
| NASSCOM state-level estimates | NASSCOM | Industry reports |
| Bangladesh garment export data | BGMEA | Public |

## Technical Specifications

- **Estimated time:** Minimum 2–3 hours; Extended 6–8 hours
- **Prerequisites:** Python (pandas, geopandas, matplotlib); basic familiarity with spatial visualization
- **Data size:** ~50 MB
- **Difficulty:** Intermediate
- **Cloud execution:** Colab-compatible (planned)

## Key References

- Dossani & Kenney (2007), "The Next Wave of Globalization"
- Grossman & Rossi-Hansberg (2008), "Trading Tasks"

## Implementation Status

- [ ] `code/it_bpo_mapping.py` — State-level export mapping scaffold
- [ ] `code/smile_curve_analysis.py` — Value chain smile curve analysis
- [ ] `code/fetch_rbi_services.py` — RBI data acquisition
- [ ] `code/concentration_comparison.py` — India vs. Bangladesh comparison
- [ ] Data acquisition pipeline
- [ ] Smoke test
