# UNHCR Intake Checklist (Lab 4 MENA)

Use this checklist when staging UNHCR displacement controls for the MENA SCM panel.

## Source and Coverage Gate
- [ ] Confirm UNHCR endpoint/table and extraction date.
- [ ] Confirm country scope aligns with Lab 4 MENA `iso3` list.
- [ ] Confirm annual coverage overlaps with WDI and ACLED panel years.

## Schema Gate
- [ ] Map source columns to `raw_templates/unhcr_displacement_template.csv`.
- [ ] Ensure `iso3` is uppercase three-letter code.
- [ ] Ensure `year` is integer and unique per (`iso3`, `year`) in panelized output.
- [ ] Convert displacement measures to numeric, non-negative fields.

## Analysis-Ready Gate
- [ ] Build canonical country-year file keyed by (`iso3`, `year`).
- [ ] Document variable definitions and aggregation choices.
- [ ] Register mapped output path in `docs/data_inventory.md`.
