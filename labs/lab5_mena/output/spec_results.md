# Lab 4 MENA SCM Spec Comparison

Run date: 2026-02-25
Panel: `data/processed/lab4/lab4_mena_estimation_panel_2000_2024_2026-02-23.csv`
Outcome: `outcome_main` (WDI GDP-per-capita growth, annual %)
Method: Synthetic Control (SLSQP + projected-gradient fallback), in-space and in-time placebos

---

## Baseline Specs

| Spec | Treated | Interv. Year | pre_yrs | post_yrs | Donors | pre_RMSPE | post_RMSPE | Ratio | Mean Gap (pp) | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| syr_2018 | SYR | 2018 | 18 | 7 | 9 | 10.38 | 4.20 | 0.41 | -3.33 | Pre-period contaminated by 2011 civil war onset; ratio < 1 indicates poor design. |
| lby_2014 | LBY | 2014 | 14 | 11 | 9 | 28.68 | 17.24 | 0.60 | -0.77 | 2011 revolution (-49%/+92% swing) distorts pre-fit; YEM-dominated synthetic is itself conflict-affected. |
| yem_2015 | YEM | 2015 | 15 | 10 | 9 | 5.66 | 17.88 | 3.16 | **-14.83** | Primary valid spec. Strong pre-fit; sharp post-divergence. Consistent with Saudi coalition intervention (Mar 2015). |

---

## Robustness: In-Space Placebos (rank-based p-values)

| Spec | In-Space Units | Baseline Ratio | Rank p-value | Interpretation |
|---|---:|---:|---:|---|
| syr_2018 | 10 | 0.58 | 0.70 | Indistinguishable from placebos; design invalid for 2018 cutoff. |
| lby_2014 | 10 | 0.87 | 0.70 | Indistinguishable from placebos; pre-period volatility undermines design. |
| yem_2015 | 10 | 4.32 | **0.10** | Only 1 of 10 placebo units has a ratio this large; strongest available inference with N=10. |

---

## Robustness: In-Time Placebos (SYR, LBY, YEM)

| Treated | True Year | Placebo Year | Placebo Ratio | Direction | Interpretation |
|---|---:|---:|---:|---|---|
| SYR | 2018 | 2014 | 0.61 | Ratio < true | 2014 placebo weaker than 2018; does not sharpen inference given baseline ratio < 1. |
| SYR | 2018 | 2020 | 0.73 | Ratio > true | No clear time-specific effect. |
| LBY | 2014 | 2016 | 0.62 | Ratio < true | Similar to baseline; no time-specific signal. |
| LBY | 2014 | 2019 | 0.59 | Ratio < true | Slightly smaller; no evidence of 2014-specific effect. |
| YEM | 2015 | 2013 | 6.13 | Ratio > true | Pre-2015 Houthi expansion already deteriorating; 2013 placebo partly spurious. |
| YEM | 2015 | 2018 | 0.26 | Ratio << true | Much smaller than 2015 baseline; supports 2015 as the structural break year. |

---

## Donor Pool Composition (top donors, weight > 5%)

| Spec | Donor | Weight |
|---|---|---:|
| syr_2018 | LBN | 0.48 |
| syr_2018 | SAU | 0.29 |
| syr_2018 | JOR | 0.22 |
| lby_2014 | YEM | 1.00 |
| yem_2015 | TUN | 0.64 |
| yem_2015 | SYR | 0.17 |
| yem_2015 | EGY | 0.12 |
| yem_2015 | LBY | 0.07 |

---

## Interpretation and Pedagogical Notes

**Yemen 2015 is the primary pedagogically valid specification.** The synthetic control (dominated by Tunisia and Egypt) tracks Yemen's GDP growth well through 2014 (pre_RMSPE = 5.66), then diverges sharply after the March 2015 Saudi coalition intervention. The mean post-treatment gap of -14.83 percentage points implies that Yemen's GDP growth was nearly 15 pp below its synthetic counterfactual on average across 2015-2024. The in-space rank p-value of 0.10 is the strongest inference available with 10 donor units.

**Syria 2018 illustrates a canonical SCM design failure.** Syria's civil war erupted in 2011 — seven years before the chosen intervention year. The pre-period therefore includes major conflict-driven GDP shocks, producing a noisy pre-fit (pre_RMSPE = 10.38). The post/pre ratio of 0.41 is below 1, meaning the synthetic control actually tracks Syria *better* in the post-period than in the pre-period — the opposite of what a valid treatment effect requires. This spec is useful in the Lab as a negative example: SCM requires a clean, conflict-free pre-period.

**Libya 2014 is intermediate.** The 2011 revolution (GDP growth: -49% in 2011, +92% in 2012) creates extreme pre-period volatility that the donor pool cannot replicate. The optimizer assigns 100% weight to Yemen — itself a conflict-affected country — which is a red flag for donor pool validity. A cleaner Libya specification might use 2019 (the Haftar offensive on Tripoli) with a pre-period beginning post-2013 to avoid the 2011 shock, but this leaves only 6 years of pre-treatment data.

**Donor pool note for YEM.** Syria (17% weight) and Libya (7% weight) are both conflict-affected donors. A robustness check excluding conflict-affected donors (restricting to EGY, JOR, MAR, SAU, TUN) is warranted for the final Lab writeup.
