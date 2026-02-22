# ACLED Intake Checklist (Lab 4 MENA)

Use this checklist immediately after ACLED access is approved.

## Access Gate
- [ ] Access request submitted and request reference logged.
- [ ] Approval date and license constraints recorded in `data/raw/metadata/acled_access_tracker_2026-02-22.json`.
- [ ] Country/time scope for MENA confirmed under approved terms.

## Raw Pull Gate
- [ ] Raw pull stored outside git (`data/external/...` or approved external path).
- [ ] Extraction metadata logged (date, endpoint, filters, account identifier alias).
- [ ] Row count and unique event ID count recorded.

## Schema Gate
- [ ] Raw columns mapped to template schema (`raw_templates/acled_events_template.csv`).
- [ ] `event_date` parseable to ISO date.
- [ ] `iso3` harmonized to uppercase three-letter codes.
- [ ] Latitude/longitude numeric and within valid ranges.
- [ ] Fatalities coerced to non-negative numeric values.

## Analysis-Ready Gate
- [ ] Country-year panel generated for SCM (`iso3`, `year`, treatment/event metrics).
- [ ] Merge coverage checked against WDI and UNHCR keys.
- [ ] Final mapped file registered in `docs/data_inventory.md`.
