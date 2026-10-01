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

# 1) user level
mkdir -p "$HOME/.claude/skills"
cp -r --update=none "$SKILLS/." "$HOME/.claude/skills/" 2>/dev/null
log "user level: $(ls "$HOME/.claude/skills" | wc -l) entries in ~/.claude/skills"

# 2) project level, in every checked-out repo (this is what cloud sessions load)
CHROME="$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)"
for R in "$REPOS_ROOT"/*/; do
  R="${R%/}"
  [ -d "$R/.git" ] || continue
  EXC="$R/.git/info/exclude"; mkdir -p "$R/.git/info"; touch "$EXC"
  mkdir -p "$R/.claude/skills"
  added=0
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
      cp "$A" "$R/.claude/agents/$n" && echo "/.claude/agents/$n" >> "$EXC"
    done
  fi
  if [ ! -e "$R/.mcp.json" ] && [ -n "$CHROME" ]; then
    printf '{\n  "mcpServers": {\n    "playwright": {\n      "command": "npx",\n      "args": ["@playwright/mcp@latest", "--executable-path=%s", "--no-sandbox"]\n    }\n  }\n}\n' "$CHROME" > "$R/.mcp.json"
    echo "/.mcp.json" >> "$EXC"
    log "$R: wrote .mcp.json (playwright)"
  fi
  log "$R: +$added skills; now $(ls "$R/.claude/skills" | wc -l) in .claude/skills; untracked in git status: $(git -C "$R" status --porcelain 2>/dev/null | wc -l)"
done

# 3) Playwright MCP at user scope too
if command -v claude >/dev/null 2>&1 && [ -n "$CHROME" ]; then
  claude mcp add --scope user playwright -- \
    npx @playwright/mcp@latest --executable-path="$CHROME" --no-sandbox >/dev/null 2>&1 \
    && log "user-scope playwright MCP added" || log "user-scope playwright MCP not added"
fi
log "done"
exit 0
