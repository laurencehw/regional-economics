# Chapter Spec: Ch.3-A - Spatial Econometrics & Inequality Measurement

## Metadata
- Part: Part I - Foundations
- Target word count: 8,000–10,000
- Target pages: 30–35
- Status: Spec drafted
- Owner: Laurence (lead)
- Draft due: 2026-03-29

## Core Thesis
Credible regional inference requires explicit modeling of spatial dependence and careful identification strategy. The toolkit is taught as a sequence: measure spatial inequality, define the spillover structure, select the appropriate model class, interpret direct vs indirect effects, then stress-test identification. This chapter covers spatial econometrics proper; trade measurement and gravity models are covered in Ch. 3-B.

## Key Arguments (3-5)
1. Before modeling spatial processes, students need formal tools for measuring spatial inequality — β-convergence, σ-convergence, Theil indices, spatial Gini, and the Williamson hypothesis.
2. OLS is generally misspecified in spatial settings because errors and outcomes propagate through geographic and network links.
3. The spatial weight matrix is a substantive modeling choice, not a technical afterthought; inference is sensitive to W construction.
4. SAR, SEM, and SDM answer different questions and require impact decomposition beyond raw coefficients.
5. The reflection problem and endogenous network formation are first-order identification threats.
6. Design-based methods (Spatial RDD, SCM, DiD with spillovers, Bartik shift-share instruments) complement parametric spatial models for causal claims.
7. The Modifiable Areal Unit Problem (MAUP) — results can change dramatically depending on how geographic boundaries are drawn.
8. Quantitative Spatial Models (QSMs) provide a structural general equilibrium framework for counterfactual analysis.

## Required Datasets
- Eurostat NUTS-2 panel with boundary shapefiles (for baseline spatial model demonstrations and σ-convergence computation).
- Chinese provincial GDP data (for comparative convergence computation in Data in Depth box).
- County/region bilateral trade or commuting flow tables for alternative W constructions.
- VIIRS night-lights grids for measurement robustness in data-sparse contexts.

## Anchor References (2-3)
1. Anselin (1988), *Spatial Econometrics: Methods and Models*.
2. LeSage and Pace (2009), *Introduction to Spatial Econometrics*.
3. Manski (1993), "Identification of Endogenous Social Effects," *Review of Economic Studies*.
4. Barro & Sala-i-Martin (1992), "Convergence," *JPE* — foundational β-convergence framework.

## Figures/Maps Needed
- Diagnostic plot showing residual spatial autocorrelation under OLS (Moran's I workflow).
- Side-by-side map of contiguity, k-nearest-neighbor, and trade-weighted W matrices.
- Direct/indirect/total-effect decomposition visual for SAR/SDM.
- MAUP illustration: same regression on different boundary definitions yielding different results.

## Data in Depth Box
- Topic: Computing σ-convergence for EU NUTS-2 regions and Chinese provinces using the same code template.
- Dataset(s): Eurostat NUTS-2 GDP + Chinese provincial GDP.
- Replication output: Two convergence plots side-by-side showing very different convergence patterns using the same methodology.

## Institutional Spotlight
- Institution/person: Eurostat GISCO and national statistical agencies maintaining harmonized regional boundaries.
- Why included: Shows that inference quality depends on institutional choices in geocoding and boundary harmonization.

## Applied Lab Linkage
- Relevant lab: Methods bridge to all labs
- Econometric method: SAR, SEM, SDM, spatial causal inference, Bartik shift-share
- Required code artifacts: shared utility module for W construction and diagnostics, convergence computation functions.

## Preview Boxes
- "In Chapter 9, we will use the Spatial RDD framework introduced here to evaluate whether EU Cohesion Funds caused convergence or simply subsidized agglomeration."
- "In Lab 5, we apply Synthetic Control Methods to estimate the counterfactual GDP trajectory of conflict-affected states."

## Open Questions/Risks
- Results can be fragile to W misspecification and boundary changes over time (MAUP).
- Spatial standard-error corrections and finite-sample behavior need transparent reporting.
- Interference assumptions in causal designs are often stronger than presented in applied work.
- QSMs require strong structural assumptions — appropriate introduction of limitations needed.
