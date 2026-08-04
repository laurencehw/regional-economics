"""Audit internal chapter/lab/figure references in manuscript markdown.

Reports:
  - Chapter references that do not match known chapter numbers
  - Lab references that do not match known labs
  - Markdown image links whose target files are missing
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
FIGURES = ROOT / "figures"

KNOWN_CHAPTERS = {
    "1", "2", "3", "3-A", "3-B", "3A", "3B", "3a", "3b",
    "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
}
KNOWN_LABS = {str(i) for i in range(1, 8)}

CHAPTER_PATTERNS = [
    re.compile(r"\bChapters?\s+([0-9]{1,2}(?:-[ABab])?)", re.I),
    re.compile(r"\bCh\.\s*([0-9]{1,2}(?:-[ABab])?)", re.I),
]
TREATY_PREFIX = re.compile(
    r"(?:USMCA|NAFTA|CPTPP|RCEP|GATS|Agreement|agreement|'s)\s*$",
    re.I,
)
LAB_PATTERN = re.compile(r"\bLabs?\s+([0-9])\b", re.I)
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def normalize_chapter(raw: str) -> str:
    s = raw.strip().upper().replace(" ", "")
    if s in {"3A", "3-A"}:
        return "3-A"
    if s in {"3B", "3-B"}:
        return "3-B"
    return s


def main() -> int:
    issues: dict[str, list[str]] = defaultdict(list)
    chapter_hits = 0
    lab_hits = 0
    image_hits = 0

    for path in sorted(CHAPTERS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()

        for pat in CHAPTER_PATTERNS:
            for m in pat.finditer(text):
                chapter_hits += 1
                ch = normalize_chapter(m.group(1))
                prefix = text[max(0, m.start() - 24):m.start()]
                if TREATY_PREFIX.search(prefix):
                    continue  # USMCA/NAFTA/etc. treaty chapters, not book chapters
                if ch not in KNOWN_CHAPTERS and ch.replace("-", "") not in {
                    "3A", "3B"
                }:
                    # allow ranges like "9–10" captured poorly; skip en-dash splits
                    if "–" in m.group(0) or ("-" in m.group(0) and ch.count("-") > 1):
                        continue
                    issues["unknown_chapter"].append(f"{rel}: {m.group(0)!r}")

        for m in LAB_PATTERN.finditer(text):
            lab_hits += 1
            if m.group(1) not in KNOWN_LABS:
                issues["unknown_lab"].append(f"{rel}: {m.group(0)!r}")

        for m in IMAGE_PATTERN.finditer(text):
            image_hits += 1
            target = m.group(1).strip()
            if target.startswith("http"):
                continue
            # resolve relative to chapter file
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                issues["missing_image"].append(f"{rel}: {target}")

    out = ROOT / "data" / "processed" / "internal_ref_audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Internal Reference Audit",
        "",
        f"- Chapter-like hits scanned: {chapter_hits}",
        f"- Lab-like hits scanned: {lab_hits}",
        f"- Image links scanned: {image_hits}",
        "",
    ]
    if not issues:
        lines.append("No unknown chapter/lab numbers or missing local images found.")
    else:
        for key, rows in issues.items():
            lines.append(f"## {key} ({len(rows)})")
            lines.append("")
            for row in rows[:200]:
                lines.append(f"- {row}")
            lines.append("")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    for key, rows in issues.items():
        print(f"  {key}: {len(rows)}")
    if not issues:
        print("  clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
