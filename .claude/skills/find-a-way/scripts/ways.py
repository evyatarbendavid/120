#!/usr/bin/env python3
"""The shared memory of find-a-way: routes that worked, kept so every session knows them.

usage:
  ways.py search "keywords or the exact error text"   [--top 5]
  ways.py add --title T --problem P --solution S [--tags "a,b"] [--tried "what failed"]
              [--verify "how to check it worked"] [--not-for "when it does not apply"]
              [--trailer "Co-Authored-By: ..."]... [--no-push]
  ways.py owner "<the owner's instruction>" [--trailer ...]   (add to OWNER.md and push)
  ways.py push <slug> [--trailer ...]                 (retry the 120 push of a way saved locally)
  ways.py list
  ways.py show <slug>

Where ways are kept:
  - ~/.claude/skills/find-a-way/ways/        (this computer; every local session reads it)
  - the skill folder this script runs from    (if different, e.g. a project copy)
  - the public repo evyatarbendavid/120       (cloud containers are rebuilt from it, so a way
                                               pushed there reaches every future session)
`add` refuses text that looks like a secret or personal data, because 120 is public.
`add` never overwrites: a way with the same title gets an "Update" section appended.

For tests: FIND_A_WAY_HOME=<dir> keeps every read and write inside <dir>, and
FIND_A_WAY_NO_PUSH=1 (or --no-push) skips the 120 push.
"""
import argparse
import datetime
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

DEFAULT_REPO = "https://github.com/evyatarbendavid/120.git"
# The only place ways are pushed. An override is accepted only as a local file:// repo, for tests,
# so an environment variable can never redirect saved ways to some other server.
REPO = os.environ.get("FIND_A_WAY_REPO", DEFAULT_REPO)
if REPO != DEFAULT_REPO and not REPO.startswith("file://"):
    sys.exit("FIND_A_WAY_REPO may only be a local file:// repo (for tests)")
SKILL_REL = os.path.join(".claude", "skills", "find-a-way")
REL = os.path.join(SKILL_REL, "ways")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write_dir():
    home = os.environ.get("FIND_A_WAY_HOME")
    if home:
        return os.path.abspath(home)
    return os.path.join(os.path.expanduser("~"), ".claude", "skills", "find-a-way", "ways")


def read_dirs():
    if os.environ.get("FIND_A_WAY_HOME"):
        return [write_dir()]
    dirs = [write_dir(), os.path.join(HERE, "ways"), os.path.join(os.getcwd(), REL)]
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=5).stdout.strip()
        if top:
            dirs.append(os.path.join(top, REL))
    except Exception:
        pass
    out, seen = [], set()
    for d in dirs:
        r = os.path.realpath(d)
        if r not in seen and os.path.isdir(r):
            seen.add(r)
            out.append(r)
    return out


def all_ways():
    found, seen = [], set()
    for d in read_dirs():
        for f in sorted(os.listdir(d)):
            if f.endswith(".md") and f != "INDEX.md" and f not in seen:
                seen.add(f)
                found.append(os.path.join(d, f))
    return found


def parse(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    meta = {}
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("\"'")
        text = text[m.end():]
    meta.setdefault("title", os.path.basename(path)[:-3])
    return meta, text


def tokens(s):
    return [t for t in re.findall(r"[a-z0-9][a-z0-9._+-]*|[֐-׿]+", s.lower()) if len(t) > 1]


def cmd_search(a):
    paths = all_ways()
    if not paths:
        print("NO WAYS SAVED YET (dirs: %s)" % ", ".join(read_dirs() or [write_dir()]))
        return
    docs = []
    for p in paths:
        meta, body = parse(p)
        head = tokens(meta.get("title", "") + " " + meta.get("tags", "").replace(",", " "))
        docs.append((p, meta, body, Counter(head * 3 + tokens(body))))
    q = set(tokens(a.query))
    n, avg = len(docs), sum(sum(d[3].values()) for d in docs) / max(len(docs), 1)
    df = Counter(t for d in docs for t in set(d[3]))
    scored = []
    for p, meta, body, c in docs:
        ln = sum(c.values())
        s = sum(math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5)) * c[t] * 2.2 / (c[t] + 1.2 * (0.25 + 0.75 * ln / avg))
                for t in q if t in c)
        if s > 0:
            scored.append((s, p, meta, body))
    scored.sort(key=lambda x: -x[0])
    print(f"SEARCHED {n} saved ways for: {' '.join(sorted(q))}")
    if not scored:
        print("(no saved way matches: this may be new; if you solve it, save it with `add`)")
    for s, p, meta, body in scored[: a.top]:
        sol = re.search(r"## Solution\s*\n(.*?)(\n## |\Z)", body, re.S)
        print(f"\n{s:5.2f}  {meta['title']}   [{meta.get('tags', '')}]")
        print(f"       {p}")
        if sol:
            print("       " + re.sub(r"\s+", " ", sol.group(1)).strip()[:300])


def cmd_list(a):
    for p in all_ways():
        meta, _ = parse(p)
        print(f"{os.path.basename(p)[:-3]:45s} {meta['title']}  [{meta.get('tags', '')}]")


def safe_slug(slug):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,80}", slug):
        sys.exit("a way's name has only lowercase letters, digits and hyphens (see `ways.py list`)")
    return slug


def cmd_show(a):
    safe_slug(a.slug)
    for p in all_ways():
        if os.path.basename(p)[:-3] == a.slug:
            print(open(p, encoding="utf-8").read())
            return
    sys.exit(f"no way named {a.slug}")


SECRET = [
    (r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}", "a GitHub token"),
    (r"\bsk-[A-Za-z0-9_-]{16,}|\bsk-ant-[A-Za-z0-9_-]{10,}", "an API key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "an AWS key"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}", "a Slack token"),
    (r"\bEAA[A-Za-z0-9]{30,}", "a Meta/Instagram token"),
    (r"\bAIza[0-9A-Za-z_-]{30,}", "a Google key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]{16,}", "a bearer token"),
    (r"(?i)\b(api[_-]?key|access[_-]?token|secret|password|passwd|pwd)\b\s*[:=]\s*['\"]?[^\s'\"<>]{6,}", "a credential assignment"),
    (r"(?<![A-Za-z0-9_/+=-])(?=[A-Za-z0-9_+/=-]*[A-Z])(?=[A-Za-z0-9_+/=-]*[a-z])(?=[A-Za-z0-9_+/=-]*[0-9])[A-Za-z0-9_+/=-]{32,}(?![A-Za-z0-9_/+=-])", "a long random string (looks like a key)"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "an email address"),
    (r"(?<!\d)(\+972[- ]?|0)5\d[- ]?\d{3}[- ]?\d{4}(?!\d)|\+\d{1,3}[- ]?\d{2,4}[- ]?\d{3,4}[- ]?\d{3,4}(?!\d)", "a phone number"),
    (r"https?://[^\s/]*:[^\s/@]+@", "a URL with a password"),
]
# Placeholders a way may legitimately contain.
ALLOWED_EMAILS = ("noreply@anthropic.com", "user@example.com", "you@example.com")


DANGER = [
    (r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|~|\$HOME|\*)(\s|$)", "deletes a whole directory tree"),
    (r"(curl|wget)[^|\n]*\|\s*(sudo\s+)?(ba|z)?sh\b", "pipes a download straight into a shell"),
    (r"(?i)--insecure\b|\bcurl\s+(-\w*k\b)|verify\s*=\s*False|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*0|--no-check-certificates?|ignoreHTTPSErrors|--ignore-certificate-errors", "turns off TLS checks"),
    (r"(?i)\bunset\s+HTTPS?_PROXY\b|--noproxy\s+\*|no_proxy\s*=\s*\*", "bypasses the agent proxy"),
    (r"(?i)\b(tor|torsocks|proxychains|sshuttle|ngrok|openvpn|wireguard|wg-quick)\b", "a tunnel or VPN around the network policy"),
    (r"(?i)\b(hooks?\b.*settings\.json|settings\.json.*\bhooks?)\b", "registers a hook in a settings file"),
    (r"(?i)\bchmod\s+(-R\s+)?777\s+/|\bmkfs\b|\bdd\s+if=.*of=/dev/", "damages the system"),
    (r"(?i)captcha\s*(solver|bypass)|2captcha|anti-?captcha", "gets around a captcha"),
    (r"(?i)base64\s+(-d|--decode)[^\n]*\|\s*(ba|z)?sh|\beval\s*\(\s*(atob|base64)|python3?\s+-c\s+['\"]?exec\(", "decodes and runs hidden code"),
    (r"(?i)https?://(bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly|rb\.gy|pastebin\.com|paste\.ee|hastebin|ghostbin|mega\.nz|mediafire\.com|anonfiles|transfer\.sh)\b", "a link shortener, paste site or file locker"),
    (r"https?://\d{1,3}(\.\d{1,3}){3}(:\d+)?/", "a download from a bare IP address"),
    (r"(?i)(>>?|tee\s+-a?)\s*~?/?[^\s]*(\.claude/(settings[^\s]*\.json|CLAUDE\.md)|\.bashrc|\.zshrc|\.profile|authorized_keys|crontab)", "rewrites Claude's settings, a shell profile, SSH keys or cron"),
]


def danger(text):
    return [f"{what}: {m.group(0)[:40]}" for pat, what in DANGER for m in re.finditer(pat, text)]


def scan(text):
    hits = []
    for pat, what in SECRET:
        for m in re.finditer(pat, text):
            s = m.group(0)
            if what == "an email address" and (s in ALLOWED_EMAILS or s.endswith("@example.com")):
                continue
            hits.append(f"{what}: {s[:12]}...")
    return hits


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return (s or "way-" + datetime.date.today().isoformat())[:70]


def render(a, today):
    tags = ", ".join(t.strip() for t in (a.tags or "").split(",") if t.strip())
    parts = [f"---\ntitle: {a.title}\ntags: {tags}\nsaved: {today}\n---\n", f"# {a.title}\n",
             f"## Problem\n{a.problem.strip()}\n", f"## Solution\n{a.solution.strip()}\n"]
    if a.tried:
        parts.append(f"## Tried first (did not work)\n{a.tried.strip()}\n")
    if a.verify:
        parts.append(f"## How to check it worked\n{a.verify.strip()}\n")
    if a.not_for:
        parts.append(f"## When this does not apply\n{a.not_for.strip()}\n")
    return "\n".join(parts)


def render_update(a, today):
    s = f"\n## Update {today}\n**Problem:** {a.problem.strip()}\n\n**Solution:** {a.solution.strip()}\n"
    if a.tried:
        s += f"\n**Tried first:** {a.tried.strip()}\n"
    if a.verify:
        s += f"\n**Check:** {a.verify.strip()}\n"
    return s


def place(folder, slug, full, update):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, slug + ".md")
    if os.path.exists(path):
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(update)
        return path, "updated"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(full)
    return path, "new"


def write_index(folder):
    rows = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".md") and f != "INDEX.md":
            meta, _ = parse(os.path.join(folder, f))
            rows.append(f"| [{meta['title']}]({f}) | {meta.get('tags', '')} | {meta.get('saved', '')} |")
    with open(os.path.join(folder, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write("# Saved ways\n\nRoutes that worked, saved by the find-a-way skill. Search them with\n"
                 "`python3 ../scripts/ways.py search \"<keywords or error text>\"`.\n\n"
                 "| Way | Tags | Saved |\n|---|---|---|\n" + "\n".join(rows) + "\n")


def git(cwd, *args, timeout=120):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)


def ident():
    """Commit identity: the configured one, or a neutral fallback so a commit never fails for lack of it."""
    if subprocess.run(["git", "config", "user.email"], capture_output=True, text=True).stdout.strip():
        return []
    return ["-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com"]


def sparse_clone():
    """A tiny fresh clone holding only the ways folder, in a temp dir; the user's own clones are never touched."""
    tmp = tempfile.mkdtemp(prefix="find-a-way-120-")
    r = git(tmp, "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse", REPO, "120", timeout=300)
    if r.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        return None, (r.stderr or r.stdout).strip()[:300]
    clone = os.path.join(tmp, "120")
    git(clone, "sparse-checkout", "set", SKILL_REL.replace(os.sep, "/"))
    return clone, ""


def push_to_120(slug, full, update, title, trailers, local_file=None):
    msg_tail = ("\n\n" + "\n".join(trailers)) if trailers else ""
    err = ""
    for attempt in range(4):
        clone, why = sparse_clone()
        if clone is None:
            return f"PUSH_SKIPPED could not clone 120: {why}"
        folder = os.path.join(clone, REL)
        if local_file:
            path, kind = merge_file(folder, slug, local_file)
        else:
            path, kind = place(folder, slug, full, update)
        write_index(folder)
        git(clone, "add", os.path.join(REL, slug + ".md"), os.path.join(REL, "INDEX.md"))
        msg = f"find-a-way: {'add' if kind == 'new' else 'update'} way \"{title}\"" + msg_tail
        c = git(clone, *ident(), "commit", "-q", "-m", msg)
        if c.returncode != 0:
            out = (c.stdout + c.stderr).strip()
            shutil.rmtree(os.path.dirname(clone), ignore_errors=True)
            if "nothing to commit" in out or "nothing added" in out:
                return "PUSH_SKIPPED 120 already has this exact way"
            return "PUSH_FAILED could not commit: " + out[:240]
        p = git(clone, "push", "-q", "origin", "HEAD:main", timeout=300)
        if p.returncode == 0:
            shutil.rmtree(os.path.dirname(clone), ignore_errors=True)
            return f"PUSHED to evyatarbendavid/120 ({kind}): every new session will have this way"
        err = (p.stderr or p.stdout).strip()
        shutil.rmtree(os.path.dirname(clone), ignore_errors=True)
        if not re.search(r"rejected|fetch first|non-fast-forward", err):
            break  # someone pushed in between: loop clones again and re-applies the way
    hint = ""
    if re.search(r"403|denied|permission|authenticat|could not read Username|not allowed", err, re.I):
        hint = (" | this session has no push access to 120: in a cloud session call the add_repo tool "
                f"(owner evyatarbendavid, repo 120, access push), then run: ways.py push {slug}; elsewhere tell the owner")
    return f"PUSH_FAILED (the way is saved locally): {err[:240]}{hint}"


def merge_file(folder, slug, local_file):
    """Bring a local way into the clone without losing anything already in 120."""
    os.makedirs(folder, exist_ok=True)
    dst = os.path.join(folder, slug + ".md")
    local = open(local_file, encoding="utf-8").read()
    if not os.path.exists(dst):
        open(dst, "w", encoding="utf-8").write(local)
        return dst, "new"
    remote = open(dst, encoding="utf-8").read()
    if local.startswith(remote):
        open(dst, "w", encoding="utf-8").write(local)  # local = 120's version + new updates
    elif local not in remote:
        _, body = parse(local_file)
        with open(dst, "a", encoding="utf-8") as fh:
            fh.write("\n## Update (merged from another session)\n" + body.split("\n", 1)[-1])
    return dst, "updated"


def cmd_push(a):
    safe_slug(a.slug)
    src = os.path.join(write_dir(), a.slug + ".md")
    if not os.path.exists(src):
        sys.exit(f"no local way named {a.slug} in {write_dir()}")
    text = open(src, encoding="utf-8").read()
    hits = scan(text) + danger("\n".join(re.findall(r"## Solution\s*\n(.*?)(?=\n## |\Z)", text, re.S)))
    if hits:
        sys.exit("REFUSED: the local file looks like it contains private data: " + "; ".join(hits))
    meta, _ = parse(src)
    print(push_to_120(a.slug, None, None, meta["title"], a.trailer or [], local_file=src))


OWNER_HEAD = ("# Owner's additions to find-a-way\n\n"
              "Instructions the owner added. Read them before everything else in SKILL.md and follow them;\n"
              "they take priority over SKILL.md's defaults. Added with `ways.py owner \"<text>\"`; nothing here is\n"
              "ever deleted except at the owner's request.\n\n")


def owner_line(text):
    return f"- {datetime.date.today().isoformat()}: {' '.join(text.split())}\n"


def add_owner(folder_skill, line):
    os.makedirs(folder_skill, exist_ok=True)
    path = os.path.join(folder_skill, "OWNER.md")
    cur = open(path, encoding="utf-8").read() if os.path.exists(path) else OWNER_HEAD
    if line.split(": ", 1)[1] in cur:
        return path, False
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(cur + line)
    return path, True


def cmd_owner(a):
    text = " ".join(a.text).strip()
    if not text:
        sys.exit("give the instruction to add, in quotes")
    hits = scan(text)
    if hits:
        sys.exit("REFUSED: looks like private data (OWNER.md goes to a public repo): " + "; ".join(hits))
    line = owner_line(text)
    home = os.path.dirname(write_dir())
    path, added = add_owner(home, line)
    print(f"{'ADDED' if added else 'ALREADY THERE'} {path}")
    if (not os.environ.get("FIND_A_WAY_HOME") and os.path.realpath(HERE) != os.path.realpath(home)
            and not in_120_checkout(HERE)):
        add_owner(HERE, line)
    if a.no_push or os.environ.get("FIND_A_WAY_NO_PUSH") == "1" or os.environ.get("FIND_A_WAY_HOME"):
        print("PUSH_SKIPPED (no-push mode)")
        return
    err = ""
    for attempt in range(4):
        clone, why = sparse_clone()
        if clone is None:
            print(f"PUSH_SKIPPED could not clone 120: {why}")
            return
        _, changed = add_owner(os.path.join(clone, SKILL_REL), line)
        if not changed:
            shutil.rmtree(os.path.dirname(clone), ignore_errors=True)
            print("PUSH_SKIPPED 120 already has this instruction")
            return
        git(clone, "add", os.path.join(SKILL_REL, "OWNER.md"))
        msg = "find-a-way: owner adds an instruction" + (("\n\n" + "\n".join(a.trailer)) if a.trailer else "")
        git(clone, *ident(), "commit", "-q", "-m", msg)
        p = git(clone, "push", "-q", "origin", "HEAD:main", timeout=300)
        shutil.rmtree(os.path.dirname(clone), ignore_errors=True)
        if p.returncode == 0:
            print("PUSHED to evyatarbendavid/120: every new session will follow it")
            return
        err = (p.stderr or p.stdout).strip()
        if not re.search(r"rejected|fetch first|non-fast-forward", err):
            break
    print(f"PUSH_FAILED (saved locally): {err[:240]} | in a cloud session call add_repo "
          "(owner evyatarbendavid, repo 120, access push) and run the same command again")


def in_120_checkout(path):
    r = subprocess.run(["git", "-C", path, "remote", "get-url", "origin"], capture_output=True, text=True)
    return "evyatarbendavid/120" in r.stdout


def cmd_add(a):
    today = datetime.date.today().isoformat()
    full = render(a, today)
    hits = scan(full)
    if hits:
        print("REFUSED: this looks like it contains private data, and saved ways go to a PUBLIC repo.")
        for h in hits:
            print("  - " + h)
        print("Rewrite it generically (a placeholder such as <TOKEN> or <EMAIL>, no names) and run add again.")
        sys.exit(2)
    bad = danger(a.solution)
    if bad:
        print("REFUSED: the solution contains a step this skill never saves, because every future session would run it:")
        for h in bad:
            print("  - " + h)
        print("Describe a safe route instead. (Unsafe routes that were tried may be named in --tried.)")
        sys.exit(3)
    slug = slugify(a.title)
    update = render_update(a, today)
    folder = write_dir()
    path, kind = place(folder, slug, full, update)
    write_index(folder)
    print(f"SAVED ({kind}) {path}")
    here = os.path.join(HERE, "ways")
    # A project copy of the skill also gets it; a checkout of 120 itself does not (the push below handles 120,
    # and writing there would leave an uncommitted file in someone's working clone).
    if (not os.environ.get("FIND_A_WAY_HOME") and os.path.realpath(here) != os.path.realpath(folder)
            and os.path.isdir(HERE) and not in_120_checkout(HERE)):
        p2, _ = place(here, slug, full, update)
        write_index(here)
        print(f"SAVED also {p2}")
    if a.no_push or os.environ.get("FIND_A_WAY_NO_PUSH") == "1" or os.environ.get("FIND_A_WAY_HOME"):
        print("PUSH_SKIPPED (no-push mode)")
        return
    if shutil.which("git") is None:
        print("PUSH_SKIPPED git is not installed")
        return
    print(push_to_120(slug, full, update, a.title, a.trailer or []))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--top", type=int, default=5)
    sub.add_parser("list")
    sh = sub.add_parser("show")
    sh.add_argument("slug")
    ow = sub.add_parser("owner")
    ow.add_argument("text", nargs="+")
    ow.add_argument("--trailer", action="append")
    ow.add_argument("--no-push", action="store_true")
    pu = sub.add_parser("push")
    pu.add_argument("slug")
    pu.add_argument("--trailer", action="append")
    ad = sub.add_parser("add")
    ad.add_argument("--title", required=True)
    ad.add_argument("--problem", required=True)
    ad.add_argument("--solution", required=True)
    ad.add_argument("--tags", default="")
    ad.add_argument("--tried", default="")
    ad.add_argument("--verify", default="")
    ad.add_argument("--not-for", dest="not_for", default="")
    ad.add_argument("--trailer", action="append")
    ad.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    {"search": cmd_search, "list": cmd_list, "show": cmd_show, "add": cmd_add, "push": cmd_push, "owner": cmd_owner}[a.cmd](a)


if __name__ == "__main__":
    main()
