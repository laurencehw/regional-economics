# Lab 1 Real-Americas Gate Summary (2024)

## Input Coverage
- Panel file: `labs/lab1_americas/data/real_americas/panel_mapped.csv`
- Trade file: `labs/lab1_americas/data/real_americas/trade_mapped.csv`
- 2024 coverage:
  - Regions with non-missing `gdp_growth`: 41
  - Regions with non-missing `log_gdp_pc`: 41
  - Regions with non-missing `manufacturing_share`: 34
  - Regions with non-missing `border_delay_index`: 3

## Baseline Model
- Output: `labs/lab1_americas/output/real_americas_2024/model_summary.json`
- Method: `SAR_manual_ML`
- `n_obs`: 34
- `rho`: -0.003789
- X columns: `log_gdp_pc`, `manufacturing_share`

## Robustness Specs
- Output table: `labs/lab1_americas/output/real_americas_2024/specs/spec_results.csv`
- Baseline all-Americas: `n=34`, `rho=-0.003789`
- Macro-only all-Americas: `n=41`, `rho=0.032934`
- Border-imputed all-Americas: `n=34`, `rho=-0.001080`
- Raw USMCA-border spec: skipped (`n=1`)

## Interpretation Notes
- Near-zero unconditional `rho` is an informative result, not a failure: average spillovers appear weak when countries are pooled without institutional interactions.
- This motivates the next model tier: interact spatial exposure with institutional quality/friction terms to test conditional spillovers rather than forcing a global average effect.
- Border proxy is not yet suitable for full-Americas specification without imputation.
- Next improvement should prioritize a broader friction proxy (for example, World Bank LPI-based measures) with coverage beyond USA/CAN/MEX.
