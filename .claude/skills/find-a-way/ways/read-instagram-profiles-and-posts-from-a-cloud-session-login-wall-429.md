---
title: Read Instagram profiles and posts from a cloud session (login wall / 429)
tags: instagram, 429, login-wall, graph-api, business-discovery, ig_read, web-operator
saved: 2026-11-21
---

# Read Instagram profiles and posts from a cloud session (login wall / 429)

## Problem
A cloud session cannot open instagram.com: profile and embed pages return 200 with only an empty login shell (no meta tags, no post data), the login page returns 429, yt-dlp gets 429 or a login wall. The owner asked that every session be able to read Instagram.

## Solution
Do not scrape or retry. Use the official API: python3 ~/.claude/skills/web-operator/scripts/ig_read.py profile <user> | posts <user> --limit N | mine | whoami (Meta Business Discovery: public data of other Business/Creator accounts; needs the owner's Facebook-Login token saved ONCE with request_credential for host graph.facebook.com, which then serves every session of that environment). For one public reel/post link use open-social-link; for what the owner sees signed in use Claude in Chrome on their computer or ask for a screenshot / screen recording; WebSearch site:instagram.com finds public handles. See web-operator/references/instagram.md.

## Tried first (did not work)
Plain curl of profile and embed pages (200 but login shell, no data); login page (429); parsing og:meta or embedded JSON (none present).

## When this does not apply
Personal or private accounts: Business Discovery cannot read them.
