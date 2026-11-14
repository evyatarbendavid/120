---
name: prompt-remix
description: Turns a prompt from a public prompt library into the user's own project, keeping the structure and crediting the creator. Triggers: remix prompt, מאגר, פרומפט.
---

# prompt-remix

## When to use (full trigger list)
Takes a reference prompt from a public prompt library (for example the GitHub repo yihui-dev/awesome-opus5-5-videos, its data/videos.json, or any "prompts" folder) and remixes it into the user's own project. It keeps the structure that made the original work, swaps all the content, removes the original creator's identity, and writes a credit line to the creator. It can also search the library for a prompt that fits the user's topic. Use when the user says "remix this prompt", "adapt this prompt to my project", "I found a prompt I like", "find me a prompt for ...", "search the prompts repo", or when the user writes in Hebrew about a prompt (פרומפט) or the repo (מאגר) and asks to adapt it (תתאים) or to search it (תחפש).

A reference prompt is a skeleton plus content. Keep the skeleton, replace the content, so the user does not start from zero and does not copy anyone.
Every video and prompt in a public library belongs to its creator (the repo README says so). A repo license such as MIT covers the repo itself, not a promise that you may republish someone's prompt as your own. So the result must be clearly new, and must credit the source.

Language: always talk to the user in Hebrew unless they write in another language. The remixed prompt itself stays in the language of the source prompt (usually English), unless the user asks otherwise.

## Sources this skill builds on (credit; keep this section)

- The repo README, https://github.com/yihui-dev/awesome-opus5-5-videos (MIT License, copyright 2026 yihui-dev). Its "How to use a prompt" steps are quoted in Step 5, and its credits rule is the reason this skill exists. The README says: "Every video and prompt belongs to its creator, linked from each entry."
- prompt-motion.com (curated by @p4nthera_), the free "Customize a prompt" tool: it adapts a prompt from four inputs (what the video is for, its format, its colors, anything else), and the prompt structure it shows (inputs, direction with a Banned list, structure, build, gotchas, start). Step 0 and Step 1 use the same ideas. Prompts there belong to their creators; nothing is copied from them.
- Skillry (skillry.dev) offers its own skills ("Make videos like this with your agent"). They need an account and its terms do not allow redistribution, so nothing from them is copied here.
- This skill is a rewrite for Hebrew-speaking creators. It is not an official skill of yihui-dev, Skillry or prompt-motion.

## Facts about the library (check them again if the user's copy looks different)

- Repo: github.com/yihui-dev/awesome-opus5-5-videos (MIT license, copyright yihui-dev).
- `prompts/` has one `.md` file per entry, named `<author>-<number>.md`. Inside: the author handle, the category, the tech the remake used, a link to the original post, and a `## Prompt` heading followed by one code block.
- `data/videos.json` holds all entries in one file. Fields: `slug`, `author`, `author_url`, `post_url`, `category` (`motion`, `3d`, `explainer`, `interactive`), `tech_tags` (for example `canvas`, `svg`, `threejs`, `gsap`, `shader`, `audio`), `prompt`, `prompt_partial`, `poster_url`, `skillry_url`, `added`, `has_remake`.
- `prompt_partial: true` means the creator shared only part of the prompt or only described the result. A partial prompt is a hint, not a full recipe.
- Prompts vary a lot: from one short line to long structured prompts with blocks such as `<inputs>`, `<direction>`, `<structure>`, `<build>`, `<gotchas>`, `<start>`.
- The prompts were written for Claude Opus 5.5. They may run differently on another model.

## Mode A - Find a prompt (when the user has no prompt yet)

1. Ask three short questions: what do you want to make (topic), what format (vertical video, website animation, explainer, 3D scene, small game), and what feeling or style. One question per line, wait for the answers.
2. Find the library on the computer. Look for a folder named `awesome-opus5-5-videos`, or any folder that has `data/videos.json`.
   - If it exists: search `data/videos.json` (not the `prompts/` folder first, because the JSON has the category and tags). Use a short script or grep: filter by `category` and `tech_tags`, then look for 3 to 5 keywords from the user's topic inside `prompt` (case-insensitive). Prefer entries with `prompt_partial: false`. Open the 3 best matches.
   - If it does not exist: tell the user two ways, and wait. (a) Download the ZIP from the repo page (green Code button, then Download ZIP), unzip it, and tell you the folder path. (b) Open the repo page, find a video they like, open its Prompt file, and paste the prompt text into the chat. Do not guess prompt text from memory. Do not invent what the library contains.
3. Show 3 candidates, one line each: what it makes, which tech it uses, whether the prompt is complete or partial, why it fits. Let the user pick one. Then go to Mode B.
4. If nothing fits, say so honestly and offer to search again with other words.

## Mode B - Remix (the main job)

### Step 0 - Collect
Ask for what is missing (one short question per missing item, never invent):
1. The source prompt (pasted text, or a file path), and where it came from: repo, file name, creator handle, link to the original post (for the credit).
2. The user's project, with the same four inputs the free Customize tool on prompt-motion.com uses: what the video is for (topic or business name, audience), its format, its colors, and anything else (text that must appear, language of the text; Hebrew is right-to-left, say so).
3. The output they want: same type as the source (for example one HTML animation file), or another.
4. Length or aspect ratio, if relevant.

If the source prompt has an `<inputs>` block (it asks the user for things), answer those items yourself from the user's project and tell the user which ones you answered.

### Step 1 - Dissect
If the source prompt is built from blocks, map them to the slots: `<inputs>` is what the prompt asks the user for; `<direction>` is style, format and the Banned list; `<structure>` is scenes and timing; `<build>` is the tech and constraints; `<gotchas>` is the pitfalls to keep; `<start>` is the order of work (ask first, plan, then build). Keep the same blocks in the remix.
Show a table: `Slot | What the source says`. Slots: Goal and format; Tech or tools named; Structure (scenes, order, timing); Motion and camera; Visual style; Content (text, numbers, names, characters, slogans); Constraints (duration, resolution, "single file", "no external images").

### Step 2 - Decide per slot, then STOP for approval
Mark each slot:
- KEEP: structure, order, timing, motion style, tech choices, constraints that make it work.
- SWAP: all content, brand, copy, colors, subject. Use the user's real details.
- DROP: anything that identifies the creator or a third party: handles, names, logos, slogans, unique characters, a real famous product used as the subject. If the prompt tells the model to fetch a real company's pages, logos or images from the internet, DROP that and use the user's own subject and their own assets, or simple drawn shapes.

Show the KEEP / SWAP / DROP list in a few lines and ask, in Hebrew, whether the user approves or wants to change something. Wait for the answer before writing the prompt.

### Step 3 - Write the remixed prompt
- Same skeleton and same order of blocks as the source, new content everywhere.
- Fill every slot with something concrete. If a fact or number is unknown, write `[FILL: what is needed]` and list it at the end. Never invent prices, statistics, customer numbers, opening hours or testimonials for the user's business.
- Do not copy sentences from the source longer than a short phrase. Rewrite in your own words.
- If the source is partial (`prompt_partial: true`), say clearly which parts you completed yourself, and mark them `(added by remix)`.

### Step 4 - Check yourself (silently, fix before showing)
No leftover names, handles or slogans from the source. Every slot is filled or marked `[FILL]`. The prompt can be pasted and run in one go. Length is reasonable. Nothing in it asks for copyrighted material or for a real person's face or voice.

### Step 5 - Deliver, exactly these parts
1. The remixed prompt in one code block.
2. A short list of 3 to 5 lines under three headings (kept, changed, dropped). Write the headings in Hebrew.
3. A credit line the user can paste into the post or the file, with the creator's handle and the original post link: `Prompt structure inspired by @<handle> (<post link>), from the awesome-opus5-5-videos list. Remixed and rewritten.` In Hebrew if the post is in Hebrew.
4. The `[FILL]` list, if any.
5. How to run it. For a prompt that writes the animation as code, use the repo's own three steps, quoted from its README: "1. Open a prompt file and copy the block under **Prompt**. 2. Paste it into Claude Opus 5.5 (Claude Code, the Claude app, or any agent running Opus 5.5). 3. Ask it to render the result as a single HTML file, then record the page if you want a video." Adapt step 1 to the remixed prompt you just wrote. If the type is a video model: say which inputs to attach and to test one short clip first.

Offer one variant ("bolder" or "safer") only if the user asks.

## When something is missing
- No access to the library and the user cannot paste: say so, and give the two ways from Mode A. Do not continue with invented text.
- The pasted prompt looks cut off: ask if the creator shared only part of it, and continue only after the user confirms.
- The user has no project details yet: ask for the three basics (topic, audience, one color). If they say they do not know, write `[FILL]` and move on.

## Do NOT
- Do not present a remix as your own original without the credit line.
- Do not copy a prompt word for word and only change the name.
- Do not keep the creator's handle, logo, slogan or characters inside the prompt (the handle belongs only in the credit line).
- Do not claim things about the user's business that the user did not give you.
- Do not guess what a library contains. If you cannot read it, say so and ask the user to paste.
- Do not promise views, virality or income.
