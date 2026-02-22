# The New Regional Economics

Working repository for drafting and replication assets for *The New Regional Economics: Spatial Dynamics, Institutions, and Applied Methods*.

## Current Scope
- Outline and drafting plan are in place.
- Chapter spec stubs are available for Chapters 1-15.
- Applied lab folders are scaffolded for Labs 1-5.

## Repository Layout
- `BOOK_OUTLINE.md`: full conceptual outline.
- `DRAFTING_PLAN.md`: phased writing and review plan.
- `chapters/specs/`: chapter specification templates and working specs.
- `labs/`: one folder per applied lab (data, code, output).
- `data/`: shared raw and processed datasets used across chapters/labs.
- `figures/`: shared figure artifacts.
- `references/`: bibliography material and source notes.
- `scripts/`: utility scripts for data prep and automation.
- `docs/`: process docs (data inventory, workflow notes, etc.).

## Drafting Workflow
1. Fill chapter specs in `chapters/specs/` before drafting prose.
2. Draft prose chapter-by-chapter in a future `chapters/drafts/` structure.
3. Build each lab in parallel with chapter drafting in `labs/`.
4. Register every dataset in `docs/data_inventory.md` before use.
5. Keep methods, notation, and variable naming consistent with Part I.

## Immediate Priorities
1. Expand WIOD/TiVA pulls from starter extracts to production-scale Lab 2 inputs (full WIOTS + additional TiVA measures), then lock concordances.
2. Open ACLED licensing/access workflow and build the first MENA-lab intake checklist while data access is pending.
3. Prepare early classroom pilot package for Labs 1 and 5 (cloud-first execution path + interpretation notes).
