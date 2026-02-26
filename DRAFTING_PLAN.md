# Book Drafting Plan

**Title:** The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods

This plan organizes the writing process into phases. Each phase produces a self-contained deliverable that can be reviewed, tested in classrooms, or sent to external reviewers before proceeding.

---

## Phase 0: Foundations and Infrastructure

**Goal:** Establish the shared analytical framework, code repositories, and data pipelines before any regional chapter is drafted.

### Deliverables

| # | Task | Notes |
|---|---|---|
| 0.1 | **Finalize the outline and chapter specifications** | Write a 1–2 page "chapter spec" for each of the 16 chapters (including 3-A/3-B): thesis statement, 3–5 key arguments, target length, required datasets, and 2–3 anchor references. **Status:** 14 of 18 specs detailed; Chs. 10, 12, 15 remain stubs; Ch. 14 needs stub-to-spec conversion. |
| 0.2 | **Build the replication repository** | Create a GitHub repo with folder structure for each Applied Lab. Set up R and Python environments and add zero-install cloud execution targets (Colab/Codespaces). |
| 0.3 | **Draft Appendix B (Data & Software Guide)** | Writing this early forces resolution of all data-access and tooling decisions before chapter drafting begins. |
| 0.4 | **Secure "Institutional Spotlight" contacts** | Identify and begin outreach for 8–12 interview subjects across regions. |
| 0.5 | **Commission GIS base maps** | Produce base map layers with consistent cartographic style for Regional Diagnostics Dashboards. |
| 0.6 | **Create dataset fallback matrix** | For each lab, document primary and backup data sources plus update cadence and deprecation risk. |
| 0.7 | **Adopt data storage policy** | Enforce a split between in-repo fixtures and external full-size datasets. |
| 0.8 | **Write "Pathways Through This Book" preface section** | 5 curated tracks with visual dependency diagram (DAG). |
| 0.9 | **Design Regional Diagnostics Dashboard template** | Standardized 1-page visual with convergence plots, services GDP map, spatial Gini, night-lights, top 5 GATS exports. |

---

## Phase 1: The Toolkit (Part I — Chapters 1, 2, 3-A, 3-B)

**Goal:** Write the theoretical and methodological core. This section must be stable before regional chapters reference it. Restructured to reduce front-loading: heavy theories distributed to regional chapters; methods split by discipline.

### Drafting Order and Rationale

| Chapter | Approach |
|---|---|
| **Ch. 1: Micro-Foundations of Space** | Draft as a self-contained survey with opening case study (Bangalore vs. Kolkata). Use as a "test chapter" for tone, notation, and pedagogical style. Add preview boxes pointing to regional chapters. |
| **Ch. 2: Institutional Toolkit & Services Architecture** | Slimmed from the old Ch. 2. Path dependency → Ch. 5 (Latin America); Varieties of Capitalism → Ch. 9 (Europe); Windows of Opportunity → Ch. 6 (East Asia). Retain institutional thickness, related variety, and services trade architecture (GATS modes, positive/negative listing, MRAs). |
| **Ch. 3-A: Spatial Econometrics & Inequality Measurement** | Spatial inequality measurement (β/σ-convergence, Theil, Gini) + SAR/SEM/SDM + MAUP + Bartik + QSMs. Build code notebooks alongside prose. |
| **Ch. 3-B: Trade Measurement & Gravity** | Structural gravity (A&vW), PPML, Grossman & Rossi-Hansberg task trading, GATS modes, TiVA servicification. Running Gravity Results Table starts here. |

### Review Gate

- Internal review of Part I.
- Pilot-test Ch. 3-A code notebooks with a small group of graduate students.
- Validate "Methods Mini-Primer" inserts for Ch. 9 (Spatial RDD) and Ch. 12 (SCM/event-study) before those chapters enter drafting.
- Revise before proceeding to regional parts.

---

## Phase 2: Regional Parts (Parts II–VII — Chapters 4–14)

**Goal:** Draft all six regional sections. The recommended order prioritizes the two regions for which the most detailed material already exists (Americas and Africa), then proceeds to the remaining four.

### Drafting Order

| Wave | Chapters | Rationale |
|---|---|---|
| **Wave A** | Part II (Americas): Chs. 4–5 + Lab 1 | Most developed in the existing outlines. Strong anchor material on USMCA, CHIPS Act, and the Middle-Income Trap. Draft first to establish the "regional chapter template." |
| **Wave B** | Part VII (Africa): Chs. 13–14 + Lab 6 | Second-most developed outline. Night-lights lab is a strong pedagogical hook. Drafting Africa early ensures equal analytical seriousness. |
| **Wave C** | Part III-A (East Asia): Chs. 6–7 + Lab 2 | Requires MRIO data pipeline: WIOD primary, ADB MRIO and OECD TiVA as backups. |
| **Wave C'** | Part III-B (South Asia): Ch. 8 + Lab 3 | New part. India's IT services geography warrants its own chapter. Lab 3 uses RBI/KLEMS data. Can draft in parallel with Wave C. |
| **Wave D** | Part V (Europe): Chs. 9–10 + Lab 4 | Spatial RDD lab requires NUTS-2 data. Benefits from having SAR/SDM code from Lab 1 already tested. |
| **Wave E** | Part VI (MENA): Chs. 11–12 + Lab 5 | SCM lab is methodologically self-contained. MENA chapters require the most original synthesis. |

### Per-Wave Process

For each wave:

1. **Research compilation** — Assemble the 15–20 core references, datasets, and institutional documents for each chapter.
2. **First draft** — Write the narrative chapters (target: 30–40 pages per chapter).
3. **Lab development** — Build the Applied Lab notebook (code + data + instructions) in parallel with the prose. Provide Minimum Viable (2–3 hrs) and Extended (6–10 hrs) versions.
4. **Pedagogical features** — Draft "Data in Depth" boxes, "Spatial Data Challenge" boxes, "Institutional Spotlight" sidebars, Regional Diagnostics Dashboard, Convergence Diagnostic figures, comparative maps, and end-of-chapter questions.
5. **Climate integration** — Ensure climate exposure content is included in each regional Part.
6. **Internal review** — Cross-check against Part I for consistency of terminology, notation, and analytical framework.
7. **Cloud execution check** — Ensure each lab runs in at least one zero-install environment (Colab or Codespaces) before wave sign-off.

### Review Gate

- After Waves A and B: full internal review plus classroom pilot of Labs 1 and 6 to de-risk methods difficulty and setup friction.
- After all waves: external review of all regional parts by 2–3 area-studies specialists per region.

---

## Phase 3: Global Synthesis (Part VIII — Chapters 15–16)

**Goal:** Write the capstone chapters that tie the regional analyses together.

### Approach

| Chapter | Approach |
|---|---|
| **Ch. 15: Climate, Stranded Regions, and the Future Map** | Repurposed from standalone climate intro to true synthesis. Climate subsections in each regional chapter provide empirical foundation; Ch. 15 provides the cross-regional framework. Pacific Islands comparative sidebar. |
| **Ch. 16: The Future of Global Regionalism & Services Trade** | The book's conclusion. Telemigration, telemedicine, splinternet, global comparative services framework matrix (USMCA/EU/AfCFTA/CPTPP/RCEP). Written last. Lab 7 (Services Gravity) accompanies this chapter. |

---

## Phase 4: Apparatus and Production

**Goal:** Complete all supporting material and prepare the manuscript for submission.

### Deliverables

| # | Task |
|---|---|
| 4.1 | **Draft Appendix A (Mathematical Foundations)** — Derivations of SAR/SEM/SDM estimators, matrix notation conventions. |
| 4.2 | **Draft Appendix C (Glossary)** — Compile all technical terms, acronyms, and notation from the manuscript. |
| 4.3 | **Finalize all GIS maps and figures** — Ensure all comparative maps are produced at publication quality with consistent cartographic style. Compile Regional Diagnostics Dashboards into a single comparative spread for Ch. 15. |
| 4.4 | **Finalize all Applied Lab code** — Ensure all 7 labs run end-to-end with Minimum Viable and Extended versions. Package the replication repo. Add technical specifications (estimated time, prereqs, data sizes, difficulty). |
| 4.5 | **Compile "Comparative Spotlight" tables** — Ensure cross-regional comparison tables are consistent and placed at the end of each Part. |
| 4.6 | **Full manuscript copyedit and reference audit** — Verify all citations, dataset URLs, and cross-references between chapters. |
| 4.7 | **Index preparation** |

---

## Phase 5: Review and Revision

| # | Task |
|---|---|
| 5.1 | **External peer review** — Send full manuscript to 3–5 reviewers spanning spatial economics, development economics, and economic geography. |
| 5.2 | **Late-stage classroom validation** — Re-test revised chapters/labs after full-draft integration. |
| 5.3 | **Revision round** — Incorporate reviewer and classroom feedback. |
| 5.4 | **Final manuscript submission** |

---

## Summary of Chapter–Lab–Method Alignment

| Part | Region | Chapters | Applied Lab | Core Method | Key Dataset(s) |
|---|---|---|---|---|---|
| I | Foundations | 1, 2, 3-A, 3-B | — | SAR, SEM, SDM, Gravity (introduced) | — |
| II | Americas | 4–5 | Lab 1 | Spatial Lag Model, Bartik | WDI, UN Comtrade, BTS |
| III-A | East Asia/ASEAN | 6–7 | Lab 2 | MRIO / Network Econometrics | WIOD, TiVA |
| III-B | South Asia | 8 | Lab 3 | Services mapping (RBI/KLEMS) | RBI, KLEMS India |
| V | Europe | 9–10 | Lab 4 | Spatial RDD | Eurostat NUTS-2 |
| VI | MENA | 11–12 | Lab 5 | Synthetic Control Method | WDI, ACLED, UNHCR |
| VII | Africa | 13–14 | Lab 6 | Night-lights / Moran's $I$ | VIIRS, Afrobarometer |
| VIII | Synthesis | 15–16 | Lab 7 | Services trade gravity, STRI | WTO BOP, OECD STRI, TiVA |

---

## Cross-Cutting Theme: Services Trade and the Spatial Paradox of Intangibility

A services trade thread runs through the entire book, integrated into existing chapters rather than isolated in a standalone section.

| Chapter | Services Trade Content |
|---|---|
| Ch. 1 | Spatial paradox of intangibility; Storper & Venables buzz; Haskel & Westlake four S's |
| Ch. 2 | Services trade architecture (GATS modes, positive/negative listing, MRAs); STRI and regulatory heterogeneity |
| Ch. 3-B | Gravity for services (consolidated treatment); Grossman & Rossi-Hansberg; servicification via TiVA |
| Ch. 4 | USMCA digital trade; APS networks; international education (Mode 2); local multipliers |
| Ch. 5 | Tourism (Mode 2, Faber & Gaubert); BPO/digital labor; platform-mediated telemigration |
| Ch. 7 | Medical tourism (Mode 2, Thailand/Singapore); ASEAN platforms; Digital Silk Road |
| Ch. 8 | India IT services geography (STPI/SEZ, BPO-to-KPO); brain circulation; telemedicine |
| Ch. 9 | EU Services Directive; Digital Single Market; GDPR; education (Bologna/Erasmus as MRA) |
| Ch. 10 | CEE nearshore BPO hubs; Brexit financial services relocation |
| Ch. 11 | Gulf aviation/logistics/finance/tourism hubs; cloud infrastructure |
| Ch. 13 | M-Pesa and digital financial services; productive service agglomeration |
| Ch. 14 | AfCFTA Protocol on Trade in Services; eco-tourism corridors |
| Ch. 16 | Telemigration synthesis; telemedicine; splinternet; global services framework comparison |
| Lab 7 | Services trade gravity model; STRI tariff equivalents; TiVA servicification; cloud geography |

Key references anchoring this thread:
- Grossman & Rossi-Hansberg (2008), "Trading Tasks"
- Kimura & Lee (2006) / Head, Mayer & Ries (2009) — gravity for services
- Storper & Venables (2004), "Buzz"
- Haskel & Westlake (2018), *Capitalism Without Capital*
- Borchert, Gootiiz & Mattoo (2014) — STRI measurement
- Faber & Gaubert (2019) — tourism as services trade
- Suri & Jack (2016) — M-Pesa
- Connell (2013) — medical tourism as Mode 2
- Diamond (2016) — spatial equilibrium of service cities
- Dossani & Kenney (2007) — India IT services geography
- Bound et al. (2021) — globalization of postsecondary education

---

## Design Principles Guiding This Plan

1. **Toolkit-first:** Part I is drafted and reviewed before any regional chapter, so that all authors and reviewers share a common analytical vocabulary.
2. **Template-then-scale:** The first two regional sections (Americas and Africa) are drafted as templates; subsequent regions follow their structure.
3. **Code-alongside-prose:** Applied Labs are developed in tandem with the chapters they accompany, not bolted on afterward.
4. **Equal analytical seriousness across regions:** Africa and MENA receive the same methodological depth as the Americas and Europe.
5. **Review gates prevent compounding errors:** The manuscript is reviewed at three checkpoints (after Part I, after the first two regional parts, and after the full draft).
6. **Services trade as cross-cutting thread:** Services content is woven through every regional chapter and synthesized in Chapter 16 and Lab 7.
7. **Reduce front-loading:** Heavy institutional theories are distributed to regional chapters where they come alive through cases, not abstracted in Part I.
8. **Climate as regional content:** Climate exposure is integrated into every regional Part rather than deferred to a standalone late chapter.
9. **Pathways for instructors:** Five curated tracks enable professors to sample from the book without requiring cover-to-cover assignment.

---

## Progress Tracker

### Phase 0 Status

| # | Task | Status |
|---|---|---|
| 0.1 | Outline and chapter specifications | 14/18 specs detailed (Chs. 10, 12, 15 are stubs; Ch. 14 needs expansion) |
| 0.2 | Replication repository | Done — Labs 1–7 scaffolded, CI passing |
| 0.3 | Appendix B (Data & Software Guide) | Not started |
| 0.4 | Institutional Spotlight contacts | Not started |
| 0.5 | GIS base maps | Not started |
| 0.6 | Dataset fallback matrix | Partially done (documented in `docs/data_storage_strategy.md`) |
| 0.7 | Data storage policy | Done |
| 0.8 | Pathways preface section | Not started |
| 0.9 | Regional Diagnostics Dashboard template | Not started |

### Phase 1 Status (Part I)

| Chapter | Prose | Key Content | Review |
|---|---|---|---|
| Ch. 1 | Draft complete (361 lines) | Spatial paradox of intangibility | Needs opening case study (Bangalore vs Kolkata) |
| Ch. 2 | Draft complete (267 lines) | Institutional toolkit | Needs slimming: move path dependency, VoC, windows of opportunity to regional chapters |
| Ch. 3 | Draft complete (559 lines) | Spatial toolkit + services data | Needs splitting into 3-A and 3-B; add inequality measurement, MAUP, Bartik, QSMs |

### Phase 2 Status (Regional Parts)

| Wave | Chapters | Prose Status | Lab Status |
|---|---|---|---|
| A (Americas) | Chs. 4–5 | Initial drafts (352 + 307 lines); need expansion | Lab 1: Complete |
| B (Africa) | Chs. 13–14 | Ch. 13 initial draft (265 lines); Ch. 14 not started | Lab 6: Scaffolded (synthetic data only) |
| C (East Asia) | Chs. 6–7 | Not started | Lab 2: Scaffolded (TiVA wired) |
| C' (South Asia) | Ch. 8 | Not started | Lab 3: Scaffolded (directory created) |
| D (Europe) | Chs. 9–10 | Not started | Lab 4: Scaffolded (NUTS-2 wired) |
| E (MENA) | Chs. 11–12 | Not started | Lab 5: Partially complete (SCM baselines) |

### Phase 3 Status (Synthesis)

| Chapter | Prose Status | Spec Status |
|---|---|---|
| Ch. 15 | Not started | Stub (needs repurposing as climate synthesis) |
| Ch. 16 | Not started | Detailed (services-trade synthesis) |

### Lab 7 (Services Trade — Cross-Regional Capstone)

| Script | Status |
|---|---|
| `gravity_services_scaffold.py` | Not started |
| `stri_tariff_equivalent.py` | Not started |
| `servicification_decomposition.py` | Not started |
| `cloud_geography_mapper.py` | Not started |
| `fetch_wto_services_trade.py` | Not started |
| `fetch_oecd_stri.py` | Not started |
