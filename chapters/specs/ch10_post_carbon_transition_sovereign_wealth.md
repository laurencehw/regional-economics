# Chapter Spec: Ch.10 - The Post-Carbon Transition and Sovereign Wealth

## Metadata
- Part: Part V - MENA
- Target word count: 10,000
- Status: Spec drafted
- Owner: Laurence (lead), Codex (support)
- Draft due: 2026-04-26

## Core Thesis
Sovereign-wealth-led diversification in MENA succeeds when institutional reforms in procurement, labor mobility, and private-sector contestability accompany capital deployment. Absent these reforms, mega-projects generate enclave urban growth with weak economy-wide spillovers.

## Key Arguments (3-5)
1. Rentier fiscal structures weaken feedback loops between taxation and productive-state capacity.
2. SWFs can function as regional industrial-policy instruments, but only under credible governance constraints.
3. Labor-market segmentation (including migrant labor institutions) shapes transmission from investment to productivity.
4. Logistics connectivity and trade openness determine whether projects integrate into broader value chains.
5. Diversification outcomes should be assessed by tradable-sector depth, not headline construction activity.

## Institutional Variable Operationalization
- Institutional variable: `diversification_governance_rt`.
- Measurement:
  - Non-oil fiscal revenue share and regulatory-quality indicators (WGI/IMF sources).
  - Procurement/transparency proxies from budget and governance reports.
  - Labor-market reform proxy (migrant labor regulation changes and private-sector employment composition).
- Spatial interaction term: `diversification_governance_rt × corridor_connectivity_rt` for non-oil output outcomes.

## Required Datasets
- IMF and WDI macro series (oil rents, non-oil GDP proxies, fiscal structure).
- WGI governance indicators and selected national governance releases.
- SWF annual reports/investment announcements (PIF, ADIA, Mubadala) with project geolocation.
- Port/logistics throughput indicators where available.
- Sectoral employment composition data (ILO or national labor-force releases).

## Anchor References (2-3)
1. Beblawi and Luciani (1987), rentier-state foundations.
2. Hertog (2010), Gulf state-business institutional structure.
3. Ross (2012), oil institutions and political economy.

## Figures/Maps Needed
- Map of major SWF-backed projects and trade corridors.
- Non-oil tradable-sector trend charts by country.
- Comparative chart: high vs low governance-capacity diversification outcomes.

## Data in Depth Box
- Topic: Event-study around flagship diversification announcements.
- Dataset(s): SWF project timeline + macro/sector indicators.
- Replication output: Difference-in-differences style estimates of non-oil tradable-sector response by governance capacity.

## Institutional Spotlight
- Institution/person: Public Investment Fund (Saudi Arabia) governance model vs comparator SWFs.
- Why included: Directly illustrates the institutional design choices that condition spillover depth from state capital.

## Applied Lab Linkage
- Relevant lab: Lab 4 (MENA)
- Econometric method: Rentier-state dynamics and diversification
- Required code artifacts:
  - `labs/lab4_mena/code/scm_pipeline.py` (planned)
  - `labs/lab4_mena/code/event_study_spillover.py` (planned)

## Open Questions/Risks
- Project-level SWF data quality and comparability are uneven.
- Attribution is difficult when reforms and capital deployment occur simultaneously.
- External oil-price shocks can dominate medium-run identification windows.

