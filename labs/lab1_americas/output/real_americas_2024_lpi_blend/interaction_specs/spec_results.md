# Real-Americas Lab 1 Institution-Interaction Spec Comparison

| Spec | Status | n_obs | Method | rho | beta(q x log_gdp) | beta(q x manuf) | X cols | Notes |
|---|---|---:|---|---:|---:|---:|---|---|
| quality_levels | ok | 34 | SAR_manual_ML | 0.004872 |  |  | log_gdp_pc,manufacturing_share,border_quality_index | Adds filled border-quality level (1 - friction). |
| quality_x_log_gdp | ok | 34 | SAR_manual_ML | -0.147778 | -3.698979 |  | log_gdp_pc,manufacturing_share,border_quality_index,quality_x_log_gdp | Tests whether GDP-level effect varies by border quality. |
| quality_x_manufacturing | ok | 34 | SAR_manual_ML | -0.017945 |  | 4.002805 | log_gdp_pc,manufacturing_share,border_quality_index,quality_x_manufacturing | Tests whether manufacturing share effect varies by border quality. |
| quality_full_interactions | ok | 34 | SAR_manual_ML | -0.093262 | -2.030848 | 2.448326 | log_gdp_pc,manufacturing_share,border_quality_index,quality_x_log_gdp,quality_x_manufacturing | Joint interaction model for conditional spillovers narrative. |
| quality_macro_interaction | ok | 41 | SAR_manual_ML | -0.033205 | -1.129836 |  | log_gdp_pc,border_quality_index,quality_x_log_gdp | Macro-only interaction spec with broader sample requirement. |
