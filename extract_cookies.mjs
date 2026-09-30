// Use Playwright to launch Chrome and extract cookies after login
import { chromium } from 'playwright';
import fs from 'fs';

(async () => {
  // Launch a fresh browser (or connect over CDP if needed)
  const browser = await chromium.launch({
    headless: false,
    channel: 'chrome',
    args: ['--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36']
  });

  const context = await browser.newContext();
  const page = await context.newPage();
  
  console.log('Navigating to leetcode.com...');
  await page.goto('https://leetcode.com', { waitUntil: 'networkidle' });
  
  // Check if we're logged in
  const userName = await page.evaluate(() => {
    // Check for the user avatar/menu which indicates login
    const avatar = document.querySelector('[data-track-action="profile_avatar"] img, .avatar img, .user-avatar');
    if (avatar) return avatar.alt || avatar.src;
    return null;
  }).catch(() => null);
  
  if (!userName) {
    console.log('Please log in to LeetCode in the browser window that opened...');
    console.log('Once logged in, press any key in this terminal to continue');
    await new Promise(resolve => process.stdin.once('data', resolve));
  }
  
  // Wait a moment for cookies to settle
  await page.waitForTimeout(2000);
  
  // Get all cookies
  const cookies = await context.cookies('https://leetcode.com');
  console.log('\n=== COOKIES FOUND ===');
  for (const cookie of cookies) {
    console.log(`${cookie.name}=${cookie.value.substring(0, 50)}...`);
  }
  
  // Find LEETCODE_SESSION specifically
  const sessionCookie = cookies.find(c => c.name === 'LEETCODE_SESSION');
  if (sessionCookie) {
    console.log(`\nLEETCODE_SESSION found (${sessionCookie.value.length} chars)`);
    
    // Write in Netscape cookie jar format
    const jar = cookies.map(c => 
      `leetcode.com\tFALSE\t${c.path || '/'}\t${c.secure ? 'TRUE' : 'FALSE'}\t${c.expires || 0}\t${c.name}\t${c.value}\n`
    ).join('');
    fs.writeFileSync('lc_cookies.txt', '# Netscape HTTP Cookie File\n' + jar);
    console.log('Saved ALL cookies to lc_cookies.txt');
  } else {
    console.log('\nNo LEETCODE_SESSION cookie found!');
    console.log('Available cookies:', cookies.map(c => c.name).join(', '));
  }
  
  await browser.close();
})();