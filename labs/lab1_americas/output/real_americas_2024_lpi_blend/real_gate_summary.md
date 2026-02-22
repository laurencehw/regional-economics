# Lab 1 Real-Americas Gate Summary (2024, LPI Blend)

## Input Coverage
- Panel file: `labs/lab1_americas/data/real_americas_lpi_blend/panel_mapped.csv`
- Trade file: `labs/lab1_americas/data/real_americas_lpi_blend/trade_mapped.csv`
- 2024 coverage:
  - Regions with non-missing `gdp_growth`: 41
  - Regions with non-missing `log_gdp_pc`: 41
  - Regions with non-missing `manufacturing_share`: 34
  - Regions with non-missing `border_delay_index`: 28 (up from 3 in BTS-only gate)

## Robustness Specs (LPI Blend)
- Output table: `labs/lab1_americas/output/real_americas_2024_lpi_blend/specs/spec_results.csv`
- Baseline all-Americas: `n=34`, `rho=-0.000002`
- Macro-only all-Americas: `n=41`, `rho=0.032934`
- Border-imputed all-Americas: `n=34`, `rho=-0.000002`
- Raw USMCA-border spec: skipped (`n=1`)

## Delta vs Prior BTS-Only Gate
- Baseline `rho`: `-0.003789 -> -0.000002`
- Border-imputed `rho`: `-0.001080 -> -0.000002`
- Macro-only `rho`: unchanged (`0.032934`)
- Sample sizes for the three all-Americas specs were unchanged because `manufacturing_share` missingness remains the binding constraint.

## Interpretation Notes
- The broader friction proxy fixed a measurement-coverage weakness but did not create a strong unconditional spillover effect.
- This reinforces the strategy to estimate institution-conditioned spillovers next (interaction terms) rather than searching for a large pooled `rho`.
