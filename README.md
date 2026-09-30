# LeetCode Automation Script

## ⚠️ Important Notice
This script is provided for educational purposes only. Using automation to solve LeetCode problems may violate their Terms of Service. Use responsibly and only on problems you've already solved manually.

## Prerequisites
- Node.js (v16+ recommended)
- Playwright (installed in `node_modules/`)

## Setup
```bash
npm install
npx playwright install chromium
```

## Usage

1. **Start the script:**
   ```bash
   node leetcode_automation.js
   ```

2. **Log in manually:**
   - A visible browser window will open
   - Log in to LeetCode.com manually
   - Press ENTER in the terminal when done

3. **Monitor for CAPTCHAs:**
   - The script will pause and notify you if a CAPTCHA appears
   - Solve the CAPTCHA manually in the browser
   - Press ENTER to resume the script

4. **Watch the automation:**
   - The script will solve 5 problems sequentially:
     1. Best Time to Buy and Sell Stock IV
     2. Two Sum
     3. Valid Parentheses
     4. Climbing Stairs
     5. Merge Two Sorted Lists
   - Each problem has a 2-second delay between actions
   - Results will be displayed in the terminal

## Features
- ✅ Manual login (no hardcoded credentials)
- ✅ Visible browser for CAPTCHA monitoring
- ✅ 2-second delays between actions
- ✅ CAPTCHA detection with pause-and-resume
- ✅ Result extraction after submission

## Files
- `leetcode_automation.js` - Main automation script
- `package.json` - Node.js project configuration
- `package-lock.json` - Dependency lock file

## Disclaimer
- Never commit credentials to version control
- Respect LeetCode's rate limits and terms of service
- Use at your own risk
- This project does not store or transmit your credentials
