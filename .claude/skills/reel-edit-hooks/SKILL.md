---
name: reel-edit-hooks
description: Edit a short vertical video (Instagram Reel, TikTok, Shorts) around a strong hook and proven retention craft - pick and score the hook, move the best moment to the start, cut dead air, set a cut and caption rhythm, design the sound and the ending, and learn the pacing from reference reels the user admires. Use when the user wants a reel edited, a hook written or fixed for an existing video, a video that "holds people", "make the first seconds stronger", "edit this like the viral ones", or in Hebrew "תערוך לי ריל עם הוק", "הוק חזק לסרטון", "שהאנשים יישארו עד הסוף", "תערוך כמו הוויראליים". It is the creative layer on top of ig-reel (hook formulas and scoring) and ai-video-editing-workflow (the technical pipeline).
license: MIT
---

# Reel edit with hooks

Written for this repository. The numbers below are craft rules of thumb to test on the owner's own
account, not Instagram rules: say so, and compare results with `ig-account-insights` when it is set up.

## How it fits with the other skills

- `ig-reel`: 26 hook formulas (`hooks.json`), `hookscore.py` to rank hook lines, `beats.py` for timing.
  Use its formulas and scripts; do not rewrite them here.
- `ai-video-editing-workflow`: the technical pipeline (transcript, captions, edit plan, HyperFrames
  scenes, checks, loudness). Run it for the actual build.
- `talking-head-recut` and `embedded-captions`: overlays and cinematic captions on talking footage.
- `open-social-link`: look at reference reels (frames, transcript, cut count).
- `ig-viral`, `ig-audit`, `ig-account-insights`: what works in the niche, and what worked on the account.

## Steps

1. **Know the footage and the goal.** Watch it (`open-social-link` on the file), read the transcript, and
   write one line: who it is for, what one thing they should take away or do. Ask only what is missing.
2. **Find the best moment.** Mark the strongest 1-2 seconds: the surprising line, the result, the
   mistake, the visual payoff. That moment, or a line that promises it, is what the video opens with.
3. **Choose the hook, as a pair.** Every reel has a spoken hook (the first ~2 seconds of speech) and an
   on-screen hook (the first frame's text and image, read before it is heard). They must agree and not
   be the same sentence. Pick 3 formulas from `ig-reel/hooks.json` that fit the footage, write one line
   for each, and rank them with `python3 ../ig-reel/hookscore.py hooks.txt`. Use the winner; show the
   user the top two and why. Never promise something the video does not deliver in the first third.
4. **Re-order for retention.** Cold open on the hook or the payoff, then context only as needed, then
   the rest. Cut: pauses, "um", false starts, the greeting, the throat-clearing before the point.
   Keep one breath of silence only where a joke or a reveal needs it.
5. **Set the rhythm.** Plan a visible change every 2-4 seconds in a talking video (a cut, a punch-in
   to a different crop, b-roll, a graphic, a caption emphasis) and faster for pure montage. Alternate
   the change types so it does not feel mechanical. Write the plan as a table: time, what changes, why.
   Check it with `python3 ../ig-reel/beats.py script.txt --target <seconds>`.
6. **Captions.** Phrase by phrase, never mid-thought, big enough for a phone, inside the safe area (away
   from the bottom strip and the right edge), highlight one word at a time at most. Hebrew right-to-left
   and Latin words need the checks in `ai-video-editing-workflow`.
7. **Sound.** Voice first and clear; music low under it and cut when the line matters; a short sound
   effect on a cut or a reveal only if it earns its place. Measure loudness (about -14 LUFS).
8. **Ending.** Close the loop: the last line or frame hands back to the first, so replays feel natural,
   or deliver the payoff and ask for one action (follow, save, comment a keyword), not three.
9. **Cover and first frame.** Pick a cover frame that reads in a small grid and shows the hook text
   clearly; check the first frame also works as a still.
10. **Check like a viewer.** Watch once with sound and once muted. At every second ask: would a stranger
    leave here? Fix the weakest 3 spots, then render.

## Learn from references (optional, strong)

When the user names reels they admire, run `open-social-link` on 2-3 of them and record for each: hook
formula used, length, number of cuts (so average shot length), caption style, music, ending. Average the
numbers and edit toward that pace and structure, copying the method and never the footage, wording or
voice. Say which numbers came from which reel.

## Deliver

Give: the chosen hook pair (spoken and on-screen) with its score, the edit plan table, the caption and
sound notes, and the render or the project files. In Hebrew unless the video is in another language.
After posting, offer to compare the result with the account's other reels.

## Never

- Never use a hook that misleads about the content or promises a result the footage does not show.
- Never copy another creator's footage, script or voice.
- Never claim a number as an Instagram rule; call them tested habits and measure them.
