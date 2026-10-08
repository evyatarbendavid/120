# Templates for the two memory files

The agent does not remember earlier conversations. These two files are its memory, so anything
that should hold for every video belongs in one of them. Copy, then adapt to the user's channel.

## Rules file (CLAUDE.md in the project)

```markdown
# Video editor: how we work

## The contract
- Input: a finished, cut video, optional extra media, a music track.
- Output: final.mp4 (9:16), SRT and VTT, a measured inspection report.
- The source file is never modified.

## Steps (stop where it says APPROVAL)
1. Ingest: copy, hash, extract audio and frames, describe where the face is.
2. Transcribe locally, with word timestamps and a glossary.
3. Review every segment. Corrections and flags go in a separate file.
   APPROVAL: show flagged moments with timestamps.
4. Re-align corrected words and compare with the raw timings.
5. Captions: one phrase per cue, measured width, below the chin.
6. Edit plan: every event has start, end, type and purpose.
   APPROVAL: show the plan as a table.
7. Build the scenes. One paused timeline per scene.
8. Inspect: automatic checks plus snapshots at every key moment.
   APPROVAL: send a draft to watch on a phone.
9. Render, composite, mix music, set pace, master to the target loudness.

## Never
- Never say "listened". Read text, look at images.
- Never replace spoken words with the script.
- Never silently swap a model or a tool. Report it.
- Never cover the face or use a platform interface area.
- Never say "done" without snapshots and a measured final file.

## Lessons learned
(every correction from a review goes here, with the date)
```

## Design file (DESIGN.md in the project)

```markdown
# Design: how our videos look

## Identity
- Font: one family, two weights, stored in assets/fonts.
- Main colour, plus one or two accents per video, each with a recorded meaning.

## Captions
- Text colour, weight, outline, size. One phrase per cue, at most two lines, just below the chin.
- Rule for Latin terms inside Hebrew (isolate, Hebrew prefix with a maqaf).
- No other on-screen text smaller than the captions.

## Visuals
- One concrete object per idea, doing what is said, starting on its word.
- Action, then response, then result. Problem before solution.
- Illustration style: one style description per video, backgrounds removed.
- Forbidden: fake logos, fake product screenshots, decoration without meaning.

## Motion
- Overlays sit below the captions as one centred group.
- Full-screen scenes: short, animated, mostly filled.
- Zoom: centred, quick ease, small percentage, hold, sharp return.

## Audio
- Speech at full level. Music always present, low under the voice.
- Pace target, speed up only, never slow down.

## Reference videos
(links, and one line on what exactly works in each)
```

Write the files in the language the team works in; the agent follows them either way.
