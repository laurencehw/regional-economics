Store Lab 5 raw, mapped, and intermediate data here.

Key files:
- `acled_intake_checklist_2026-02-22.md`: gate checklist for ACLED licensing, schema, and QA.
- `unhcr_intake_checklist_2026-02-23.md`: gate checklist for UNHCR displacement-control intake.
- `source_mappings.json`: canonical mapping of raw source columns to Lab 5 analysis fields.
- `raw_templates/acled_events_template.csv`: minimal schema template for ACLED event-level intake.
- `raw_templates/unhcr_displacement_template.csv`: minimum schema template for UNHCR country-year controls.
- `data/raw/unhcr/unhcr_lab4_origin_controls_2000_2024_2026-02-23.csv`: first real UNHCR pull for Lab 5 scope.
- `data/processed/lab5/unhcr_lab4_controls_mena_2000_2024_2026-02-23.csv`: mapped country-year displacement controls.
- `data/processed/lab5/acled_lab4_country_year_counts_2018_2025_2026-02-23.csv`: ACLED country-year event-count proxy under current access scope.
- `data/processed/lab5/lab4_mena_estimation_panel_2000_2024_2026-02-23.csv`: merged WDI + ACLED + UNHCR estimation-ready panel.
