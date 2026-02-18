Lab 1 data workspace.

Key files:
- `source_mappings.json`: canonical variable mappings from WDI/Comtrade/BTS source columns.
- `panel_template.csv` and `trade_template.csv`: minimal canonical templates.
- `raw_templates/`: expected raw-source schemas for mapping.
- `comtrade_api_pull.csv`: direct pull from UN Comtrade API in expected raw schema.

Primary generated artifacts from `code/prepare_lab1_inputs.py`:
- `panel_mapped.csv`
- `trade_mapped.csv`
- `mapping_summary.json`
