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
- **Lab 2 (East Asia):** **Complete** — 8 scripts (convergence scaffold, prepare inputs, run specs, DVA trajectory plotter, convergence comparison table, fetch TiVA electronics, DVA decomposition, trade network visualizer); 9 tests passing
- **Lab 3 (South Asia):** **Complete** — concentration scaffold + prepare inputs; 3 tests passing
- **Lab 4 (Europe):** **Complete** — RDD scaffold + prepare inputs + real-data specs; 4 tests passing
- **Lab 5 (MENA):** **Complete** — SCM baseline + robustness pipeline + 5 visualization/analysis scripts (gap plotter, placebo distribution, donor weights, comparison table, conflict event study); 8 tests passing
- **Lab 6 (Africa):** Scaffolded — Moran's I with permutation inference, synthetic data only; VIIRS fetch script built; 4 tests passing. Real VIIRS data blocked on EOG license
- **Lab 7 (Services):** **Complete** — 7 scripts (PPML estimator, gravity scaffold, STRI tariff equivalent, servicification decomposition, cloud geography mapper, 2 fetch scripts); 5 tests passing
- **Infrastructure:** 37 smoke tests passing, GitHub Actions CI, requirements.txt, data storage policy
- **Data:** WDI, Comtrade, BTS, LPI, Eurostat NUTS-2, WIOD, TiVA, ACLED (count-only), UNHCR acquired; VIIRS and Afrobarometer template-only

### What's Not Done
- ~~Chapters 6–12, 15–16 prose (9 remaining chapters)~~ **Done** — all 16 chapters have expanded prose (~9,000–11,600w each)
- ~~Ch 3 prose needs splitting into 3-A and 3-B files~~ **Done** (2026-02-26)
- ~~Ch 2 prose needs slimming (path dependency to Ch 5, VoC to Ch 9, Windows to Ch 6)~~ **Done** (2026-02-26)
- ~~Ch 1 prose needs opening case study (Bangalore vs Kolkata)~~ **Done** (2026-02-26)
- ~~Companion chapter specs stubs~~ **Done** — all 18 specs now detailed (2026-02-26)
- ~~Spatial Data Challenge boxes (content specified, prose not written)~~ **Done for Waves A+B** — 6 boxes written across Chs 4, 5, 13, 14; remaining regions (Waves C–E) still needed
- ~~Lab 3 code implementation~~ **Done** (2026-02-28)
- ~~Lab 7 code implementation~~ **Done** (2026-02-28)
- ~~Pathways preface section and dependency diagram~~ **Done** — `chapters/preface_pathways.md`
- ~~Appendices A-C~~ **Done** — all three appendices complete
- ~~Bibliography incomplete entries~~ **Done** — 0 incomplete entries remaining
- Convergence Diagnostic figures for Chs 4 and 5 (placeholder only — requires actual data visualization)
- Lab 6 real-data validation (VIIRS/Afrobarometer acquisition)
- Regional Diagnostics Dashboard template
- Zero-install cloud targets (Colab/Codespaces)
- ACLED row-level access confirmation
- GIS maps and publication-quality figures
- Index preparation
- Final manuscript proofread

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
- **Completed (2026-02-26):** `scripts/fetch_viirs_africa.py` built. Supports `--smoke-test` (synthetic 54-country panel) and `--local-tif` (real NOAA/EOG VNL v2.1 GeoTIFF). Also builds Africa adjacency edge list from Natural Earth boundaries (`--write-adjacency`). Three new tests added to `test_lab6_pipeline_smoke.py` (19/19 passing). rasterio 1.5.0 + geopandas 1.1.1 already installed.
- **Remaining:** Download real VIIRS VNL v2.1 rasters from eogdata.mines.edu (requires registration). Files are ~200-500 MB/year. Run `python scripts/fetch_viirs_africa.py --local-tif VNL_YYYY.tif --year YYYY` for each year (2015-2023 recommended for panel depth). Afrobarometer licensing still pending.

### Tier 3: Important

#### 6. ~~Implement Lab 3 (South Asia) and Lab 7 (Services) Code~~ **Done** (2026-02-28)
#### 7. Add Zero-Install Cloud Execution Targets
#### 8. Design Regional Diagnostics Dashboard Template
#### 9. ~~Write Pathways Preface Section~~ **Done** — `chapters/preface_pathways.md`

### Tier 4: All Chapter Prose Complete

- ~~Chapter 6 prose~~ **COMPLETE** (~10,964w)
- ~~Chapter 7 prose~~ **COMPLETE** (~11,618w)
- ~~Chapter 8 prose (Wave C': South Asia)~~ **COMPLETE** (~10,622w)
- ~~Chapters 9-10 prose (Wave D: Europe)~~ **COMPLETE** — Ch 9 ~10,356w, Ch 10 ~10,877w
- ~~Chapters 11-12 prose (Wave E: MENA)~~ **COMPLETE** — Ch 11 ~10,423w, Ch 12 ~9,894w
- ~~Chapters 15-16 prose (Phase 3: Synthesis)~~ **COMPLETE** — Ch 15 ~9,981w, Ch 16 ~11,295w
- ~~Appendices A-C~~ **COMPLETE**
- GIS base maps and publication-quality figures — not started
- Index preparation — not started

---

## Suggested Execution Sequence

```
Week 1-2:   [DONE] Split Ch. 3, slim Ch. 2, fill specs, add Ch. 1 case study
Week 3-6:   [DONE] Expand Chs. 4-5, 13-14 (Waves A+B)
Week 7-8:   [DONE] Expand Chs. 6-8 (Waves C/C'), complete Labs 2-3
Week 9-10:  [DONE] Expand Chs. 9-12 (Waves D/E), complete Labs 4-5
Week 11-12: [DONE] Expand Chs. 15-16, complete Lab 7, appendices, bibliography
            [DONE] Structural standardization, consistency review
--- Current: Phase 4 (Apparatus and Production) ---
Next:       Complete Lab 6 (visualization scripts on synthetic data)
            Acquire VIIRS real data, validate Lab 6 at scale
            GIS maps and publication-quality figures
            Regional Diagnostics Dashboards
            Index preparation
            Final manuscript proofread
            Zero-install cloud targets (Colab/Codespaces)
            Classroom pilot (Labs 1 + 6)
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
| ~~Lab renumbering breaking CI~~ | **Resolved** — 37 smoke tests passing | Done |
| Services content coherence | Cross-reference table in DRAFTING_PLAN.md | Ongoing |
| Lab 6 real data | VIIRS fetch script built; blocked on EOG license/download | Lab 6 |

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

### 2026-02-28: Wave D Prose Expansion (Chs 9-10)
- **Ch 9** expanded from ~6,126w to ~10,400w (+4,241w):
  - Introduction: Bratislava/Prešov vignette, per-capita transfer humanization, Ch 10 forward cross-ref
  - §9.1: CME inequality ratios (Hamburg:Mecklenburg 1.8:1 vs London:Blackpool 4:1), Sparkassen (380) and Fraunhofer (76) as spatial policy instruments, French intermediate case (Schmidt 2002, Paris 31% GDP), Nordic expansion (Sweden Gini 0.12 vs UK 0.28, Nokia/Finland flexicurity), DME forward ref
  - §9.2: Becker et al. heterogeneity (tertiary education threshold), Rodríguez-Pose & Fratesi spending decomposition (infrastructure vs human capital), Boldrin-Canova counterfactual detail, political economy of transfers, freedom of movement as organic "people" strategy, Austin/Glaeser/Summers non-employment, Barca Report institutional traps, US comparison
  - §9.3: Foray/David/Hall European Paradox, Basque Country (Mondragon 80K, 9% R&D), Lower Austria bioeconomy, Calabria 12-priority failure, Foray "me-too" (80% listed health/biotech), institutional paradox
  - §9.4: Bologna scale (5.6M mobile students), Romania brain drain (15%), Dutch English programs (200→1,600), Parey & Waldinger causal evidence, Erasmus top-20 city concentration, Brexit/Turing Scheme loss
  - §9.5: EC 1.8% GDP gain estimate (~€300B), tariff-equivalent (45% professional services), legal services fragmentation, EU-US productivity gap, Digital Single Market geo-blocking/VAT
  - §9.6: RDD identification detail, institutional heterogeneity extension, spatial spillover concern
  - Data in Depth: PPS measurement caveats, spatial lag student exercise
  - ERDF Spotlight: additionality principle, climate conditionality (30% threshold)
  - Conclusion: NEG framework connection, polycentric financial geography, Ch 10 transition
- **Ch 10** expanded from ~5,484w to ~10,900w (+5,402w):
  - Introduction: Castellón urbanizaciones vignette, Ch 1-2 analytical framework cross-ref
  - §10.1: Krugman (1993) OCA warning, convergence play (600→20bp spreads, current accounts Spain 10%/Greece 15%/Germany +6%), OCA endogeneity failure (4% vs 30% mobility), internal devaluation spatial mechanism, Italy lost generation (quarter-century zero growth, Lombardy 8% vs Calabria 23%), Basque resilience comparison, emigration (500K Greeks, 700K Spaniards, 1M Italians), Portugal recovery, doom loop mechanism (Ireland 40% GDP), Draghi institutional improvisation, Fiscal Compact procyclicality, NGEU governance (€750B, 527 milestones), US fiscal federalism comparison (30¢ vs 5¢), Balassa-Samuelson SDC expansion
  - §10.2: FDI scale (€200B cumulative, >50% foreign-owned mfg), Nölke/Vliegenthart DME, Czech auto spatial granularity (Mladá Boleslav/Nošovice/Kolín), EV transition threat (2,000→200 parts), wage convergence (20→35-40%), re-shoring/automation phase, Poland 430K SSC workers, Warsaw Mokotów detail (Goldman/JPMorgan/Samsung), Kraków BPO→R&D trajectory, mfg-services labor competition, Poland resilience (only EU state avoiding 2008-09 recession)
  - §10.3: Brexit timing/COVID overlap, TCA services omission, Goodwin/Heath education decomposition, Los et al. Sunderland paradox, Springford synthetic control (5% GDP loss), regulatory divergence, NI Protocol dual-market, Rodríguez-Pose comparative geography of discontent (Le Pen, AfD, Fidesz), McCann fiscal centralization (UK 5% vs Germany 23%), Levelling Up assessment, Ch 4 Rust Belt comparison
  - Data in Depth: ecological inference caveat, spatial lag student exercise
  - ECB Spotlight: governance tension (20 NCBs), TPI (2022), Weidmann resignation
  - Conclusion: Mezzogiorno as sobering case, deeper-vs-heterogeneity choice, defense/security dimension (Ukraine), Ch 11 transition
- **Tests:** 25/25 passing
- **Documentation:** DRAFTING_PLAN.md Phase 2 table updated

### 2026-03-02: Lab 2 + Lab 5 Completion, Bibliography Cleanup
- **Lab 2 (East Asia):** Complete — 8 scripts total (convergence scaffold, prepare inputs, run specs, DVA trajectory plotter, convergence comparison table, fetch TiVA electronics, DVA decomposition, trade network visualizer); 9/9 tests passing
- **Lab 5 (MENA):** Complete — added 5 visualization/analysis scripts (scm_gap_plotter, placebo_distribution_plotter, donor_weight_visualizer, scm_comparison_table, conflict_event_study); all support `--run-smoke-test` mode; 8/8 tests passing
- **Bibliography:** All incomplete entries resolved (was 7 incomplete, now 0)
- **Real SCM data:** 3 real-data SCM specifications run (YEM 2015, SYR 2018, LBY 2014) with outputs in `labs/lab5_mena/output/real_scm_baseline/`
- **Tests:** 37/37 passing (up from 32)
- **Lab status:** 6 of 7 labs complete (Lab 6 Africa remains scaffolded, blocked on VIIRS license)
- **Documentation:** DRAFTING_PLAN.md, next_steps, MEMORY.md updated
