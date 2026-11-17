---
title: Let Claude see and click in the owner's own browser (Instagram signed in) from a cloud session
tags: browser, chrome, extension, instagram, signed-in, computer-use, remote-control, built-in-browser
saved: 2026-11-17
---

# Let Claude see and click in the owner's own browser (Instagram signed in) from a cloud session

## Problem
The owner wants Claude to have 'eyes and a mouse' in their own Chrome (watch reels, browse, draft DMs on their Instagram). A cloud session has no claude-in-chrome or Claude_Browser tools, list_computer_folders is empty, and the cloud Playwright browser is not signed in (Instagram login wall / 429).

## Solution
The browser must run where the owner signed in: (1) Claude in Chrome extension from the Chrome Web Store (publisher Anthropic), owner signs in to Instagram in Chrome, then a Cowork session or a LOCAL Claude Code session ('claude --chrome') uses mcp__claude-in-chrome__* tools (read the chrome-browser skill). (2) Or the Claude desktop app's built-in browser in Cowork / a session linked to the computer running the app (tools mcp__Claude_Browser__* or mcp__remote-devices__Claude_Browser__*; read built-in-browser). In any session, first ToolSearch 'claude-in-chrome' and 'Claude_Browser' / 'enable__mcp' to see if they are already there. Never sign in for the owner, never move cookies to the cloud. Every DM, like, follow, comment or post needs the owner's yes per action; human pace. Details: web-operator/references/instagram.md.

## Tried first (did not work)
Cloud Playwright (not signed in; typing the owner's password is not allowed); list_computer_folders (no Remote Control folders).
