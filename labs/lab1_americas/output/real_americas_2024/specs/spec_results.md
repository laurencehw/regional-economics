# Real-Americas Lab 1 Spec Comparison

| Spec | Status | n_obs | Method | rho | X cols | Notes |
|---|---|---:|---|---:|---|---|
| baseline_all | ok | 34 | SAR_manual_ML | -0.003789 | log_gdp_pc,manufacturing_share | Primary all-Americas baseline. |
| macro_only_all | ok | 41 | SAR_manual_ML | 0.032934 | log_gdp_pc | Less restrictive sample requirement. |
| border_imputed_all | ok | 34 | SAR_manual_ML | -0.001080 | log_gdp_pc,manufacturing_share,border_delay_index_filled | Border proxy mean-imputed outside USA/CAN/MEX (robustness only). |
| usmca_border_raw | skipped | 1 |  |  | log_gdp_pc,manufacturing_share,border_delay_index | Insufficient observations (n=1) |
