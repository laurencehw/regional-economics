# Lab 1 Interaction Gate Summary (2024, LPI Blend)

## Objective
Test whether institutional quality (proxied by border/logistics quality) conditions estimated spillovers after fixing border-proxy coverage.

## Inputs
- Panel: `labs/lab1_americas/data/real_americas_lpi_blend/panel_mapped.csv`
- Trade: `labs/lab1_americas/data/real_americas_lpi_blend/trade_mapped.csv`
- Output table: `labs/lab1_americas/output/real_americas_2024_lpi_blend/interaction_specs/spec_results.csv`

## Coverage (2024)
- Regions in year slice: 41
- Non-missing `border_quality_index`: 41
- Non-missing `manufacturing_share`: 34

## Key Results
- `quality_levels`: `n=34`, `rho=0.004872`
- `quality_x_log_gdp`: `n=34`, `rho=-0.147778`, `beta(quality_x_log_gdp)=-3.698979`
- `quality_x_manufacturing`: `n=34`, `rho=-0.017945`, `beta(quality_x_manufacturing)=4.002805`
- `quality_full_interactions`: `n=34`, `rho=-0.093262`, `beta(quality_x_log_gdp)=-2.030848`, `beta(quality_x_manufacturing)=2.448326`
- `quality_macro_interaction`: `n=41`, `rho=-0.033205`, `beta(quality_x_log_gdp)=-1.129836`

## Interpretation
- Baseline pooled spillover remains small near zero when interactions are excluded.
- Interaction specifications produce materially different `rho` and non-zero interaction coefficients, consistent with the design premise that spillovers are conditional rather than uniform.
- Next step is inferential tightening (uncertainty intervals and robustness around interaction sign/magnitude) before prose claims.
