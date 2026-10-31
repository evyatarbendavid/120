---
title: Playwright Chromium shows certificate errors in the cloud
tags: playwright, chromium, browser, ssl, certificate, proxy
saved: 2026-10-31
---

# Playwright Chromium shows certificate errors in the cloud

## Problem
Pages opened with the Playwright browser fail with ERR_CERT_AUTHORITY_INVALID or a privacy error, because Chromium does not trust the agent proxy's CA.

## Solution
Import the proxy CAs into Chromium's NSS store once per container: bash ~/.claude/skills/open-social-link/scripts/trust-proxy-ca.sh then reopen the page. (It reads /root/.ccr/ca-bundle.crt and adds each CA with certutil to ~/.pki/nssdb.)

## Tried first (did not work)
ignoreHTTPSErrors / --ignore-certificate-errors: works but disables TLS checks; do not use.

## How to check it worked
browser_navigate to https://www.instagram.com/ loads the page instead of an error screen.
