---
title: YouTube captions download from the cloud even when the video gets 403
tags: youtube, transcript, captions, subtitles, yt-dlp, cloud, 403, 429
saved: 2026-10-31
---

# YouTube captions download from the cloud even when the video gets 403

## Problem
yt-dlp / open_link.py fails on a YouTube video with 'ERROR: unable to download video data: HTTP Error 403: Forbidden' (YouTube blocks cloud IPs for media), but the user only needs a transcript

## Solution
Skip the media and fetch only the caption track: yt-dlp --compat-options no-certifi --skip-download --write-subs --write-auto-subs --sub-langs 'en,en-en' --sub-format vtt -o 'subs/%(id)s' '<URL>'. Ask for one or two exact languages; requesting many (en.*) triggers HTTP 429 on the extra tracks. Read the .vtt and strip the timestamps. Title/channel: https://www.youtube.com/oembed?url=<URL>&format=json. If the video has no caption track at all, fall back to the owner uploading the file or a Local session, then faster-whisper.

## Tried first (did not work)
open-social-link open_link.py: metadata only, video download 403. A broad --sub-langs 'en.*' got 429 Too Many Requests on the translated tracks.

## How to check it worked
subs/<ID>.en.vtt exists and holds cue lines; uploaded (non-auto) captions say 'Kind: captions'.

## When this does not apply
Videos with no captions and no auto-captions, or when the actual video/audio file is needed (editing, frames): then
the owner uploads the file, or it runs in a Local session / on their computer via Remote Control (list_computer_folders).
Do not use the owner's YouTube login or cookies for this.
