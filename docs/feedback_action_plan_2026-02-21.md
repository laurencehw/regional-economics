# Integrated Feedback Action Plan (2026-02-21)

This plan consolidates reviewer feedback received through 2026-02-21 and maps each point to an execution step.

## Progress Update (2026-02-26)
- **Wave A complete:** Ch 4 expanded with IRA green industrial policy, Mode 2 education, 2 SDC boxes. Ch 5 expanded with Central American Dry Corridor climate migration, 2 SDC boxes.
- **Wave B complete:** Ch 13 expanded with Sahel climate-migration subsection, e-government/digital-ID subsection, SDC box. Ch 14 expanded with eco-tourism corridors subsection, new §14.5 on AfCFTA Protocol on Trade in Services (mobile money interoperability, Mode 3 banking, professional MRAs), SDC box on mirror statistics.
- **All 18 specs detailed:** Chs 5, 10, 12 filled in; P3 companion-specs item closed.
- **Ch 1 opening case study:** Bangalore vs Kolkata (~900 words) added; Part I cross-references verified.
- **CI verified:** 17 smoke tests passing post-renumbering; lab renumbering risk resolved.

## Progress Update (2026-02-24)
- WIOD pull expanded to full WIOTS packages (`WIOTS_in_R.zip`, `WIOTS_in_EXCEL.zip`) with size-validated manifest logging.
- OECD TiVA constrained extract pulled for core Asia economies.
- Additional TiVA robustness extract pulled (`EXGR_FNL` with `OECD` counterpart) and compared against `EXGR_DVA`.
- WIOD-TiVA country/activity concordance templates generated in `data/processed/lab2/`.
- Eurostat NUTS-2 GDP and NUTS 2024 geometry pulled and registered.
- ACLED licensing workflow initialized with a submit-ready request draft, scripted API pull path, validation pull, and production country-year count extraction.
- UNHCR first real pull completed and mapped to Lab 6 country-year controls.
- First Lab 6 estimation-ready panel built by merging WDI outcomes, UNHCR controls, and ACLED count-based treatment proxy.

## Priority Actions

| Priority | Feedback Item | Action | Status | Target Date |
|---|---|---|---|---|
| P0 | Lab setup friction for students | Add zero-install runtime targets (Colab/Codespaces) for Labs 1 and 6, then apply same pattern to Labs 2-5. | In progress | 2026-02-28 |
| P0 | Dataset pipeline risk (WIOD lag; NUTS-2; ACLED licensing) | Acquire WIOD/TiVA and NUTS-2 next; open ACLED licensing track immediately; document backups (ADB MRIO/OECD TiVA). | In progress (WIOD/NUTS done; ACLED request pending) | 2026-03-03 |
| P0 | Early pedagogical validation | Move first classroom pilot to post-Wave B (Labs 1 and 6) to tune difficulty before building Labs 2-5. | Planned | 2026-03-10 |
| P1 | Near-zero Americas `rho` interpretation | Treat weak unconditional spillovers as a design signal; prioritize institution-interaction specs and document logic in gate note. | Done | 2026-02-22 |
| P1 | Border proxy coverage too narrow (3 of 44 countries) | Prototype broader friction proxy using World Bank LPI and compare against BTS-only proxy. | Done | 2026-02-22 |
| P1 | Code hygiene and portability | Remove hardcoded OS paths, reduce absolute-path output printing, add root dependency file, add data storage policy. | In progress | 2026-02-24 |
| P2 | Methods transition to Lab 4/5 is steep | Add Chapter 3 bridge content (counterfactual intuition + boundary discontinuities) and mini-primers in Ch. 9/12. | Planned | 2026-03-15 |
| P2 | Africa lab relevance | Explicitly frame Lab 6 as a nowcasting/on-time measurement use case, not only a data-scarcity workaround. | Done | 2026-02-21 |
| P2 | Americas thematic parallel | Expand Ch. 4 framing of internal US divergence (superstar metros vs left-behind regions). | Done | 2026-02-21 |
| P3 | Companion chapter specs (5/7/9/11/13) remain stubs | Keep as Phase 2 backlog; do not block Part I drafting and methods stabilization. | **Done** — all 18 specs detailed as of 2026-02-26 | 2026-02-26 |

## Immediate Execution Queue
1. Land Lab 6 smoke tests and run full smoke suite (Lab 1 + Lab 6).
2. Finalize code-hygiene sweep (remaining path prints and docs normalization).
3. Capture ACLED request/approval metadata and confirm historical row-level field access scope.
4. Run Lab 5 placebo/robustness SCM checks (alternative treated units and intervention years).

Completed item:
- Institution-interaction specs were run on the blended proxy; see `labs/lab1_americas/output/real_americas_2024_lpi_blend/interaction_specs/`.
- TiVA alternative measure robustness step completed (`EXGR_FNL` vs `EXGR_DVA`) with summary in `data/processed/lab2/tiva_measure_comparison_summary_exgr_dva_vs_exgr_fnl_2026-02-23.json`.
- UNHCR intake schema staging completed (`labs/lab5_mena/data/raw_templates/unhcr_displacement_template.csv` and `labs/lab5_mena/data/unhcr_intake_checklist_2026-02-23.md`).
- ACLED validation pull completed with count-only access under current scope (`data/raw/metadata/acled_lab4_pull_validation_egypt_2024_2026-02-23.json`).
- UNHCR real pull and mapped controls completed (`data/raw/unhcr/unhcr_lab4_origin_controls_2000_2024_2026-02-23.csv`, `data/processed/lab5/unhcr_lab4_controls_mena_2000_2024_2026-02-23.csv`).
- ACLED country-year count proxy extracted for 10 countries (2018-2025) and merged into Lab 5 panel (`data/processed/lab5/lab4_mena_estimation_panel_2000_2024_2026-02-23.csv`).
- First Lab 5 SCM baseline executed for `SYR` (intervention `2018`) with outputs in `labs/lab5_mena/output/scm_baseline/`.

## Definition of Done for This Feedback Round
- Drafting plan updated to reflect cloud execution, early pilot timing, and dataset fallback strategy.
- Lab 1 interpretation docs reflect conditional-spillover framing.
- Lab 6 docs explicitly connect night-lights analysis to nowcasting.
- Repository has a documented data-storage policy and root dependency baseline.
