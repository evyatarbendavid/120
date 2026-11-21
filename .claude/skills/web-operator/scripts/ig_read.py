#!/usr/bin/env python3
"""Read Instagram through Meta's official Graph API (read-only). Works in any cloud session once the owner's
token is saved as the environment's network secret (request_credential, host graph.facebook.com).

usage:
  ig_read.py whoami                         which Instagram account the token reads as
  ig_read.py profile <username>             another Business/Creator account: bio, website, followers, post count
  ig_read.py posts <username> [--limit 12]  the same plus its latest posts (caption, type, likes, comments, link, date)
  ig_read.py mine [--limit 12]              the owner's own latest posts with likes and comments
  add --json to any command for raw JSON.

What this can and cannot read (Meta's Business Discovery): public data of OTHER professional (Business or Creator)
accounts only. A personal account, a private account or a misspelled name returns an error, and so do age-gated
accounts. No stories, no followers list, no DMs, no search. Some media fields are missing for reels whose owner
turned off downloads. Instagram's website itself shows a cloud session only a login wall (the login page returns
429); do not scrape it, use this instead.

Token, never in chat or in a repo file; from the first that exists:
  1. the environment's saved network secret for graph.facebook.com (the proxy adds the header itself);
  2. $IG_ACCESS_TOKEN;  3. ~/.config/ig-account-insights/token.
One request per call, no retries: a rate-limit answer stops the command so the account is never hammered.
Standard library only. Network: only graph.facebook.com (or graph.instagram.com with --host for `mine`).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "web-operator-ig-read/1.0"
RATE_CODES = {4, 17, 32, 613}


def token():
    t = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if t:
        return t
    p = os.path.expanduser("~/.config/ig-account-insights/token")
    if os.path.isfile(p):
        return open(p).read().strip()
    return "proxy-injected"  # in a cloud session the proxy swaps this for the saved network secret


def get(a, path, params=None):
    base = os.environ.get("IG_READ_TEST_BASE")  # tests only: a local mock server on 127.0.0.1
    if base and not base.startswith("http://127.0.0.1:"):
        sys.exit("IG_READ_TEST_BASE may only point at http://127.0.0.1 (tests)")
    url = f"{base or 'https://' + a.host}/{a.api_version}/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token(), "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode()).get("error", {})
        except Exception:
            err = {}
        fail(e.code, err)
    except urllib.error.URLError as e:
        sys.exit(f"network error: {e.reason}")


def fail(status, err):
    code, msg = err.get("code"), err.get("message", "")
    if status == 401 or code == 190:
        sys.exit("TOKEN: missing, expired or invalid. Ask the owner to save a fresh token with request_credential "
                 "(host graph.facebook.com, Authorization, Bearer). Never ask for it in chat. (" + msg + ")")
    if code in RATE_CODES or status == 429:
        sys.exit("RATE LIMIT from Instagram. Stop; do not retry now. Wait an hour or more. (" + msg + ")")
    if code == 100 and ("business_discovery" in msg or "username" in msg.lower() or "Unsupported get" in msg):
        sys.exit("NOT READABLE: this username is not a public Business/Creator account (personal, private, age-gated "
                 "or misspelled), or the token lacks permission. (" + msg + ")")
    if code == 10 or code == 200:
        sys.exit("PERMISSION: the token lacks a permission (instagram_basic, pages_show_list, pages_read_engagement). (" + msg + ")")
    sys.exit(f"HTTP {status} code {code}: {msg}")


def my_ig(a):
    """The Instagram account id and username the token reads as."""
    if a.ig_id:
        return a.ig_id, "?"
    d = get(a, "me", {"fields": "instagram_business_account{id,username}"})
    acc = d.get("instagram_business_account")
    if not acc:
        d = get(a, "me/accounts", {"fields": "name,instagram_business_account{id,username}"})
        for page in d.get("data", []):
            if page.get("instagram_business_account"):
                acc = page["instagram_business_account"]
                break
    if not acc:
        sys.exit("No Instagram professional account is linked to this token's Facebook Page. The work account must be "
                 "Business or Creator and connected to a Page.")
    return acc["id"], acc.get("username", "?")


def media_fields(n):
    return f"media.limit({n}){{caption,media_type,permalink,timestamp,like_count,comments_count}}"


def show_profile(b):
    print(f"@{b.get('username')}  {b.get('name') or ''}".rstrip())
    print(f"  followers {b.get('followers_count')}  following {b.get('follows_count')}  posts {b.get('media_count')}")
    if b.get("biography"):
        print("  bio:", " | ".join(b["biography"].splitlines()))
    if b.get("website"):
        print("  site:", b["website"])


def show_posts(items):
    for m in items:
        cap = " ".join((m.get("caption") or "").split())[:140]
        print(f"- {m.get('timestamp', '')[:10]} {m.get('media_type', '')} likes {m.get('like_count', '-')} "
              f"comments {m.get('comments_count', '-')}  {m.get('permalink', '')}")
        if cap:
            print("    ", cap)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="graph.facebook.com", choices=["graph.facebook.com", "graph.instagram.com"])
    ap.add_argument("--api-version", default="v21.0")
    ap.add_argument("--ig-id", help="the owner's Instagram professional account id (found automatically if omitted)")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    for name in ("profile", "posts"):
        p = sub.add_parser(name)
        p.add_argument("username")
        p.add_argument("--limit", type=int, default=12)
    p = sub.add_parser("mine")
    p.add_argument("--limit", type=int, default=12)
    a = ap.parse_args()

    if a.cmd == "whoami":
        iid, uname = my_ig(a)
        print(json.dumps({"id": iid, "username": uname}) if a.json else f"reads as @{uname} (id {iid})")
        return
    if a.cmd == "mine":
        n = max(1, min(a.limit, 25))
        iid, _ = my_ig(a)
        d = get(a, iid, {"fields": f"username,followers_count,media_count,{media_fields(n)}"})
        if a.json:
            print(json.dumps(d, ensure_ascii=False, indent=1))
            return
        print(f"@{d.get('username')}  followers {d.get('followers_count')}  posts {d.get('media_count')}")
        show_posts(d.get("media", {}).get("data", []))
        return
    username = a.username.lstrip("@").strip()
    if not username.replace(".", "").replace("_", "").isalnum():
        sys.exit("username: letters, digits, dots and underscores only")
    n = max(1, min(a.limit, 25))
    fields = "username,name,biography,website,followers_count,follows_count,media_count"
    if a.cmd == "posts":
        fields += "," + media_fields(n)
    iid, _ = my_ig(a)
    d = get(a, iid, {"fields": f"business_discovery.username({username}){{{fields}}}"})
    b = d.get("business_discovery", {})
    if a.json:
        print(json.dumps(b, ensure_ascii=False, indent=1))
        return
    show_profile(b)
    if a.cmd == "posts":
        show_posts(b.get("media", {}).get("data", []))


if __name__ == "__main__":
    main()
