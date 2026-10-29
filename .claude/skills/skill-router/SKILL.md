---
name: skill-router
description: Pick the best installed skills and agents for a build or creation request before starting the work, then use them. Scans every skill and agent available right now (repo, user folder, claude.ai account, plugins), so newly added skills are included automatically. Use this FIRST whenever the user asks to build, create, make, design, write, edit, produce or plan something non-trivial - a website, landing page, app, dashboard, video, reel, animation, logo, bot, automation, campaign, document, deck or code - and whenever they ask "which skill should I use" or "what fits this". Hebrew triggers - "תבנה", "תיצור", "תעשה לי", "תכין", "תעצב", "תכתוב", "תערוך", "איזה סקיל מתאים", "תבחר סקילים".
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

1. **Pin the goal.** One line: the deliverable, who it is for, the platform or format, and any limit
   the user stated (language, budget, deadline, style).

2. **Search twice** with the bundled script. Run it from the user's project folder (so that project's
   own skills are included) and give its full path: `<this skill's folder>/scripts/find_skills.py`.
   - `python3 <path>/find_skills.py "<the user's request, as written>"`
   - `python3 <path>/find_skills.py "<your own English keywords: deliverable, domain, platform, tech, style>"`
   The script scans every skill and agent installed at this moment and ranks them. It is a shortlist,
   not the answer: keyword scores miss intent (a skill's own description may point elsewhere), so
   you make the final call. Tags after a name, `[key?]`, `[paid?]`, `[own computer?]`, are text hints
   found in that skill's instructions; confirm in its `SKILL.md` before warning the user.

3. **Choose a small team.** Usually 1 lead skill, 1 to 3 supporting skills, and an agent only when the
   task benefits from a specialist's review or a separate pass. Prefer:
   - the skill whose description names this exact deliverable over a general one;
   - an entry-point skill when a family has one (for example `hyperframes` before its sub-skills,
     `ecc-guide` for engineering choices, `ig-reel` for reels);
   - skills that hand work to each other (for example `hallmark` to build, then `avoid-ai-design`
     to check) over two skills that do the same thing;
   - free and local over paid: flag any skill that needs a paid service, an API key, or the user's own
     computer (for example `moneyprinterturbo-video`, `scroll-world`, `fal-ai-media`) before using it.

4. **Look closer only when it matters.** If two candidates look equally right, read the first ~40 lines
   of each `SKILL.md` (the path is in the script's output). For a large build where many candidates
   compete, and the Agent tool exists, send one subagent to read the top candidates and return a ranked
   recommendation with reasons, so the main conversation stays focused.

5. **Tell the user, briefly, then start.** In the user's language, a short table in the order the skills
   will be used, marking which one leads. Then load the lead skill with the Skill tool and do the work, bringing in
   the supporting skills at their step. Wait for the user only if they asked for a recommendation
   alone, or the plan involves money or something hard to undo.

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

- Nothing to maintain: the script reads the skill folders every time, so a skill added to the repo, to
  `~/.claude/skills`, to the claude.ai account or by a plugin shows up on the next run.
- Account skills appear in sessions with a prefix (for example `anthropic-skills:docx`); call them by the
  name the Skill tool lists.
- If the script finds nothing relevant, say so and work without a skill rather than forcing a poor match.
