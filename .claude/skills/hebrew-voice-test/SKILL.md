---
name: hebrew-voice-test
description: Prepares Hebrew text for text-to-speech, writes test sentences and a scoring table to compare voice tools. Triggers: Hebrew voice, Cartesia, ElevenLabs, קרטזיה, קול.
---

# hebrew-voice-test

## When to use (full trigger list)
Prepares Hebrew text for text-to-speech reading, writes 8 test sentences that expose Hebrew pronunciation and stress problems, builds a blind A/B test sheet and a scoring table for comparing two voice services (for example ElevenLabs vs Cartesia) on the same lines, and runs a consent checklist before any voice cloning. Use when the user asks for a Hebrew voice test, Hebrew TTS check, preparing a script for text-to-speech, comparing ElevenLabs and Cartesia, test sentences for a voice, a scoring table for voices, or complains that a voice mangles Hebrew words. Hebrew trigger words - קרטזיה, קול, בדיקה.

Problem: Hebrew text-to-speech often reads a word wrong, puts the stress on the wrong syllable, reads English names oddly, or stumbles on numbers. Each service fails on different words. The only way to know which service is better FOR THE USER'S TEXT is to give both the exact same sentences and listen.

This skill does not decide which service is better. It makes the test fair and gives the user a scorecard. You cannot hear audio, so you never say how something sounded. Only the user's ears and scores decide.

Always talk to the user in Hebrew. Use plain Hebrew, short sentences, no jargon without a one-line explanation. These instructions are in English because it is more reliable for the model.

## Step 0: Ask first (ONE numbered message, then wait)

1. What is the text for? (reel voiceover, ad, course, podcast.) Paste the real script if there is one. If there is no script, say you will use a sample set.
2. Which two services are being compared? Default suggestion: ElevenLabs and Cartesia. Which plan and which model/voice is each using? (If the user does not know, tell them to look at the model selector in each tool and write down the name; the name goes in the result file.)
3. Voice type: (a) a ready-made voice from the service library, (b) a clone of the user's OWN voice, (c) a clone of someone else. For (c) go to the "Consent checklist" below BEFORE anything else. For the comparison itself, (a) is enough and is the fairest: a clone adds a second variable.
4. Does the text contain English words, brand names, numbers, dates, prices, abbreviations?
5. Who is speaking: a man, a woman, or neutral? Hebrew first-person verbs and adjectives depend on the speaker's gender, so write every test sentence in the speaker's own gender and never guess it. (If the user does not say, ask once; if there is still no answer, write gender-neutral sentences.)
6. Does the user want to continue to cloning after the test? (Only then bring up the consent checklist.)

Do not continue until the user answered. If the user answers only part, state your assumption in one line and continue.

## Step 1: Prepare the Hebrew text for reading ("reading version")

Take the script and produce a reading version. Never change the meaning and never add words the user would not say. Rules:
- Short sentences: split any sentence over about 15 words at a natural breath.
- Numbers, prices, dates, times: write them as Hebrew words in the right grammatical form (for example ninety-nine shekels, the fifteenth of November, two minutes, each written out in Hebrew letters and in the correct gender). Do not rely on the service to read digits in Hebrew. Keep a list of every number you changed.
- English names and tools: keep Latin letters first (for example `Claude`). Keep the Hebrew prefix letters exactly as the user wrote them (a letter attached to an English name with a hyphen). Do NOT rewrite them into extra words. A prefix attached to an English name is a known weak spot, so test it as written and change it only if the test shows a problem. Only if the user reports that the service mangles a name, add a phonetic Hebrew spelling for THAT name and list it in the fix list. Never replace silently.
- Abbreviations: spell out (for example the abbreviation for shekels becomes the full word, and "etc." becomes its full Hebrew form).
- Ambiguous words: Hebrew written without vowel marks can be read in two ways (for example the word ספר: book, barber, he counted). List every ambiguous word you find and ask the user which meaning is intended. Then either rephrase the sentence so the meaning is clear from context, or (as an experiment) add vowel marks (niqqud) on that one word only. Whether a service honors niqqud is NOT known: tell the user to test one sentence with and without, and record the result.
- Punctuation controls pauses: comma for a short pause, period for a full stop, question mark for a question. End every sentence with `.`, `?` or `!`. Avoid long dashes, ALL CAPS for emphasis, and many exclamation marks.
- Service-specific pause tags differ (some services support a break tag, some newer models do not). Do NOT add tags unless the user says their service supports them; use punctuation and shorter sentences instead.

Output exactly three things:
(a) the reading version, in one block, ready to paste;
(b) a fix list as a table: original word or phrase | what I changed | why;
(c) only if the fix list has words that need a respelling: a pronunciation list as JSON, one entry per word, in the format of Cartesia custom pronunciation dictionaries: `{"text": "<word as written>", "pronunciation": "<how it should sound, spelled the way it sounds>", "case_sensitive": false}`. Tell the user (in Hebrew) that Cartesia describes this dictionary as a simple search and replace that happens before the text reaches the model, and that it can be created in the playground or through the API. ElevenLabs has its own pronunciation dictionaries (in its Studio and API), and its Eleven v4 model accepts IPA written between slashes. Whether either dictionary works well for Hebrew is NOT confirmed: tell the user to test ONE entry first and record the result.

STOP POINT 1: ask the user in Hebrew whether the reading version is approved and what to fix. Wait for approval before step 2.

## Step 2: Write 8 test sentences (T1 to T8)

Use the user's own topic and vocabulary where possible. Each is 5 to 15 words (T7 is shorter, T8 is longer). Cover:
- T1: ambiguous reading or stress (for example the word ספר used in a sentence where context makes the meaning clear to a human).
- T2: a number, a price and a date in one sentence.
- T3: two English brand or tool names inside a Hebrew sentence.
- T4: a question (does the intonation rise at the end?).
- T5: a list of 5 to 7 items (breath and rhythm).
- T6: an emotional line, excited or serious, whatever the user needs.
- T7: a very short line, 3 to 4 words (tone on short phrases).
- T8: a real paragraph of 3 to 4 sentences from the user's script (flow).

Write every test sentence only once, with numbers written as words, and print the sentences ready to paste with nothing else mixed into the block (no notes, no digit versions). Only if the user explicitly wants to test digit handling, add a separate extra line labelled T2a with the digits version.

If the user has no script, write 8 original sentences that follow the coverage list above, on a neutral everyday topic, and say they are a sample set. (The PDF this skill came with also contains a ready sample set that the user can paste in; if the user pastes it, use it as is.)

STOP POINT 2: ask the user in Hebrew whether the 8 sentences are approved. Wait.

## Step 3: Blind test sheet (fair test)

Tell the user how to run it, in numbered Hebrew steps:
1. In each service use the same 8 sentences, one voice per service, default speed and default settings (write the settings down). Set the language to Hebrew explicitly wherever the tool has a language field. In ElevenLabs choose a model that lists Hebrew (Eleven v3 or v4 at the time of writing, check the current models page); the Multilingual v2 and Flash v2.5 models did not list Hebrew. In the ElevenLabs API there is a `language_code` field for this, and it is not supported on Multilingual v2. In Cartesia, choose from the Hebrew voices and audition two or three on one short sentence first. Cartesia's own Hebrew page names two example Hebrew voices, Ayala and Noam, as a place to start.
1b. Preview first: generate one short sentence in each tool before the full set, to check the voice, the language setting and the speed.
2. Generate each sentence ONCE per service. No cherry picking. (If the user wants "best of 3", it must be 3 tries for both services.)
3. Save the files with neutral names: `T1_X.mp3`, `T1_Y.mp3` and so on. Choose at random which service is X and which is Y, separately for each sentence, and write the key on a separate paper or in the key file. Best: ask a friend to rename the files so the user does not know which is which.
4. Listen with headphones. First with eyes closed, then again while reading the text.

Create the key as a table the user fills BEFORE listening: sentence | X is | Y is. If the user wants, generate a random assignment for them (use a script or a coin flip you can show) and keep it in a file `test-key.md`, telling the user not to open it until scoring is done.

## Step 4: Scorecard (blank table and fill-in)

Create `voice-test-scorecard.md` with one row per sentence and per file (X, Y). Scores 1 to 5 where 5 is best:
- Pronunciation (הגייה): every word correct?
- Stress (הטעמה): is the emphasis on the right syllable?
- Rhythm (קצב): does it sound like a person or like a reading machine?
- Voice quality: clean, no robotic artifacts, no clipped endings? (Hebrew column label: איכות)
Plus two free columns: "words it got wrong" and "fix that worked" (respelling, niqqud, punctuation, shorter sentence). Write the column headers in Hebrew.

After the user fills it and reveals the key: sum per service, show per-sentence gaps, list each service's 3 most annoying mistakes, and say which sentence types each service lost on (numbers, English names, questions...). Then ask in Hebrew: which of the two would you publish under your own name, and what would you still fix by hand? Report the result as "according to your scores" (in Hebrew), never as a general fact about the services.

If the user pastes scores, do the arithmetic with a script or show the math. Do not guess scores.

## Step 5: Save results

If you can write files, save in the user's folder: `reading-version.md`, `fix-list.md`, `test-sentences.md`, `test-key.md`, `voice-test-scorecard.md`, and after scoring `result.md` (services and model names with date, settings, totals, mistakes, fixes that worked). If you cannot write files, print each as a code block and tell the user to save them.

## Consent checklist (voice cloning)

Cloning means making a copy of a real person's voice. The test above does NOT need cloning. Before the user clones any voice, ask these and require a yes to each:
1. Is it the user's own voice, or does the owner of the voice know and agree? (For anything that will be published, get a clear written yes: a message is enough as a record.)
2. Is it NOT a person who did not agree, a famous person, an actor, a singer, a politician, a child or a person who passed away? If it is: stop. Do not help clone it. Suggest a library voice or a voice designed from a text description.
3. Will it be used only for what the owner agreed to (what content, which platform, for how long)?
4. Does the service's own terms and plan allow cloning for this plan and use? Tell the user to read the plan page and the terms; do not quote plan names, prices or limits from memory.
5. Will the user mark the content as AI-generated voice where the platform or law requires?
If any answer is "no" or "not sure", do not continue with cloning and say why in one sentence.

## When something is missing

- No audio tool or no way to play audio: you do not need one. The user listens in the services' own websites. You prepare text and tables only.
- The user has only one service: do the text preparation, the 8 sentences and the scorecard anyway, and suggest running the second service later on the same sentences.
- The user's service does not offer Hebrew or a Hebrew voice: say so and tell them to check the service's language page; do not suggest workarounds that change the meaning.
- The user has no script: use the sample set above.

## What NOT to do

- Do not claim one service sounds better. You did not hear it.
- Do not state prices, free-plan allowances, model names or language lists from memory. Tell the user to check the service's pricing and models pages (name the page type, not a number).
- Do not help clone a voice of a person who has not agreed.
- Do not change the meaning of the user's words to make the audio sound better.
- Do not promise perfect Hebrew. Keep the fix list so the fixes can be repeated next time.

## Sources and credits

The original idea (give two voice tools the same Hebrew sentences and compare) comes from a reel by Evyatar Yzhak (https://www.instagram.com/reel/DeydKf8MW7H/). The creator's own guide is private (sent in direct messages) and was not available, so this skill is a new build, not a copy.
Public material used as input, rewritten here (no text copied):
- Cartesia, Hebrew page: https://cartesia.ai/languages/hebrew (check pronunciation with a fluent reviewer, write ambiguous numbers and dates the way they should be spoken, preview short passages first).
- Cartesia docs, custom pronunciations: https://docs.cartesia.ai/build-with-cartesia/capability-guides/custom-pronunciations
- Cartesia docs, Sonic prompting tips: https://docs.cartesia.ai/build-with-cartesia/sonic-3/prompting-tips
- ElevenLabs official skills, text-to-speech (MIT License): https://github.com/elevenlabs/skills (language_code and text normalization notes).
- ElevenLabs docs, models and text best practices: https://elevenlabs.io/docs/overview/models
- Independent public Hebrew TTS comparison snapshot from March 2025 (no license stated, so only referenced): https://github.com/danielrosehill/Hebrew-TTS-Providers

