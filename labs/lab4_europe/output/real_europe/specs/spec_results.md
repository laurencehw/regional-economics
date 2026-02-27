# Real-Europe Lab 4 RDD Spec Comparison

| Spec | Status | Year | n_obs | n_eff | tau | se | p-value | BW | Kernel | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| baseline_2022 | ok | 2022 | 298 | 269.2 | 1.9495 | 2.0329 | 0.3376 | 325971.3 | triangular | Primary specification. |
| narrow_bw_2022 | ok | 2022 | 289 | 241.9 | 1.0865 | 2.0586 | 0.5977 | 162985.6 | triangular | Tighter bandwidth — less bias, more variance. |
| wide_bw_2022 | ok | 2022 | 299 | 279.1 | 2.1674 | 2.0272 | 0.2850 | 488956.9 | triangular | Wider bandwidth — more precision, more bias. |
| uniform_2022 | ok | 2022 | 298 | 298.0 | 2.3752 | 2.0381 | 0.2439 | 325971.3 | uniform | Kernel sensitivity check. |
| baseline_2019 | ok | 2019 | 306 | 276.4 | 1.8793 | 0.7655 | 0.0141 | 325971.3 | triangular | Pre-COVID cross-section. |
| baseline_2020 | ok | 2020 | 306 | 276.4 | 1.6226 | 1.0048 | 0.1064 | 325971.3 | triangular | COVID year — structural break check. |
