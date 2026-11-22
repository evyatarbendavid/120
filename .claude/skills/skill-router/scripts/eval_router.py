#!/usr/bin/env python3
"""Measure how well find_skills.py picks skills: python3 eval_router.py <dev|test|file.json> [--script path] [-v]
For each request: recall of the `should` skills in the first 8 results, and `must_not` skills shown in the first 5.
Reads only. Needs the skills installed (run it where find_skills.py finds them)."""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("-")]
verbose = "-v" in sys.argv
script = here + "/find_skills.py"
if "--script" in sys.argv:
    script = sys.argv[sys.argv.index("--script") + 1]
    args = [a for a in args if a != script]
which = args[0] if args else "dev"
path = which if which.endswith(".json") else os.path.join(here, "..", "references", "eval", which + ".json")
cases = json.load(open(path))
def norm(n): return n.split(":")[-1]
def flat_leads(d):
    """Leads of every need first, then supports, checks, found, also (how a reader picks one lead per need)."""
    out = []
    for role in ("lead", "support", "check"):
        for nd in d.get("needs", []):
            out += [norm(i["name"]) for i in nd.get("items", []) if i["role"] == role]
    for nd in d.get("needs", []):
        out += [norm(i["name"]) for i in nd.get("more", [])]
    out += [norm(i["name"]) for i in d.get("also", d.get("skills", []))]
    seen = []
    for n in out:
        if n not in seen: seen.append(n)
    return seen
def flat(d):
    out = []
    for nd in d.get("needs", []):
        out += [norm(i["name"]) for i in nd.get("items", [])] + [norm(i["name"]) for i in nd.get("more", [])]
    out += [norm(i["name"]) for i in d.get("also", d.get("skills", []))]
    seen = []
    for n in out:
        if n not in seen: seen.append(n)
    return seen
tot = noise = good = tot2 = 0
for c in cases:
    r = subprocess.run([sys.executable, script, c["q"], "--json"], capture_output=True, text=True)
    d = json.loads(r.stdout)
    f = flat(d)
    top8, top5 = f[:8], f[:5]
    hit = [s for s in c["should"] if s in top8]
    bad = [m for m in c["must_not"] if m in top5]
    rec = len(hit) / min(len(c["should"]), 4)
    rec = min(rec, 1.0)
    f2 = flat_leads(d)[:8]
    tot2 += min(len([x for x in c['should'] if x in f2]) / min(len(c['should']), 4), 1.0)
    tot += rec; noise += len(bad); good += rec >= 0.5
    if verbose or rec < 0.5 or bad:
        print(f"{rec:4.2f} noise={bad}  {c['q'][:60]}\n      top8={top8}\n      missed={[s for s in c['should'] if s not in top8]}")
n = len(cases)
print(f"\n{which}: mean recall@8 {tot/n:.2f} | requests with recall>=0.5: {good}/{n} | wrong skills in top5: {noise} | leads-first reading: {tot2/n:.2f}")
