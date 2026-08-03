#!/bin/bash
# Build consolidated book PDF
# Usage: bash build_pdf.sh

PANDOC="C:/Users/lwils/AppData/Local/Pandoc/pandoc.exe"
XELATEX="C:/Users/lwils/AppData/Local/Programs/MiKTeX/miktex/bin/x64/xelatex.exe"
OUTFILE="book_review_draft.pdf"

cd "G:/My Drive/book drafts/regional economics/regional-economics"

# Ordered list of all chapters
FILES=(
  chapters/preface_pathways.md
  chapters/ch01_micro_foundations_of_space.md
  chapters/ch02_evolutionary_and_institutional_frameworks.md
  chapters/ch03a_spatial_econometrics.md
  chapters/ch03b_trade_measurement_gravity.md
  chapters/ch04_the_north_american_core.md
  chapters/ch05_latin_america_middle_income_trap.md
  chapters/ch06_flying_geese_and_tech_ascendancy.md
  chapters/ch07_china_divergence_asean_fragmentation.md
  chapters/ch08_india_geography_of_it_services.md
  chapters/ch09_single_market_convergence.md
  chapters/ch10_north_south_divide_disintegration.md
  chapters/ch11_post_carbon_transition_sovereign_wealth.md
  chapters/ch12_fragile_states_conflict_economics.md
  chapters/ch13_urbanization_without_industrialization.md
  chapters/ch14_afcfta_functional_corridors.md
  chapters/ch15_climate_stranded_regions_future_map.md
  chapters/ch16_future_of_global_regionalism.md
  chapters/appendix_a_mathematical_foundations.md
  chapters/appendix_b_data_software_guide.md
  chapters/appendix_c_glossary.md
  chapters/bibliography.md
)

echo "Building PDF from ${#FILES[@]} files..."

"$PANDOC" \
  "${FILES[@]}" \
  -o "$OUTFILE" \
  --pdf-engine="$XELATEX" \
  --number-sections \
  --toc \
  --toc-depth=2 \
  -V documentclass=report \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V linkcolor=blue \
  -V urlcolor=blue \
  -V toccolor=black \
  -V mainfont="Cambria" \
  -V sansfont="Calibri" \
  -V monofont="Consolas" \
  -V title="The New Regional Economics" \
  -V subtitle="Spatial Dynamics, Institutions, and Applied Methods" \
  -V author="Laurence Wilse-Samson" \
  -V date="Review Draft — March 2026" \
  --top-level-division=chapter \
  --resource-path=.:figures \
  2>&1

if [ $? -eq 0 ]; then
  echo ""
  echo "SUCCESS: $OUTFILE created"
  ls -lh "$OUTFILE"
else
  echo ""
  echo "FAILED — see errors above"
fi
