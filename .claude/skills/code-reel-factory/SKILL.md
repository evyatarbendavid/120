---
name: code-reel-factory
description: Plans and renders a vertical reel built from code with HyperFrames: script, voiceover, scenes, checks. Triggers: code reel, HyperFrames, מפעל, ריל.
---

# code-reel-factory

## When to use (full trigger list)
Plan and build a short vertical reel (9:16) with CODE instead of an AI video model, rendered by HyperFrames (HTML to video). From one line of topic it asks a few questions, writes a script, prepares the voiceover and word timing, lists the scenes, builds the composition, scores and fixes its own weak moments, and renders a draft and then the final file. Use when the user says the Hebrew word "ריל" with a topic and the word "מקוד" or "מפעל", "code reel", "reel with HyperFrames", "make a reel programmatically", "reel from code", or gives one line about a reel topic and wants a rendered video without a video-generation model.

You turn one line of topic into a short vertical video (1080x1920) that is built from HTML, CSS and animation code and rendered by HyperFrames. No AI video model is used.

Idea source: a reel by Adilet (adilet.fndr) showing a Claude skill that, from one typed line, writes the script, records the voiceover, animates each scene, scores its own motion and renders the file. His own skill is a paid product (per his public page, adiletfndr.com) and it was not used, copied or seen. You do NOT know how his system is built. This skill is an independent, simpler workflow built from what his reel shows and on the official HyperFrames skills (HeyGen, Apache-2.0, github.com/heygen-com/hyperframes). Never say or imply that it is his system or that it gives his results.

Always talk to the user in Hebrew unless they write in another language. Use simple Hebrew, short sentences, no jargon without a one-line explanation. These instructions are in English.

## Division of work

- This skill owns the editorial part: questions, script, voice and timing, scene list, self-check rubric, approvals.
- The HyperFrames skills own the technical part: composition structure, `data-*` timing attributes, validation, preview and render. When you build, load `/hyperframes` (or `/hyperframes:hyperframes` when it was installed as a plugin) and follow it. Do not write composition HTML from memory.
- Anything you cannot do or verify, you say in one plain sentence. You never pretend a step worked.

## Step 0: Preflight (report in 4 short lines, then continue or stop)

1. `node --version` must be 22 or newer.
2. `ffmpeg -version` must work.
3. `npx hyperframes doctor` : read the list. Missing Chrome is fixed by the doctor's own hint. `whisper-cpp` is needed only for transcription (see Step 4).
4. HyperFrames skills: if `/hyperframes` is not available in this session, run `npx hyperframes skills update`, then tell the user to close and reopen Claude Code and run this skill again. If that command fails, show the error. Do not reconstruct the HyperFrames rules from memory.

If something is missing: say what, give the one plain fix, stop.

## Step 1: Ask (one message, then wait)

1. The topic line, for example "why IKEA makes you walk through the whole store", OR a finished script that the user pastes. A pasted script skips the writing in Step 3 but is still shown for approval and checked for facts and length.
2. Language of the voice and of the captions: Hebrew, English or other. Never assume.
3. Length: 30 to 45 seconds unless the user says otherwise.
4. Style in one line, or offer three: (a) clean light cards, (b) dark and bold, (c) illustrated and playful.
5. Voice: (a) the user's own recording, (b) a generated voice, (c) no voice, text and music only. For (b) go to Step 4, "Voice options".
6. Optional: up to three reels the user likes. Use them only to learn pace (cut speed, caption size, how fast the hook lands). Never copy their text, footage or designs.
7. Optional: a folder with the user's own logo, colors or footage to use.

Create a planning folder `reel-plans/<slug>/` (slug = short English name). Save the answers in `reel-plans/<slug>/answers.md`. Keep `reel-plans/<slug>/progress.md` with one line per finished step. At the start of every run, if a progress file exists, ask in Hebrew whether to resume from the first unfinished step. The HyperFrames project is created later (Step 6) in a separate folder, because `hyperframes init` needs an empty folder.

## Step 2: Style kit (short, reusable)

Keep one file `reel-kit/style.md` that every future reel starts from. If it does not exist, create it from the answers; if it exists, read it first and ask only what changed. It holds:
- Hook patterns that fit the user (for example: a question about a daily annoyance, a surprising number the user can verify, a before and after).
- Pacing rules (for example: a new visual every 2 to 3 seconds, hook inside the first 3 seconds).
- Caption style (font size, position, how many words at a time, highlight color).
- Colors and fonts. Hebrew needs a font that has Hebrew letters; say which one you chose.
Also keep a folder `reel-kit/scenes/` with reusable scenes (title card, number counter, list reveal, diagram) saved as HTML files after a reel is approved. The next reel starts from these.
Derive style from the user's own material and the three reels' pace only. Do not copy any creator's library.

## Step 3: Script (approval gate)

- Spoken lines, one breath per line. About 2.3 words per second in Hebrew or English; compute the target word count from the length.
- Seconds 0 to 3: a clear hook that names the viewer's pain or curiosity. Within the next 5 seconds: one concrete example.
- Facts only from what the user gave or what you can verify with a source. Put [לבדוק] after anything unverified, and list those at the end.
- No promises about views, followers or money.
- If the voice will be generated, add one line to the post text saying, in Hebrew, that the voice was generated by AI. Write that sentence in Hebrew yourself.
Show the script. Ask in Hebrew whether the user approves it or wants a change (a yes, or what to fix). Continue only after a clear yes. A bare "ok" about something else is not a yes.
Save as `reel-plans/<slug>/script.md`.

## Step 4: Voice and timing

### Voice options (check, do not assume)
- Own recording: always works. Ask for a quiet room, a phone is fine. Save as `voice.wav` or `voice.mp3`.
- Hebrew generated voice. The built-in local voice of HyperFrames (`npx hyperframes tts`, Kokoro) has NO Hebrew voice: its languages are English, Spanish, French, Hindi, Italian, Japanese, Portuguese (Brazil) and Mandarin. Do not use it for Hebrew.
  Providers whose official pages list Hebrew: ElevenLabs only with the models Eleven v3 or v4 (Multilingual v2 and Flash v2.5 do not list Hebrew), Cartesia Sonic 3.6, Google Gemini 3.8 Flash TTS (the HyperFrames audio engine supports it with `provider: "gemini"` and a `GEMINI_API_KEY`). Each needs the user's own account or key. Ask which one the user has. Never ask the user to paste a key into the chat: tell them to put it in an environment variable or a `.env` file that you do not read aloud.
  You cannot judge how natural a Hebrew voice sounds. Generate one 5-second test line, give the user the file, and ask in Hebrew whether it sounds natural. If not, offer another provider or an own recording.
- English generated voice: `npx hyperframes tts "<text>" --voice af_heart -o voice.wav` works locally with no account. Run `npx hyperframes tts --list` for the voices.
- Never clone a real person's voice without that person's written consent. Never present a generated voice as a real person.

### Make or receive the audio
- Check that the file plays, and compare its length to the script (`ffprobe -v error -show_entries format=duration -of csv=p=0 voice.wav`). Off by more than 15 percent: fix the script or ask for a new take.

### Word timing for captions
- `npx hyperframes transcribe voice.wav --language he --model small` (use `--model medium` or `large-v3` if the result is poor; for English use `--language en`). The default model is English only, so always pass the language for Hebrew.
- It may need whisper.cpp. If `doctor` said it is missing, run the command anyway and read its own message; tell the user in one sentence what is missing. If transcription cannot run, ask the user for an .srt or .vtt file with word or line timing (the transcribe command can import both), or use a text-to-speech provider that returns word timestamps.
- Save the word list as `words.json`.
- Always compare the transcript to the approved script. Replace misspelled words with the script's words. For Hebrew, read the corrected caption lines back to the user before building.

## Step 5: Scene list (approval gate)

Make a table: scene # | start-end (seconds, from the real audio) | spoken line | what is on screen | motion | big text (max 3 words) | source of any number.
Rules:
- Something moves in every scene. Nothing static for more than 2 seconds.
- Frame 0 already shows the title or the key image (the first frame is the thumbnail on social players).
- One idea per scene. Captions follow the words; big text is separate and short.
- Keep important things away from the top 10 percent and the bottom 20 percent of the frame (app buttons cover them).
- Reuse scenes from `reel-kit/scenes/` when they fit.
Show the table. Ask for approval. Save as `reel-plans/<slug>/scenes.md`.

## Step 6: Build with HyperFrames

1. Create the project in an empty folder: `npx hyperframes init videos/<slug> --non-interactive --example=blank`.
2. Write `BRIEF.md` in the project root, as the first action after init, so HyperFrames asks no brief questions again:
   - frontmatter: `workflow: faceless-explainer`, `flow: automation`, `storyboard: no`, `message: "<one sentence>"`, `aspect: 1080x1920`, `language: he` (or `en`), `length: <seconds>s`
   - body: `## Intent` (the topic and the style in the user's words), `## Assets` (the voice file, `words.json`, any logo or footage, one line each), `## Notes` (the approved script is locked, scene list is approved, captions are word by word from `words.json`).
   Copy the approved script to `SCRIPT.md` and the audio and `words.json` into the project. Tell HyperFrames that the script, the audio and the scene table are already approved and must be used as they are.
3. Load `/hyperframes` and build the composition from the approved scene table. The canvas is `data-width="1080" data-height="1920"` on the root. Prefer ready blocks when they fit (`npx hyperframes catalog --query "<what you need, in English>"`, then `npx hyperframes add <name>`).
4. Hebrew: set `<html lang="he" dir="rtl">`, use a font with Hebrew letters, and check punctuation, numbers and English words inside Hebrew lines. (A vertical Hebrew test render with `dir="rtl"` came out in the right order.)

## Step 7: Self-check (before the user sees anything)

1. `npx hyperframes check`. Fix every error. List every warning you did not fix and why. A `first_frame_empty` warning means frame 0 is blank: fix it.
2. Look at the scenes: `npx hyperframes snapshot --at <middle of each scene, comma separated>` then open the images. Fix overlaps, cut-off text, missing fonts, text that a phone screen would not show.
3. Score the motion 0 to 10 with this rubric and write the score, the reasons and the fixes in `self-check.md`: every scene moves (3 points), no static stretch over 2 seconds (2), captions match the voice (2), text readable on a phone (2), no overlaps or cut-off text (1). This is your own simple rubric. It is not an official metric and not the score of any creator. Fix what lost points and score again, at most 3 rounds. Then tell the user, in plain words, what is still weak.
4. Do not say it is good because the score is high. Say what you checked and what you could not check (for example, how the Hebrew voice sounds).

## Step 8: Preview, draft, final

- `npx hyperframes preview --background`. Give the user the local address and ask in Hebrew whether to change something or to render now. Stop it later with `npx hyperframes preview --stop`.
- Draft: `npx hyperframes render --quality draft --output draft.mp4`. Check the file is not empty and its duration matches the voice.
- Only after a clear yes on the draft: `npx hyperframes render --quality delivery --output final.mp4`.
- Never upload or publish anything. Tell the user where the files are.
- After approval, save the reusable scenes into `reel-kit/scenes/` and update `reel-kit/style.md` with what worked.

## Rules

- Wait for a clear yes at the script and at the scene list. If the user says "just do it", you may combine the two approvals into one, but never skip the question before the final render.
- Never claim the reel will go viral, get followers or earn money. Never invent numbers, quotes or sources.
- Do not copy another creator's script, footage, designs or scene library.
- Mark AI-generated voices and AI-generated characters as AI in the post text.
- Final message in Hebrew: where the file is, its length, a one-line description of each scene, the self-check score with reasons, what is unverified, and one suggestion for the next reel.
