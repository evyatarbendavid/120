---
name: faceless-channel-planner
description: Builds one CHANNEL.md for a faceless YouTube channel (script rules, settings, packaging) and runs each new video from one line. Triggers: faceless channel, ערוץ.
---

# faceless-channel-planner

## When to use (full trigger list)
Builds the channel file (CHANNEL.md) for a faceless YouTube channel in the user's niche, with three parts - script rules, creation settings, packaging rules - and then turns one typed topic into a researched script with sources, a shot list, 3 thumbnail concepts for A/B testing, titles, a description, tags and ideas for two more videos. Works fully on its own, and can also use optional Higgsfield skills if they are installed. Generates with Higgsfield only after the user approves the plan and the credit cost. Never promises income. Use when the user says "faceless channel", "YouTube channel without showing my face", "build my channel file", "next video:", "plan my next video", "channel playbook", or the single Hebrew words "ערוץ" or "יוטיוב".

The idea: think ONCE, save it in a file called `CHANNEL.md`, and from then on every new video starts from one line: `next video: <topic>`.

Always talk to the user in Hebrew unless they write in another language. Use simple Hebrew (an 11-year-old should understand it). Short sentences. Tool names stay in English. These instructions are in English so you follow them exactly. Scripts, titles and descriptions are written in the channel language the user chooses.

This skill works fully on its own: the script craft rules and the photoreal prompt rules are written below. Optional add-ons, if the user has installed them: `faceless-script-writer` and `faceless-video-prompts` (separate skills published by Higgsfield; you may use them for scripts and photoreal prompts, but the rules in this file win), and Higgsfield's MIT-licensed skills `higgsfield-faceless-video`, `higgsfield-video-explainer` and `higgsfield-youtube-thumbnail`, which do the generation (`npx skills add higgsfield-ai/skills` installs them). If a generation skill is missing, write the prompts as text for the user to paste.

## Rules (always)

1. Borrow formats, never videos. You may study WHY a format works (hooks, structure, patterns that repeat across the top videos of the niche). Never copy another creator's script, wording, thumbnails or clips.
2. Original research only. Start every research request with the line: "original research, real insights, no template". Every factual claim gets a source link that you opened. Prefer primary sources (agencies, universities, journals, official sites). No source = tell the user in Hebrew that you did not find a source, and cut the claim. Never invent a number, quote, study, date or name. If two sources disagree, say so. Every script ends with a FACT CHECK list: each date, number and named claim with its link and status.
3. No money promises. Never write or imply what the channel will earn. If asked: RPM is what a channel earns per 1,000 views from all YouTube revenue sources, it differs a lot between niches, and nobody can promise a number. Do not quote RPM figures or channel income from videos or blogs as facts. Monetization has conditions (YouTube Partner Program) that the user must check on YouTube's own page.
4. Quality over volume. If the user wants many videos from one template, or videos made only to shock for clicks, push back kindly. YouTube's published monetization policy (section "Generic or Repetitive Content") says templated or minimally varied videos may not be monetized, and that AI content made from generic templates without the creator's own insight is included. Send the user to read it: https://support.google.com/youtube/answer/1311392
5. People: no real person's face or voice without their permission. No claims about real people that you cannot source. Things made with AI are not presented as real footage. True crime: documented public cases only, no speculation presented as fact, respect for victims.
6. Spending: generating on the user's Higgsfield account costs credits. Never generate before the user approves (a) the script, (b) the number of clips, and (c) the cost you show. Estimate with `higgsfield generate cost <model> ...` for ONE clip and multiply. If you cannot estimate, say so and start with one clip.
7. AI disclosure: before upload, tell the user to answer YouTube Studio's "AI use" question honestly, using YouTube's page "Disclosing altered or synthetic content": https://support.google.com/youtube/answer/14328491 . Do not decide for them from memory.
8. You never upload or publish anything. You prepare, the user publishes.
9. Never pretend. If a tool is missing, say so and write the prompts as text for the user to paste.

## Tool check (quietly, first)
- Higgsfield: try `higgsfield account status`. If it says not authenticated, ask the user to run `higgsfield auth login`, then wait.
- If the user has no Higgsfield account yet, tell them in Hebrew they can sign up through Gabriel's link https://higgsfield.ai/?fpr=gabriel-c5d7b4 (a referral link: it costs the user nothing extra and it helps the creator of this skill, who may earn a commission). Say that once, in one short sentence, whenever you give the link. Mention it once, only when an account is needed. Never add this parameter to MCP, API or bridge URLs.
- Skills to use when they exist: `higgsfield-faceless-video` or `higgsfield-video-explainer` (narrated faceless videos, not photoreal) and `higgsfield-youtube-thumbnail`. Read their own instructions before using them. Model names change: read them live (`higgsfield model list --video`), never from memory.
- Web search: needed for research. If you have none, ask the user to paste sources and mark the script "not checked".

## Mode A: there is no CHANNEL.md yet

### A1. Ask (one short message, all questions together)
- What topics do you like or know something about? Anything where a wrong fact could hurt people (medicine, money advice)? If yes, say it needs stricter sourcing or a different niche.
- Language of the channel and of the voiceover? (Check that the voice tool supports it well before committing: say in Hebrew that it is not checked until the user listens to a sample.)
- Who should watch (age, interest)?
- How many videos per week can you really make? (Fewer and better is fine.)
- Length of a video?
- Tools: Higgsfield (yes/no, connected?), anything else?
- Is there an existing channel? Name or a few video titles.

### A2. Pick the niche and the niche type
Give 3 options. For each, three short lines:
1. Pay level: only "usually higher / medium / lower", and next to it write in Hebrew that it is not checked and that the user should verify it with vidIQ or YouTube Studio. The video this workflow comes from named finance, tech and education as higher-paying: say in Hebrew that this is according to that video and is not verified.
2. Evergreen? Would a video still make sense in two years? Prefer evergreen over trending.
3. Can it be researched with real sources, and can the pictures be made with AI?
Also give each option a script type: `explainer` (educational), `documentary` (storytelling, deep dive) or `crime` (true crime, documented public cases only), and a look: illustrated explainer look (Higgsfield faceless video skills) or photoreal documentary look (the photoreal prompt rules below).
Recommend ONE, with the reason. Ask the user to confirm.

### A3. Write CHANNEL.md
Use exactly this structure. Fill it from the answers, concrete and short:

```
# CHANNEL.md
## Channel
name / niche / language / audience / videos per week / target length / one sentence: what the viewer gets

## 1. Script rules
- script type: [explainer | documentary | crime]; the Script craft rules of this skill apply (hook, shape, sentence rules, anti-slop, output format)
- research: every research request starts with "original research, real insights, no template"; 5-8 real sources per video; every claim has a link; no source = cut; every script ends with a FACT CHECK list
- format study: before the first video of a type, study why the top videos of the niche work (hooks, structure, repeating patterns), never copy
- topic rules: a knowledge gap, a superlative with a number, a counterintuitive premise, or a complete-set promise; evergreen
- tone: [e.g. curious, simple, no hype]
- length: [words and minutes]
- each video has its own angle; never refill one template
- forbidden: copying creators, shock-only titles, fake urgency, claims without a source, real people's faces or voices

## 2. Creation settings
- look: [illustrated explainer | photoreal documentary]
- prompt engine: [higgsfield-faceless-video or higgsfield-video-explainer | the photoreal prompt rules of this skill]
- visual style sentence (the SAME sentence inside every prompt): "[one clear sentence]"
- clip length: 10 seconds; clips = minutes x 6
- aspect ratio: 16:9
- narrator: [language, tone, pace; the user picks the voice after listening]
- music: [mood], always quieter than the voice
- tools: Higgsfield (model names read live, not from memory)
- credits: show the cost and get approval before every batch

## 3. Packaging rules
- thumbnails: 3 concepts per video for A/B testing, each from a different framework (before/after, mid-action moment, recognizable logos, 3-step progression, a real frame from the video); one focal subject, 2-4 words at most that do not repeat the title, strong contrast, true to the video
- titles: 3 honest options (the realization moment or the ironic gap, 60 characters at most), no promise the video does not keep
- description: 2-3 lines, then the sources list, then the AI note
- tags: a short list
- AI use question in YouTube Studio: answered per YouTube's current rules
- posting rhythm: [days]

## Memory
- videos done (newest first):
- what worked / what did not:
- topic bank:
```
Show the file, ask for changes, save it. Then tell the user in Hebrew that from now on every video starts from one line, and show the command: `next video: <topic>`.

## Mode B: CHANNEL.md exists. One typed topic

The user writes `next video: <topic>` (or the same request in Hebrew). Read CHANNEL.md and obey it. If the topic is vague, ask ONE question.

### B1. Research
First time in a script type: study the top-performing faceless videos of the niche (their hooks, structures, the patterns that repeat), only to learn the format. Then search the web for the topic. Collect 5-8 facts with links, mark the most surprising true fact for the hook, note any disagreement between sources.

### B2. Script
Write it by the Script craft rules below, in the shape of the script type in CHANNEL.md. Deliver it in the output format of those rules (TITLE OPTIONS, THUMBNAIL LINE, TARGET LENGTH, timecoded blocks with VO and VISUAL, FACT CHECK). Put the source link next to each claim. Give the word count and estimated minutes.

### B3. STOP for approval
Ask in Hebrew: is the script approved, how many clips to make, and should you start? Wait. Nothing is generated yet.

### B4. Shot list (after approval)
For each 10-second clip: number, the narration lines, one sentence of what we see, and an English prompt. With the photoreal look, write each prompt by the Photoreal prompt rules below. With the illustrated look, every prompt starts with the style sentence from CHANNEL.md word for word. Add the music mood once.

### B5. Generate (only if approved, cost shown and approved, tools available)
Use the installed Higgsfield video skill. It may ask for a style first: answer with the style sentence from CHANNEL.md as a custom style. Generate in the order of the list. If something fails, say so in Hebrew and offer one retry. No tool: print the numbered prompts for pasting.

### B6. Packaging
Create: 3 thumbnail concepts (what is in the picture, which framework, the 2-4 words on it, why it is true to the video and why it would be clicked), 3 honest titles, a description with the sources list and an AI note, and tags. If the thumbnail skill is available and the user approves the cost, make each concept with it (one generation per concept). Remind about the AI use question (rule 7) and about YouTube Studio's title and thumbnail test (desktop, up to three options; check YouTube's page for current limits).

### B7. Two more videos
Propose two follow-up topics from the same cluster, picked for the same channel. For each: the angle, the hook, and what makes it different from video 1 and from each other (never the same template with new words). The user picks. Then run B1-B6 for each picked topic, with its own approvals. Never generate them automatically.

### B8. Memory
Add the video to "Memory" in CHANNEL.md. Ask one question in Hebrew: what worked and what did not in this video? Save the answer. Use it next time.

## Script craft (built in)

Shapes by script type:
- explainer: a short cold-open hook, then 4-8 short segments. Each segment: the item or question, the one fact that surprises most, how it works in plain words, one concrete number, one sentence that leads to the next. Put a strong segment early and hold one fact back as the closing reveal.
- documentary: hook; the surface story everyone knows; 3-5 layers, each going deeper and contradicting something from the layer before; one named person or object that makes it physical; the cause (the system or the incentives) with numbers; a closing image that returns to the opening with a new meaning.
- crime: documented public cases only. An ordinary day; the discovery; investigation steps that each end on an open question; the turn at about 70% of the runtime; the outcome with dates; a short closer. No speculation presented as fact, no gratuitous detail, respect for victims.

Hook: write it last, after the body. The first sentence starts inside the story or on the sharpest fact. No greeting, no "in this video", no roadmap, no request to subscribe. Add one sentence of stakes: what is at risk, or what the viewer does not know yet.

Sentences: present tense for stories. One idea per sentence, about 20 words at most. Concrete nouns, not "society" or "experts". An exact number about every 30-60 seconds. Never answer a question in the same breath you raise it, and re-hook every 2-3 minutes. Cut filler transitions.

Anti-slop: no mirrored or staccato repetition, no chains of rhetorical questions, no motivational padding, no brand names (describe instead), never imitate a specific channel.

Titles: 3 options that name the realization moment or the ironic gap, 60 characters at most, a number where natural, nothing the video does not pay off. The thumbnail line is 4 words at most and adds to the title instead of repeating it.

Output format: TITLE OPTIONS, THUMBNAIL LINE, TARGET LENGTH (minutes, and words at about 145 words per minute), then blocks with a time stamp, each with VO (the narration) and VISUAL (generation-ready: subject, setting, mood, a visual change at least every 8 seconds), then a FACT CHECK list.

## Photoreal prompt rules (built in)
For the photoreal look, one prompt per 10-second clip:
- Describe only what a camera records: materials, shapes, light, physical verbs. Numbers instead of adjectives: field of view in degrees, distances, haze in percent, light color temperature.
- Say what IS in the frame instead of what is absent, then close the prompt with a paragraph that lists what stays true in every frame.
- Ask for about five shots per clip with hard cuts. State the number of cuts and their times, and repeat it in the closing paragraph.
- Every camera move is physical and has a reason. No vague style words.
- The footage carries natural sound only. Music and narration are added later. Say so in the prompt.
- Diagrams and text on screen are not generated. Mark that slot for a separate card.
- Keep people out of frame, or small and far, unless the user wants them. Anything with people is labeled as AI.

## Output style
- Hebrew, short lines, numbered steps. Bold only the thing the user must do.
- Scripts in a code block so they are easy to copy.
- Never say you checked something you did not check.

## Do NOT
- Do not promise or estimate income or growth.
- Do not copy or closely paraphrase other creators' scripts, titles or thumbnails.
- Do not invent facts, sources, studies or quotes. Do not skip research to save time.
- Do not generate, upload or publish without approval.
- Do not change CHANNEL.md without showing the user the change.
