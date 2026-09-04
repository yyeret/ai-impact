#!/usr/bin/env python3
"""Pre-publication gate for this skills library.

These are public files that get loaded into other people's agents. The failure
modes that matter are not syntax errors — they are a private path, an unreleased
sibling skill, or an uncredited borrowing making it out of the repo. This checks
for those.

Usage: python3 scripts/validate_skills.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

# A machine-specific path or a workspace only Yuval has. Named the way they
# actually appeared here, not as a generic "looks like a path" heuristic.
PRIVATE_PATTERNS = [
    (r"(?<![\w-])[~/]?(?:Users|home)/[a-z][\w.-]*/", "absolute home-directory path"),
    (r"[A-Za-z]:\\\\", "Windows absolute path"),
    (r"Knowledge_Base_\w+", "private knowledge-base file"),
    (r"_Vault\b", "private vault path"),
    (r"\$AGENT_MEMORY_ROOT|\$WORKSPACE_ROOT", "private harness env var"),
    (r"(?<![\w`])\$[a-z][a-z0-9-]{3,}(?![\w`])", "private $skill reference"),
]

REQUIRED_FRONTMATTER = ("name", "description")

# Kept small on purpose: a tag vocabulary that grows per-skill stops being a
# vocabulary. Add to this deliberately, not incidentally.
ALLOWED_TAGS = {"flow-agile", "product-strategy", "ai-transformation"}


def frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if re.match(r"^[a-zA-Z-]+:", line):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def main() -> int:
    errors: list[str] = []
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    known = {p.name for p in skill_dirs}

    if not skill_dirs:
        print("no skills found", file=sys.stderr)
        return 1

    for d in skill_dirs:
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{d.name}: no SKILL.md")
            continue

        text = skill_md.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{d.name}: SKILL.md has no YAML frontmatter")
        else:
            for key in REQUIRED_FRONTMATTER:
                if not fm.get(key):
                    errors.append(f"{d.name}: frontmatter missing '{key}'")
            if fm.get("name") and fm["name"] != d.name:
                errors.append(
                    f"{d.name}: frontmatter name '{fm['name']}' != directory name"
                )

        # Every skill states where it came from. That is the whole promise of
        # the README, and it is the thing that quietly rots.
        if "## Source" not in text:
            errors.append(f"{d.name}: no '## Source' section")

        meta = re.search(r"^metadata:\n((?:  .*\n)+)", text, re.M)
        if not meta:
            errors.append(f"{d.name}: no metadata block")
        else:
            block = meta.group(1)
            if not re.search(r"^  version: ", block, re.M):
                errors.append(f"{d.name}: metadata missing 'version'")
            tag_line = re.search(r"^  tags: (.+)$", block, re.M)
            if not tag_line:
                errors.append(f"{d.name}: metadata missing 'tags'")
            else:
                for tag in (t.strip() for t in tag_line.group(1).split(",")):
                    if tag not in ALLOWED_TAGS:
                        errors.append(f"{d.name}: unknown tag {tag!r}")

        for md in sorted(d.rglob("*.md")) + sorted(d.rglob("*.yaml")):
            body = md.read_text(encoding="utf-8")
            rel = md.relative_to(ROOT)
            for pattern, label in PRIVATE_PATTERNS:
                for hit in re.findall(pattern, body):
                    errors.append(f"{rel}: {label} -> {hit!r}")

            # A skill that points at a sibling this repo does not ship sends
            # the reader to a dead end.
            for ref in re.findall(r"`([a-z][a-z0-9-]{4,})`", body):
                if ref.endswith("-coach") or ref.startswith("sniff-test"):
                    if ref not in known:
                        errors.append(f"{rel}: references unshipped skill '{ref}'")

            # Relative links must resolve on disk.
            for link in re.findall(r"\]\((?!https?:|mailto:|#)([^)]+)\)", body):
                target = (md.parent / link.split("#")[0]).resolve()
                if not target.exists():
                    errors.append(f"{rel}: broken relative link -> {link}")

    for name in ("README.md", "CREDITS.md", "LICENSE", "LICENSE-CODE"):
        if not (ROOT / name).exists():
            errors.append(f"missing {name}")

    for link in re.findall(
        r"\]\((?!https?:|mailto:|#)([^)]+)\)", (ROOT / "README.md").read_text()
    ):
        if not (ROOT / link.split("#")[0]).exists():
            errors.append(f"README.md: broken relative link -> {link}")

    if errors:
        print(f"FAIL — {len(errors)} problem(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"OK — {len(skill_dirs)} skills validated: {', '.join(sorted(known))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
