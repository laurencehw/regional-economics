# The New Regional Economics

**Spatial Dynamics, Institutions, and Applied Methods**

*Laurence Wilse-Samson* | NYU Wagner School of Public Policy

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

This book provides a unified treatment of regional economics across six world regions, combining new economic geography, institutional analysis, and modern spatial econometric methods. Each regional section pairs analytical chapters with a hands-on applied lab that uses real data to replicate or extend key empirical findings.

**Read online:** [GitBook edition](https://lwilsesamson.gitbook.io/regional-economics) *(coming soon)*

---

## Contents

### Part I: Theoretical and Methodological Foundations
1. The Micro-Foundations of Space
2. The Institutional Toolkit & Services Architecture
3-A. Spatial Econometrics & Inequality Measurement
3-B. Trade Measurement and the Gravity Model

### Part II: The Americas
4. The North American Core
5. Latin America and the Middle-Income Trap
- **Lab 1:** Spatial Autoregressive Models — Border Effects in the Americas

### Part III-A: East Asia
6. Flying Geese and Technology Ascendancy
7. China's Internal Divergence and ASEAN Fragmentation
- **Lab 2:** Convergence & GVC Decomposition — East Asian Supply Chains

### Part III-B: South Asia
8. India and the Geography of IT Services
- **Lab 3:** Market Concentration — India's IT Clusters

### Part IV: Europe
9. The Single Market and Convergence
10. The North-South Divide and Disintegration
- **Lab 4:** Regression Discontinuity — EU Structural Funds

### Part V: Middle East and North Africa
11. Post-Carbon Transition and Sovereign Wealth
12. Fragile States and Conflict Economics
- **Lab 5:** Synthetic Control Methods — Conflict & GDP in MENA

### Part VI: Sub-Saharan Africa
13. Urbanization Without Industrialization
14. AfCFTA and Functional Corridors
- **Lab 6:** Spatial Autocorrelation — Nighttime Luminosity in Africa

### Part VII: Synthesis
15. Climate, Stranded Regions, and the Future Map
16. The Future of Global Regionalism
- **Lab 7:** Gravity & Services Trade — PPML Estimation

### Appendices
- A: Mathematical Foundations
- B: Data and Software Guide
- C: Glossary of Key Terms

---

## Applied Labs

Each lab is a self-contained replication exercise in `labs/labN_region/`. Data is fetched via scripts in `scripts/` — no data files are stored in this repository. To run a lab:

```bash
pip install -r requirements.txt
python scripts/fetch_wdi_lab1.py        # example: fetch Lab 1 data
python labs/lab1_americas/code/lab1_americas_sar_scaffold.py
```

Run the test suite with:

```bash
pytest
```

See [Appendix B](chapters/appendix_b_data_software_guide.md) for full setup instructions, data sources, and software requirements.

---

## Citation

```bibtex
@book{wilsesamson2026regional,
  author    = {Wilse-Samson, Laurence},
  title     = {The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods},
  year      = {2026},
  publisher = {NYU Wagner School of Public Policy},
  url       = {https://github.com/lwilsesamson/regional-economics}
}
```

---

## License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). You are free to share and adapt this material for non-commercial purposes with attribution.
