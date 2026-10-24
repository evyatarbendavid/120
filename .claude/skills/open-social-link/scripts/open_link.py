#!/usr/bin/env python3
"""Open a social video link or a local video file: metadata, the video file, a frame grid and the audio.

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

    r = run(["yt-dlp", "--no-playlist", "--write-info-json", "--no-write-playlist-metafiles",
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
    if r.returncode != 0 or not os.path.exists(video):
        err = (r.stderr or "")[-1500:]
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
