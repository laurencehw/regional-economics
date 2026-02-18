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
1. Complete Chapter 1-3 specs with concrete thesis/argument/data decisions.
2. Stand up Lab 1 and Lab 5 minimum reproducible notebooks.
3. Resolve access and licensing for WIOD, VIIRS, NUTS-2, ACLED, and Afrobarometer.
