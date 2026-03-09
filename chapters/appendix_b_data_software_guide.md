# Appendix B: Data and Software Guide

---

This appendix provides practical instructions for accessing the datasets used throughout the book and setting up the software environment needed to run the Applied Labs. It is organized in three parts: (1) a master dataset inventory covering all data sources referenced in the text, (2) software setup instructions for R and Python, and (3) per-lab data dictionaries and technical specifications.

---

## B.1 Master Dataset Inventory

The table below lists every external dataset referenced in the book's chapters and labs, with access instructions, licensing information, and the chapters/labs where each dataset is used.

### International Trade and Services

| Dataset | Provider | Access | License | Used In |
|---|---|---|---|---|
| **UN Comtrade** | United Nations | [comtradeplus.un.org](https://comtradeplus.un.org/) — free API with registration | Open | Chs. 3-B, 4, 5, 6 |
| **WTO BOP Services Trade** | WTO | [timeseries.wto.org](https://timeseries.wto.org/) — free download | Open | Ch. 16, Lab 7 |
| **OECD TiVA** | OECD | [oecd.org/sti/ind/measuring-trade-in-value-added.htm](https://www.oecd.org/sti/ind/measuring-trade-in-value-added.htm) — free download | Open | Chs. 6, 7, Lab 2 |
| **WIOD** | University of Groningen | [wiod.org](http://www.wiod.org/) — free download | Academic use | Ch. 6, Lab 2 |
| **OECD STRI** | OECD | [oecd.org/trade/topics/services-trade](https://www.oecd.org/trade/topics/services-trade/) — free download | Open | Chs. 2, 9, 16, Lab 7 |
| **CEPII GeoDist** | CEPII | [cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=6](http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=6) — free download | Open | Ch. 3-B, Lab 7 |

### Macroeconomic and Development

| Dataset | Provider | Access | License | Used In |
|---|---|---|---|---|
| **World Development Indicators (WDI)** | World Bank | [databank.worldbank.org](https://databank.worldbank.org/) — free API and bulk download | Open (CC BY 4.0) | Chs. 4, 5, 11, 13, Labs 1, 5 |
| **IMF World Economic Outlook** | IMF | [imf.org/en/Publications/WEO](https://www.imf.org/en/Publications/WEO) — free download | Open | Chs. 11, 12 |
| **Penn World Table** | University of Groningen | [rug.nl/ggdc/productivity/pwt](https://www.rug.nl/ggdc/productivity/pwt/) — free download | Academic use | Chs. 3-A, 6 |

### European Data

| Dataset | Provider | Access | License | Used In |
|---|---|---|---|---|
| **Eurostat NUTS-2 Regional Statistics** | Eurostat | [ec.europa.eu/eurostat](https://ec.europa.eu/eurostat) — free bulk download | Open | Chs. 9, 10, Lab 4 |
| **EU Cohesion Data** | European Commission | [cohesiondata.ec.europa.eu](https://cohesiondata.ec.europa.eu/) — free download | Open | Ch. 9, Lab 4 |

### Conflict and Displacement

| Dataset | Provider | Access | License | Used In |
|---|---|---|---|---|
| **ACLED** | ACLED | [acleddata.com](https://acleddata.com/) — free with registration; redistribution restricted | Academic use (see terms) | Chs. 12, Lab 5 |
| **UNHCR Population Statistics** | UNHCR | [unhcr.org/refugee-statistics](https://www.unhcr.org/refugee-statistics/) — free download | Open | Ch. 12, Lab 5 |

### Remote Sensing and Alternative Data

| Dataset | Provider | Access | License | Used In |
|---|---|---|---|---|
| **VIIRS Night-lights** | NASA/NOAA | [eogdata.mines.edu/products/vnl](https://eogdata.mines.edu/products/vnl/) — free download after registration | Open (public domain) | Ch. 13, Lab 6 |
| **Afrobarometer** | Afrobarometer | [afrobarometer.org](https://www.afrobarometer.org/) — free download with registration | Academic use | Ch. 13, Lab 6 |

### India and South Asia

| Dataset | Provider | Access | License | Used In |
|---|---|---|---|---|
| **RBI State-level Data** | Reserve Bank of India | [rbi.org.in](https://www.rbi.org.in/) — free download | Open | Ch. 8, Lab 3 |
| **KLEMS India** | RBI/ICRIER | [rbi.org.in/scripts/klaborprod.aspx](https://www.rbi.org.in/scripts/klaborprod.aspx) — free download | Open | Ch. 8, Lab 3 |
| **NASSCOM Reports** | NASSCOM | [nasscom.in](https://nasscom.in/) — some reports require membership | Mixed | Ch. 8 |

### Logistics and Infrastructure

| Dataset | Provider | Access | License | Used In |
|---|---|---|---|---|
| **World Bank Logistics Performance Index (LPI)** | World Bank | [lpi.worldbank.org](https://lpi.worldbank.org/) — free download | Open (CC BY 4.0) | Chs. 4, 14, Lab 1 |
| **Bureau of Transportation Statistics (BTS)** | US DOT | [bts.gov](https://www.bts.gov/) — free download | Open (US public domain) | Ch. 4, Lab 1 |

---

## B.2 Software Environment Setup

The Applied Labs use Python (primary) with optional R extensions. All labs are designed to run in zero-install cloud environments (Google Colab) or in a local Python installation.

### Python Setup (Recommended)

**Minimum Python version:** 3.10+

**Required packages:**

```
numpy>=1.26
pandas>=2.2
scipy>=1.12
requests>=2.31
pycountry>=23.12
```

**Installation:**

```bash
# Clone the repository
git clone https://github.com/laurencehw/regional-economics.git
cd regional-economics

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

**Verify installation:**

```bash
python -m pytest tests/ -v
```

All 107 tests should pass.

### Google Colab (Zero-Install)

Colab notebooks are provided for Labs 1 and 6. To use them:

1. Open the `.ipynb` file from the repository in Google Colab
2. The notebook installs any additional dependencies in its first cell
3. Synthetic data is generated within the notebook — no external data downloads needed for the Minimum Viable Version

### R Setup (Optional)

Some extended lab versions offer R alternatives using the spatial econometrics ecosystem:

```r
install.packages(c("spdep", "spatialreg", "sf", "fixest", "gravity"))
```

**Key R packages by lab:**
- **Lab 1 (SAR):** `spatialreg`, `spdep` for spatial weight matrices and lag models
- **Lab 4 (RDD):** `rdrobust` for regression discontinuity estimation
- **Lab 7 (Gravity):** `fixest` for PPML with high-dimensional fixed effects; `gravity` for standard gravity estimation

---

## B.3 Per-Lab Technical Specifications

### Lab 1: Americas — Spatial Lag Model and Border Effects

| Specification | Value |
|---|---|
| **Estimated time** | Minimum: 2–3 hrs; Extended: 6–8 hrs |
| **Difficulty** | Intermediate |
| **Prerequisites** | Ch. 1, Ch. 3-A (SAR/SEM), Ch. 4 |
| **Software** | Python (numpy, pandas, scipy) |
| **Data (Minimum)** | Synthetic 34-economy panel (built-in) |
| **Data (Extended)** | WDI, BTS border crossing, LPI |
| **Key scripts** | `labs/lab1_americas/code/lab1_americas_sar_scaffold.py` |
| **Colab notebook** | `labs/lab1_americas/Lab1_Americas_SAR.ipynb` |
| **Key outputs** | SAR coefficients, spatial weight matrix, rho estimate, robustness table |

### Lab 2: East Asia — Beta-Convergence and DVA Participation

| Specification | Value |
|---|---|
| **Estimated time** | Minimum: 3–4 hrs; Extended: 8–10 hrs |
| **Difficulty** | Advanced |
| **Prerequisites** | Ch. 3-A (convergence), Ch. 3-B (TiVA, GVCs), Ch. 6 |
| **Software** | Python (numpy, pandas) |
| **Data (Minimum)** | Synthetic 12-economy East Asian panel (built-in) |
| **Data (Extended)** | WIOD or OECD TiVA |
| **Key scripts** | `labs/lab2_asia/code/lab2_asia_convergence_scaffold.py` |
| **Key outputs** | Beta-convergence estimates, half-life calculations, DVA participation shares, sigma-convergence trends |

### Lab 3: South Asia — IT Services Concentration

| Specification | Value |
|---|---|
| **Estimated time** | Minimum: 2–3 hrs; Extended: 5–6 hrs |
| **Difficulty** | Introductory–Intermediate |
| **Prerequisites** | Ch. 8 |
| **Software** | Python (numpy, pandas) |
| **Data (Minimum)** | Synthetic 12-state IT panel (built-in) |
| **Data (Extended)** | RBI state-level data, KLEMS India |
| **Key scripts** | `labs/lab3_south_asia/code/lab3_concentration_scaffold.py`, `prepare_lab3_inputs.py` |
| **Key outputs** | Location Quotients, Herfindahl index, Gini coefficient, time-series HHI |

### Lab 4: Europe — Spatial Regression Discontinuity

| Specification | Value |
|---|---|
| **Estimated time** | Minimum: 3–4 hrs; Extended: 8–10 hrs |
| **Difficulty** | Advanced |
| **Prerequisites** | Ch. 3-A (RDD concepts), Ch. 9 |
| **Software** | Python (numpy, pandas, scipy); R `rdrobust` for extended version |
| **Data (Minimum)** | Synthetic NUTS-2 panel (built-in) |
| **Data (Extended)** | Eurostat NUTS-2 regional GDP, EU Cohesion Fund allocations |
| **Key scripts** | `labs/lab4_europe/code/lab4_europe_rdd_scaffold.py` |
| **Key outputs** | RDD estimates, bandwidth sensitivity, kernel comparison, temporal dynamics |

### Lab 5: MENA — Synthetic Control Method

| Specification | Value |
|---|---|
| **Estimated time** | Minimum: 3–4 hrs; Extended: 8–10 hrs |
| **Difficulty** | Advanced |
| **Prerequisites** | Ch. 11, Ch. 12 |
| **Software** | Python (numpy, pandas, scipy) |
| **Data (Minimum)** | Synthetic 15-country MENA panel (built-in) |
| **Data (Extended)** | WDI, ACLED, UNHCR refugee statistics |
| **Key scripts** | `labs/lab5_mena/code/conflict_event_study.py`, `scm_gap_plotter.py`, `donor_weight_visualizer.py` |
| **Key outputs** | Synthetic control weights, counterfactual GDP trajectory, placebo tests, gap plot |

### Lab 6: Africa — Night-Lights and Moran's I

| Specification | Value |
|---|---|
| **Estimated time** | Minimum: 2–3 hrs; Extended: 6–8 hrs |
| **Difficulty** | Intermediate |
| **Prerequisites** | Ch. 3-A (Moran's I), Ch. 13 |
| **Software** | Python (numpy, pandas, scipy) |
| **Data (Minimum)** | Synthetic 15-region grid (built-in) |
| **Data (Extended)** | VIIRS night-lights, Afrobarometer governance surveys |
| **Key scripts** | `labs/lab6_africa/code/lab6_africa_moran_scaffold.py`, `prepare_lab6_inputs.py` |
| **Colab notebook** | `labs/lab6_africa/Lab6_Africa_Morans_I.ipynb` |
| **Key outputs** | Moran's I statistic, permutation p-value, residualized Moran's I, spatial autocorrelation diagnostics |

### Lab 7: Cross-Regional — Services Trade Gravity

| Specification | Value |
|---|---|
| **Estimated time** | Minimum: 3–4 hrs; Extended: 8–10 hrs |
| **Difficulty** | Intermediate–Advanced |
| **Prerequisites** | Ch. 3-B (gravity, PPML), Ch. 16 |
| **Software** | Python (numpy, pandas) |
| **Data (Minimum)** | Synthetic 10-country bilateral trade panel (built-in) |
| **Data (Extended)** | WTO BOP services trade, CEPII GeoDist, OECD STRI |
| **Key scripts** | `labs/lab7_services/code/gravity_services_scaffold.py`, `stri_tariff_equivalent.py`, `ppml_estimator.py` |
| **Key outputs** | PPML coefficients for services vs. goods gravity, distance elasticity comparison, STRI tariff equivalents by country and sector |

---

## B.4 Data Dictionary Conventions

All labs use a consistent data format:

- **Panel data:** CSV files with columns `region` (or `country`, `exporter`/`importer`), `year`, and variable columns
- **Spatial weights:** CSV edge lists with columns `region_i`, `region_j`, `weight` (or JSON adjacency format)
- **Model outputs:** JSON files with standardized keys: `method`, `n_obs`, `betas`, `se`, `beta_names`

Column mappings between raw data sources and canonical lab formats are stored in `source_mappings.json` files in each lab's `data/` directory. These mappings ensure that the preparation scripts (`prepare_lab*_inputs.py`) can adapt to different raw data formats without changing the analysis scripts.

---

## B.5 Troubleshooting

**"ModuleNotFoundError" when running a lab script.**
Ensure you have activated the virtual environment and installed requirements: `pip install -r requirements.txt`

**Smoke tests fail on import.**
The lab scripts use relative imports within the `labs/*/code/` directories. Run scripts from the repository root or add the code directory to your Python path.

**Template data produces unrealistic results.**
Template datasets are synthetic and designed for mechanical testing, not substantive analysis. Real-data results will differ substantially. See each lab's README for instructions on substituting real data.

**VIIRS data download requires registration.**
VIIRS night-lights data requires a free account at the Earth Observation Group. Registration is typically approved within 24 hours. See the Lab 6 README for detailed instructions.

**ACLED data redistribution.**
ACLED data is free for academic use but has redistribution restrictions. Do not commit raw ACLED downloads to public repositories. Use the template data for testing and store full datasets externally per the data storage policy.
