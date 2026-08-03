"""Bidirectional citation audit for manuscript chapters vs bibliography.md.

Extracts Author (Year) / Author et al. (Year) style citations from chapter
markdown and matches them against bibliography author-year keys.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


NAME = r"(?:(?:van|von|de|la|di)\s+)?[A-Z][A-Za-z'’\-]+"
CITE_RE = re.compile(
    r"(?<![A-Za-z0-9])"
    r"("
    rf"{NAME}"  # first author / org token
    r"(?:"
    rf"(?:,\s+{NAME})+"  # Author, Author, Author
    rf"(?:,?\s+and\s+{NAME})?"
    r"|"
    rf"(?:\s+and\s+{NAME})"  # Author and Author
    r"|"
    r"(?:\s+et\s+al\.)"  # Author et al.
    r")?"
    r")"
    r"\s*\((\d{4}[a-z]?)\)"
)

# Also match "Author (Year)" already covered; capture multi-cite "A (Y), B (Y)"
# via finditer.

BIB_YEAR_RE = re.compile(r"\b((?:17|18|19|20)\d{2}[a-z]?)\b")
CHAPTER_TAG_RE = re.compile(r"\[([^\]]+)\]\s*$")


def normalize_author_token(token: str) -> str:
    token = token.strip().replace("’", "'")
    # Drop organizational parentheticals like BCG (Boston...)
    token = re.sub(r"\s*\([^)]*\)\s*", " ", token)
    token = re.sub(r"'s\b", "", token)  # Viner's (1950) -> Viner
    token = re.sub(r"\s+", " ", token)
    return token


FALSE_POSITIVE_AUTHORS = {
    "act",
    "bureau",
    "canada",
    "china",
    "commission",
    "congress",
    "equation",
    "figure",
    "global",
    "group",
    "ira",
    "japan",
    "korea",
    "law",
    "limited",
    "section",
    "site",
    "strategy",
    "table",
    "chapter",
    "lab",
}


def author_keys_from_citation(author_blob: str) -> List[str]:
    """Return candidate bibliography author keys for a citation blob."""
    blob = normalize_author_token(author_blob)
    blob = re.sub(r"\s+et\s+al\.$", "", blob, flags=re.IGNORECASE)
    # Common particle surnames
    blob_l = blob.lower()
    keys: List[str] = []
    if "van wincoop" in blob_l or blob_l == "wincoop":
        keys.append("anderson")  # Anderson and van Wincoop
        keys.append("van wincoop")
        keys.append("wincoop")
    if "santos silva" in blob_l or blob_l.startswith("silva and"):
        keys.append("santos silva")
        keys.append("silva")
    if blob_l.startswith("mayer") or "head and mayer" in blob_l or blob_l.endswith("and mayer"):
        keys.append("head")
        keys.append("mayer")
    if "porta" in blob_l and "shleifer" in blob_l:
        keys.append("la porta")
        keys.append("porta")

    parts = re.split(r",\s*|\s+and\s+", blob)
    first = parts[0].strip()
    words = first.split()
    if len(words) >= 2 and words[0].lower() in {"van", "von", "de", "la", "di"}:
        keys.append(" ".join(words[:2]).lower())
        keys.append(words[-1].lower())
    elif len(words) <= 3 and all(w[:1].isupper() for w in words if w):
        keys.append(first.lower())
        keys.append(words[-1].lower())
    else:
        keys.append(first.lower())
        if words:
            keys.append(words[-1].lower())

    # Also try other surnames in the citation
    for p in parts[1:]:
        pw = p.strip().split()
        if pw:
            keys.append(pw[-1].lower())

    # Deduplicate preserving order
    out: List[str] = []
    for k in keys:
        if k and k not in out:
            out.append(k)
    return out


def author_key_from_citation(author_blob: str) -> str:
    keys = author_keys_from_citation(author_blob)
    return keys[0] if keys else ""


def parse_bibliography(path: Path) -> List[Dict[str, object]]:
    entries: List[Dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("Counts"):
            continue
        if line.startswith("##"):
            continue
        year_matches = BIB_YEAR_RE.findall(line)
        if not year_matches:
            continue
        # First year after author block is usually the publication year
        year = year_matches[0]
        # Author block: text before year
        year_pos = line.find(year)
        author_block = line[:year_pos].rstrip(" .")
        # First author surname
        if "," in author_block:
            first_author = author_block.split(",")[0].strip()
        else:
            first_author = author_block.split()[0].strip() if author_block else ""
        tags = CHAPTER_TAG_RE.search(line)
        chapter_tags = tags.group(1) if tags else ""
        key = first_author.lower()
        author_keys = {key}
        # Index particle / compound surnames appearing before the year.
        for m in re.finditer(
            r"\b((?:van|von|de|la|di)\s+[A-Z][A-Za-z'’\-]+|[A-Z][A-Za-z'’\-]+)\b",
            author_block,
        ):
            author_keys.add(m.group(1).lower())
        if "santos silva" in author_block.lower():
            author_keys.add("santos silva")
            author_keys.add("silva")
        entries.append(
            {
                "line": line,
                "year": year,
                "first_author": first_author,
                "key": f"{key}|{year}",
                "author_key": key,
                "author_keys": sorted(author_keys),
                "chapter_tags": chapter_tags,
            }
        )
    return entries


def extract_citations(text: str) -> List[Tuple[str, str, str]]:
    """Return list of (author_blob, year, raw_match)."""
    found: List[Tuple[str, str, str]] = []
    for m in CITE_RE.finditer(text):
        author = m.group(1).strip()
        year = m.group(2)
        # Skip false positives like Equation (2020) rare; filter short all-caps? keep.
        if author.lower() in {"figure", "table", "chapter", "section", "equation", "lab"}:
            continue
        found.append((author, year, m.group(0)))
    return found


def match_citation(
    author_blob: str,
    year: str,
    bib_by_key: Dict[str, List[Dict[str, object]]],
    bib_by_author_year: Dict[Tuple[str, str], List[Dict[str, object]]],
) -> bool:
    for akey in author_keys_from_citation(author_blob):
        if (akey, year) in bib_by_author_year:
            return True
        for (b_author, b_year), _ in bib_by_author_year.items():
            if b_year == year and (b_author.startswith(akey) or akey.startswith(b_author)):
                return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit chapter citations vs bibliography")
    parser.add_argument("--chapters-dir", default="chapters")
    parser.add_argument("--bibliography", default="chapters/bibliography.md")
    parser.add_argument("--output-json", default="data/processed/citation_audit.json")
    parser.add_argument("--output-md", default="data/processed/citation_audit.md")
    args = parser.parse_args()

    bib_path = Path(args.bibliography)
    chapters_dir = Path(args.chapters_dir)
    entries = parse_bibliography(bib_path)

    bib_by_author_year: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for e in entries:
        for ak in e.get("author_keys", [e["author_key"]]):
            bib_by_author_year[(str(ak), str(e["year"]))].append(e)

    chapter_files = sorted(
        p
        for p in chapters_dir.glob("*.md")
        if p.name != "bibliography.md"
    )

    missing: Dict[str, Set[str]] = defaultdict(set)
    cited_keys: Set[Tuple[str, str]] = set()
    cite_counts: Dict[str, int] = defaultdict(int)

    for ch in chapter_files:
        text = ch.read_text(encoding="utf-8")
        for author, year, raw in extract_citations(text):
            if author_key_from_citation(author) in FALSE_POSITIVE_AUTHORS:
                continue
            cite_counts[raw] += 1
            for akey in author_keys_from_citation(author):
                cited_keys.add((akey, year))
            if not match_citation(author, year, {}, bib_by_author_year):
                missing[ch.name].add(f"{author} ({year})")

    # Orphan bibliography: no chapter file cites matching author-year
    # Use chapter tags as weak evidence of intentional retention
    orphans: List[str] = []
    intentional: List[str] = []
    for e in entries:
        akey = str(e["author_key"])
        year = str(e["year"])
        matched = any(
            a == akey and y == year
            or (y == year and (a.startswith(akey) or akey.startswith(a)))
            for a, y in cited_keys
        )
        if matched:
            continue
        tag = str(e["chapter_tags"])
        line_short = f"{e['first_author']} ({year})"
        if tag:
            intentional.append(f"{line_short} — tagged [{tag}] but no in-text match detected")
        else:
            orphans.append(line_short)

    out = {
        "bibliography_entries": len(entries),
        "unique_intext_citations": len(cite_counts),
        "chapters_with_missing": {k: sorted(v) for k, v in sorted(missing.items())},
        "missing_total": int(sum(len(v) for v in missing.values())),
        "orphan_bibliography_no_tag_match": sorted(set(orphans)),
        "tagged_but_unmatched_in_text": intentional[:200],
        "notes": [
            "Matcher is heuristic (first-author/year). Manual review required for org names and et al.",
            "tagged_but_unmatched may be false negatives if citation style differs.",
        ],
    }

    out_json = Path(args.output_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, indent=2), encoding="utf-8")

    lines = [
        "# Citation Audit",
        "",
        f"- Bibliography entries parsed: {out['bibliography_entries']}",
        f"- Unique in-text citation strings: {out['unique_intext_citations']}",
        f"- Missing author-year pairs (heuristic): {out['missing_total']}",
        "",
        "## Missing from bibliography (by chapter)",
        "",
    ]
    if not missing:
        lines.append("_None detected._")
    else:
        for ch, cites in sorted(missing.items()):
            lines.append(f"### {ch}")
            for c in sorted(cites):
                lines.append(f"- {c}")
            lines.append("")

    lines.extend(
        [
            "## Bibliography entries with no detected in-text match and no chapter tag",
            "",
        ]
    )
    if not orphans:
        lines.append("_None detected._")
    else:
        for o in sorted(set(orphans))[:100]:
            lines.append(f"- {o}")

    out_md = Path(args.output_md)
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    print(f"Missing pairs: {out['missing_total']} across {len(missing)} chapters")
    print(f"Untagged unmatched bib entries: {len(set(orphans))}")


if __name__ == "__main__":
    main()
