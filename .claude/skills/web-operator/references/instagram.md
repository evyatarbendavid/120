# Instagram with the work account

## Read (no login)
Any public post, reel or profile: `open-social-link`. The account's own numbers: `ig-account-insights`.

## One-time setup (only when the owner wants to post; guide in Hebrew, one step at a time)
1. The work account is an Instagram **professional (Business)** account. API publishing does not work on
   personal accounts, and Meta's docs say Reels publishing needs Business.
2. Meta for Developers: create an app, add **Instagram API with Instagram Login**, permissions
   `instagram_business_basic` and `instagram_business_content_publish`, generate a token for the work account.
3. Call `request_credential` (host `graph.instagram.com`, Authorization, Bearer); the owner pastes the token in
   the form. Check: `python3 <skill>/scripts/ig_publish.py whoami`. (Local session without the form: the owner
   puts it in `~/.config/ig-account-insights/token` themselves; never through chat.)

## Every post
1. Media must be at a public https URL (Instagram downloads it): the owner's own public place (a public GitHub
   repo's raw link, their site). Only media meant to be public.
2. `ig_publish.py prepare` with `--image-url URL` (photo), `--video-url URL [--cover-url URL] [--no-feed]` (reel),
   or `--carousel URL URL ...` (2-10), and `--caption "..."` (max 2,200 chars). `--ai-label` for AI-made media.
   This builds the post WITHOUT publishing it.
3. Check the caption and image for personal details (SKILL.md section 3), then ask with `AskUserQuestion`:
   "לפרסם?" with the exact media and caption. "I approve everything" means ask fast, not skip: a public post
   cannot be unsaid.
4. On a yes: `ig_publish.py publish <container_id>`; report the permalink. `ig_publish.py limit` = 24 h quota
   (Meta: 100 API posts a day). A container in ERROR means Instagram could not process the media: check the
   format (JPEG photo; MP4/H.264 reel, 9:16, 3-90 s) and the URL.

## Not done (bans the account, breaks Instagram's terms)
Automated follow/unfollow, mass likes or comments, mass DMs, scraping other people's followers, buying
engagement. Replies and DMs are drafted for the owner to send (`ig-reply`, `ig-dm`, `ig-comment`).

## Other platforms, same pattern (official API + credential form + a yes per post)
Facebook Pages (`graph.facebook.com`, `ig_publish.py --host graph.facebook.com` for IG via Facebook Login),
YouTube (Data API), TikTok (Content Posting API, needs app approval), Shopify (connector, drafts). Check
`ListConnectors` first: a connected service needs no token.

## Browse Instagram signed in (the owner's own browser)
Instagram shows almost nothing to a logged-out cloud browser (login wall, 429). To browse signed in, use a browser the
owner signed into THEMSELVES; never type their password, never copy their cookies or session into the cloud.
- Claude in Chrome (their real Chrome, existing sign-ins): a Local Claude Code session started with `claude --chrome`,
  or Cowork, with the extension connected. Read the `chrome-browser` skill first.
- The desktop app's built-in browser: Cowork, or a session linked to their computer. Read `built-in-browser` first;
  the owner signs in once in the pane and the sign-in persists.
Rules while signed in: read and browse only. Every like, follow, comment, DM, story reply, post or setting change
needs the owner's yes for that exact action. Human pace (a few pages a minute, no bulk scrolling or mass profile
visits), no scraping lists of other people's followers, no personal details out. Prefer the work account.
