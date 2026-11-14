// render.mjs - render a canvas explainer (one HTML file) to MP4 with sound.
// usage: node render.mjs video.html out.mp4 [fps=30] [voiceover.mp3|wav|m4a]
// needs: Node 18+, ffmpeg on PATH, Chrome or Edge, and `npm i puppeteer-core` once in this folder.
import puppeteer from 'puppeteer-core';
import { spawn, spawnSync } from 'node:child_process';
import { writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [html, out = 'draft.mp4', fpsArg = '30', voice] = process.argv.slice(2);
if (!html) { console.error('usage: node render.mjs video.html out.mp4 [fps] [voiceover]'); process.exit(1); }
if (spawnSync('ffmpeg', ['-version']).error) { console.error('ffmpeg not found on PATH. Install it, reopen the terminal, try again.'); process.exit(1); }
const candidates = [
  process.env.CHROME_PATH,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium',
].filter(Boolean);
const executablePath = candidates.find((p) => existsSync(p));
if (!executablePath) { console.error('No Chrome/Edge found. Set the CHROME_PATH environment variable.'); process.exit(1); }

const browser = await puppeteer.launch({ executablePath, headless: true });
const page = await browser.newPage();
page.on('pageerror', (e) => console.error('page error:', e.message));
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.waitForFunction('typeof window.seek === "function" && window.DURATION > 0');
await page.evaluate(() => window.READY || true);
const { w, h, dur } = await page.evaluate(() => {
  const c = document.querySelector('canvas');
  return { w: c.width, h: c.height, dur: window.DURATION };
});
const fps = Number(fpsArg);
const frames = Math.round(dur * fps);

let sfx = null;
if (await page.evaluate(() => typeof window.renderAudioWav === 'function')) {
  const b64 = await page.evaluate(() => window.renderAudioWav());
  sfx = path.resolve('sfx.wav');
  writeFileSync(sfx, Buffer.from(b64, 'base64'));
}

const args = ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-'];
const audioInputs = [sfx, voice].filter(Boolean);
audioInputs.forEach((a) => args.push('-i', a));
if (audioInputs.length === 2) {
  args.push('-filter_complex', '[1:a][2:a]amix=inputs=2:duration=longest:normalize=0[a]', '-map', '0:v', '-map', '[a]');
} else if (audioInputs.length === 1) {
  args.push('-map', '0:v', '-map', '1:a');
}
args.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-r', String(fps));
if (audioInputs.length) args.push('-c:a', 'aac', '-b:a', '192k', '-t', String(dur));
args.push(out);

const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
for (let i = 0; i < frames; i++) {
  const dataUrl = await page.evaluate((t) => {
    window.seek(t);
    return document.querySelector('canvas').toDataURL('image/png');
  }, i / fps);
  const buf = Buffer.from(dataUrl.split(',')[1], 'base64');
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
console.log(`wrote ${out}: ${frames} frames, ${w}x${h}, ${dur}s`);
