#!/usr/bin/env python3
"""Find and download images and audio that are legal to reuse, and record the credit for each.

usage:
  free_media.py search "coffee cup" [--type image|audio] [--source openverse|commons|nasa|all]
                [--use commercial|modify|any] [--limit 8] [--json]
  free_media.py get <url> --out DIR --title T --creator C --license L --license-url U --source-url S

Licenses that come back are filtered by --use:
  commercial  CC0, Public Domain Mark, CC BY, CC BY-SA (no NC)      <- default
  modify      as commercial, and no ND (you may edit, crop, remix)
  any         also NC / ND (personal or non-commercial use only)
`get` saves the file and appends a line to DIR/CREDITS.md and DIR/credits.json, so the
attribution the license requires is never lost. Standard library only; network: the
public APIs of Openverse, Wikimedia Commons and NASA, and the file host of each result.
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

UA = "free-media-finder/1.0 (Claude Code skill web-hunter; https://github.com/evyatarbendavid/120)"
OK_COMMERCIAL = {"cc0", "pdm", "by", "by-sa", "public domain"}
NO_MODIFY = {"by-nd", "by-nc-nd"}


def get_json(url, tries=2):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception as e:  # 5xx from a busy API, or a refused host
            last = e
    raise last


def allowed(lic, use):
    lic = (lic or "").lower()
    if use == "any":
        return True
    if lic not in OK_COMMERCIAL:
        return False
    return not (use == "modify" and lic in NO_MODIFY)


def openverse(q, kind, use, limit):
    lt = {"commercial": "commercial", "modify": "commercial,modification", "any": ""}[use]
    url = f"https://api.openverse.org/v1/{'images' if kind == 'image' else 'audio'}/?q={urllib.parse.quote(q)}&page_size={limit}"
    if lt:
        url += "&license_type=" + lt
    out = []
    for r in get_json(url).get("results", []):
        out.append({"source": "openverse/" + (r.get("source") or ""), "title": r.get("title") or "",
                    "creator": r.get("creator") or "unknown", "license": (r.get("license") or "").lower(),
                    "license_version": r.get("license_version") or "", "license_url": r.get("license_url") or "",
                    "url": r.get("url") or "", "source_url": r.get("foreign_landing_url") or "",
                    "size": f"{r.get('width')}x{r.get('height')}" if kind == "image" else r.get("duration")})
    return out


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def commons(q, kind, use, limit):
    if kind != "image":
        return []
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6"
           f"&gsrsearch={urllib.parse.quote(q + ' filetype:bitmap')}&gsrlimit={limit}&prop=imageinfo"
           "&iiprop=url|size|extmetadata&iiurlwidth=1600")
    out = []
    for p in (get_json(url).get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        short = (md.get("LicenseShortName", {}).get("value") or "").lower()
        lic = ("cc0" if "cc0" in short else "pdm" if "public domain" in short else
               re.sub(r"^cc[ -]", "", short).split()[0] if short.startswith("cc") else short)
        out.append({"source": "wikimedia-commons", "title": p.get("title", "").replace("File:", ""),
                    "creator": strip(md.get("Artist", {}).get("value")) or "unknown", "license": lic,
                    "license_version": "", "license_url": md.get("LicenseUrl", {}).get("value", ""),
                    "url": (ii.get("thumburl") or ii.get("url") or "").split("?")[0],
                    "source_url": ii.get("descriptionurl", ""), "size": f"{ii.get('width')}x{ii.get('height')}"})
    return out


def nasa(q, kind, use, limit):
    if kind != "image":
        return []
    d = get_json(f"https://images-api.nasa.gov/search?q={urllib.parse.quote(q)}&media_type=image&page_size={limit}")
    out = []
    for it in d.get("collection", {}).get("items", [])[:limit]:
        data = (it.get("data") or [{}])[0]
        link = next((l.get("href") for l in it.get("links", []) if l.get("rel") == "preview"), "")
        nid = data.get("nasa_id", "")
        out.append({"source": "nasa", "title": data.get("title", ""), "creator": data.get("photographer")
                    or data.get("center") or "NASA", "license": "pdm", "license_version": "",
                    "license_url": "https://www.nasa.gov/nasa-brand-center/images-and-media/",
                    "url": link.replace("~thumb", "~medium"), "source_url": f"https://images.nasa.gov/details/{nid}",
                    "size": "", "note": "NASA media is generally not copyrighted; do not imply NASA endorses you, and do not use the NASA logo."})
    return out


def cmd_search(a):
    srcs = ["openverse", "commons", "nasa"] if a.source == "all" else [a.source]
    found, errors = [], []
    for s in srcs:
        try:
            found += [r for r in {"openverse": openverse, "commons": commons, "nasa": nasa}[s](a.query, a.type, a.use, a.limit)
                      if allowed(r["license"], a.use)]
        except Exception as e:
            errors.append(f"{s}: {str(e)[:120]}")
    if a.json:
        print(json.dumps({"results": found, "errors": errors}, ensure_ascii=False, indent=1))
        return
    for i, r in enumerate(found, 1):
        print(f"{i:2}. [{r['license'].upper()}{(' ' + r['license_version']) if r['license_version'] else ''}] "
              f"{r['title'][:70]}  by {r['creator'][:40]}  ({r['source']}, {r['size']})")
        print(f"    file: {r['url']}\n    page: {r['source_url']}")
    for e in errors:
        hint = ("a blocked host: see find-a-way section 6" if "403" in e or "Tunnel" in e
                else "rate limited: wait a minute and retry" if "429" in e else "try again or another --source")
        print(f"ERROR {e}  ({hint})")
    if not found:
        print("(nothing with a license that fits --use; try other words, --source all, or --use any for personal use)")


def cmd_get(a):
    os.makedirs(a.out, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", os.path.basename(urllib.parse.urlparse(a.url).path))[:90] or "file"
    path = os.path.join(a.out, name)
    req = urllib.request.Request(a.url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as fh:
        fh.write(r.read())
    lic = a.license.upper()
    credit = (f"\"{a.title}\" by {a.creator}, {lic}" + (f" ({a.license_url})" if a.license_url else "")
              + f", from {a.source_url}")
    with open(os.path.join(a.out, "CREDITS.md"), "a", encoding="utf-8") as fh:
        fh.write(f"- `{name}`: {credit}\n")
    cj = os.path.join(a.out, "credits.json")
    items = json.load(open(cj, encoding="utf-8")) if os.path.exists(cj) else []
    items.append({"file": name, "title": a.title, "creator": a.creator, "license": a.license,
                  "license_url": a.license_url, "source_url": a.source_url, "file_url": a.url})
    json.dump(items, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"SAVED {path} ({os.path.getsize(path)} bytes)\nCREDIT {credit}")
    if a.license.lower() not in {"cc0", "pdm", "public domain"}:
        print("NOTE this license needs the credit line shown where the media is used (caption, description or credits page).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--type", default="image", choices=["image", "audio"])
    s.add_argument("--source", default="all", choices=["openverse", "commons", "nasa", "all"])
    s.add_argument("--use", default="commercial", choices=["commercial", "modify", "any"])
    s.add_argument("--limit", type=int, default=8)
    s.add_argument("--json", action="store_true")
    g = sub.add_parser("get")
    g.add_argument("url")
    g.add_argument("--out", required=True)
    for k in ("title", "creator", "license"):
        g.add_argument("--" + k, required=True)
    g.add_argument("--license-url", default="")
    g.add_argument("--source-url", required=True)
    a = ap.parse_args()
    (cmd_search if a.cmd == "search" else cmd_get)(a)


if __name__ == "__main__":
    main()
