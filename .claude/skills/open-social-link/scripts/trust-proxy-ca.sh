#!/bin/bash
# Make Chromium (Playwright) trust the Claude Code cloud proxy, which re-signs HTTPS.
# Without it every page in the browser shows a certificate error. Imports only the
# proxy's own CA certificates (subject O = Anthropic) from the bundle the cloud
# environment provides, into the user's browser trust store. Safe to run twice.
BUNDLE="${CA_BUNDLE:-/root/.ccr/ca-bundle.crt}"
[ -f "$BUNDLE" ] || { echo "trust-proxy-ca: no $BUNDLE (not a cloud session?)"; exit 0; }
command -v certutil >/dev/null 2>&1 || apt-get install -y -q --no-install-recommends libnss3-tools >/dev/null 2>&1
command -v certutil >/dev/null 2>&1 || { echo "trust-proxy-ca: certutil unavailable"; exit 0; }
DB="sql:$HOME/.pki/nssdb"; mkdir -p "$HOME/.pki/nssdb"
[ -f "$HOME/.pki/nssdb/cert9.db" ] || certutil -d "$DB" -N --empty-password
T="$(mktemp -d)"; n=0
awk -v d="$T" '/BEGIN CERT/{i++} {print > sprintf("%s/c%03d.pem", d, i)}' "$BUNDLE"
for f in "$T"/c*.pem; do
  subj="$(openssl x509 -in "$f" -noout -subject 2>/dev/null)" || continue
  case "$subj" in *"O = Anthropic"*|*"O=Anthropic"*)
    certutil -d "$DB" -A -t "C,," -n "ccr-proxy-$(basename "$f" .pem)" -i "$f" && n=$((n+1));;
  esac
done
rm -rf "$T"; echo "trust-proxy-ca: imported $n proxy CA certificates into $HOME/.pki/nssdb"
