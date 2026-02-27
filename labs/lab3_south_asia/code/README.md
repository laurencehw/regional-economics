# Lab 3 Code

Scripts for the South Asia IT-BPO concentration analysis lab.

## Scripts

| Script | Description | Status |
|---|---|---|
| `prepare_lab3_inputs.py` | Map KLEMS IT-sector data to canonical panel | Complete |
| `lab3_concentration_scaffold.py` | Compute LQ, HHI, Gini; synthetic data mode | Complete |
| `fetch_rbi_services.py` | RBI services trade data acquisition | Not started |

## Usage

### Smoke test (synthetic data)
```bash
python lab3_concentration_scaffold.py --run-smoke-test --output-dir ../output
```

### Real data
```bash
python prepare_lab3_inputs.py \
  --klems-input ../data/raw/klems_india.csv \
  --mappings ../data/source_mappings.json \
  --output-dir ../data

python lab3_concentration_scaffold.py \
  --panel ../data/panel_mapped.csv \
  --year 2018 \
  --output-dir ../output
```
