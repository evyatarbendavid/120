# my-skills

A mirror of the open-source Claude skills I use (478 of them), plus a setup
script that makes them available in every Claude Code cloud session on any repo.

## How it is used

In the cloud environment's **Setup script** (claude.ai/code, environment settings):

```bash
git clone --depth 1 -q https://github.com/evyatarbendavid/120.git /tmp/s120 && bash /tmp/s120/scripts/personal-setup.sh; rm -rf /tmp/s120
```

Cloud sessions load skills from the checked-out repo's `.claude/skills`, not from
`~/.claude/skills`. The script therefore copies the skills into every checked-out repo,
adds them to `.git/info/exclude` (so `git status` stays clean and nothing is committed by
accident), never overwrites an existing file, and writes a log to `/tmp/personal-setup.log`.
It also adds a Playwright MCP config (`.mcp.json`) where a repo has none, and installs `yt-dlp` (used by the `watch` skill) and `ffmpeg`.

## Standing rule: add only, never remove

Skills are only ever **added** to this repository. Never delete, rename away or replace a skill
that is already here, and never shrink one. Fixes and updates to an existing skill are additive
edits. A skill leaves only if the owner asks for it by name, or if it does something actually harmful (hidden data theft, destructive actions, self-installing hooks); in that case report it to the owner. Disclosed analytics, opt-in API calls and documentation about attacks are not harmful, so those skills stay. The
setup script follows the same rule: it copies, it never overwrites or deletes a skill.

## How things get added

This repository is the single source for what every Claude Code session gets. New skills,
tools and knowledge are added here, vetted first, and then show up in every new session:

- **A skill** (a folder with a `SKILL.md`, from a zip or a GitHub link): checked for a valid
  SKILL.md, for secrets and for a license that allows redistribution (this repo is public),
  for hooks that would run automatically, and for name clashes. Then it goes to
  `.claude/skills/<name>/` and gets a line in `NOTICES.md`.
- **A tool a skill needs** (`pip`, `apt`, `npm` packages): one guarded line in
  `scripts/personal-setup.sh`, logged to `/tmp/personal-setup.log`.
- **An MCP server**: added to the `.mcp.json` template written by the same script.
- **Anything private or not redistributable**: not here. Upload it to the claude.ai account
  (Customize > Skills) instead.

Cloud sessions pick up changes on their next start. Local sessions: copy the new folders
from this repo into `%USERPROFILE%\.claude\skills`, never overwriting existing ones.

## What is here

- `.claude/skills/` — the skills, each unmodified from its source (see `NOTICES.md`).
- `LICENSES/` — the upstream license texts.
- `scripts/personal-setup.sh` — the setup script.

Nothing private is in this repository.

## Checking what is here

`python3 -I scripts/scan-skills.py out.json .claude/skills` runs a static scan (it executes nothing) over
every skill: hook wiring, download-and-run, obfuscation, credential access, exfiltration channels, destructive
commands, prompt-injection phrases, hidden Unicode, secrets, binaries and broken files. Run it on anything new
before it is added, and read every hit; most are documentation about security rather than anything harmful.
