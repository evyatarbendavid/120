---
name: ig-account-insights
description: Analyze the owner's own Instagram account privately and safely - followers, posts and reels with their reach, views, saves and shares, best and worst performers, posting rhythm, audience, and who does not follow back - through Meta's official read-only API or through the account's own data export. Never uses a password or an unofficial login. Use when the user asks to analyze their Instagram account, "what works on my account", "my insights", "my best reels", "who unfollowed me", "who doesn't follow me back", or in Hebrew "תנתח לי את האינסטגרם", "הנתונים של החשבון שלי", "מה עובד אצלי", "מי לא עוקב בחזרה". Pair with ig-audit for the content verdict and ig-plan for what to post next.
license: MIT
---

# Instagram account insights

Written for this repository. Two safe routes into the owner's own account. Pick the first one the
user has set up; if neither is set up, explain both in plain Hebrew and let them choose.

## Safety rules (always)

- Never ask for, accept or store an Instagram password, and never use unofficial login libraries
  (instaloader, instagrapi and the like). They break Instagram's terms and can get the account locked.
- Never ask the user to paste a token into the chat. If they paste one anyway, do not repeat it, tell
  them to revoke it in Meta's dashboard and make a new one.
- Read only. Nothing here posts, likes, follows, comments or sends messages.
- Keep all downloaded data in a scratchpad or temp folder, never inside a git repository.
- Direct messages are private: do not open them unless the user explicitly asks.

## Route A: official API (live numbers, best for ongoing work)

Needs, once: a Professional account (Creator or Business, free: Instagram > Settings > Account type
and tools) and a token from a free Meta developer app with the permissions
`instagram_business_basic` and `instagram_business_manage_insights` (Meta's "Instagram API with
Instagram login"). Walk the user through it step by step when they ask; the token lasts about 60 days.

Where the token goes (never the chat):
- On their own computer: the file `~/.config/ig-account-insights/token` (create the folder, save the
  token as the only line, `chmod 600` on Mac/Linux), or the environment variable `IG_ACCESS_TOKEN`.
- In cloud sessions: the environment's settings, as the variable `IG_ACCESS_TOKEN`. Tell the user that
  environment variables there are visible to anyone who can edit that environment, so the token must
  be read-only and they can revoke it any time.
- The domain `graph.instagram.com` must be allowed in the environment's network settings.

Commands (from this skill's folder, output into a scratchpad folder):
1. `python3 scripts/ig_api.py check` - confirms the token and the account, without printing the token.
2. `python3 scripts/ig_api.py profile --out <dir>`
3. `python3 scripts/ig_api.py media --out <dir> --limit 50 --insights` - each post and reel with reach,
   views, likes, comments, shares, saves and, for reels, average watch time.
4. `python3 scripts/ig_api.py account --out <dir> --days 28` - daily reach, views, interactions,
   follows and unfollows, and follower demographics.

## Route B: the account's own data export (no developer setup at all)

Instagram > Settings > Accounts Center > Your information and permissions > Download your information >
choose the account, **JSON** format, the date range, and the categories they want (followers and
following, content, interactions). The file arrives by email within minutes to hours. The user then
attaches the zip to the chat; it lands in `~/.claude/uploads/<session>/`.

`python3 scripts/ig_export.py <zip> --out <dir>` unpacks it safely, skips direct messages, and writes
`summary.json`: followers, following, who they follow that does not follow back (and the reverse),
posts, reels and stories per month, comments and likes they gave per month. The export has no reach or
view counts; for those, Route A or screenshots of Professional dashboard insights.

## Analysis

From whatever data you have, answer in Hebrew with numbers and examples, not generalities:
- Top 5 and bottom 5 posts by reach and by saves plus shares, with what they have in common (format,
  length, topic, hook, posting time). Link each with its permalink.
- Posting rhythm against results: which days, times and frequency did best.
- Reels: average watch time against length; where people likely drop.
- Followers: growth per week, follows against unfollows, and the not-following-back list on request.
- Three concrete next steps. Hand content work to `ig-reel`, `ig-plan` and `ig-audit` if useful.

Say plainly which numbers came from the API, which from the export, and what is missing.
