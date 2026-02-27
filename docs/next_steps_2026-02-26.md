# Next Steps Plan (2026-02-26)

This document captures the current project state and prioritized next steps based on a full repository review.

---

## Current State Summary

### What's Done
- **Book structure:** Restructured to 16 chapters (from 15) with Asia split into East Asia (Part III-A) and South Asia (Part III-B), Ch 3 split into 3-A (Spatial Econometrics) and 3-B (Trade/Gravity), and 7 labs (from 6)
- **Chapter prose drafted — Wave A+B complete:** 8 chapter files, all substantially expanded beyond initial drafts:
  - Ch. 1 (~425 lines): full micro-foundations + Bangalore vs Kolkata opening case study (~900 words, 7 paragraphs)
  - Ch. 2 (~233 lines, slimmed): institutional toolkit, forward refs to regional chapters
  - Ch. 3-A (~559 lines): full spatial econometrics treatment
  - Ch. 3-B (~236 lines): full trade measurement and gravity treatment
  - Ch. 4 (~490 lines): USMCA/CHIPS core + IRA green industrial policy subsection + Mode 2 education + 2 SDC boxes
  - Ch. 5 (~420 lines): middle-income trap + Central American climate migration subsection + 2 SDC boxes
  - Ch. 13 (~375 lines): urbanization without industrialization + Sahel climate-migration + e-government + SDC box
  - Ch. 14 (~466 lines): AfCFTA/corridors + eco-tourism corridors + services protocol §14.5 + SDC box; renumbered §14.5→14.6, §14.6→14.7
- **Spatial Data Challenge boxes:** 6 boxes written across Waves A+B — Mode 3 FDI measurement gap (Ch 4), Remoteability estimation mismatch (Ch 4), Informal trade undercounting (Ch 5), Deindustrialization in heterogeneous services (Ch 5), GDP rebasing/gas flares/night-lights limits (Ch 13), Mirror statistics divergence (Ch 14)
- **Chapter specs:** All 18 specs detailed (Chs. 10 and 12 filled out 2026-02-26)
- **Services trade cross-cutting theme:** Fully integrated across outline, drafting plan, all detailed specs, and drafted chapters; AfCFTA services protocol prose now in Ch. 14
- **Editorial feedback integrated:** New outline with Pathways, Regional Diagnostics Dashboard, Spatial Data Challenge boxes, climate distributed into regions, tourism/education as recurring themes, gravity model consolidated
- **Lab 1 (Americas):** Complete — real-data SAR pipeline, 3 specification bundles, Bartik extension
- **Lab 2 (East Asia):** Scaffolded — real TiVA data wired, beta-convergence scaffold, smoke test passing
- **Lab 3 (South Asia):** Scaffolded — directory structure and README created
- **Lab 4 (Europe):** Scaffolded — real Eurostat NUTS-2 data wired, RDD scaffold, smoke test passing
- **Lab 5 (MENA):** Partially complete — estimation panel built, 3 SCM baselines, placebo/robustness checks
- **Lab 6 (Africa):** Scaffolded — Moran's I with permutation inference, synthetic data only
- **Lab 7 (Services):** Scaffolded — README with 4 exercises, code directory with planned scripts
- **Infrastructure:** 17 smoke tests passing (CI verified post-renumbering), GitHub Actions CI, requirements.txt, data storage policy
- **Data:** WDI, Comtrade, BTS, LPI, Eurostat NUTS-2, WIOD, TiVA, ACLED (count-only), UNHCR acquired; VIIRS and Afrobarometer template-only

### What's Not Done
- Chapters 6–12, 15–16 prose (9 remaining chapters)
- ~~Ch 3 prose needs splitting into 3-A and 3-B files~~ **Done** (2026-02-26)
- ~~Ch 2 prose needs slimming (path dependency to Ch 5, VoC to Ch 9, Windows to Ch 6)~~ **Done** (2026-02-26)
- ~~Ch 1 prose needs opening case study (Bangalore vs Kolkata)~~ **Done** (2026-02-26)
- ~~Companion chapter specs stubs~~ **Done** — all 18 specs now detailed (2026-02-26)
- ~~Spatial Data Challenge boxes (content specified, prose not written)~~ **Done for Waves A+B** — 6 boxes written across Chs 4, 5, 13, 14; remaining regions (Waves C–E) still needed
- Convergence Diagnostic figures for Chs 4 and 5 (placeholder only — requires actual data visualization)
- Lab 3 code implementation (4 planned scripts)
- Lab 7 code implementation (6 planned scripts)
- Lab 6 real-data validation (VIIRS/Afrobarometer acquisition)
- Pathways preface section and dependency diagram
- Regional Diagnostics Dashboard template
- Zero-install cloud targets (Colab/Codespaces)
- ACLED row-level access confirmation
- Appendices A-C

---

## Prioritized Next Steps

### Tier 1: Critical Path

#### 1. Stabilize Part I After Restructuring
- **Completed (2026-02-26):** Bangalore vs Kolkata opening case study added to Ch 1 (7 paragraphs, ~900 words). Part I cross-references verified and fixed (Ch 1 conclusion updated to reference "Chapters 3-A and 3-B"). Discussion Question 6 added to Ch 1 linking back to case study.

#### 2. Complete Wave A (Americas): Expand Chs. 4-5
- **Completed (2026-02-26):** Ch 4 expanded with IRA/green industrial policy subsection, Mode 2 international education section, and two Spatial Data Challenge boxes (Mode 3 FDI measurement gap; remoteability estimation mismatch). Ch 5 expanded with Central American climate migration subsection and two Spatial Data Challenge boxes (informal trade undercounting; diagnosing premature deindustrialization in heterogeneous services).
- **Lab 1** is complete and validated.
- **Remaining:** Convergence Diagnostic figures (placeholder only — requires actual data visualization).

### Tier 2: High Priority

#### 3. Complete Wave B (Africa): Expand Chs. 13 and 14
- **Completed (2026-02-26):** Ch. 13 expanded with Sahel climate-migration subsection (Lake Chad, Dell/Jones/Olken, distress urbanization), e-government/digital-ID subsection (Rwanda Irembo, Nigeria BVN/NIN, Ganapati & Ravi), and Spatial Data Challenge box (GDP rebasing, gas-flare masking, VIIRS limits). Ch. 14 expanded with eco-tourism corridors subsection (KAZA UniVisa, Serengeti-Mara revenue sharing, Virunga conflict vulnerability), new §14.5 on the AfCFTA Protocol on Trade in Services (mobile money interoperability, Mode 3 banking, professional MRAs), and Spatial Data Challenge box (mirror statistics divergence, zero trade flows, PPML lower-bounds caveat). Sections renumbered: old §14.5 Lab 6 → §14.6; old §14.6 Conclusion → §14.7.

#### 4. ~~Fill Remaining Stub Chapter Specs (Chs. 10, 12)~~ **Done** (2026-02-26)
- Both specs now fully detailed with core thesis, key arguments, institutional variables, datasets, references, and lab linkage.

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
Week 1-2:  [DONE] Split Ch. 3 prose into 3-A and 3-B
           [DONE] Slim Ch. 2 (distribute to regional chapters)
           [DONE] Fill Ch. 10 and Ch. 12 specs
           [DONE] Add Ch. 1 opening case study (Bangalore vs Kolkata)
           [DONE] Part I cross-references verified and fixed
Week 3-4:  [DONE] Expand Ch. 4 to full draft (IRA, Mode 2 education, 2 SDC boxes)
           Acquire VIIRS, start Lab 6 real-data validation  ← next priority
Week 5-6:  [DONE] Expand Ch. 5 to full draft (climate migration, 2 SDC boxes)
Week 7-8:  Wave A review gate  ← pending
           [DONE] Expand Ch. 13 to full draft (Sahel climate, e-govt, SDC box)
           Build Lab 3 IT-BPO mapping script  ← deferred
Week 9-10: [DONE] Expand Ch. 14 to full draft (eco-tourism, services protocol §14.5, SDC box)
           Build Lab 7 gravity script + WTO data fetch  ← deferred
Week 11-12: Classroom pilot (Labs 1 + 6)
            Wave A+B review gate
```

---

## Open Risks

| Risk | Mitigation | Owner |
|---|---|---|
| ~~Ch 3 splitting complexity~~ | **Resolved** — split complete with section renumbering and lab ref updates | Done |
| ~~Ch 2 content redistribution~~ | **Resolved** — VoC and path-dependency condensed with forward refs | Done |
| ACLED row-level access denied | Continue with count-based proxy | Pending |
| VIIRS raster processing at 30+ countries | Pre-aggregated NOAA annual composites | Lab 6 |
| RBI/KLEMS data for Lab 3 | NASSCOM reports as fallback | Lab 3 |
| ~~Lab renumbering breaking CI~~ | **Resolved** — 17 smoke tests passing post-renumbering | Done |
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

### 2026-02-26: Part I Stabilization and Spec Completion
- Ch 3 split into ch03a_spatial_econometrics.md (559 lines) and ch03b_trade_measurement_gravity.md (236 lines, new)
- Ch 2 slimmed: VoC condensed to 3 paragraphs with forward ref to Ch 9; path-dependency case studies condensed with forward refs to Chs 5, 6
- All lab references in Ch 3-A updated to new numbering (Lab 3→4, Lab 4→5, Lab 5→6, Lab 6→7)
- Ch 10 spec filled: Eurozone crisis, post-socialist integration, Brexit, institutional mismatch
- Ch 12 spec filled: Conflict economics, refugee spatial shocks, youth bulge, climate-conflict nexus
- DRAFTING_PLAN and next_steps updated to reflect completed work

### 2026-02-26: Wave A Expansion (Ch 4, Ch 5) and Part I Stabilization
- **Ch 1** — Bangalore vs Kolkata opening case study (~900 words, 7 paragraphs covering IISc 1909, HAL 1940, STPI 1991, Left Front 1977–2011); cross-reference fixed to "Chapters 3-A and 3-B"; Discussion Question 6 added
- **Ch 4** — Added: IRA/green industrial policy subsection (Battery Belt, Appalachian coal, CBAM), Mode 2 international education section (Bound et al., Hausman), SDC box: Mode 3 FDI measurement gap, SDC box: Remoteability estimation mismatch (Dingel & Neiman)
- **Ch 5** — Added: Central American Dry Corridor climate migration subsection (Schlenker & Roberts, Dell et al., Hsiang et al.), SDC box: Informal trade undercounting (mirror statistics), SDC box: Diagnosing premature deindustrialization in heterogeneous services (RAIS, ENOE)

### 2026-02-26: Wave B Expansion (Ch 13, Ch 14)
- **Ch 13** — Added: "Climate Migration and the Sahel Urban Push" subsection (Lake Chad ~90% shrinkage, Fulani-farmer conflict, distress urbanization), "E-Government and the Spatial Politics of Digital Inclusion" subsection (Rwanda Irembo, Nigeria BVN/NIN, Ganapati & Ravi 2023), SDC box: GDP rebasing/gas-flare masking/VIIRS limits
- **Ch 14** — Added: "Eco-Tourism Corridors" subsection (KAZA UniVisa, Serengeti-Mara revenue sharing models, Virunga conflict vulnerability, climate risk), new §14.5 "The Protocol on Trade in Services" (GSMA $836B figure, mobile money interoperability, AU Continental Data Policy, Mode 3 banking via Equity Bank/Standard Bank, professional MRAs and WHO physician-density gap), SDC box: Mirror statistics divergence (>50% gap in 40% of African bilateral pairs, zero-flow bias, PPML lower bounds)
- **Ch 14 section renumbering:** old §14.5 Lab 6 → §14.6; old §14.6 Conclusion → §14.7

### 2026-02-26: Services Trade Integration
- Cross-cutting services trade theme integrated throughout the book
- 8 specs enriched; Ch. 13 and Ch. 16 specs fully written
- Prose updated in Chs. 1, 4, 5, 13
- Lab 7 scaffolded
