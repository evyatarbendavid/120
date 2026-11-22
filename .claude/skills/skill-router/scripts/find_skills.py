#!/usr/bin/env python3
"""Find the right installed skills for a task, need by need.

usage: find_skills.py "<the request as written>" [--need "english keywords"]... [--max-needs 5] [--top 6] [--json] [-v]

A task is a bundle of needs (a site needs design, a booking backend, hosting, copy). This script
  1. detects the needs in the request from Hebrew/English phrases (references/needs.json), and adds any you pass with
     --need "english keywords" (write your own list of needs, it knows your task best);
  2. for every need shows a team: lead / support / check skills from the catalog that are installed right now, plus
     the best keyword matches found by searching that need alone (so a skill added tomorrow is found too);
  3. adds a whole-request keyword search as a fallback, with tools such as web-operator held back unless asked for.
It scans, at run time, every place Claude Code loads skills and agents from:
  <project>/.claude/skills and .claude/agents, ~/.claude/skills (including skills synced from the claude.ai account),
  ~/.claude/agents and ~/.claude/plugins. There is no list to maintain.
Prints a shortlist; Claude makes the final choice. Measure it: scripts/eval_router.py.
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
    "קידום": "seo marketing", "גוגל": "google seo", "חיפוש": "search seo", "עסק": "business",
    "תוכנית": "plan strategy", "אסטרטגיה": "strategy", "השקה": "launch", "מכירות": "sales",
    "לקוח": "client customer", "לקוחות": "customers clients crm", "וואטסאפ": "whatsapp bot messaging",
    "טלגרם": "telegram bot", "ריאקט": "react", "נקסט": "nextjs next", "פריסה": "deploy deployment vercel",
    "להעלות": "deploy publish upload", "דומיין": "domain dns", "נגישות": "accessibility a11y wcag",
    "מהיר": "performance speed", "ביצועים": "performance", "ai": "ai llm", "בינה": "ai llm",
    # added 2026-11-01: business, money and deals
    "עסקים": "business", "עסקי": "business", "כסף": "money revenue profit", "להרוויח": "profit revenue money",
    "רווח": "profit margin", "רווחים": "profit margin", "הכנסה": "revenue income", "הזדמנות": "opportunity business",
    "הזדמנויות": "opportunity opportunities business", "עסקה": "deal business", "עסקאות": "deals business",
    "ויראלי": "viral trend", "ויראליים": "viral trends", "ויראלית": "viral", "טרנד": "trend viral", "טרנדים": "trends viral",
    "מתחרים": "competitors competitor", "מתחרה": "competitor", "זול": "cheap price sourcing", "בזול": "cheap sourcing price",
    "למכור": "sell sales selling", "מכירה": "sale sales", "לקנות": "buy purchase", "יבוא": "import sourcing",
    "סיטונאי": "wholesale supplier", "דרופשיפ": "dropshipping", "השקעה": "investment", "משא": "negotiation",
    "מומחה": "expert", "שיווקי": "marketing", "פרסומת": "ad ads", "פרסומות": "ads creative",
    "לחפש": "search find", "חיפוש": "search find", "תמצא": "find search", "דרך": "way route",
    "לא": "", "עובד": "working fix", "חסום": "blocked access", "גישה": "access",
    "אינסטגרמי": "instagram", "רשתות": "social media", "סטורי": "story instagram", "קרוסלה": "carousel instagram",
    # added 2026-11-22: systems, booking, local businesses, trading
    "מערכת": "system application platform backend", "מערכות": "systems platform", "ניהול": "management admin dashboard",
    "תיק": "portfolio", "עבודות": "portfolio work", "תורים": "booking appointment scheduling", "תור": "booking appointment",
    "הזמנת": "booking reservation order", "מספרה": "barber salon booking", "קפה": "coffee cafe", "מסעדה": "restaurant",
    "מסעדות": "restaurants", "ליד": "lead prospecting", "לידים": "leads prospecting outreach", "שיחה": "call script outreach",
    "משימות": "tasks todo", "זכרונות": "memories notes", "אירועים": "events calendar", "תזכורות": "reminders notifications",
    "בנייד": "mobile responsive", "נייד": "mobile responsive", "מובייל": "mobile", "מניה": "stock trading", "מניות": "stocks trading",
    "כניסה": "entry trading", "יציאה": "exit trading", "הצעה": "proposal quote", "שירות": "service", "מכשיר": "device",
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
                out += eng.split()  # an empty expansion just drops the word
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


HERE = os.path.dirname(os.path.abspath(__file__))
NEEDS_FILE = os.path.join(HERE, "..", "references", "needs.json")
# Tools and meta skills: shown only when a need asks for them, never from a loose keyword match.
META = {"web-operator", "find-a-way", "skill-router", "web-hunter", "skill-scout", "is-agentic", "configure-ecc", "ecc-guide",
        "skill-stocktake", "skill-comply", "skill-host-compat", "session-start-hook", "update-config", "keybindings-help", "init",
        "ecc-recipes", "token-card", "learn-skill", "academy-guide", "hermes-imports", "rules-distill", "continuous-learning",
        "continuous-learning-v2", "plan-canvas", "dmux-workflows", "nanoclaw-repl", "strategic-compact", "safety-guard",
        "gateguard", "delivery-gate", "plankton-code-quality", "inherit-legacy-style", "ck", "context-budget", "token-budget-advisor"}


NICHE_WORDS = set("llm llms gpu gpus pytorch fine tuning finetune finetuning lora rlhf training inference model models kubernetes k8s rust golang "
                  "go kotlin java spring django laravel rails perl flutter dart swift android hipaa healthcare bgp vlan cisco wireguard pihole "
                  "homelab defi solidity evm quantization vllm embedding embeddings vector rag".split())


def niche_names():
    """Skills listed by name only (niche libraries: ML research, backend languages, healthcare, networking, crypto)."""
    try:
        text = open(os.path.join(HERE, "..", "references", "name-only-skills.md"), encoding="utf-8").read()
    except OSError:
        return set()
    return set(re.findall(r"^- ([^:\s]+):", text, re.M))


def load_needs():
    try:
        return json.load(open(NEEDS_FILE, encoding="utf-8")).get("needs", [])
    except (OSError, ValueError):
        return []


def norm_query(text):
    return " " + re.sub(r"[,.!?;:()\"'׳״/\-_]", " ", text.lower()) + " "


def trigger_score(q, trig):
    """Weight of one trigger in the normalised query, 0 if absent. 'a&b' needs both parts."""
    w = 2
    if isinstance(trig, list):
        trig, w = trig[0], trig[1]
    for part in trig.lower().split("&"):
        part = part.replace("-", " ").replace("'", " ")
        if re.fullmatch(r"[a-z0-9 .+#]+", part):
            if not re.search(r"(?<![a-z0-9])" + re.escape(part.strip()) + r"(s|es|ing)?(?![a-z0-9])", q):
                return 0
        elif part not in q:
            return 0
    return w


BUILD_VERBS = ["תבנה", "לבנות", "בנה", "תיצור", "ליצור", "תכין", "להכין", "תעצב", "לעצב", "בניית", "תפתח", "לפתח", "build", "create",
               "make", "develop", "design"]


def detect_needs(query, catalog, limit):
    """Needs found in the request. A deliverable (site, app, video...) leads; a capability (booking, hosting...)
    comes after the deliverables; an activity (outreach, research, trading...) competes on its score. A build verb
    ("תבנה", "build") gives deliverables a bonus, so 'dashboard for tracking leads' starts with the dashboard."""
    q = norm_query(query)
    verb = any(v in q for v in BUILD_VERBS)
    fired = []
    for order, nd in enumerate(catalog):
        s = sum(trigger_score(q, t) for t in nd.get("triggers", []))
        if s >= 2:
            fired.append((s, order, nd))
    scores = {nd["id"]: s for s, _, nd in fired}
    keep = [(s, o, nd) for s, o, nd in fired
            if not any(scores.get(y, 0) >= s for y in nd.get("yields_to", []) if y != nd["id"])]

    def key(x):
        s, o, nd = x
        kind = nd.get("kind", "activity")
        eff = s + (3 if verb and kind == "deliverable" else 0)
        return (1 if kind == "capability" else 0, -eff, o)

    keep.sort(key=key)
    return keep[:limit]


def short(it, n=110):
    d = " ".join(it["desc"].split())
    return d if len(d) <= n else d[: n - 1] + "…"


def build(query, extra_needs, items, max_needs, top):
    by_name = {}
    for it in items:
        by_name.setdefault(it["name"], it)
    catalog = load_needs()
    fired = detect_needs(query + " " + " ".join(extra_needs), catalog, max_needs)
    used = set()
    shown = {}
    out_needs = []
    skills_only = [i for i in items if i["kind"] == "skill"]
    NICHE = niche_names()
    niche_ok = bool(set(tokens(query + " " + " ".join(extra_needs))) & NICHE_WORDS)

    def more_for(kw, exclude, k, floor, ratio=0.6):
        res = []
        for s, it in rank(skills_only, kw):
            if it["name"] in exclude or it["name"] in used:
                continue
            s2 = s * (0.35 if it["name"] in META else 1.0)
            if (it["name"] in NICHE or os.path.basename(it["path"]) in NICHE) and not niche_ok:
                s2 *= 0.4
            res.append((s2, it))
        res.sort(key=lambda x: -x[0])
        best = res[0][0] if res else 0
        return [(s, it) for s, it in res if s >= max(floor, ratio * best)][:k]

    for s, _, nd in fired:
        entry = {"id": nd["id"], "label": nd["label"], "score": s, "items": [], "more": [], "agents": [], "note": nd.get("note", "")}
        team_names = set()
        for role in ("lead", "support", "check"):
            for name in nd["team"].get(role, []):
                it = by_name.get(name)
                if it and it["kind"] == "skill" and name not in team_names:
                    team_names.add(name)
                    if name in shown:
                        entry.setdefault("shared", []).append({"name": name, "need": shown[name], "role": role})
                        continue
                    shown[name] = len(out_needs) + 1
                    entry["items"].append({"role": role, "name": name, "kind": "skill", "desc": short(it), "path": it["path"]})
        for name in nd.get("builtin", []):
            entry["items"].append({"role": "support", "name": name, "kind": "skill", "desc": "built-in skill from your own skill list (not on disk)", "path": ""})
        for name in nd.get("agents", []):
            it = by_name.get(name)
            if it and it["kind"] == "agent":
                entry["agents"].append({"name": name, "desc": short(it, 90)})
        used |= team_names
        for sc, it in more_for(nd["query"], team_names, 2, 6.0, 0.75):
            entry["more"].append({"name": it["name"], "desc": short(it), "path": it["path"], "score": round(sc, 2)})
            used.add(it["name"])
            shown[it["name"]] = len(out_needs) + 1
        out_needs.append(entry)
    for kw in extra_needs:
        entry = {"id": "ad-hoc", "label": kw, "score": 0, "items": [], "more": [], "agents": [], "note": ""}
        for sc, it in more_for(kw, set(), 5, 3.0):
            entry["more"].append({"name": it["name"], "desc": short(it), "path": it["path"], "score": round(sc, 2)})
            used.add(it["name"])
        if entry["more"]:
            out_needs.append(entry)
    also = []
    for sc, it in more_for(query, set(), top, 5.0 if len(out_needs) < 2 else 8.0, 0.75):
        also.append({"name": it["name"], "desc": short(it), "path": it["path"], "score": round(sc, 2)})
    return out_needs, also


def print_needs(out_needs, also, verbose):
    if not out_needs:
        print("\nNEEDS  none recognised: use the keyword list below, or pass your own with --need \"english keywords\".")
    for i, nd in enumerate(out_needs, 1):
        tag = f"  [{nd['id']}]" if verbose else ""
        print(f"\nNEED {i}: {nd['label']}{tag}")
        for it in nd["items"]:
            fl = needs(it["path"]) if it["path"] else []
            print(f"  {it['role']:8} {it['name']}" + (f"  [{' '.join(fl)}]" if fl else "") + f"  ::  {it['desc']}")
        for it in nd["more"]:
            fl = needs(it["path"])
            print(f"  found    {it['name']}" + (f"  [{' '.join(fl)}]" if fl else "") + f"  ::  {it['desc']}")
        if nd.get("shared"):
            by_need = {}
            for sh in nd["shared"]:
                by_need.setdefault(sh["need"], []).append(sh["name"])
            print("  shared   " + "; ".join(f"{', '.join(v)} (see NEED {k})" for k, v in by_need.items()))
        if nd["agents"]:
            print("  agents   " + ", ".join(a["name"] for a in nd["agents"]))
        if nd["note"]:
            print(f"  note     {nd['note']}")
    if also:
        print("\nALSO matched by the request's own words (weaker; skip unless one fits)")
        for it in also:
            fl = needs(it["path"])
            print(f"  {it['name']}" + (f"  [{' '.join(fl)}]" if fl else "") + f"  ::  {it['desc']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--need", action="append", default=[], help="a need in English keywords (repeat for each need)")
    ap.add_argument("--max-needs", type=int, default=5)
    ap.add_argument("--top", type=int, default=4, help="size of the whole-request fallback list")
    ap.add_argument("--agents", type=int, default=6, help="(kept for compatibility)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    items = collect()
    n_s = sum(1 for i in items if i["kind"] == "skill")
    n_a = len(items) - n_s
    out_needs, also = build(a.query, a.need, items, a.max_needs, a.top)
    if a.json:
        print(json.dumps({"indexed_skills": n_s, "indexed_agents": n_a, "needs": out_needs, "also": also,
                          "skills": also}, ensure_ascii=False, indent=1))
        return
    print(f"INDEXED {n_s} skills, {n_a} agents (scanned now)")
    if a.verbose:
        print(f"QUERY TERMS {' '.join(dict.fromkeys(expand(a.query)))}")
    print_needs(out_needs, also, a.verbose)
    roots_seen = []
    for nd in out_needs:
        for it in nd["items"] + nd["more"]:
            if it.get("path"):
                r = os.path.dirname(it["path"])
                if r not in roots_seen:
                    roots_seen.append(r)
    for it in also:
        r = os.path.dirname(it["path"])
        if r not in roots_seen:
            roots_seen.append(r)
    if roots_seen:
        print("\nSKILL.md of any name above: " + " | ".join(f"{r}/<name>/SKILL.md" for r in roots_seen[:3]))

if __name__ == "__main__":
    main()
