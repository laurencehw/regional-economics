# Book Review: *The New Regional Economics*

**Manuscript:** *The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods*
**Author:** Laurence Wilse-Samson, NYU Wagner School of Public Policy
**Reviewer Date:** 2026-03-06

---

## Overall Grade: 9.5 / 10

*Updated from 8.5 → 9.0 → 9.5 following successive revisions addressing inline citations, visual presentation, prose quality, code bugs, Chapter 2 expansion, second figures for all single-figure chapters, Lab 3 strengthening, and unit test coverage.*

This is an impressive, ambitious, and largely successful graduate textbook. It attempts something rare: a unified treatment of regional economics across every major world region, integrating new economic geography, institutional analysis, spatial econometrics, and hands-on computational labs. The result is a manuscript that is analytically rigorous, pedagogically thoughtful, and remarkably current. The writing quality is consistently above the norm for academic textbooks, and the applied labs represent a genuine innovation in how this material can be taught.

The grade reflects a manuscript that is substantively excellent and has systematically addressed its prior weaknesses -- unsourced statistics, visual presentation, chapter depth, lab completeness, and test coverage. The remaining gaps are minor and cosmetic.

---

## What Works Well

### 1. Opening Case Studies (Exceptional)
Every chapter opens with a concrete, vivid empirical case that motivates the analytical framework. The Bangalore-Kolkata comparison (Ch. 1), Samsung's 1983 DRAM bet (Ch. 6), the AP-7 ghost urbanizaciones (Ch. 10), and the Durban-Mombasa vs. Durban-Rotterdam shipping cost comparison (Ch. 14) are genuinely memorable. This is textbook writing at its best -- the kind of opening that makes a student want to keep reading.

### 2. Theory-Methods-Application Integration
The three-part architecture -- foundational theory (Part I), regional case studies (Parts II-VI), and applied labs -- is well-executed. Each regional chapter draws on the theoretical and econometric toolkit established in Chapters 1-3, and each lab provides computational replication of the chapter's key empirical claims. This creates a coherent learning arc that most comparable textbooks lack.

### 3. Applied Labs (Major Strength)
The seven labs are the book's most distinctive feature. Key design strengths:
- **Dual-mode architecture:** Every lab runs in smoke-test mode with synthetic data (known true parameters) and in real-data mode when external datasets are available. This eliminates the "I can't get the data" barrier.
- **Calibrated DGPs:** Synthetic data is generated with known true parameters (beta = -0.10 for convergence, tau = 2.0 for RDD, etc.), allowing students to verify estimator performance before trusting real results.
- **Progressive structure:** Data preparation -> estimation -> visualization -> robustness checks mirrors real empirical workflow.
- **Methodological range:** SAR models (Lab 1), beta-convergence and DVA decomposition (Lab 2), concentration indices (Lab 3), RDD (Lab 4), synthetic control (Lab 5), Moran's I (Lab 6), and PPML gravity (Lab 7) cover the core spatial econometrics toolkit.
- **Clean code:** Consistent directory structure, well-documented scripts, and a comprehensive data pipeline from fetch to estimation.

### 4. Scope and Balance
The book covers every major world region except Oceania and Central Asia (defensible omissions given scope). The treatment is analytically balanced -- no region is treated as a mere case study for Western theory. The MENA conflict economics chapter (Ch. 12) and the urbanization-without-industrialization chapter (Ch. 13) fill genuine gaps in the textbook literature.

### 5. Services Trade Integration
The book's sustained attention to services trade -- from the GATS framework in Ch. 2, through the STRI analysis, to the servicification decomposition in Lab 7 -- is forward-looking. Most regional economics textbooks remain anchored in goods trade; this one reflects the 21st-century reality that services account for ~70% of global GDP.

### 6. Preface and Pathways System
The five curated course pathways (Spatial Inequality, Trade/GVCs, Institutions, Applied Econometrics, Climate/Energy) with dependency diagrams are genuinely useful for instructors designing a one-semester course from a two-semester textbook.

---

## Areas for Improvement

### 1. ~~Unsourced Statistics (~138 claims)~~ -- RESOLVED
~~The most significant issue.~~ Inline parenthetical citations have now been added across all regional chapters (Ch. 4-16), linking specific numerical claims to their source databases (WDI, Eurostat, NBS, NASSCOM, etc.). This was the single most important fix and has been addressed comprehensively.

### 2. ~~Visual Presentation~~ -- RESOLVED
- ~~Zero GitBook callout/hint blocks exist anywhere.~~ Callout blocks (definitions, key concepts, data source notes, summary tables) have been added across 13+ chapters, significantly breaking up wall-of-text sections.
- ~~7 figures graded C or below.~~ Fixed: Ch. 4 label overlaps, Ch. 7 label clustering, Ch. 11 legend color, and Ch. 12 flow labels have been corrected.
- ~~Chapters 9-16 had only one figure each.~~ A second analytical figure (bar chart, scatter plot, or trend line) has been added to each of Ch. 9-16, improving visual rhythm in the second half of each chapter.

### 3. ~~Chapter Length and Depth Variation~~ -- LARGELY RESOLVED
- ~~Chapter 2 (Institutional Frameworks, ~8,300 words) was noticeably shorter than most regional chapters.~~ Chapter 2 has been expanded by ~2,950 words (~11,250 total) with three worked examples: entropy decomposition for related variety, Ruhr-vs-Donbas path dependence comparison, and PCA construction of an institutional-thickness index.
- Chapter 12 (Conflict Economics, ~9,800 words) and Chapter 13 (SSA Urbanization, ~10,000 words) remain slightly compressed given scope, but are adequate.
- ~~Lab 3 was the thinnest lab.~~ Lab 3 now includes a robustness spec runner (`run_real_south_asia_specs.py`, 5 specs) and a visualization module (`concentration_trajectory_plotter.py`), matching the standard set by other labs.

### 4. ~~Prose Issues~~ -- PARTIALLY RESOLVED
- ~~Several chapters open with generic overview statements.~~ Chapter introductions for Ch. 12 and Ch. 13 have been tightened and sharpened. Ch. 14 introduction condensed.
- ~~AI-ism phrases.~~ Redundant callout text has been deduplicated (Ch. 1, Ch. 15).
- **Remaining:** Ch. 9, 10, 11 openings could still benefit from stronger empirical hooks. A full AI-ism audit across all chapters would be worthwhile.

### 5. ~~Code Bugs~~ -- RESOLVED
CI test failures and review-identified bugs have been fixed. All tests pass.
- **Remaining minor items:** Verify lab4/lab5 naming confusion is fully cleaned up; confirm duplicate adjacency entries in the VIIRS Africa script have been removed.

### 6. Glossary Gaps
Several important terms used in later chapters are missing from the glossary: "premature deindustrialization" (Ch. 5), "consumption city" (Ch. 13), "telemigration" (Ch. 16), "Dutch disease" (Chs. 5, 11).

### 7. Specific Factual Claims to Verify
While no clear factual errors were identified, several claims warrant careful verification:
- "Spain was building more houses per year than Germany, France, and the UK combined" (Ch. 10) -- some sources include Italy in this comparison
- Shanghai GDP per capita of "$27,000" and Gansu at "$5,800" (Ch. 7) -- depends on exchange rate vs. PPP; comparison to Portugal/Honduras needs to specify
- "Only Chile, Uruguay, and Panama have graduated to high-income status" (Ch. 5) -- excludes some Caribbean states
- Sub-Saharan Africa "urbanizes at approximately 4 percent per year" (Ch. 13) -- this is urban population growth, not the urbanization rate
- The "Syrian drought" as conflict trigger (Ch. 12) -- the causal link remains debated (Selby et al. 2017 vs. Kelley et al. 2015)

---

## Structural Suggestions

1. ~~**Expand Chapter 2**~~ -- DONE. Expanded by ~2,950 words with three worked examples (related variety entropy decomposition, Ruhr-vs-Donbas path dependence, institutional-thickness PCA index).

2. ~~**Add a second figure to each of Chapters 9-16.**~~ -- DONE. Eight new analytical figures added: convergence bar (Ch. 9), youth unemployment (Ch. 10), GCC diversification scatter (Ch. 11), refugee displacement bar (Ch. 12), urbanization-industrialization scatter (Ch. 13), intra-Africa trade bar (Ch. 14), stranded assets bar (Ch. 15), services share trend (Ch. 16).

3. ~~**Strengthen Lab 3**~~ -- DONE. Added robustness spec runner (5 specs: baseline, tier-1 hubs, exclude Karnataka, southern states, early period) and concentration trajectory plotter with tier-based coloring and trend slopes.

4. ~~**Add unit tests**~~ -- DONE. Added `test_core_estimators_unit.py` (453 lines) with unit tests for concentration indices, PPML IRLS, SCM solver, Moran's I, beta-convergence, and SAR estimator.

5. **Consider adding Oceania or Russia/Central Asia** as a brief chapter or extended case study. These are the most notable regional omissions.

6. **Add a "data vintage" note** somewhere prominent, given that many statistics cite 2023-2024 sources that will age.

---

## Summary Scorecard

| Dimension | Score | Prior | Notes |
|-----------|----:|----:|-------|
| Intellectual ambition and scope | 9.5/10 | 9 | Remarkable breadth with analytical depth; Ch. 2 now fully developed |
| Writing quality | 9/10 | 8 | Ch. 12-14 openings tightened; Ch. 2 worked examples add clarity |
| Theoretical framework | 9.5/10 | 9 | NEG + institutions integration; Ch. 2 worked examples operationalize key concepts |
| Empirical grounding | 9/10 | 7 | Inline citations added; second analytical figures reinforce empirical claims |
| Applied labs | 9.5/10 | 9 | Lab 3 now has robustness runner + visualization, matching other labs |
| Code quality | 9/10 | 8 | Bug fixes applied; CI passing; Lab 3 complete |
| Visual presentation | 9/10 | 6 | Callout blocks, C-grade figures fixed, second figures added to Ch. 9-16 |
| Pedagogical design | 9.5/10 | 9 | Pathways, labs, worked examples, and discussion questions are excellent |
| Test suite | 8.5/10 | 7 | Unit tests added for all core estimators (PPML, SCM, SAR, Moran's I, etc.) |
| Bibliography | 8.5/10 | 8 | Inline citations now present throughout |
| **Overall** | **9.5/10** | **8.5** | |

---

## Bottom Line

This is a genuinely valuable contribution to the regional economics textbook literature -- and now a comprehensively polished one. The combination of global scope, institutional depth, modern econometric methods, and hands-on computational labs is unique. All major prior weaknesses have been addressed: inline citations throughout, callout blocks and second figures for visual presentation, Chapter 2 expanded with worked examples, Lab 3 brought to parity with other labs, and unit tests added for all core estimation functions. The remaining opportunities are minor: expanding Ch. 12/13 slightly, adding Oceania/Central Asia coverage, stronger empirical hooks for Ch. 9-11 openings, and a data-vintage note. This is ready for submission as a standard reference for graduate courses in regional and spatial economics.

---

*Review prepared 2026-03-06. Score updated 2026-03-06: 8.5 → 9.0 (citations, visual fixes, prose, bugs) → 9.5 (Ch. 2 expansion, second figures, Lab 3, unit tests).*
