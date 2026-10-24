#!/usr/bin/env python3
"""Summarize the owner's own Instagram data export ("Download your information", JSON format).

usage: ig_export.py EXPORT.zip_or_folder [--out DIR] [--include-messages]

Unpacks the export into DIR (safely: no paths outside DIR), lists what is inside,
and writes summary.json with what can be counted reliably: followers, following,
who you follow that does not follow back, posts and reels by month, comments and
likes you gave. Direct messages are skipped unless --include-messages is given.
Nothing leaves this machine.
"""
import argparse
import collections
import datetime
import json
import os
import sys
import zipfile


def safe_unzip(zpath, dest):
    dest = os.path.realpath(dest)
    with zipfile.ZipFile(zpath) as z:
        for m in z.infolist():
            target = os.path.realpath(os.path.join(dest, m.filename))
            if target != dest and not target.startswith(dest + os.sep):
                sys.exit(f"UNSAFE_ZIP entry outside the folder: {m.filename}")
        z.extractall(dest)
    return dest


def load(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (ValueError, OSError):
        return None


def fix(s):
    """Meta exports store text as UTF-8 bytes read as Latin-1; undo that so Hebrew is readable."""
    if isinstance(s, str):
        try:
            return s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return s
    return s


def usernames(obj):
    """Collect usernames from Meta's string_list_data structures, whatever the wrapper key."""
    out = set()
    def walk(x):
        if isinstance(x, dict):
            if "string_list_data" in x:
                for s in x["string_list_data"]:
                    if s.get("value"):
                        out.add(fix(s["value"]))
                    elif s.get("href"):
                        out.add(s["href"].rstrip("/").split("/")[-1])
                if x.get("title"):
                    out.add(fix(x["title"]))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return out


def timestamps(obj):
    found = []
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ("creation_timestamp", "timestamp") and isinstance(v, (int, float)) and v > 1e9:
                    found.append(int(v))
                else:
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return found


def by_month(ts):
    c = collections.Counter(datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m") for t in ts)
    return dict(sorted(c.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--out", default=os.path.join(os.getcwd(), "ig-export"))
    ap.add_argument("--include-messages", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    root = safe_unzip(a.export, os.path.join(a.out, "data")) if a.export.lower().endswith(".zip") else a.export

    files = []
    for dp, dn, fn in os.walk(root):
        if not a.include_messages:
            dn[:] = [d for d in dn if d not in ("messages", "inbox", "message_requests")]
        for f in fn:
            if f.endswith(".json"):
                files.append(os.path.join(dp, f))
    cats = collections.Counter(os.path.relpath(f, root).split(os.sep)[0] for f in files)
    print("FILES", len(files), "json files;", dict(cats))

    followers, following, posts, reels, stories, comments, likes = set(), set(), [], [], [], [], []
    for f in files:
        name = os.path.basename(f).lower()
        rel = os.path.relpath(f, root).lower()
        d = load(f)
        if d is None:
            continue
        if name.startswith("followers"):
            followers |= usernames(d)
        elif name.startswith("following") and "hashtag" not in name:
            following |= usernames(d)
        elif name.startswith("posts_"):
            posts += timestamps(d)
        elif name.startswith("reels"):
            reels += timestamps(d)
        elif name.startswith("stories"):
            stories += timestamps(d)
        elif "comments" in name and "content" not in rel:
            comments += timestamps(d)
        elif name.startswith("liked_posts") or name.startswith("liked_comments"):
            likes += timestamps(d)

    summary = {
        "followers": len(followers),
        "following": len(following),
        "you_follow_they_dont_follow_back": sorted(following - followers),
        "they_follow_you_dont_follow_back": sorted(followers - following),
        "posts_by_month": by_month(posts),
        "reels_by_month": by_month(reels),
        "stories_by_month": by_month(stories),
        "comments_you_wrote_by_month": by_month(comments),
        "likes_you_gave_by_month": by_month(likes),
        "messages_included": a.include_messages,
        "data_folder": root,
    }
    p = os.path.join(a.out, "summary.json")
    json.dump(summary, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("WROTE", p)
    print("FOLLOWERS", summary["followers"], "| FOLLOWING", summary["following"],
          "| not following back:", len(summary["you_follow_they_dont_follow_back"]),
          "| posts", len(posts), "| reels", len(reels), "| stories", len(stories))


if __name__ == "__main__":
    main()
