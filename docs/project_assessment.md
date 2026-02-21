# Project Assessment: The New Regional Economics

**Date:** 2026-02-21 (revision 3)
**Reviewer:** Claude (automated structural review)
**Prior reviews:** 2026-02-18 (rev 1), 2026-02-21 (rev 2)

---

## Tracker: Issues Raised Across All Reviews

| # | Issue (rev raised) | Status | Evidence |
|---|---|---|---|
| 1 | Chapter specs empty for Parts II–VII (rev 1) | **Closed** | Chs 4, 6, 8, 10, 12 have full specs with falsifiable theses and institutional operationalization |
| 2 | Data acquisition not started (rev 1) | **Partially closed** | WDI, Comtrade, BTS acquired and validated; VIIRS/Afrobarometer wired to Lab 5 templates; 4 datasets remain outstanding |
| 3 | Risk of overextension (rev 1) | **Mitigated** | Phased plan with review gates and classroom pilot after Waves A+B; dual-track framing (modular publication) adopted in spirit |
| 4 | Lab code untested on real data (rev 1) | **Closed** | Lab 1 SAR on 34 economies; Lab 5 Moran scaffold runs on synthetic (15 regions). Both pass CI |
| 5 | Missing test infrastructure (rev 1) | **Closed** | 4 smoke tests (2 per lab), GitHub Actions CI, top-level pytest.ini |
| 6 | Institutional analysis underspecified (rev 1) | **Closed** | Each regional spec has named variable, measurement strategy, and spatial interaction term |
| 7 | Companion specs (5, 7, 9, 11, 13) still stubs (rev 2) | **Open** | Acknowledged as Phase 2 backlog |
| 8 | Near-zero rho interpretation needed (rev 2) | **Closed** | Gate summary updated with conditional-spillover framing |
| 9 | Code hygiene: hardcoded paths (rev 2) | **Mostly closed** | `build_lab1_americas_real_raw.py` now uses `Path.home()`; `scripts/README.md` still has Windows examples but docs are secondary |
| 10 | No top-level requirements.txt (rev 2) | **Closed** | Root `requirements.txt` added (numpy, pandas, scipy, requests, pycountry, pytest) |
| 11 | No data storage strategy (rev 2) | **Closed** | `docs/data_storage_strategy.md` established with rules, registry requirement, and pressure-point notes |
| 12 | Border proxy coverage (3/44) (rev 2) | **Open** | LPI prototype planned for 2026-03-07 |

**Summary:** 8 of 12 issues closed, 2 mitigated/partially closed, 2 open.

---

## What Changed Since Revision 2

### 1. Lab 5 (Africa) is now scaffolded with working code

Two new scripts (~470 lines total):

- **`prepare_lab5_inputs.py`** (209 lines) — maps VIIRS radiance, Afrobarometer governance, and adjacency edge-list CSVs into canonical panel and adjacency files. Handles both wide and long VIIRS formats. Symmetrizes adjacency links. Well-structured with the same pattern as Lab 1's preparation script.

- **`lab5_africa_moran_scaffold.py`** (261 lines) — computes global Moran's I on night-lights, then re-estimates on governance-residualized values. Features:
  - Permutation-based inference (configurable draws, seeded RNG)
  - Adjacency-based W construction with row standardization
  - OLS residualization before computing residual Moran's I
  - Synthetic data generator (15-region grid with spatially autocorrelated signal)
  - Smoke-test mode matching Lab 1's pattern

Both scripts follow Lab 1's architectural template: CLI arguments, JSON config-driven mappings, CSV/JSON outputs. The pattern is now validated across two labs.

### 2. Template data fixtures for Lab 5

Three example CSVs in `labs/lab5_africa/data/raw_templates/`:
- `viirs_example.csv` — 8 Sub-Saharan African countries, 2024, avg_radiance values
- `afrobarometer_example.csv` — 8 countries, 2024, trust_local_gov scores
- `adjacency_example.csv` — 12 border-sharing pairs with `shared_border_km` weights

Plus `source_mappings.json` connecting raw column names to canonical names. The Lab 5 README documents the full variable mapping and build checklist.

### 3. Smoke tests pass (4/4)

```
tests/test_lab1_pipeline_smoke.py::test_prepare_lab1_inputs_smoke    PASSED
tests/test_lab1_pipeline_smoke.py::test_sar_scaffold_smoke           PASSED
tests/test_lab5_pipeline_smoke.py::test_prepare_lab5_inputs_smoke    PASSED
tests/test_lab5_pipeline_smoke.py::test_moran_scaffold_smoke         PASSED
```

CI workflow updated to run both Lab 1 and Lab 5 tests.

### 4. Infrastructure improvements

- **Top-level `requirements.txt`** added (numpy, pandas, scipy, requests, pycountry, pytest)
- **`data_storage_strategy.md`** — clear rules on what stays in git vs. external, naming conventions, registry requirements, and identified pressure points (WIOD, VIIRS rasters)
- **`.gitignore` expanded** — now excludes `.pytest_cache/`, `.venv/`, `.tmp/`, `data/external/`, `data/staging/`
- **Hardcoded Windows path fixed** in `build_lab1_americas_real_raw.py` (now `Path.home() / ".claude" / "settings.json"`)
- **Feedback action plan** (`docs/feedback_action_plan_2026-02-21.md`) consolidates all reviewer feedback into a prioritized execution queue with target dates

### 5. Drafting plan updated

Key additions to `DRAFTING_PLAN.md`:
- Zero-install execution targets (Colab/Codespaces) added to Phase 0 deliverables
- Dataset fallback matrix added as Phase 0.6
- Data storage policy as Phase 0.7
- Wave B is now Africa (not Asia), reflecting Lab 5 as second proof-of-concept
- Cloud execution check added to per-wave process
- Post-Wave-A+B classroom pilot gate before proceeding to Waves C–E
- Methods mini-primer validation gate for Chs 8 and 11 before those chapters enter drafting

---

## Current State of Completion

### Foundation (~55% complete, up from ~50%)
- Book outline, drafting plan, and data storage strategy in place
- 8 of 15 chapter specs detailed (Chs 1–4, 6, 8, 10, 12)
- Feedback action plan with prioritized execution queue

### Implementation (~25% complete, up from ~20%)
- **Lab 1:** Complete real-data pipeline (fetch → map → estimate → robustness), 3 specs documented
- **Lab 5:** Complete scaffold (prepare → Moran's I with permutation inference), smoke-tested on synthetic data
- **Labs 2–4:** Scaffolded directories only
- 4 data acquisition scripts, 4 smoke tests, CI pipeline
- Top-level requirements, data storage policy, expanded .gitignore
- No chapter prose yet

---

## What's Working Well (New Observations)

### 1. The Lab 1 → Lab 5 pattern transfer worked cleanly

Lab 5 follows the same architectural template as Lab 1 — CLI-driven scripts, JSON-configured mappings, canonical CSVs, JSON model summaries — but adapts it for a fundamentally different method (Moran's I vs. SAR). This validates the claim that the Lab 1 pattern can scale to the remaining labs without major refactoring. The consistency will also help students: once they understand one lab's structure, the others follow.

### 2. Lab 5's framing is stronger than a data-scarcity workaround

The README and drafting plan now frame Lab 5 as a "nowcasting/on-time measurement" use case, not just "we use night-lights because GDP data are bad." This is the right framing — night-lights analysis is a legitimate measurement innovation used by development economists regardless of data availability (Henderson, Storeygard, and Weil 2012). The two-step estimation (raw Moran's I → governance-residualized Moran's I) directly operationalizes Chapter 12's thesis about service capacity conditioning urbanization outcomes.

### 3. The feedback action plan shows project management maturity

The `feedback_action_plan_2026-02-21.md` document does something most academic projects don't: it takes external feedback, prioritizes it (P0/P1/P2/P3), assigns target dates, and tracks status. The P0 items (student setup friction, dataset pipeline risk, early pedagogical validation) are the right priorities. The P3 acknowledgment of companion specs as Phase 2 backlog shows appropriate scope discipline.

### 4. Drafting order change (Africa → Wave B) is smart

Moving Africa to Wave B (right after Americas) rather than leaving it for later ensures it isn't treated as an afterthought — which is one of the book's stated design principles. It also means Labs 1 and 5 (the two implemented labs) get classroom-tested together before investing in the more data-dependent Labs 2–4.

---

## Remaining Issues and Recommendations

### Issue 1: Companion chapter specs (5, 7, 9, 11, 13) — still open

These are correctly deprioritized behind Part I prose and Wave A/B implementation, but they should be drafted before their respective waves begin. In particular, **Ch. 5 (Latin America middle-income trap)** needs a spec before Wave A can be considered complete.

**Recommendation:** Spec Ch. 5 alongside or immediately after Ch. 4 prose drafting. Its thesis should be distinct from Ch. 4 — if Ch. 4 is about USMCA compliance capacity, Ch. 5 should be about sub-national institutional fragmentation and premature deindustrialization patterns across LAC.

### Issue 2: Four datasets still unacquired (WIOD, NUTS-2, ACLED, UNHCR)

VIIRS and Afrobarometer have moved from "not started" to "in progress" via Lab 5 template wiring. The remaining four are correctly prioritized in the feedback action plan (WIOD/NUTS-2 as low-friction next targets, ACLED licensing as early-start item).

**Recommendation:** No change from rev 2 guidance. Execute per the action plan.

### Issue 3: Lab 5 needs real data to validate at scale

Lab 5 is in the same position Lab 1 was at rev 1 — mechanically correct on synthetic data, but untested with real VIIRS rasters and Afrobarometer surveys. The Moran's I implementation is clean, but the adjacency weighting strategy (shared border km) may behave differently with real African border geometries (some borders are extremely long — DRC shares borders with 9 countries).

**Recommendation:** When VIIRS and Afrobarometer data arrive, run Lab 5 on at least 30 Sub-Saharan African countries and check sensitivity of Moran's I to: (a) binary vs. border-length weighting, (b) k-nearest-neighbor alternatives, (c) different Afrobarometer survey waves. Document this as a robustness spec table parallel to Lab 1's `spec_results.md`.

### Issue 4: CI tests cover pipeline mechanics but not statistical output

The smoke tests check that scripts run and produce files with expected schema. They don't check that Moran's I is within plausible bounds, that the weight matrix is correctly symmetric, or that residualization actually reduces spatial autocorrelation on the synthetic data (it should, by construction). Adding a few statistical assertions to the smoke tests would catch regressions more effectively.

**Recommendation:** Add to `test_moran_scaffold_smoke`:
- Assert `moran_i > 0` on synthetic data (the data generator explicitly introduces positive spatial autocorrelation)
- Assert `residual_moran_i < moran_i` (governance-residualized clustering should be weaker than raw)
- Assert the weight matrix is symmetric

These are cheap checks that catch real bugs.

### Issue 5: No Lab 5 robustness runner yet

Lab 1 has `run_real_americas_specs.py` which orchestrates multiple specifications and produces a comparison table. Lab 5 doesn't have an equivalent yet. When real data arrives, you'll want to compare multiple W construction strategies and governance measures systematically.

**Recommendation:** Build `run_real_africa_specs.py` following the Lab 1 pattern, but defer until real data are available. The Lab 1 spec runner can serve as a direct template.

### Issue 6: Methods transition steepness (Labs 3 and 4)

The feedback action plan notes this (P2) and plans bridge content in Chapter 3 plus mini-primers in Chs 8 and 11. This is important — the jump from "here is a SAR model" and "here is Moran's I" to "here is a spatial RDD" and "here is synthetic control" is substantial. Students who can run Labs 1 and 5 will not automatically be ready for Labs 3 and 4.

**Recommendation:** When writing Chapter 3, include a dedicated subsection (~2 pages) on "From correlation to causation in spatial settings" that introduces the intuition for boundary discontinuities, donor pool construction, and parallel-trends-with-spillovers. This prepares students for Labs 3–4 without requiring them to learn the methods cold in those chapters.

---

## Revised Verdict

**The project is now in a credible early-execution phase.** The three previous reviews tracked a progression:

1. **Rev 1:** Good concept, but specs are empty, no real data, no tests — risk of producing descriptive surveys
2. **Rev 2:** Specs have analytical teeth, Lab 1 works on real data, tests exist — risk has shifted from conception to execution
3. **Rev 3:** Two labs implemented with a consistent reusable pattern, infrastructure professionalized (requirements, data strategy, CI, feedback tracking), drafting plan adapted based on feedback

The project is now past the "is this a real project?" threshold. Two of five labs work. Eight of fifteen chapter specs are substantive. The infrastructure can support scaling. The feedback action plan shows the author is integrating critique rather than just collecting it.

**What should happen next:**

1. **Write Chapter 1 prose.** This is the single most important next step. Specs and infrastructure are necessary but insufficient — the project needs to demonstrate it can produce readable, teachable text. Chapter 1 (micro-foundations of space) is the right test case: self-contained, well-specified, and foundational for everything else.

2. **Acquire VIIRS + run Lab 5 at scale.** Lab 5 is close to a real-data gate. VIIRS is NASA open data with no licensing friction. Running Moran's I on 30+ African countries validates the Lab 1→5 pattern transfer on real data and produces a publishable result.

3. **Draft Ch. 5 spec.** Completes Part II specification before Wave A prose drafting begins in earnest.

4. **Add statistical assertions to smoke tests.** Cheap investment that catches real regressions.

The remaining risks are execution pace and data access for Labs 2–4, not project viability.
