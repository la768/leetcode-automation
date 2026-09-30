"""Rebuild solved/unsolved ledgers for a NEW (friend's) account.

Same catalog source as regen_ledgers.py (/api/problems/all/), but:
  - treats a valid user_name as the authenticated identity, even when
    num_solved == 0 (a genuinely fresh account solves nothing yet);
  - never inherits the previous account's solved list: the ledger is
    rebuilt ONLY from the friend's current status == 'ac' entries;
  - never prints cookie material (only counts and slugs).

Usage: python regen_ledgers_fresh.py [jar]
"""
import json
import subprocess
import sys
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
JAR = sys.argv[1] if len(sys.argv) > 1 else "lc_cookies.txt"

r = subprocess.run(
    ["curl.exe", "-s", "--max-time", "35", "https://leetcode.com/api/problems/all/",
     "-H", "User-Agent: " + UA, "-b", JAR],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
try:
    dec = json.JSONDecoder()
    d, _ = dec.raw_decode(r.stdout[r.stdout.find("{"):])
except Exception:
    print("FAILED: response was not JSON (Cloudflare or network).")
    sys.exit(1)

if not d.get("user_name"):
    print("FAILED: not authenticated (empty user_name). Re-run manual login first.")
    sys.exit(1)

pairs = d.get("stat_status_pairs") or []
stamp = time.strftime("%Y-%m-%d %H:%M")
solved = sorted(p["stat"]["question__title_slug"] for p in pairs if p.get("status") == "ac")
solved_set = set(solved)

with open("solved.txt", "w", encoding="utf-8") as f:
    f.write("solved: " + str(len(solved)) + " | updated: " + stamp + "\n" + "\n".join(solved) + "\n")

easy = [p["stat"]["question__title_slug"] for p in pairs if p["difficulty"]["level"] == 1]
medium = [p["stat"]["question__title_slug"] for p in pairs if p["difficulty"]["level"] == 2]
uns_easy = sorted(s for s in easy if s not in solved_set)
uns_med = sorted(s for s in medium if s not in solved_set)

with open("unsolved.txt", "w", encoding="utf-8") as f:
    f.write("unsolved: easy=" + str(len(uns_easy)) + " | updated: " + stamp + "\n" + "\n".join(uns_easy) + "\n")
with open("unsolved_easy.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(uns_easy) + "\n")
with open("unsolved_medium.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(uns_med) + "\n")

print("authenticated as:", d.get("user_name"))
print("num_solved (profile):", d.get("num_solved"), "| solved.txt entries:", len(solved))
print("unsolved easy:", len(uns_easy), "| unsolved medium:", len(uns_med))
