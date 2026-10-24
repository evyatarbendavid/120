---
name: "seedance-prompt"
description: "Turn a rough video idea (Hebrew or English) into a complete, structured Seedance 2.5 prompt ready to paste into Higgsfield."
---

# Seedance 2.5 Prompt Builder

Take the user's video idea, however rough, and return ONE production-ready Seedance 2.5 prompt, written in English, in a single copyable code block.

## Step 1: Extract or default the essentials

Pull these from the idea. Ask only if something critical is missing AND there is no sensible default (max 2 short questions, in one message). Otherwise use the defaults and list them under "Assumptions".

| Field | Default |
|---|---|
| Duration | 5s for tests, 10-15s for real content (max 30s) |
| Aspect ratio | 9:16 (TikTok / Reels) |
| Number of shots | 1 shot per ~3-5 seconds |
| Style | Clean, modern, natural color, soft film grain |
| Audio | Ambience + foley, no music, no dialogue |
| References | None, unless the user mentions uploading images/video/audio |

If the idea is in Hebrew, understand it in Hebrew but write the prompt in English (the model follows English best).

## Step 2: Write the prompt in this exact section order

One continuous block, each section labeled in caps. Never skip a section; skipped sections produce predictable failures (e.g. no CAMERA = random movement).

1. **GLOBAL STYLE**: genre, look, color grade, film stock/grain, aspect ratio, shutter feel. End with global exclusions (e.g. "No text overlays. No slow motion.").
2. **SCENE**: one-line logline: who does what, where, with what mood.
3. **CHARACTERS**: each character named (e.g. "Maya") with age range, build, hair, wardrobe. Reuse the exact same name everywhere after.
4. **LOCATION**: space, props, time of day. Kept separate from characters.
5. **FIRST FRAME AND BLOCKING**: exact starting positions (e.g. "Maya at x 40%, y 60%, facing camera-left").
6. **SHOT-BY-SHOT**: `SHOT 1 (0-4s): shot type, action, one primary change, end state.` Separate shots with `HARD CUT.` Time ranges consecutive, non-overlapping, covering the full duration.
7. **CAMERA**: per shot: framing, lens/focal length, height, movement (dolly push-in, locked tripod, slow orbit, handheld).
8. **PHYSICS**: only what moves: hair, fabric, liquid, smoke, particles.
9. **LIGHTING**: motivated source, direction, quality, color temperature.
10. **AUDIO**: use brackets: `(music)`, `<sound effects>`, `{dialogue}`. End with exclusions ("No music." / "No dialogue.").

## Rules that prevent common failures

- **One action per time range.** Never pack several actions into a second. Timestamps are a pacing budget, not frame-accurate.
- **Show, don't imply speech.** Never put quoted thoughts in action text ("a look that says 'really?'"); the model will voice it. Describe visible behavior ("eyebrows lift, she holds the stare").
- **Exclusions as separate sentences.** Write "Do not show a logo." not "a shirt without a logo." The model is bad at subtraction.
- **On-screen text is unreliable.** Avoid readable signs, UI text or subtitles in the prompt; add them in editing. Mention this in Notes if the idea depends on text.
- **Keep it concrete.** No vague words like "epic", "beautiful", "cinematic" without saying what makes it so (lens, light, movement).

## References (only if the user uploads material)

One role sentence per material, each with its own exclusion:

- `@Image 1 defines Maya's face, hair and build. Do not use the background or clothing from the image.`
- `@Video 1 defines the camera movement and pacing only. Do not use the people or location in the video.`
- `@Audio 1 defines Maya's voice tone. Do not use the words spoken in the audio.`

If several images show one subject, say so: "@Images 1-3 all define one character, Maya." Never map several images to several characters in one sentence. Stay within ~1-8 image subjects for stability.

## Dialogue

Default to no dialogue. If the user wants speech:

- Declare the language before the line: `Dialogue language: natural Israeli Hebrew. Maya says: {...}`
- Keep lines short (one sentence per ~3s).
- For Hebrew, add a Note: Hebrew lip-sync and pronunciation may be unreliable; test with a 5s clip first, or plan a voiceover in editing instead.

## Output format

Return exactly this, nothing more:

**Settings:** duration, aspect ratio, mode (text-to-video / image-to-video / references)

```
[the full prompt]
```

**Assumptions:** bullet list of defaults you chose (only if any).

**Notes:** 1-3 bullets max: the riskiest part of this prompt and what to tweak first if the result is off.

Do not offer multiple prompt variants unless asked. If the user asks for iteration after a generation, ask what went wrong (or read their description) and change only the section responsible.
