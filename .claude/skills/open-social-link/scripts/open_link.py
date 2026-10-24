#!/usr/bin/env python3
"""Open any link (social video, other video sites, a direct video file, or a web page) or a local video file: metadata, the video file, a frame grid and the audio.

usage: open_link.py URL_OR_FILE [--out DIR] [--transcribe] [--model small] [--lang he]

Downloads with yt-dlp (720p at most), writes info.json, video.mp4, grid.jpg (8 frames
spread over the video, for looking at), audio.wav (16 kHz mono) and, with
--transcribe, transcript.txt made locally with faster-whisper (free, no API key).
Prints the paths and a one-line diagnosis when a site blocks the request.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

BLOCKS = [
    ("IP address is blocked", "This post is blocked for cloud-server addresses (usually a region limit set by the poster). "
                              "Other posts from the same site often work; this one opens only in a Local session."),
    ("not a bot", "YouTube blocks cloud servers. Use the title/description from info if present, "
                  "or open the link in a Local session on the owner's computer."),
    ("CONNECT tunnel failed", "The environment's network policy blocks a host. Add it under the "
                              "environment's Network access > Allowed domains."),
    ("403", "A host was refused (network policy or the site). Check the proxy status: "
            "curl -sS \"$HTTPS_PROXY/__agentproxy/status\" lists the refused hosts."),
    ("login", "The site wants a logged-in account from a cloud server. Single posts/reels usually "
              "work; whole profiles usually do not. Otherwise use a Local session."),
    ("429", "Rate-limited by the site. Wait a few minutes or use a single-post link."),
    ("impersonat", "TikTok needs curl_cffi: python3 -m pip install curl_cffi"),
]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def diagnose(text):
    low = text.lower()
    for key, advice in BLOCKS:
        if key.lower() in low:
            return advice
    return None


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def proxy_failures():
    """(time, host) pairs the cloud network policy refused (empty outside a cloud session)."""
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not proxy:
        return set()
    r = run(["curl", "-sS", "-m", "15", proxy.rstrip("/") + "/__agentproxy/status"])
    try:
        fails = json.loads(r.stdout).get("recentRelayFailures", [])
    except ValueError:
        return set()
    return {(f.get("ts", ""), f.get("host", "").split(":")[0]) for f in fails if f.get("host")}


def fallback(a, video, err):
    """When yt-dlp cannot read a link: fetch it directly. A direct video file becomes
    video.mp4; any other page is saved as page.txt (title and readable text) so it can
    still be read. Returns True only when a video was obtained."""
    if "youtube.com/" in a.url or "youtu.be/" in a.url:
        # YouTube blocks cloud servers from the video, but its oEmbed endpoint still names it.
        import urllib.parse as _up
        o = run(["curl", "-sS", "-m", "30", "https://www.youtube.com/oembed?format=json&url=" + _up.quote(a.url, safe="")])
        try:
            meta = json.loads(o.stdout)
            keep = {"title": meta.get("title"), "uploader": meta.get("author_name"),
                    "channel_url": meta.get("author_url"), "webpage_url": a.url, "thumbnail": meta.get("thumbnail_url")}
            json.dump(keep, open(os.path.join(a.out, "info.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("INFO", os.path.join(a.out, "info.json"))
            print("TITLE", keep["title"], "|", keep["uploader"], "| YouTube (metadata only)")
            thumb = keep.get("thumbnail")
            if thumb and run(["curl", "-sS", "-m", "30", "-o", os.path.join(a.out, "thumbnail.jpg"), thumb]).returncode == 0:
                print("THUMBNAIL", os.path.join(a.out, "thumbnail.jpg"))
        except ValueError:
            pass
        return False
    raw = os.path.join(a.out, "download.bin")
    hdr = os.path.join(a.out, "headers.txt")
    r = run(["curl", "-sSL", "-m", "300", "--max-filesize", "1500000000", "-A", UA,
             "-D", hdr, "-o", raw, a.url])
    if r.returncode != 0 or not os.path.exists(raw):
        return False
    ctype = ""
    for line in open(hdr, encoding="latin-1"):
        if line.lower().startswith("content-type:"):
            ctype = line.split(":", 1)[1].strip().lower()
    if ctype.startswith(("video/", "audio/", "application/octet-stream")):
        c = run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-c", "copy", "-movflags", "+faststart", video])
        if c.returncode != 0:
            c = run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-c:v", "libx264", "-preset", "veryfast",
                     "-c:a", "aac", video])
        os.remove(raw)
        if c.returncode == 0 and os.path.exists(video):
            print("TITLE", a.url, "| direct media file")
            return True
        return False
    if "html" in ctype or "text" in ctype:
        import html as _html
        import re as _re
        page = open(raw, encoding="utf-8", errors="replace").read()
        title = _re.search(r"<title[^>]*>(.*?)</title>", page, _re.S | _re.I)
        meta = dict(_re.findall(r'<meta[^>]+(?:property|name)=["\'](og:title|og:description|description)["\'][^>]+content=["\']([^"\']*)', page, _re.I))
        body = _re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", " ", page)
        body = _html.unescape(_re.sub(r"(?s)<[^>]+>", " ", body))
        body = _re.sub(r"[ \t\r\f\v]+", " ", body)
        body = "\n".join(l.strip() for l in body.splitlines() if l.strip())
        out = os.path.join(a.out, "page.txt")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("URL: %s\nTITLE: %s\n" % (a.url, _html.unescape(title.group(1).strip()) if title else ""))
            for k, v in meta.items():
                fh.write("%s: %s\n" % (k.upper(), _html.unescape(v)))
            fh.write("\n" + body[:60000] + "\n")
        os.remove(raw)
        print("PAGE", out, "(no video found on this page; its title and text are saved)")
        print("TIP", "For a screenshot of the page, open it with the Playwright browser tool.")
        return False
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default=os.path.join(os.getcwd(), "social-link"))
    ap.add_argument("--transcribe", action="store_true")
    ap.add_argument("--model", default="small", help="faster-whisper model (small, medium, large-v3)")
    ap.add_argument("--lang", default=None, help="language code, e.g. he or en (default: detect)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    video = os.path.join(a.out, "video.mp4")
    info = {}
    local = os.path.expanduser(a.url)
    if os.path.isfile(local):
        # A file the user attached or uploaded (for example ~/.claude/uploads/...): no download.
        r = run(["ffmpeg", "-loglevel", "error", "-y", "-i", local, "-c", "copy", "-movflags", "+faststart", video])
        if r.returncode != 0:
            r = run(["ffmpeg", "-loglevel", "error", "-y", "-i", local, "-vf", "scale=-2:'min(720,ih)'",
                     "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", video])
        if r.returncode != 0 or not os.path.exists(video):
            print("OPEN_FAILED")
            print((r.stderr or "").strip().splitlines()[-1] if (r.stderr or "").strip() else "(not a video ffmpeg can read)")
            sys.exit(2)
        info = {"title": os.path.basename(local), "source_file": local}
        json.dump(info, open(os.path.join(a.out, "info.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("INFO", os.path.join(a.out, "info.json"))
        print("TITLE", info["title"], "| local file")
        return finish(a, video, info)
    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp is not installed: python3 -m pip install yt-dlp")

    before = proxy_failures()
    r = run(["yt-dlp", "--compat-options", "no-certifi", "--no-playlist", "--write-info-json", "--no-write-playlist-metafiles",
             "-f", "b[height<=720]/bv*[height<=720]+ba/b", "--merge-output-format", "mp4",
             "-o", os.path.join(a.out, "video.%(ext)s"), a.url], timeout=600)
    info_path = os.path.join(a.out, "video.info.json")
    if os.path.exists(info_path):
        info = json.load(open(info_path, encoding="utf-8"))
        keep = {k: info.get(k) for k in ("title", "uploader", "channel", "duration", "upload_date",
                                         "view_count", "like_count", "description", "webpage_url")}
        json.dump(keep, open(os.path.join(a.out, "info.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("INFO", os.path.join(a.out, "info.json"))
        print("TITLE", keep.get("title"), "|", keep.get("uploader") or keep.get("channel"),
              "|", keep.get("duration"), "s")
    if (r.returncode != 0 or not os.path.exists(video)) and fallback(a, video, r.stderr or ""):
        return finish(a, video, {"title": a.url, "webpage_url": a.url})
    if r.returncode != 0 or not os.path.exists(video):
        err = (r.stderr or "")[-1500:]
        refused = sorted({h for t, h in proxy_failures() - before})
        if refused:
            err += "\nCONNECT tunnel failed"
            print("REFUSED_HOSTS", " ".join(refused))
        print("DOWNLOAD_FAILED")
        print(err.strip().splitlines()[-1] if err.strip() else "(no error text)")
        advice = diagnose(err)
        if advice:
            print("WHY", advice)
        sys.exit(2)
    return finish(a, video, info)


def finish(a, video, info):
    print("VIDEO", video)
    dur = float(info.get("duration") or 0)
    if not dur:
        p = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video])
        try:
            dur = float(p.stdout.strip())
        except ValueError:
            dur = 30.0
    step = max(dur / 8.0, 0.5)
    grid = os.path.join(a.out, "grid.jpg")
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", video, "-vf",
         f"fps=1/{step:.3f},scale=270:-1,tile=4x2", "-frames:v", "1", grid])
    if os.path.exists(grid):
        print("GRID", grid, f"(8 frames, one every {step:.1f}s, left to right, top to bottom)")
    wav = os.path.join(a.out, "audio.wav")
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav])
    if os.path.exists(wav):
        print("AUDIO", wav)

    if a.transcribe and os.path.exists(wav):
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            for extra in ([], ["--break-system-packages"]):
                if run([sys.executable, "-m", "pip", "install", "-q", "faster-whisper", *extra]).returncode == 0:
                    break
            from faster_whisper import WhisperModel
        model = WhisperModel(a.model, device="cpu", compute_type="int8")
        segs, meta = model.transcribe(wav, language=a.lang, vad_filter=True)
        lines = [f"[{s.start:6.1f}] {s.text.strip()}" for s in segs]
        path = os.path.join(a.out, "transcript.txt")
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("TRANSCRIPT", path, f"(language {meta.language}, model {a.model})")


if __name__ == "__main__":
    main()
