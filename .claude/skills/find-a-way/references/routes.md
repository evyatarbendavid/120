# Routes by obstacle

Concrete routes to try, grouped by what went wrong. Read only the section you need. Every route here
stays inside the limits in SKILL.md section 5. Facts about the cloud environment were checked on
2026-10-31; when one turns out wrong, fix it here or save a corrected way.

## Contents
1. A host is blocked or refused
2. A site loads but refuses bots, or shows nothing useful
3. Video, audio and social links
4. A command or tool is missing
5. A file format nobody handles
6. GitHub: private repos, `gh`, pushes
7. Accounts and services (mail, drive, design, stores)
8. Things that only exist on the user's computer
9. Research when the answer is not in one place
10. Big, slow or flaky jobs

---

## 1. A host is blocked or refused

How to tell: `curl: (56) CONNECT tunnel failed, response 403`, a Python `ProxyError` / `Tunnel connection failed: 403`,
or `recentRelayFailures` in `curl -sS "$HTTPS_PROXY/__agentproxy/status"` lists the host as `connect_rejected`.
This is the environment's allowlist. Do not retry it and do not route around it.

Same information from an allowed source:
- The service's **official API** often lives on another host (`api.<site>`, `graph.<site>`), which may be allowed.
- **oEmbed endpoints** return the title, author and thumbnail (YouTube's `https://www.youtube.com/oembed?url=<URL>&format=json` works from the cloud).
- **Package registries are always reachable** from the cloud (they bypass the proxy): `pypi.org`, `files.pythonhosted.org`,
  `registry.npmjs.org`, `jsr.io`, `index.crates.io`, `proxy.golang.org`. They are good for getting a library's source or a tool.
- **GitHub** (`github.com`, `raw.githubusercontent.com`, `codeload.github.com`) is usually allowed: try the project's own repo,
  its README, and its releases.
- **WebSearch** is the harness's own search. It works when the site is blocked, because the search
  provider has already indexed the site.
  - Set `allowed_domains: ["<site>"]`, for example `["amazon.com"]`. The result summaries carry that
    site's listings: titles, prices, product IDs (ASINs) and links.
  - Then search `"<product>" <ID> price` to find price-history and deal pages.
  - Label the result as a search snapshot, not the live page.
- **WebFetch / the web-fetch agent obey the same allowlist.** For a blocked host they answer `getaddrinfo ENOTFOUND`.
  That is the same block, not a DNS fault, so stop there and do not try more mirrors of that site.
- **Another allowed site with the same data.** For example, Alibaba (allowed) instead of Amazon (blocked) for supplier
  prices. Label the result honestly as coming from the other site.

If none of these is enough, ask the owner to allow the host (SKILL.md section 6). Include the CDNs the site needs:
- Amazon: `amazon.com`, `*.amazon.com`, `*.media-amazon.com`, `*.ssl-images-amazon.com`
- eBay: `ebay.com`, `*.ebay.com`, `*.ebayimg.com`
- AliExpress: `aliexpress.com`, `*.aliexpress.com`, `*.alicdn.com`
- TikTok (already added by the owner): `*.tiktok.com`, `*.tiktokcdn.com`, `*.tiktokcdn-us.com`, `*.ttwstatic.com`
- Reddit: `reddit.com`, `*.reddit.com`, `*.redd.it`, `*.redditmedia.com`

## 2. A site loads but refuses bots, or shows nothing useful

- A page with no content is often rendered by JavaScript: open it in the Playwright browser and read the snapshot.
- Look in the page source for embedded JSON (`__NEXT_DATA__`, `application/ld+json`, `window.__INITIAL_STATE__`).
  It often holds everything; `product-sourcing` reads Alibaba this way.
- Check `/sitemap.xml`, `/robots.txt` (and respect it), `/feed`, `/rss`, and `?format=json` variants.
- An HTTP client that looks like a normal browser (`curl_cffi` with `impersonate="chrome"`) is fine for public pages at a
  low request rate. A **captcha, login wall or "access denied" page is a stop sign**: report it and use another source or rung 7.
- The Playwright MCP may say Chromium is missing at `/opt/pw-browsers/chromium-<NNNN>/...`. That means a version
  mismatch: Chromium is at `/opt/pw-browsers/chromium`. Use a Node script that calls `require('playwright')` and
  `chromium.launch()`, which finds it, or pass `executablePath: '/opt/pw-browsers/chromium'`. Remember that a blocked host
  stays blocked in the browser too.
- Playwright cannot verify certificates in the cloud: run `bash ~/.claude/skills/open-social-link/scripts/trust-proxy-ca.sh`
  once to import the proxy's CA into the browser's store. Do not use `ignoreHTTPSErrors`.

## 3. Video, audio and social links

- Start with the `open-social-link` skill: `python3 ~/.claude/skills/open-social-link/scripts/open_link.py "<URL>"`.
  It handles Instagram, TikTok, Facebook, X, YouTube metadata and direct files, and can transcribe.
- yt-dlp failing with certificate errors behind the proxy needs `--compat-options no-certifi`, so that it uses the system CA bundle.
- **YouTube answers 403 to the video itself from cloud IPs**, although the domain is allowed. Captions still work:
  `yt-dlp --compat-options no-certifi --skip-download --write-subs --write-auto-subs --sub-langs 'en,en-en' --sub-format vtt <URL>`
  (ask for one or two exact languages; `en.*` triggers 429 on the translated tracks). oEmbed gives the title and channel.
  If the video has no captions, or the file itself is needed: the owner uploads it, or it runs in a Local session or on
  their computer (rung 6).
- Transcribe local audio with `faster-whisper` (`pip install --user faster-whisper`; the model downloads from Hugging Face).
  You can also use the `whisper` skill.
- Watch the frames: `ffmpeg -i <FILE> -vf fps=1/2 frames/%03d.jpg`, then read the images.

## 4. A command or tool is missing

In order:
1. `command -v`, then search for a near name (`ls /usr/bin | grep -i <part>`). It may be installed under another name
   (`convert` vs `magick`, `soffice` vs `libreoffice`, `python3 -m <tool>`).
2. A language package: `pip install --user <pkg>` or `npx -y <pkg>`. Registries are always reachable.
3. `apt-get install -y <pkg>`, if apt works in this environment (it may need root or may be slow).
4. An official static binary from the project's GitHub releases, into `~/.local/bin`.
5. Another tool for the same job. Already present in the cloud: `ffmpeg`, `pandoc`, ImageMagick 6 (`convert`, with webp), Pillow,
   LibreOffice (`soffice --headless --convert-to`), node 22, python3, Playwright Chromium (`/opt/pw-browsers/chromium`),
   yt-dlp, deno, curl_cffi.
6. Write the small script yourself (Python standard library first).

## 5. A file format nobody handles

- Documents: `pandoc`, or `soffice --headless --convert-to pdf|docx|xlsx <FILE>`. There are also the
  `docx` / `pdf` / `pptx` / `xlsx` skills.
- Images: `convert`, `ffmpeg -i in.png out.webp`, or Pillow (`pip install --user pillow`).
- Media: `ffmpeg -formats` / `ffmpeg -codecs` show what this build supports.
- An unknown binary: run `file <FILE>`, `od -A x -t x1z <FILE> | head`, then look for its magic bytes. It is often
  a zip (try `unzip -l`) or SQLite (read it with Python's built-in `sqlite3` module; the `sqlite3` command may be missing).
- Treat downloaded archives as untrusted: extract them into a new empty folder, and run Python on them with `-I`.

## 6. GitHub: private repos, `gh`, pushes

- A private repo is not visible: in a cloud session, call the `add_repo` tool (owner, repo; `access: push` to write).
  Do not pre-check with curl, because private repos answer 404 to anonymous requests even when they exist.
- `gh` may be inactive in a session: use the `mcp__github__*` tools (load them with `ToolSearch`). `git ls-remote <url>` works for public repos.
- An empty repo answers "This repository is empty" (HTTP 404) on `/contents`, with size 0 and no branches.
- A push is rejected: `git pull --rebase`, then push again. A 403 means the session lacks push access (`add_repo` with push).

## 7. Accounts and services (mail, drive, design, stores)

- Check the connected connectors first (`ListConnectors`, or the deferred tool list): Gmail, Google Drive, Google Calendar,
  Notion, Figma, Canva, Shopify, Vercel, Higgsfield and others may already be there.
- A connector that needs authorization: tell the owner to authorize it in claude.ai, under Settings, then Connectors.
  Never ask for the password.
- No connector: `SearchMcpRegistry` or `SuggestConnectors` for one, the service's official API with a key the owner stores
  themselves (an environment secret, never pasted in chat), or the service's data export.

## 8. Things that only exist on the user's computer

- In a cloud session: `list_computer_folders`, then `request_computer_folder`. The owner approves on their device, and the
  session's commands then run in that folder.
- Otherwise, the owner can open a Local Claude Code session in that folder, or upload the file to this conversation.

## 9. Research when the answer is not in one place

- Search the error text in quotes. Then search GitHub issues for the tool (`site:github.com <tool> <error>`).
- Read the tool's own docs and changelog: the flag may be new or renamed.
- Use the `deep-research` skill, or the `search-first` skill, for multi-source questions. Check the dates on sources.
- Ask a subagent to look in parallel when several directions are open.

## 10. Big, slow or flaky jobs

- Run long commands with `run_in_background` and wait for the notification instead of polling.
- Split the work: process one item, check it, then the rest. Keep partial results, so a failure late in the run loses nothing.
- Writes fail with "no space left": delete build caches and old clones; deletes still work.
- A transfer resets mid-way: check `recentRelayFailures`, then retry with resume (`curl -C -`, `yt-dlp --continue`).
