#!/usr/bin/env python3
"""Find Claude skills on GitHub, vet them with the repo's scanner, and install the safe ones.

usage:
  skill_hunter.py search "tiktok captions"            GitHub repos that look like skills, by stars
  skill_hunter.py fetch <github url> [--work DIR]     shallow clone (untrusted) and list its skills
  skill_hunter.py vet <skill folder>                  run 120's scan-skills.py and read the license
  skill_hunter.py install <skill folder> --source <github url> [--name NAME] [--update] [--no-120]
                  [--trailer "..."]...

install copies the skill to ~/.claude/skills/<name> (never over an existing one unless --update),
then, when the license allows redistribution and `vet` found nothing HIGH, adds it to the public
repo evyatarbendavid/120 so every new session has it. .git, hooks, plugin files, tests and
node_modules are never copied. Vetting is delegated to 120/scripts/scan-skills.py, the single
source of the safety rules; this file adds none of its own. Standard library (+ git).
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

REPO = "https://github.com/evyatarbendavid/120.git"
UA = "skill-hunter/1.0 (Claude Code skill web-hunter)"
DONT_COPY = {".git", "hooks", "node_modules", "__pycache__", "tests", "test", ".claude-plugin", ".github", ".openclaw"}
DONT_COPY_FILES = {"hooks.json", "settings.json", "settings.local.json", "plugin.json", ".mcp.json"}
# License families that may be redistributed in the public mirror. Copyleft is allowed but flagged.
LICENSES = [
    (r"MIT License|Permission is hereby granted, free of charge", "MIT", True),
    (r"Apache License,? Version 2\.0", "Apache-2.0", True),
    (r"Redistribution and use in source and binary forms|BSD \d-Clause", "BSD", True),
    (r"\bISC License\b", "ISC", True),
    (r"CC0|public domain dedication|released into the public domain", "CC0/Public-Domain", True),
    (r"Creative Commons Attribution(?!.*NonCommercial)", "CC-BY", True),
    (r"Mozilla Public License", "MPL-2.0", True),
    (r"GNU (AFFERO |LESSER )?GENERAL PUBLIC LICENSE", "GPL-family (copyleft: keep license+source)", True),
    (r"NonCommercial|No Derivatives|CC BY-NC|CC BY-ND", "Creative-Commons-restricted (no redistribution)", False),
]


def scanner():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in ("/home/user/120/scripts/scan-skills.py",
                 os.path.join(here, "..", "..", "..", "..", "scripts", "scan-skills.py"),
                 os.path.expanduser("~/.claude/skills/.scan-skills.py")):
        if os.path.isfile(cand):
            return os.path.abspath(cand)
    return None


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def cmd_search(a):
    q = urllib.parse.quote(f'"{a.query}" claude-code skill SKILL.md in:name,description,readme')
    try:
        d = get_json(f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page={a.limit}")
    except Exception as e:
        sys.exit(f"GitHub search failed: {str(e)[:150]} (if it is a blocked host, see find-a-way section 6)")
    items = d.get("items", [])
    if a.json:
        print(json.dumps([{"full_name": r["full_name"], "stars": r["stargazers_count"], "url": r["html_url"],
                           "license": (r.get("license") or {}).get("spdx_id"), "desc": r.get("description")}
                          for r in items], ensure_ascii=False, indent=1))
        return
    print(f"{d.get('total_count', 0)} repos match; top {len(items)} by stars:")
    for r in items:
        lic = (r.get("license") or {}).get("spdx_id") or "no-license"
        print(f"  * {r['full_name']}  ({r['stargazers_count']} stars, {lic})")
        print(f"    {r['html_url']}\n    {(r.get('description') or '').strip()[:150]}")
    print("\nNext: skill_hunter.py fetch <url>, then vet, then install.")


def repo_url(u):
    u = u.strip().rstrip("/")
    m = re.match(r"(?:https?://github\.com/|git@github\.com:)?([^/\s]+)/([^/\s]+?)(?:\.git)?$", u)
    if not m:
        sys.exit("not a github owner/repo or URL")
    return f"https://github.com/{m.group(1)}/{m.group(2)}.git", m.group(2)


def cmd_fetch(a):
    url, name = repo_url(a.url)
    work = a.work or tempfile.mkdtemp(prefix="skill-hunter-")
    dest = os.path.join(work, name)
    shutil.rmtree(dest, ignore_errors=True)
    r = subprocess.run(["git", "clone", "--depth", "1", "-q", url, dest], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        sys.exit("clone failed: " + (r.stderr or r.stdout).strip()[:200])
    skills = []
    for dp, dn, fn in os.walk(dest):
        dn[:] = [d for d in dn if d not in DONT_COPY]
        if "SKILL.md" in fn:
            skills.append(dp)
            dn[:] = []
    print(f"CLONED (untrusted) {dest}\n{len(skills)} skill(s):")
    for s in skills:
        print("  " + s)
    print("\nThis is unvetted downloaded code. Read it, then: skill_hunter.py vet <folder>.")


def read_license(folder):
    # the skill folder, then up to the repo root (a LICENSE often sits at the top of the repo)
    roots, d = [], folder
    for _ in range(4):
        roots.append(d)
        if os.path.isdir(os.path.join(d, ".git")):
            break
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    for root in roots:
        for fn in sorted(os.listdir(root)) if os.path.isdir(root) else []:
            if re.match(r"(?i)(licen[sc]e|copying|unlicense)", fn):
                txt = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read(6000)
                for pat, name, ok in LICENSES:
                    if re.search(pat, txt, re.I):
                        return name, ok, os.path.join(root, fn)
                return "unrecognized", False, os.path.join(root, fn)
    return None, False, None


def cmd_vet(a):
    folder = os.path.abspath(a.folder)
    if not os.path.isfile(os.path.join(folder, "SKILL.md")):
        sys.exit("no SKILL.md in " + folder)
    sc = scanner()
    high = med = 0
    if sc:
        tmp = tempfile.mkdtemp(prefix="vet-")
        root = os.path.join(tmp, "root")
        os.makedirs(root)
        shutil.copytree(folder, os.path.join(root, os.path.basename(folder)))
        out = os.path.join(tmp, "out.json")
        subprocess.run([sys.executable, "-I", sc, out, root], capture_output=True, text=True, timeout=120)
        findings = json.load(open(out)).get("findings", []) if os.path.isfile(out) else []
        for f in findings:
            sev = f.get("sev")
            high += sev == "HIGH"
            med += sev == "MED"
            if sev in ("HIGH", "MED"):
                print(f"  {sev}  {f['cat']}  {f['file']}:{f.get('line', 0)}  {f['snip'][:100]}")
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        print("  (scanner scan-skills.py not found; read the code by hand before installing)")
    lic, ok, path = read_license(folder)
    print(f"\nLICENSE: {lic or 'NONE FOUND'}" + ("" if ok else "  <- not clearly redistributable"))
    has_code = any(os.path.splitext(f)[1] in {".py", ".js", ".ts", ".sh", ".rb", ".go", ".php", ".pl"}
                   for _, _, fs in os.walk(folder) for f in fs)
    verdict = "BLOCK" if high else ("REVIEW" if (med or has_code or not ok) else "OK")
    print(f"VERDICT: {verdict}" + (f" ({high} HIGH, {med} MED)" if (high or med) else ""))
    if verdict == "BLOCK":
        print("Do not install. Report the finding to the owner.")
    elif verdict == "REVIEW":
        print("Read the flagged files / the code yourself; install only if it is clean. "
              "License must allow redistribution before it goes to 120.")
    else:
        print("Looks clean (text, recognized free license). Still skim SKILL.md before installing.")
    sys.exit(2 if verdict == "BLOCK" else 0)


def copy_clean(src, dst):
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst)
    for dp, dn, fn in os.walk(src):
        dn[:] = [d for d in dn if d not in DONT_COPY]
        rel = os.path.relpath(dp, src)
        tgt = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(tgt, exist_ok=True)
        for f in fn:
            if f not in DONT_COPY_FILES:
                shutil.copy2(os.path.join(dp, f), os.path.join(tgt, f))


def cmd_install(a):
    folder = os.path.abspath(a.folder)
    name = a.name or os.path.basename(folder)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
        sys.exit("skill name must be lowercase letters, digits and hyphens")
    dest = os.path.join(os.path.expanduser("~/.claude/skills"), name)
    if os.path.exists(dest) and not a.update:
        sys.exit(f"{name} already in ~/.claude/skills (pass --update to replace)")
    copy_clean(folder, dest)
    lic, ok, lic_path = read_license(folder)
    # carry the license into the skill folder if it lived at the repo root, so attribution travels with it
    if lic_path and not any(re.match(r"(?i)(licen[sc]e|copying|unlicense)", f) for f in os.listdir(dest)):
        shutil.copy2(lic_path, os.path.join(dest, os.path.basename(lic_path)))
    print(f"INSTALLED ~/.claude/skills/{name}")
    if a.no_120:
        print("PUSH_SKIPPED (--no-120)")
        return
    if not ok:
        print(f"PUSH_SKIPPED license is {lic or 'missing'}: not clearly redistributable, so not added to the public 120. "
              "Confirm the license with the owner first.")
        return
    print(push_120(folder, name, a.source, lic, a.trailer or []))


def git(cwd, *args, t=120):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=t)


def push_120(folder, name, source, lic, trailers):
    tmp = tempfile.mkdtemp(prefix="sh-120-")
    r = git(tmp, "clone", "-q", "--depth", "1", REPO, "120", t=300)
    if r.returncode != 0:
        return "PUSH_FAILED clone: " + (r.stderr or r.stdout).strip()[:160]
    clone = os.path.join(tmp, "120")
    rel = os.path.join(".claude", "skills", name)
    if os.path.exists(os.path.join(clone, rel)):
        shutil.rmtree(tmp, ignore_errors=True)
        return f"PUSH_SKIPPED 120 already has {name}"
    dstdir = os.path.join(clone, rel)
    copy_clean(folder, dstdir)
    _, _, lic_path = read_license(folder)
    if lic_path and not any(re.match(r"(?i)(licen[sc]e|copying|unlicense)", f) for f in os.listdir(dstdir)):
        shutil.copy2(lic_path, os.path.join(dstdir, os.path.basename(lic_path)))
    note = os.path.join(clone, "NOTICES.md")
    if os.path.isfile(note):
        with open(note, "a", encoding="utf-8") as fh:
            fh.write(f"| `{name}` | [{source}]({source}), via web-hunter {datetime.date.today()}. "
                     f"Vetted with scan-skills.py (no HIGH findings). | {lic} |\n")
    ident = [] if git(clone, "config", "user.email").stdout.strip() else \
        ["-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com"]
    git(clone, "add", "-A", rel, "NOTICES.md")
    msg = f"web-hunter: add skill {name} from {source} ({lic})"
    if trailers:
        msg += "\n\n" + "\n".join(trailers)
    c = git(clone, *ident, "commit", "-q", "-m", msg)
    if c.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        return "PUSH_SKIPPED nothing to commit"
    for _ in range(4):
        p = git(clone, "push", "-q", "origin", "HEAD:main", t=300)
        if p.returncode == 0:
            shutil.rmtree(tmp, ignore_errors=True)
            return f"PUSHED {name} to evyatarbendavid/120: every new session will have it"
        err = (p.stderr or p.stdout).strip()
        if re.search(r"rejected|fetch first|non-fast-forward", err):
            git(clone, "pull", "-q", "--rebase", "origin", "main", t=300)
            continue
        break
    shutil.rmtree(tmp, ignore_errors=True)
    hint = (" | no push access: in a cloud session call add_repo (owner evyatarbendavid, repo 120, access push) "
            "and run install again") if re.search(r"403|denied|authenticat|could not read Username", err, re.I) else ""
    return f"PUSH_FAILED (installed locally): {err[:180]}{hint}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=10)
    s.add_argument("--json", action="store_true")
    f = sub.add_parser("fetch")
    f.add_argument("url")
    f.add_argument("--work")
    v = sub.add_parser("vet")
    v.add_argument("folder")
    i = sub.add_parser("install")
    i.add_argument("folder")
    i.add_argument("--source", required=True)
    i.add_argument("--name")
    i.add_argument("--update", action="store_true")
    i.add_argument("--no-120", action="store_true")
    i.add_argument("--trailer", action="append")
    a = ap.parse_args()
    {"search": cmd_search, "fetch": cmd_fetch, "vet": cmd_vet, "install": cmd_install}[a.cmd](a)


if __name__ == "__main__":
    main()
