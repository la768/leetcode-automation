/* Manual LeetCode login helper for a NEW (friend's) account.
 *
 * Launches a headed browser with a fresh local profile, navigates to the
 * LeetCode login page, and waits for the USER to sign in manually. It polls
 * for LEETCODE_SESSION and then exports leetcode.com cookies to the local
 * lc_cookies.txt jar consumed by the existing automation.
 *
 * Secrets handling: cookie values are written only to the local jar file.
 * They are never printed, logged, or pasted into source.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROFILE_DIR = path.join(HERE, 'playwright_profile');
const JAR_PATH = path.join(HERE, 'lc_cookies.txt');
const STATUS_PATH = path.join(HERE, 'login_status.json');
const TIMEOUT_MS = 15 * 60 * 1000;

function setStatus(obj) {
  fs.writeFileSync(STATUS_PATH, JSON.stringify({ ts: new Date().toISOString(), ...obj }));
}

function toNetscape(cookies) {
  const lines = ['# Netscape HTTP Cookie File', ''];
  for (const c of cookies) {
    if (!String(c.domain || '').includes('leetcode.com')) continue;
    const sub = String(c.domain).startsWith('.') ? 'TRUE' : 'FALSE';
    const secure = c.secure ? 'TRUE' : 'FALSE';
    const expiry = String(Math.floor(c.expires || 0));
    lines.push([c.domain, sub, c.path || '/', secure, expiry, c.name, c.value].join('\t'));
  }
  return lines.join('\n') + '\n';
}

(async () => {
  setStatus({ state: 'waiting', note: 'browser open, manual login required' });
  const baseOpts = {
    headless: false,
    viewport: { width: 1280, height: 800 },
    args: ['--disable-blink-features=AutomationControlled'],
  };
  // Prefer real installed Chrome for the most normal fingerprint.
  let context;
  try {
    context = await chromium.launchPersistentContext(PROFILE_DIR, { ...baseOpts, channel: 'chrome' });
    console.log('Using installed Chrome channel.');
  } catch (e) {
    console.log('Installed Chrome not available, using bundled Chromium.');
    context = await chromium.launchPersistentContext(PROFILE_DIR, baseOpts);
  }
  const page = context.pages()[0] || (await context.newPage());
  await page.goto('https://leetcode.com/accounts/login/', { waitUntil: 'domcontentloaded' });
  console.log('Please sign in to the FRIEND account in the opened browser window.');

  const start = Date.now();
  let done = false;
  while (Date.now() - start < TIMEOUT_MS) {
    const cookies = await context.cookies('https://leetcode.com');
    const session = cookies.find((c) => c.name === 'LEETCODE_SESSION');
    if (session && String(session.value || '').length > 50) {
      fs.writeFileSync(JAR_PATH, toNetscape(cookies), 'utf8');
      setStatus({ state: 'done', cookieCount: cookies.length, note: 'jar exported' });
      console.log(`Login detected. Exported ${cookies.length} cookies to lc_cookies.txt.`);
      done = true;
      break;
    }
    await new Promise((r) => setTimeout(r, 5000));
  }
  if (!done) {
    setStatus({ state: 'timeout', note: 'no LEETCODE_SESSION within 15 minutes' });
    console.log('Timed out waiting for login.');
  }
  await context.close();
  process.exit(done ? 0 : 2);
})().catch((e) => {
  setStatus({ state: 'error', note: String(e && e.message || e).slice(0, 200) });
  console.error('Login helper failed:', e);
  process.exit(1);
});
