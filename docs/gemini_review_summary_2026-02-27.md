# Gemini Review Summary — All Completed Chapters
**Date: 2026-02-27**

Reviews conducted on 10 chapters (Chs 1, 2, 3-A, 4, 5, 6, 7, 8, 13, 14). Chapter 7 was reviewed separately earlier and fixes already applied.

**STATUS: All 15 critical fixes applied 2026-02-27. Moderate fixes and structural suggestions remain for future revision passes.**

---

## CRITICAL FIXES (Factual Errors)

### Ch 1 — Micro Foundations
1. **Von Thünen ring order wrong**: Forestry should be the SECOND ring (not later), due to weight-to-value ratios. Text also incorrectly says Von Thünen found forestry placement "surprising" — it was a core prediction.
2. **Bangalore IT employment overstated**: Claims "more than a million workers" by mid-2000s. NASSCOM data: entire Indian IT-BPO was ~1M in FY2004-05; Bangalore alone was ~300-450k. Fix: either change to ~400k or change timeframe to mid-2010s.
3. **Platform economies cross-ref wrong**: Points to Ch 15 (Climate Synthesis) — should be Ch 16 (Future Regionalism).
4. **Missing Hsieh & Moretti (2019)**: Book outline specifies this section (zoning as centrifugal force) but it's absent from draft.

### Ch 3-A — Spatial Econometrics
5. **Chronological paradox**: Intro says "In 2010, a team... published a study... But when Ertur and Koch (2007) reestimated..." — a 2007 paper can't re-estimate a 2010 paper. Fix the chronology.
6. **NUTS-2 count wrong**: Claims 283 NUTS-2 regions. Correct figure is ~244 for EU-27 under NUTS 2024.
7. **Title mismatch**: Chapter titled "Spatial Econometrics & Inequality Measurement" but contains zero inequality measurement content (no Gini, Theil, spatial decomposition). Either add content or fix title.
8. **Missing Lab 3 reference**: Roadmap mentions Labs 1, 2, 4, 5, 6, 7 but omits Lab 3 (South Asia).
9. **Roadmap numbering**: Section 3A.6 (Spatial Panels) exists in text but is missing from the numbered intro roadmap.

### Ch 4 — North American Core
10. **Laredo truck volume ~4× too low**: Claims 3,500 trucks/day. Actual 2023-24 volume: ~14,000-16,000 commercial crossings/day across Laredo bridges.
11. **US-Mexico wage ratio likely wrong**: Claims "roughly 4:1" — most sources show 8:1 or 10:1 for manufacturing. If PPP-adjusted or sector-specific, needs clarification.

### Ch 13 — Africa Urbanization
12. **Lake Chad "90% shrinkage" is a zombie statistic**: Recent satellite data shows the lake stabilized around ~14,000 km² (including wetlands) since the 1990s. The "shrank to 1,500 km²" figure is outdated/misleading.
13. **Lagos top-5 city claim**: UN projections place Lagos in top 10-15 by 2030, not top 5.
14. **WHO physician density benchmark**: "23 per 10,000" refers to total health workers (doctors + nurses + midwives), not physicians alone.

### Ch 14 — AfCFTA & Corridors
15. **Dubious citation**: "Aker, Klein, O'Connell, and Yang (2014)" — Gemini cannot find this four-author combination. May be conflating Aker (2010) on cell phones/grain markets with other studies. Verify.

---

## MODERATE FIXES (Citations, Dates, Clarifications)

### Ch 1
- Kremer (1993) cited for matching/risk-sharing in thick labor markets — should be Helsley & Strange (1990) for matching.

### Ch 2 — Evolutionary/Institutional
- **Becker & Woessmann (2009) misattributed** for Polish phantom borders. That paper is about Protestant Reformation/literacy. Should be Grosfeld & Zhuravskaya (2015).
- De Soto's "289 bureaucratic steps" — clarify this is the 1980s Peru equilibrium.

### Ch 4
- Lab 1's "unconditional ρ ≈ 0" claim — verify matches actual lab code output.

### Ch 5 — Latin America
- Chile's high-income "dip in 2017" is likely wrong — Chile has remained high-income since 2013. The dip was 2014-16 commodity slump but didn't cross the threshold.

### Ch 6 — Flying Geese
- **ASML EUV price**: $350M is High-NA EUV (EXE:5000 series); standard EUV is $180-200M. Should specify.
- Section 6.3 / Institutional Spotlight overlap on "astronauts" and ITRI — de-duplicate.

### Ch 8 — India IT
- **Lab 3 mapping conflict**: Chapter 8 says Lab 3 = India IT mapping, but `fetch_eurostat_nuts2_lab4.py (renamed from lab3)` is European data. Reconcile numbering.
- Medical tourism cross-ref to Ch 7 — verify this is intentional (it is; Ch 7 now has full medical tourism section).

### Ch 14
- Shipping cost comparison (Durban-Mombasa vs Durban-Rotterdam) — note 2023 was volatile; index or caveat.
- Nigeria GDP ($475B) may be overstated for 2026 due to Naira devaluation.

---

## STRUCTURAL SUGGESTIONS (Missing Content)

### Ch 1
- Missing "Consumer City" (Glaeser, Kolko, Saiz 2001) — consumption-side agglomeration
- Missing First Nature vs Second Nature formal distinction
- Missing "Nursery Cities" hypothesis (Duranton & Puga 2001)

### Ch 2
- Missing "Relatedness Trap" concept in Section 2.3
- China puzzle: heavy Acemoglu/Robinson binary doesn't prep for China chapters
- No digital institutions discussion

### Ch 4
- Missing USMCA Environment Chapter 24, NADBank, cross-border water
- No agriculture (Salinas-Sinaloa produce corridor)
- No energy integration (pipelines, Quebec-New England electricity)

### Ch 5
- Missing China Commodities Super-Cycle (2003-2013) timing for Brazil deindustrialization
- Remittances as Dutch Disease mechanism in Central America underdeveloped
- Missing political economy / elite capture dimension of middle-income trap

### Ch 6
- Almost 100% hardware — no software/platform dimension for "Tech Ascendancy"
- No "Flying Geese of Services" (BPO, data centers)
- Missing green energy constraint on fab location (Rapidus/Hokkaido)

### Ch 8
- **Major omission: Post-COVID WFH** and its impact on IT concentration
- Missing India Stack / domestic digital services dimension
- Missing congestion costs as centrifugal force (Bangalore water, traffic)

### Ch 13
- Missing "Consumption Cities" / resource-rent-driven urbanization (Gollin et al.)
- Missing customary vs formal land tenure conflict
- Missing youth bulge / demographic absorption framing
- Missing Chinese BRI infrastructure impact on African urban form

### Ch 14
- Missing PAPSS (Pan-African Payment and Settlement System)
- Missing Guided Trade Initiative (AfCFTA pilot, late 2022)
- North Africa underrepresented (Egypt, Morocco manufacturing/auto)
- Missing African green minerals strategy

---

## PROSE/TONE NOTES

| Chapter | Issue |
|---------|-------|
| Ch 1 | "Tacit vs codified knowledge" explained twice in 1.5 |
| Ch 2 | "Settling the horse race" slightly overconfident; S3/Entrepreneurial Discovery redundant |
| Ch 4 | "Compliance-intensive production" repeated in every section |
| Ch 5 | "Deindustrialization into informality" used 3× — vary phrasing |
| Ch 6 | Section 6.6 slightly journalistic tone vs rest of chapter |
| Ch 8 | "Institutional scaffolding" used 3× in 4 paragraphs |
| Ch 13 | "Urbanization without industrialization" appears 12+ times |
| Ch 14 | "Institutional, not tariff-based" repeated in nearly every section |

---

## CROSS-CHAPTER CONSISTENCY FLAGS

1. Ch 1 cross-refs Ch 15 for platforms → should be Ch 16
2. Ch 3-A omits Lab 3 from its lab survey
3. Ch 5 discusses sovereign wealth → ensure Ch 11 links back
4. Ch 6 Spotlight duplicates Section 6.3 (astronauts/ITRI) — same pattern as Ch 7 (now fixed)
5. Ch 8 Lab 3 numbering conflicts with Eurostat script naming
6. Ch 13 references M-Pesa "Nairobi case study" — verify Ch 13 actually has deep dive
7. Ch 14 Aker et al. (2014) citation needs verification
