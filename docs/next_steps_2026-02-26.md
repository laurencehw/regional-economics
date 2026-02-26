# Next Steps Plan (2026-02-26)

This document captures the current project state and prioritized next steps based on a full repository review.

---

## Current State Summary

### What's Done
- **Part I chapters:** Ch. 1 (343 lines) and Ch. 2 (267 lines) drafted as prose
- **Chapter specs:** 10 of 15 detailed (Chs. 1–6, 8, 10, 12, plus stub metadata for 7/9/11/13/14/15)
- **Lab 1 (Americas):** Complete — real-data SAR pipeline, 3 specification bundles, interaction terms, LPI friction proxy
- **Lab 2 (Asia):** Scaffolded — real TiVA data wired, β-convergence scaffold, smoke test passing
- **Lab 3 (Europe):** Scaffolded — real Eurostat NUTS-2 data wired, RDD scaffold, smoke test passing
- **Lab 4 (MENA):** Partially complete — estimation panel built, 3 SCM baselines, placebo/robustness checks
- **Lab 5 (Africa):** Scaffolded — Moran's I with permutation inference, synthetic data only
- **Infrastructure:** 17 smoke tests passing, GitHub Actions CI, requirements.txt, data storage policy, feedback action plan
- **Data:** WDI, Comtrade, BTS, LPI, Eurostat NUTS-2, WIOD, TiVA, ACLED (count-only), UNHCR acquired; VIIRS and Afrobarometer template-only

### What's Not Done
- Chapter 3 prose (completes Part I — prerequisite for all regional chapters)
- Chapters 4–15 prose (all regional and synthesis chapters)
- 5 companion chapter specs still stubs (Chs. 7, 9, 11, 13, 14/15)
- Lab 5 real-data validation (VIIRS/Afrobarometer acquisition)
- Lab 5 robustness runner (`run_real_africa_specs.py`)
- Zero-install cloud targets (Colab/Codespaces)
- ACLED row-level access confirmation
- Appendices A–C

---

## Prioritized Next Steps

### Tier 1: Critical Path (blocks everything downstream)

#### 1. Draft Chapter 3: The Modern Spatial Toolkit
- **Why now:** Completes Part I. The drafting plan requires Part I to be stable before any regional chapter. Ch. 3 operationalizes Chs. 1–2 into methods students will use.
- **Key content:** SAR/SEM/SDM estimation walkthrough, weight-matrix construction, spatial counterfactual intuition, "from correlation to causation" bridge subsection (prepares students for RDD in Lab 3 and SCM in Lab 4).
- **Co-deliverable:** Code notebooks for SAR/SEM/SDM should co-evolve with the prose per the drafting plan.
- **Spec exists:** Yes (`chapters/specs/ch03_modern_spatial_toolkit.md`)

#### 2. Draft Chapters 4–5 (Wave A: Americas)
- **Why now:** First regional section. Lab 1 is complete and validated. Both chapter specs are detailed (Ch. 4: USMCA compliance capacity; Ch. 5: Latin American middle-income trap).
- **Deliverables:** 8,000–12,000 words per chapter, "Data in Depth" boxes, "Institutional Spotlight" sidebars, end-of-chapter questions.
- **Review gate:** After Wave A, internal review + classroom pilot preparation.

### Tier 2: High Priority (unlocks Wave B and classroom pilot)

#### 3. Draft Chapters 12–13 (Wave B: Africa)
- **Why now:** Wave B was moved to Africa to ensure equal analytical seriousness and to get both proof-of-concept labs (1 and 5) classroom-tested together.
- **Prerequisite:** Ch. 13 spec is a stub — must be filled before drafting begins.
- **Deliverables:** Same template as Wave A chapters.

#### 4. Fill Companion Chapter Specs (Chs. 7, 9, 11, 13)
- **Why now:** These are all stubs (every field is "TBD"). Each needs a falsifiable thesis, key arguments, required datasets, anchor references, and institutional spotlight before its wave begins.
- **Priority order:** Ch. 13 first (needed for Wave B), then Ch. 7 (Wave C), Ch. 9 (Wave D), Ch. 11 (Wave E).

#### 5. Acquire VIIRS Data and Validate Lab 5 at Scale
- **Why now:** Lab 5 works on 8-country synthetic data but hasn't been tested on real African geographies. VIIRS is NASA open data with no licensing friction.
- **Target:** Run Moran's I on 30+ Sub-Saharan African countries. Test sensitivity to binary vs. border-length weighting and k-nearest-neighbor alternatives.
- **Co-deliverable:** Build `run_real_africa_specs.py` following Lab 1's robustness runner pattern.

### Tier 3: Important (supports quality and usability)

#### 6. Add Zero-Install Cloud Execution Targets
- **Status:** P0 in feedback action plan, in progress since 2026-02-21.
- **Action:** Add Colab notebooks and/or Codespaces devcontainer for Labs 1 and 5, then extend to Labs 2–4.
- **Why it matters:** Eliminates student setup friction — the #1 barrier to classroom adoption.

#### 7. Confirm ACLED Row-Level Access
- **Status:** Request drafted, count-based access confirmed, row-level historical fields still redacted.
- **Action:** Follow up on licensing request. Lab 4's SCM pipeline currently uses country-year conflict counts; row-level event data would enable finer-grained treatment measures.

#### 8. Draft Appendix B: Data & Software Guide
- **Why now:** Phase 0 deliverable that forces resolution of remaining data-access and tooling decisions. Useful for classroom pilots.

### Tier 4: Deferred (Phase 3+)

- Chapters 6–7 prose (Wave C: Asia) — after Labs 2 TiVA pipeline is validated at scale
- Chapters 8–9 prose (Wave D: Europe) — after Ch. 3 bridge content is stable
- Chapters 10–11 prose (Wave E: MENA) — after ACLED access is resolved
- Chapters 14–15 prose (Phase 3: Synthesis) — after all regional parts
- Appendices A and C (Phase 4)
- GIS base maps and publication-quality figures (Phase 4)

---

## Suggested Execution Sequence

```
Week 1-2:  Draft Ch. 3 prose + code notebooks
           Fill Ch. 13 spec (unblocks Wave B)
Week 3-4:  Draft Ch. 4 prose
           Acquire VIIRS, start Lab 5 real-data validation
Week 5-6:  Draft Ch. 5 prose
           Build run_real_africa_specs.py
           Part I internal review gate
Week 7-8:  Draft Ch. 12 prose
           Fill Ch. 7 spec (unblocks Wave C)
Week 9-10: Draft Ch. 13 prose
           Classroom pilot preparation (Labs 1 + 5)
           Wave A+B review gate
```

---

## Open Risks

| Risk | Mitigation | Owner |
|---|---|---|
| ACLED row-level access denied | Continue with count-based proxy; document limitation | Pending |
| VIIRS raster processing complexity at 30+ countries | Use pre-aggregated country-level radiance from NOAA annual composites | Lab 5 |
| Methods transition steepness (Labs 3-4) | Ch. 3 bridge subsection + mini-primers in Chs. 8/11 | Ch. 3 draft |
| Chapter prose pace (13 chapters remaining) | Template-then-scale: Waves A+B establish the pattern | Drafting plan |
| Afrobarometer survey wave inconsistency | Document which rounds are used; test sensitivity across waves | Lab 5 |

---

## Tests Status (2026-02-26)

All 17 smoke tests passing:
- Lab 1: 3 tests (pipeline, LPI proxy, interaction specs)
- Lab 2: 1 test (pipeline)
- Lab 3: 1 test (pipeline)
- Lab 4: 1 test (pipeline)
- Lab 5: 1 test (pipeline)

No regressions detected.
