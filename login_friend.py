"""Manual LeetCode login helper for a new account.

Launches headed Chromium with a persistent local profile, navigates to
LeetCode login, and waits for the USER to sign in manually. Nothing is
submitted and no cookies are printed.

After the user presses ENTER, the script exports the authenticated cookies
to a local Netscape-format jar consumed by the existing automation
(check_login.py, solver2.py, regen_ledgers.py).

Cookie values are treated as secrets: they are written only to the local
jar file and never printed, logged, or pasted into source.
"""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PROFILE_DIR = HERE / "playwright_profile"
JAR_PATH = HERE / "lc_cookies.txt"


def write_netscape_jar(cookies, path: Path) -> int:
    lines = ["# Netscape HTTP Cookie File", ""]
    count = 0
    for c in cookies:
        if "leetcode.com" not in c.get("domain", ""):
            continue
        domain = c["domain"]
        include_sub = "TRUE" if domain.startswith(".") else "FALSE"
        secure = "TRUE" if c.get("secure") else "FALSE"
        expiry = str(int(c.get("expires", 0) or 0))
        lines.append(
            "\t".join(
                [
                    domain,
                    include_sub,
                    c.get("path", "/"),
                    secure,
                    expiry,
                    c.get("name", ""),
                    c.get("value", ""),
                ]
            )
        )
        count += 1
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return count


def main() -> int:
    print("Launching headed Chromium with a fresh local profile...")
    print("1. Sign in to the FRIEND's LeetCode account in the opened browser.")
    print("2. Make sure the LeetCode home page shows the friend's username.")
    print("3. Return here and press ENTER (or type q + ENTER to abort).")
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 800},
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://leetcode.com/accounts/login/", wait_until="domcontentloaded")
        try:
            while True:
                answer = input("Press ENTER when logged in (q to quit): ").strip().lower()
                if answer == "q":
                    print("Aborted before exporting any cookies.")
                    context.close()
                    return 2
                cookies = context.cookies("https://leetcode.com")
                names = {c.get("name") for c in cookies}
                if "LEETCODE_SESSION" not in names:
                    print("LEETCODE_SESSION not found yet; finish login and try again.")
                    continue
                break
        finally:
            # Export happens after the loop only when authenticated.
            pass
        cookies = context.cookies("https://leetcode.com")
        count = write_netscape_jar(cookies, JAR_PATH)
        print(f"Exported {count} leetcode.com cookies to {JAR_PATH.name}.")
        print("Cookie values were not displayed. You can close the browser.")
        context.close()
    return 0


if __name__ == "__main__":
    start = time.time()
    code = main()
    print(f"Done in {time.time() - start:.0f}s.")
    sys.exit(code)
