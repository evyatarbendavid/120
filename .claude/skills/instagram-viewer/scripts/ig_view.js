#!/usr/bin/env node
/* View PUBLIC Instagram pages the way a person visiting without an account does, in a real browser.

usage:
  ig_view.js profile <username> [--scroll N] [--no-embed] [--out DIR]
  ig_view.js post <url-or-shortcode> [--out DIR]
  ig_view.js status

profile  opens instagram.com/<user>, closes the dismissible "sign up" box like a visitor would, reads name, bio,
         followers, following, post count, saves screenshots (the grid, scrolled a little), then opens the official
         embed page of the profile and collects links of the latest posts and reels.
post     opens the post's official embed page and the post page: author, caption, likes and comments when public,
         screenshots, and the video address of a reel when the page names one.
status   shows this session's page-load budget.

Rules built in: public pages only, no login, no cookies, no account. One page at a time, a pause of 8-15 s between
page loads, at most 10 page loads per hour, and a one-hour cooldown after Instagram says 429 (state in ~/.cache/instagram-viewer/state.json). If Instagram answers with a
wall that cannot be closed (login page, "try again later", 429, private account, page not found) the command stops
and says so: it never retries and never tries to get around it. Output files are screenshots and a summary only;
no media is downloaded here (use open-social-link for a reel's video).
Needs Playwright (global npm package) and Chromium; ig_view.sh sets that up.
*/
const fs = require('fs');
const os = require('os');
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { try { ({ chromium } = require('playwright-core')); } catch (e2) {
  console.error('Playwright is not installed (npm i -g playwright). Use ig_view.sh so NODE_PATH is set.'); process.exit(2); } }

const HOURLY_LIMIT = 10;
const STATE = path.join(os.homedir(), '.cache', 'instagram-viewer', 'state.json');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const jitter = (a, b) => a + Math.random() * (b - a);

function readState() { try { return JSON.parse(fs.readFileSync(STATE, 'utf8')); } catch { return { loads: [] }; } }
function budget() {
  const now = Date.now(); const st = readState();
  st.loads = (st.loads || []).filter((t) => now - t < 3600e3);
  return { st, left: HOURLY_LIMIT - st.loads.length };
}
function recordLoad() {
  const { st } = budget(); st.loads.push(Date.now());
  fs.mkdirSync(path.dirname(STATE), { recursive: true }); fs.writeFileSync(STATE, JSON.stringify(st));
}
function cooldownUntil() { return readState().blocked_until || 0; }
function stop(code, msg) {
  console.log(code + ': ' + msg); process.exitCode = 3;
  if (code === 'RATE_LIMIT') {
    const st = readState(); st.blocked_until = Date.now() + 3600e3;
    fs.mkdirSync(path.dirname(STATE), { recursive: true }); fs.writeFileSync(STATE, JSON.stringify(st));
  }
}

function args(argv) {
  const o = { _: [], scroll: 2, embed: true, out: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--scroll') o.scroll = Math.max(0, Math.min(5, parseInt(argv[++i], 10) || 0));
    else if (a === '--no-embed') o.embed = false;
    else if (a === '--out') o.out = argv[++i];
    else o._.push(a);
  }
  return o;
}

async function launch() {
  const exe = process.env.CHROME_PATH || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
  const browser = await chromium.launch({ ...(exe ? { executablePath: exe } : {}), args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-US' });
  return { browser, page: await ctx.newPage() };
}

let lastLoad = 0;
async function load(page, url) {
  const cd = cooldownUntil();
  if (cd > Date.now()) { stop('COOLDOWN', `Instagram limited this address; no page loads until ${new Date(cd).toISOString().slice(11, 16)} UTC. Use another route (ig_read.py, the owner's browser, a screen recording).`); return null; }
  const { left } = budget();
  if (left <= 0) { stop('BUDGET', `already ${HOURLY_LIMIT} page loads in the last hour; wait before looking at more pages`); return null; }
  const wait = lastLoad ? Math.max(0, lastLoad + jitter(8000, 15000) - Date.now()) : 0;
  if (wait) await sleep(wait);
  recordLoad(); lastLoad = Date.now();
  let resp, navStatus = 0;
  const onResp = (r) => { try { if (r.request().isNavigationRequest() && r.frame() === page.mainFrame()) navStatus = r.status(); } catch (e) { /* ignore */ } };
  page.on('response', onResp);
  try { resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 }); }
  catch (e) {
    page.off('response', onResp);
    if (navStatus === 429 || navStatus === 403 || /ERR_HTTP_RESPONSE_CODE_FAILURE/.test(e.message)) {
      stop('RATE_LIMIT', `Instagram answered with an error page (HTTP ${navStatus || '4xx'}) and no content: it is limiting this network address right now. Stop; do not retry for at least an hour. Other routes: ig_read.py (official API), the owner's own browser, or a screen recording.`);
    } else stop('NETWORK', e.message.split('\n')[0].slice(0, 120));
    return null;
  }
  page.off('response', onResp);
  await sleep(jitter(4000, 6500));
  return resp;
}

async function bodyText(page) { return (await page.evaluate(() => document.body ? document.body.innerText : '')).replace(/[ \t]+/g, ' ').replace(/\n{2,}/g, '\n').trim(); }

/* Returns a stop code when Instagram shows something this tool must not go around, else null. */
async function wall(page, resp, text) {
  const url = page.url();
  if (resp && resp.status() === 429) return ['RATE_LIMIT', 'Instagram answered 429 (too many requests). Stop; do not retry now.'];
  if (/\/accounts\/login/.test(url) && !/instagram\.com\/(p|reel|tv)\//.test(url)) return ['LOGIN_WALL', 'Instagram sent the page to its login screen.'];
  if (/wait a few minutes|try again later|temporarily blocked|unusual activity/i.test(text)) return ['RATE_LIMIT', 'Instagram asks to wait before trying again. Stop; do not retry now.'];
  if (/isn.t available|link you followed may be broken|page may have been removed/i.test(text)) return ['NOT_FOUND', 'No such public page (wrong name, deleted, or blocked for the public).'];
  return null;
}

/* The "sign up / log in" box on public pages has a close button. A visitor closes it; if it will not close, stop. */
async function closeBox(page) {
  const dlg = page.locator('div[role="dialog"]').first();
  if (!(await dlg.count())) return true;
  for (const sel of ['div[role="dialog"] [aria-label="Close"]', 'div[role="dialog"] button:has(svg[aria-label="Close"])', 'div[role="dialog"] svg[aria-label="Close"]']) {
    const el = page.locator(sel).first();
    if (await el.count()) {
      await page.mouse.move(jitter(300, 900), jitter(200, 500), { steps: 8 });
      await el.click({ timeout: 4000 }).catch(() => {});
      await sleep(jitter(900, 1600));
      if (!(await page.locator('div[role="dialog"]').count())) return true;
    }
  }
  await page.keyboard.press('Escape').catch(() => {}); await sleep(900);
  return !(await page.locator('div[role="dialog"]').count());
}

async function meta(page, name) {
  return page.evaluate((n) => { const m = document.querySelector(`meta[property="${n}"],meta[name="${n}"]`); return m ? m.content : ''; }, name);
}
async function links(page) {
  return page.evaluate(() => [...new Set([...document.querySelectorAll('a[href]')].map((a) => a.href).filter((h) => /instagram\.com\/([^/]+\/)?(p|reel|tv)\/[A-Za-z0-9_-]+/.test(h)).map((h) => h.split('?')[0]))]);
}
async function scrollLike(page, n, shots, base) {
  for (let i = 1; i <= n; i++) {
    for (let k = 0; k < 4; k++) { await page.mouse.wheel(0, jitter(160, 260)); await sleep(jitter(250, 600)); }
    await sleep(jitter(1200, 2200));
    const f = `${base}-scroll${i}.png`; await page.screenshot({ path: f }); shots.push(f);
  }
}
const num = (s) => { const m = /([\d][\d.,]*\s*[KMBkmb]?)/.exec(s || ''); return m ? m[1].replace(/\s/g, '') : ''; };

async function profile(o) {
  const user = (o._[1] || '').replace(/^@/, '');
  if (!/^[A-Za-z0-9._]{1,30}$/.test(user)) return stop('INPUT', 'username: letters, digits, dots and underscores, up to 30');
  const out = o.out || path.join(os.tmpdir(), 'ig-view', user); fs.mkdirSync(out, { recursive: true });
  const { browser, page } = await launch();
  try {
    const resp = await load(page, `https://www.instagram.com/${user}/`); if (!resp) return;
    let text = await bodyText(page);
    let w = await wall(page, resp, text); if (w) return stop(w[0], w[1]);
    const og = await meta(page, 'og:description');
    const closed = await closeBox(page);
    text = await bodyText(page);
    const shots = []; const f0 = path.join(out, 'profile.png'); await page.screenshot({ path: f0 }); shots.push(f0);
    if (/this account is private/i.test(text)) { console.log('PRIVATE: this account is private; only its name and counts are public. Nothing else is shown.'); }
    if (!closed) { console.log('NOTE: the sign-up box would not close, so only what is visible around it is reported.'); }
    else await scrollLike(page, o.scroll, shots, path.join(out, 'profile'));
    const counts = { followers: num((/([\d.,]+[KMB]?)\s+Followers/i.exec(og) || /([\d.,]+[KMB]?)\s+followers/i.exec(text) || [])[1]),
      following: num((/([\d.,]+[KMB]?)\s+Following/i.exec(og) || /([\d.,]+[KMB]?)\s+following/i.exec(text) || [])[1]),
      posts: num((/([\d.,]+[KMB]?)\s+Posts/i.exec(og) || [])[1]) };
    const ogTitle = await meta(page, 'og:title');
    let postLinks = await links(page);
    if (o.embed) {
      const r2 = await load(page, `https://www.instagram.com/${user}/embed/`);
      if (r2) {
        const t2 = await bodyText(page); const w2 = await wall(page, r2, t2);
        if (w2) console.log(`NOTE: embed page not shown (${w2[0]}).`);
        else {
          const f1 = path.join(out, 'embed-grid.png'); await page.screenshot({ path: f1 }); shots.push(f1);
          if (!counts.posts) counts.posts = num((/([\d.,]+[KMB]?)\s+posts/i.exec(t2) || [])[1]);
          postLinks = [...new Set([...postLinks, ...(await links(page))])];
        }
      }
    }
    const summary = { user, title: ogTitle, counts, description: og, page_text: text.split('\n').slice(0, 40).join(' | ').slice(0, 900), post_links: postLinks.slice(0, 24), screenshots: shots };
    fs.writeFileSync(path.join(out, 'summary.json'), JSON.stringify(summary, null, 1));
    console.log(`PROFILE @${user}  ${ogTitle || ''}`.trim());
    console.log(`  followers ${counts.followers || '?'}   following ${counts.following || '?'}   posts ${counts.posts || '?'}`);
    if (og) console.log('  public summary: ' + og.slice(0, 300));
    console.log('  page text: ' + summary.page_text.slice(0, 500));
    console.log(`  post/reel links (${postLinks.length}): ` + postLinks.slice(0, 12).join(' '));
    console.log('  screenshots (open them with the Read tool): ' + shots.join(' '));
    console.log('  summary file: ' + path.join(out, 'summary.json'));
  } finally { await browser.close(); }
}

async function post(o) {
  let ref = o._[1] || '';
  const m = /instagram\.com\/(?:[^/]+\/)?(?:p|reel|tv)\/([A-Za-z0-9_-]+)/.exec(ref); const code = m ? m[1] : ref;
  if (!/^[A-Za-z0-9_-]{5,20}$/.test(code)) return stop('INPUT', 'give an instagram.com/p/…, /reel/… link or the shortcode');
  const out = o.out || path.join(os.tmpdir(), 'ig-view', 'post-' + code); fs.mkdirSync(out, { recursive: true });
  const { browser, page } = await launch();
  try {
    const shots = [];
    const r1 = await load(page, `https://www.instagram.com/p/${code}/embed/captioned/`); if (!r1) return;
    const t1 = await bodyText(page); const w1 = await wall(page, r1, t1);
    let embedText = '';
    if (!w1) { embedText = t1.split('\n').slice(0, 25).join(' | '); const f = path.join(out, 'embed.png'); await page.screenshot({ path: f }); shots.push(f); }
    const r2 = await load(page, `https://www.instagram.com/p/${code}/`); if (!r2) return;
    let t2 = await bodyText(page); const w2 = await wall(page, r2, t2);
    if (w2 && w1) return stop(w2[0], w2[1]);
    const og = w2 ? '' : await meta(page, 'og:description'); const ogTitle = w2 ? '' : await meta(page, 'og:title');
    const ogVideo = w2 ? '' : await meta(page, 'og:video');
    if (!w2) { await closeBox(page); const f = path.join(out, 'post.png'); await page.screenshot({ path: f }); shots.push(f); }
    const summary = { code, title: ogTitle, description: og, embed_text: embedText, video: ogVideo, screenshots: shots };
    fs.writeFileSync(path.join(out, 'summary.json'), JSON.stringify(summary, null, 1));
    console.log(`POST ${code}  ${ogTitle || ''}`.trim());
    if (og) console.log('  public summary: ' + og.slice(0, 500));
    if (embedText) console.log('  embed text: ' + embedText.slice(0, 500));
    if (ogVideo) console.log('  video address (use open-social-link to watch it): ' + ogVideo.slice(0, 160));
    console.log('  screenshots (open them with the Read tool): ' + shots.join(' '));
  } finally { await browser.close(); }
}

(async () => {
  const o = args(process.argv.slice(2)); const cmd = o._[0];
  if (cmd === 'status') {
    const b = budget(); const cd = cooldownUntil();
    console.log(`page loads left this hour: ${b.left} of ${HOURLY_LIMIT}` + (cd > Date.now() ? `; COOLDOWN until ${new Date(cd).toISOString().slice(11, 16)} UTC (Instagram limited this address)` : ''));
    return;
  }
  if (cmd === 'profile') return profile(o);
  if (cmd === 'post') return post(o);
  console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0].replace('#!/usr/bin/env node\n/*', '').trim());
})().catch((e) => { console.error('ERROR: ' + (e && e.message || e)); process.exit(1); });
