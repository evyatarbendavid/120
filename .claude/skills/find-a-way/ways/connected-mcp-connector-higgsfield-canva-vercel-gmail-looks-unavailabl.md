---
title: Connected MCP connector (Higgsfield, Canva, Vercel, Gmail...) looks unavailable or 'no access'
tags: mcp, connector, higgsfield, canva, vercel, gmail, toolsearch, deferred, permissions, auto-mode
saved: 2026-11-17
---

# Connected MCP connector (Higgsfield, Canva, Vercel, Gmail...) looks unavailable or 'no access'

## Problem
A session says it has no access to Higgsfield (or another claude.ai connector) although the connector is connected: its tools are not in the tool list, a call fails with 'unknown tool' or missing schema, or an auto-mode safety check fails on the call.

## Solution
1) Connector tools are DEFERRED: they appear only by name in a system message. Load them first with ToolSearch: query 'select:mcp__Higgsfield__balance' (exact) or '+Higgsfield balance' (keyword), then call. 2) If the system says the server needs authentication, call one of its tools by name or run a ToolSearch with the server name once; that reconnects with the existing sign-in. Only if that is refused, tell the owner to re-authorize it in claude.ai Settings > Connectors. 3) If the call is blocked by an auto-mode check error (server-side), retry; read-only connector tools are pre-allowed in ~/.claude/settings.json permissions.allow by 120/scripts/personal-setup.sh (list: 120/scripts/permissions-allow.json), which skips that check. 4) Never say 'no access' before steps 1-2.

## Tried first (did not work)
Assuming the connector is missing because its tools are not listed at the start of the conversation.

## How to check it worked
mcp__Higgsfield__balance returns the credit balance.

## When this does not apply
A connector that is not connected at all (ListConnectors / SuggestConnectors shows it as available to connect).
