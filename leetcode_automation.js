/**
 * LeetCode Automation Script
 * 
 * Automates solving LeetCode problems using Playwright.
 * - Manual login (no hardcoded credentials)
 * - Visible browser (headless=false) for CAPTCHA handling
 * - 2-second delays between actions
 * - Notifies when CAPTCHA is detected
 */

const { chromium } = require('playwright');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function waitForUserConfirmation(message) {
  return new Promise((resolve) => {
    rl.question(message, () => {
      console.log('   Resuming automation...');
      resolve();
    });
  });
}

async function checkForCaptcha(page) {
  const selectors = [
    'iframe[src*="captcha"]', '.captcha', '#captcha',
    'iframe[title*="captcha"]', 'iframe[title*="reCAPTCHA"]',
    '.g-recaptcha', '[data-sitekey]'
  ];
  for (const selector of selectors) {
    try { await page.waitForSelector(selector, { timeout: 2000 }); return true; } catch {}
  }
  return false;
}

async function fillCodeEditor(page, code) {
  await page.waitForSelector('.monaco-editor, textarea', { timeout: 15000 });
  const editor = await page.$('.monaco-editor');
  if (editor) {
    await editor.click();
    await page.keyboard.press('Control+A');
    await page.keyboard.press('Delete');
    await page.keyboard.type(code, { delay: 20 });
  } else {
    await page.fill('textarea', code);
  }
}

async function solveProblem(page, url, name, code) {
  console.log(`\n=== \${name} ===`);
  console.log(`URL: \${url}`);
  console.log('Navigating...');
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  if (await checkForCaptcha(page)) {
    console.log(`CAPTCHA DETECTED on \${name}! Solve manually.`);
    await waitForUserConfirmation('Press ENTER after solving CAPTCHA...');
  }
  console.log('Filling code editor...');
  await fillCodeEditor(page, code);
  await page.waitForTimeout(2000);
  console.log('Clicking Submit...');
  const selectors = [
    'button[data-click="submit"]',
    'button:has-text("Submit")',
    'button[aria-label*="Submit"]',
    '.submit-button'
  ];
  let submitted = false;
  for (const sel of selectors) {
    try {
      const btn = await page.$(sel);
      if (btn) { await btn.click(); submitted = true; console.log('Submitted!'); break; }
    } catch {}
  }
  if (!submitted) { console.log('Submit button not found. Click manually.'); return false; }
  await page.waitForTimeout(15000);
  if (await checkForCaptcha(page)) {
    console.log(`CAPTCHA after submit for \${name}! Solve manually.`);
    await waitForUserConfirmation('Press ENTER after solving CAPTCHA...');
  }
  const result = await page.evaluate(() => {
    const els = ['.result-content', '.submission-result', '[class*="result"]'];
    for (const s of els) { const e = document.querySelector(s); if (e && e.textContent && e.textContent.trim()) return e.textContent.trim().substring(0,200); }
    if (document.querySelector('[class*="accepted"], [class*="Accepted"]')) return "Accepted";
    if (document.querySelector('[class*="wrong"], [class*="Wrong"]')) return "Wrong Answer";
    return null;
  });
  console.log(`Result: \${result || 'Check browser manually.'}`);
  return true;
}

// Problem solutions
const problems = [
  {
    name: "Best Time to Buy and Sell Stock IV",
    url: "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/",
    code: `var maxProfit = function(k, prices) {
    if (!prices || prices.length < 2 || k < 1) return 0;
    if (k >= Math.floor(prices.length / 2)) {
        let profit = 0;
        for (let i = 1; i < prices.length; i++) {
            if (prices[i] > prices[i-1]) profit += prices[i] - prices[i-1];
        }
        return profit;
    }
    const buy = new Array(k + 1).fill(Infinity);
    const sell = new Array(k + 1).fill(0);
    for (const price of prices) {
        for (let j = 1; j <= k; j++) {
            buy[j] = Math.min(buy[j], price - sell[j-1]);
            sell[j] = Math.max(sell[j], price - buy[j]);
        }
    }
    return sell[k];
};`
  },
  {
    name: "Two Sum",
    url: "https://leetcode.com/problems/two-sum/",
    code: `var twoSum = function(nums, target) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const comp = target - nums[i];
        if (map.has(comp)) return [map.get(comp), i];
        map.set(nums[i], i);
    }
    return [];
};`
  },
  {
    name: "Valid Parentheses",
    url: "https://leetcode.com/problems/valid-parentheses/",
    code: `var isValid = function(s) {
    const stack = [];
    const map = { ')': '(', '}': '{', ']': '[' };
    for (const c of s) {
        if (map[c]) { if (stack.pop() !== map[c]) return false; }
        else stack.push(c);
    }
    return stack.length === 0;
};`
  },
  {
    name: "Climbing Stairs",
    url: "https://leetcode.com/problems/climbing-stairs/",
    code: `var climbStairs = function(n) {
    if (n <= 2) return n;
    let a = 1, b = 2;
    for (let i = 3; i <= n; i++) [a, b] = [b, a + b];
    return b;
};`
  },
  {
    name: "Merge Two Sorted Lists",
    url: "https://leetcode.com/problems/merge-two-sorted-lists/",
    code: `var mergeTwoLists = function(l1, l2) {
    const dummy = new ListNode(0);
    let curr = dummy;
    while (l1 && l2) {
        if (l1.val <= l2.val) { curr.next = l1; l1 = l1.next; }
        else { curr.next = l2; l2 = l2.next; }
        curr = curr.next;
    }
    curr.next = l1 || l2;
    return dummy.next;
};`
  }
];

async function main() {
  console.log('=== LeetCode Automation (Safe Mode) ===');
  console.log('IMPORTANT:';
  - A browser window will open
  - Manually log in to LeetCode
  - Watch for CAPTCHAs\n');

  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();

  console.log('Opening LeetCode...');
  await page.goto('https://leetcode.com/accounts/login/', { waitUntil: 'networkidle' });
  console.log('\nLog in manually. Press ENTER when done.');
  await waitForUserConfirmation('');
  console.log('\nStarting automation...\n');

  let success = 0;
  for (let i = 0; i < problems.length; i++) {
    const ok = await solveProblem(page, problems[i].url, problems[i].name, problems[i].code);
    if (ok) success++;
    if (i < problems.length - 1) {
      console.log('\nWaiting 2 seconds...');
      await page.waitForTimeout(2000);
    }
  }

  console.log(`\n=== COMPLETE: ${success}/${problems.length} processed ===`);
  console.log('Check browser for results/CAPTCHAs. Press ENTER to close.');
  await waitForUserConfirmation('');
  await browser.close();
  rl.close();
  console.log('Done.');
}

main().catch(e => { console.error(e); process.exit(1); });
