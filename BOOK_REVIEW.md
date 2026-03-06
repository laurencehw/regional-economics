# Book Review: *The New Regional Economics*

**Manuscript:** *The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods*
**Author:** Laurence Wilse-Samson, NYU Wagner School of Public Policy
**Reviewer Date:** 2026-03-06

---

## Overall Grade: 8.5 / 10

This is an impressive, ambitious, and largely successful graduate textbook. It attempts something rare: a unified treatment of regional economics across every major world region, integrating new economic geography, institutional analysis, spatial econometrics, and hands-on computational labs. The result is a manuscript that is analytically rigorous, pedagogically thoughtful, and remarkably current. The writing quality is consistently above the norm for academic textbooks, and the applied labs represent a genuine innovation in how this material can be taught.

The grade reflects a manuscript that is substantively excellent but has addressable issues in sourcing, visual presentation, and a few structural gaps that prevent it from reaching its full potential.

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

### 1. Unsourced Statistics (~138 claims) -- HIGH PRIORITY
The most significant issue. The theory/methods chapters (Ch. 1-3) generally cite their sources well. The regional chapters (Ch. 4-16) contain extensive specific numerical claims from public databases (WDI, Eurostat, NBS, NASSCOM) without inline attribution. Examples:
- "North American goods trade exceeded $1.5 trillion in 2024" (Ch. 4 -- no source)
- "TSMC manufactures over 90% of advanced chips below 7nm" (Ch. 6 -- no source)
- "India exported approximately $200 billion in IT-BPO services" (Ch. 8 -- no source)
- "Shipping Durban to Mombasa cost approximately $1,800" (Ch. 14 -- no source)

Many of these sources already exist in the bibliography -- they simply need inline parenthetical citations. Peer reviewers will flag this immediately. **This is the single most important fix before submission.**

### 2. Visual Presentation -- HIGH PRIORITY
- **167 wall-of-text sections** (5+ consecutive paragraphs with no visual break) across the manuscript. Zero GitBook callout/hint blocks exist anywhere. Adding definition boxes, warning callouts, and key-concept highlights would dramatically improve readability at low cost.
- **Figure front-loading:** In two-figure chapters, both figures appear in the first 70 lines, leaving 60-90% of the chapter as a figure-free zone. Chapters 9-16 have only one figure each.
- **7 figures graded C or below** with overlapping labels, oversaturated color palettes, and legibility problems. The MENA energy map (Ch. 11) and North America map (Ch. 4) are the worst offenders and need Gulf inset maps / label offset adjustments.

### 3. Chapter Length and Depth Variation
- Chapter 2 (Institutional Frameworks, ~8,300 words) is noticeably shorter than most regional chapters (~10,000-11,800 words), leaving foundational concepts like related variety and institutional thickness underdeveloped given how heavily later chapters rely on them.
- Chapter 12 (Conflict Economics, ~9,800 words) and Chapter 13 (SSA Urbanization, ~10,000 words) are slightly compressed given the enormous scope of their topics.
- Lab 3 (South Asia, IT concentration) is the thinnest lab -- it lacks a robustness spec runner and visualization modules that the other labs have.

### 4. Prose Issues
Several chapters (Ch. 9, 10, 11, 12, 13, 14) open with generic overview statements rather than the vivid empirical hooks that make Ch. 1, 6, and 10 so effective. The existing editorial board report provides excellent rewritten openings for all of these. Additionally, a handful of AI-ism phrases appear: "plays a crucial role" (3 chapters), "multifaceted" (2 chapters), "a testament to" (1 chapter), "in the realm of" (1 chapter). These should be eliminated.

### 5. Code Bugs (Minor but Should Be Fixed)
- **Intervention year mismatch (Lab 5):** The SCM baseline defaults to `--intervention-year 2018` while the robustness script defaults to `2022`. This will confuse students.
- **lab4/lab5 naming confusion:** ACLED fetch scripts reference "Lab 4" in docstrings but have `lab5` filenames. The panel builder outputs to a path containing `lab4` within the `lab5` directory. This is clearly a residual from a renaming.
- **Duplicate adjacency entries** in the VIIRS Africa script (4 reverse pairs).
- **Missing bibliography entries:** Anselin (1995), Head & Mayer (2014), Taylor & Derudder (2016) are cited but not in the bibliography.

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

1. **Expand Chapter 2** by ~2,000-3,000 words. The institutional toolkit is foundational to everything that follows. Related variety, institutional thickness, and path dependency deserve worked examples.

2. **Add a second figure to each of Chapters 9-16.** Currently these chapters have only one figure each, leaving long stretches of unbroken text.

3. **Strengthen Lab 3** with a robustness spec runner and at least one visualization module to match the standard set by the other labs.

4. **Add unit tests** for core estimation functions (SAR estimator, SCM solver, PPML IRLS loop). The current test suite is entirely subprocess-based smoke tests -- excellent for integration testing but insufficient for catching numerical regressions.

5. **Consider adding Oceania or Russia/Central Asia** as a brief chapter or extended case study. These are the most notable regional omissions.

6. **Add a "data vintage" note** somewhere prominent, given that many statistics cite 2023-2024 sources that will age.

---

## Summary Scorecard

| Dimension | Score | Notes |
|-----------|:-----:|-------|
| Intellectual ambition and scope | 9/10 | Remarkable breadth with analytical depth |
| Writing quality | 8/10 | Strong overall; 6 chapter openings need rework |
| Theoretical framework | 9/10 | Excellent NEG + institutions integration |
| Empirical grounding | 7/10 | Good content, but 138 unsourced claims |
| Applied labs | 9/10 | Innovative dual-mode design; Lab 3 is thin |
| Code quality | 8/10 | Clean and well-organized; minor bugs |
| Visual presentation | 6/10 | Figures exist but quality uneven; no callout blocks |
| Pedagogical design | 9/10 | Pathways, labs, and discussion questions are excellent |
| Test suite | 7/10 | Good smoke tests; no unit or numerical tests |
| Bibliography | 8/10 | Comprehensive; 3 missing entries, 138 missing inline citations |
| **Overall** | **8.5/10** | |

---

## Bottom Line

This is a genuinely valuable contribution to the regional economics textbook literature. The combination of global scope, institutional depth, modern econometric methods, and hands-on computational labs is unique. The manuscript's weaknesses -- unsourced statistics, visual presentation gaps, a few prose issues -- are all fixable without structural changes. With the improvements outlined above, this could be a 9.5/10 textbook and the standard reference for graduate courses in regional and spatial economics.

---

*Review prepared 2026-03-06.*
