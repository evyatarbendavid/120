# Transcription and transcript review

## Why it matters
The transcript is the base of the whole edit. Captions are built from it, and every animation is
timed to a word, so the output must have a timestamp for every word.

## Local models
- Run transcription on the user's own computer; it avoids per-minute fees and keeps the footage
  private.
- For Hebrew, prefer a Whisper model tuned for Hebrew (the ivrit.ai models are trained on very
  large amounts of Hebrew speech) over the generic multilingual model. There is typically a full
  version (more accurate, slower) and a turbo version (faster); use the full one for the main pass
  and the other as a second opinion on a doubtful word.
- Heavy models and their Python environment belong on the user's computer, in a project-local
  virtual environment, not in a cloud session.
- Fonts, images and music used later also live inside the project folder.

## Three settings worth knowing
1. **Word-level timestamps**: each word gets a start and an end. Without them, captions and
   animations cannot be timed precisely.
2. **Silence filtering (voice activity detection)**: skips stretches without speech so the model
   does not invent text over silence. Occasionally it swallows a word, so look at the transcript
   afterwards.
3. **A glossary prompt**: a short list of names and terms (brand names, English words) handed to
   the model as a hint. This noticeably reduces the most common errors.

## What typically goes wrong
- **Names and brands**: spelled phonetically instead of as the brand writes them.
- **English terms inside Hebrew**: written in Hebrew letters (a product name rendered as a
  Hebrew transliteration) or the opposite.
- **Numbers**: split by a space, written as words once and digits another time, or version
  numbers broken up.
- **Words split or merged**, or a word that spilled into the next one.
- **Correct sound, wrong meaning**: a word that sounds right but makes no sense in context.
  Reading the whole sentence catches this.

## Review procedure
1. Read the entire transcript, one sentence at a time, before any editing.
2. Write every fix to a corrections file: before, after, reason. Do not edit the raw output.
3. Mark words you are not sure about, with the reason, instead of choosing silently.
4. Show the flagged moments with their timestamps and wait for the user's decision.
5. Re-align the corrected words so each has exact timing, and compare with the raw timings.
6. A final read before rendering, because a single wrong caption lowers the whole video.

If the user has a written script, it helps to understand words, but it never replaces what was
actually said.
