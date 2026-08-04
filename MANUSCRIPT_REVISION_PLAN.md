# Manuscript Revision Plan

**Manuscript:** *The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods*  
**Baseline review:** 6.5/10 (2026-08-02)  
**Target:** 8.5+/10 and external-review readiness  
**Scope:** Technical accuracy, factual reliability, lab reproducibility, pedagogy, and production quality

## Status Legend

- [ ] Not started
- [~] In progress
- [x] Complete
- [!] Blocked or requires specialist review

## Definition of Done

The manuscript is ready for external review when:

1. Every P0 and P1 item below is complete.
2. Every quantitative claim has a traceable source, vintage, unit, and geographic definition.
3. Published findings, author calculations, lab results, synthetic illustrations, and hypotheses are visibly distinguished.
4. All equations and empirical specifications have passed specialist review.
5. Every lab implements the method promised in the text and documentation.
6. The full test suite passes in a pinned environment on Windows and Linux.
7. All chapters pass a final citation, terminology, cross-reference, figure, and copyediting audit.

---

## P0 — Technical and Reproducibility Blockers

### T1. Chapter 1: Classical and New Economic Geography

- [x] Correct Weber terminology: distinguish the material index from the transport-cost-minimizing location.
- [x] Reconcile central-place theory's firm-level scale thresholds with the later claim that it assumes away increasing returns.
- [x] Remove backward/forward input-output linkages from the description of the basic Krugman (1991) model, or explicitly introduce the model extension that contains intermediate inputs.
- [x] Attribute re-dispersion near free trade to the appropriate extensions rather than the basic two-region Krugman model.
- [x] Reserve “functional region” for integrated labor-market/commuting systems; describe Silicon Valley–Hsinchu as a transnational production or innovation network.
- [x] Add a compact assumptions/results table separating Krugman (1991), Helpman (1998), Puga (1999), and multi-region extensions.

**Acceptance criteria:** Model assumptions, mechanisms, and comparative statics match the cited papers; terminology is consistent with standard graduate texts.

### T2. Chapter 3-A: Spatial Econometrics

- [x] Remove any claim that row-standardizing \(W\) makes \(\rho\) an elasticity.
- [x] Rewrite the SEM discussion: distinguish spatially correlated errors from HAC-style covariance correction.
- [x] Separate geographic boundary RDD from eligibility-threshold RDD.
- [x] Remove causal or additive interpretations of residualized Moran's \(I\).
- [x] Replace “smaller estimates are more credible” reasoning with identification-based evaluation.
- [x] Verify SAR/SDM direct, indirect, and total-effect definitions against Appendix A and code.

**Acceptance criteria:** A spatial econometrician can reproduce each interpretation from the stated model and assumptions.

### T3. Chapter 3-B: Gravity and Trade Measurement

- [x] Correct PPML interpretation for coefficients on logged continuous regressors.
- [x] Repair the STRI specification: importer-only STRI cannot be estimated with importer fixed effects in a cross-section.
- [x] Correct Mode 4 measurement; do not treat remittances as a direct Mode 4 measure.
- [x] Correct TiVA accounting so DVX is not added as a mutually exclusive component beside DVA.
- [x] Distinguish BOP exports from foreign-affiliate sales and state when aggregation is inappropriate.
- [x] Separate Grossman–Rossi-Hansberg task trade from adjacent routineness/offshorability frameworks.
- [x] Audit multilateral-resistance notation against conventional exporter/importer indexing.

**Acceptance criteria:** All worked calculations are numerically correct and each showcased regression is identified.

### T4. Regional Empirical Methods

- [~] Chapter 7: corrected the half-life transformation and removed unsupported real-data findings; re-estimation awaits a compatible TiVA DVA-share denominator and committed real-data outputs.
- [x] Chapter 9: represent Cohesion Policy assignment as a fuzzy treatment-intensity design where appropriate.
- [x] Chapter 13: remove “share attributable to governance” interpretations of residual Moran's \(I\).
- [x] Chapter 14: distinguish adjacency effects from domestic-versus-international border effects.
- [x] Chapter 14: remove GDP regressors when absorbed by exporter/importer fixed effects.
- [x] Revise exercises so students test identification assumptions rather than confirm predetermined findings.

**Acceptance criteria:** Each design has a stated estimand, assignment mechanism, identifying assumptions, inference method, and limitations.

### T5. Appendix A Mathematical Audit

- [x] Correct SAR partial-effect dimensions and notation.
- [x] Correct the RDD HC1 sandwich covariance expression.
- [x] Add the finite-sample correction and tail definition for Moran permutation inference.
- [x] Reconcile all convergence half-life formulas with lab implementations.
- [ ] Check parameter domains, matrix dimensions, and notation against Chapters 3-A/3-B.

**Acceptance criteria:** Independent derivation review completed; equations agree with tests and code.

### R1. Reproducibility and Test Suite

- [x] Diagnose and repair `test_ch04_figures_smoke` DBF read failure.
- [x] Determine whether the DBF failure is a corrupt cache, dependency/platform issue, or script defect.
- [x] Pin the supported Python and geospatial dependency versions.
- [ ] Run all tests on Windows and Linux.
- [ ] Record test count, runtime, environment, and known data-network requirements in Appendix B.

**Current baseline:** The prior failure came from non-atomic shapefile sidecar writes inside the synced workspace. Natural Earth archives are now downloaded atomically to a local temporary cache and read directly from ZIP. On Windows/Python 3.14.0, all 108 collected tests pass in 225.6 seconds. Linux validation remains required. The run emits one environment warning from `pytest-asyncio` about its future default fixture-loop scope.

**Acceptance criteria:** Clean full-suite run in both supported environments with no undocumented warnings.

### R2. Lab–Text Alignment

- [x] Lab 7: implement structural PPML with exporter and importer fixed effects.
- [x] Lab 7: add an identified STRI design using sector, bilateral, or time variation.
- [x] Lab 7: add robust/clustered inference, zero handling, and convergence diagnostics.
- [x] Verify Lab 2's method and description are consistent across outline, prose, README, and code. Share panel + year-FE subgroup/LOO specs are reproducible under `labs/lab2_asia/output/real_asia/specs_share/`; Chapter 7 treats estimates as imprecise, not established findings. Optional C26 electronics share pull and small-cluster inference remain.
- [x] Reconcile every lab README checklist with actual implementation and outputs.
- [~] Label synthetic demonstrations separately from real-data replications. Labs 1–7 READMEs now distinguish synthetic vs author-calculation outputs; Lab 4/6/7 summaries record `mode`.

**Acceptance criteria:** A method-to-code matrix shows that every advertised estimator and robustness check is implemented and tested.

---

## P1 — Factual Reliability and Analytical Balance

### F1. Claim-Level Fact Audit

- [~] Build a chapter-by-chapter claim ledger: claim, source, year, unit, geography, transformation, and verification status. Seed ledger in `CLAIM_LEDGER.md` covers corrected high-risk clusters; quantitative backlog remains for Ch. 4/6/8/11/14/16.
- [~] Correct or qualify known high-risk claims:
  - [x] USMCA steel/aluminum rules and border-restriction dates.
  - [x] Shenzhen 1979 population baseline and Hong Kong income comparison.
  - [x] Hukou treatment in resident-population statistics.
  - [x] Indian students abroad and IIT graduate migration.
  - [x] Basque Country R&D share.
  - [x] History of EU collective borrowing.
  - [x] Pre-2018 GCC corporate taxation.
  - [x] Mohamed Bouazizi's education.
  - [x] AfCFTA Secretariat location.
  - [x] South Africa's share of SADC GDP and SACU distribution.
  - [x] Climate-cost and migration projections in Chapter 15.
- [~] Replace unstable contemporary values with dated statements and a declared data cutoff. The manuscript-wide cutoff is now July 1, 2026; chapter-level dating audit remains.

**Acceptance criteria:** No precise factual claim lacks a source and vintage; all corrections are reflected in figures and exercises.

### F2. Citation Integrity

- [~] Run a bidirectional audit: every in-text citation appears in the bibliography and every bibliography entry is referenced or intentionally retained. Heuristic auditor added (`scripts/audit_citations.py`); 17 core scholarly gaps filled; remaining flags are mostly agency/date false positives pending manual pass.
- [ ] Add pinpoint references for important quantitative claims.
- [ ] Triangulate corporate, government, advocacy, and industry-association claims with independent sources.
- [x] Correct the Boeing bibliography/source collision.
- [x] Remove self-reported bibliography completeness claims until independently verified.
- [ ] Add dataset identifiers, access dates, and table/series references to data notes.

**Acceptance criteria:** Automated audit passes, followed by manual verification of all P0/P1 claims.

### A1. Causal Discipline and Competing Explanations

- [x] Rewrite monocausal Korea framing to include initial conditions, occupation, aid, security, land reform, and developmental-state policy.
- [x] Add alternative explanations to Ruhr–Donbas, Pittsburgh–Detroit, science parks, Latin American deindustrialization, Gulf diversification, Syrian conflict, and African urbanization.
- [~] Distinguish descriptive comparison, correlation, quasi-experimental evidence, structural inference, and interpretation. Evidence boxes now cover science parks, Ruhr–Donbas, Pittsburgh–Detroit, LAC deindustrialization, Gulf diversification, Syria, and African urbanization.
- [x] Add an “Evidence and alternatives” summary to each major case listed in A1.
- [x] Treat DVA as one imperfect upgrading indicator alongside productivity, wages, occupations, ownership, patents, and supplier depth.

**Acceptance criteria:** No central causal conclusion relies solely on descriptive comparison or unqualified cross-sectional evidence.

### A2. Scenario and Policy Currency

- [x] Replace bare CMIP6 RCP terminology with SSP–RCP combinations.
- [x] Add source, scenario, base year, and uncertainty interval to climate projections.
- [~] Add legal-status dates to trade and digital-regulation comparisons. AfCFTA ROO, RCEP EIF/membership, CHIPS awards, Gulf SWF figures, and Ch. 16 digital-regime comparisons now tied to the July 1, 2026 cutoff.
- [~] Update the US, EU, China, India, AfCFTA, RCEP, AI-chip, and platform-policy descriptions to the declared cutoff. Core dating notes added in Ch. 4, 7, 11, 14, and 16; chapter-by-chapter refresh of every statute citation remains.
- [x] Remove or clarify “rules of origin for services.”

**Acceptance criteria:** Every forward-looking table and policy statement has an “as of” date.

---

## P2 — Pedagogy, Coverage, and Production

### P1. Evidence Presentation

- [~] Label each empirical item as published evidence, author calculation, lab output, synthetic illustration, preliminary result, or hypothesis. Ch. 6/8/11 figure notes and Lab 2 evidence status now distinguish illustration vs author calculation.
- [~] Add uncertainty and sample/specification notes to all author calculations. Started on Ch. 6/8/11 figures and Lab 2 share specs.
- [ ] Add evidence-strength tables where competing findings are central.
- [~] Ensure calibrated figures cannot be mistaken for reproduced data. Explicit “illustrative / not exact reproduction” notes on Ch. 6 and 8 charts.

### P2. Regional Balance

- [~] Expand case-selection rationale in every regional part. Added selection notes in Ch. 5/8/11/13; remaining regional chapters can inherit the same pattern.
- [~] Broaden Latin American treatment of Central America and the Caribbean. CAFTA-DR / Caribbean comparative note in Ch. 5 (Dry Corridor already in body).
- [~] Broaden South Asian treatment beyond India and Bangladesh. Pakistan comparative note + existing Sri Lanka/SAARC material in Ch. 8.
- [~] Broaden MENA treatment beyond the GCC and Syria. Maghreb/Eastern Mediterranean note in Ch. 11; conflict MENA deferred to Ch. 12.
- [~] Add proportionate treatment of francophone West Africa, Central Africa, Ethiopia, Sudan, and current conflict/displacement cases. Francophone/Ethiopia note in Ch. 13; Sudan via Ch. 12.
- [x] Review whether Oceania and Central Asia need a dedicated comparative box or an explicit scope note. Explicit scope note already in `preface_pathways.md`.

### P3. Prose and Structure

- [~] Cut repeated framing and chapter conclusions by approximately 15–20%. Trimmed conclusions in Ch. 4–16 regional/synthesis set (plus earlier Ch. 6/8/11).
- [~] Reduce repeated use of “institutional thickness,” “binding constraint,” “spatial implication,” and formulaic transitions. Diversified filler uses across Ch. 3-B/4/6/8–10/12–16; keep conceptual “institutional thickness” where it is the framework term (esp. Ch. 2/12).
- [ ] Separate theory, evidence, illustration, and speculation visually.
- [ ] Break long paragraphs and sentences where argument structure is obscured.
- [x] Reconcile pathway workload estimates with actual chapter length. Added instructor workload note (~95–115k words / 17–21 pp/week); moved Pathway 1’s misplaced week-14 elective into Electives and gave Ch. 14/15 two-week slots.
- [x] Standardize discussion-question counts or remove the numerical promise. Preface now says “typically five to eight”; chapter sets standardized to six questions each.

### P4. Figures and Tables

- [~] Fix all label collisions and C-range figures identified in the editorial audit. Priority C/C- maps (Ch. 4/7/11/12) regenerated with offset/inset fixes; Ch. 9 figure order corrected (9.2 fan, 9.3 clubs).
- [x] Add a Gulf inset to the Chapter 11 map.
- [ ] Split Chapter 16's wide services-regime table.
- [ ] Use a muted, accessible, color-blind-safe palette.
- [~] Add source, vintage, method, and uncertainty notes to every figure. Regional/synthesis chapters (4–16) now carry expanded figure source notes; theory chapters pending if needed.
- [ ] Distribute figures through chapters rather than front-loading them.

### P5. Glossary, Index, and Cross-References

- [ ] Replace chapter-only index locators with page or section anchors.
- [~] Prevent bibliography/glossary-only and ambiguous regex matches from generating index entries. `generate_index.py` now omits bibliography scanning and drops apparatus-only hits; regenerated `subject_index.md` (267 terms).
- [~] Add subentries and curated “see/see also” links. Capstone see-also links added; fuller subentry pass still open.
- [x] Add missing capstone terms: stranded regions, climate migration, digital sovereignty, Splinternet, just transition, and related concepts.
- [~] Audit notation and definitions across chapters, glossary, appendices, and labs. Aligned Ch. 14 gravity MR terms to $$P_j,\Pi_i$$; Ch. 16 now states PPML+FE as preferred; glossary MR notation note added.
- [ ] Validate all internal links and chapter/lab references.

### P6. External Validation

- [ ] Recruit specialist reviewers for NEG, spatial econometrics, structural gravity, climate economics, and each regional part.
- [ ] Conduct classroom pilots of Chapters 3-A/3-B and Labs 4, 6, and 7.
- [ ] Log reviewer decisions and unresolved disagreements.
- [ ] Complete sensitivity review for conflict, migration, Indigenous rights, gender, and migrant-labor coverage.

---

## Work Order

1. T1 — Chapter 1 theory corrections.
2. T2/T3/T5 — methods chapters and mathematical appendix.
3. T4 — regional empirical designs.
4. R1/R2 — reproducibility and lab alignment.
5. F1/F2 — factual and citation audit.
6. A1/A2 — analytical balance and currency.
7. P1–P6 — pedagogy, coverage, production, and external validation.

## Revision Log

| Date | Item | Change | Verification |
|---|---|---|---|
| 2026-08-02 | Plan | Created consolidated revision plan from full-manuscript review | Baseline documented |
| 2026-08-02 | T1 | Corrected Weber terminology, NEG mechanisms and integration claims, functional-region terminology; added model-comparison table and Venables (1996) reference | Text and bibliography cross-check |
| 2026-08-02 | T2 | Corrected normalization, SEM, threshold-RDD, Moran residualization, and coefficient-credibility interpretations in Chapter 3-A | Targeted terminology search; Appendix audit remains |
| 2026-08-02 | T3 | Corrected PPML interpretation, STRI identification, Mode 4 measurement, FATS/BOP comparison, task-framework attribution, and TiVA accounting | Equation and collinearity review |
| 2026-08-02 | T5 | Corrected SAR/SDM effect dimensions, RDD HC1 covariance, and Moran permutation inference | Cross-checked against lab implementations |
| 2026-08-02 | T4 / T5 | Corrected percentage-point convergence half-life in Lab 2, tests, Appendix A, and Chapter 7; removed unsupported Chapter 7 subgroup results | 50 focused tests passed |
| 2026-08-02 | T4 | Reframed Chapter 9 as eligibility/fuzzy RDD, corrected Chapters 13–14 Moran interpretations, and replaced Chapter 14's adjacency-as-border specification with identified gravity designs | Targeted claim search |
| 2026-08-02 | R1 | Replaced synced-workspace shapefile cache with atomic local ZIP cache; removed partial sidecars | Chapter 4 figure smoke test passed |
| 2026-08-02 | R1 | Added missing geospatial/plotting dependencies, exact Windows lock, and versioned setup guidance | Python 3.14.0 environment captured |
| 2026-08-02 | R1 | Established a new full Windows reproducibility baseline | 108/108 tests passed in 225.6s |
| 2026-08-02 | F1 | Corrected ten known high-risk fact clusters across Chapters 4, 7–12, and 14; added authoritative sources and a July 1, 2026 information cutoff | Cross-checked against USTR, CBP, NBS China, Eustat, European Commission, IMF, AfCFTA, SADC, SACU, and UN-Habitat sources |
| 2026-08-02 | F1 / A2 | Rewrote Chapter 15 Groundswell and CMIP6 language as SSP–RCP scenarios with upper bounds, not forecasts; added Clement et al. (2021) | Checked against World Bank Groundswell Part 2 |
| 2026-08-02 | A1 / F2 | Softened Korea monocausal opening; fixed Boeing OSMnx/source-list collision; removed bibliography completeness self-claims | Targeted text and bibliography review |
| 2026-08-02 | A1 / A2 | Added non-institutional confounders to Ruhr–Donbas; clarified that RCEP “rules of origin for services” are preferential-qualification analogues, not goods ROO | Text consistency check |
| 2026-08-02 | A1 | Added competing explanations for Pittsburgh–Detroit, LAC deindustrialization, Gulf diversification, Syria, and African urbanization | Targeted chapter edits |
| 2026-08-02 | R2 | Lab 7 structural PPML with exporter/importer FE; identified sectoral STRI design; clustered SEs and zero diagnostics; README/status sync | Focused Lab 7 and PPML unit/smoke tests |
| 2026-08-02 | A1 | Added science-park alternatives (diaspora, market timing, Cold War access, branch-plant strategies) | Chapter 6 text review |
| 2026-08-02 | R2 | Reconciled Labs 1–6 READMEs; Lab 4 eligibility-threshold labeling; Lab 6 residual comparison de-causalized | Focused Lab 4/6 smoke tests |
| 2026-08-02 | R2 | Implemented Lab 2 `dva_share = EXGR_DVA/EXGR`, share-mode convergence with optional year FE, templates/tests; softened Ch. 7 Q5 | Lab 2 smoke/unit tests |
| 2026-08-03 | R2 | Fetched TiVA `EXGR`, rebuilt share panel (230/230), ran year-FE subgroup/LOO specs; aligned Ch. 7 estimand and evidence status; significance-gated `convergence_detected` | Lab 2 smoke tests; `specs_share` outputs |
| 2026-08-03 | F2 | Added citation auditor; filled 17 missing scholarly bibliography entries (Albouy, Baldwin–Taglioni, Cameron–Miller, Tabuchi, Viner, etc.); glossary Amin year aligned to 1994 | `data/processed/citation_audit.md` |
| 2026-08-03 | F1 / A1 / A2 | Seeded `CLAIM_LEDGER.md`; DVA imperfect-indicator language; Evidence-and-alternatives boxes (science parks, Syria); AfCFTA ROO dating to cutoff | Text review |
| 2026-08-03 | A1 / A2 | Evidence boxes for Ruhr–Donbas, Pittsburgh–Detroit, LAC deindustrialization, Gulf diversification, African urbanization; policy dating in Ch. 4/7/11/16 | Text review |
| 2026-08-03 | F1 / P2 | Deepened Ch. 6/8/11 claim ledger; figure vintage/method notes; trimmed Ch. 6 and 11 conclusions; qualified NASSCOM/NEOM/DVA figure labels | Text review |
| 2026-08-03 | P2 / P5 | Expanded figure notes across Ch. 4–16; trimmed remaining regional/synthesis conclusions; added glossary terms (stranded regions, climate migration, digital sovereignty, Splinternet, just transition) | Text review |
| 2026-08-03 | P3 / P5 / F1 | Phrase diversification (spatial implication / binding constraint fillers); index generator filters + see-also; regenerated subject index; ledgered Ch. 4/14/16 quantitative claims | `python scripts/generate_index.py` |
| 2026-08-03 | P1 / F1 | Standardized discussion questions to six per chapter; softened preface count promise; ledgered Ch. 9/10 EU fiscal magnitudes | Question-count script; text review |
| 2026-08-03 | P2 | Case-selection + comparative notes (CAFTA/Caribbean; Pakistan; Maghreb; francophone WA/Ethiopia); Oceania/Central Asia scope note confirmed | Text review |
| 2026-08-03 | P4 | Gulf inset on Ch. 11 map; label-offset fixes Ch. 4/7/12; widen C-range maps; renumber Ch. 9 figures | Figure smoke tests ch04/07/11/12 |
| 2026-08-03 | P5 | Notation pass: Ch. 14 structural gravity MR terms; Ch. 16 PPML+FE preferred form; glossary MR convention | Text cross-check vs Ch. 3-B / App. A |
| 2026-08-03 | P1 | Pathway workload note + Pathway 1 schedule cleanup | Word-count audit of ch01–ch16 |

