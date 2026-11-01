#!/bin/bash
# Makes the skills in this repo (and a Playwright MCP config) available in a
# Claude Code cloud session on ANY repo. Paste this one line into the cloud
# environment's "Setup script" (no token, this repo is public):
#
#   git clone --depth 1 -q https://github.com/evyatarbendavid/120.git /tmp/s120 && bash /tmp/s120/scripts/personal-setup.sh; rm -rf /tmp/s120
#
# Cloud sessions load skills from the repo's own .claude/skills (and from the
# claude.ai account), not from ~/.claude/skills. So the skills are copied into
# every checked-out repo and listed in .git/info/exclude: `git status` stays
# clean and nothing is committed by accident. Existing files are never
# overwritten. Everything is logged to /tmp/personal-setup.log. Always exits 0.

LOG=/tmp/personal-setup.log
REPOS_ROOT="${REPOS_ROOT:-/home/user}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log() { echo "personal-setup: $*" | tee -a "$LOG" >&2; }
: > "$LOG"
log "v3 start $(date -u +%FT%TZ) pwd=$PWD home=$HOME user=$(id -un) source=$HERE"

if [ ! -d "$HERE/.claude/skills" ]; then
  log "no .claude/skills next to this script; nothing to install"; exit 0
fi
SKILLS="$HERE/.claude/skills"
AGENTS="$HERE/.claude/agents"
log "source has $(ls "$SKILLS" | wc -l) skills"

# ffmpeg is a convenience for some skills (motion-studio can bring its own).
command -v ffmpeg >/dev/null 2>&1 || \
  apt-get install -y --no-install-recommends ffmpeg >/dev/null 2>&1 || log "ffmpeg not installed"

# yt-dlp: the `watch` skill downloads videos with it.
if ! command -v yt-dlp >/dev/null 2>&1; then
  python3 -m pip install -q yt-dlp >/dev/null 2>&1 \
    || python3 -m pip install -q --break-system-packages yt-dlp >/dev/null 2>&1 \
    || log "yt-dlp not installed"
fi
command -v yt-dlp >/dev/null 2>&1 && log "yt-dlp $(yt-dlp --version 2>&1 | head -1)"

# Social links (open-social-link skill): deno lets yt-dlp read YouTube, curl_cffi lets it
# read TikTok, and the browser must trust the cloud proxy or every page is a certificate error.
pipq() { python3 -m pip install -q "$@" >/dev/null 2>&1 || python3 -m pip install -q --break-system-packages "$@" >/dev/null 2>&1; }
command -v deno >/dev/null 2>&1 || pipq deno || log "deno not installed"
python3 -c "import curl_cffi" >/dev/null 2>&1 || pipq curl_cffi || log "curl_cffi not installed"
[ -f "$SKILLS/open-social-link/scripts/trust-proxy-ca.sh" ] && bash "$SKILLS/open-social-link/scripts/trust-proxy-ca.sh" 2>&1 | while read -r l; do log "$l"; done

# 1) user level
mkdir -p "$HOME/.claude/skills"
cp -r --update=none "$SKILLS/." "$HOME/.claude/skills/" 2>/dev/null
log "user level: $(ls "$HOME/.claude/skills" | wc -l) entries in ~/.claude/skills"

# Skill listing size (approved by the owner on 2026-11-01). By default Claude Code spends 1% of the
# context window on skill descriptions, so with ~580 skills only ~30 show what they do and the rest
# appear as bare names that are never picked automatically. These two settings show every skill with
# up to 250 characters of description (~37k tokens). Merged into ~/.claude/settings.json; every other
# key in that file is kept. Not a hook.
python3 - "$HOME/.claude/settings.json" <<'PYEOF' && log "skill listing: every skill shown with a description (settings.json)"
import json, os, sys
p = sys.argv[1]
try:
    cur = json.load(open(p)) if os.path.exists(p) else {}
except Exception:
    sys.exit(0)  # never rewrite a settings file this script cannot read
cur.setdefault("skillListingBudgetFraction", 0.05)
cur.setdefault("skillListingMaxDescChars", 250)
os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(cur, open(p, "w"), indent=2)
PYEOF

# Standing instructions for every session, in the user-level CLAUDE.md that Claude Code loads
# everywhere. Added once (marked), never overwrites what is already in the file.
MEM="$HOME/.claude/CLAUDE.md"
if ! grep -q "skill-router (from evyatarbendavid/120)" "$MEM" 2>/dev/null; then
  cat >> "$MEM" <<'MEMEOF'

<!-- skill-router (from evyatarbendavid/120) -->
## Before building anything
When the user asks to build, create, make, design, write, edit or produce something non-trivial
(a site, page, app, video, reel, animation, logo, bot, automation, campaign, document, deck, code),
use the `skill-router` skill first: it scans every installed skill and agent and picks the best ones
for the job. Then do the work with them. Skip it for questions and small edits.
Never register a hook in any settings file without the owner's explicit yes.
MEMEOF
  log "added skill-router instructions to ~/.claude/CLAUDE.md"
fi
if ! grep -q "find-a-way (from evyatarbendavid/120)" "$MEM" 2>/dev/null; then
  cat >> "$MEM" <<'MEMEOF'

<!-- find-a-way (from evyatarbendavid/120) -->
## When something fails or looks impossible
Before telling the user something cannot be done (an error, a blocked site, a missing tool or access),
use the `find-a-way` skill: search the saved ways, then try every legitimate route, and save the route
that worked so every session knows it. Never go around the network allowlist, logins, captchas,
TLS checks or permission settings; ask the owner for the one thing only they can do.
MEMEOF
  log "added find-a-way instructions to ~/.claude/CLAUDE.md"
fi

# 2) project level, in every checked-out repo (this is what cloud sessions load)
# Prefer the stable link the image keeps current (/opt/pw-browsers/chromium); fall back to any
# versioned build in either folder layout (chrome-linux or chrome-linux64).
if [ -x /opt/pw-browsers/chromium ]; then CHROME=/opt/pw-browsers/chromium
else CHROME="$(ls -d /opt/pw-browsers/chromium-*/chrome-linux*/chrome 2>/dev/null | sort -V | tail -1)"; fi
for R in "$REPOS_ROOT"/*/; do
  R="${R%/}"
  [ -d "$R/.git" ] || continue
  EXC="$R/.git/info/exclude"; mkdir -p "$R/.git/info"; touch "$EXC"
  mkdir -p "$R/.claude/skills"
  added=0; agents_added=0
  for S in "$SKILLS"/*/; do
    n="$(basename "$S")"
    [ -e "$R/.claude/skills/$n" ] && continue
    cp -r "$S" "$R/.claude/skills/$n" && echo "/.claude/skills/$n/" >> "$EXC" && added=$((added+1))
  done
  if [ -d "$AGENTS" ]; then
    mkdir -p "$R/.claude/agents"
    for A in "$AGENTS"/*.md; do
      [ -f "$A" ] || continue
      n="$(basename "$A")"
      [ -e "$R/.claude/agents/$n" ] && continue
      cp "$A" "$R/.claude/agents/$n" && echo "/.claude/agents/$n" >> "$EXC" && agents_added=$((agents_added+1))
    done
  fi
  if [ ! -e "$R/.mcp.json" ] && [ -n "$CHROME" ]; then
    printf '{\n  "mcpServers": {\n    "playwright": {\n      "command": "npx",\n      "args": ["@playwright/mcp@latest", "--executable-path=%s", "--no-sandbox"]\n    }\n  }\n}\n' "$CHROME" > "$R/.mcp.json"
    echo "/.mcp.json" >> "$EXC"
    log "$R: wrote .mcp.json (playwright)"
  elif [ -f "$R/.mcp.json" ] && [ -n "$CHROME" ]; then
    # An existing .mcp.json is never replaced, but a Playwright browser path that no longer
    # exists (the image moved to a newer Chromium) is swapped for the current one. Only that
    # one argument changes; the rest of the file is kept byte for byte.
    python3 - "$R/.mcp.json" "$CHROME" <<'PYEOF' && log "$R: .mcp.json had a missing browser path; now $CHROME"
import os, re, sys
p, chrome = sys.argv[1], sys.argv[2]
s = open(p).read()
def fix(m):
    return m.group(1) + (m.group(2) if os.access(m.group(2), os.X_OK) else chrome)
new = re.sub(r'(--executable-path=)([^"\s]+)', fix, s)
if new == s: sys.exit(1)
open(p, "w").write(new)
PYEOF
  fi
  log "$R: +$added skills, +$agents_added agents; now $(ls "$R/.claude/skills" | wc -l) in .claude/skills, $(ls "$R/.claude/agents" 2>/dev/null | wc -l) in .claude/agents; untracked in git status: $(git -C "$R" status --porcelain 2>/dev/null | wc -l)"
done

# 3) Playwright MCP at user scope too
if command -v claude >/dev/null 2>&1 && [ -n "$CHROME" ]; then
  claude mcp add --scope user playwright -- \
    npx @playwright/mcp@latest --executable-path="$CHROME" --no-sandbox >/dev/null 2>&1 \
    && log "user-scope playwright MCP added" || log "user-scope playwright MCP not added"
fi
log "done"
exit 0
