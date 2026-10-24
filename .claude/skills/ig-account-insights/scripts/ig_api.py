#!/usr/bin/env python3
"""Read-only access to the owner's own Instagram account through Meta's official API.

usage:
  ig_api.py check                       # is a token present and valid? which account?
  ig_api.py profile  [--out DIR]        # username, followers, following, post count
  ig_api.py media    [--out DIR] [--limit 50] [--insights]   # posts and reels, optional per-post insights
  ig_api.py account  [--out DIR] [--days 28]                 # account-level reach, views, follower change

The token is read from the IG_ACCESS_TOKEN environment variable or from
~/.config/ig-account-insights/token (one line, file mode 600). It is never printed.
Only GET requests are made: nothing is posted, liked, followed or changed.
Needs a Professional (Creator or Business) account and a token with the
instagram_business_basic and instagram_business_manage_insights permissions.
"""
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://graph.instagram.com"
TOKEN_FILE = os.path.expanduser("~/.config/ig-account-insights/token")
POST_METRICS = "reach,views,likes,comments,shares,saved,total_interactions"
REEL_EXTRA = ",ig_reels_avg_watch_time,ig_reels_video_view_total_time"


def token():
    t = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if not t and os.path.isfile(TOKEN_FILE):
        t = open(TOKEN_FILE, encoding="utf-8").read().strip()
    if not t:
        sys.exit("NO_TOKEN: set IG_ACCESS_TOKEN or put the token in " + TOKEN_FILE +
                 " (see the skill's setup steps). Never paste it into the chat.")
    return t


def get(path, **params):
    tok = token()
    params["access_token"] = tok
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "ig-account-insights"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace").replace(tok, "<token>")
        try:
            err = json.loads(body).get("error", {})
            msg = f"{err.get('type', 'HTTPError')} {err.get('code', e.code)}: {err.get('message', '')}"
        except ValueError:
            msg = f"HTTP {e.code}"
        if "190" in msg:
            msg += "  (the token is invalid or expired: make a new one and save it the same way)"
        raise SystemExit("API_ERROR " + msg)
    except urllib.error.URLError as e:
        raise SystemExit(f"NETWORK_ERROR {e.reason} (is graph.instagram.com allowed in the environment?)")


def save(out, name, data):
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, name)
    if name.endswith(".csv"):
        keys = sorted({k for row in data for k in row})
        with open(p, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(data)
    else:
        json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("WROTE", p)


def profile(a):
    d = get("/me", fields="user_id,username,name,account_type,followers_count,follows_count,media_count,biography,website")
    save(a.out, "profile.json", d)
    print("ACCOUNT", d.get("username"), "|", d.get("account_type"), "| followers", d.get("followers_count"),
          "| following", d.get("follows_count"), "| posts", d.get("media_count"))


def media(a):
    fields = "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count"
    rows, page = [], get("/me/media", fields=fields, limit=min(a.limit, 50))
    while True:
        rows += page.get("data", [])
        nxt = page.get("paging", {}).get("cursors", {}).get("after")
        if len(rows) >= a.limit or not nxt or not page.get("paging", {}).get("next"):
            break
        page = get("/me/media", fields=fields, limit=50, after=nxt)
    rows = rows[: a.limit]
    if a.insights:
        for r in rows:
            metrics = POST_METRICS + (REEL_EXTRA if r.get("media_product_type") == "REELS" else "")
            try:
                ins = get(f"/{r['id']}/insights", metric=metrics)
            except SystemExit as e:  # some metrics are unavailable for some media types or old posts
                r["insights_error"] = str(e)[:160]
                continue
            for m in ins.get("data", []):
                vals = m.get("values") or [{}]
                r[m["name"]] = vals[0].get("value", m.get("total_value", {}).get("value"))
    for r in rows:
        r["caption"] = (r.get("caption") or "").replace("\n", " ")[:300]
    save(a.out, "media.json", rows)
    save(a.out, "media.csv", rows)
    print("MEDIA", len(rows), "items", "(with insights)" if a.insights else "")


def account(a):
    import time
    until = int(time.time())
    since = until - a.days * 86400
    out = {}
    for metric, extra in (("reach", {}), ("views", {}), ("accounts_engaged", {}), ("total_interactions", {}),
                          ("follows_and_unfollows", {"breakdown": "follow_type"})):
        try:
            d = get("/me/insights", metric=metric, period="day", metric_type="total_value",
                    since=since, until=until, **extra)
            out[metric] = d.get("data", [])
        except SystemExit as e:
            out[metric] = {"error": str(e)[:200]}
    try:
        out["follower_demographics"] = get("/me/insights", metric="follower_demographics", period="lifetime",
                                           metric_type="total_value", breakdown="country,city,age,gender").get("data", [])
    except SystemExit as e:
        out["follower_demographics"] = {"error": str(e)[:200]}
    save(a.out, f"account_{a.days}d.json", out)


def check(a):
    d = get("/me", fields="user_id,username,account_type")
    print("TOKEN_OK", d.get("username"), "|", d.get("account_type"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "profile", "media", "account"])
    ap.add_argument("--out", default=os.path.join(os.getcwd(), "ig-account"))
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--insights", action="store_true")
    ap.add_argument("--days", type=int, default=28)
    a = ap.parse_args()
    {"check": check, "profile": profile, "media": media, "account": account}[a.cmd](a)


if __name__ == "__main__":
    main()
