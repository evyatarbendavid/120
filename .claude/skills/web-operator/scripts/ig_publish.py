#!/usr/bin/env python3
"""Publish to an Instagram professional (work) account through Meta's official Content Publishing API.

usage:
  ig_publish.py whoami                                   which account the token belongs to
  ig_publish.py limit                                    posts used in the last 24 h (Meta allows 100)
  ig_publish.py prepare --image-url URL --caption "..."  [--ai-label]          single photo
  ig_publish.py prepare --video-url URL --caption "..."  [--cover-url URL] [--no-feed] [--ai-label]   reel
  ig_publish.py prepare --carousel URL URL ... --caption "..."  [--ai-label]   2-10 photos/videos
  ig_publish.py status <container_id>                    FINISHED / IN_PROGRESS / ERROR
  ig_publish.py publish <container_id>                   makes the prepared post public

Two steps on purpose: `prepare` builds the post on Instagram's side without publishing it; `publish`
makes it public. Claude shows the owner the exact media and caption between the two and publishes
only after a yes. Media must be at a public https URL (Instagram fetches it).

Token, never in chat or in a file in a repo, from the first that exists:
  1. the cloud session's saved network secret for the API host (the proxy adds the header itself);
  2. $IG_ACCESS_TOKEN;
  3. ~/.config/ig-account-insights/token (shared with the ig-account-insights skill).
Host: graph.instagram.com (Instagram Login, default) or --host graph.facebook.com (Facebook Login).
Standard library only. Network: only the host above.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "web-operator-ig-publish/1.0"


def token():
    t = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    if t:
        return t
    p = os.path.expanduser("~/.config/ig-account-insights/token")
    if os.path.isfile(p):
        return open(p).read().strip()
    # No local token: in a cloud session the proxy replaces this with the saved network secret.
    return "proxy-injected"


def call(a, method, path, params=None):
    base = os.environ.get("IG_PUBLISH_TEST_BASE")  # tests only: a local mock server on 127.0.0.1
    if base and not base.startswith("http://127.0.0.1:"):
        sys.exit("IG_PUBLISH_TEST_BASE may only point at http://127.0.0.1 (tests)")
    url = f"{base or 'https://' + a.host}/{a.api_version}/{path.lstrip('/')}"
    data = None
    if params and method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    elif params:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": "Bearer " + token(), "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            err = json.loads(body).get("error", {})
            msg = f"{err.get('type', '')} {err.get('code', '')}: {err.get('message', body[:200])}"
        except ValueError:
            msg = body[:200]
        hint = ""
        if e.code == 401 or '"code":190' in body.replace(" ", ""):  # 190 = invalid or expired token
            hint = ("\nHINT no valid token. In a cloud session ask the owner through the credential form "
                    f"(host {a.host}, Authorization: Bearer). Never ask for it in chat.")
        sys.exit(f"API ERROR HTTP {e.code} {msg}{hint}")


def me(a):
    fields = "user_id,username,account_type,media_count" if a.host == "graph.instagram.com" else "id,name"
    return call(a, "GET", "me", {"fields": fields})


def ig_id(a):
    if a.ig_id:
        return a.ig_id
    m = me(a)
    return m.get("user_id") or m.get("id")


def cmd_whoami(a):
    print(json.dumps(me(a), ensure_ascii=False, indent=1))


def cmd_limit(a):
    d = call(a, "GET", f"{ig_id(a)}/content_publishing_limit", {"fields": "quota_usage,config"})
    print(json.dumps(d, ensure_ascii=False, indent=1))


def container(a, uid, **p):
    if a.ai_label:
        p["is_ai_generated"] = "true"
    return call(a, "POST", f"{uid}/media", p)["id"]


def wait(a, cid, tries=60):
    for _ in range(tries):
        s = call(a, "GET", cid, {"fields": "status_code,status"})
        code = s.get("status_code")
        if code in ("FINISHED", "PUBLISHED"):
            return code
        if code in ("ERROR", "EXPIRED"):
            sys.exit(f"CONTAINER {cid} {code}: {s.get('status', '')}")
        time.sleep(5)
    sys.exit(f"CONTAINER {cid} still processing; check later with: status {cid}")


def cmd_prepare(a):
    if not (a.carousel or a.video_url or a.image_url):
        sys.exit("give --image-url, --video-url or --carousel")
    for u in (a.carousel or []) + [a.video_url or "", a.image_url or "", a.cover_url or ""]:
        if u and not u.startswith("https://"):
            sys.exit(f"media must be a public https URL (Instagram downloads it): {u}")
    if a.carousel and not 2 <= len(a.carousel) <= 10:
        sys.exit("a carousel takes 2 to 10 items")
    if len(a.caption) > 2200:
        sys.exit(f"caption is {len(a.caption)} characters; Instagram allows 2,200")
    uid = ig_id(a)
    if a.carousel:
        kids = []
        for u in a.carousel:
            is_vid = u.lower().split("?")[0].endswith((".mp4", ".mov"))
            kid = container(a, uid, is_carousel_item="true",
                            **({"media_type": "VIDEO", "video_url": u} if is_vid else {"image_url": u}))
            wait(a, kid)
            kids.append(kid)
        cid = container(a, uid, media_type="CAROUSEL", children=",".join(kids), caption=a.caption)
    elif a.video_url:
        p = {"media_type": "REELS", "video_url": a.video_url, "caption": a.caption,
             "share_to_feed": "false" if a.no_feed else "true"}
        if a.cover_url:
            p["cover_url"] = a.cover_url
        cid = container(a, uid, **p)
    elif a.image_url:
        cid = container(a, uid, image_url=a.image_url, caption=a.caption)
    else:
        sys.exit("give --image-url, --video-url or --carousel")
    code = wait(a, cid)
    print(f"PREPARED container {cid} ({code}). NOT published yet.")
    print(f"Show the owner the media and this caption, then on a yes run: publish {cid}")
    print("CAPTION:\n" + a.caption)


def cmd_status(a):
    print(json.dumps(call(a, "GET", a.container, {"fields": "status_code,status"}), indent=1))


def cmd_publish(a):
    uid = ig_id(a)
    d = call(a, "POST", f"{uid}/media_publish", {"creation_id": a.container})
    mid = d.get("id")
    link = call(a, "GET", mid, {"fields": "permalink"}).get("permalink", "") if mid else ""
    print(f"PUBLISHED media {mid} {link}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="graph.instagram.com", choices=["graph.instagram.com", "graph.facebook.com"])
    ap.add_argument("--api-version", default="v21.0")
    ap.add_argument("--ig-id", help="Instagram account id (found automatically with Instagram Login)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    sub.add_parser("limit")
    p = sub.add_parser("prepare")
    p.add_argument("--image-url")
    p.add_argument("--video-url")
    p.add_argument("--cover-url")
    p.add_argument("--carousel", nargs="+")
    p.add_argument("--caption", default="")
    p.add_argument("--no-feed", action="store_true", help="reel: do not also show it in the main feed")
    p.add_argument("--ai-label", action="store_true", help="mark as AI-generated (use for AI images/video)")
    s = sub.add_parser("status")
    s.add_argument("container")
    pu = sub.add_parser("publish")
    pu.add_argument("container")
    a = ap.parse_args()
    if getattr(a, "ai_label", None) is None:
        a.ai_label = False
    {"whoami": cmd_whoami, "limit": cmd_limit, "prepare": cmd_prepare, "status": cmd_status,
     "publish": cmd_publish}[a.cmd](a)


if __name__ == "__main__":
    main()
