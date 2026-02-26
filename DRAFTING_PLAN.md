# Book Drafting Plan

**Title:** The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods

This plan organizes the writing process into phases. Each phase produces a self-contained deliverable that can be reviewed, tested in classrooms, or sent to external reviewers before proceeding.

---

## Phase 0: Foundations and Infrastructure

**Goal:** Establish the shared analytical framework, code repositories, and data pipelines before any regional chapter is drafted.

### Deliverables

| # | Task | Notes |
|---|---|---|
| 0.1 | **Finalize the outline and chapter specifications** | Write a 1–2 page "chapter spec" for each of the 15 chapters: thesis statement, 3–5 key arguments, target length (word count), required datasets, and 2–3 anchor references. **Status:** 11 of 15 detailed; Chs. 7, 9, 11, 14 remain stubs. |
| 0.2 | **Build the replication repository** | Create a GitHub repo with folder structure for each Applied Lab. Set up R and Python environments (Docker or `renv`/`conda`) and add zero-install cloud execution targets (Colab/Codespaces) for student onboarding. Confirm access to all datasets (WIOD, VIIRS, NUTS-2, WDI, Afrobarometer). |
| 0.3 | **Draft Appendix B (Data & Software Guide)** | Writing this early forces resolution of all data-access and tooling decisions before chapter drafting begins. |
| 0.4 | **Secure "Institutional Spotlight" contacts** | Identify and begin outreach for 8–12 interview subjects across regions (policy-makers, trade negotiators, regional development officials). |
| 0.5 | **Commission GIS base maps** | Engage a cartographer or GIS specialist to produce the base map layers (administrative boundaries, trade corridors, night-lights composites) that will be populated with chapter-specific data throughout drafting. |
| 0.6 | **Create dataset fallback matrix** | For each lab, document primary and backup data sources (e.g., WIOD with ADB MRIO/OECD TiVA backups) plus update cadence and known deprecation risk. |
| 0.7 | **Adopt data storage policy** | Enforce a split between in-repo fixtures and external full-size datasets before Labs 2-5 scale up. |

---

## Phase 1: The Toolkit (Part I — Chapters 1–3)

**Goal:** Write the theoretical and methodological core. This section must be stable before regional chapters reference it.

### Drafting Order and Rationale

| Chapter | Approach |
|---|---|
| **Ch. 1: Micro-Foundations of Space** | Draft as a self-contained survey. Use as a "test chapter" for tone, notation, and pedagogical style. Circulate for early feedback. |
| **Ch. 2: Evolutionary & Institutional Frameworks** | Draft in parallel with Ch. 1. The two chapters establish the "two lenses" (spatial economics + institutional economics) that structure every regional chapter. |
| **Ch. 3: The Modern Spatial Toolkit** | Draft after Chs. 1–2 are stable, since it operationalizes their concepts. Build the first code notebooks (SAR, SEM, SDM estimation) alongside the prose — the text and the code should co-evolve. Add explicit intuition for spatial counterfactuals and boundary discontinuities to bridge into Labs 3 and 4. |

### Review Gate

- Internal review of Part I.
- Pilot-test Ch. 3 code notebooks with a small group of graduate students.
- Validate "Methods Mini-Primer" inserts for Ch. 8 (Spatial RDD) and Ch. 11 (SCM/event-study) before those chapters enter drafting.
- Revise before proceeding to regional parts.

---

## Phase 2: Regional Parts (Parts II–VI — Chapters 4–13)

**Goal:** Draft all five regional sections. The recommended order prioritizes the two regions for which the most detailed material already exists (Americas and Africa), then proceeds to the remaining three.

### Drafting Order

| Wave | Chapters | Rationale |
|---|---|---|
| **Wave A** | Part II (Americas): Chs. 4–5 + Lab 1 | Most developed in the existing outlines. Strong anchor material on USMCA, CHIPS Act, and the Middle-Income Trap. Draft first to establish the "regional chapter template." |
| **Wave B** | Part VI (Africa): Chs. 12–13 + Lab 5 | Second-most developed outline. Night-lights lab is a strong pedagogical hook and nowcasting bridge to modern GDP measurement. Drafting Africa early also ensures it is not an afterthought — consistent with the book's ethos of treating all regions with equal analytical seriousness. |
| **Wave C** | Part III (Asia): Chs. 6–7 + Lab 2 | Requires MRIO data pipeline (set up in Phase 0): WIOD primary, with ADB MRIO and OECD TiVA as active backups to reduce currency risk. |
| **Wave D** | Part IV (Europe): Chs. 8–9 + Lab 3 | Spatial RDD lab requires NUTS-2 data and careful econometric exposition. Benefits from having the SAR/SDM code from Lab 1 already tested. |
| **Wave E** | Part V (MENA): Chs. 10–11 + Lab 4 | Synthetic Control Method lab is methodologically self-contained. MENA chapters require the most original synthesis due to relative data scarcity and institutional complexity. |

### Per-Wave Process

For each wave:

1. **Research compilation** — Assemble the 15–20 core references, datasets, and institutional documents for each chapter.
2. **First draft** — Write the narrative chapters (target: 8,000–12,000 words per chapter).
3. **Lab development** — Build the Applied Lab notebook (code + data + instructions) in parallel with the prose.
4. **Pedagogical features** — Draft "Data in Depth" boxes, "Institutional Spotlight" sidebars, comparative maps, and end-of-chapter questions.
5. **Internal review** — Cross-check against Part I for consistency of terminology, notation, and analytical framework.
6. **Cloud execution check** — Ensure each lab runs in at least one zero-install environment (Colab or Codespaces) before wave sign-off.

### Review Gate

- After Waves A and B: full internal review plus classroom pilot of Labs 1 and 5 to de-risk methods difficulty and setup friction before Waves C-E.
- After all five waves: external review of all regional parts by 2–3 area-studies specialists per region.

---

## Phase 3: Global Synthesis (Part VII — Chapters 14–15)

**Goal:** Write the capstone chapters that tie the regional analyses together.

### Approach

| Chapter | Approach |
|---|---|
| **Ch. 14: Climate Change and the Future Economic Map** | Must be drafted *after* all regional parts, since it synthesizes climate–economy interactions raised in every region (Sahel migration, Gulf stranded assets, European green deal, Asian supply chain reconfiguration). |
| **Ch. 15: The Future of Global Regionalism** | The book's conclusion. Written last. Draws comparative lessons and identifies the discipline's open questions. |

---

## Phase 4: Apparatus and Production

**Goal:** Complete all supporting material and prepare the manuscript for submission.

### Deliverables

| # | Task |
|---|---|
| 4.1 | **Draft Appendix A (Mathematical Foundations)** — Derivations of SAR/SEM/SDM estimators, matrix notation conventions. |
| 4.2 | **Draft Appendix C (Glossary)** — Compile all technical terms, acronyms, and notation from the manuscript. |
| 4.3 | **Finalize all GIS maps and figures** — Ensure all comparative maps are produced at publication quality with consistent cartographic style. |
| 4.4 | **Finalize all Applied Lab code** — Ensure all notebooks run end-to-end, are documented, and include expected output. Package the replication repo for distribution. |
| 4.5 | **Compile "Comparative Spotlight" tables** — Ensure cross-regional comparison tables are consistent and placed at the end of each Part. |
| 4.6 | **Full manuscript copyedit and reference audit** — Verify all citations, dataset URLs, and cross-references between chapters. |
| 4.7 | **Index preparation** |

---

## Phase 5: Review and Revision

| # | Task |
|---|---|
| 5.1 | **External peer review** — Send full manuscript to 3–5 reviewers spanning spatial economics, development economics, and economic geography. |
| 5.2 | **Late-stage classroom validation** — Re-test revised chapters/labs after full-draft integration to confirm edits from the early pilot and external review. |
| 5.3 | **Revision round** — Incorporate reviewer and classroom feedback. |
| 5.4 | **Final manuscript submission** |

---

## Summary of Chapter–Lab–Method Alignment

This table summarizes the book's integrated structure, ensuring each regional section teaches a distinct empirical method.

| Part | Region | Chapters | Applied Lab | Core Method | Key Dataset(s) |
|---|---|---|---|---|---|
| I | Foundations | 1–3 | — | SAR, SEM, SDM (introduced) | — |
| II | Americas | 4–5 | Lab 1 | Spatial Lag Model, $W$ matrix | WDI, UN Comtrade, BTS |
| III | Asia | 6–7 | Lab 2 | MRIO / Network Econometrics | WIOD, TiVA |
| IV | Europe | 8–9 | Lab 3 | Spatial RDD | Eurostat NUTS-2 |
| V | MENA | 10–11 | Lab 4 | Synthetic Control Method | WDI, ACLED, UNHCR |
| VI | Africa | 12–13 | Lab 5 | Night-lights / Moran's $I$ | VIIRS, Afrobarometer |
| VII | Synthesis | 14–15 | Lab 6 | Services trade gravity, STRI | WTO BOP, OECD STRI, TiVA, ECIPE |

---

## Cross-Cutting Theme: Services Trade and the Spatial Paradox of Intangibility

A services trade thread runs through the entire book, integrated into existing chapters rather than isolated in a standalone section. The integration points are:

| Chapter | Services Trade Content |
|---|---|
| Ch. 1 | Spatial paradox of intangibility; Storper & Venables buzz; Haskel & Westlake four S's |
| Ch. 2 | STRI and regulatory heterogeneity as institutional barriers to services trade |
| Ch. 3 | Services trade measurement (BOP modes, TiVA servicification, STRI); gravity model for services |
| Ch. 4 | USMCA digital trade provisions; North American APS networks; local multipliers; nearshoring |
| Ch. 5 | BPO/digital labor as upgrading path; platform-mediated telemigration; medical tourism; tourism multipliers |
| Ch. 6 | India's IT services geography; Grossman & Rossi-Hansberg task trading; servicification of Asian manufacturing |
| Ch. 7 | Platform economies (Alibaba, Grab, Gojek); Digital Silk Road; data sovereignty |
| Ch. 8 | EU Services Directive failure; Digital Single Market; GDPR; APS networks; education as traded service |
| Ch. 9 | CEE nearshore BPO hubs; Brexit financial services relocation |
| Ch. 10 | Gulf aviation/logistics/finance hubs; medical tourism; cloud infrastructure; telemedicine |
| Ch. 12 | M-Pesa and digital financial services; productive service agglomeration in African cities |
| Ch. 13 | AfCFTA Protocol on Trade in Services; mobile money interoperability |
| Ch. 15 | Telemigration synthesis; splinternet; gravity model for services; remote work spatial equilibrium |
| Lab 6 | Services trade gravity model; STRI tariff equivalents; TiVA servicification; cloud geography |

Key references anchoring this thread:
- Grossman & Rossi-Hansberg (2008), "Trading Tasks" — theoretical backbone
- Kimura & Lee (2006) / Head, Mayer & Ries (2009) — gravity for services empirics
- Storper & Venables (2004), "Buzz" — why services cluster
- Haskel & Westlake (2018), *Capitalism Without Capital* — intangible economy framework
- Borchert, Gootiiz & Mattoo (2014) — STRI measurement
- Faber & Gaubert (2019) — tourism as services trade with spatial identification
- Suri & Jack (2016) — M-Pesa and digital financial inclusion
- Connell (2013) — medical tourism as Mode 2 services trade
- Diamond (2016) — spatial equilibrium of service cities

---

## Design Principles Guiding This Plan

1. **Toolkit-first:** Part I is drafted and reviewed before any regional chapter, so that all authors and reviewers share a common analytical vocabulary.
2. **Template-then-scale:** The first two regional sections (Americas and Africa) are drafted as templates; subsequent regions follow their structure.
3. **Code-alongside-prose:** Applied Labs are developed in tandem with the chapters they accompany, not bolted on afterward.
4. **Equal analytical seriousness across regions:** Africa and MENA receive the same methodological depth as the Americas and Europe — a deliberate correction of the typical textbook pattern.
5. **Review gates prevent compounding errors:** The manuscript is reviewed at three checkpoints (after Part I, after the first two regional parts, and after the full draft) rather than only at the end.
6. **Services trade as cross-cutting thread:** Rather than a standalone services chapter, services trade content is woven through every regional chapter and synthesized in Chapter 15 and Lab 6. This ensures students encounter services geography as a recurring analytical lens, not a one-off topic.

---

## Progress Tracker

### Phase 0 Status

| # | Task | Status |
|---|---|---|
| 0.1 | Outline and chapter specifications | 11/15 detailed (Chs. 7, 9, 11, 14 are stubs) |
| 0.2 | Replication repository | Done — Labs 1–6 scaffolded, CI passing |
| 0.3 | Appendix B (Data & Software Guide) | Not started |
| 0.4 | Institutional Spotlight contacts | Not started |
| 0.5 | GIS base maps | Not started |
| 0.6 | Dataset fallback matrix | Partially done (documented in `docs/data_storage_strategy.md`) |
| 0.7 | Data storage policy | Done |

### Phase 1 Status (Part I)

| Chapter | Prose | Services Content | Review |
|---|---|---|---|
| Ch. 1 | Draft complete (361 lines) | §1.5 spatial paradox of intangibility | Pending internal review |
| Ch. 2 | Draft complete (267 lines) | — | Pending internal review |
| Ch. 3 | Draft complete (559 lines) | §3.7 services data sources | Pending internal review |

### Phase 2 Status (Regional Parts)

| Wave | Chapters | Prose Status | Lab Status |
|---|---|---|---|
| A (Americas) | Chs. 4–5 | Initial drafts (352 + 307 lines); need expansion to target length | Lab 1: Complete |
| B (Africa) | Chs. 12–13 | Ch. 12 initial draft (265 lines); Ch. 13 not started | Lab 5: Scaffolded (synthetic data only) |
| C (Asia) | Chs. 6–7 | Not started | Lab 2: Scaffolded (TiVA wired) |
| D (Europe) | Chs. 8–9 | Not started | Lab 3: Scaffolded (NUTS-2 wired) |
| E (MENA) | Chs. 10–11 | Not started | Lab 4: Partially complete (SCM baselines) |

### Phase 3 Status (Synthesis)

| Chapter | Prose Status | Spec Status |
|---|---|---|
| Ch. 14 | Not started | Stub |
| Ch. 15 | Not started | Detailed (services-trade synthesis) |

### Lab 6 (Services Trade — Cross-Regional Capstone)

| Script | Status |
|---|---|
| `gravity_services_scaffold.py` | Not started |
| `stri_tariff_equivalent.py` | Not started |
| `servicification_decomposition.py` | Not started |
| `cloud_geography_mapper.py` | Not started |
| `fetch_wto_services_trade.py` | Not started |
| `fetch_oecd_stri.py` | Not started |
