---
title: Read Meta Ad Library (any country) from a cloud session when the Playwright MCP browser will not launch
tags: business, competitors, meta, facebook, ad-library, playwright, chromium, cloud
saved: 2026-11-01
---

# Read Meta Ad Library (any country) from a cloud session when the Playwright MCP browser will not launch

## Problem
mcp__playwright__browser_navigate fails: 'executable doesn't exist at /opt/pw-browsers/chromium-1194/chrome-linux/chrome' (the MCP expects an older Chromium build than the one installed). Competitor research needs facebook.com/ads/library, which is JavaScript-only.

## Solution
1) bash ~/.claude/skills/open-social-link/scripts/trust-proxy-ca.sh. 2) Use the global node playwright with the installed build: chromium.launch({executablePath:'/opt/pw-browsers/chromium' (a stable link to the installed build), args:['--no-sandbox']}), run with NODE_PATH=$(npm root -g). 3) goto https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IL&q=<urlencoded keyword>&search_type=keyword_unordered&media_type=all, wait ~9s, scroll 3-4 times, read document.body.innerText and split on the 'Library ID' label (Hebrew UI: 'מזהה ספרייה:'). Each block has the start date ('התחילה לפעול ב-'), the advertiser (line before 'ממומן'/'Sponsored'), the ad text and the landing domain. No login needed; read only.

## Tried first (did not work)
Playwright MCP (wrong chromium build path); WebSearch (does not index Ad Library); curl (page needs JS)

## How to check it worked
The result count line ('כ-16 תוצאות' / 'about 16 results') and advertiser names print for a common keyword

## Note
The setup script now points the Playwright MCP at /opt/pw-browsers/chromium too (fixed 2026-11-01), so mcp__playwright__* should launch in new sessions; this route stays as the fallback.

## When this does not apply
Ad spend or reach numbers (only shown for political/EU ads); logged-in filters
