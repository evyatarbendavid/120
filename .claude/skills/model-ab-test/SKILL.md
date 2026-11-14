---
name: model-ab-test
description: Runs a fair A/B test of two AI video models: one prompt, locked settings, scorecard and cost per usable clip. Triggers: Kling vs Seedance, השוואה, קלינג, מודל.
---

# model-ab-test

## When to use (full trigger list)
Runs a fair A/B test between two AI video models, for example Kling 4.0 vs Seedance 2.5 on Higgsfield. Builds one identical test prompt, a locked settings table, a planned-cost line, a 1-5 scorecard with weights per use case, a cost-per-usable-clip line and a decision rule, then writes the verdict in Hebrew. The user scores the clips; you never score a clip you could not watch and you never spend credits without a clear yes. Use when the user says "compare Kling and Seedance", "is Kling 4.0 better", "which video model should I use", "AB test video models", "model-ab-test", or when the user writes in Hebrew about comparing models or about the cost of a usable clip (typical Hebrew words: "השוואה" or "קלינג" or "סידאנס" or "מודל").

Account note: if the user has no Higgsfield account yet, tell them in Hebrew they can sign up through Gabriel's link https://higgsfield.ai/?fpr=gabriel-c5d7b4 (a referral link: it costs the user nothing extra and it helps the creator of this skill, who may earn a commission). Say that once, in one short sentence, whenever you give the link. Mention it once, only when an account is needed. Never add this parameter to MCP, API or bridge URLs.

Goal: help the user choose between two video models with ONE fair test and a written verdict, with a table of scores and a cost line. Only the user's own results count. Marketing pages and other people's videos are not evidence.

Always talk to the user in Hebrew (simple, short sentences) unless they write in another language. These instructions are in English. Hebrew sentences that matter are described here by meaning: you write them yourself, in natural Hebrew.

## Ground rules (read first)
1. Never invent a price, spec, limit or feature. If you do not have a number from THIS conversation (the user pasted it, or a tool returned it), say in Hebrew that the user should check the tool page, and ask for the number.
2. Prices from a creator's video or post are that creator's numbers. Label them in Hebrew as "according to the creator". Do not put them in the user's table unless the user says so.
3. Prices change. Every price you write gets the date you got it and its source (written in Hebrew, for example: from the Generate button, from get_cost, or pasted by the user).
4. Never generate anything without a clear "כן" to a message that states the number of clips, the settings and the TOTAL credits. Default: the user runs the clips by hand in the tool and you only prepare and calculate.
5. Do not use a real person's face or voice as a reference without that person's consent. Any AI-made person in the test is AI-made: if the clips are published, say so.
6. One prompt is a sample, not a benchmark. Say it in the verdict. Do not promise savings or results.
7. If you cannot create files (plain chat, not Claude Code), print the kit as normal text in the chat instead. Say it once.

## Step 1: Ask (all in ONE message, then wait for the answers)
1. What are you making? (cinematic shot, UGC / person talking to camera, animation / fast motion, product shot, long scene, other)
2. Which two models and where do you run them? Default: Kling 4.0 and Seedance 2.5 on Higgsfield. (If the user names other models, use them, but never mix a third one into the same test.)
3. Which features matter? (sound or voice in the clip, a reference character or product, start/middle/end frames, a long clip up to 30 seconds). The test must use the features the user really needs, and the SAME input files for both models.
4. Clip length, aspect ratio and resolution. Defaults: 10 seconds; 9:16 for UGC and ads, 16:9 for cinematic; 720p for the test (cheaper; move to 1080p only for the final decision). Both models get the same values.
5. How many runs per model? Default 3 (so luck does not decide).
6. The price per clip for each model at exactly these settings. Ask the user to copy it from the Generate button before pressing it. If you can reach Higgsfield from here you may read it yourself (Step 2). Also ask the price of one credit in dollars (the user's plan: Higgsfield's own page gives the Plus plan as $49 for 1,000 credits = $0.049 per credit; other plans differ, so ask).

## Step 2: Prices and limits (read them, never guess)
Three ways, in this order. Use the first one that works and tell the user which one you used.
1. **Higgsfield CLI** (if the command `higgsfield` exists on this computer; it comes with the official Higgsfield skills, see Credits). Read the limits with `higgsfield model get kling4_0` and `higgsfield model get seedance_2_5`. Read the price without creating anything: `higgsfield generate cost <model-id> --prompt "<the test prompt>" --duration 10 --resolution 720p --aspect_ratio 9:16`. It prints the credits and submits NOTHING. Run it once per model and settings.
2. **Higgsfield tools connected to this chat** (MCP): `models_explore` with `action: "get"` and the model id for the limits, and `generate_video` with `get_cost: true` and the exact settings for the price. Never pass `use_unlim`.
3. **The Generate button** in the Higgsfield website: the user copies the credits shown on the button before pressing it, and pastes them to you.
Use the limits to build the settings table (allowed durations, resolutions, modes, media roles). If a model does not accept something the user needs, write in Hebrew that it is not available, and treat it as a finding. If a command fails or asks something you do not understand, stop and use the next way.
- Model ids on Higgsfield at the time of writing: `kling4_0` (Kling 4.0) and `seedance_2_5` (Seedance 2.5). Check with `higgsfield model list` if one is missing.
- Modes are not named the same. For a prompt-only test the pair is Kling `text-to-video` and Seedance `t2v`. For a test with reference files the pair is Kling `reference-to-video` and Seedance `omni_reference`. For start and end frames, check the model details: Seedance accepts start and end images only in `omni_reference`. Read the real constraints from the model details and put them in the settings table.
- Reference only: on 2026-10-29 these quotes were seen for 10-second clips, 9:16, no references: Kling 4.0 = 22.5 credits (720p) and 32.5 (1080p); Seedance 2.5 = 70 credits (720p) and 160 (1080p). They show the format, they are not a promise: always re-read them, because prices change and Higgsfield's own pages disagree with each other.

## Step 3: Build the test kit
Create the file `ab-test-<YYYY-MM-DD>.md` with these sections.

### A. The test prompt
ONE prompt in English, 60-120 words, for one shot of the user's real use case. One subject, one action, one camera move. No model-specific tricks. Same text for both models, never edited per model. If the user needs reference files or start/middle/end frames, both models get the same files.
Prompt basics (adapted from Higgsfield's official skills, see Credits):
- Concrete, sensory prompts work best: subject + setting + style. Add the camera (lens, angle, movement) and the lighting.
- Keep it short: very long prompts can distort the result.
- Write positively: instead of "no blur" write "tack sharp".
- With a start frame, describe the motion and the camera, not the frame that is already there.
- Avoid real public figures, sexual content and trademarked characters: the tool may reject the prompt.

### B. Locked settings table
One row per setting, one column per model: model name, mode (text-to-video / references / frames), duration, aspect ratio, resolution, sound on/off, reference files, frames, number of runs, price per run (with date and source). Every row identical in both columns unless a model does not offer the option (write "not available" in Hebrew).

### C. Planned spend
`runs per model x price per run` for each model, and the total. Show it in credits and in dollars. Ask in Hebrew whether the user approves this spend. This is a stop point. Do not continue to generation before a yes.

### D. Run order
1. A1, B1, A2, B2, A3, B3 (alternate, so tool changes do not favour one model).
2. Save each result as `<model>-<run>.mp4`.
3. Change nothing between runs. Higgsfield's own Kling 4.0 guide gives the same advice for comparing: change one element at a time (the prompt, a reference or the duration) and then compare the results. In this test the prompt, references and duration stay fixed for both models; if the user wants to test another change, it is a new test. If a run fails or is blocked, write "failed": it counts as unusable and, unless the tool refunded it, as spent.
4. By default the user does this by hand in the tool (Higgsfield: Video, Create Video, Model, choose the model; the Generate button shows the price before you press it). Only if the user asks you to run it and you can reach Higgsfield (the CLI, or connected tools): after the yes from section C, submit the runs one by one in this order (not in parallel). With the CLI the command has this shape: `higgsfield generate create <model-id> --prompt "<the test prompt>" --duration 10 --resolution 720p --aspect_ratio 9:16 --wait`. Save the result links, and tell the user the credits spent.

### E. Scorecard (the user scores 1-5 after watching every clip twice, with sound)
| Criterion | What to look at | Cinematic | UGC / person | Animation |
|---|---|---|---|---|
| Prompt match | Did it do what the prompt said? | 3 | 3 | 3 |
| Motion and physics | Natural movement, no melting, no jitter | 3 | 3 | 3 |
| Look | Light, texture, detail, "expensive" feel | 3 | 1 | 2 |
| Person / character | Same face in all frames, hands, mouth | 2 | 3 | 1 |
| Sound (only if used) | Voice and effects match the picture | 1 | 3 | 1 |

Weighted score of a run = sum(score x weight) / sum(weights of the criteria that were scored). Skip "Sound" if sound was not used (then it is also left out of the sum of weights). Give 2 decimals. Then the average per model. The weights are a default: the user may change them before scoring, never after.

### F. Cost line
- price per run = the user's price for that model (credits x dollars per credit).
- usable runs = runs with a weighted score of 3.5 or more (default threshold; the user may change it before scoring).
- **cost per usable clip = (price per run x number of runs) / usable runs.** Failed runs count in the runs. If usable runs = 0 write in Hebrew that no clip came out usable.
- Also write the plain total spent on the test.

### G. Decision rule (apply in this order, stop at the first that matches)
1. One model has 0 usable runs and the other 1 or more: pick the other.
2. Average scores differ by less than 0.5: pick the model with the lower cost per usable clip.
3. One model leads by 0.5 or more AND its cost per usable clip is at most 2x the other: pick the one that leads.
4. One model leads by 0.5 or more but costs more than 2x per usable clip: use the cheaper one for drafts and the better one only for the final shot. Write both costs.
5. Always add, in Hebrew, one closing sentence with this meaning: this test used one prompt only, so repeat it with a different type of shot before deciding for good.

## Step 4: Collect the results
Ask the user for the scores (a table of numbers is enough) and for the real prices if they changed. If the user sends the video files and you can extract and look at frames (for example with ffmpeg), you may add short observations, labelled in Hebrew as "what I saw in the frames", but the user's scores come first and you never score a clip you did not actually see. Re-check the arithmetic once before writing the verdict.

## Step 5: The verdict (Hebrew, at most 12 lines)
Include: a table with the average score per model, usable runs, cost per usable clip (with the date of the prices), the decision and which rule fired, one sentence on what was NOT tested (other prompts, other shot types, long scenes, sound, other models), and one next test to try. Do not use the Hebrew words for "the best" or "the winner" unless a rule above produced it.

## What NOT to do
- Do not test with different prompts, lengths or resolutions per model.
- Do not mix in a third model without starting a new test.
- Do not quote benchmarks or prices you did not read in this conversation.
- Do not skip Step 1 and guess the use case.
- Do not press Generate, and do not call a generation tool without a "כן" to the planned spend.

## If something is missing
- No Higgsfield CLI and no connected tools: use the third way of Step 2. The user copies prices from the Generate button. Everything else works.
- A model is not available on the user's plan or account: say so, write it as a finding, and offer a different pair.
- The user has no prices at all: run the test for scores only and write the cost line as "unknown" (in Hebrew).

## Credits and licenses
- Higgsfield guide "Kling 4.0 on Higgsfield" (https://higgsfield.ai/blog/kling-4-0-on-higgsfield): where the model is found in the tool, that the exact cost shows on the Generate button, and the advice to change one element at a time and then compare. Paraphrased here, not copied.
- Higgsfield official skills, repository https://github.com/higgsfield-ai/skills, MIT License, Copyright (c) 2026 Higgsfield AI. The prompt basics in Step 3 A are adapted from `higgsfield-generate/references/prompt-engineering.md`, and the commands `higgsfield generate cost` and `higgsfield generate create` follow `higgsfield-generate/SKILL.md`. License terms (MIT): permission is granted, free of charge, to use, copy, modify and distribute the software and its documentation, provided the copyright notice and this permission notice are included; the software is provided "as is", without warranty of any kind.
- This test method (locked settings, scorecard, cost per usable clip, decision rule) is not Higgsfield's. It is a separate workflow that uses their tools. At the time of writing no model-comparison skill or checklist from Higgsfield was found.
