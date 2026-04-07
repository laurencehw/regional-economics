# Book Review: *The New Regional Economics*

**Manuscript:** *The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods*
**Author:** Laurence Wilse-Samson, NYU Wagner School of Public Policy
**Reviewer:** Independent review (Claude, Opus 4.6)
**Date:** 2026-04-07

---

## Overall Score: 8.8 / 10

This is an outstanding graduate textbook — arguably the most ambitious single-author treatment of regional economics in print. It attempts to unify new economic geography, institutional analysis, spatial econometrics, and hands-on computational labs across every major world region. The writing quality is exceptional by academic textbook standards, frequently rising to the level of a well-edited monograph. The applied labs are a genuine pedagogical innovation. The 216,000-word manuscript, with 16 chapters, 3 appendices, 7 labs, and 107 passing tests, represents a monumental intellectual effort.

The score of 8.8 reflects a manuscript that is publication-ready in substance but has identifiable gaps in four categories: (1) missing figure files that break the visual program, (2) uneven deployment of pedagogical apparatus across chapters, (3) residual prose patterns that betray the book's AI-assisted drafting, and (4) a handful of analytical thinness in the synthesis chapters relative to the regional chapters. The path to 9.5+ is concrete and achievable.

---

## What Works Exceptionally Well

### 1. Opening Case Studies (Best-in-Class)
Every chapter opens with a vivid, specific empirical narrative that motivates the chapter's analytical framework. The Bangalore-Kolkata divergence (Ch. 1) is a masterclass in motivating NEG theory through historical specifics. The Samsung 1983 DRAM gamble (Ch. 6), the Aleppo-to-Gaziantep textile cluster relocation (Ch. 12), and the Phoenix heat-death opening (Ch. 15) are equally compelling. These openings do real intellectual work — they are not decorative anecdotes but carefully chosen cases that the chapter's theory is designed to explain.

### 2. Theory-Methods-Application Architecture
The three-part structure — foundational theory (Part I: Chs. 1-3B), regional case studies (Parts II-VI: Chs. 4-14), and synthesis (Part VII: Chs. 15-16) — creates a coherent intellectual arc. Each regional chapter explicitly draws on the toolkits from Chapters 1-3, and each lab provides computational replication of key claims. The dependency diagram in the Preface makes this architecture transparent and navigable.

### 3. Applied Labs (Major Differentiator)
The seven labs are the book's most distinctive feature and its strongest claim to originality:
- **Dual-mode architecture:** Every lab runs with synthetic data (known true parameters) and with real data when available. Students verify estimator performance on calibrated DGPs before trusting real-data results.
- **Methodological breadth:** SAR (Lab 1), beta-convergence with DVA decomposition (Lab 2), concentration indices (Lab 3), RDD (Lab 4), synthetic control (Lab 5), Moran's I (Lab 6), and PPML gravity (Lab 7).
- **Code quality:** All 107 tests pass. Consistent directory structure. Scaffold code is well-documented. Supporting scripts for data fetching, visualization, and comparison tables are comprehensive.
- **Pedagogical scaffolding:** Each lab has a minimum viable version (2-3 hours) and an extended version (6-10 hours), accommodating courses with different quantitative emphases.

### 4. Institutional Depth
The institutional analysis (Ch. 2) is not merely a nod to "institutions matter" but a substantive analytical framework — institutional thickness, related variety, path dependence, varieties of capitalism — that is operationalized throughout the regional chapters. The kafala system in Ch. 11, the Rapid Response Labor Mechanism in Ch. 4, the varieties-of-capitalism spatial signatures in Ch. 9, and the institutional collapse analysis in Ch. 12 all demonstrate that the institutional framework is load-bearing, not decorative.

### 5. Services Trade Integration
The sustained attention to services trade — from the GATS modes framework in Ch. 2/3-B, through STRI analysis, to telemigration in Ch. 16, to the PPML gravity estimation in Lab 7 — is forward-looking and fills a genuine gap in the regional economics textbook literature. Most competing texts remain goods-centric.

### 6. Pathways System
The five curated course pathways (Spatial Inequality, Trade & GVCs, Institutions & Political Economy, Applied Spatial Econometrics, Climate & Energy) with dependency diagrams and weekly syllabi are a genuinely useful instructor resource. The companion-volume note connecting to urban economics is a thoughtful touch.

### 7. Chapter 3-A (Spatial Econometrics)
At 613 lines, this is the most technically dense chapter and also the best-organized. The seven-step logical sequence — from weight matrix construction through model selection, impact decomposition, identification, causal inference, panel extensions, and data landscape — is a model of methodological exposition. The treatment of Manski's reflection problem and the bridge to design-based methods (RDD, SCM) are particularly strong.

### 8. Cross-Referencing Network
The book's internal cross-referencing is dense and well-executed. Chapter 12's connection of the Aleppo-Gaziantep corridor to Chapter 6's semiconductor supply chain disruption, Chapter 15's systematic callback to climate sections in every prior regional chapter, and Chapter 16's integration of frameworks from Chapters 1-3B all demonstrate a manuscript that reads as a unified work rather than a collection of standalone essays.

### 9. Hint/Callout Blocks
The GitBook-style `{% hint %}` blocks are consistently well-written, providing key definitions (Maquiladora, Cohesion Policy, Telemigration, Digital Sovereignty), methodological warnings (MAUP, Conditional vs. Absolute Convergence), and synthesis findings (Conflict Relocates Agglomeration, Multiple Equilibria and History Dependence). These are a genuine pedagogical asset.

### 10. Discussion Questions
Every chapter (including Chs. 1-16) ends with 6 discussion questions that are substantive, thought-provoking, and connected to the chapter's analytical framework. They are not recall questions but genuine essay prompts that require synthesis.

---

## Issues Identified

### Category A: Missing Figure Files (New Finding)

Eight figures referenced in chapters do not have corresponding PNG files in the `figures/` directory. These will render as broken images in any build:

| # | Chapter | Missing File | Description |
|---|---------|-------------|-------------|
| A1 | Ch. 9 | `fig_ch09_chart_eu_convergence_bar.png` | EU convergence clubs bar chart |
| A2 | Ch. 10 | `fig_ch10_chart_youth_unemployment.png` | Youth unemployment North-South divergence |
| A3 | Ch. 11 | `fig_ch11_chart_gdp_diversification.png` | GCC diversification progress |
| A4 | Ch. 12 | `fig_ch12_chart_refugee_displacement.png` | MENA displacement crisis chart |
| A5 | Ch. 13 | `fig_ch13_chart_urbanization_scatter.png` | Urbanization scatter plot |
| A6 | Ch. 14 | `fig_ch14_chart_intra_africa_trade.png` | Intra-African trade comparison |
| A7 | Ch. 15 | `fig_ch15_chart_stranded_assets.png` | Stranded assets by country |
| A8 | Ch. 16 | `fig_ch16_chart_services_share_trend.png` | Services share of GDP trend |

All 8 missing figures follow the naming pattern `fig_chXX_chart_*` — suggesting they are a category of thematic charts that were referenced in the text but never generated. The corresponding figure-generation scripts (`chXX_figures.py`) exist but may not produce these specific outputs. **This is the highest-priority fix** because broken images are immediately visible to readers.

### Category B: Uneven Pedagogical Apparatus

| # | Issue | Scope | Impact |
|---|-------|-------|--------|
| B1 | **Chapter 2 has zero hint/callout blocks.** Every other chapter has 2-8. Ch. 2 introduces key concepts (institutional thickness, related variety, path dependence, VoC) that would benefit from definition boxes, especially given the chapter's length (447 lines). | Ch. 2 | Medium |
| B2 | **Figure numbering inconsistency in Ch. 6.** Figure 6.3 (DVA decomposition) appears *before* Figure 6.2 (DVA trajectory) on lines 75 and 83 respectively. | Ch. 6 | Low |
| B3 | **Figure 15.3 appears before Figure 15.2** (lines 157 and 163). Same numbering-order issue as Ch. 6. | Ch. 15 | Low |
| B4 | **No "Data in Depth" box in most regional chapters.** Ch. 1 has an excellent "Data in Depth: Estimating the Urban Wage Premium" section. This pattern is not replicated in the regional chapters, which would benefit from similar worked empirical examples. | Chs. 4-16 | Low |
| B5 | **No "Institutional Spotlight" in most chapters.** Ch. 1 has "Institutional Spotlight: OMB Metropolitan Definitions." This excellent pedagogical device appears sporadically elsewhere but is not systematic. | Chs. 4-16 | Low |

### Category C: Prose Patterns

| # | Issue | Severity |
|---|-------|----------|
| C1 | **Residual formulaic transitions.** "The spatial implication is..." and "The question is whether..." still appear frequently across regional chapters (less than the prior review noted, but still detectable). "This is not merely X; it is Y" remains a recurring construction. | Low |
| C2 | **Overlong sentences.** Some sentences in Chs. 9 and 16 exceed 100 words with nested subordinate clauses. The VoC section in Ch. 9 (lines 23-31) contains a ~200-word sentence. The telemigration section in Ch. 16 has several 80+ word sentences. | Low |
| C3 | **"The binding constraint" overuse.** Still appears frequently in Chs. 9-16, though less than in prior iterations. | Low |

### Category D: Analytical Gaps (Remaining)

| # | Location | Issue |
|---|----------|-------|
| D1 | Ch. 15-16 | **Synthesis chapters run in parallel rather than converging.** Ch. 15 (Climate) and Ch. 16 (Services/Digital) treat their subjects as independent forces. The intersection — how climate policy reshapes services trade geography (data center energy costs, green finance as a tradeable service, climate-driven telemigration) — is gestured at but not developed into a unified framework. A concluding section that integrates both chapters' insights would strengthen the book's culmination. |
| D2 | Ch. 16 | **AI impact specificity still thin.** The chapter now has substantial content on LLMs and compute sovereignty (Section 16.2), which is good. But the task-level predictions for which services will be re-onshored by AI vs. which will remain offshore lack the empirical grounding that the rest of the book provides. No concrete data on AI adoption rates by service category or country is cited. |
| D3 | Ch. 2 | **Measurement of institutional thickness.** The chapter introduces institutional thickness as a core concept but does not provide a concrete operationalization beyond the PCA worked example. How would a researcher measure institutional thickness for a specific region? What data sources? This would strengthen the concept's empirical utility. |
| D4 | All | **Oceania and Central Asia absence.** The preface could acknowledge this gap more explicitly. Australia, New Zealand, and the Pacific Islands (beyond the brief SIDS discussion in Ch. 15) are absent, as are the Central Asian economies. For a book subtitled "Spatial Dynamics, Institutions, and Applied Methods," a brief note on what the exclusion means for generalizability would be appropriate. |

### Category E: Minor Technical Issues

| # | Issue |
|---|-------|
| E1 | **README GitBook link says "(coming soon)."** If the GitBook is not yet live, this is fine; if it is, the link should be updated. |
| E2 | **Ch. 3-B notation convention.** Uses $P_j$ for inward multilateral resistance and $\Pi_i$ for outward, reversing the Anderson-van Wincoop convention. Internally consistent but may confuse students reading the original literature. A footnote acknowledging the notational choice would help. |
| E3 | **Appendix B states "All 107 tests should pass"** — this is correct as of today, but the count will change if tests are added. Consider "All tests should pass" without a specific number. |

---

## Summary Scorecard

| Dimension | Score | Notes |
|-----------|------:|-------|
| Intellectual ambition and scope | 9.5/10 | Remarkable breadth; global coverage unmatched by competitors |
| Writing quality | 9.0/10 | Consistently above textbook norms; occasional overlong sentences |
| Theoretical framework | 9.5/10 | NEG, institutional analysis, and firm heterogeneity are integrated and load-bearing |
| Empirical grounding | 9.0/10 | Strong sourcing throughout; synthesis chapters slightly less empirically grounded |
| Analytical depth | 9.0/10 | Regional chapters excellent; synthesis chapters (15-16) could be more integrated |
| Applied labs | 9.5/10 | Best-in-class pedagogical design; dual-mode architecture is innovative |
| Code quality | 9.5/10 | 107/107 tests pass; clean code; comprehensive test coverage |
| Visual program | 8.0/10 | 8 missing figure files; 2 chapters with out-of-order figure numbering |
| Pedagogical design | 9.0/10 | Pathways, labs, discussion questions excellent; hint blocks absent from Ch. 2 |
| Cross-referencing | 9.5/10 | Dense and well-executed internal linkages |
| Bibliography | 9.5/10 | 260+ references; consistency notes; legislative citations |
| Appendices | 9.0/10 | Math foundations, data guide, and glossary are comprehensive; weak inter-appendix cross-referencing |
| **Overall** | **8.8/10** | |

---

## Path to 9.5+: Prioritized Improvements

### Tier 1: Must-Fix (8.8 -> 9.2)

These are issues that are immediately visible to readers and undermine an otherwise excellent manuscript.

1. **Generate or fix the 8 missing figure files** (A1-A8). Every `fig_chXX_chart_*` reference in Chs. 9-16 resolves to a broken image. The figure-generation scripts (`chXX_figures.py`) exist in the `figures/` directory and likely need to be run or updated to produce these specific outputs. This is the single highest-impact fix.

2. **Add hint/callout blocks to Chapter 2.** Ch. 2 introduces foundational concepts (institutional thickness, related variety, path dependence, varieties of capitalism, developmental state, extractive vs. inclusive institutions) that deserve the same `{% hint %}` treatment every other chapter provides. 5-7 blocks covering the key definitions would bring Ch. 2 into line with the rest of the book.

3. **Fix figure numbering order in Chs. 6 and 15.** Figure 6.3 appears before Figure 6.2; Figure 15.3 appears before Figure 15.2. Either renumber the figures or reorder them in the text.

### Tier 2: Important (9.2 -> 9.4)

4. **Write a convergence section for Ch. 16's conclusion** that integrates the climate analysis of Ch. 15 with the services/digital analysis of Ch. 16. The book's two synthesis chapters currently run in parallel. A 500-word concluding section — "Climate, Services, and the Future Map" — that identifies the intersection (green finance as tradeable service, data center energy geography, climate-driven migration and telemigration) would give the book a unified culmination rather than two separate endings.

5. **Strengthen AI specificity in Ch. 16.** Add 2-3 concrete data points on AI adoption rates in tradeable services (e.g., GitHub Copilot adoption rates among developers, AI-assisted legal research tools market size, AI customer service chatbot deployment rates by country). The rest of the book is empirically dense; the AI section reads as speculative by comparison.

6. **Add a brief operationalization guide for institutional thickness in Ch. 2.** How would a researcher construct an institutional thickness index for a specific region? What data sources (WGI, ICRG, Doing Business successor, subnational surveys)? The PCA worked example is good but abstract. A paragraph connecting it to available datasets would close the gap.

7. **Break overlong sentences in Chs. 9 and 16.** The VoC section of Ch. 9 and the telemigration section of Ch. 16 contain multiple sentences exceeding 100 words. Breaking these into 2-3 shorter sentences would improve readability without losing analytical content.

### Tier 3: Polish (9.4 -> 9.5+)

8. **Reduce residual prose repetition.** A final search-and-vary pass on "the spatial implication is," "the question is whether," "the binding constraint," and "this is not merely X; it is Y" would further polish the prose.

9. **Acknowledge the Oceania/Central Asia gap** in the preface or a footnote. Even a single sentence — "This edition does not cover Oceania or Central Asia, which present distinct spatial dynamics worthy of separate treatment" — would demonstrate intentionality rather than oversight.

10. **Update the README** to remove "(coming soon)" from the GitBook link if the online version is now live, or add a target date if it is not.

11. **Consider hardcoding test count out of Appendix B** — replace "All 107 tests should pass" with "All tests should pass" to prevent documentation drift as tests are added.

12. **Add a footnote in Ch. 3-B** acknowledging that the notation convention for multilateral resistance terms ($P_j$, $\Pi_i$) reverses the Anderson-van Wincoop standard and explaining why.

---

## Comparison to Prior Reviews

This manuscript has been reviewed previously (2026-03-09, scored 8.5 -> 9.5 after revisions; Editorial Board Report 2026-03-05). The prior review identified 18 factual errors, 12 analytical gaps, 9 documentation-drift issues, and 8 prose-quality concerns, and all three tiers of recommended improvements were implemented. This review confirms that the previously identified issues have been addressed:

- Hsieh-Moretti figure corrected (Ch. 1, line 186: now reads "$1.7 trillion" and "8.9 percent")
- Tabuchi multi-region extensions added (Ch. 1, line 190)
- Albouy/Glaeser et al. critique of AJR noted (Ch. 2, line 51)
- Target2 balances added (Ch. 10)
- PAPSS/currency fragmentation added (Ch. 14)
- RDD and SCM sections added to Appendix A
- All 107 tests pass

The new issues identified in this review (missing figure files, Ch. 2 hint blocks, figure ordering, synthesis convergence) are distinct from previously reported concerns.

---

## Bottom Line

This is a genuinely exceptional contribution to the regional economics textbook literature. The combination of global scope, institutional depth, modern econometric methods, and hands-on computational labs is unique. No competing text — not Combes, Mayer, and Thisse (2008), not Brakman, Garretsen, and van Marrewijk (2009), not McCann (2013) — attempts anything close to this breadth while maintaining this level of analytical rigor.

The writing quality is consistently engaging. The opening case studies alone would justify adopting the book. The labs set a new standard for how spatial econometrics can be taught. The five-pathway system demonstrates genuine pedagogical thoughtfulness.

The path from 8.8 to 9.5+ is short and concrete: generate the 8 missing figures, add hint blocks to Ch. 2, write a synthesis-convergence section for Ch. 16, and make a final prose-polish pass. None of these require rethinking the book's architecture. They are finishing touches on an already impressive edifice.

**Recommendation:** Publish with the Tier 1 corrections. This manuscript is ready to become the standard reference for graduate courses in regional and spatial economics.

---

*Independent review prepared 2026-04-07.*
