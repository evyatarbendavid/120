---
name: motion-brief
description: Interviews the user and writes a precise motion-graphics brief for HyperFrames. Triggers: animation brief, motion, מושן, אנימציה, בריף.
---

# motion-brief

## When to use (full trigger list)
Interviews the user with a few questions and writes a precise animation / motion brief (a 5 to 7 second full-screen vertical clip by default), where every adjective becomes a number and every banned default has a replacement. Then it helps build the clip with HyperFrames, check three frames, fix one line at a time, and render an MP4. Use it instead of a vague "make it look nice". Use when the user wants an animation, motion graphic, logo end card, title card, number counter, kinetic text, short vertical video made from code, or says "motion brief", "make it pretty", "the animation came out generic", or writes in Hebrew about an animation (אנימציה), a brief (בריף), or motion (מושן).

Goal: turn a vague wish ("make me a nice animation") into a short, exact brief, then build it from that brief.
Vague words such as "nice", "modern", "smooth", "premium", "cinematic" are not instructions. A model fills every gap with its own defaults, and they look the same in every run. Every adjective you turn into a number is a decision taken back from those defaults.

Language: always talk to the user in Hebrew unless they write in another language. Write the final brief in English (animation tools follow English motion words best), unless the user asks otherwise. Text that must appear on screen is written in the user's language, in quotes, exactly as the user gave it.

## Sources this skill builds on (credit; keep this section)

- HyperFrames skill `references/spec.md` and `references/types/vertical.md`, and the HyperFrames docs pages "Ask for a great video" and "Ask for smooth motion and transitions". By HeyGen, Apache License 2.0. https://github.com/heygen-com/hyperframes . The spec template, the "words to numbers" table, the banned defaults, the composition numbers and the vertical safe band below are adapted from there (shortened and edited for a 5 to 7 second clip).
- prompt-motion.com (curated by @p4nthera_): the structure of its prompts (inputs, direction with a Banned list, structure, build, gotchas, start) and its advice to pair every ban with a replacement. Prompts there belong to their creators; nothing is copied from them.
- This skill is a rewrite for Hebrew-speaking creators. It is not an official HeyGen or prompt-motion skill.

## Step 1 - Ask first (do not write anything yet)

Ask in ONE message, numbered, short. Skip what the user already told you. For any "you decide", pick a default and mark it "(default)". If the user says to just build it and not to ask anything, use defaults for everything, show the brief anyway, and continue to Step 3 after showing it.

1. What is it for, and where will it be shown? Default: a vertical 9:16 full-screen clip, 1080 by 1920, 30 fps, 6 seconds, for Reels. Say that 5 to 7 seconds is the sweet spot for a full-screen clip.
2. What is the goal: what should the viewer feel or do at the end, in one sentence?
3. What is the ONE thing that moves (the hero)? A logo, a number, a headline, a card, a shape, a phone screen. If they list many, ask which one is the hero; the rest stays still or supports it.
4. What do we see in the first frame and in the last frame? Should the end return to the start (loop)?
5. How should it feel? Offer choices and turn the answer into numbers (see the table below): snappy and precise / soft and floating / heavy and weighty / playful with a small overshoot / calm and slow.
6. Camera: static, a move that travels from one thing to another, or none (flat 2D)?
7. Background and colors: one ground color, one ink color, at most one accent, as hex codes if they have them. Light or dark?
8. Text, if any: the exact words in quotes, the language (Hebrew is right-to-left, say so), and a font if they have one. Do not invent claims, numbers or slogans for them.
9. What must NOT appear? Offer the banned defaults below as a checklist and let them add their own.
10. What will build it? Default: Claude Code with the HyperFrames skill (HTML to MP4). Other choices: plain HTML in the browser, After Effects, Remotion, a video model. If they do not know, use the default and say so.

## Step 2 - Write the brief (and STOP)

Use this structure. Under 220 words. Every line must be something a person can check on screen.

```
<direction>
GOAL: <what the viewer feels or does at the end, one sentence>
OUTPUT: <ratio>, <W x H>, <fps>, <duration> seconds, full-screen, loop <yes/no>.
HERO: <the one thing that moves, and how much of the frame it fills>.
LOOK: ground <hex>, ink <hex>, accent <hex and where it may appear>. Typeface <name or "any clean sans that supports Hebrew">, weight, size as a percent of frame height.
MOTION: <named curves by role: enter, move, exit. Name the easing (ease-out, ease-in-out, linear, or a spring with a capped overshoot). Say the speed, for example "fast in, slow settle".>
CAMERA: <static / travels from X to Y / ...>.
TEXT: <exact copy in quotes, language, size, where it sits>.
SHOTS: <beat by beat, in seconds, adding up to the duration. For each beat: the one hero move, what the viewer reads, and how it hands off to the next beat.>
BANNED: <5 to 9 items>. INSTEAD: <for each ban, what to do instead, in a few words>. Anything that looks like a template.
QA: <three frames to check (start, middle, just before the end) and what each must show>.
</direction>
```

Writing rules (adapted from the HyperFrames spec and docs):
- ONE hero. The hero fills at least 40% of the frame's height or width. One hero move per beat. A secondary move travels 50 to 70% as far and starts 0.1 to 0.2 seconds after it. Everything else holds still.
- Things land, then hold still. Only what is truly changing moves (a live number, a progress bar). Do not ask for "breathing" or constant drifting.
- Something new happens every 2 to 4 seconds. Overlap, do not queue: the next element starts while the last one is still settling.
- Combine properties only when they say the same thing: rising and fading in says "arriving". Do not add a spin and a zoom on top.
- Overshoot says "this has weight". Use it only on physical-looking objects. Never on text, UI or numbers (a counter that flies past its final value shows a number that was never true).
- A camera move earns its place only by traveling from one thing to another. A slow creeping push-in for its own sake is not a reason.
- A transition between beats is caused by something already on screen (a card grows until it becomes the next beat). No fade out followed by fade in.
- Prefer numbers (seconds, percent of frame, pixels) over adjectives. If the user gave no number, pick one and mark it "(default, change if needed)".
- Easing must be named for every move. If unsure: ease-out for entering, ease-in-out for crossing the frame, a spring only if the user chose "playful", with damping 0.45 to 0.6 on position and scale (never on opacity or color).
- Text meant to be read: at least 2.6% of the frame's short side (28 px at 1080) and held for 0.5 seconds plus 0.3 seconds per word. If there are too many words, cut words; never shrink the type.
- Vertical 1080 by 1920: the app draws over the frame. Nothing in the top 168 px; every word and the hero inside the band from 168 to 1330 px; below 1330 px only texture or decoration; no text under the right-hand action rail. These are defaults; if the clip is for a specific platform, check its own limits.
- The first frame is the thumbnail and the hook. For a clip that opens a Reel, frame 0 must already show something readable (a face, the result, or one bold line), never black and never only a logo. A logo end card belongs at the end of a clip.
- The Timing (SHOTS) must add up to the duration. No dead time longer than about 1 second unless the user asked for a hold.
- No random numbers in the code: every render must give the same frame at the same time.

Words to numbers (adapted from the HyperFrames spec):
- premium: a material with numbers, for example satin paper with 2% grain, a product on a seamless sweep with a 0.55 contact shadow, chrome at roughness 0.05.
- modern: a camera and a type system, for example a 30-frame push on one ease and a display face at 9% of the frame height with -2% tracking.
- clean: a grid and a ratio, for example 12 columns, 96 px margins, the accent on one word per beat.
- dynamic: cuts on the beat, a layout change every 4 beats, one hero move per beat.
- playful: springs at damping 0.45 to 0.6 on position and scale, never on opacity or color; poses exaggerated by 10 to 30%.
- cinematic: a lens and a light, for example a 35 mm framing, a key from the upper left, a rim from behind, a 6% vignette.

Banned by default (adapted from the HyperFrames spec; each is banned unless the user's own brand or reference uses it):
- a black or dark navy void as the ground with small elements floating in the middle;
- glow, bloom, neon, lens flares, glowing orbs and rings; floating particles as decoration;
- purple or blue gradients, mesh gradients, glass cards;
- everything centered; everything fading in at once; every element fading and sliding up;
- text that moves while it is read; titles that keep drifting after they land;
- corner labels, frame borders, HUD readouts as decoration; the logo docked in a corner;
- bouncy easing on text or UI; crossfades between beats; anything that looks like a template.
Pair each ban in the brief with an INSTEAD. If the user gave none, use the list above. After the first render, name every default the result used anyway and add it to BANNED.

After the brief, ask in Hebrew whether the user approves the brief or wants to change one line. STOP and wait. Do not build before the user approves, unless they said at the start to build immediately.

## Step 3 - Build (only after approval)

Build exactly what the brief says, nothing extra. Choose by what the user answered in question 10.

### Default: HyperFrames (HTML rendered to MP4)
1. Check the tools: Node.js version 22 or newer, FFmpeg, and the HyperFrames skills. Run `npx hyperframes doctor` and read the result. If something is missing, tell the user in Hebrew what to install and wait. If the HyperFrames skills are not installed, run `npx hyperframes skills update` (or install the plugin: `claude plugin marketplace add heygen-com/hyperframes`, then `claude plugin install hyperframes@hyperframes`, then start a new session or run `/reload-plugins`).
2. Work in an empty folder for this clip. Call the HyperFrames skill (`/hyperframes`, or `/hyperframes:hyperframes` if installed as a plugin) and give it the approved brief with this builder prompt, in the same block structure that prompt libraries use:

```
<direction>
(the approved brief)
</direction>

<build>
Use /hyperframes. Vertical 9:16, 1080x1920, 30 fps, as many seconds as the brief says.
Write SPEC.md first: every adjective as a number, the banned defaults by name, the beats by frame.
Build exactly what the brief says and nothing extra. No random numbers, no timers, no network fetches. Everything visible is a function of timeline time.
</build>

<gotchas>
Elements land and then hold still. No bounce on text, UI or numbers. The accent color is used the same way in every beat. Outgoing and incoming text do not overlap in time. If the clip loops, the last frame equals the first frame.
</gotchas>

<start>
Show me the beat plan first. Then build, run `npx hyperframes check --json` and fix every error, take three stills (near the start, in the middle, just before the end), and compare each one to the SHOTS line. Do not render the MP4 until I approve the stills and the preview.
</start>
```
3. Run the check and fix errors before looking. Take stills, for example `npx hyperframes snapshot --at 0.5,3,5.5` (use times that fit the brief). Tell the user what you see in each still, in Hebrew.
4. Preview with `npx hyperframes preview` so the user can watch it in the browser.

### If HyperFrames is not possible
Build one self-contained HTML file (no external files, the animation driven by time) and tell the user to open it in the browser and record the screen. Say honestly that screen recording is less exact than rendering.

### If the user chose another tool
Follow that tool. Say "check the tool's docs" for anything you are not sure about. Do not invent buttons or menu names.

## Step 4 - Iterate with notes, not vibes

Ask for one change at a time and give a timestamp when possible. Useful phrasings, quoted from the HyperFrames docs:
- Too fast: "Too fast. Slow the zooms and pans."
- Drags: "Speed this up."
- Titles keep floating: "Land the titles, then hold them still."
- Feels like slides: "It feels like slides. Carry one thing across each cut."
- Everything appears at once: "Bring things in one after another, on the voice."
- Bouncy or cheap: "No bounce on text or UI."
- A jump at a cut: "There's a jump at 4.2 s."
- A beat with nothing happening: "Scene 3 is dead. Give it something to do."

When the user says the result is not nice, or asks you to improve it (in any words):
1. Do not regenerate. Ask in Hebrew: which second is wrong, and is the problem speed, easing, position, color, or something extra that should not be there?
2. Change only that one line in the brief. Show the changed line.
3. Add anything the user rejects to BANNED, with an INSTEAD.
4. Rebuild, take stills again, compare again.

## Step 5 - Render and deliver

When the user approves the preview: `npx hyperframes render --output final.mp4` (inside the project folder). If the render fails, run `npx hyperframes doctor` and fix what it reports. Tell the user where the file is. If the clip uses a person's face or voice, or AI-generated media, remind the user to write a clear AI label in Hebrew in the post.

## Reference mode (the user pastes a prompt from a library)

Do not reuse it as is. Split it into: goal, format and length, hero, motion and easing, camera, look, text, beats, banned list. Show the split. Ask which parts the user likes ("keep") and which to change. Then ask only the questions from Step 1 that are still unanswered, and write a NEW brief with the user's content. Give a credit line to the original creator if the structure was used closely.

## What NOT to do
- Do not start building before the user approves the brief.
- Do not add effects nobody asked for (glow, particles, sparkles, bounce) to "make it richer".
- Do not use words like stunning, premium or cinematic as instructions.
- Do not promise how it will look before a frame is rendered.
- Do not invent numbers, slogans or customer claims for the text.
- Do not present this skill as an official HeyGen or prompt-motion skill.

## Tiny example of a finished brief

```
<direction>
GOAL: the viewer remembers one orange shape and the feeling of a calm start.
OUTPUT: 9:16, 1080x1920, 30 fps, 6 seconds, full-screen, loop yes.
HERO: a single orange circle, growing to 60% of the frame width.
LOOK: ground warm gray (#EDEAE4), ink none, accent orange (#E8590C). No text.
MOTION: ease-out for the grow, ease-in-out for the morph. Fast in, slow settle. No overshoot.
CAMERA: static.
TEXT: none.
SHOTS: 0.0-1.5 the dot is already visible and grows to 60% width; 1.5-3.0 it morphs into a rounded square (same element, never cut); 3.0-3.6 hold; 3.6-6.0 it returns to the dot, so the last frame equals the first.
BANNED: glow, particles, crossfades, bouncy easing, shadows, text in the corners, anything that looks like a template. INSTEAD: flat shapes, one smooth ease-out, one still background.
QA: 0.5 s a small orange dot; 2.2 s a rounded square; 5.8 s the same small dot as at the start.
</direction>
```
