# Lab 7 Code

Scripts for the services trade gravity capstone lab.

## Scripts

| Script | Description | Status |
|---|---|---|
| `gravity_services_scaffold.py` | PPML gravity estimation (services vs. goods) | Complete |
| `stri_tariff_equivalent.py` | Convert STRI to ad-valorem tariff equivalents | Complete |
| `servicification_decomposition.py` | TiVA service content decomposition | Not started |
| `cloud_geography_mapper.py` | Map cloud data centers vs. data localization | Not started |
| `fetch_wto_services_trade.py` | Fetch WTO BOP services trade data | Not started |
| `fetch_oecd_stri.py` | Fetch OECD STRI scores | Not started |

## Usage

### Smoke test (synthetic data)
```bash
python gravity_services_scaffold.py --run-smoke-test --output-dir ../output
python stri_tariff_equivalent.py --run-smoke-test --output-dir ../output/stri
```

### Real data
```bash
python gravity_services_scaffold.py \
  --trade ../data/raw/wto_services_bilateral.csv \
  --gravity ../data/raw/cepii_geodist.csv \
  --year 2019 \
  --output-dir ../output

python stri_tariff_equivalent.py \
  --stri ../data/raw/oecd_stri.csv \
  --trade ../data/raw/wto_services_bilateral.csv \
  --gravity ../data/raw/cepii_geodist.csv \
  --year 2019 \
  --output-dir ../output/stri
```
