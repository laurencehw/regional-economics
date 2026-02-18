# Chapter Spec: Ch.1 - The Micro-Foundations of Space

## Metadata
- Part: Part I - Foundations
- Target word count: 9,500
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-03-15

## Core Thesis
Regional concentration is best explained by micro-level behavior under increasing returns and transport/coordination frictions. Classical location theory and New Economic Geography are complementary tools, and both point to the same policy implication: functional economic areas, not administrative borders, should be the unit of analysis.

## Key Arguments (3-5)
1. Classical models (Von Thunen, Weber, Christaller, Losch) still define the benchmark logic of land rent, transport cost, and market access.
2. NEG formalizes a nonlinear balance of centripetal and centrifugal forces, generating multiple spatial equilibria and path-dependent lock-in.
3. The Marshallian trinity (sharing, matching, learning) explains why productivity gains rise with density in some sectors but not universally.
4. Functional regions built from commuting, supply-chain, and knowledge flows outperform administrative units for inference and policy design.
5. Digitalization weakens some distance costs but does not eliminate tacit-knowledge spillovers or local labor-market pooling effects.

## Required Datasets
- OECD Functional Urban Areas and TL3 regional indicators.
- US BEA Regional Economic Accounts and BLS QCEW for employment/wage structure.
- LEHD LODES commuting flows (US) for functional region construction.
- GHSL or WorldPop raster products for settlement density and urban form.

## Anchor References (2-3)
1. Fujita, Krugman, and Venables (1999), *The Spatial Economy*.
2. Krugman (1991), "Increasing Returns and Economic Geography," *Journal of Political Economy*.
3. Duranton and Puga (2004), "Micro-Foundations of Urban Agglomeration Economies," in *Handbook of Regional and Urban Economics*.

## Figures/Maps Needed
- Monocentric-city bid-rent gradient schematic.
- Core-periphery bifurcation diagram (iceberg transport cost sensitivity).
- Functional-region map comparing commuting zones vs state/province boundaries.

## Data in Depth Box
- Topic: Estimating the urban wage premium with sector and worker controls.
- Dataset(s): BEA/BLS regional panel + commuting-zone crosswalk.
- Replication output: Baseline and fixed-effects wage-density regressions with sensitivity to region definitions.

## Institutional Spotlight
- Institution/person: US OMB metropolitan definitions and OECD FUA methodology teams.
- Why included: Demonstrates how measurement institutions shape observed spatial inequality and policy targeting.

## Applied Lab Linkage
- Relevant lab: None (foundation chapter)
- Econometric method: NEG micro-foundations and agglomeration logic
- Required code artifacts: `scripts/ch01_density_premium_scaffold.py`, reproducible figure script for core-periphery comparative statics.

## Open Questions/Risks
- Reverse causality between productivity and density remains a core identification challenge.
- Commuting-flow definitions vary across countries and may reduce comparability.
- Post-2020 remote work may change short-run elasticities while leaving long-run agglomeration intact.
