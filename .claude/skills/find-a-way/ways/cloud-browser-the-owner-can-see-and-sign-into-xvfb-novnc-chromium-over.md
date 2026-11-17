---
title: Cloud browser the owner can see and sign into (Xvfb + noVNC + Chromium over CDP); Instagram 429s it
tags: browser, novnc, vnc, xvfb, cdp, playwright, sign-in, preview, instagram, 429
saved: 2026-11-17
---

# Cloud browser the owner can see and sign into (Xvfb + noVNC + Chromium over CDP); Instagram 429s it

## Problem
Need a signed-in browser in a cloud session without typing the owner's password: the owner should see the cloud browser and sign in themselves while Claude drives it.

## Solution
apt-get install -y x11vnc novnc websockify; bash ~/.claude/skills/open-social-link/scripts/trust-proxy-ca.sh; Xvfb :99 -screen 0 1280x900x24 &; DISPLAY=:99 /opt/pw-browsers/chromium --no-sandbox --user-data-dir=<DIR> --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --proxy-server="$HTTPS_PROXY" <URL> &; x11vnc -display :99 -localhost -forever -shared -nopw -rfbport 5900 &; websockify --web /usr/share/novnc 127.0.0.1:6080 127.0.0.1:5900 &; report_preview_port 6080 (owner opens /vnc.html in the preview and signs in). Claude drives it with NODE_PATH=$(npm root -g) node + chromium.connectOverCDP('http://127.0.0.1:9222'); use curl --noproxy '*' for localhost checks. The sign-in lives only in that container.

## Tried first (did not work)
Instagram: HTTP ERROR 429 on /accounts/login/ itself from the cloud IP (2026-11-17), so this route does not work for Instagram; use Claude in Chrome on the owner's computer instead (see the way about the owner's own browser).

## When this does not apply
Instagram and other sites that rate-limit datacenter IPs; never retry around a 429.
