Shared figures and map assets for manuscript chapters.

## Quick start

```bash
# Generate all figures (smoke-test mode — no external data needed)
for f in figures/ch*_figures.py; do python "$f" --run-smoke-test; done

# Generate a single chapter's figures
python figures/ch04_figures.py --run-smoke-test --output-dir figures/output

# Run smoke tests
pytest tests/test_figures_smoke.py -v
```

## Architecture

- `figure_utils.py` — Shared infrastructure: style constants, projections, Natural Earth loader, city/corridor annotator, source note helper, plotnine base theme
- `annotations.json` — Per-chapter geographic annotation data (cities, corridors, trade blocs, energy zones, etc.)
- `ch01_figures.py` – `ch16_figures.py` — One script per chapter, each with `--run-smoke-test` and `--output-dir` CLI options
- `output/` — Generated PNGs + PDFs + JSON summaries (gitignored)

## Figure inventory (24 figures)

| # | Chapter | File stem | Type |
|---|---------|-----------|------|
| 1 | Ch 1 | `fig_ch01_concept_von_thunen` | Concentric land-use rings + bid-rent curves |
| 2 | Ch 1 | `fig_ch01_concept_core_periphery` | Krugman tomahawk bifurcation |
| 3 | Ch 2 | `fig_ch02_concept_institutional_spectrum` | Institutional quality spectrum |
| 4 | Ch 3A | `fig_ch03a_concept_weight_matrix` | Spatial weight matrix heatmap |
| 5 | Ch 3A | `fig_ch03a_concept_moran_scatter` | Moran's I scatter plot |
| 6 | Ch 3B | `fig_ch03b_concept_gravity_decay` | Distance-decay curve |
| 7 | Ch 4 | `fig_ch04_map_north_america` | USMCA corridors + Rust Belt |
| 8 | Ch 4 | `fig_ch04_thematic_manufacturing_shift` | Manufacturing employment shift |
| 9 | Ch 5 | `fig_ch05_map_latin_america` | Trade blocs + key economies |
| 10 | Ch 5 | `fig_ch05_thematic_middle_income` | Middle-income trap scatter |
| 11 | Ch 6 | `fig_ch06_map_east_asia` | Tech corridors + SEZs |
| 12 | Ch 6 | `fig_ch06_thematic_dva_trajectory` | DVA trajectory by economy |
| 13 | Ch 7 | `fig_ch07_map_china_asean` | BRI corridors + integration |
| 14 | Ch 7 | `fig_ch07_thematic_provincial_divergence` | Coastal vs inland GDP |
| 15 | Ch 8 | `fig_ch08_map_india_it` | IT-BPO clusters + SEZs |
| 16 | Ch 8 | `fig_ch08_thematic_it_concentration` | IT concentration by state |
| 17 | Ch 9 | `fig_ch09_map_eu_convergence` | EU NUTS-2 GDP choropleth |
| 18 | Ch 10 | `fig_ch10_map_north_south` | North-South divide + Brexit |
| 19 | Ch 11 | `fig_ch11_map_mena_energy` | GCC energy + diversification |
| 20 | Ch 12 | `fig_ch12_map_conflict_zones` | Conflict zones + refugees |
| 21 | Ch 13 | `fig_ch13_map_ssa_urbanization` | Primate cities + corridors |
| 22 | Ch 14 | `fig_ch14_map_afcfta_corridors` | AfCFTA trade corridors |
| 23 | Ch 15 | `fig_ch15_map_climate_vulnerability` | Climate vulnerability global |
| 24 | Ch 16 | `fig_ch16_thematic_services_network` | APS city network |

## Dependencies

- **Required:** numpy, matplotlib
- **Maps:** geopandas (graceful fallback to placeholder if unavailable)
- **Thematic charts:** plotnine + hrbrthemes (optional, falls back to matplotlib)

## Data

Natural Earth shapefiles are downloaded automatically to `data/geodata/` (gitignored) on first use.
