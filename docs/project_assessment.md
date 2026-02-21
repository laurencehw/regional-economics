# Project Assessment: The New Regional Economics

**Date:** 2026-02-21 (revision 2)
**Reviewer:** Claude (automated structural review)
**Prior review:** 2026-02-18 (revision 1)

---

## Summary of Changes Since First Review

The first assessment (2026-02-18) identified six structural issues. Four have been substantially addressed:

| Issue | Status | Evidence |
|---|---|---|
| 1. Chapter specs empty for Parts II–VII | **Addressed** | Chs 4, 6, 8, 10, 12 now have full specs with falsifiable theses, institutional variable operationalization, and lab linkages |
| 2. Data acquisition not started | **Partially addressed** | WDI, Comtrade, and BTS acquired for Lab 1 scope (3 of 9 datasets). 6 remain outstanding |
| 3. Risk of overextension | Not yet addressed | Scope unchanged at 15 chapters |
| 4. Lab code untested on real data | **Addressed** | SAR estimated on 34 Americas economies with 3 robustness specifications |
| 5. Missing test infrastructure | **Addressed** | pytest smoke tests + GitHub Actions CI added |
| 6. Institutional analysis underspecified | **Addressed** | Each updated chapter spec now has an explicit "Institutional Variable Operationalization" section |

---

## Current State of Completion

### Foundation (~50% complete, up from ~30%)
- Full book outline (7 parts, 15 chapters)
- Detailed chapter specifications for Chapters 1–3 (theoretical foundations)
- Detailed chapter specifications for Chapters 4, 6, 8, 10, 12 (one lead chapter per region)
- Drafting plan with 5 phases and review gates
- Directory scaffolding for all 15 chapters and 5 labs

### Implementation (~20% complete, up from ~5–10%)
- Lab 1 has a complete real-data pipeline: fetch → map → estimate → robustness specs
- 4 data acquisition scripts (`fetch_wdi_lab1.py`, `fetch_bts_border_crossings.py`, `build_lab1_americas_real_raw.py`, `derive_lab1_bts_border_proxy.py`)
- Real data for 44 Americas economies, 25 years (2000–2024), 895 bilateral trade flows
- 3 SAR robustness specifications run and documented
- Smoke test suite + GitHub Actions CI pipeline
- Labs 2–5 remain scaffolded but unimplemented
- No chapter prose written yet

---

## What's Working Well

### 1. Chapter specs now have analytical teeth
The five new regional specs each have a **falsifiable core thesis** rather than a topic description:

- **Ch. 4 (Americas):** "Reshoring gains concentrate where regulatory-compliance capacity and border-governance quality interact with network position — trade exposure alone doesn't predict upgrading."
- **Ch. 6 (Asia):** "Technology upgrading is institutionally engineered, not an automatic flying-geese sequence — state-coordination capacity drives value-added positioning."
- **Ch. 8 (Europe):** "Cohesion policy promotes convergence only above a threshold of regional administrative capacity — below it, transfers produce weaker productivity and stronger out-migration."
- **Ch. 10 (MENA):** "SWF-led diversification succeeds only with accompanying institutional reforms in procurement, labor mobility, and contestability — otherwise mega-projects create enclaves."
- **Ch. 12 (Africa):** "Urbanization raises productivity only where municipal service capacity converts density into lower transaction costs — otherwise density scales congestion and informality."

These are testable, specific, and differentiated from one another. Each chapter is now arguing something, not just describing a region.

### 2. Institutional variable operationalization is concrete
Each spec now specifies: (a) a named institutional variable, (b) how it's measured, and (c) a spatial interaction term. For example, Ch. 8 defines `absorption_capacity_rt` measured by cohesion-fund disbursement rates and QoG effectiveness indicators, interacted with treatment status and spatial lag. This is exactly the level of specificity needed to write code and prose.

### 3. Lab 1 now runs on real data at credible scale
- **44 Americas economies** in the panel (up from 6 synthetic)
- **34 observations** in the baseline cross-section (after requiring non-missing manufacturing_share)
- **895 bilateral trade flows** constructing the W matrix
- **3 robustness specifications** documented in a comparison table
- The rho estimate (-0.004 in baseline) is near zero and substantively interpretable — it says trade-weighted spatial spillovers in Americas GDP growth are weak in a simple cross-section, which is a plausible starting point for the argument that *institutional variables* are needed to explain heterogeneity

### 4. Test infrastructure exists
- `tests/test_lab1_pipeline_smoke.py` — 2 tests covering the preparation and estimation pipeline
- `.github/workflows/lab1-smoke-tests.yml` — CI on push to main and all PRs
- `pytest.ini` — configured

---

## Remaining Issues and Recommendations

### Issue 1: Five companion chapter specs are still stubs (Chs 5, 7, 9, 11, 13)

The "second" chapter in each regional part (the companion to the lead chapter) is still TBD. These chapters handle the trickier, more heterogeneous cases — Latin America's middle-income trap, ASEAN fragmentation, post-socialist transitions, fragile states, and AfCFTA corridors.

**Recommendation:** Draft these specs next, but do not hold up Part I prose writing for them. The lead chapter in each region is sufficient to establish the analytical framework; the companion can be specified while Part I is being written.

### Issue 2: Scope is still 15 chapters

The project hasn't been scoped down. This remains a risk, but the phased drafting plan with review gates provides some protection. The specs now have enough substance that individual chapters could stand alone as working papers if the full book stalls.

**Recommendation:** Adopt a dual-track framing: the full 15-chapter book is the aspiration, but each Part I–III unit (theory + one region) should be publishable independently as a self-contained module. This gives exit ramps and interim publication opportunities.

### Issue 3: Six datasets still unacquired (WIOD, NUTS-2, VIIRS, Afrobarometer, ACLED, UNHCR)

These block Labs 2–5 and chapters 6–13 prose that relies on empirical examples.

**Priority order by lab dependency and licensing risk:**

| Priority | Dataset | Blocks | Licensing Risk |
|---|---|---|---|
| 1 | WIOD / TiVA | Lab 2 (Asia) | Low — academic use |
| 2 | Eurostat NUTS-2 + GISCO | Lab 3 (Europe) | Low — open data |
| 3 | VIIRS night-lights | Lab 5 (Africa) | Low — NASA open |
| 4 | ACLED | Lab 4 (MENA) | **Medium — academic license, redistribution restrictions** |
| 5 | Afrobarometer | Lab 5 (Africa) | **Medium — check redistribution terms** |
| 6 | UNHCR | Lab 4 (MENA) | Low — open |

**Recommendation:** Acquire WIOD and NUTS-2 next (both low-friction, open data). Initiate ACLED and Afrobarometer license conversations early — they often take weeks to process.

### Issue 4: Lab 1 estimation reveals a substantive puzzle that needs to be discussed

The baseline rho is effectively zero (-0.004). This is stable across specifications (macro-only: +0.033, border-imputed: -0.001). This means either:

1. Trade-weighted spatial spillovers in Americas GDP growth genuinely are near zero in a single cross-section (plausible — the Americas are highly heterogeneous and a single year flattens dynamics)
2. The cross-sectional design lacks power — a panel SAR would be more appropriate
3. The W matrix (bilateral trade only) may not capture the relevant spatial linkage (FDI, migration, policy diffusion)

This isn't a problem — it's an opportunity. A near-zero baseline rho sets up the Chapter 4 argument perfectly: *unconditional* spatial spillovers are weak, but *conditional on institutional variables* (compliance capacity, border governance), spillovers become significant. That's the whole thesis.

**Recommendation:** Document this interpretive logic explicitly. Run a panel specification (multiple years) as an additional robustness check. Consider augmenting W with FDI or migration flows if data are available.

### Issue 5: Some code hygiene items

- **Hardcoded Windows path** in `build_lab1_americas_real_raw.py` line 27: `DEFAULT_SETTINGS_PATH = r"C:\Users\lwils\.claude\settings.json"` and in `scripts/README.md` usage examples (`C:\Python314\python.exe`). These should use platform-independent paths or environment variables for portability.
- **Output paths in `spec_results.csv`** contain absolute Windows paths (`G:\My Drive\book drafts\...`). These should be relative paths for reproducibility.
- **No `.gitignore` for large raw data files.** The BTS crossings file is 72,540 rows (likely several MB). As the project acquires WIOD, VIIRS rasters, and Afrobarometer surveys, raw data will quickly exceed what should be committed to git. Consider git-LFS or a data-fetch-on-demand strategy documented in the README.
- **`requests` dependency** in `fetch_wdi_lab1.py` not in any top-level requirements file; Lab 1's `requirements.txt` includes it, but the scripts in `scripts/` have no corresponding requirements file.

**Recommendation:** Add a top-level `requirements.txt` covering all scripts. Decide on a data storage strategy (git-LFS vs. fetch scripts + `.gitignore`) before acquiring larger datasets.

### Issue 6: Border-delay proxy has limited geographic coverage

The BTS border-friction proxy only covers USA, CAN, and MEX (3 of 44 regions). Mean-imputation to the other 41 countries is acknowledged as a robustness check, not a valid specification. For Chapter 4's thesis about border governance and compliance capacity, this needs to be expanded.

**Recommendation:** Consider supplementary friction proxies with broader coverage — World Bank Logistics Performance Index (LPI), Doing Business trading-across-borders indicators, or port-throughput data. These would give friction measures for all 44 Americas economies and make the border-governance interaction term testable at full scale.

---

## Revised Verdict: Is This Worth Proceeding?

**Yes, more confidently than before.** The project has addressed the most important concerns from the first review:

- The regional chapters now argue specific, testable claims rather than describing topics
- The institutional analysis is operationalized, not just invoked
- The Lab 1 pipeline works on real data at scale
- The near-zero baseline rho is interpretively useful, not a failure

**What has changed in my assessment:**

Previously, the risk was that the project would produce descriptive surveys indistinguishable from existing textbooks. That risk has diminished substantially. The institutional-variable operationalization section in each spec — with named variables, measurement strategies, and spatial interaction terms — commits each chapter to a specific empirical argument. This is the book's distinctive contribution: not just "here is regional economics by region" but "here is how institutions condition spatial spillovers, tested region by region with the most appropriate method."

**Remaining risks:**
1. **Execution timeline.** The scope is still large (15 chapters). The phased plan with gates helps, but the companion chapters (5, 7, 9, 11, 13) still need specification.
2. **Data access for Labs 2–5.** Six datasets remain unacquired. ACLED and Afrobarometer licensing are the highest-risk items.
3. **Prose quality.** Specs are strong, but specs are not chapters. The gap between a well-specified argument and a well-written chapter is substantial. Part I prose drafting will be the real test.

**Suggested next steps (updated priority sequence):**

1. Begin Chapter 1 prose drafting — test the writing workflow
2. Acquire WIOD/TiVA and Eurostat NUTS-2 (low-friction, unblock Labs 2–3)
3. Draft companion specs for Chapters 5 and 7 (complete Parts II–III specifications)
4. Run Lab 1 with panel specification (multi-year) and consider augmenting W matrix
5. Add a top-level `requirements.txt` and a data storage strategy
6. Initiate ACLED and Afrobarometer license applications
7. Build Lab 2 (Asia MRIO) as the second fully implemented lab
