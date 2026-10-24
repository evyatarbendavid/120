---
name: open-social-link
description: Open a link to a video or post from Instagram, Facebook, TikTok or YouTube (or any site yt-dlp supports), or a video file the user attached to the chat, and actually look at it - title, author and caption, the video downloaded, a grid of frames to view, and a free local transcript of what is said. Use whenever the user pastes such a link, says "look at this reel/video/post", "what does he say here", "open this link", "analyze this video", attaches a video file, or in Hebrew "תראה את הסרטון", "תפתח את הקישור", "מה הוא אומר פה", "תנתח את הריל". For deeper video analysis after this, see the watch and ig-viral skills.
license: MIT
---

# Open a social link

Written for this repository. It turns a link the user pasted into things you can read and see.

## Steps

0. **An attached video file** arrives in `~/.claude/uploads/<session id>/` with a short prefix on its
   name. Find the newest one with `ls -t ~/.claude/uploads/*/ | head` and pass its full path instead
   of a URL. The helper then skips the download and does everything else the same way.
1. Run the helper from this skill's folder, writing into the session's scratchpad or a temp dir:
   `python3 scripts/open_link.py "<URL or file path>" --out <dir> --transcribe --lang he`
   Leave out `--lang` when the language is not Hebrew. `--model medium` is more accurate and slower.
   The first transcription downloads the model once (about 500 MB for `small`).
2. Read `info.json` (title, author, caption, duration) and look at `grid.jpg` with the Read tool:
   8 frames in time order. For a closer look at a moment, cut a frame with
   `ffmpeg -ss <seconds> -i video.mp4 -frames:v 1 frame.jpg` and read it.
3. Read `transcript.txt`. A small model mishears words, so mark guesses and do not invent text.
4. Answer what the user asked, in their language. Say what you saw and heard, not what you assume.

## When it fails

The helper prints `DOWNLOAD_FAILED` and a `WHY` line. Pass that on plainly, then:

- **YouTube "not a bot"**: YouTube blocks cloud servers. Give what the page shows (title, channel,
  description) if the browser tool can open it, and say the video itself opens in a Local session
  on the user's own computer.
- **Network policy (403, CONNECT failed)**: run `curl -sS "$HTTPS_PROXY/__agentproxy/status"`; its
  `recentRelayFailures` list the refused hosts. Ask the user to add exactly those under the cloud
  environment's Network access > Allowed domains, then open a new session.
- **Login wall or 429 on Instagram**: a whole profile needs an account from a cloud server. Ask for a
  link to the single reel or post.
- **The browser (Playwright) shows a certificate error on every site**: run
  `bash scripts/trust-proxy-ca.sh` from this folder; it makes the browser trust the cloud proxy.
  The setup script normally does this already.

## Rules

- Never ask the user for a password, cookies or a login. If a site needs an account, say so and offer
  the Local-session route, where their own browser is already signed in.
- Do not post, like, comment or follow anything. This skill only reads.
- Keep downloads in a temp or scratchpad folder, never inside the user's repository.
