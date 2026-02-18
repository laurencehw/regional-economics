# Chapter Spec: Ch.3 - The Modern Spatial Econometric Toolkit

## Metadata
- Part: Part I - Foundations
- Target word count: 11,000
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-03-29

## Core Thesis
Credible regional inference requires explicit modeling of spatial dependence and careful identification strategy. The toolkit should be taught as a sequence: define the spillover structure, select the appropriate model class, interpret direct vs indirect effects, then stress-test identification.

## Key Arguments (3-5)
1. OLS is generally misspecified in spatial settings because errors and outcomes propagate through geographic and network links.
2. The spatial weight matrix is a substantive modeling choice, not a technical afterthought; inference is sensitive to W construction.
3. SAR, SEM, and SDM answer different questions and require impact decomposition beyond raw coefficients.
4. The reflection problem and endogenous network formation are first-order identification threats.
5. Design-based methods (Spatial RDD, Synthetic Control, DiD with spillovers) complement parametric spatial models for causal claims.

## Required Datasets
- Eurostat NUTS-2 panel with boundary shapefiles (for baseline spatial model demonstrations).
- County/region bilateral trade or commuting flow tables for alternative W constructions.
- VIIRS night-lights grids for measurement robustness in data-sparse contexts.

## Anchor References (2-3)
1. Anselin (1988), *Spatial Econometrics: Methods and Models*.
2. LeSage and Pace (2009), *Introduction to Spatial Econometrics*.
3. Manski (1993), "Identification of Endogenous Social Effects," *Review of Economic Studies*.

## Figures/Maps Needed
- Diagnostic plot showing residual spatial autocorrelation under OLS (Moran's I workflow).
- Side-by-side map of contiguity, k-nearest-neighbor, and trade-weighted W matrices.
- Direct/indirect/total-effect decomposition visual for SAR/SDM.

## Data in Depth Box
- Topic: Sensitivity audit for spatial estimates under alternative W matrices.
- Dataset(s): NUTS-2 GDP growth panel + shapefiles + interregional trade proxy.
- Replication output: Table comparing SAR/SEM/SDM coefficients and spillover impacts across W specifications.

## Institutional Spotlight
- Institution/person: Eurostat GISCO and national statistical agencies maintaining harmonized regional boundaries.
- Why included: Shows that inference quality depends on institutional choices in geocoding and boundary harmonization.

## Applied Lab Linkage
- Relevant lab: Methods bridge to all labs
- Econometric method: SAR, SEM, SDM and spatial causal inference
- Required code artifacts: shared utility module for W construction and diagnostics, plus method-specific starter notebooks for Labs 1-5.

## Open Questions/Risks
- Results can be fragile to W misspecification and boundary changes over time.
- Spatial standard-error corrections and finite-sample behavior need transparent reporting.
- Interference assumptions in causal designs are often stronger than presented in applied work.
