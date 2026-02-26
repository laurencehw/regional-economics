# Next Steps Plan (2026-02-26)

This document captures the current project state and prioritized next steps based on a full repository review.

---

## Current State Summary

### What's Done
- **Book structure:** Restructured to 16 chapters (from 15) with Asia split into East Asia (Part III-A) and South Asia (Part III-B), Ch 3 split into 3-A (Spatial Econometrics) and 3-B (Trade/Gravity), and 7 labs (from 6)
- **Chapter prose drafted:** Chs. 1 (361 lines), 2 (267 lines), 3 (559 lines, needs splitting), 4 (352 lines), 5 (307 lines), 13 (265 lines), 14 (326 lines) — 7 chapters
- **Chapter specs:** 15 of 18 detailed (Chs. 1–9, 11, 13–16 + 3-A, 3-B, 8); Chs. 10, 12 are stubs; Ch. 15 has partial content
- **Services trade cross-cutting theme:** Fully integrated across outline, drafting plan, all detailed specs, and drafted chapters
- **Editorial feedback integrated:** New outline with Pathways, Regional Diagnostics Dashboard, Spatial Data Challenge boxes, climate distributed into regions, tourism/education as recurring themes, gravity model consolidated
- **Lab 1 (Americas):** Complete — real-data SAR pipeline, 3 specification bundles, Bartik extension
- **Lab 2 (East Asia):** Scaffolded — real TiVA data wired, beta-convergence scaffold, smoke test passing
- **Lab 3 (South Asia):** Scaffolded — directory structure and README created
- **Lab 4 (Europe):** Scaffolded — real Eurostat NUTS-2 data wired, RDD scaffold, smoke test passing
- **Lab 5 (MENA):** Partially complete — estimation panel built, 3 SCM baselines, placebo/robustness checks
- **Lab 6 (Africa):** Scaffolded — Moran's I with permutation inference, synthetic data only
- **Lab 7 (Services):** Scaffolded — README with 4 exercises, code directory with planned scripts
- **Infrastructure:** 17 smoke tests (need re-verification after renumbering), GitHub Actions CI, requirements.txt, data storage policy
- **Data:** WDI, Comtrade, BTS, LPI, Eurostat NUTS-2, WIOD, TiVA, ACLED (count-only), UNHCR acquired; VIIRS and Afrobarometer template-only

### What's Not Done
- Chapters 6–12, 15–16 prose (9 remaining chapters)
- Ch 3 prose needs splitting into 3-A and 3-B files
- Ch 2 prose needs slimming (path dependency to Ch 5, VoC to Ch 9, Windows to Ch 6)
- Ch 1 prose needs opening case study (Bangalore vs Kolkata)
- 2 companion chapter specs still stubs (Chs. 10, 12); Ch. 15 partially filled
- Lab 3 code implementation (4 planned scripts)
- Lab 7 code implementation (6 planned scripts)
- Lab 6 real-data validation (VIIRS/Afrobarometer acquisition)
- Pathways preface section and dependency diagram
- Regional Diagnostics Dashboard template
- Spatial Data Challenge boxes (content specified, prose not written)
- Zero-install cloud targets (Colab/Codespaces)
- ACLED row-level access confirmation
- Appendices A-C

---

## Prioritized Next Steps

### Tier 1: Critical Path

#### 1. Stabilize Part I After Restructuring
- **Why now:** Ch 3 needs splitting into 3-A (spatial econometrics) and 3-B (trade/gravity). Ch 2 needs slimming. Ch 1 needs opening case study.
- **Action:** Split ch03 prose file into ch03a and ch03b. Move path dependency, VoC, and windows of opportunity content from Ch 2 prose to regional chapter stubs. Add Bangalore vs Kolkata case study to Ch 1.
- **Co-deliverable:** Verify all Part I prose is internally consistent after restructuring.

#### 2. Complete Wave A (Americas): Expand Chs. 4-5
- **Status:** Both chapters have initial prose drafts including services trade content. Need expansion to target length (30-40 pages), Data in Depth boxes, Spatial Data Challenge boxes, Institutional Spotlight sidebars, climate sections, and Convergence Diagnostic figures.
- **Lab 1** is complete and validated.

### Tier 2: High Priority

#### 3. Complete Wave B (Africa): Expand Chs. 13 and 14
- **Status:** Ch. 13 has initial prose (265 lines). Ch. 14 has initial prose (326 lines). Both need expansion to target length.

#### 4. Fill Remaining Stub Chapter Specs (Chs. 10, 12)
- **Priority order:** Ch. 10 (Wave D, Europe), Ch. 12 (Wave E, MENA). Ch. 15 has partial content but needs Institutional Spotlight and lab linkage.

#### 5. Acquire VIIRS Data and Validate Lab 6 at Scale

### Tier 3: Important

#### 6. Implement Lab 3 (South Asia) and Lab 7 (Services) Code
#### 7. Add Zero-Install Cloud Execution Targets
#### 8. Design Regional Diagnostics Dashboard Template
#### 9. Write Pathways Preface Section

### Tier 4: Deferred (Phase 3+)

- Chapters 6-7 prose (Wave C: East Asia)
- Chapter 8 prose (Wave C': South Asia)
- Chapters 9-10 prose (Wave D: Europe)
- Chapters 11-12 prose (Wave E: MENA)
- Chapters 15-16 prose (Phase 3: Synthesis)
- Appendices A and C
- GIS base maps and publication-quality figures

---

## Suggested Execution Sequence

```
Week 1-2:  Split Ch. 3 prose into 3-A and 3-B
           Slim Ch. 2 (distribute to regional chapters)
           Add Ch. 1 opening case study
           Part I internal review gate
Week 3-4:  Expand Ch. 4 to full draft (boxes, sidebars, climate)
           Acquire VIIRS, start Lab 6 real-data validation
Week 5-6:  Expand Ch. 5 to full draft
           Fill Ch. 10 spec (unblocks Wave D)
Week 7-8:  Wave A review gate
           Expand Ch. 13 to full draft
           Build Lab 3 IT-BPO mapping script
Week 9-10: Draft Ch. 14 prose
           Fill Ch. 12 spec (unblocks Wave E)
           Build Lab 7 gravity script + WTO data fetch
Week 11-12: Classroom pilot (Labs 1 + 6)
            Wave A+B review gate
```

---

## Open Risks

| Risk | Mitigation | Owner |
|---|---|---|
| Ch 3 splitting complexity | Careful section assignment; shared utility module | Phase 1 |
| Ch 2 content redistribution | Mark moved content with forward references | Phase 1 |
| ACLED row-level access denied | Continue with count-based proxy | Pending |
| VIIRS raster processing at 30+ countries | Pre-aggregated NOAA annual composites | Lab 6 |
| RBI/KLEMS data for Lab 3 | NASSCOM reports as fallback | Lab 3 |
| Lab renumbering breaking CI | Run full test suite after renumbering | Immediate |
| Services content coherence | Cross-reference table in DRAFTING_PLAN.md | Ongoing |

---

## Recent Changes Log

### 2026-02-26: Major Restructuring (Editorial Feedback)
- **Asia split:** Part III becomes Part III-A (East Asia, Chs. 6-7) + Part III-B (South Asia, Ch. 8)
- **Ch 3 split:** Ch 3 becomes Ch 3-A (Spatial Econometrics) + Ch 3-B (Trade/Gravity)
- **Ch 2 slimmed:** Path dependency to Ch 5, VoC to Ch 9, Windows to Ch 6
- **16 chapters, 7 labs** (was 15 chapters, 6 labs)
- **New specs:** Ch 3-A, Ch 3-B, Ch 8 (South Asia)
- **New lab:** Lab 3 (South Asia IT-BPO mapping)
- **All files renumbered:** Specs, chapters, labs, tests, scripts, processed data
- **BOOK_OUTLINE.md completely rewritten** for new structure
- **DRAFTING_PLAN.md completely rewritten** for new structure

### 2026-02-26: Services Trade Integration
- Cross-cutting services trade theme integrated throughout the book
- 8 specs enriched; Ch. 13 and Ch. 16 specs fully written
- Prose updated in Chs. 1, 4, 5, 13
- Lab 7 scaffolded
