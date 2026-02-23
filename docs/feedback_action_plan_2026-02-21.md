# Integrated Feedback Action Plan (2026-02-21)

This plan consolidates reviewer feedback received through 2026-02-21 and maps each point to an execution step.

## Progress Update (2026-02-23)
- WIOD pull expanded to full WIOTS packages (`WIOTS_in_R.zip`, `WIOTS_in_EXCEL.zip`) with size-validated manifest logging.
- OECD TiVA constrained extract pulled for core Asia economies.
- Additional TiVA robustness extract pulled (`EXGR_FNL` with `OECD` counterpart) and compared against `EXGR_DVA`.
- WIOD-TiVA country/activity concordance templates generated in `data/processed/lab2/`.
- Eurostat NUTS-2 GDP and NUTS 2024 geometry pulled and registered.
- ACLED licensing workflow initialized with a submit-ready request draft (submission pending).
- UNHCR intake schema template and checklist staged for Lab 4 controls.

## Priority Actions

| Priority | Feedback Item | Action | Status | Target Date |
|---|---|---|---|---|
| P0 | Lab setup friction for students | Add zero-install runtime targets (Colab/Codespaces) for Labs 1 and 5, then apply same pattern to Labs 2-4. | In progress | 2026-02-28 |
| P0 | Dataset pipeline risk (WIOD lag; NUTS-2; ACLED licensing) | Acquire WIOD/TiVA and NUTS-2 next; open ACLED licensing track immediately; document backups (ADB MRIO/OECD TiVA). | In progress (WIOD/NUTS done; ACLED request pending) | 2026-03-03 |
| P0 | Early pedagogical validation | Move first classroom pilot to post-Wave B (Labs 1 and 5) to tune difficulty before building Labs 2-4. | Planned | 2026-03-10 |
| P1 | Near-zero Americas `rho` interpretation | Treat weak unconditional spillovers as a design signal; prioritize institution-interaction specs and document logic in gate note. | Done | 2026-02-22 |
| P1 | Border proxy coverage too narrow (3 of 44 countries) | Prototype broader friction proxy using World Bank LPI and compare against BTS-only proxy. | Done | 2026-02-22 |
| P1 | Code hygiene and portability | Remove hardcoded OS paths, reduce absolute-path output printing, add root dependency file, add data storage policy. | In progress | 2026-02-24 |
| P2 | Methods transition to Lab 3/4 is steep | Add Chapter 3 bridge content (counterfactual intuition + boundary discontinuities) and mini-primers in Ch. 8/11. | Planned | 2026-03-15 |
| P2 | Africa lab relevance | Explicitly frame Lab 5 as a nowcasting/on-time measurement use case, not only a data-scarcity workaround. | Done | 2026-02-21 |
| P2 | Americas thematic parallel | Expand Ch. 4 framing of internal US divergence (superstar metros vs left-behind regions). | Done | 2026-02-21 |
| P3 | Companion chapter specs (5/7/9/11/13) remain stubs | Keep as Phase 2 backlog; do not block Part I drafting and methods stabilization. | Acknowledged | 2026-03-20 |

## Immediate Execution Queue
1. Land Lab 5 smoke tests and run full smoke suite (Lab 1 + Lab 5).
2. Finalize code-hygiene sweep (remaining path prints and docs normalization).
3. Submit ACLED licensing request and log approval metadata in tracker JSON.
4. Execute first UNHCR pull and map to canonical Lab 4 country-year controls.

Completed item:
- Institution-interaction specs were run on the blended proxy; see `labs/lab1_americas/output/real_americas_2024_lpi_blend/interaction_specs/`.
- TiVA alternative measure robustness step completed (`EXGR_FNL` vs `EXGR_DVA`) with summary in `data/processed/lab2/tiva_measure_comparison_summary_exgr_dva_vs_exgr_fnl_2026-02-23.json`.
- UNHCR intake schema staging completed (`labs/lab4_mena/data/raw_templates/unhcr_displacement_template.csv` and `labs/lab4_mena/data/unhcr_intake_checklist_2026-02-23.md`).

## Definition of Done for This Feedback Round
- Drafting plan updated to reflect cloud execution, early pilot timing, and dataset fallback strategy.
- Lab 1 interpretation docs reflect conditional-spillover framing.
- Lab 5 docs explicitly connect night-lights analysis to nowcasting.
- Repository has a documented data-storage policy and root dependency baseline.
