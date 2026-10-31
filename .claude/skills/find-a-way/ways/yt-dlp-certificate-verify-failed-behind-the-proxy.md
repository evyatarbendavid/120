---
title: yt-dlp certificate verify failed behind the proxy
tags: yt-dlp, ssl, certificate, proxy, video, download
saved: 2026-10-31
---

# yt-dlp certificate verify failed behind the proxy

## Problem
yt-dlp fails with 'CERTIFICATE_VERIFY_FAILED' / 'unable to get local issuer certificate' in a cloud session, even on allowed hosts such as github.com.

## Solution
Add --compat-options no-certifi so yt-dlp uses the system CA bundle (which includes the proxy CA) instead of its bundled certifi: yt-dlp --compat-options no-certifi <URL>. open-social-link's open_link.py already does this.

## Tried first (did not work)
Passing --no-check-certificates works but disables TLS checks; do not use it.

## How to check it worked
yt-dlp --compat-options no-certifi -F <URL> lists formats without a certificate error.
