# The New Regional Economics

Working repository for drafting and replication assets for *The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods*.

## Current Scope
- 16-chapter structure (Parts I–VII) with 7 Applied Labs.
- All 18 chapter specs are detailed (Chs 1–16 including 3-A and 3-B).
- **8 chapters drafted — Waves A and B complete:**
  - Part I foundations: Chs 1, 2, 3-A, 3-B
  - Wave A (Americas): Chs 4, 5 — full drafts with climate, services, and Spatial Data Challenge content
  - Wave B (Africa): Chs 13, 14 — full drafts with climate migration, e-government, eco-tourism, services protocol, and Spatial Data Challenge content
- 9 chapters remaining (Chs 6–12, 15–16).
- Applied lab folders scaffolded for Labs 1–7; Lab 1 complete on real data; Labs 4 and 5 partially complete; Labs 2, 3, 6, 7 scaffolded.

## Repository Layout
- `BOOK_OUTLINE.md`: full conceptual outline.
- `DRAFTING_PLAN.md`: phased writing and review plan.
- `chapters/specs/`: all 18 chapter specifications (detailed).
- `chapters/`: 8 drafted chapter files.
- `labs/`: one folder per applied lab (data, code, output).
- `data/`: shared raw and processed datasets used across chapters/labs.
- `figures/`: shared figure artifacts.
- `references/`: bibliography material and source notes.
- `scripts/`: utility scripts for data prep and automation.
- `docs/`: process docs (data inventory, workflow notes, next steps).

## Drafting Workflow
1. Fill chapter specs in `chapters/specs/` before drafting prose.
2. Draft prose chapter files in `chapters/`.
3. Build each lab in parallel with chapter drafting in `labs/`.
4. Register every dataset in `docs/data_inventory.md` before use.
5. Keep methods, notation, and variable naming consistent with Part I.

## Immediate Priorities
1. **Acquire VIIRS data and validate Lab 6 at scale** (30+ Sub-Saharan African countries).
2. **Wave A+B review gate** — internal review of Chs 1–5, 13–14 before proceeding to Wave C.
3. **Wave C (East Asia): Chs 6–7** — next prose drafting wave.
4. ACLED row-level access confirmation (currently count-based proxy only).
5. Zero-install cloud execution targets for Labs 1 and 6 (Colab/Codespaces).
