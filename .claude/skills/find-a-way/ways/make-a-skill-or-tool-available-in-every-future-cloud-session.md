---
title: Make a skill or tool available in every future cloud session
tags: skills, persistence, cloud, session, 120, setup
saved: 2026-10-31
---

# Make a skill or tool available in every future cloud session

## Problem
Files written to ~/.claude/skills in a cloud session disappear when the container is rebuilt, so the next session does not have the new skill or knowledge.

## Solution
Commit it to the public repo evyatarbendavid/120 under .claude/skills/<name>/ (or .claude/agents/). The cloud environment's setup script clones 120 and copies its skills and agents into ~/.claude/skills and into every repo under /home/user, so the next session has it. Secret-free content only: 120 is public. For a local Windows/Mac machine, ~/.claude/skills persists by itself. find-a-way's ways.py add does this automatically for saved ways.

## How to check it worked
In a new session: ls ~/.claude/skills/<name> exists.
