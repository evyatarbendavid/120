---
name: skill-router
description: Use FIRST when asked to build, create, make, design, write, edit or produce something non-trivial (site, app, video, reel, logo, bot, campaign, document, code) or "which skill fits": splits the task into its needs and picks the right installed skills per need. תבנה, תיצור, תעשה לי, תכין, תעצב, איזה סקיל מתאים. Searches every skill and agent installed now (repo, ~/.claude, account, plugins).
license: MIT
---

# Skill router

Written for this repository. Hundreds of skills and agents are installed; this makes sure the right
ones are used for each request instead of whichever one happens to come to mind.

## When to route, and when not

Route any request that produces something: a page, an app, a video, a design, a document, a campaign,
a bot, code with more than a few lines. Skip routing for questions, small edits, and one-step tasks,
because the routing would cost more than it saves.

## Steps

1. **Break the task into needs.** One line for the goal (deliverable, who it is for, platform, limits the user stated).
   Then list the 2-5 needs it is made of, in your head or in one line: what is being built or made (a site, an app,
   a video), what it must do (booking, payments, a dashboard), and what comes around it (copy, hosting, SEO, tracking).
   Tell apart the thing to deliver from the topic it is about: a portfolio *website* about video editing is a website,
   not a video.

2. **Search per need** with the bundled script, from the user's project folder (so that project's skills are
   included), by its full path: `<this skill's folder>/scripts/find_skills.py`.
   - `python3 <path>/find_skills.py "<the user's request, as written>" --need "<english keywords for need 1>" --need "<need 2>"`
   The script recognises the usual needs by itself from Hebrew and English phrases (`references/needs.json`) and, for
   each one, shows a team (lead / support / check skills that are installed right now) plus the best matches found by
   searching that need alone. Your `--need` lines cover what it did not recognise, and they are searched on their
   own too, so a skill added yesterday is found. If it printed "none recognised", rerun with `--need` lines.
   Tags after a name, `[key?]`, `[paid?]`, `[own computer?]`, are text hints from that skill's instructions: confirm
   in its `SKILL.md` before warning the user. The last list ("also matched") is weaker; skip it unless one fits.

3. **Choose a small team.** Usually 1 lead skill for the main need, 1 to 3 supporting skills, and an agent only when
   the task benefits from a specialist's review or a separate pass. Prefer:
   - the skill whose description names this exact deliverable over a general one;
   - an entry-point skill when a family has one (`hyperframes` before its sub-skills, `ig-plan` for Instagram planning);
   - skills that hand work to each other (`hallmark` to build, then `avoid-ai-design` to check) over two that overlap;
   - free and local over paid: flag any skill that needs a paid service, an API key, or the user's own computer
     before using it.
   Skills that live in your own skill list but not on disk (marked "built-in", such as `dataviz` or `artifact-design`)
   are used the same way, by name through the Skill tool.

4. **Look closer only when it matters.** If two candidates look equally right, read the first ~40 lines of each
   `SKILL.md` (the path is printed once at the end). For a large build where many candidates compete, and the Agent
   tool exists, send one subagent to read the top candidates and return a ranked recommendation with reasons.

5. **Tell the user, briefly, then start.** In the user's language, a short table in the order the skills will be used,
   marking which one leads. Then load the lead skill with the Skill tool and do the work, bringing in the supporting
   skills at their step. Wait for the user only if they asked for a recommendation alone, or the plan involves money
   or something hard to undo.

## Output format

```
**סקילים לעבודה הזו**
| # | סקיל / סוכן | מוביל / תומך / בדיקה | התפקיד כאן |
|---|---|---|---|
| 1 | `support-skill` | תומך | ... |
| 2 | `lead-skill` | מוביל | ... |
| 3 | `check-skill` | בדיקה | ... |
```
`#` is the order of work. One line under it with anything to watch for: a paid service or key, needs
the user's computer, or a decision only the user can make (for example where a sign-up form sends).

## Notes

- Nothing to maintain for new skills: the script reads the skill folders every time, so a skill added to the repo, to
  `~/.claude/skills`, to the claude.ai account or by a plugin shows up on the next run. To teach it a new kind of
  need, add an entry to `references/needs.json` (phrases, an English query, a lead/support/check team); never remove
  entries the owner uses.
- Measured 2026-11-22 with `scripts/eval_router.py` (recall of the right skills in the first 8 results; old word-match
  router -> need-based router): 0.31 -> 0.96 and 0.33 -> 0.94 on the two sets the catalog was built from, and on three
  sets of new requests written before the fixes 0.32 -> 0.60, 0.21 -> 0.63, 0.28 -> 0.62 (0.93, 0.88, 0.83 after
  the gaps they showed were closed). New phrasings still miss sometimes: that is what your `--need` lines are for.
- Account skills appear in sessions with a prefix (for example `anthropic-skills:docx`); call them by the
  name the Skill tool lists.
- If the script finds nothing relevant, say so and work without a skill rather than forcing a poor match.
- Skills listed by name only (~150 niche ones, see `120/scripts/skill-listing-tiers.json`) are found exactly the
  same way: the script reads every SKILL.md description from disk and never reads the listing settings, so its
  ranking is identical with or without the name-only listing. Their listing text is in
  `references/name-only-skills.md` (written by `scripts/name_only_index.py` at setup) for choosing without the script.
