/**
 * get_cookie.js - log in to LeetCode in a real browser on THIS machine and save the
 * session cookies to lc_cookies.txt in the Netscape jar format solver2.py expects.
 *
 * WHY: LeetCode binds a session to the device/IP/User-Agent that created it.
 * Additionally, LEETCODE_SESSION is an opaque token set by LeetCode's servers
 * (NOT the eyJ... JWT that users sometimes copy from localStorage). Copying
 * the JWT as LEETCODE_SESSION results in "num_solved: 0" API responses.
 * Logging in via this script guarantees both device-binding AND correct
 * token extraction.
 *
 * USAGE
 *   node get_cookie.js
 *   -> Chromium opens; log in there (normal / Google / GitHub login)
 *   -> the script detects the login, writes lc_cookies.txt, and closes the browser
 *
 * Run it from the folder that contains solver2.py.
 */
const { chromium } = require('playwright');
const fs = require('fs');

const TIMEOUT_S = 900;

async function catalogStatus(page) {
  try {
    return await page.evaluate(async () => {
      const r = await fetch('https://leetcode.com/api/problems/all/');
      const j = await r.json();
      return { user: j.user_name || '', solved: j.num_solved || 0 };
    });
  } catch (e) {
    return { user: '', solved: 0 };
  }
}

(async () => {
  console.log('Opening a Chromium window. Log in to LeetCode inside it.');
  console.log('Waiting up to ' + TIMEOUT_S + 's - the login is detected automatically.');

  const browser = await chromium.launch({ headless: false, slowMo: 20 });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  page.on('framenavigated', f => {
    if (f === page.mainFrame()) console.log('nav: ' + f.url().slice(0, 90));
  });

  // Tolerant navigation: a slow/heavy page must not kill the script.
  try {
    await page.goto('https://leetcode.com/accounts/login/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  } catch (e) {
    console.log('goto warning (continuing anyway): ' + e.message.split('\n')[0]);
  }

  let saved = false;
  for (let i = 0; i < TIMEOUT_S; i++) {
    await page.waitForTimeout(1000);
    if (i > 0 && i % 30 === 0) console.log('...still waiting for login (' + i + 's)');

    let cookies = [];
    try { cookies = await context.cookies('https://leetcode.com'); } catch (e) { }
    const sid = cookies.find(c => c.name === 'LEETCODE_SESSION');
    if (!sid) continue;

    const st = await catalogStatus(page);
    if (!st.solved) continue;

    const csrf = cookies.find(c => c.name === 'csrftoken');
    const lines = ['# Netscape HTTP Cookie File'];
    lines.push('.leetcode.com\tTRUE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + sid.value);
    if (csrf) lines.push('.leetcode.com\tTRUE\t/\tTRUE\t0\tcsrftoken\t' + csrf.value);
    fs.writeFileSync('lc_cookies.txt', lines.join('\n') + '\n', 'utf8');

    console.log('OK: logged in as ' + st.user + ', num_solved=' + st.solved);
    console.log('session length=' + sid.value.length + ' - wrote lc_cookies.txt');
    saved = true;
    break;
  }

  if (!saved) console.log('TIMEOUT: no logged-in session detected - nothing written.');
  await browser.close();
  console.log('browser closed');
})().catch(e => { console.error('ERROR: ' + e.message.split('\n')[0]); process.exit(1); });