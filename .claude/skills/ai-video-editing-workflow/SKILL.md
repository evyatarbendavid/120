---
name: ai-video-editing-workflow
description: Principles and a step-by-step workflow for editing short vertical videos (reels) with an AI agent - local transcription, careful transcript review, readable captions in Hebrew or English, an approved edit plan, HyperFrames scenes, automated plus visual checks, loudness mastering and a pre-publish checklist. Use when asked to edit, caption, cut, animate or master a talking-head or reel video, or to design an automated video-editing pipeline (ערוך סרטון, כתוביות, ריל, פייפליין עריכה, עריכת וידאו אוטומטית). It is the process and quality layer; for HyperFrames mechanics use the hyperframes skills.
---

# AI video editing workflow

A working method for turning a finished talking-head recording into a polished short video
(captions, motion graphics, music, mastering) with an agent doing the work and the human
approving at a few cheap checkpoints. The principles are distilled from a practitioner's guide
(Roy Shavit, 2026) and rewritten here in my own words; the numbers are sensible defaults to tune,
not laws.

Answer the user in Hebrew unless they write in another language.

## How this fits with the other skills

- `hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-cli`: how to write,
  check and render the scenes. Read them before writing any scene.
- `embedded-captions`, `talking-head-recut`, `music-to-video`: finished workflows for narrower jobs.
- This skill: the order of work, what to verify, and the quality bar. Use it to decide what to do
  next; use the others to do it.

## The core idea

The agent is the editor and the scripts are its hands.

- **Judgment belongs to the agent and the human**: what the sentence means, where a cut or an
  emphasis belongs, whether a correction is right, whether the result looks right.
- **Mechanical work belongs to scripts**: extracting audio and frames, running transcription,
  building captions from a word list, rendering, compositing, measuring loudness. Write a script
  once, reuse it for every video, and fix the script (not just the current video) when it breaks.

## Three rules that hold the system together

1. **The original is never touched.** Every step writes a new file, so you can always go back.
2. **Every step leaves a file behind**: transcript, corrections, edit plan, snapshots, report.
   When something is wrong you can see exactly where it went wrong.
3. **Check, do not guess.** Never say "looks good" about a frame you have not rendered and
   looked at. When unsure, mark the spot and say so; do not invent.

## The pipeline

| # | Stage | Output | Human gate |
|---|---|---|---|
| 1 | Ingest | copy of source, hash, audio, sample frames, facts about the file | |
| 2 | Transcribe | raw transcript with a timestamp per word | |
| 3 | Review transcript | corrections and flags in a separate file; corrected words re-aligned | **approve flagged moments** |
| 4 | Captions | caption list, SRT and VTT | |
| 5 | Edit plan | table of events: start, end, type, purpose | **approve the plan** |
| 6 | Scenes | HyperFrames compositions timed to the words | |
| 7 | Inspect | automatic checks plus snapshots you actually look at | **approve a draft on a phone** |
| 8 | Render and master | final MP4, composited, mixed, loudness-measured | |

Put the gates where a change is cheap (a table, a draft), not after the expensive render.
Details per stage are below; the full pre-publish list is in `references/checklist.md`.

### 1. Ingest
Copy the source and never edit it. Record a hash. Extract mono 16 kHz audio for transcription and
sample a frame every few seconds. Report resolution, aspect ratio (9:16 for reels), frame rate and
length, and flag anything unusual before going further. The frames are how the agent "sees" where
the face is: it does not watch video. Extra material (logo, product screenshot, music) goes into
the project folder; it must be real, not generated, and each file gets checked.

### 2. Transcribe
The transcript is the foundation: captions are built from it and every animation is timed to a
word, so you need a timestamp per word. Run a local model; for Hebrew prefer a Hebrew-tuned
Whisper model over the generic one. Three settings matter: word-level timestamps, silence
filtering (so the model does not hallucinate text over silence), and a short glossary of names and
terms (brand names, English words) given as a prompt. Details in `references/transcription.md`.

### 3. Review the transcript
Read all of it, sentence by sentence, before touching the edit. One wrong caption makes the whole
video look amateur. Never edit the raw transcript: write corrections to a separate file, each with
a before, an after and a reason. Mark uncertain words instead of guessing; if two models disagree
on a word, that is a flag. Then re-align: corrected words need exact timings, so rebuild the word
list and compare it with the raw timings. You read text and look at images; you do not hear. Do
not say you listened, and do not replace spoken words with a script even if one exists, because
captions must match what was said.

### 4. Captions
A caption is a unit of meaning, not a word count. Split by phrase, not every N words. One phrase
per cue, at most two lines, measured in pixels (Hebrew and Latin letters differ in width), kept
on screen briefly after the last word, with a tiny gap between cues so they do not flicker.
Never drop, merge into silence or invent words. Build SRT and VTT from the same list as the
on-screen captions so they always match. Placement and mixed-script rules are in
`references/captions.md`.

### 5. Edit plan
Before any animation, write the plan as a file and show it as a table. Every event has a start,
an end, a type (overlay, full screen, top graphic, zoom), and a **purpose tied to a specific
sentence**. An event without a purpose does not go in. The human approves the table; a script then
builds the timeline, captions and zooms from it.

### 6. Scenes in HyperFrames
A scene is a small web page: HTML for structure, CSS for look, an animation library for motion,
played back frame by frame. Keep the page deterministic and time-driven: one paused timeline per
scene, registered under the composition id; no wall-clock time and no unseeded randomness. Hide
every element that enters later from the very start in CSS, otherwise it flashes in the frames
before its entrance. This is the most common bug. Keep fonts, images and music inside the
project; a render that depends on the internet will break. Render graphics with a transparent
background and composite them over the untouched source with FFmpeg, so the source keeps its
original quality.

### 7. Inspect, twice
- **Automatic**: the tool's lint and structure checks (missing files, code errors, unreadable or
  too-small text).
- **Visual**: snapshots at every key moment: each object's entrance, middle and end, before,
  during and after each zoom, roughly every few seconds, and captions at the largest and
  smallest text in both Hebrew and English. Look at them yourself. Photograph, fix, photograph
  again until clean. "Looks fine" without a frame is not a result.
Typical things to catch: text smaller than the captions, an object appearing before its word, a
missing hidden initial state, a covered face, text in a platform UI zone, a font that did not
load, reversed Hebrew or number order.

### 8. Render and master
Composite, mix the music under the voice, adjust pace, then **measure the final file** rather than
trusting the settings. Defaults: -14 LUFS integrated loudness and a true peak of at most -1 dBTP
(the usual delivery level for social platforms). Do it in two passes: measure, then correct, then
measure again. If the speech was recorded quietly, raise it before mixing in the music. Deliver the
MP4 (1080x1920 for a reel), SRT and VTT, and a short report with the measured numbers.

## Design principles (the visual language)

- **Every element does what is being said, at the moment it is said.** The difference between
  cheap and professional editing is not the number of effects; it is whether each one carries
  meaning.
- One concrete object per idea, starting on its word. Think action, then response, then result.
  Show the problem before the solution. Objects that return through the video create continuity.
- Build an idea from three beats: something happens, something responds, the result is visible.
  Most viewers watch without sound, so the picture must carry the idea alone.
- One font family in two weights. One main colour plus one or two accents, each with a fixed
  meaning (for example warm for a problem, cool green for solved).
- Motion has a house style: how things enter and leave, how fast, how a zoom behaves (a short
  centred punch-in, a hold, a sharp return). Energy only where something happens.
- Overlays sit below the captions as one centred group. Full-screen scenes are short and mostly
  filled. Music is always present but low under the voice.
- Pace: a brisk speaking rate can be reached by speeding up, never by slowing down; do not shift
  pitch.
- Never use a fake logo or a fake product screenshot. Generated illustrations should share one
  flat style and have clean cut-outs without halos.
- To learn from a video you admire, analyse it (scene count and length, how text enters, colours,
  what moves) and write down what suits your own design file. The aim is to learn, not to copy.

## Working with the user

- The user is the editor-in-chief: they approve at the gates and give notes in the form
  "time, what I see, what I want". Specific beats vague: "at 0:12 the chart appears before I say
  three" is actionable; "this is not good" is not.
- Sort every note into **this video only** or **a lasting rule**. Lasting rules go into the
  project's rules file or design file, with the date, so the next video starts better. The agent
  does not remember earlier conversations; those two files are its memory.
- When something breaks: find the cause, check the tool's current documentation (these tools
  change quickly), explain it in a sentence, fix it in the shared script, and record the lesson.
- Never silently swap a model or a tool. If the planned one failed, say so and say what replaced it.

## Project layout and the two memory files

```
my-video-editor/
  CLAUDE.md         the rules: steps, gates, what never to do
  DESIGN.md         the look: font, colours, captions, motion
  scripts/          the mechanical steps, written once
  assets/fonts/     the font, stored locally
  videos/<name>/    source/  transcript/  scenes/  checks/  exports/
```

Templates for both files are in `references/templates.md`.

## Never

- Never edit the source file.
- Never say you listened to the audio. You read text and look at images.
- Never replace spoken words with the written script.
- Never put captions or graphics over the face or in a platform UI zone.
- Never say "done" without snapshots and a measured final file.
- Never leave a fix only in one video; put it in the shared script or the rules file.
