# Captions: detailed rules

## Splitting
- Split by expression, never by a fixed number of words. Tools that cut every four or five words
  produce captions that stop in the middle of a thought. Read the sentence and decide where it
  breathes.
- One caption is one full expression, at most two lines. If a line would be too wide, split it
  at a natural pause rather than shrinking the text.
- Words are never dropped and never invented. The caption list is built from the corrected,
  re-aligned word list, so each word keeps its own time.

## Timing
- A caption starts with its first word and stays a moment after the last word (roughly half a
  second) so it can be read.
- Keep a very small gap between consecutive captions, so the text does not appear to flicker.
- Generate SRT and VTT from the same list that drives the on-screen text. Then they cannot
  disagree.

## Measuring width
- Measure a line in rendered pixels in the browser, not in characters. Hebrew and Latin letters
  have different widths, so a character count is wrong for mixed text.
- Render each caption line in the real font and check that it fits inside the safe area.

## Style
- White text, bold weight, thin dark outline or soft shadow so it reads on any background.
- Big enough to read at a glance on a phone. No other on-screen text should be smaller than the
  captions.
- A highlighted word, if used, gets a restrained accent colour. The highlight must be earned by
  the meaning, not applied to everything.

## Placement
- Keep the captions out of the face and out of the platform interface areas. On a vertical
  video those are typically the bottom strip (account name, description, buttons) and the right
  edge (like, comment, share).
- Place them just below the speaker's chin, horizontally centred, with a small margin. Find the
  face position from the sampled frames. If the speaker moves in the frame, check again and move
  the captions.
- Check on a real frame, not by reasoning about coordinates.

## Mixed Hebrew and English
- Latin terms inside Hebrew text need bidirectional isolation, otherwise the order of the words
  or the punctuation around the term can flip. Isolate the Latin run, and attach a Hebrew prefix
  to it with a maqaf (for example the Hebrew letter bet, a maqaf, then API).
- Numbers and units are the other common source of order bugs. Render them and look.
- Check the result on a rendered frame in the final font; these bugs only show on screen.
