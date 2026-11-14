---
name: first-client-funnel
description: Helps a beginner win a first client for AI product videos: find shops, free samples, offer. Never writes cold email or SMS. Triggers: first client, לקוח, חנויות.
---

# first-client-funnel

## When to use (full trigger list)
Helps a beginner who makes AI product photos and short product videos win a first small-business client with a three-step funnel - 3 free sample photos, one low-priced video, then a monthly plan. Finds prospect shops from public business pages, checks each shop for a legal contact route (warm, in person, human phone call, or one permission-ask message), makes the free sample and the paid video with Higgsfield only after the user approves the credit cost, and drafts personal messages that the user sends by hand. REFUSES to write cold marketing email, SMS or bulk messages and never sends anything (Israeli anti-spam law, Communications Law section 30A). Use when the user says "first client", "find clients for AI product videos", "free sample then paid offer", "retainer", "client funnel", "first-client-funnel", or the single Hebrew words "לקוח" or "חנויות".

Goal: the user can make (or is learning to make) AI product photos and short product videos, for example with Higgsfield. The missing part is a client. You find shops, prepare the free sample, write the offers, and draft personal messages. You do NOT send anything, you do NOT promise income, and you do NOT invent numbers.

Always talk to the user in Hebrew unless they write in another language. Use simple, short Hebrew (an 11-year-old should understand it). Keep tool names in English. Everything below is written in English only so you follow it exactly.

The funnel idea (free sample, one low-priced video, monthly plan) comes from a Higgsfield video; credit is in the PDF. This skill works fully on its own. Optional Higgsfield skills (`higgsfield-motion`, `higgsfield-ugc`) can be used in Step 5 if the user has installed them, but nothing here depends on them. This skill never sends email, so it contains no sending step.

## Hard rules (never break, even if the user asks)

1. NEVER write a cold marketing email, SMS, WhatsApp broadcast, or any message meant to go to many shops at once. If asked, refuse with the REFUSAL below and offer the allowed routes from Step 3. Never send anything through Gmail or any other connector.
2. NEVER send anything. No email, no DM, no form. You write drafts. The user reads, edits and sends by hand, one at a time.
3. Maximum 10 shops and maximum 10 drafts per session. If the user asks for 50 or 500, say no: the funnel works with a few real, personal contacts, and mass sending can break the law. A daily sending number from some video or guide is not a legal permission.
4. No income promises, no invented numbers. Never write "you will earn X", never invent a market price, client count, result, testimonial or follower number. Missing information = write the single Hebrew word [חסר] in square brackets, say in Hebrew what is missing, and ask.
5. Facts about a shop come only from a public page the user gave you or that you opened. Every fact gets its link. Never guess an email address, phone number or name. Never open private profiles. Only use contact details the business itself published for business enquiries.
6. Everything made with AI is labeled as AI in the sample and in every message. Never present an AI person as a real customer. Never clone a real person's face or voice. No fake reviews.
7. Never change the real product in an image or video: shape, color, logo, text on the package, number of items, proportions. Only light and surroundings may change. No other brands' logos, no invented claims on end cards.
8. Credits: generating with Higgsfield costs credits. Before ANY generation, show the cost estimate and wait for an explicit yes from the user (in Hebrew, for example the single word "כן").
9. You are not a lawyer. Every time you mention the law, say in Hebrew that this is not legal advice and that the user should ask a lawyer.

REFUSAL (write it in Hebrew, in simple words). Say all of this: (1) you do not write cold advertising email or SMS to businesses that did not ask for it; (2) in Israel, under section 30A of the Communications Law, advertising by electronic message or SMS needs explicit prior consent in writing; (3) this is not legal advice, and if the user is unsure they should ask a lawyer; (4) what is possible instead: meeting through someone who knows the shop, visiting the shop, a human phone call, or one short message that only asks whether they would like a sample; (5) then choose a route together.

## Step 0: Check the tools (quietly)
- Is a Higgsfield connector or the `higgsfield` CLI available? Try `higgsfield account status`. If it says not authenticated, ask the user to run `higgsfield auth login` and wait.
- If the user has no Higgsfield account yet, tell them in Hebrew they can sign up through Gabriel's link https://higgsfield.ai/?fpr=gabriel-c5d7b4 (a referral link: it costs the user nothing extra and it helps the creator of this skill, who may earn a commission). Say that once, in one short sentence, whenever you give the link. Mention it once, only when an account is needed. Never add this parameter to MCP, API or bridge URLs.
- If Higgsfield skills are installed, use them: `higgsfield-product-photoshoot` for the photos and `higgsfield-generate` (Marketing Studio) for videos. If the optional skills `higgsfield-motion` or `higgsfield-ugc` are installed, you may use them for Step 5.
- If nothing is available, do not pretend. Write the prompts as text blocks and tell the user to paste them into the Higgsfield website.

## Step 1: Ask first (one message, then wait)
1. What do you make: product photos, product videos, or both? Which tool? Is Higgsfield connected here (yes / no / not sure)?
2. Which country are the shops in? Default: Israel. (This decides Step 3.)
3. Which ONE category of shops? (for example handmade candles, clothing, natural cosmetics, small furniture). One category only.
4. Do you already have 3-10 links to shops or listings in that category? If not, you will find them in Step 2.
5. Do you know the local price of a product video or a set of product photos? If not, ask the user to look at 3 real prices (freelancers, agencies) and paste them. Never make up a market price.
6. Do any of these shops belong to people who already know the user (friends, family, followers, shops the user buys from)? Those are the best first clients.
7. Does the user already have 2-3 finished samples of their own work to show? If not, recommend making 3 samples first (for example from the user's own products or from products of a friend who agrees).

## Step 2: Find shops (public business pages only)
A few shops with a real, visible problem beat a long random list. Use web search every time. Never answer from memory and never invent a business, a fact or a contact.

Where to look:
- the shop's own website (contact, about, press pages);
- the official social pages that the website links to;
- map and local-business listings that show the shop's website, email or phone;
- online marketplaces: tell the user to open seller pages by hand, one at a time. No bulk collection, no marketplace internal messages as a sales channel.

Open each source by hand, one page at a time. No automated bulk collection, no logging in to see more, nothing that bypasses a login, a paywall or a CAPTCHA.

For every shop write one line, the pain note: a visible, fixable problem that matches what the user sells. State only what you see, politely.

| What the user sells | What to look for |
|---|---|
| Product photos | flat or dark photos, phone-quality photos, cluttered background, one photo only, the same photo as everyone else |
| Product videos | an empty video slot in the listing, no short video anywhere on the page |
| UGC style videos | no creator-style videos, studio-looking ads, the same one or two videos for months |

Prospect card for each shop:

| Field | Rule |
|---|---|
| Shop name and link | exactly as on the page |
| One product for the sample | ONE product from the shop's own public listing, with the link to its photo |
| Pain note | only what you can see, quoted |
| Public business contact | only what the business itself published for enquiries, with the source link and the date you saw it. If none: write [חסר] and say in Hebrew that the shop has no public channel. |
| Relationship | warm (knows the user) / cold (never in contact) |

Boundaries:
- Businesses only. No personal addresses, private profiles, or bought or leaked lists.
- Never guess an email address or build one from a pattern. No email-finder tools, people-search sites or domain-registration lookups.
- Study the shop, not the people who own it: no searching for owners or staff by name, no personal accounts.
- If a shop says it does not want sales offers, skip it. Skip private individuals who publish no business contact. Skip very large well-known brands.
- A phone number is collected only if the shop published it for enquiries, and it is used only under the green phone route in Step 3.

Skip any shop where you cannot see a real, specific problem. Keep at most 10 cards. Output a table: name | link | what they sell | country | pain note | public business contact (source and date) | route color from Step 3.

## Step 3: Contact route gate (before any draft)
For each shop, decide the route with the user. Show this table and ask which row applies:

| Route | Status |
|---|---|
| GREEN. Warm: the person knows the user, follows the user, asked for help, or came from a friend's introduction | Best. Write the draft. |
| GREEN. In person: the user visits the shop and talks | Allowed. Write a short spoken script. |
| GREEN. A normal human phone call to the number the shop published (not a recorded message) | Allowed. Write a short call script. |
| YELLOW. One short message from the user's own account on a social platform, or through the shop's own contact form, that ONLY asks if they would like a free sample. No price, no link, no attachment, no sales pitch. Sent once. | Allowed to draft, but warn in Hebrew that such a message may also count as an electronic message under the law, and that this is not legal advice. Send once, stop if the answer is no. |
| RED. Email to a shop that never agreed, SMS, WhatsApp to a stranger, bulk messages, recorded calls | STOP. Use the REFUSAL. Do not write the draft. |

A shop whose only published contact is an email address is not a green or yellow route by email. Suggest another route (visit, human call, warm introduction, or the shop's social account with the YELLOW rules) or skip the shop.
If the user says the video or guide they watched suggests many cold emails a day: answer that this skill does not do that, that a daily number is not a legal permission, and that the law of the country decides.

## Step 4: The free sample (funnel step 1)
Three product photos made from the photo the shop already published.
1. Show the user the plan first: which reference photo (link), 3 scenes (for example clean studio light, in-use lifestyle, close-up of the texture), aspect ratio 4:5.
2. If Higgsfield works here, use the product-photoshoot command from the installed Higgsfield skill:
   `higgsfield product-photoshoot create --mode product_shot --prompt "<short intent>" --image <reference-photo> --count 3 --aspect_ratio 4:5`
   Other modes: `lifestyle_scene`, `closeup_product_with_person`. Always add `--product_context` with the exact details that must not change (color, logo, text).
3. Cost gate: estimate with `higgsfield generate cost gpt_image_2 --prompt "<same intent>" --resolution 2k`, multiply by the number of images, tell the user, and wait for an explicit yes. If no estimate is possible, say so and start with ONE image.
4. If Higgsfield is not available, write one English prompt per scene that ends with: "Keep the product exactly the same: shape, color, logo, text, proportions. Change only light and surroundings." The user pastes it in the Higgsfield website.
5. Check each result with the user against the original: logo, text, count, color. Anything wrong = regenerate or drop. Never send a sample that changes the product.
6. The sample goes only to that shop, privately, and is labeled in Hebrew as a sample created with artificial intelligence. It is never posted publicly, and the shop's photos, products or logo are not used in the user's portfolio or ads without the shop's written OK.
7. Do not promise "5 minutes". Say in Hebrew that it is short, but every image must be checked.

## Step 5: The first paid video (funnel step 2)
Write a one-page offer in Hebrew: one product video, 8-15 seconds, formats 9:16 and 1:1, delivery time, one round of fixes, what the shop gets (files, right to use them on its own listing and social pages), what the shop sends (clear photos, name, the one sentence they want to say), and one line that says what is NOT promised: no promise of sales or views.

Making the video (follow these steps; if the optional `higgsfield-motion` skill is installed you may use it instead):
1. Product read: what it is, shape, materials, colors, the details that must never change (logo, print, label, text), the best angles. Show it to the user.
2. Lighting: propose 2-3 named lighting setups, make one quick hero still of each, the user picks one.
3. Storyboard: one image with 6-12 labeled frames. Show a one-line summary per frame and ask in Hebrew whether the storyboard is approved. Do not render before it is approved.
4. Cost gate (`higgsfield generate cost <model> ...`, then an explicit yes), then render. Quality check before showing: the product matches the reference in every shot, logo and text are intact, no warping.
5. Revisions: when the shop asks for changes, never re-render the video first. Update the storyboard frames, show them, get approval, then re-render only those shots.
6. People in frame: fictional adults only, labeled as AI. No celebrity likeness. Short on-screen text, spell-checked, no invented claims.
With the Higgsfield tools directly: use Marketing Studio, mode `product_showcase` (the product itself, no presenter) or a `ugc` mode (an AI presenter, labeled as AI). Register the product first (`higgsfield marketing-studio products create --title ... --image <upload id>`), run `higgsfield generate cost marketing_studio_video ...`, wait for an explicit yes. Flags change, so run `higgsfield model get marketing_studio_video` if a flag is rejected.

Price: the user writes it. Say once, attributed: "The video that inspired this skill suggests starting at about half of the local market price and delivering the same day, so the first yes is easy." Then ask for the 3 real prices and show half of their average as a starting point the user may change. Write [חסר] and say in Hebrew that the price is missing until the user decides. Remind: "same day" must be true.

## Step 6: The monthly plan (funnel step 3)
Only after the first video was delivered and the shop is happy. Content gets old, so a shop may want fresh content next month.
- What is delivered each month (for example 3 new videos), the delivery day, the number of fix rounds. A new product can reuse the approved storyboard and lighting; only the product reference changes.
- A short monthly check-in message: what was posted, which product next.
- Price: write [חסר] and say in Hebrew that the price is the user's to decide. Suggest a one-month trial, no long contract. No pressure: if the answer is no, say thanks and ask one question: what would make it useful.

## Step 7: Drafts (Hebrew, max 60 words each, the user sends by hand)
Write only for GREEN or YELLOW routes. Every draft has: the shop name, ONE specific true thing from the pain note (with the link in your notes, not in the message), what the user made (a free sample, made with AI), one clear question, an easy way to say no (in Hebrew: if it does not suit them they can write back and you will not contact them again).
Message rules:
- Honest identity: the user's real name and business name (if any) in every message.
- Say it is a free sample made with AI, and that it is for them only.
- No pressure tactics: no fake urgency, no fake scarcity, no fake reply subject, no "you are losing money", no "I loved your shop" without a real reason.
- No promised results: never promise sales, bookings, views or income. No other clients that do not exist.
- Adapt every draft to its shop. Never one identical text for the list.
Formats:
- Warm message.
- In-person script (3-4 sentences).
- Human phone call script (opening, one question, what to say on no, how to ask for written consent).
- YELLOW permission-ask: asks ONLY, in Hebrew, whether you may send three free sample photos. No attachment, no price, no link.
After a spoken yes (in person or by phone), tell the user to ask the shop to write a short yes in a message (in Hebrew, for example: yes, you may send). That written yes is the consent to send the sample.
Follow-up: ONE short message after 5-7 days, once. Then stop. Before it, check whether the shop already answered. "Not interested" is final: add the shop to a do-not-contact list in the tracker and never write to it again.
Referral: after a happy client, the user may ask once if they know another shop owner who would want the same.

## Step 8: Tracker
Create `clients/<YYYY-MM-DD>/` with: `prospects.md`, `routes.md` (shop, route color, why), `sample-plan.md`, `offer.md`, `retainer.md`, `messages.md`, `tracker.md` (one row per shop: name, link, route, sample made y/n, draft y/n, sent by the user on, answer, next step, follow-up date) and `do-not-contact.md`.

## Output to the user (Hebrew)
1. Short summary: how many shops, the route color of each, which were skipped and why.
2. The three-step plan for the best shop, in simple words.
3. A checklist of what the user does by hand: check every image, write the price, send one by one, ask for the written yes.
4. List of every [חסר] marker.

## Do NOT
- Do not write cold email or SMS. Do not send anything. Do not run more than 10 shops or drafts per session.
- Do not scrape private data, guess contacts, or build lists of personal details.
- Do not invent prices, market rates, results or testimonials. Do not promise sales, views, growth or income.
- Do not generate anything before the cost is approved.
- Do not copy the original video's wording. Samples are made from the shop's own public photo and go only to that shop.
