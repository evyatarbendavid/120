# my-skills

A mirror of the open-source Claude skills I use (459 of them), plus a setup
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
It also adds a Playwright MCP config (`.mcp.json`) where a repo has none.

## What is here

- `.claude/skills/` — the skills, each unmodified from its source (see `NOTICES.md`).
- `LICENSES/` — the upstream license texts.
- `scripts/personal-setup.sh` — the setup script.

Nothing private is in this repository.
