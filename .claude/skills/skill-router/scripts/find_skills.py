#!/usr/bin/env python3
"""Rank every skill and agent available right now against a request.

usage: find_skills.py "keywords or the request itself" [--top 15] [--agents 6] [--json]

Scans, at run time, every place Claude Code loads skills and agents from:
  - <project>/.claude/skills and .claude/agents (the current directory and its git root)
  - ~/.claude/skills (including skills synced from the claude.ai account) and ~/.claude/agents
  - ~/.claude/plugins (skills and agents that come with installed plugins)
so a skill added anywhere is found the next time this runs; there is no list to maintain.
Scores with BM25 over name + description (name matches weigh more) after expanding common
Hebrew words to English. Prints a ranked shortlist; Claude makes the final choice.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter

HEB = {
    "אתר": "website site web landing page frontend", "אתרים": "website site web frontend",
    "דף": "page landing", "נחיתה": "landing page", "עיצוב": "design ui ux visual", "לעצב": "design ui",
    "ממשק": "ui interface ux", "אפליקציה": "app application mobile", "אפליקציית": "app mobile",
    "לוגו": "logo brand identity", "מיתוג": "brand branding identity", "באנר": "banner ad",
    "פוסטר": "poster canvas art", "מצגת": "slides presentation deck pptx", "מצגות": "slides presentation",
    "סרטון": "video", "סרטונים": "video", "וידאו": "video", "ריל": "reel instagram short video hook",
    "רילס": "reels instagram short video", "הוק": "hook reel", "עריכה": "edit editing video",
    "לערוך": "edit editing", "כתוביות": "captions subtitles", "אנימציה": "animation motion",
    "אנימציות": "animation motion", "תלת": "3d three", "מימד": "3d", "מימדי": "3d", "מימדית": "3d",
    "אינסטגרם": "instagram reel post", "טיקטוק": "tiktok short video", "יוטיוב": "youtube video",
    "פייסבוק": "facebook social", "שיווק": "marketing growth", "מודעה": "ad ads creative",
    "מודעות": "ads ad creative", "פרסום": "ads advertising marketing", "קופי": "copywriting copy",
    "מייל": "email", "מיילים": "email sequence", "ניוזלטר": "newsletter email", "חנות": "store ecommerce shop",
    "מוצר": "product", "מוצרים": "products sourcing", "ספק": "supplier sourcing", "ספקים": "suppliers sourcing",
    "דרופשיפינג": "dropshipping sourcing", "מחיר": "pricing price", "תמחור": "pricing",
    "בוט": "bot chatbot agent", "צאטבוט": "chatbot bot", "סוכן": "agent", "סוכנים": "agents",
    "אוטומציה": "automation workflow", "משחק": "game", "משחקים": "games", "תמונה": "image picture",
    "תמונות": "images", "מסמך": "document docx doc", "וורד": "docx word document", "אקסל": "xlsx spreadsheet excel",
    "גיליון": "spreadsheet xlsx", "פידיאף": "pdf", "קוד": "code programming", "באג": "bug debug fix",
    "בדיקות": "testing tests qa", "בדיקה": "test audit review", "אבטחה": "security", "שרת": "server backend api",
    "דשבורד": "dashboard analytics", "נתונים": "data analytics", "גרף": "chart graph dataviz",
    "מחקר": "research", "כתיבה": "writing", "טקסט": "text writing copy", "מאמר": "article blog writing",
    "בלוג": "blog article", "תסריט": "script video", "קריינות": "voiceover narration tts",
    "מוזיקה": "music audio", "סאונד": "audio sound", "פודקאסט": "podcast audio",
    "קידום": "seo marketing", "גוגל": "google seo", "חיפוש": "search seo", "עסק": "business startup",
    "תוכנית": "plan strategy", "אסטרטגיה": "strategy", "השקה": "launch", "מכירות": "sales",
    "לקוח": "client customer", "לקוחות": "customers clients crm", "וואטסאפ": "whatsapp bot messaging",
    "טלגרם": "telegram bot", "ריאקט": "react", "נקסט": "nextjs next", "פריסה": "deploy deployment vercel",
    "להעלות": "deploy publish upload", "דומיין": "domain dns", "נגישות": "accessibility a11y wcag",
    "מהיר": "performance speed", "ביצועים": "performance", "ai": "ai llm", "בינה": "ai llm",
}
STOP = set("the a an and or to of for in on with my me i we you it this that is are be do make build create want need please "
           "של את על עם לי שלי זה זאת אני אתה רוצה צריך תבנה תעשה תכין ליצור לבנות משהו כמו גם וגם או אבל כי".split())


def roots():
    cwd = os.getcwd()
    proj = {cwd}
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=5).stdout.strip()
        if top:
            proj.add(top)
    except Exception:
        pass
    home = os.path.expanduser("~/.claude")
    skill_roots = [os.path.join(p, ".claude", "skills") for p in proj] + [os.path.join(home, "skills")]
    agent_roots = [os.path.join(p, ".claude", "agents") for p in proj] + [os.path.join(home, "agents")]
    return skill_roots, agent_roots, os.path.join(home, "plugins")


def frontmatter(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read(20000)
    except OSError:
        return {}
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():  # small YAML subset: key: value, and folded blocks
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            out[key] = "" if val in (">", ">-", "|", "|-") else val.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            out[key] = (out.get(key, "") + " " + line.strip()).strip()
    return out


def find_skill_files(root, depth=5):
    """SKILL.md files under root; a folder that has a SKILL.md is not searched further (its own subfolders are not skills)."""
    found = []
    if not os.path.isdir(root):
        return found
    base = root.rstrip(os.sep).count(os.sep)
    for dp, dn, fn in os.walk(root, followlinks=True):
        if "SKILL.md" in fn and dp != root:
            found.append(os.path.join(dp, "SKILL.md"))
            dn[:] = []
            continue
        if dp.count(os.sep) - base >= depth:
            dn[:] = []
        dn[:] = [d for d in dn if not d.startswith(".") and d not in ("node_modules", "__pycache__")]
    return found


def collect():
    skill_roots, agent_roots, plugins = roots()
    items, seen = [], set()
    for r in skill_roots:
        for p in find_skill_files(r):
            fm = frontmatter(p)
            name = fm.get("name") or os.path.basename(os.path.dirname(p))
            if name in seen:
                continue
            seen.add(name)
            items.append({"kind": "skill", "name": name, "desc": fm.get("description", ""), "path": os.path.dirname(p)})
    if os.path.isdir(plugins):
        for dp, dn, fn in os.walk(plugins):
            dn[:] = [d for d in dn if not d.startswith(".") and d != "node_modules"]
            if os.path.basename(dp) == "skills":
                for p in find_skill_files(dp, depth=2):
                    fm = frontmatter(p)
                    name = fm.get("name") or os.path.basename(os.path.dirname(p))
                    if name not in seen:
                        seen.add(name)
                        items.append({"kind": "skill", "name": name, "desc": fm.get("description", ""),
                                      "path": os.path.dirname(p), "plugin": True})
            if os.path.basename(dp) == "agents":
                agent_roots.append(dp)
    aseen = set()
    for r in agent_roots:
        if not os.path.isdir(r):
            continue
        for f in sorted(os.listdir(r)):
            if not f.endswith(".md"):
                continue
            fm = frontmatter(os.path.join(r, f))
            name = fm.get("name")
            if not name or name in aseen:
                continue
            aseen.add(name)
            items.append({"kind": "agent", "name": name, "desc": fm.get("description", ""), "path": os.path.join(r, f)})
    return items


NEEDS = [
    (r"api[_ -]?key|access[_ -]?token|\bapi token\b|bearer", "key?"),
    (r"pay-per|paid (service|plan|account)|credits?\b|billing|per (clip|second|minute|request)\b|subscription", "paid?"),
    (r"macos and windows only|on the user's own computer|local session only|windows/mac", "own computer?"),
]


def needs(path):
    try:
        text = open(os.path.join(path, "SKILL.md"), encoding="utf-8", errors="replace").read().lower()
    except OSError:
        return []
    return [tag for pat, tag in NEEDS if re.search(pat, text)]


def tokens(s):
    s = s.lower()
    return [t for t in re.findall(r"[a-z0-9][a-z0-9.+#]*|[֐-׿]+", s) if t not in STOP and len(t) > 1]


def expand(query):
    out = []
    for t in tokens(query):
        out.append(t)
        for heb, eng in HEB.items():
            if t == heb or (len(t) > 3 and t.endswith(heb) and len(heb) > 2) or (len(t) > 3 and t[1:] == heb):
                out += eng.split()
    return out


def rank(items, query):
    q = expand(query)
    if not q:
        return []
    docs = []
    for it in items:
        name_t = tokens(it["name"].replace("-", " "))
        docs.append(Counter(name_t * 3 + tokens(it["desc"])))
    n = len(docs)
    avg = sum(sum(d.values()) for d in docs) / max(n, 1)
    df = Counter(t for d in docs for t in set(d))
    scores = []
    for it, d in zip(items, docs):
        ln = sum(d.values())
        s = 0.0
        for t in set(q):
            if t in d:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                tf = d[t]
                s += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * ln / avg))
        if s > 0:
            scores.append((s, it))
    scores.sort(key=lambda x: -x[0])
    return scores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--agents", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    items = collect()
    ranked = rank(items, a.query)
    skills = [(s, it) for s, it in ranked if it["kind"] == "skill"][: a.top]
    agents = [(s, it) for s, it in ranked if it["kind"] == "agent"][: a.agents]
    n_s = sum(1 for i in items if i["kind"] == "skill")
    n_a = len(items) - n_s
    if a.json:
        print(json.dumps({"indexed_skills": n_s, "indexed_agents": n_a,
                          "skills": [dict(score=round(s, 2), needs=needs(it["path"]), **it) for s, it in skills],
                          "agents": [dict(score=round(s, 2), **it) for s, it in agents]}, ensure_ascii=False, indent=1))
        return
    print(f"INDEXED {n_s} skills, {n_a} agents (scanned now)")
    print(f"QUERY TERMS {' '.join(dict.fromkeys(expand(a.query)))}")
    print("\nSKILLS")
    for s, it in skills:
        flags = needs(it["path"])
        print(f"{s:6.2f}  {it['name']}" + (f"  [{' '.join(flags)}]" if flags else "") + f"  ::  {it['desc'][:170]}")
        print(f"        {it['path']}")
    if agents:
        print("\nAGENTS")
        for s, it in agents:
            print(f"{s:6.2f}  {it['name']}  ::  {it['desc'][:150]}")
    if not skills:
        print("(no match: try other English keywords)")


if __name__ == "__main__":
    main()
