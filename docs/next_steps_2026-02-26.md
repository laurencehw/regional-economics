# Next Steps Plan (2026-02-26)

This document captures the current project state and prioritized next steps based on a full repository review.

---

## Current State Summary

### What's Done
- **Chapter prose drafted:** Chs. 1 (361 lines), 2 (267 lines), 3 (559 lines), 4 (352 lines), 5 (307 lines), 12 (265 lines) — 6 of 15 chapters
- **Chapter specs:** 11 of 15 detailed (Chs. 1–6, 8, 10, 12–13, 15); stub metadata for Chs. 7, 9, 11, 14
- **Services trade cross-cutting theme:** Fully integrated across outline (BOOK_OUTLINE.md), drafting plan, 8 chapter specs (Chs. 4–6, 8, 10, 12–13, 15), and 4 drafted chapters (Chs. 1, 4, 5, 12). Ch. 15 spec fully rewritten as services-trade synthesis chapter.
- **Lab 1 (Americas):** Complete — real-data SAR pipeline, 3 specification bundles, interaction terms, LPI friction proxy
- **Lab 2 (Asia):** Scaffolded — real TiVA data wired, β-convergence scaffold, smoke test passing
- **Lab 3 (Europe):** Scaffolded — real Eurostat NUTS-2 data wired, RDD scaffold, smoke test passing
- **Lab 4 (MENA):** Partially complete — estimation panel built, 3 SCM baselines, placebo/robustness checks
- **Lab 5 (Africa):** Scaffolded — Moran's I with permutation inference, synthetic data only
- **Lab 6 (Services):** Scaffolded — README with 4 exercises (services gravity, STRI tariff equivalents, TiVA servicification, cloud geography), code directory with planned scripts list. No code yet.
- **Infrastructure:** 17 smoke tests passing, GitHub Actions CI, requirements.txt, data storage policy, feedback action plan
- **Data:** WDI, Comtrade, BTS, LPI, Eurostat NUTS-2, WIOD, TiVA, ACLED (count-only), UNHCR acquired; VIIRS and Afrobarometer template-only

### What's Not Done
- Chapters 6–11, 13–15 prose (9 remaining regional and synthesis chapters)
- 4 companion chapter specs still stubs (Chs. 7, 9, 11, 14)
- Lab 6 code implementation (6 planned scripts: gravity, STRI, servicification, cloud mapper, WTO fetch, OECD STRI fetch)
- Lab 5 real-data validation (VIIRS/Afrobarometer acquisition)
- Lab 5 robustness runner (`run_real_africa_specs.py`)
- Zero-install cloud targets (Colab/Codespaces)
- ACLED row-level access confirmation
- Appendices A–C

---

## Prioritized Next Steps

### Tier 1: Critical Path (blocks everything downstream)

#### 1. Internal Review of Part I (Chs. 1–3)
- **Why now:** All three Part I chapters now have prose. The drafting plan requires Part I to be stable before proceeding. Ch. 3's code notebooks should co-evolve with the prose.
- **Action:** Review Part I for consistency of tone, notation, and pedagogical style. Pilot-test Ch. 3 code notebooks with a small group.
- **Co-deliverable:** Validate "Methods Mini-Primer" inserts planned for Chs. 8 and 11.

#### 2. Complete Wave A (Americas): Expand Chs. 4–5
- **Status:** Both chapters have initial prose drafts (Ch. 4: 352 lines, Ch. 5: 307 lines) including services trade content. Need expansion to target length (8,000–12,000 words), "Data in Depth" boxes, "Institutional Spotlight" sidebars, and end-of-chapter questions.
- **Lab 1** is complete and validated.
- **Review gate:** After Wave A, internal review + classroom pilot preparation.

### Tier 2: High Priority (unlocks Wave B and classroom pilot)

#### 3. Complete Wave B (Africa): Expand Ch. 12, Draft Ch. 13
- **Status:** Ch. 12 has initial prose (265 lines) with services content. Ch. 13 spec is now detailed (no longer a stub), so drafting can begin.
- **Deliverables:** Same template as Wave A chapters.

#### 4. Fill Remaining Companion Chapter Specs (Chs. 7, 9, 11, 14)
- **Why now:** These are all stubs (every field is "TBD"). Each needs a falsifiable thesis, key arguments, required datasets, anchor references, and institutional spotlight before its wave begins.
- **Priority order:** Ch. 7 (Wave C), Ch. 9 (Wave D), Ch. 11 (Wave E), Ch. 14 (Phase 3).
- **Note:** Ch. 13 and Ch. 15 specs were completed during services trade integration — down from 6 stubs to 4.

#### 5. Acquire VIIRS Data and Validate Lab 5 at Scale
- **Why now:** Lab 5 works on 8-country synthetic data but hasn't been tested on real African geographies. VIIRS is NASA open data with no licensing friction.
- **Target:** Run Moran's I on 30+ Sub-Saharan African countries. Test sensitivity to binary vs. border-length weighting and k-nearest-neighbor alternatives.
- **Co-deliverable:** Build `run_real_africa_specs.py` following Lab 1's robustness runner pattern.

### Tier 3: Important (supports quality and usability)

#### 6. Implement Lab 6 Code Scripts
- **Why now:** Lab 6 (Services Trade) is scaffolded with README and exercise design but has no executable code yet. Six scripts are planned.
- **Priority scripts:** `gravity_services_scaffold.py` (PPML gravity model) and `fetch_wto_services_trade.py` (data acquisition) should be built first to validate data pipeline feasibility.
- **Datasets needed:** WTO BOP bilateral services trade, OECD STRI scores, TiVA (already acquired for Lab 2), ECIPE Digital Trade Estimates.

#### 7. Add Zero-Install Cloud Execution Targets
- **Status:** P0 in feedback action plan, in progress since 2026-02-21.
- **Action:** Add Colab notebooks and/or Codespaces devcontainer for Labs 1 and 5, then extend to Labs 2–6.
- **Why it matters:** Eliminates student setup friction — the #1 barrier to classroom adoption.

#### 8. Confirm ACLED Row-Level Access
- **Status:** Request drafted, count-based access confirmed, row-level historical fields still redacted.
- **Action:** Follow up on licensing request. Lab 4's SCM pipeline currently uses country-year conflict counts; row-level event data would enable finer-grained treatment measures.

#### 9. Draft Appendix B: Data & Software Guide
- **Why now:** Phase 0 deliverable that forces resolution of remaining data-access and tooling decisions. Useful for classroom pilots. Should now include Lab 6 data sources (WTO BOP, OECD STRI).

### Tier 4: Deferred (Phase 3+)

- Chapters 6–7 prose (Wave C: Asia) — after Labs 2 TiVA pipeline is validated at scale
- Chapters 8–9 prose (Wave D: Europe) — after Ch. 3 bridge content is stable
- Chapters 10–11 prose (Wave E: MENA) — after ACLED access is resolved
- Chapters 14–15 prose (Phase 3: Synthesis) — after all regional parts
- Lab 6 remaining scripts (STRI tariff equivalents, servicification decomposition, cloud geography mapper)
- Appendices A and C (Phase 4)
- GIS base maps and publication-quality figures (Phase 4)

---

## Suggested Execution Sequence

```
Week 1-2:  Part I internal review gate (Chs. 1–3 prose now complete)
           Begin expanding Ch. 4 to target length
           Acquire VIIRS, start Lab 5 real-data validation
Week 3-4:  Expand Ch. 4 to full draft (boxes, sidebars, figures)
           Expand Ch. 5 to full draft
           Fill Ch. 7 spec (unblocks Wave C)
Week 5-6:  Wave A review gate
           Expand Ch. 12 to full draft
           Build Lab 6 gravity script + WTO data fetch
Week 7-8:  Draft Ch. 13 prose
           Fill Ch. 9 spec (unblocks Wave D)
           Build run_real_africa_specs.py
Week 9-10: Classroom pilot preparation (Labs 1 + 5)
           Wave A+B review gate
           Fill Ch. 11 spec (unblocks Wave E)
```

---

## Open Risks

| Risk | Mitigation | Owner |
|---|---|---|
| ACLED row-level access denied | Continue with count-based proxy; document limitation | Pending |
| VIIRS raster processing complexity at 30+ countries | Use pre-aggregated country-level radiance from NOAA annual composites | Lab 5 |
| Methods transition steepness (Labs 3-4) | Ch. 3 bridge subsection + mini-primers in Chs. 8/11 | Ch. 3 draft |
| Chapter prose pace (9 chapters remaining) | Template-then-scale: Chs. 4, 5, 12 provide initial drafts as templates | Drafting plan |
| Afrobarometer survey wave inconsistency | Document which rounds are used; test sensitivity across waves | Lab 5 |
| Lab 6 data access (WTO BOP, OECD STRI) | WTO BOP is public; OECD STRI requires OECD.Stat API access. TiVA already acquired for Lab 2. Fallback: ECIPE Digital Trade Estimates | Lab 6 |
| Services content coherence across chapters | Cross-reference table in DRAFTING_PLAN.md; Ch. 15 serves as synthesis | Drafting plan |

---

## Tests Status (2026-02-26)

All 17 smoke tests passing:
- Lab 1: 3 tests (pipeline, LPI proxy, interaction specs)
- Lab 2: 1 test (pipeline)
- Lab 3: 1 test (pipeline)
- Lab 4: 1 test (pipeline)
- Lab 5: 1 test (pipeline)
- Lab 6: No tests yet (code not implemented)

No regressions detected.

---

## Recent Changes Log

### 2026-02-26: Services Trade Integration
- **Scope:** Cross-cutting services trade theme integrated throughout the book
- **Outline:** BOOK_OUTLINE.md updated with services content for all 15 chapters + Lab 6
- **Specs updated:** Chs. 4, 5, 6, 8, 10, 12, 13, 15 (8 specs enriched with services trade arguments, datasets, and references)
- **Specs completed from stubs:** Ch. 13 (AfCFTA services protocol) and Ch. 15 (fully rewritten as services-trade synthesis)
- **Prose updated:** Ch. 1 (§1.5 spatial paradox of intangibility), Ch. 4 (new §4.5 APS geography), Ch. 5 (BPO/digital labor/tourism subsection), Ch. 12 (digital services frontier subsection)
- **New lab:** Lab 6 (Services Trade) scaffolded with README and code directory
- **Drafting plan:** Cross-reference table added; design principle #6 (services as cross-cutting thread)
- **Key references anchoring the thread:** Grossman & Rossi-Hansberg (2008), Kimura & Lee (2006), Head/Mayer/Ries (2009), Storper & Venables (2004), Haskel & Westlake (2018), Faber & Gaubert (2019), Suri & Jack (2016), Connell (2013), Diamond (2016)
