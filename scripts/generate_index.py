"""Generate a subject index for the Regional Economics textbook.

Scans all chapter markdown files for key terms (glossary entries, place names,
acronyms, named models/theorems, datasets, and concepts) and outputs a
formatted markdown index at chapters/subject_index.md.

Usage:
    python scripts/generate_index.py
"""

import re
from pathlib import Path
from collections import defaultdict

REPO = Path(r"G:\My Drive\book drafts\regional economics\regional-economics")
CHAPTERS_DIR = REPO / "chapters"
OUTPUT = CHAPTERS_DIR / "subject_index.md"

# Ordered list of files to scan, with their index labels
FILES_AND_LABELS = [
    ("preface_pathways.md", "P"),
    ("ch01_micro_foundations_of_space.md", "1"),
    ("ch02_evolutionary_and_institutional_frameworks.md", "2"),
    ("ch03a_spatial_econometrics.md", "3-A"),
    ("ch03b_trade_measurement_gravity.md", "3-B"),
    ("ch04_the_north_american_core.md", "4"),
    ("ch05_latin_america_middle_income_trap.md", "5"),
    ("ch06_flying_geese_and_tech_ascendancy.md", "6"),
    ("ch07_china_divergence_asean_fragmentation.md", "7"),
    ("ch08_india_geography_of_it_services.md", "8"),
    ("ch09_single_market_convergence.md", "9"),
    ("ch10_north_south_divide_disintegration.md", "10"),
    ("ch11_post_carbon_transition_sovereign_wealth.md", "11"),
    ("ch12_fragile_states_conflict_economics.md", "12"),
    ("ch13_urbanization_without_industrialization.md", "13"),
    ("ch14_afcfta_functional_corridors.md", "14"),
    ("ch15_climate_stranded_regions_future_map.md", "15"),
    ("ch16_future_of_global_regionalism.md", "16"),
    ("appendix_a_mathematical_foundations.md", "A"),
    ("appendix_b_data_software_guide.md", "B"),
    ("appendix_c_glossary.md", "C"),
    ("bibliography.md", "Bib"),
]


def extract_glossary_terms(glossary_path: Path) -> list[str]:
    """Extract bold-defined terms from the glossary."""
    text = glossary_path.read_text(encoding="utf-8")
    terms = []
    for m in re.finditer(r"^\*\*(.+?)\.\*\*", text, re.MULTILINE):
        term = m.group(1).strip()
        # Handle math-symbol terms: $$\beta$$-convergence -> beta-convergence display
        # Replace known math symbols with readable text
        term = term.replace(r"$$\beta$$", "Beta")
        term = term.replace(r"$$\sigma$$", "Sigma")
        # Clean up any remaining markdown math
        term = re.sub(r"\$\$.*?\$\$", "", term).strip()
        # Skip empty terms or terms that are just punctuation
        if term and len(term) > 1:
            terms.append(term)
    return terms


def build_term_registry(glossary_terms: list[str]) -> dict[str, list[str]]:
    """Build a dict mapping display_name -> list of regex patterns to search.

    Returns dict: {display_name: [pattern1, pattern2, ...]}
    """
    registry: dict[str, list[str]] = {}

    # Terms to skip from glossary (handled better by manual entries below)
    glossary_skip = {
        "Night-lights data",  # handled by night-lights concept entry
        "Bartik instrument",  # handled by models_scholars
        "CBAM (Carbon Border Adjustment Mechanism)",  # handled by acronyms
        "GATS (General Agreement on Trade in Services)",  # handled by acronyms
        "STRI (Services Trade Restrictiveness Index)",  # handled by acronyms
        "PPML (Poisson Pseudo-Maximum Likelihood)",  # handled by acronyms + datasets
        "MRA (Mutual Recognition Agreement)",  # handled by acronyms
    }

    # --- 1. Glossary terms ---
    for term in glossary_terms:
        if term in glossary_skip:
            continue

        # For terms with parenthetical expansions like "MAUP (Modifiable...)"
        # index under the main form
        display = term
        patterns = [re.escape(term)]

        # Also match without the parenthetical
        paren_match = re.match(r"^(.+?)\s*\((.+)\)$", term)
        if paren_match:
            short = paren_match.group(1).strip()
            expanded = paren_match.group(2).strip()
            patterns.append(r"\b" + re.escape(short) + r"\b")
            patterns.append(re.escape(expanded))
        else:
            # Add word-boundary version for short terms
            if len(term.split()) <= 3:
                patterns = [r"\b" + re.escape(term) + r"\b"]
            else:
                patterns = [re.escape(term)]

        # Special handling for Beta/Sigma-convergence: search for the
        # LaTeX source form and common prose forms
        if "Beta-convergence" in display:
            patterns = [
                r"\\beta.*convergence",
                r"\bbeta.{0,3}convergence\b",
                r"\bconditional\s+convergence\b",
            ]
        elif "Sigma-convergence" in display:
            patterns = [
                r"\\sigma.*convergence",
                r"\bsigma.{0,3}convergence\b",
            ]

        registry[display] = patterns

    # --- 2. Acronyms and institutions ---
    acronyms = {
        "ACLED (Armed Conflict Location and Event Data)": ["ACLED"],
        "AfCFTA (African Continental Free Trade Area)": ["AfCFTA"],
        "ASEAN (Association of Southeast Asian Nations)": ["ASEAN"],
        "BRI (Belt and Road Initiative)": ["BRI", "Belt and Road"],
        "CBAM (Carbon Border Adjustment Mechanism)": ["CBAM"],
        "CPTPP": ["CPTPP", "Trans-Pacific Partnership"],
        "ECB (European Central Bank)": ["ECB", "European Central Bank"],
        "ERDF (European Regional Development Fund)": ["ERDF"],
        "EU (European Union)": ["EU", "European Union"],
        "FDI (Foreign Direct Investment)": ["FDI", "foreign direct investment"],
        "GATS (General Agreement on Trade in Services)": ["GATS"],
        "GCC (Gulf Cooperation Council)": ["GCC", "Gulf Cooperation Council"],
        "GDPR (General Data Protection Regulation)": ["GDPR"],
        "GVC (Global Value Chain)": ["GVC", "global value chain"],
        "ILO (International Labour Organization)": ["ILO"],
        "IMF (International Monetary Fund)": ["IMF", "International Monetary Fund"],
        "IRA (Inflation Reduction Act)": ["Inflation Reduction Act"],
        "NAFTA (North American Free Trade Agreement)": ["NAFTA"],
        "NASSCOM": ["NASSCOM"],
        "NEG (New Economic Geography)": ["NEG", "New Economic Geography"],
        "NUTS (Nomenclature of Territorial Units)": ["NUTS"],
        "OCA (Optimum Currency Area)": ["OCA", "optimum currency area"],
        "OECD": ["OECD"],
        "RCEP (Regional Comprehensive Economic Partnership)": ["RCEP"],
        "SAARC": ["SAARC"],
        "STRI (Services Trade Restrictiveness Index)": ["STRI"],
        "SWF (Sovereign Wealth Fund)": ["SWF", "sovereign wealth fund"],
        "UNHCR": ["UNHCR"],
        "USMCA (United States-Mexico-Canada Agreement)": ["USMCA"],
        "World Bank": ["World Bank"],
        "WTO (World Trade Organization)": ["WTO", "World Trade Organization"],
    }

    for display, search_terms in acronyms.items():
        pats = []
        for st in search_terms:
            if st.isupper() and len(st) <= 6:
                pats.append(r"\b" + re.escape(st) + r"\b")
            else:
                pats.append(r"\b" + re.escape(st) + r"\b")
        # Only add if not already covered by glossary
        if display not in registry:
            registry[display] = pats

    # --- 3. Named models, theorems, and scholars ---
    models_scholars = {
        "Acemoglu, Daron": [r"\bAcemoglu\b"],
        "Akamatsu, Kaname": [r"\bAkamatsu\b"],
        "Anderson-van Wincoop gravity model": [r"\bAnderson.{0,5}van\s*Wincoop\b"],
        "Arrow, Kenneth": [r"\bArrow\b"],
        "Baldwin, Richard": [r"\bBaldwin\b"],
        "Bartik instrument": [r"\bBartik\b"],
        "Christaller, Walter": [r"\bChristaller\b"],
        "Combes, Pierre-Philippe": [r"\bCombes\b"],
        "Dixit-Stiglitz model": [r"\bDixit.{0,3}Stiglitz\b"],
        "Duranton, Gilles": [r"\bDuranton\b"],
        "Fujita, Masahisa": [r"\bFujita\b"],
        "Glaeser, Edward": [r"\bGlaeser\b"],
        "Grossman-Rossi-Hansberg (task trading)": [r"\bGrossman.{0,5}Rossi.{0,3}Hansberg\b"],
        "Head-Mayer (gravity)": [r"\bHead.{0,5}Mayer\b"],
        "Heckscher-Ohlin model": [r"\bHeckscher.{0,3}Ohlin\b"],
        "Henderson, J. Vernon": [r"\bHenderson\b"],
        "Hotelling, Harold": [r"\bHotelling\b"],
        "Jacobs, Jane": [r"\bJacobs\b"],
        "Johnson, Chalmers": [r"\bChalmers\b", r"\bJohnson.*MITI\b"],
        "Krugman, Paul": [r"\bKrugman\b"],
        "Lewis, W. Arthur": [r"\bLewis\b.*\b(?:dual|surplus|turning)\b", r"\bW\.\s*Arthur\s*Lewis\b", r"\bLewis\s*model\b", r"\bLewisian\b"],
        "Marshall, Alfred": [r"\bMarshall(?:ian)?\b"],
        "Melitz model": [r"\bMelitz\b"],
        "Mundell, Robert": [r"\bMundell\b"],
        "Myrdal, Gunnar": [r"\bMyrdal\b"],
        "North, Douglass": [r"\bDouglass\s*North\b", r"\bNorth\s*\(\d{4}\)\b"],
        "Olson, Mancur": [r"\bOlson\b"],
        "Porter, Michael": [r"\bPorter\b"],
        "Ricardo, David": [r"\bRicardo\b", r"\bRicardian\b"],
        "Rodrik, Dani": [r"\bRodrik\b"],
        "Romer, Paul": [r"\bRomer\b"],
        "Rybczynski theorem": [r"\bRybczynski\b"],
        "Sachs, Jeffrey": [r"\bSachs\b"],
        "Santos Silva and Tenreyro (PPML)": [r"\bSantos\s*Silva\b", r"\bTenreyro\b"],
        "Stolper-Samuelson theorem": [r"\bStolper.{0,3}Samuelson\b"],
        "Venables, Anthony": [r"\bVenables\b"],
        "Viner, Jacob (trade creation/diversion)": [r"\bViner\b"],
        "von Thunen, Johann Heinrich": [r"\bvon\s*Th.{0,2}nen\b", r"\bTh.{0,2}nen\b"],
        "Weber, Alfred (location theory)": [r"\bWeber\b.*\b(?:location|triangle|weight)\b", r"\bWeber(?:ian)?\s+(?:triangle|location|model)\b"],
        "Williamson, Oliver": [r"\bWilliamson\b"],
        "Zipf's law": [r"\bZipf\b"],
    }

    for display, pats in models_scholars.items():
        if display not in registry:
            registry[display] = pats

    # --- 4. Datasets and empirical tools ---
    datasets = {
        "ACLED (Armed Conflict Location and Event Data)": [r"\bACLED\b"],
        "Comtrade (UN)": [r"\bComtrade\b"],
        "FRED (Federal Reserve Economic Data)": [r"\bFRED\b"],
        "Penn World Table": [r"\bPenn\s*World\s*Table\b"],
        "TiVA (Trade in Value Added)": [r"\bTiVA\b"],
        "VIIRS (night-lights satellite data)": [r"\bVIIRS\b"],
        "WDI (World Development Indicators)": [r"\bWDI\b", r"\bWorld Development Indicators\b"],
        "WIOD (World Input-Output Database)": [r"\bWIOD\b"],
    }
    for display, pats in datasets.items():
        if display not in registry:
            registry[display] = pats

    # --- 5. Place names ---
    places = {
        "Abu Dhabi": [r"\bAbu\s*Dhabi\b"],
        "Addis Ababa": [r"\bAddis\s*Ababa\b"],
        "Bangladesh": [r"\bBangladesh\b"],
        "Bangalore (Bengaluru)": [r"\bBangalore\b", r"\bBengaluru\b"],
        "Beijing": [r"\bBeijing\b"],
        "Brazil": [r"\bBrazil\b"],
        "Buenos Aires": [r"\bBuenos\s*Aires\b"],
        "Cairo": [r"\bCairo\b"],
        "Cambodia": [r"\bCambodia\b"],
        "Chile": [r"\bChile\b"],
        "China": [r"\bChin(?:a|ese)\b"],
        "Ciudad Juarez": [r"\bCiudad\s*Ju.{0,2}rez\b"],
        "Colombia": [r"\bColombia\b"],
        "Dar es Salaam": [r"\bDar\s*es\s*Salaam\b"],
        "Detroit": [r"\bDetroit\b"],
        "Dhaka": [r"\bDhaka\b"],
        "Dubai": [r"\bDubai\b"],
        "East Asia": [r"\bEast\s*Asia\b"],
        "Egypt": [r"\bEgypt\b"],
        "Ethiopia": [r"\bEthiopia\b"],
        "Gaziantep": [r"\bGaziantep\b"],
        "Germany": [r"\bGerman(?:y|ies)?\b"],
        "Ghana": [r"\bGhana\b"],
        "Guangdong": [r"\bGuangdong\b"],
        "Ho Chi Minh City": [r"\bHo\s*Chi\s*Minh\b"],
        "Hong Kong": [r"\bHong\s*Kong\b"],
        "India": [r"\bIndi(?:a|an)\b"],
        "Indonesia": [r"\bIndonesia\b"],
        "Iran": [r"\bIran\b"],
        "Iraq": [r"\bIraq\b"],
        "Istanbul": [r"\bIstanbul\b"],
        "Japan": [r"\bJapan(?:ese)?\b"],
        "Jordan": [r"\bJordan\b"],
        "Kampala": [r"\bKampala\b"],
        "Kenya": [r"\bKenya\b"],
        "Kigali": [r"\bKigali\b"],
        "Kolkata (Calcutta)": [r"\bKolkata\b", r"\bCalcutta\b"],
        "Lagos": [r"\bLagos\b"],
        "Lebanon": [r"\bLebanon\b"],
        "Libya": [r"\bLibya\b"],
        "London": [r"\bLondon\b"],
        "Malaysia": [r"\bMalaysia\b"],
        "Manila": [r"\bManila\b"],
        "Mexico": [r"\bMexico\b"],
        "Mexico City": [r"\bMexico\s*City\b"],
        "Mezzogiorno (Southern Italy)": [r"\bMezzogiorno\b"],
        "Morocco": [r"\bMorocco\b"],
        "Mumbai": [r"\bMumbai\b", r"\bBombay\b"],
        "Nairobi": [r"\bNairobi\b"],
        "New Delhi": [r"\bNew\s*Delhi\b"],
        "New York": [r"\bNew\s*York\b"],
        "Nigeria": [r"\bNigeria\b"],
        "Pakistan": [r"\bPakistan\b"],
        "Pearl River Delta": [r"\bPearl\s*River\s*Delta\b"],
        "Philippines": [r"\bPhilippines\b"],
        "Qatar": [r"\bQatar\b"],
        "Riyadh": [r"\bRiyadh\b"],
        "Rwanda": [r"\bRwanda\b"],
        "Santiago": [r"\bSantiago\b"],
        "Sao Paulo": [r"\bS.{0,2}o\s*Paulo\b"],
        "Saudi Arabia": [r"\bSaudi\s*Arabia\b"],
        "Seoul": [r"\bSeoul\b"],
        "Shanghai": [r"\bShanghai\b"],
        "Shenzhen": [r"\bShenzhen\b"],
        "Silicon Valley": [r"\bSilicon\s*Valley\b"],
        "Singapore": [r"\bSingapore\b"],
        "Somalia": [r"\bSomalia\b"],
        "South Africa": [r"\bSouth\s*Africa\b"],
        "South Korea": [r"\bSouth\s*Korea\b", r"\bKore(?:a|an)\b"],
        "Sri Lanka": [r"\bSri\s*Lanka\b"],
        "Sub-Saharan Africa": [r"\bSub.{0,1}Saharan\s*Africa\b"],
        "Sudan": [r"\bSudan\b"],
        "Syria": [r"\bSyria\b"],
        "Taipei": [r"\bTaipei\b"],
        "Taiwan": [r"\bTaiwan\b"],
        "Tanzania": [r"\bTanzania\b"],
        "Thailand": [r"\bThailand\b"],
        "Tokyo": [r"\bTokyo\b"],
        "Tunisia": [r"\bTunisia\b"],
        "Turkey (Turkiye)": [r"\bTurk(?:ey|iye|ish)\b"],
        "UAE (United Arab Emirates)": [r"\bUAE\b", r"\bUnited\s*Arab\s*Emirates\b"],
        "Uganda": [r"\bUganda\b"],
        "United Kingdom": [r"\bUnited\s*Kingdom\b", r"\bBritain\b", r"\bBritish\b"],
        "United States": [r"\bUnited\s*States\b", r"\bU\.?S\.?\b"],
        "Vietnam": [r"\bVietnam\b"],
        "Yangtze River Delta": [r"\bYangtze\b"],
        "Yemen": [r"\bYemen\b"],
    }

    for display, pats in places.items():
        if display not in registry:
            registry[display] = pats

    # --- 6. Key concepts (not already in glossary) ---
    concepts = {
        "absolute advantage": [r"\babsolute\s+advantage\b"],
        "brain drain": [r"\bbrain\s+drain\b"],
        "carbon leakage": [r"\bcarbon\s+leakage\b"],
        "catch-up growth": [r"\bcatch.{0,1}up\s+growth\b"],
        "cluster (industrial)": [r"\bindustrial\s+cluster\b", r"\bcluster(?:s|ing)?\b"],
        "congestion costs": [r"\bcongestion\s+cost\b", r"\bcongestion\b"],
        "convergence": [r"\bconvergence\b"],
        "corruption": [r"\bcorruption\b"],
        "creative destruction": [r"\bcreative\s+destruction\b"],
        "decarbonization": [r"\bdecarboni[sz]ation\b"],
        "demographic dividend": [r"\bdemographic\s+dividend\b"],
        "diaspora": [r"\bdiaspora\b"],
        "digital services": [r"\bdigital\s+services\b"],
        "divergence": [r"\bdivergence\b"],
        "dual economy": [r"\bdual\s+economy\b"],
        "economic corridor": [r"\beconomic\s+corridor\b"],
        "economies of scale": [r"\beconomies\s+of\s+scale\b"],
        "employment zone": [r"\bemployment\s+zone\b", r"\bfree\s+zone\b"],
        "exchange rate": [r"\bexchange\s+rate\b"],
        "export processing zone": [r"\bexport\s+processing\s+zone\b"],
        "fiscal transfer": [r"\bfiscal\s+transfer\b"],
        "flying geese model": [r"\bflying\s+geese\b"],
        "fragile state": [r"\bfragile\s+state\b"],
        "green hydrogen": [r"\bgreen\s+hydrogen\b"],
        "human capital": [r"\bhuman\s+capital\b"],
        "import substitution": [r"\bimport\s+substitution\b"],
        "industrial policy": [r"\bindustrial\s+policy\b"],
        "inequality": [r"\binequality\b"],
        "infant industry": [r"\binfant\s+industr\b"],
        "inflation": [r"\binflation\b"],
        "informal economy": [r"\binformal\s+(?:economy|sector|employment)\b"],
        "infrastructure": [r"\binfrastructure\b"],
        "internally displaced persons": [r"\binternally\s+displaced\b", r"\bIDP\b"],
        "just transition": [r"\bjust\s+transition\b"],
        "knowledge economy": [r"\bknowledge\s+economy\b"],
        "labor mobility": [r"\blabor\s+mobility\b", r"\blabour\s+mobility\b"],
        "land use": [r"\bland\s+use\b"],
        "logistics": [r"\blogistics\b"],
        "market access": [r"\bmarket\s+access\b"],
        "migration": [r"\bmigration\b"],
        "monetary union": [r"\bmonetary\s+union\b"],
        "nearshoring": [r"\bnearshoring\b"],
        "night-lights (satellite radiance)": [r"\bnight.{0,1}lights?\b"],
        "offshoring": [r"\boffshoring\b"],
        "oil (petroleum)": [r"\bpetroleum\b", r"\boil\s+(?:price|revenue|export|rent|sector|boom)\b"],
        "outsourcing": [r"\boutsourcing\b"],
        "place-based policy": [r"\bplace.{0,1}based\s+polic\b"],
        "polarization": [r"\bpolari[sz]ation\b"],
        "poverty": [r"\bpoverty\b"],
        "productivity": [r"\bproductivity\b"],
        "refugee": [r"\brefugee\b"],
        "remittances": [r"\bremittance\b"],
        "rent-seeking": [r"\brent.{0,1}seeking\b"],
        "reshoring": [r"\breshoring\b"],
        "sanctions": [r"\bsanctions\b"],
        "services trade": [r"\bservices\s+trade\b"],
        "structural transformation": [r"\bstructural\s+transformation\b"],
        "supply chain": [r"\bsupply\s+chain\b"],
        "tariff": [r"\btariff\b"],
        "technology transfer": [r"\btechnology\s+transfer\b"],
        "trade costs": [r"\btrade\s+cost\b"],
        "trade liberalization": [r"\btrade\s+liberali[sz]ation\b"],
        "transport costs": [r"\btransport\s+cost\b"],
        "urban primacy": [r"\burban\s+primacy\b"],
        "urbanization": [r"\burbaniz\b"],
        "value chain": [r"\bvalue\s+chain\b"],
        "wage premium": [r"\bwage\s+premium\b"],
    }

    for display, pats in concepts.items():
        if display not in registry:
            registry[display] = pats

    return registry


def chapter_sort_key(label: str) -> tuple:
    """Sort key for chapter labels: numeric chapters first, then appendices."""
    if label == "P":
        return (0, 0, "")
    if label == "Bib":
        return (3, 0, "")
    # Appendices: A, B, C
    if label in ("A", "B", "C"):
        return (2, 0, label)
    # Numeric chapters: "1", "3-A", "3-B", "10", etc.
    parts = label.split("-")
    num = int(parts[0])
    suffix = parts[1] if len(parts) > 1 else ""
    return (1, num, suffix)


def search_chapters(registry: dict[str, list[str]]) -> dict[str, list[str]]:
    """Search each chapter for each term and return {display: [chapter_labels]}."""
    # Load all chapter texts
    chapter_texts: list[tuple[str, str]] = []  # (label, text)
    for fname, label in FILES_AND_LABELS:
        fpath = CHAPTERS_DIR / fname
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8")
            chapter_texts.append((label, text))
        else:
            print(f"  WARNING: {fname} not found, skipping")

    # Compile patterns
    compiled: dict[str, list[re.Pattern]] = {}
    for display, patterns in registry.items():
        compiled[display] = [re.compile(p, re.IGNORECASE) for p in patterns]

    # Search
    index: dict[str, set[str]] = defaultdict(set)
    for label, text in chapter_texts:
        for display, pat_list in compiled.items():
            for pat in pat_list:
                if pat.search(text):
                    index[display].add(label)
                    break  # one match per chapter is enough

    # Filter: only keep terms that appear in at least 1 chapter
    # (but not in ALL chapters — those are too generic)
    total_chapters = len(chapter_texts)
    max_chapters = total_chapters - 2  # allow very common terms but not literally everywhere

    result = {}
    for display, labels in index.items():
        if 1 <= len(labels) <= max_chapters:
            sorted_labels = sorted(labels, key=chapter_sort_key)
            result[display] = sorted_labels

    return result


def format_index(index: dict[str, list[str]]) -> str:
    """Format the index as markdown, grouped by first letter."""
    # Sort entries case-insensitively
    # Strip leading special chars for sorting (e.g., beta, sigma)
    def sort_key(display: str) -> str:
        # Remove leading non-alpha chars for sorting
        clean = re.sub(r"^[^a-zA-Z]+", "", display)
        if not clean:
            clean = display
        return clean.lower()

    sorted_entries = sorted(index.keys(), key=sort_key)

    lines = [
        "# Subject Index",
        "",
        "Terms are indexed by chapter number. "
        '"P" = Preface, "A"/"B"/"C" = Appendices A/B/C, "Bib" = Bibliography.',
        "",
    ]

    current_letter = None
    for display in sorted_entries:
        # Determine letter heading
        clean = re.sub(r"^[^a-zA-Z]+", "", display)
        if not clean:
            letter = "#"
        else:
            letter = clean[0].upper()

        if letter != current_letter:
            current_letter = letter
            lines.append(f"## {current_letter}")
            lines.append("")

        chapters_str = ", ".join(index[display])
        lines.append(f"**{display}**, {chapters_str}")
        lines.append("")

    return "\n".join(lines)


def main():
    print("Generating subject index...")

    # Step 1: Extract glossary terms
    glossary_path = CHAPTERS_DIR / "appendix_c_glossary.md"
    glossary_terms = extract_glossary_terms(glossary_path)
    print(f"  Extracted {len(glossary_terms)} glossary terms")

    # Step 2: Build full registry
    registry = build_term_registry(glossary_terms)
    print(f"  Total terms in registry: {len(registry)}")

    # Step 3: Search chapters
    index = search_chapters(registry)
    print(f"  Terms with matches: {len(index)}")

    # Step 4: Format and write
    md = format_index(index)
    OUTPUT.write_text(md, encoding="utf-8")
    print(f"  Written to {OUTPUT}")
    print("Done.")


if __name__ == "__main__":
    main()
