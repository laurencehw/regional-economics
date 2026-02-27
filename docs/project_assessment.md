# Project Assessment: The New Regional Economics

**Date:** 2026-02-27 (revision 5)
**Reviewer:** Claude (automated structural review)
**Prior reviews:** 2026-02-18 (rev 1), 2026-02-21 (rev 2), 2026-02-21 (rev 3), 2026-02-26 (rev 4)

---

## Tracker: Issues Raised Across All Reviews

| # | Issue (rev raised) | Status | Evidence |
|---|---|---|---|
| 1 | Chapter specs empty for Parts II–VII (rev 1) | **Closed** | All 18 specs detailed as of 2026-02-26 |
| 2 | Data acquisition not started (rev 1) | **Partially closed** | WDI, Comtrade, BTS, LPI, WIOD, TiVA, NUTS-2, ACLED (count-only), UNHCR acquired; VIIRS requires license (blocker), Afrobarometer template-only |
| 3 | Risk of overextension (rev 1) | **Mitigated** | Phased plan with review gates; Waves A+B complete before proceeding to Waves C–E |
| 4 | Lab code untested on real data (rev 1) | **Closed** | Lab 1 SAR on 34 economies; Lab 4 RDD on Eurostat NUTS-2; Lab 5 SCM with UNHCR/ACLED panel; Lab 6 real-data testing tracked separately under Issue #14 |
| 5 | Missing test infrastructure (rev 1) | **Closed** | 19 smoke tests, GitHub Actions CI, top-level pytest.ini; all passing |
| 6 | Institutional analysis underspecified (rev 1) | **Closed** | Each regional spec has named variable, measurement strategy, and spatial interaction term |
| 7 | Companion specs (5, 7, 9, 11, 13) still stubs (rev 2) | **Closed** | All 18 specs now detailed — Chs 5, 10, 12 filled in 2026-02-26 session |
| 8 | Near-zero rho interpretation needed (rev 2) | **Closed** | Gate summary updated with conditional-spillover framing |
| 9 | Code hygiene: hardcoded paths (rev 2) | **Mostly closed** | `build_lab1_americas_real_raw.py` now uses `Path.home()` |
| 10 | No top-level requirements.txt (rev 2) | **Closed** | Root `requirements.txt` in place; all 6 used packages listed |
| 11 | No data storage strategy (rev 2) | **Closed** | `docs/data_storage_strategy.md` established |
| 12 | Border proxy coverage (3/44) (rev 2) | **Closed** | LPI blend prototype completed; interaction specs run |
| 13 | No chapter prose (rev 3) | **Substantially closed** | 8+1 chapters drafted; Waves A+B complete with climate, services, and SDC box content; Ch 6 & Ch 7 first drafts |
| 14 | Lab 6 untested on real data (rev 3) | **Open** | Still synthetic only; VIIRS license is blocker |
| 15 | Stale cross-references after Ch 3 split and lab renumbering (rev 5) | **Closed** | 20+ stale "Chapter 3" → "Chapter 3-A/3-B" refs fixed; 5 wrong chapter xrefs fixed (Ch 12→13, Ch 6→8); 3 stale lab numbers fixed (Lab 5→6); old ch03_the_modern_spatial_toolkit.md deleted |
| 16 | Typos and grammatical errors (rev 5) | **Closed** | "a engine"→"an engine", "understated"→"understate", "incumbant"→"incumbent", "arterie"→"artery" |
| 17 | Section count mismatch in Ch 4 intro (rev 5) | **Closed** | "five sections" → "six sections"; missing §4.5 (services) added to roadmap |
| 18 | Numerical inconsistency in Ch 5 (rev 5) | **Closed** | "six CEPALSTAT countries" → "five" to match Data in Depth enumeration |
| 19 | Services trade undercounting stat discrepancy (rev 5) | **Closed** | Ch 3-A and Ch 3-B now use consistent "50–70 percent larger" framing |

**Summary:** 16 of 19 issues effectively closed (including 1 mostly closed and 1 substantially closed), 1 mitigated, 1 partially closed, 1 open.

---

## What Changed Since Revision 4

### 1. Wave A+B consistency review completed — 20+ cross-reference errors fixed

A systematic chapter-by-chapter review of all 8+1 drafted chapters uncovered significant stale cross-references from the Ch 3 split (Ch 3 → Ch 3-A/3-B) and the lab renumbering (old Labs 3-5 → new Labs 4-6). Fixes include:

- **20+ "Chapter 3" references** updated to "Chapter 3-A" or "Chapter 3-B" across Chs 4, 5, 13, 14
- **5 wrong chapter cross-references** fixed: Ch 1 referenced India as Ch 6 (should be Ch 8); Ch 5 referenced Diao/McMillan/Rodrik as Ch 12 (should be Ch 13); Ch 13 referenced the AfCFTA chapter as Ch 13 (should be Ch 14); Ch 14 referenced urbanization thesis as Ch 12 (should be Ch 13) in 4 places; Ch 14 referenced "Section 13.4" (should be Section 14.4)
- **3 stale lab numbers** fixed: Ch 5 "Lab 5" → "Lab 6" (Africa); data_storage_strategy "Lab 4/5" → "Lab 5/6"; Lab 4 output header "Lab 3" → "Lab 4"
- **Old ch03_the_modern_spatial_toolkit.md deleted** — the pre-split version was left behind and contained entirely stale references

### 2. Typos, grammatical errors, and inconsistencies fixed

- "a engine" → "an engine" (Ch 4)
- "will understated" → "will understate" (Ch 4)
- "incumbant" → "incumbent" (Ch 13)
- "arterie" → "artery" (Ch 14)
- "five sections" → "six sections" in Ch 4 intro (Section 4.5 on services was omitted from the roadmap)
- "six CEPALSTAT countries" → "five" in Ch 5 (matched to Data in Depth enumeration)
- Services undercounting statistic harmonized between Ch 3-A and Ch 3-B

### 3. DRAFTING_PLAN progress tracker updated

Phase 1 and Phase 2 status tables updated to reflect current line counts and completed content (SDC boxes, climate sections, services thread, cross-reference updates).

### 4. Statistical assertions already in place (contrary to rev 4 recommendation)

Rev 4 recommended adding statistical assertions to Lab 6 smoke tests. Upon audit, these were already present: `moran_i > 0`, `residual_moran_i < moran_i`, symmetric W matrix, row-standardized W, p-value bounds. All labs (1, 2, 4, 5, 6) have comparable statistical assertions in their smoke tests. The CI pipeline is stronger than rev 4 recognized.

### 5. Remaining known issues from review (deferred, not blocking)

- **Notation conflicts across chapters**: $\tau$ means iceberg transport costs in Ch 1 but temporal lag in Ch 3-A; $\lambda$ means manufacturing share in Ch 1 but spatial error parameter in Ch 3-A. These are standard in their respective contexts but should be flagged with notation notes in final manuscript.
- **Ch 2 services thread is weak**: The institutional chapter does not substantively connect its frameworks to services trade barriers. A paragraph in the VoC section linking CME/LME to service-sector specialization would close the gap.
- **Ch 2 section numbering inconsistent**: Uses mixed numbered/unnumbered headings unlike Chs 1, 3-A, 3-B.
- **Part I chapters lack Spatial Data Challenge boxes**: These are present in Waves A/B regional chapters but not in the foundational chapters. May be by design (SDC is a "regional" feature).
- **Ch 6 needs climate content and expanded services thread**: First draft is complete but lacks climate subsection and could strengthen services trade integration.

---

## What Changed Since Revision 3

### 1. Waves A and B prose complete — project crosses the "can it produce text?" threshold

The single most important milestone since Rev 3 is the completion of 8 chapter drafts, including full expansions of Chs 4, 5, 13, and 14. Rev 3 noted this as the "single most important next step" and it is now done. All four expanded chapters include:

- **Climate subsections:** Dry Corridor climate migration (Ch 5); Sahel urbanization push (Ch 13); eco-tourism climate vulnerability (Ch 14)
- **Services trade content:** Mode 2 international education (Ch 4); BPO/platform labor (Ch 5); M-Pesa and e-government (Ch 13); AfCFTA services protocol (Ch 14)
- **Spatial Data Challenge boxes:** 6 total (2 per chapter for Chs 4 and 5; 1 per chapter for Chs 13 and 14), each identifying a specific measurement gap in that region's empirical landscape

The text produced is consistent with the book's stated voice ("wry, scholarly, hopeful, wide-ranging") and analytical framework — falsifiable claims, institutional operationalization, cross-references to Part I methods, and lab linkages.

### 2. All 18 chapter specs now detailed

Rev 3 flagged Ch 5 as missing its spec ("the most important gap before Wave A begins"). All specs are now complete with: core thesis, 4–7 key arguments, institutional variable, datasets, references, lab linkage, climate content, and services trade thread.

### 3. Six Spatial Data Challenge boxes written

The editorial feedback integration called for SDC boxes in every chapter. Waves A and B now have 6:
- Ch 4: Mode 3 FDI measurement gap; Remoteability estimation mismatch
- Ch 5: Informal trade undercounting; Deindustrialization in heterogeneous services
- Ch 13: GDP rebasing, gas-flare masking, VIIRS limits
- Ch 14: Mirror statistics divergence in intra-African trade

### 4. Ch 14 services section adds analytical depth

The new §14.5 ("The Protocol on Trade in Services") is not merely a checklist of PTSS sectors. It connects the AfCFTA's formal services commitments to the digital-finance and banking-expansion realities already documented in Ch 13 (M-Pesa, Equity Bank), identifies the Mode 3 enclave risk as a parallel to Ch 5's resource-curse framing, and grounds the MRA discussion in the WHO physician-density data. This cross-chapter connective tissue strengthens the book's analytical coherence.

### 5. Section renumbering handled cleanly

Ch 14 needed §14.5 inserted (services protocol) between the functional corridors section (§14.4) and the Lab 6 analysis (§14.5→14.6). The renumbering was executed without breaking cross-references.

---

## Current State of Completion (Rev 4)

### Foundation (~85% complete, up from ~55% in rev 3)
- Book outline, drafting plan, and data storage strategy in place
- All 18 chapter specs detailed
- 6 Spatial Data Challenge boxes written
- Services cross-cutting thread integrated through prose

### Implementation (~35% complete, up from ~25%)
- **Lab 1:** Complete real-data pipeline, validated
- **Lab 4:** Eurostat NUTS-2 data wired, RDD scaffold passing
- **Lab 5:** Estimation panel built, SCM baselines and robustness complete
- **Lab 6:** Scaffold tested on synthetic data; real-data validation pending
- **Labs 2, 3, 7:** Scaffolded only
- 17 smoke tests passing; CI pipeline healthy

### Prose (~50% complete by chapter count, up from 0%)
- 8 of 16 chapters drafted (Chs 1, 2, 3-A, 3-B, 4, 5, 13, 14)
- All 8 are expanded beyond bare initial drafts; Waves A and B meet the per-wave process requirements (climate, services, SDC boxes, lab linkage, institutional analysis)
- 9 chapters remaining (Chs 6–12, 15–16) — Waves C through E plus synthesis

---

## What Changed Since Revision 2

### 1. Lab 6 (Africa) is now scaffolded with working code

Two new scripts (~470 lines total):

- **`prepare_lab6_inputs.py`** (209 lines) — maps VIIRS radiance, Afrobarometer governance, and adjacency edge-list CSVs into canonical panel and adjacency files. Handles both wide and long VIIRS formats. Symmetrizes adjacency links. Well-structured with the same pattern as Lab 1's preparation script.

- **`lab6_africa_moran_scaffold.py`** (261 lines) — computes global Moran's I on night-lights, then re-estimates on governance-residualized values. Features:
  - Permutation-based inference (configurable draws, seeded RNG)
  - Adjacency-based W construction with row standardization
  - OLS residualization before computing residual Moran's I
  - Synthetic data generator (15-region grid with spatially autocorrelated signal)
  - Smoke-test mode matching Lab 1's pattern

Both scripts follow Lab 1's architectural template: CLI arguments, JSON config-driven mappings, CSV/JSON outputs. The pattern is now validated across two labs.

### 2. Template data fixtures for Lab 6

Three example CSVs in `labs/lab6_africa/data/raw_templates/`:
- `viirs_example.csv` — 8 Sub-Saharan African countries, 2024, avg_radiance values
- `afrobarometer_example.csv` — 8 countries, 2024, trust_local_gov scores
- `adjacency_example.csv` — 12 border-sharing pairs with `shared_border_km` weights

Plus `source_mappings.json` connecting raw column names to canonical names. The Lab 6 README documents the full variable mapping and build checklist.

### 3. Smoke tests pass (4/4)

```
tests/test_lab1_pipeline_smoke.py::test_prepare_lab1_inputs_smoke    PASSED
tests/test_lab1_pipeline_smoke.py::test_sar_scaffold_smoke           PASSED
tests/test_lab6_pipeline_smoke.py::test_prepare_lab6_inputs_smoke    PASSED
tests/test_lab6_pipeline_smoke.py::test_moran_scaffold_smoke         PASSED
```

CI workflow updated to run both Lab 1 and Lab 6 tests.

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
- Wave B is now Africa (not Asia), reflecting Lab 6 as second proof-of-concept
- Cloud execution check added to per-wave process
- Post-Wave-A+B classroom pilot gate before proceeding to Waves C–E
- Methods mini-primer validation gate for Chs 9 and 12 before those chapters enter drafting

---

## Current State of Completion

### Foundation (~55% complete, up from ~50%)
- Book outline, drafting plan, and data storage strategy in place
- 8 of 16 chapter specs detailed (Chs 1–4, 6, 9, 11, 13)
- Feedback action plan with prioritized execution queue

### Implementation (~25% complete, up from ~20%)
- **Lab 1:** Complete real-data pipeline (fetch → map → estimate → robustness), 3 specs documented
- **Lab 6:** Complete scaffold (prepare → Moran's I with permutation inference), smoke-tested on synthetic data
- **Labs 2–5:** Scaffolded directories only
- 4 data acquisition scripts, 4 smoke tests, CI pipeline
- Top-level requirements, data storage policy, expanded .gitignore
- No chapter prose yet

---

## What's Working Well (New Observations)

### 1. The Lab 1 → Lab 6 pattern transfer worked cleanly

Lab 6 follows the same architectural template as Lab 1 — CLI-driven scripts, JSON-configured mappings, canonical CSVs, JSON model summaries — but adapts it for a fundamentally different method (Moran's I vs. SAR). This validates the claim that the Lab 1 pattern can scale to the remaining labs without major refactoring. The consistency will also help students: once they understand one lab's structure, the others follow.

### 2. Lab 6's framing is stronger than a data-scarcity workaround

The README and drafting plan now frame Lab 6 as a "nowcasting/on-time measurement" use case, not just "we use night-lights because GDP data are bad." This is the right framing — night-lights analysis is a legitimate measurement innovation used by development economists regardless of data availability (Henderson, Storeygard, and Weil 2012). The two-step estimation (raw Moran's I → governance-residualized Moran's I) directly operationalizes Chapter 13's thesis about service capacity conditioning urbanization outcomes.

### 3. The feedback action plan shows project management maturity

The `feedback_action_plan_2026-02-21.md` document does something most academic projects don't: it takes external feedback, prioritizes it (P0/P1/P2/P3), assigns target dates, and tracks status. The P0 items (student setup friction, dataset pipeline risk, early pedagogical validation) are the right priorities. The P3 acknowledgment of companion specs as Phase 2 backlog shows appropriate scope discipline.

### 4. Drafting order change (Africa → Wave B) is smart

Moving Africa to Wave B (right after Americas) rather than leaving it for later ensures it isn't treated as an afterthought — which is one of the book's stated design principles. It also means Labs 1 and 6 (the two implemented labs) get classroom-tested together before investing in the more data-dependent Labs 2–5.

---

## Remaining Issues and Recommendations

### Issue 1: Companion chapter specs (5, 7, 10, 12, 14) — still open

These are correctly deprioritized behind Part I prose and Wave A/B implementation, but they should be drafted before their respective waves begin. In particular, **Ch. 5 (Latin America middle-income trap)** needs a spec before Wave A can be considered complete.

**Recommendation:** Spec Ch. 5 alongside or immediately after Ch. 4 prose drafting. Its thesis should be distinct from Ch. 4 — if Ch. 4 is about USMCA compliance capacity, Ch. 5 should be about sub-national institutional fragmentation and premature deindustrialization patterns across LAC.

### Issue 2: Four datasets still unacquired (WIOD, NUTS-2, ACLED, UNHCR)

VIIRS and Afrobarometer have moved from "not started" to "in progress" via Lab 6 template wiring. The remaining four are correctly prioritized in the feedback action plan (WIOD/NUTS-2 as low-friction next targets, ACLED licensing as early-start item).

**Recommendation:** No change from rev 2 guidance. Execute per the action plan.

### Issue 3: Lab 6 needs real data to validate at scale

Lab 6 is in the same position Lab 1 was at rev 1 — mechanically correct on synthetic data, but untested with real VIIRS rasters and Afrobarometer surveys. The Moran's I implementation is clean, but the adjacency weighting strategy (shared border km) may behave differently with real African border geometries (some borders are extremely long — DRC shares borders with 9 countries).

**Recommendation:** When VIIRS and Afrobarometer data arrive, run Lab 6 on at least 30 Sub-Saharan African countries and check sensitivity of Moran's I to: (a) binary vs. border-length weighting, (b) k-nearest-neighbor alternatives, (c) different Afrobarometer survey waves. Document this as a robustness spec table parallel to Lab 1's `spec_results.md`.

### Issue 4: CI tests cover pipeline mechanics but not statistical output

The smoke tests check that scripts run and produce files with expected schema. They don't check that Moran's I is within plausible bounds, that the weight matrix is correctly symmetric, or that residualization actually reduces spatial autocorrelation on the synthetic data (it should, by construction). Adding a few statistical assertions to the smoke tests would catch regressions more effectively.

**Recommendation:** Add to `test_moran_scaffold_smoke`:
- Assert `moran_i > 0` on synthetic data (the data generator explicitly introduces positive spatial autocorrelation)
- Assert `residual_moran_i < moran_i` (governance-residualized clustering should be weaker than raw)
- Assert the weight matrix is symmetric

These are cheap checks that catch real bugs.

### Issue 5: No Lab 6 robustness runner yet

Lab 1 has `run_real_americas_specs.py` which orchestrates multiple specifications and produces a comparison table. Lab 6 doesn't have an equivalent yet. When real data arrives, you'll want to compare multiple W construction strategies and governance measures systematically.

**Recommendation:** Build `run_real_africa_specs.py` following the Lab 1 pattern, but defer until real data are available. The Lab 1 spec runner can serve as a direct template.

### Issue 6: Methods transition steepness (Labs 4 and 5)

The feedback action plan notes this (P2) and plans bridge content in Chapter 3 plus mini-primers in Chs 9 and 12. This is important — the jump from "here is a SAR model" and "here is Moran's I" to "here is a spatial RDD" and "here is synthetic control" is substantial. Students who can run Labs 1 and 6 will not automatically be ready for Labs 4 and 5.

**Recommendation:** When writing Chapter 3, include a dedicated subsection (~2 pages) on "From correlation to causation in spatial settings" that introduces the intuition for boundary discontinuities, donor pool construction, and parallel-trends-with-spillovers. This prepares students for Labs 4–5 without requiring them to learn the methods cold in those chapters.

---

## Revised Verdict (Rev 4)

**The project has crossed into its mid-execution phase.** The four reviews now track a clear progression:

1. **Rev 1:** Good concept, but specs are empty, no real data, no tests — risk of producing descriptive surveys
2. **Rev 2:** Specs have analytical teeth, Lab 1 works on real data, tests exist — risk has shifted from conception to execution
3. **Rev 3:** Two labs implemented with a consistent reusable pattern, infrastructure professionalized, drafting plan adapted
4. **Rev 4:** 8 chapters drafted with full content (climate, services, SDC boxes, lab linkage); Waves A and B complete; all specs detailed; 6 SDC boxes written

The project is past the "can it produce text?" threshold. Half the chapters exist in substantive form. The analytical voice is consistent. The services cross-cutting theme and climate integration are working as designed — they appear in the prose naturally, not as check-the-box additions.

**What should happen next:**

1. **Acquire VIIRS + run Lab 6 at scale.** This is now the blocking item for the classroom pilot. VIIRS is NASA open data with no licensing friction; once acquired, Lab 6 can be validated on 30+ countries and the SDC box in Ch 13 has a live computational counterpart.

2. **Wave A+B review gate.** Before drafting Wave C (East Asia: Chs 6–7), the 8 completed chapters should be reviewed for consistency of voice, notation, cross-references, and services thread coherence. The Drafting Plan calls for this gate explicitly.

3. **Draft Ch 6 (Flying Geese and Tech Ascendancy) prose.** Wave C begins with East Asia. The spec is detailed and the WIOD/TiVA data pipeline is scaffolded.

4. **Add statistical assertions to Lab 6 smoke tests.** Rev 3 recommended this; it remains undone. Three cheap assertions would make the CI pipeline meaningfully stronger: `moran_i > 0`, `residual_moran_i < moran_i`, and symmetric $W$.

The remaining risks are VIIRS acquisition and Lab 6 real-data validation, plus execution pace for Waves C–E. Project viability is not in question.

---

## Revised Verdict (Rev 3)

**The project is now in a credible early-execution phase.** The three previous reviews tracked a progression:

1. **Rev 1:** Good concept, but specs are empty, no real data, no tests — risk of producing descriptive surveys
2. **Rev 2:** Specs have analytical teeth, Lab 1 works on real data, tests exist — risk has shifted from conception to execution
3. **Rev 3:** Two labs implemented with a consistent reusable pattern, infrastructure professionalized (requirements, data strategy, CI, feedback tracking), drafting plan adapted based on feedback

The project is now past the "is this a real project?" threshold. Two of seven labs work. Eight of sixteen chapter specs are substantive. The infrastructure can support scaling. The feedback action plan shows the author is integrating critique rather than just collecting it.

**What should happen next (from Rev 3 — superseded by Rev 4 above):**

1. ~~Write Chapter 1 prose.~~ **Done.**
2. **Acquire VIIRS + run Lab 6 at scale.** Still the priority.
3. ~~Draft Ch. 5 spec.~~ **Done.**
4. **Add statistical assertions to smoke tests.** Still pending.
