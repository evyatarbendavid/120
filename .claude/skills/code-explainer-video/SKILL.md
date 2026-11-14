---
name: code-explainer-video
description: Builds a short animated explainer video in code, in a pasted style, with storyboard approval and word-synced sound. Triggers: code video, explainer, אטלס, אנימציה.
---

# code-explainer-video

## When to use (full trigger list)
Builds a short animated explainer video with CODE instead of an AI video model - ONE HTML file where plain JavaScript draws every frame on a canvas, sound effects are synthesized in code, an optional voiceover is timed to the words (word-level transcript), with a storyboard the user approves first and an optional MP4 render. Starts from style reference CODE the user pastes (or a saved style, or the built-in starter style) so the look stays the same from video to video. It never needs a video as input. Use when the user says "explainer video with code", "motion graphics with Claude", "style atlas", the Hebrew word "אטלס", or asks in Hebrew for an animated explainer built with code instead of a video model, or pastes code or a long prompt of a code-made video and wants a new video on a new topic in the same style.

You make a short animated explainer (reel, YouTube explainer, or square) as ONE HTML file: plain JavaScript draws every frame on a canvas, the sound effects are synthesized in code, and an optional voiceover is timed to the words. No AI video model, no animation framework (no Remotion, no HyperFrames). The input is TEXT and CODE only: a topic, optional style code, optional audio + transcript. You never need to watch a video.

Idea source (say it once in your final message): the YouTube video "Claude Makes a New Kind of Video - Full Tutorial" by Futurepedia (https://www.youtube.com/watch?v=Ge1B-Ok1Pfk). You do NOT know how that creator's "Style Atlas" prompts are written and this skill is not a copy of them. It is a separate, simpler workflow on the same idea: a code-made video is easiest to repeat when you start from the real CODE of an example, not from a description of it.

Always talk to the user in Hebrew (simple, short sentences, no jargon without a one-line explanation) unless they write in another language. These instructions are in English. Hebrew sentences that matter are described here by meaning: you write them yourself, in natural Hebrew.

## 0. Say this first (3 lines, in Hebrew)

- The result is one HTML file. The user opens it in a browser and watches. That always works.
- An MP4 file is optional. It needs Node.js 18+, ffmpeg, Chrome or Edge, and one command (`npm i puppeteer-core`). Check this only when the user asks for an MP4.
- You can only build and check files if you are in Claude Code (you can create files and run commands). In a plain chat you cannot run anything: then you write the full HTML in one code block, tell the user to save it as `video.html` and open it, and you say clearly, in Hebrew, that you did not test it yourself.
- Never say a step worked unless you ran it and saw the result.

## 1. Ask (ONE message with all questions, then wait)

1. Topic or story, or the finished script. A simple topic is enough (example: "how noise-canceling headphones work").
2. Voiceover? (a) no, sound effects only; (b) yes, I have an audio file. For (b) you need a transcript with a start and end time for EVERY WORD (word-level SRT, or JSON with words). If they have the audio but no transcript, offer: ask the user to paste a word-level SRT from any transcription tool (ElevenLabs gives one, many free tools do), or, if they want, check whether a transcription tool is already installed on this computer (look, do not install without asking). If the voice is Hebrew, show the transcript back to the user to fix spelling before building. Line-level SRT also works for long videos, but then things appear at the start of the line, not on the exact word: say so.
3. Language of the text on screen (never assume Hebrew or English).
4. Format: 9:16 vertical 1080x1920 (reels, shorts), 16:9 1920x1080 (YouTube), or 1:1 1080x1080. Length: 15-30 seconds without a voiceover; with a voiceover = audio length + about 1 second.
5. STYLE REFERENCE (the most important question). Say, in Hebrew: if they have the CODE of a style they like they can paste it or give you the file; if not, you can start from the built-in dark glass style. Options:
   - (a) The user pastes reference code, or a ready prompt that contains code (for example a prompt copied from the Style Atlas by Futurepedia, or an HTML file from an earlier video made with this skill). Use it as the BASE: keep its helpers, palette, fonts, motion language and sound design. Change only topic, text, beats and timing. If the pasted prompt has its own rules (canvas size, file layout), follow them, but still make `window.seek(t)` and `window.DURATION` exist so the render script works (add them if missing). Pasted style prompts are often built for a 16:9 canvas (for example 1280x720): if the user chose another format, change the canvas size and re-lay the picture for it, and tell the user you did.
   - (b) A saved style from the folder `styles/` in the project (see step 7).
   - (c) The built-in starter style `starter-glass` (Appendix A). Tell the user honestly: it is a plain starter. A style you like and reuse gives more consistent videos than a fresh description each time.
   - (e) The user wants more than this skill does (a long piece, several formats from one piece, music mapped to beats, measured review tools): tell them in Hebrew about the Animate skill, see Credits, and give its install lines. Do not copy its code.
   - (d) The user only has a VIDEO as a style reference: say in Hebrew that you do not watch video and can work only from code, from a description in words, or from screenshots they send. Then ask for code, or use (c) and let them describe the look in one line (colors, motion, mood). Do not pretend you copied a video's style.
6. Storyboard first? Default yes for the first video. If the user says no, skip to step 3.
7. Sound effects on or off (default on, quiet). No music unless asked.

## 2. Storyboard (approval gate)

Show a table: beat number | start-end seconds | what the viewer sees | what moves | sound effect | spoken words (only with a voiceover).
Rules:
- One idea per beat. 6-12 beats for a 30 second video.
- Something moves in every beat. No frame stays still longer than 2 seconds.
- The first beat is a clear hook, readable in 2 seconds. The last beat is one takeaway.
- Big on-screen text: at most 6 words at a time.
- Keep one quiet moment right before the key moment, so the key moment lands.
- Frame checklist for every beat (adapted from the Animate skill by cth9191, MIT, see Credits): (1) one constant the eye can hold, such as a hero, a stage or a page that stays while the rest changes; (2) a colour means one thing, and one reserved colour is for the thing the story follows; (3) the medium shows (paper, ink, glass, pixels) in every frame, so no frame could be "any style"; (4) the idea is acted out, not only labelled; (5) something is happening in every frame, and held frames still have small idle life; (6) at most one short caption per beat, large enough to read on a phone; (7) vary the scale: wide shots, mid shots and at least one close-up; (8) a recurring thread (a prop, a colour, a shape) comes back changed; (9) phone-safe: on 1080x1920 keep what matters inside x 60-940 and y 250-1500.
- Facts and numbers: only what the user gave you. Mark anything unverified with [לבדוק]. Never invent numbers, quotes or sources.
Ask in Hebrew whether the user approves the storyboard or wants a change (for example: change beat X). Continue ONLY after a clear yes. This is a stop point.

## 3. Build: the page contract

Write ONE file `<project>/<name>.html`. These rules make a code video reliable and easy to edit:

1. One `<canvas>` whose width and height in pixels equal the output size. Everything the viewer sees is drawn on that canvas (no HTML overlays), so the MP4 is identical to the preview. Player buttons outside the canvas are fine.
2. `window.DURATION` = total seconds.
3. `window.seek(t)` draws the complete frame for time `t` from scratch. It is a pure function of `t`: no `Date.now()`, no `Math.random()` (use a seeded random generator), nothing that remembers the previous frame. Then any frame can be drawn on demand, edits are precise, and the render is repeatable.
4. A player in the browser: play / pause, scrub, loop, sound on/off. Playback only calls `seek(elapsed)` on every animation frame.
5. Sound: a list of events `{t, type}` and a function that creates the sounds with WebAudio (oscillators, filtered noise, short envelopes). The SAME function runs on an `OfflineAudioContext`, and `window.renderAudioWav()` returns that render as a base64 string of a 48 kHz stereo 16-bit WAV, so the MP4 gets the same sound. Sound design: hit the moments that matter (a thing pops in, a label lands, the key moment); at most 3 sounds at once; effects quieter than the voice; small silences so the big hit is heard. No music unless asked.
6. Voiceover: a "Load voiceover" button (file picker and drag-and-drop) that plays the audio in sync with `seek`. Embed word timings as `const WORDS = [{w, s, e}]` (word, start seconds, end seconds). Each beat starts when its first word starts; key words trigger the pops. Do not guess timings by eye: read them from `WORDS`. To convert an SRT: `HH:MM:SS,mmm` = hours*3600 + minutes*60 + seconds + ms/1000.
7. Text on screen: for 9:16 keep important content inside x 60-940 and y 250-1500 on a 1080x1920 canvas (the app interface covers the rest). Headlines at least 64px on a 1080-wide canvas. Hebrew: set `LANG = 'he'` in the starter (it sets `ctx.direction = 'rtl'`), use a font with Hebrew letters (Heebo if installed, otherwise Arial), and look at a real frame to check punctuation and English words inside Hebrew lines. The starter's sample titles are English placeholders: you write the real titles in the language the user chose.
8. Fonts: use a font the computer already has, or load one and set `window.READY` to the promise of `document.fonts.load(...)` so the renderer waits for it.
9. Comment every beat in the code with its storyboard number, so "make beat 4 slower" is a one-place edit.

If you have reference code (option a, b or c): copy its structure and helpers into your file, then change only what the storyboard requires. Do not redesign the style. The working starter file in Appendix A already follows all 9 rules: to use it, write it to the project folder, then edit only its section 1 (settings), section 2 (BEATS) and, if needed, the picture functions in `PICS`.

## 4. Self-check (before the user sees anything; only if you can run commands)

Give a short list of what passed and what you fixed. Do not invent a numeric score.
1. Open the page in headless Chrome. No console errors.
2. For every beat capture frames at its start, middle and end (`seek(t)`, then `canvas.toDataURL`) and LOOK at them. Fix cut-off text, overlaps, low contrast, wrong Hebrew direction, empty frames.
3. Determinism: `seek(2.0)`, `seek(5.0)`, `seek(2.0)` again. The first and third images must be identical. If not, find the hidden state or the `Math.random()`.
4. Motion: compare frames every 0.25 s; if a whole second is identical, add motion.
5. With a voiceover: each key word and its visual within about 0.15 s.
6. Sound: `renderAudioWav()` is not empty and the peak is below 1.0 (the starter file has `sfxPeak()` for this).
At most 3 fix rounds, then tell the user what is still weak.

## 5. Show it, then render

- Tell the user where the HTML file is, to open it in a browser (double click), and ask what to change. Browsers block sound until the first click: tell them to press play.
- MP4, only after the user saw the preview and asked for it: make sure Node 18+, ffmpeg and Chrome/Edge exist (run `node -v` and `ffmpeg -version`). Missing one? Say which, give the one plain fix (install it, then reopen Claude Code), and offer the fallback: play the HTML full screen and screen-record. Then save `render.mjs` (Appendix B) in the project folder, run `npm i puppeteer-core` there once, make a draft: `node render.mjs name.html draft.mp4 15 [voiceover-file]`, and after approval the final: `node render.mjs name.html final.mp4 30 [voiceover-file]`. A 17 second 1080x1920 draft at 10 fps took about half a minute on a normal PC.
- Never upload or publish anything. Tell the user where the files are.

## 6. Changes

Changes are precise because it is code: palette, speed, one beat, one word. Edit only what was asked, keep the previous version as `name.v1.html`, and re-run the self-check on the beats you touched.

## 7. Save the style (offer once, when the user is happy)

Ask in Hebrew whether they want to keep this style for next time. If yes, create `styles/<style-name>/` with `reference.html` (the final working file) and `style-card.md`, a short style card of 8-12 plain lines with these fields: Name, Look (what the picture looks like), Motion (how things move), How it explains (how an idea is shown), palette hex values, fonts, sound palette, and hard rules such as "max 6 words on screen". Next time, start from `reference.html` and change only the topic, text and timing. If the base came from someone else's library, remind the user to check that library's terms before sharing the files. Tip for the user: this skill's own style folder is the way to avoid going back to a library every time.

## 8. Rules

- Wait for a clear yes at the storyboard (unless the user turned it off).
- No AI video model. If the user wants photoreal footage, say this skill makes graphic, animated explainers.
- Report what you measured (frames checked, peak level, motion check), not just that it looks fine.
- Never promise views, followers, income, or that the result "does not look like AI".
- Do not copy another creator's code, prompts or designs on your own initiative. Use only what the user pasted or gave you.
- A voice made by AI (text-to-speech) must be described as AI-made if the video is published. Never clone a real person's voice or face without their consent.
- If a tool, font or voice is missing, say it in one plain sentence. Do not pretend it worked.
- Final message in Hebrew: file paths, length, a one-line list of the beats, what the self-check found (or, in Hebrew, that you could not run it), one thing to improve next, and the idea source (the Futurepedia video) in one line.

## Credits and licenses
- Idea source: the YouTube video "Claude Makes a New Kind of Video - Full Tutorial" by Futurepedia, https://www.youtube.com/watch?v=Ge1B-Ok1Pfk. Its "Style Atlas" (https://www.futurepedia.io/resources/ai-style-atlas) was not available to the author of this skill (blocked for automated access), so none of its prompts or code are included or copied. This skill rebuilds the method the video shows, in its own words: a style card, a helper library, rules for staying in the style, sound rules (score the moments that land, a quiet bed, at most 3 sounds at once, small silences), and a render through headless Chrome and ffmpeg. This skill is not the creator's skill.
- Animate by cth9191, https://github.com/cth9191/animate, MIT License, Copyright (c) 2026 cth9191. The frame checklist in step 2 is adapted from its `grammar/FRAME.md`, and the "report what you measured" rule from its non-negotiables. License terms (MIT): permission is granted, free of charge, to use, copy, modify and distribute the software and its documentation, provided the copyright notice and the permission notice are included; the software is provided "as is", without warranty of any kind. Animate is a separate, larger skill (seven built-in styles, music mapped to beats, several formats from one piece, a measured review step). Install lines from its README: `/plugin marketplace add cth9191/animate` and then `/plugin install animate@animate`; it needs Node 18+, Playwright with Chromium, and ffmpeg. It is not related to the Futurepedia video as far as the author of this skill knows.

## Appendix A: starter-glass/reference.html (tested: 16.8 s, 1080x1920, Hebrew RTL, sound, word timing)

Write this to `<project>/styles/starter-glass/reference.html` (and copy it to `<project>/video.html` to start a new video). It is a working example about "how noise-canceling headphones work" with English placeholder titles: replace the topic and the titles in BEATS, and set `LANG = 'he'` when the on-screen text is Hebrew.

```html
<!doctype html>
<html lang="he"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>starter-glass</title>
<style>
html,body{margin:0;background:#000;color:#ccc;font:14px system-ui,Arial}
#wrap{display:flex;flex-direction:column;align-items:center;gap:8px;padding:8px}
canvas{height:calc(100vh - 76px);max-width:96vw;aspect-ratio:9/16;background:#000}
#bar{display:flex;gap:6px;align-items:center;width:min(96vw,520px)}
#bar input[type=range]{flex:1}
button{background:#7C5CFF;color:#fff;border:0;border-radius:8px;padding:6px 10px;cursor:pointer}
button.off{background:#444}
</style></head><body>
<div id="wrap"><canvas id="c" width="1080" height="1920"></canvas>
<div id="bar"><button id="pl">play</button><input id="sk" type="range" min="0" max="1000" value="0"><button id="lp" class="off">loop</button><button id="sn">sound</button><button id="vo">Load voiceover</button><input id="vf" type="file" accept="audio/*" hidden></div></div>
<script>
// ======== 1. SETTINGS (change these first) ========
const W = 1080, H = 1920, LANG = 'en';              // 'he' = right-to-left text (set it when the on-screen text is Hebrew)
const PAL = { bg1: '#0B0910', bg2: '#17131F', ink: '#F4F1FB', mute: '#ABA4BF', a: '#7C5CFF', b: '#B8A8FF', c: '#FFB547' };
const FONT = 'Heebo, Arial, sans-serif';
// WORDS (optional voiceover timing): [{w:'word', s:startSeconds, e:endSeconds}, ...]. Empty = no voiceover.
const WORDS = [];
// ======== 2. BEATS (the titles below are English placeholders: write the real titles in the language of the video). (one per storyboard row). t,d = start and length in seconds (ignored when WORDS is filled:
// then "at" = index of the word that starts the beat). draw = which picture. sfx = [[sound, secondsAfterBeatStart]].
const BEATS = [
  { t: 0.0,  d: 2.6, title: 'How do headphones cancel noise?',        sub: '',                         draw: 'ring',  at: 0 },            // beat 1
  { t: 2.6,  d: 2.6, title: 'A microphone hears the noise',           sub: 'It is always outside',            draw: 'wave',  at: 3 },            // beat 2
  { t: 5.2,  d: 3.2, title: 'They make an opposite wave',               sub: 'The exact opposite of the noise',         draw: 'pair',  at: 7 },            // beat 3
  { t: 8.4,  d: 3.2, title: 'Together they cancel out',         sub: '',                         draw: 'sum',   at: 11, sfx: [['whoosh', -0.05], ['pop', 0.15], ['hit', 1.5]] }, // beat 4
  { t: 11.6, d: 2.4, title: 'The noise falls, the quiet rises',            sub: '',                         draw: 'bars',  at: 15 },           // beat 5
  { t: 14.0, d: 2.8, title: 'Quiet. In code.',                      sub: '',                         draw: 'check', at: 19, sfx: [['whoosh', -0.05], ['chime', 0.3]] } // beat 6
];
// ======== 3. TOOLS (usually no need to touch) ========
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, u) => a + (b - a) * u;
const eo = (x) => 1 - Math.pow(1 - clamp(x), 3);
const eb = (x) => { x = clamp(x); const c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
// timeline: start/end of every beat (from WORDS when they exist)
const TL = BEATS.map((b, i) => ({ ...b, s: WORDS.length ? WORDS[Math.min(b.at, WORDS.length - 1)].s : b.t }));
TL[0].s = 0;   // the first beat always starts at 0
TL.forEach((b, i) => { b.e = i + 1 < TL.length ? TL[i + 1].s : (WORDS.length ? WORDS[WORDS.length - 1].e + 1 : b.s + b.d); });
window.DURATION = TL[TL.length - 1].e;
const R0 = rng(7);
const BLOBS = Array.from({ length: 5 }, () => ({ x: R0() * W, y: R0() * H, r: 300 + R0() * 300, ph: R0() * 6.28, sp: 0.25 + R0() * 0.3, c: [PAL.a, PAL.b, PAL.c][Math.floor(R0() * 3)] }));
const BARS = Array.from({ length: 12 }, () => 0.5 + R0() * 0.5);
function card(x, y, w, h) {
  ctx.save(); ctx.beginPath(); ctx.roundRect(x, y, w, h, 44);
  ctx.fillStyle = 'rgba(255,255,255,0.07)'; ctx.fill();
  ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(255,255,255,0.18)'; ctx.stroke(); ctx.restore();
}
function wrap(text, maxW) {
  const words = text.split(' '), lines = []; let cur = '';
  for (const w of words) { const t = cur ? cur + ' ' + w : w; if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t; }
  if (cur) lines.push(cur); return lines;
}
function text(str, x, y, size, color, weight = 700, maxW = 900, lh = 1.15, alpha = 1) {
  ctx.save(); ctx.font = weight + ' ' + size + 'px ' + FONT; ctx.fillStyle = color; ctx.globalAlpha = alpha;
  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.direction = LANG === 'he' ? 'rtl' : 'ltr';
  const lines = wrap(str, maxW); lines.forEach((l, i) => ctx.fillText(l, x, y + i * size * lh)); ctx.restore(); return lines.length;
}
const CX = 120, CY = 640, CW = 840, CH = 640;           // the glass card that holds the picture
const nz = (x, tt) => Math.sin(0.02 * x - tt * 5) + 0.5 * Math.sin(0.047 * x - tt * 8.5);
function line(fn, y0, amp, color, wd, alpha) {
  ctx.save(); ctx.beginPath(); ctx.rect(CX + 20, CY, CW - 40, CH); ctx.clip(); ctx.beginPath();
  for (let x = 0; x <= CW; x += 6) { const y = CY + y0 - amp * fn(x); x ? ctx.lineTo(CX + x, y) : ctx.moveTo(CX + x, y); }
  ctx.strokeStyle = color; ctx.lineWidth = wd; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.globalAlpha = alpha; ctx.stroke(); ctx.restore();
}
const PICS = {
  ring(u, t) { for (let i = 0; i < 4; i++) { const p = ((t * 0.45 + i / 4) % 1); ctx.beginPath(); ctx.arc(CX + CW / 2, CY + CH / 2, 40 + p * 270, 0, 7); ctx.strokeStyle = PAL.c; ctx.lineWidth = 8; ctx.globalAlpha = (1 - p) * 0.9; ctx.stroke(); } ctx.globalAlpha = 1; ctx.beginPath(); ctx.arc(CX + CW / 2, CY + CH / 2, 34, 0, 7); ctx.fillStyle = PAL.ink; ctx.fill(); },
  wave(u, t) { const a = eo(u / 0.7); line((x) => nz(x, t), CH / 2, 120 * a, PAL.c, 10, 1); },
  pair(u, t) { const a = eo(u / 0.6), b = eo((u - 0.7) / 0.7); line((x) => nz(x, t), 190, 80 * a, PAL.c, 9, 1); line((x) => -nz(x, t), 450, 80 * b, PAL.b, 9, b); },
  sum(u, t) { const p = eo((u - 0.3) / 1.2); const sh = 150 * (1 - p); const anti = (x) => -nz(x - sh, t);
    line((x) => nz(x, t), 130, 60, PAL.c, 7, 0.9); line(anti, 300, 60, PAL.b, 7, 0.9);
    line((x) => nz(x, t) + anti(x), 510, 60, PAL.ink, 12, 1); },
  bars(u, t) { const k = eo(u / 1.6); BARS.forEach((v, i) => { const h = (CH - 160) * (v * (1 - 0.88 * k) + 0.04 + 0.03 * Math.sin(t * 6 + i)); const w = 48, gap = (CW - 120 - 12 * w) / 11, x = CX + 60 + i * (w + gap);
    ctx.beginPath(); ctx.roundRect(x, CY + CH - 80 - h, w, h, 18); ctx.fillStyle = k > 0.8 ? PAL.b : PAL.c; ctx.fill(); }); },
  check(u, t) { const p = eo(u / 0.8), cx = CX + CW / 2, cy = CY + CH / 2; ctx.beginPath(); ctx.arc(cx, cy, 190 * p, 0, 7); ctx.fillStyle = PAL.a; ctx.fill();
    const q = eo((u - 0.4) / 0.6); ctx.beginPath(); ctx.moveTo(cx - 90, cy + 5); ctx.lineTo(lerp(cx - 90, cx - 25, clamp(q * 2)), lerp(cy + 5, cy + 70, clamp(q * 2)));
    if (q > 0.5) ctx.lineTo(lerp(cx - 25, cx + 95, (q - 0.5) * 2), lerp(cy + 70, cy - 60, (q - 0.5) * 2));
    ctx.strokeStyle = PAL.ink; ctx.lineWidth = 26; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.stroke(); }
};
function draw(t) {
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, PAL.bg1); g.addColorStop(1, PAL.bg2); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  for (const b of BLOBS) { const x = b.x + Math.sin(t * b.sp + b.ph) * 90, y = b.y + Math.cos(t * b.sp * 0.8 + b.ph) * 90;
    const rg = ctx.createRadialGradient(x, y, 0, x, y, b.r); rg.addColorStop(0, b.c + '33'); rg.addColorStop(1, b.c + '00'); ctx.fillStyle = rg; ctx.fillRect(0, 0, W, H); }
  ctx.fillStyle = 'rgba(255,255,255,0.15)'; ctx.fillRect(90, 170, 900, 6); ctx.fillStyle = PAL.b; ctx.fillRect(90, 170, 900 * clamp(t / DURATION), 6);   // progress line (top safe area)
  let k = TL.findIndex((b) => t >= b.s && t < b.e); if (k < 0) k = TL.length - 1; const b = TL[k], u = t - b.s;
  const s = eb(u / 0.5); ctx.save(); ctx.translate(W / 2, 360); ctx.scale(lerp(0.85, 1, s), lerp(0.85, 1, s)); ctx.globalAlpha = clamp(u / 0.25);
  text(b.title, 0, 0, 104, PAL.ink, 700, 840, 1.15); ctx.restore();                                       // beat title (max ~6 words)
  const c = eo(u / 0.5); ctx.save(); ctx.translate(0, (1 - c) * 60); ctx.globalAlpha = c; card(CX, CY, CW, CH);
  ctx.save(); ctx.beginPath(); ctx.roundRect(CX, CY, CW, CH, 44); ctx.clip(); PICS[b.draw](u, t); ctx.restore(); ctx.restore();
  if (b.sub) text(b.sub, W / 2, 1390, 56, PAL.mute, 500, 800, 1.2, eo((u - 0.5) / 0.4));
}
window.seek = (t) => draw(clamp(t, 0, DURATION));          // pure function of time: no Math.random, no Date.now, no memory
window.READY = (document.fonts && document.fonts.load) ? document.fonts.load('700 64px Heebo').catch(() => {}) : Promise.resolve();
// ======== 4. SOUND (made in code) ========
const SFX = []; TL.forEach((b) => (b.sfx || [['whoosh', -0.05], ['pop', 0.15]]).forEach(([type, dt]) => SFX.push({ t: Math.max(0, b.s + dt), type })));
function scheduleSfx(ac, dest) {
  const nb = ac.createBuffer(1, ac.sampleRate, ac.sampleRate), d = nb.getChannelData(0), r = rng(99); for (let i = 0; i < d.length; i++) d[i] = r() * 2 - 1;
  const env = (g, t0, pk, a, rel) => { g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(pk, t0 + a); g.gain.exponentialRampToValueAtTime(0.0001, t0 + a + rel); };
  const osc = (type, f0, f1, t0, pk, a, rel) => { const o = ac.createOscillator(), g = ac.createGain(); o.type = type; o.frequency.setValueAtTime(f0, t0); o.frequency.exponentialRampToValueAtTime(f1, t0 + a + rel); env(g, t0, pk, a, rel); o.connect(g).connect(dest); o.start(t0); o.stop(t0 + a + rel + 0.05); };
  for (const e of SFX) { const t0 = e.t;
    if (e.type === 'pop') osc('sine', 500, 900, t0, 0.3, 0.01, 0.12);
    if (e.type === 'tick') osc('triangle', 1800, 1500, t0, 0.15, 0.003, 0.04);
    if (e.type === 'hit') { osc('sine', 140, 45, t0, 0.5, 0.005, 0.45); }
    if (e.type === 'chime') { osc('sine', 880, 880, t0, 0.2, 0.01, 0.9); osc('sine', 1320, 1320, t0 + 0.08, 0.14, 0.01, 0.8); }
    if (e.type === 'whoosh') { const s = ac.createBufferSource(), f = ac.createBiquadFilter(), g = ac.createGain(); s.buffer = nb; f.type = 'bandpass'; f.Q.value = 1.2; f.frequency.setValueAtTime(400, t0); f.frequency.exponentialRampToValueAtTime(2600, t0 + 0.35); env(g, t0, 0.2, 0.12, 0.25); s.connect(f).connect(g).connect(dest); s.start(t0); s.stop(t0 + 0.5); } }
}
async function renderSfx() { const sr = 48000, oc = new OfflineAudioContext(2, Math.ceil(DURATION * sr), sr); scheduleSfx(oc, oc.destination); return oc.startRendering(); }
function encodeWav(buf) {
  const n = buf.length, sr = buf.sampleRate, L = buf.getChannelData(0), Rr = buf.numberOfChannels > 1 ? buf.getChannelData(1) : L, o = new DataView(new ArrayBuffer(44 + n * 4));
  const s = (p, str) => { for (let i = 0; i < str.length; i++) o.setUint8(p + i, str.charCodeAt(i)); };
  s(0, 'RIFF'); o.setUint32(4, 36 + n * 4, true); s(8, 'WAVE'); s(12, 'fmt '); o.setUint32(16, 16, true); o.setUint16(20, 1, true); o.setUint16(22, 2, true); o.setUint32(24, sr, true); o.setUint32(28, sr * 4, true); o.setUint16(32, 4, true); o.setUint16(34, 16, true); s(36, 'data'); o.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) { o.setInt16(44 + i * 4, Math.round(clamp(L[i], -1, 1) * 32767), true); o.setInt16(46 + i * 4, Math.round(clamp(Rr[i], -1, 1) * 32767), true); }
  const u = new Uint8Array(o.buffer); let bin = ''; for (let i = 0; i < u.length; i += 0x8000) bin += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); return btoa(bin);
}
window.renderAudioWav = async () => encodeWav(await renderSfx());          // the renderer mixes this with the voiceover file
window.sfxPeak = async () => { const b = await renderSfx(); let p = 0; for (let c = 0; c < b.numberOfChannels; c++) for (const v of b.getChannelData(c)) p = Math.max(p, Math.abs(v)); return p; };
// ======== 5. PLAYER (browser only; the video itself is only the canvas) ========
let playing = false, loop = false, snd = true, tNow = 0, t0 = 0, actx = null, sfxBuf = null, voiceBuf = null, srcs = [];
const $ = (id) => document.getElementById(id);
function stopAudio() { srcs.forEach((s) => { try { s.stop(); } catch (e) {} }); srcs = []; }
async function startAudio(off) {
  stopAudio(); if (!snd) return; actx = actx || new (window.AudioContext || window.webkitAudioContext)(); await actx.resume(); sfxBuf = sfxBuf || await renderSfx();
  for (const b of [sfxBuf, voiceBuf]) { if (!b) continue; const s = actx.createBufferSource(); s.buffer = b; s.connect(actx.destination); if (off < b.duration) s.start(0, off); srcs.push(s); }
}
async function play() { playing = true; $('pl').textContent = 'pause'; if (tNow >= DURATION - 0.05) tNow = 0; await startAudio(tNow); t0 = performance.now() - tNow * 1000; requestAnimationFrame(tick); }
function pause() { playing = false; $('pl').textContent = 'play'; stopAudio(); }
function tick() { if (!playing) return; tNow = (performance.now() - t0) / 1000; if (tNow >= DURATION) { if (loop) { tNow = 0; startAudio(0); t0 = performance.now(); } else { tNow = DURATION; pause(); } } seek(tNow); $('sk').value = Math.round(1000 * tNow / DURATION); if (playing) requestAnimationFrame(tick); }
$('pl').onclick = () => (playing ? pause() : play());
$('sk').oninput = (e) => { tNow = DURATION * e.target.value / 1000; seek(tNow); if (playing) { startAudio(tNow); t0 = performance.now() - tNow * 1000; } };
$('lp').onclick = (e) => { loop = !loop; e.target.classList.toggle('off', !loop); };
$('sn').onclick = (e) => { snd = !snd; e.target.classList.toggle('off', !snd); if (playing) startAudio(tNow); };
async function loadVoice(file) { actx = actx || new (window.AudioContext || window.webkitAudioContext)(); voiceBuf = await actx.decodeAudioData(await file.arrayBuffer()); $('vo').textContent = 'voiceover loaded'; }
$('vo').onclick = () => $('vf').click(); $('vf').onchange = (e) => e.target.files[0] && loadVoice(e.target.files[0]);
document.addEventListener('dragover', (e) => e.preventDefault()); document.addEventListener('drop', (e) => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) loadVoice(f); });
seek(0);
</script></body></html>
```

## Appendix B: render.mjs (tested: HTML to MP4 with sound)

Run `npm i puppeteer-core` once in the project folder. Usage: `node render.mjs name.html out.mp4 30 voiceover.mp3`. Needs ffmpeg and Chrome or Edge (set `CHROME_PATH` if it is not found). The file uses `import`, so keep the name `render.mjs`.

```js
// render.mjs - render a canvas explainer (one HTML file) to MP4 with sound.
// usage: node render.mjs video.html out.mp4 [fps=30] [voiceover.mp3|wav|m4a]
// needs: Node 18+, ffmpeg on PATH, Chrome or Edge, and `npm i puppeteer-core` once in this folder.
import puppeteer from 'puppeteer-core';
import { spawn, spawnSync } from 'node:child_process';
import { writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [html, out = 'draft.mp4', fpsArg = '30', voice] = process.argv.slice(2);
if (!html) { console.error('usage: node render.mjs video.html out.mp4 [fps] [voiceover]'); process.exit(1); }
if (spawnSync('ffmpeg', ['-version']).error) { console.error('ffmpeg not found on PATH. Install it, reopen the terminal, try again.'); process.exit(1); }
const candidates = [
  process.env.CHROME_PATH,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium',
].filter(Boolean);
const executablePath = candidates.find((p) => existsSync(p));
if (!executablePath) { console.error('No Chrome/Edge found. Set the CHROME_PATH environment variable.'); process.exit(1); }

const browser = await puppeteer.launch({ executablePath, headless: true });
const page = await browser.newPage();
page.on('pageerror', (e) => console.error('page error:', e.message));
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.waitForFunction('typeof window.seek === "function" && window.DURATION > 0');
await page.evaluate(() => window.READY || true);
const { w, h, dur } = await page.evaluate(() => {
  const c = document.querySelector('canvas');
  return { w: c.width, h: c.height, dur: window.DURATION };
});
const fps = Number(fpsArg);
const frames = Math.round(dur * fps);

let sfx = null;
if (await page.evaluate(() => typeof window.renderAudioWav === 'function')) {
  const b64 = await page.evaluate(() => window.renderAudioWav());
  sfx = path.resolve('sfx.wav');
  writeFileSync(sfx, Buffer.from(b64, 'base64'));
}

const args = ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-'];
const audioInputs = [sfx, voice].filter(Boolean);
audioInputs.forEach((a) => args.push('-i', a));
if (audioInputs.length === 2) {
  args.push('-filter_complex', '[1:a][2:a]amix=inputs=2:duration=longest:normalize=0[a]', '-map', '0:v', '-map', '[a]');
} else if (audioInputs.length === 1) {
  args.push('-map', '0:v', '-map', '1:a');
}
args.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-r', String(fps));
if (audioInputs.length) args.push('-c:a', 'aac', '-b:a', '192k', '-t', String(dur));
args.push(out);

const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
for (let i = 0; i < frames; i++) {
  const dataUrl = await page.evaluate((t) => {
    window.seek(t);
    return document.querySelector('canvas').toDataURL('image/png');
  }, i / fps);
  const buf = Buffer.from(dataUrl.split(',')[1], 'base64');
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
console.log(`wrote ${out}: ${frames} frames, ${w}x${h}, ${dur}s`);
```
