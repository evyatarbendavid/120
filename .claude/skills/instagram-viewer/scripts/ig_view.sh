#!/bin/bash
# Runs ig_view.js with the browser trust and Playwright path set up (cloud or local).
D="$(cd "$(dirname "$0")" && pwd)"
for T in "$HOME/.claude/skills/open-social-link/scripts/trust-proxy-ca.sh"; do [ -f "$T" ] && bash "$T" >/dev/null 2>&1; done
export NODE_PATH="$(npm root -g 2>/dev/null):${NODE_PATH:-}"
exec node "$D/ig_view.js" "$@"
