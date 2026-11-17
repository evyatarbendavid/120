---
title: Recover a cloud environment's old allowed-domain list after it was changed
tags: environment, allowlist, domains, network_before, recover, transcript
saved: 2026-11-17
---

# Recover a cloud environment's old allowed-domain list after it was changed

## Problem
The owner asks which domains were allowed in the environment before it was switched to Unrestricted (or edited); get_environment only shows the current state and an unrestricted environment has no list.

## Solution
The update_environment result stores the old state in network_before. Search the session transcripts: python3 -c "import re;s=open('<TRANSCRIPT>.jsonl').read();m=list(re.finditer(r'network_before.{0,40}allowed_hosts.{0,8}\[([^\]]*)\]',s));print(m[-1].group(1))" over ~/.claude/projects/*/*.jsonl, or grep 'allowed_hosts'. Earlier get_environment results also hold the list. A copy from 2026-11-16 is old-allowed-domains.txt in the owner's hub repo.

## Tried first (did not work)
get_environment (shows only the current, unrestricted state)
