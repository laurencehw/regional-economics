"""Build consolidated book PDF from chapter markdown files."""
import os
import re
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

REPO = Path(r"G:\My Drive\book drafts\regional economics\regional-economics")
PANDOC = r"C:\Users\lwils\AppData\Local\Pandoc\pandoc.exe"
XELATEX = r"C:\Users\lwils\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"
OUTFILE = REPO / "book_review_draft.pdf"
HEADER_TEX = REPO / "header.tex"

# Ordered chapter list
CHAPTERS = [
    "chapters/preface_pathways.md",
    "chapters/ch01_micro_foundations_of_space.md",
    "chapters/ch02_evolutionary_and_institutional_frameworks.md",
    "chapters/ch03a_spatial_econometrics.md",
    "chapters/ch03b_trade_measurement_gravity.md",
    "chapters/ch04_the_north_american_core.md",
    "chapters/ch05_latin_america_middle_income_trap.md",
    "chapters/ch06_flying_geese_and_tech_ascendancy.md",
    "chapters/ch07_china_divergence_asean_fragmentation.md",
    "chapters/ch08_india_geography_of_it_services.md",
    "chapters/ch09_single_market_convergence.md",
    "chapters/ch10_north_south_divide_disintegration.md",
    "chapters/ch11_post_carbon_transition_sovereign_wealth.md",
    "chapters/ch12_fragile_states_conflict_economics.md",
    "chapters/ch13_urbanization_without_industrialization.md",
    "chapters/ch14_afcfta_functional_corridors.md",
    "chapters/ch15_climate_stranded_regions_future_map.md",
    "chapters/ch16_future_of_global_regionalism.md",
    "chapters/appendix_a_mathematical_foundations.md",
    "chapters/appendix_b_data_software_guide.md",
    "chapters/appendix_c_glossary.md",
    "chapters/bibliography.md",
    "chapters/subject_index.md",
]

# Map of hint styles to tcolorbox environment names
HINT_STYLES = {
    "info": "infobox",
    "warning": "warningbox",
    "success": "successbox",
}


def fix_text_underscores(text: str) -> str:
    r"""Escape underscores inside \text{...} for LaTeX compatibility."""
    def escape_text_block(m):
        inner = m.group(1).replace("_", r"\_")
        return r"\text{" + inner + "}"
    return re.sub(r"\\text\{([^}]+)\}", escape_text_block, text)


def fix_image_paths(text: str) -> str:
    """Fix ../figures/ paths to figures/ (since we run from repo root)."""
    return text.replace("../figures/", "figures/")


def fix_inline_math(text: str) -> str:
    """Convert GitBook inline $$...$$ to Pandoc inline $...$ math.

    GitBook uses $$ for both display and inline math. Pandoc treats $$
    as display math. We convert inline uses ($$...$$ within a line of
    prose, not on their own line) to single-dollar $...$ delimiters.
    """
    lines = text.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # Skip lines that are display math openers/closers (just "$$" alone)
        if stripped == "$$":
            result.append(line)
            i += 1
            continue
        # Skip raw LaTeX blocks
        if stripped.startswith("```"):
            result.append(line)
            i += 1
            continue
        # For lines with content: convert inline $$...$$ to $...$
        # Match $$...$$ that appears within prose (not standalone)
        if "$$" in line and stripped != "$$":
            # Replace pairs of $$ with $ for inline math
            # But only if the line has text around the math
            line = re.sub(r'\$\$([^$]+?)\$\$', r'$\1$', line)
        result.append(line)
        i += 1
    return "\n".join(result)


def strip_manual_section_numbers(text: str) -> str:
    """Strip manual 3A.X / 3B.X prefixes from section headings in Ch 3-A/3-B.

    These clash with Pandoc's --number-sections, producing double numbers
    like '3.2 3A.1 The Spatial Weight Matrix'.
    """
    # Match ## 3A.1, ## 3A.2, ..., ## 3B.1, ## 3B.2, etc.
    text = re.sub(r'^(##\s+)3[AB]\.\d+\s+', r'\1', text, flags=re.MULTILINE)
    return text


def convert_hint_boxes(text: str) -> str:
    """Convert GitBook {% hint style="..." %} blocks to raw LaTeX tcolorbox environments."""
    # Process line by line, tracking which box type is open.
    result = []
    lines = text.split("\n")
    open_env = None

    for line in lines:
        # Check for opening hint tag
        m_open = re.match(r'\s*\{%\s*hint\s+style="(\w+)"\s*%\}', line)
        if m_open:
            style = m_open.group(1)
            env_name = HINT_STYLES.get(style, "infobox")
            open_env = env_name
            # Insert raw LaTeX block markers for Pandoc
            result.append("")
            result.append("```{=latex}")
            result.append("\\begin{" + env_name + "}")
            result.append("```")
            result.append("")
            continue

        # Check for closing hint tag
        m_close = re.match(r'\s*\{%\s*endhint\s*%\}', line)
        if m_close:
            env_name = open_env if open_env else "infobox"
            result.append("")
            result.append("```{=latex}")
            result.append("\\end{" + env_name + "}")
            result.append("```")
            result.append("")
            open_env = None
            continue

        result.append(line)

    return "\n".join(result)


def fix_preface_numbering(text: str) -> str:
    """Convert preface heading to unnumbered chapter so it doesn't consume Ch. 1's number."""
    # Use simple string replacement to avoid regex backslash issues
    old_heading = "# Pathways Through This Book"
    new_heading = (
        "```{=latex}\n"
        "\\chapter*{Pathways Through This Book}\n"
        "\\addcontentsline{toc}{chapter}{Pathways Through This Book}\n"
        "```"
    )
    return text.replace(old_heading, new_heading, 1)


def preprocess(src: Path, is_preface: bool = False) -> str:
    """Read and preprocess a chapter file."""
    raw = src.read_text(encoding="utf-8")
    raw = fix_image_paths(raw)
    raw = fix_text_underscores(raw)
    raw = fix_inline_math(raw)
    raw = strip_manual_section_numbers(raw)
    raw = convert_hint_boxes(raw)
    if is_preface:
        raw = fix_preface_numbering(raw)
    return raw


def main():
    # Create temp dir with preprocessed files
    tmpdir = Path(tempfile.mkdtemp(prefix="book_pdf_"))
    print(f"Temp dir: {tmpdir}")

    # Copy figures directory
    fig_src = REPO / "figures"
    fig_dst = tmpdir / "figures"
    if fig_src.exists():
        shutil.copytree(fig_src, fig_dst,
                       ignore=shutil.ignore_patterns("*.py", "__pycache__"))
        print(f"Copied {len(list(fig_dst.glob('*.png')))} figure PNGs")

    # Copy header.tex into temp dir
    if HEADER_TEX.exists():
        shutil.copy2(HEADER_TEX, tmpdir / "header.tex")
        print("Copied header.tex")
    else:
        print("WARNING: header.tex not found — hint boxes and font fixes will be missing")

    # Preprocess chapters
    processed_files = []
    for ch in CHAPTERS:
        src = REPO / ch
        if not src.exists():
            print(f"WARNING: {ch} not found, skipping")
            continue
        is_preface = "preface" in Path(ch).name
        content = preprocess(src, is_preface=is_preface)
        dst = tmpdir / Path(ch).name
        dst.write_text(content, encoding="utf-8")
        processed_files.append(str(dst))

    print(f"Preprocessed {len(processed_files)} files")
    print("Running Pandoc (this may take a few minutes)...")

    cmd = [
        PANDOC,
        *processed_files,
        "-o", str(OUTFILE),
        f"--pdf-engine={XELATEX}",
        "--number-sections",
        "--toc",
        "--toc-depth=2",
        "-H", str(tmpdir / "header.tex"),
        "-V", "documentclass=report",
        "-V", "geometry:margin=1in",
        "-V", "fontsize=11pt",
        "-V", "linkcolor=blue",
        "-V", "urlcolor=blue",
        "-V", "toccolor=black",
        "-V", "monofont=Consolas",
        "-V", "title=The New Regional Economics",
        "-V", "subtitle=Spatial Dynamics, Institutions, and Applied Methods",
        "-V", "author=Laurence Wilse-Samson",
        "-V", "date=Review Draft — March 2026",
        "--top-level-division=chapter",
        f"--resource-path={tmpdir}{os.pathsep}{tmpdir / 'figures'}",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(tmpdir))

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        # Print warnings but filter noise
        for line in result.stderr.splitlines():
            print(line)

    if result.returncode == 0:
        size_mb = OUTFILE.stat().st_size / (1024 * 1024)
        print(f"\nSUCCESS: {OUTFILE.name} ({size_mb:.1f} MB)")
    else:
        print(f"\nFAILED (exit code {result.returncode})")
        sys.exit(1)

    # Clean up
    shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
