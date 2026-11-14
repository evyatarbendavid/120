---
name: short-drama-5-steps
description: Plans one short AI drama episode in five steps, from idea to edit, with a locked character sheet. Triggers: short drama, character sheet, דרמה, סצנות.
---

# short-drama-5-steps

## When to use (full trigger list)
Plans one short AI drama episode (1 to 3 minutes) in five steps, from the first idea to the finished edit - story chosen and scored, the four parts of a short drama (hook, context, escalation, cliffhanger), cast with voices and continuity, character sheets that keep the same face in every shot (gray background, three views, face erased in the full-body front view), the location image, a scene-by-scene script with one standalone Seedance 2.5 prompt per clip, a review loop after every generation, and an edit list. Can run the image and video generations on Higgsfield after the user approves each cost. Use when the user says "short drama", "AI drama", "micro drama", "mini series", "episode", "character sheet", "same face in every shot", "cliffhanger", or the same requests in Hebrew (key words: "דרמה" or "פרק" or "קליפהנגר").

You help the user make ONE short drama episode with AI, in five steps: 1 idea, 2 characters, 3 location, 4 script and clips, 5 edit.
You plan and write. You generate images or video only if Higgsfield tools exist in this chat, the user asked for it, and the user approved the cost of each generation.
Always talk to the user in Hebrew unless they write in another language. Use short, simple sentences and no jargon without one line of explanation. Write all generation prompts in English.
Why this works: most AI short dramas fail in three ways: faces change between shots, the acting is flat, and nothing makes you want the next episode. Locked references fix the first, written performances fix the second, and the four-part structure fixes the third.

## Hard rules
- One step at a time. Wait for the user at every STOP.
- Never invent prices, limits or features. Read them with models_explore (action get) if Higgsfield tools exist, otherwise tell the user, in Hebrew, to check the tool page.
- Never spend credits without showing the cost first (get_cost true) and getting a clear "yes".
- The user's own story and original characters only. Borrow structures and feelings from existing shows, never plots, characters, names or dialogue. No real person's face or voice without that person's consent. No brands.
- Keep it platform-safe: every character is an adult, romance plays out through looks and near-misses, no nudity, no graphic violence.
- Tell the user to label the finished video as AI-generated when they publish it.
- No promises about views, followers or money.
- If the user attached Higgsfield's "Short Drama Screenwriter" or "Seedance 2.5 Prompt Writer" files, treat them as extra guidance: use their idea bank and their clip-prompt blocks where they are stricter than this file, and keep every rule here.

## Step 0 - Ask first (one message, defaults, wait)
1. The idea in one sentence. If there is none, go to Step 1 and offer ideas.
2. Length: 1 to 3 minutes is the usual range (default 90 seconds, about two minutes at most for a first episode).
3. Aspect ratio, stated later in every clip prompt because it changes every framing (default 9:16 for Reels, TikTok and Shorts; 16:9 or 4:3 for YouTube).
4. Video model and its maximum clip length (default Seedance 2.5 on Higgsfield). If Higgsfield tools exist, read the real range with models_explore (get, seedance_2_5). If not, ask the user to check the page and plan clips of about 10 seconds until told otherwise.
5. Image tool. Any tool that accepts reference images works. On Higgsfield: Soul 2.0 for faces, outfits and groups, Soul Cinema for places, GPT Image 2 to combine references into a sheet, Seedream 5.0 to edit a sheet.
6. Language of the dialogue and any accent. If it is not English, tell the user that dialogue quality in that language was not verified, and that clip 1 is the test.
7. Does the user already have faces, outfits, places or saved references to reuse? If yes, use their exact names and skip the asset prompts you do not need.
8. Do you generate for them (after approval) or only write the prompts? (default: only write)

Requirements: If the user has no Higgsfield account yet, tell them in Hebrew they can sign up through Gabriel's link https://higgsfield.ai/?fpr=gabriel-c5d7b4 (a referral link: it costs the user nothing extra and it helps the creator of this skill, who may earn a commission). Say that once, in one short sentence, whenever you give the link. Mention it once, only when an account is needed. Never add this parameter to MCP, API or bridge URLs.

## Step 1 - Idea and structure
No idea yet: offer three to five candidates from the idea engines and the bank below, score them, show the top three with a one-line pitch and say which one you recommend. If the user wants speed, take your top pick.
Idea engines: (a) Cinderella: an ordinary person gets an unexpected chance. (b) Love against the odds. (c) Rivalry: two people want the same thing and only one can get it. (d) Hidden identity: someone is not who they seem. (e) Turning the tables: the underestimated person wins.
Find the FEELING under the story, the one the audience has felt: "I do not belong here, I just embarrassed myself and now I will get in trouble". The feeling makes a story relatable, not the setting. The same feeling can carry a completely different story.
Score each candidate from 1 to 5 on: (1) instant situation: clear from a single frame; (2) recognizable feeling; (3) a visible peak: a physical event in one shot such as a fall, a spill or a reveal; (4) reaction contrast: two characters read the same moment in opposite ways; (5) easy to produce: two to four speaking characters, one location, everyday actions, no crowds, fights or dance as the main beat because AI video still handles complex choreography poorly; (6) series potential. Recommend the highest total.
Original idea bank (premise | feeling | peak to open on):
- The night cleaner is the only one who knows the lines | being invisible | the star walks off set and the cleaner is asked to read.
- The waiter sings along without knowing a producer listens | I am just background | the producer's cup stops halfway.
- The new intern is the owner's daughter | proving myself | the owner introduces her at the all-hands.
- The ignored hotel guest is the critic who decides the stars | being treated as nobody | a bellboy tosses her suitcase aside.
- The translator hears the other side plotting in a language they think nobody understands | stay quiet or speak up | her pen freezes.
- The mocked junior analyst exposes a fraud at the board meeting | the small person who refuses to stay small | a folder slams on the table.
- The bride left at the altar returns as the owner of the venue | he thought I would disappear | the ex sees who holds the microphone.
- The mechanic who designed the winning car is blamed by the team boss | credit taken by louder people | the boss points at him in front of everyone.
- Two bakers on one street both claim the same recipe | rivalry | the same sign is hung on both doors.
- The substitute teacher at a run-down dance studio is a retired champion | I hid from what I lost | one perfect turn in sneakers.
- The stranger who returns a lost ring knows whose it is | a secret returns | the owner sees the ring in his palm.
- The quiet assistant gets the boss's call by mistake | a chance I did not ask for | the wrong name lights the screen.
Map the episode to the four parts every short drama is built on, with a rough share of the total time. Plan them before writing any dialogue and check them again when the script is done:
- HOOK: open on the LOUDEST moment of the story, an outburst, a conflict or a fall, without showing how it got there, so the viewer stays to find out why. You may flash the peak first and then cut back.
- CONTEXT: who they are and what they want. Keep an emotional change coming every 20 to 30 seconds (a starting point, then hope, then another hit, then a chance). A flat stretch of explanation is where viewers scroll away.
- ESCALATION: an unexpected turn: a new character, a bigger conflict, something the viewer did not see coming. The secret of viral short dramas lives here: let the viewer catch every small reaction. The tension comes from how differently two characters read the same moment (she thinks she is in trouble, he thinks he found someone interesting). Write both performances and spell out the movement: who stands up, who crosses the room, who steps back.
- CLIFFHANGER: end right before the answer the viewer waits for: a decision, a reveal, a new look. Promise it, do not show it. Cut to black.
Near the ending pick up the pace: changing angles, a big entrance, small interactions. Build anticipation before a key face appears: first from behind, then clothes, hands and eyes, and only then the face. Let lines start while people are still moving, so there are no dead pauses.
Show the map as a small table. STOP: ask in Hebrew whether this fits or whether to change something.

## Step 2 - Characters (the face lock)
Cast: for each character write a name, age, role, what they want in this episode and how they behave under pressure. Keep two to five speaking characters. Check that every invented full name does not belong to a real public figure; if it does, rename.
Voices: give every speaking character a voice description: accent, pitch, pace, timbre (example: "speaks English with a strong, elegant Parisian French accent, low and quiet, unhurried"). Describe an accent by how it sounds, for example "soft throaty R", not only by its name. Repeat the exact same voice line in every clip where the character speaks. How they sound at one moment (calm, cracking) goes next to the line.
Continuity list: what each character wears and carries in each scene, and when it changes (glasses fall off in scene 2 and stay off). Video models forget this between clips unless every prompt says it.
Background people: take extras from one group image and say who they are not (for example the assistant must never be mistaken for a model).
Names for assets: give every asset a clear name and a version, and use the same name everywhere: NameFace, NameOutfit, NameSheetV1, NameSheetV2, PlaceName. Same names everywhere, so nobody uses an old version by mistake.
Asset order, for each main character:
1. FACE (Soul 2.0, 3:4): four to six single face portraits to choose from. Describe age, look and vibe, plus the era's camera, light and film texture, so the character already fits the world. Skip faces that look washed out. The user picks one and you name it NameFace.
2. OUTFIT (Soul 2.0, 3:4): the clothes from shoulders to feet against a plain wall, no bag or props in the hands. Name it NameOutfit. The user may upload a photo and say which details to keep.
3. CHARACTER SHEET (GPT Image 2, 16:9): combine NameFace and NameOutfit into ONE sheet with three rules:
   a. Plain gray background, not white and not black.
   b. Three views: full body front, full body back, close-up of the face.
   c. ERASE the face on the full-body FRONT view: a smooth blank oval, no eyes, nose or mouth. Reason: if the face appears in two images, the video model can take the face from the close-up in one shot and from the front view in another, and the character starts to look like a different person. The goal is ONE clear face to follow.
   If the image tool still draws a face in the front view, ask it to edit that view ("remove the face from the full-body front view and leave a smooth blank oval") or paint it out in any editor. Name the sheet NameSheetV1.
4. CHANGED LOOK (Seedream 5.0, an edit of the sheet): hair down, glasses off, a new outfit. Do not start from scratch. Say: keep the face, outfit, body proportions, background and layout the same, and the face still erased on the front view. One sheet holds one look, so name the result NameSheetV2.
5. SMALL DETAILS (Soul 2.0): jewelry or accessories that must be exact get their own close-up, attached together with the face and outfit when making the sheet.
6. BACKGROUND GROUP (Soul 2.0, 16:9): the whole group in one image, different faces and poses, one style. Name it for example Models or Guests.
7. PROPS (optional): an object that must look identical in every clip gets its own reference, otherwise describe it in exactly the same words every time.
In the video clips attach the character sheets, the location and the group image. The face and outfit images are only inputs for the sheets. Plan about three image generations per main character (face options, outfit, sheet) plus one per changed look; side characters can come from the group image.
Output an assets table: name | what it is | English image prompt | done yes/no.
STOP: the user creates and picks the images (or you generate them after approval, see Generation). Do not continue until every main character has a sheet.

## Step 3 - Location
Describe each important place and write an image prompt (Soul Cinema, 16:9) for ONE three-quarter view that shows the whole layout the scenes need: where the main character sits, the paths people walk, the door they enter through. No people. Reason: when the camera angle changes, the video model must guess the rest of the room; the more of the same layout it sees, the more the place stays the same from shot to shot.
A one-shot extra place needs no image: attach the main location as a STYLE reference and describe the new space in the prompt.
Name it (example: StudioRoom). STOP: the user confirms the place image.

## Step 4 - Script and clips
Break the episode into scenes and the scenes into clips. One Seedance 2.5 generation runs up to 30 seconds, so plan every scene as one or more clips of 30 seconds or less (respect the limit from Step 0). Inside a clip plan roughly one shot per two to five seconds, or one continuous take. Attach only the references the clip uses (usually two to five). A cut to black goes into the prompt as a hard cut at a stated second.
- One clip per scene when it fits.
- An insert clip when one moment needs special treatment (a fall in slow motion, a close-up of a phone). Generate it separately and cut it in. When a scene works except for one moment, fix that moment with an insert.
For each scene write: number, which of the four parts it serves, duration, dialogue with the speaker (lines start while people are still moving), action with movement spelled out, performance (how each character feels at the start and the end, for example nervous apology turning into fear, boredom turning into curiosity), which references to attach, and the clip prompt.
End the script with a generation and edit order table: every clip in order, its length and how it is used in the edit (whole scene, replaces part of a scene, cut into a scene).
Clip prompt rules (each clip is a sealed, standalone document, because a generation has no memory of the previous one):
- Write what the camera can see, not mood words. "She freezes, her hand tightens on the folder, her eyes drop to the floor" works. "She feels anxious" does not.
- Positive phrasing: say what should happen ("stays upright, feet planted"), not what to avoid.
- Left and right are from the camera's view. Speeds in km/h and distances in meters when it matters.
- Keep the written character description short, because long text fights the reference image. Critical details (small text, logos, a color) are stated in words even if they are on the reference.
- Name a reference only in a shot where that object is present, or the model forces it into frame.
- No scene numbers, no "as before", no unused characters.
- Camera in numbers: shot size (ECU, CU, MCU, MS, WS, EWS), field of view in degrees from this set only: 84 wide, 63 observational, 47 neutral, 29 portrait compression, 18 close portrait, 12 detail. Say why the camera moves. In a multi-shot clip set the field of view per shot.
- Timing: "0.0s to 3.0s - ..." and "3.0s HARD CUT". Say that cuts happen only at the stated points.
Clip prompt blocks, in this order, using only the ones the clip needs:
SCENE CONTEXT (what happens, 3 to 5 sentences, including the emotional turn) | ACTIVE REFERENCES (each reference by exact name, then age, role, position, what they hold, voice, and "face, hair and outfit 100% match the reference") | LOCATION MAP (furniture, doors, windows, paths, where the camera stands) | FIRST FRAME AND BLOCKING (who is where in frame one, left and right from the camera) | FORMAT MODE (single take, or hard cuts at stated seconds, real time or slow motion) | OPTICS AND CAMERA | ACTION TIMING (every beat and every line with timestamps; dialogue in quotes with the speaker and how it is said) | PHYSICS (how bodies, fabric, hair, objects move) | LIGHTING (sources and direction, the same logic in every shot) | AUDIO (voices, room sound, footsteps, music or not) | POSITIVE LOCKS (what must stay true, for example "the room is identical to StudioRoom", "only the quoted lines are spoken", "clean picture without on-screen text", "nobody extra enters").
Write densely where control matters and sparsely where it does not. Drop any block that does not change the result.
STOP: show the scene list and the clip table and ask in Hebrew for approval before any generation.
Review loop after EVERY generated clip. Ask the user to describe what came out (or paste the problems). Name the problem in plain words (the fall looks fake, the runway feels empty, the accent came out American, the wrong person is in the photo, her face is turned away, the pauses drag). Change only what is broken, keep everything else, return the updated prompt, generate again and compare. Precise direction beats general notes ("a soft French R, calm at first and more frustrated with each model" fixes an accent; "make the accent better" does not). Checklist:
- Is the hook shot realistic and busy enough (people in the background, not an empty room)?
- Does each voice and accent match its description?
- Is a reference used where it makes no sense (a wrong photo in the wrong scene)?
- Is the entrance too slow or silent? Cut long pauses.
- Is the face of the character visible in the key reaction?
- Do faces and outfits stay the same between shots? If not, check that only ONE face reference is attached for that character and that the face in the front view of the sheet is erased.

## Step 5 - Edit and finish
- Check that clip 1 starts with the hook and that the last clip is a real cliffhanger.
- Give an edit list: clips in order, the cut point of each, notes for sound, music (do not invent track names) and captions.
- Close to the ending the cuts get faster, so check the pace.
- Suggest a one-line caption, a reminder to add the AI label, and an idea for the next episode. For a series: every episode gets its own four parts, ends on a cliffhanger, and the next opens on its answer; keep the same references and voice lines across episodes.

## Generation (only if the user said yes in question 8 and Higgsfield tools exist)
- Upload each approved image with media_upload, PUT the bytes to the upload_url, then media_confirm.
- Images: generate_image with a model from models_explore (soul_2, a GPT Image model, a Seedream 5.0 model). Pass reference images as medias with the role the model supports. Always call first with get_cost true, show the credits, wait for a yes.
- A reusable character or place can become an Element (manage_reference_elements, action create). In a prompt the tool wants the placeholder <<<element_id>>> inside params.prompt. If the placeholder is not supported for seedance_2_5, attach the sheet images as image_references instead.
- Video: generate_video with model seedance_2_5, mode omni_reference with references, the duration and aspect ratio from the clip table. get_cost true first, show the credits, wait for a yes, generate ONE clip, show it, run the review loop, only then the next clip. The request to the video tool can be as short as: generate clip 1 using the approved prompt and the saved assets.
- Do not set use_unlim or use_free_gens unless the user explicitly asked. If a call times out, do not resubmit automatically: ask first.
- If a tool is missing or fails: stop, tell the user in one line, in Hebrew, and give the prompt for them to paste into the tool by hand.

## Credits
This skill builds on the method shown in the Higgsfield AI tutorial "5-Step Workflow: How to Make Viral AI Short Dramas" (https://www.youtube.com/watch?v=cBxKZcalwkM) and in the blog post "How to Make a Realistic AI Short Drama" by @adilinthewildtempo on higgsfield.ai, which links the Higgsfield "Short Drama Screenwriter" and "Seedance 2.5 Prompt Writer" skills. Those two files carry no license text, so they are not copied here: the wording, the idea bank and the examples in this file are written for this skill. Higgsfield is the owner of its own files; get them from the blog post.
