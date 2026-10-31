---
title: Host blocked by the cloud network allowlist (CONNECT 403)
tags: network, proxy, 403, allowlist, blocked, domain
saved: 2026-10-31
---

# Host blocked by the cloud network allowlist (CONNECT 403)

## Problem
A request fails with 'curl: (56) CONNECT tunnel failed, response 403', 'ProxyError ... Tunnel connection failed: 403', or a tool times out/ resets on one site while others work.

## Solution
1) Run: curl -sS "$HTTPS_PROXY/__agentproxy/status" and read recentRelayFailures; kind connect_rejected for the host = the environment allowlist blocks it. Do not retry or route around it. 2) Look for the same data on an allowed host (official API host, oEmbed, GitHub, package registries, an allowed site with the same data) and with WebSearch limited to the blocked site (allowed_domains: ["<site>"]) - its result summaries carry the site's content. WebFetch answers 'getaddrinfo ENOTFOUND' for blocked hosts: same block. 3) If still needed, ask the owner to add the host plus its *.subdomains and CDNs in the cloud environment menu in the session's title bar > Edit > Network access > Allowed domains, leaving 'Allow package managers' ticked (docs: https://code.claude.com/docs/en/cloud-environments#network-access; check current steps with read_documentation topic environment.network). Word it as the owner's action: Claude cannot change the allowlist.

## How to check it worked
After the owner saves, curl -sS -o /dev/null -w '%{http_code}' https://<host>/ returns a normal status instead of 000/403.

## When this does not apply
A 403 that comes from the site itself (curl shows HTTP 403 with a body, not a CONNECT failure): that is the site refusing, see routes.md section 2.
