#!/usr/bin/env python3
"""Write the descriptions of the skills that are listed to Claude by NAME ONLY.

The setup script (120/scripts/personal-setup.sh) lists some niche skills by name only to cut the
per-session prompt. So that Claude still chooses exactly as it would with the full list, this writes
the same text the list would have shown (the SKILL.md description, cut at 250 characters like the
listing) to skill-router/references/name-only-skills.md, grouped by area. ~/.claude/CLAUDE.md tells
Claude to read that file when a request touches one of those areas.

usage: name_only_index.py <skill-listing-tiers.json> <skills dir> [<out file>]
Reads only; writes only the out file. No network.
"""
import json, os, re, sys

MAX = 250  # same as skillListingMaxDescChars


def description(skill_md):
    try:
        text = open(skill_md, encoding="utf-8").read()
    except OSError:
        return ""
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    front = m.group(1)
    try:
        import yaml
        d = yaml.safe_load(front) or {}
        desc = d.get("description", "")
    except Exception:
        dm = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", front, re.M)
        desc = dm.group(1) if dm else ""
    desc = " ".join(str(desc).split()).strip("'\"")
    return desc if len(desc) <= MAX else desc[: MAX - 1] + "…"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    tiers, skills = sys.argv[1], sys.argv[2]
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(here, "references", "name-only-skills.md")
    groups = json.load(open(tiers, encoding="utf-8")).get("groups", {})
    lines = [
        "# Skills listed by name only",
        "",
        "These skills appear in Claude's skill list without a description. Below is the exact text the",
        "list would have shown. When a request touches one of these areas, choose a skill as if these",
        "lines were in the list, then invoke it with the Skill tool as usual.",
        "",
    ]
    n = 0
    for area, names in groups.items():
        lines += [f"## {area}", ""]
        for name in names:
            p = os.path.join(skills, name, "SKILL.md")
            if os.path.exists(p):
                lines.append(f"- {name}: {description(p)}")
                n += 1
        lines.append("")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"name-only index: {n} skills -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
