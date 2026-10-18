---
name: chief-of-staff
description: Personal AI chief of staff (from mimurchison/claude-chief-of-staff) - morning briefing (gm), inbox triage with drafts in the owner's voice that are never sent without approval (triage), goal-linked task tracking (my-tasks) and a self-updating personal CRM (enrich). Use when the user says "good morning", "brief me", "morning briefing", "triage my inbox", "what needs a reply", "my tasks", "add a task", "update my contacts", "who should I follow up with", "set up my chief of staff", or the Hebrew equivalents (בוקר טוב, תדריך בוקר, תעבור על המיילים, המשימות שלי, אנשי קשר).
license: MIT
metadata:
  upstream: "https://github.com/mimurchison/claude-chief-of-staff"
---

# Chief of Staff

This skill packages the open-source "AI Chief of Staff" by Mike Murchison. Everything the owner
wrote is unmodified in `upstream/`. This file only says how to use it as a skill.

## Files

- `upstream/CLAUDE.md`: the operating-system template. Core principles, the never-send-without-approval
  rule, confidentiality, writing style, triage tiers, contact tiers, operating modes. Placeholders look
  like `{{YOUR_NAME}}`.
- `upstream/commands/gm.md`, `triage.md`, `my-tasks.md`, `enrich.md`: the four workflows.
- `upstream/goals.yaml`, `my-tasks.yaml`, `schedules.yaml`, `contacts/example-contact.md`: data templates.
- `upstream/docs/`: setup, customisation, MCP servers. `upstream/README.md`: the overview.

## Running a workflow

1. Map the request: briefing -> `gm`, inbox -> `triage`, tasks -> `my-tasks`, people -> `enrich`.
2. Read `upstream/commands/<name>.md` and `upstream/CLAUDE.md`, then follow the command step by step.
3. The user's data lives where upstream expects it: `~/.claude/goals.yaml`, `~/.claude/my-tasks.yaml`,
   `~/.claude/schedules.yaml`, `~/.claude/contacts/`, and the profile described below. If a file is
   missing, say so and offer the setup below instead of inventing content.
4. Fill placeholders from the profile. Where the profile has no value, ask once.
5. Channels come from whatever connectors or MCP servers this session actually has (for example
   Gmail, Google Calendar, Slack). Skip a channel that is not connected, silently, as upstream says.
   The `mcp add` commands in `upstream/docs/mcp-servers.md` are illustrative, not real package names.

## Setup (only when the user asks for it)

Do the job of `upstream/install.sh` by hand. **Never run `install.sh`**: it overwrites
`~/.claude/CLAUDE.md` without asking.

1. Ask for name, first name, role, company, work and personal email, company site, timezone, currency,
   and any time limits. Ask in one message.
2. Write the filled-in template to `~/.claude/chief-of-staff-profile.md`. If `~/.claude/CLAUDE.md`
   exists, do not replace it. Offer to add one line, `@chief-of-staff-profile.md`, to its end so the
   profile is loaded in every session, and add it only after a yes.
3. Copy the data templates into `~/.claude/` only where the file does not exist yet.
4. Tell the user that in a cloud session these files disappear when the session ends; the setup is
   meant for their own computer.

## Rules that always hold

- Never send, post, archive or delete anything on any channel without the user's explicit "send" or
  "yes" for that exact item (upstream rule 1.4).
- Draft in the user's language and voice. The owner writes in Hebrew.
- Scheduled runs (cron) are optional and only on the user's own machine, only if they ask.
