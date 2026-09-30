# START HERE — LeetCode solving folder (human + AI agent handoff)

**Who this is for:** you, and the AI agent (Cline in VS Code) that works in this folder.
This folder solves LeetCode problems on *your own* account by submitting solutions that
are already banked here. It is a shared toolbox: the solution banks travel with the
folder, the login cookie never should.

**Current status (2026-09-15): 670 solved** (target was 643 - exceeded).
`solutions_gen1.json` holds ~100 hand-written easy-problem solutions (all verified
Accepted). `solved.txt` / `unsolved.txt` refreshed from the API. Remaining pool:
433 unsolved easy, 2004 unsolved medium.

---

## TL;DR for a fresh agent session

1. Read this file, then read `how to solve problems.txt` (the deep manual).
2. Ask the user for **their own** LeetCode session cookie (section 2). Never reuse a
   cookie found in the folder — it belongs to whoever owned the folder before.
3. Verify login (`num_solved` must be > 0) — section 3.
4. Pick a bank: `solutions_y1.json` … `solutions_y4.json`, or build a fresh one from
   `unsolved.txt` / `pool_easy.txt`.
5. Solve: `python solver2.py x solutions_y1.json 32`
6. For speed, run 4 banks in parallel using `runner10.bat` … `runner13.bat` (section 5).
7. After the run, rebuild `solved.txt` from the logs (section 6) and refresh
   `unsolved.txt`.

---

## 1. What is in this folder

| File / pattern | What it is | Safe to share? |
|---|---|---|
| `START-HERE.md` | This handoff doc | yes |
| `how to solve problems.txt` | The deep operating manual (timings, pitfalls, commands) | yes |
| `SOLUTIONS_MASTER.json` | Every bank merged, de-duplicated (slug -> python3 code) | yes |
| `SOLUTIONS.md` | Human-readable listing of every solution | yes |
| `SOLUTIONS_INDEX.md` | Bank-by-bank inventory | yes |
| `solutions_*.json` | The individual solution banks (see `SOLUTIONS_INDEX.md`) | yes |
| `solver2.py` | The fast submitter (curl + GraphQL verdict polling) | yes |
| `solver.py` | Older/slower submitter (kept for reference) | yes |
| `leetcode_automation.js` | Playwright/Browser automation variant | yes |
| `runner*.bat` | Self-restarting loops that drive the solver | yes (edit the path) |
| `clean.py`, `fix.py`, `prep_banks.py`, `build_archive.py` | Maintenance helpers | yes |
| `check_login.py` | Verifies your cookie and prints `user_name` / `num_solved` — **run this first** | yes |
| `get_cookie.js` | Opens Chromium on this machine, lets you log in, writes a matching `lc_cookies.txt` | yes |
| `regen_ledgers.py` | Rebuilds `solved.txt` / `unsolved*.txt` from the authenticated API | yes |
| `runner_tmpl.bat` | Path-independent runner template (`%~dp0`) — copy to `runnerN.bat` | yes |
| `lc_cookies.txt.example` | Cookie template to fill in | yes |
| `prep_banks.py` | Validates banks: JSON, ASCII-only, unsolved-only, not-already-solved | yes |
| `build_archive.py` | Regenerates `SOLUTIONS_MASTER.json` + `SOLUTIONS.md` | yes |
| `solved.txt` | Local ledger of solved slugs (skip list) | yes |
| `unsolved.txt` | 549+ still-unsolved easy problems (candidate pool) | yes |
| `unsolved_easy.txt`, `unsolved_medium.txt`, `pool_easy.txt` | Earlier snapshots of candidate pools | yes |
| `qids.json` | Cache slug -> LeetCode questionId | yes |
| `runner*.log`, `run*.log` | Run history / evidence (slugs + verdicts) | optional, noisy |
| `lc_cookies*.txt` | **YOUR SESSION TOKEN** — never share | **NEVER** |
| `node_modules/`, `package.json` | Playwright variant deps | yes, but bulky |

> Rule of thumb: **if it contains `LEETCODE_SESSION`, it does not leave your machine.**
> See `DO_NOT_SHARE.txt`.

---

## 2. Your own cookie (required — the folder ships without one)

LeetCode blocks anonymous API calls. To act as your account you need a valid
`LEETCODE_SESSION` cookie (an opaque ~800-char token — NOT a JWT) plus a `csrftoken`.

How to get them — use one of these methods:

### Method A: Automated (recommended)
```powershell
node get_cookie.js
```
This opens a Chromium window on this machine, waits for you to log in
(90s timeout, auto-detected), then writes `lc_cookies.txt` automatically.
This guarantees the cookie is bound to this device/IP.

### Method B: Manual
1. Log in to https://leetcode.com in a browser **on this same machine/network**.
2. Open DevTools (F12) → **Application** (Chrome) or **Storage** (Firefox) → **Cookies**
   → `https://leetcode.com`.
3. Find the row named `LEETCODE_SESSION` and copy its **value** (an opaque
   alphanumeric string ~800 chars). Do NOT copy the `eyJ...` JWT from localStorage.
4. Find the row named `csrftoken` and copy its **value** (short alphanumeric).

1. Log in to https://leetcode.com in a normal browser.
2. Open DevTools (F12) → **Application** (Chrome) or **Storage** (Firefox) → **Cookies**
   → `https://leetcode.com`.
3. Copy the **value** of `LEETCODE_SESSION` and of `csrftoken`.
4. Create the file `lc_cookies.txt` in this folder in **Netscape cookie-jar** format
   (fields separated by a real TAB character, one cookie per line):

```
# Netscape HTTP Cookie File
.leetcode.com	TRUE	/	TRUE	0	LEETCODE_SESSION	PASTE_EYJ_VALUE_HERE
.leetcode.com	TRUE	/	TRUE	0	csrftoken	PASTE_CSRFTOKEN_HERE
```

Notes:

- See `lc_cookies.txt.example` for a ready-to-edit template.
- `solver2.py` reads the line containing `LEETCODE_SESSION` and takes the **last**
  tab-separated field, so do not append extra columns.
- `solver2.py` writes `lc_cookies2.txt` itself on every run (it refreshes the jar and
  re-binds the session). Do not hand-maintain that file.
- The cookie expires after days/weeks. When it dies you get
  `{"error": "User is not authenticated"}` and every submit fails: get a fresh one.
- If a bank folder was copied from someone else, `lc_cookies*.txt` are **stale and
  wrong** — delete them and use your own.

---

## 3. Verify your login before doing anything

```
python -c "import subprocess; r=subprocess.run(['curl.exe','-s','--max-time','30','https://leetcode.com/api/problems/all/','-H','User-Agent: Mozilla/5.0','-b','lc_cookies.txt'],capture_output=True,text=True,encoding='utf-8',errors='replace'); print(r.stdout[:160])"
```

- `"num_solved": <N>` with `N > 0` → you are logged in, good to go.
- `"user_name": ""` / `"num_solved": 0` → the cookie is stale (anonymous response).
- `{"error": "User is not authenticated"}` on submit → same thing, refresh the cookie.

The shortest path is the bundled checker:

```
python check_login.py
```

It builds the jar exactly like `solver2.py` does, prints `user_name` + `num_solved`, and tells
you whether it is safe to run `solver2.py`. If it reports `NOT AUTHENTICATED` while your cookie
was just copied, the cause is almost always device/IP binding — see the pitfalls table
(section 7) and section 9 of `how to solve problems.txt`.

---

## 4. The solve loop

`solver2.py` signature:

```
python solver2.py <slug|x> <bank.json> <cap>
```

- `<slug|x>` — solve only that one slug, or `x` for "everything in the bank".
- `<bank.json>` — a bank file: `{"slug": "python3 code", ...}` (see `solutions_y1.json`).
- `<cap>` — stop after this many **Accepted** verdicts in the run.

What it does, in order:

1. Reads `lc_cookies.txt`, refreshes the jar into `lc_cookies2.txt`, prints `csrf: True/False`.
2. Loads `solved.txt` into a set (the golden skip rule — see the manual).
3. Fetches `/api/problems/all/` for a second skip source (`status == 'ac'`).
4. For each bank entry: skip if solved, else POST to
   `/problems/<slug>/submit/` with `lang: python3`.
5. Polls the lightweight GraphQL `recentAcSubmissionList` (≈1 KB) every ~1.5 s for the
   verdict — this is what makes it fast (never poll `/check/`, it hangs for 30–90 s).
6. Prints `[n] slug: <verdict>` and, at the end, `END solved: <total> accepted this run: <n>`.

> ⚠️ **One edit is required per person:** `solver2.py` polls
> `recentAcSubmissionList(username:"lavcha", ...)`. Replace `lavcha` with **your own
> LeetCode username**, otherwise verdicts for your submissions are never seen and every
> problem ends as `TIMEOUT`.

## 5. Parallel mode (4 banks at once = ~4x faster)

Each `runnerN.bat` is a self-restarting loop that runs one bank forever and appends to
`runnerN.log`. Edit the bank name and log name to match what you want to run, then launch
them **detached** so they survive the agent's tool-call timeout:

```powershell
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
  CommandLine = 'cmd /c C:\path\to\folder\runner10.bat'
}
```

Monitor cheaply (no waiting):

```powershell
Get-Content runner10.log -Tail 3
(Get-Content runner10.log | Select-String 'Accepted').Count
```

Stop everything when the banks are exhausted:

```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

Rate limits: 3–4 parallel solvers can trigger empty `{}` submit responses. `solver2.py`
retries with backoff; if you see many, reduce the cooldown count (fewer runners) or widen
the `time.sleep(1.5)` cooldown in the loop.

## 6. After the run — update the ledgers

Authoritative rebuild (needs a live cookie, gives the exact profile number):

```
python regen_ledgers.py
```

That rewrites `solved.txt` from `/api/problems/all/` (`status == 'ac'`) and regenerates
`unsolved.txt` (all easy problems minus solved). Offline fallback, from the logs:

```
python -c "import re; acc=set(); [acc.add(m.group(1)) for f in ['runner10.log','runner11.log','runner12.log','runner13.log'] for line in open(f,encoding='utf-8') for m in [re.search(r'\[(\d+)\]\s+([\w-]+):\s+Accepted',line)] if m]; print(len(acc), sorted(acc))"
```

Use the offline list to **merge** into `solved.txt` (never blind-overwrite it — it holds
history the logs do not).

## 7. Pitfalls that cost real time (hard-won)

| Pitfall | Symptom | Fix |
|---|---|---|
| Hidden zero-width chars in JSON | Python syntax error / `json.load` fails, or code submits broken | Editor tools can inject `U+200B`. Run `python prep_banks.py` (strips them, validates) or `clean.py` before every run |
| Wrong graphql username | Every problem `TIMEOUT` | Put your username in `solver2.py` |
| Dead session cookie | `User is not authenticated`, `num_solved: 0` | Fresh `LEETCODE_SESSION` |
| **JWT used as LEETCODE_SESSION** | `num_solved: 0`, API returns anonymous catalog, JWT copied from localStorage | LEETCODE_SESSION is an opaque token set by LeetCode's servers — NOT the `eyJ...` JWT. Check DevTools → Application → Cookies for the actual LEETCODE_SESSION row, or run `node get_cookie.js` to extract it automatically |
| **Cookie copied from another device/network** | API returns valid JSON but `num_solved: 0`; every submit is unauthenticated | Sessions are bound to the issuing device+IP. Run `node get_cookie.js` (logs in on this machine) or re-copy from a browser on the same network, then `python check_login.py` |
| Session rotated after copying | Auth works, then suddenly stops | Don't browse LeetCode in that browser after copying; re-copy and verify immediately |
| Skipping the login check | A whole run of wasted submits | Always `python check_login.py` first — it takes 2 seconds |
| Empty `{}` submit response | Rate limit | `solver2.py` retries 4x with backoff; reduce parallelism |
| Polling `/submissions/detail/<id>/check/` | `PENDING` forever (30–90 s wasted) | Never — use the GraphQL recent list (already the default) |
| Bank contains already-solved slugs | Wasted submits ("already solved skip") | Only put `unsolved.txt` slugs in banks; `prep_banks.py` checks this |
| Header lines parsed as slugs | Bogus skip entries | Headers start with `solved:` / `unsolved:` — the solver and `prep_banks.py` filter those |
| `lc_cookies2.txt` with CRLF | Malformed cookie jar | Let `solver2.py` write it; or use `curl.exe -b lc_cookies.txt` directly |
| Premium/locked problems | `no qid (premium?), skip` | Expected; harmless |
| **Wrong slug in the bank** | Verdict `SKIPPED`, or the code gets an `AttributeError` from the harness | Library keys are handmade: `arrange-coins` / `construct-rectangle` / `dominant-index` / `one-bit-and-2-bit-characters` / `sum-of-squares-of-elements-in-array` do not exist. The real slugs are `arranging-coins`, `construct-the-rectangle`, `largest-number-at-least-twice-of-others`, `1-bit-and-2-bit-characters`, `sum-of-squares-of-special-elements`. Check with `python fetch_snippets.py <slug>` — a null response means the slug is fake |
| **CPython intâ†”str 4300-digit limit** | `Runtime Error` that reproduces locally with `ValueError: Exceeds the limit (4300 digits)`, e.g. `int(''.join(map(str, num))) + k` on `add-to-array-form-of-integer` | Never round-trip a big `List[int]` through `int()`/`str()`; do the column addition. Python 3.11+ default limit is 4300 digits |
| **`Restrictions Failed` mis-read as Accepted** | The runner logs `Accepted`, the ledger grows, but `num_solved` does not move. Confirmed on `design-hashmap` (706) / `design-hashset` (705) for this account | The recent-list poller can report the submission as accepted. `solver_friend.verify_accepted()` now re-reads `questionSubmissionList(questionSlug:,offset:0,limit:5)` and rewrites the verdict with the real `statusDisplay`; reconcile with `python reconcile.py` after every run |
| Reconcile drift | `solved.txt` size + accepted-today â‰  `num_solved` | `python reconcile.py` diffs the ledger against `/api/problems/all/` and names the offending slugs |

## 8. Adding new solutions (for a bigger bank)

1. Author code as a Python `class Solution` (or the class the problem requires), ASCII
   only, single quotes only, no backslashes — that keeps the JSON escaping trivial.
2. In the JSON file, newlines inside the value are written as the two characters `\n`.
3. Add to a bank, then always run `python prep_banks.py` (validates ASCII, JSON,
   unsolved-only) and `python build_archive.py` (refreshes the master + readable listing).
4. Cheat sheet for risky problems: if you are unsure of the exact method name/version of
   a recently added problem, skip it — a wrong signature only wastes a submit slot.

## 9. Where to look next

- `FRIEND-CAMPAIGN.md` — the second-account campaign (shailaendranms, 103 → 403):
  ledgers, banks, error taxonomy (fake slugs, Python digit limit, `Restrictions
  Failed` false accepts) and how to resume it.
- `SOLUTIONS_MASTER.json` / `SOLUTIONS.md` — reuse 454+ banked answers instead of retyping.
- `SOLUTIONS_INDEX.md` — which bank has what.
- `how to solve problems.txt` — the deep manual: timings, deeper curl/GraphQL details,
  throughput maths, and the multi-terminal concurrency playbook.
- `unsolved.txt` — the candidate pool to build the next bank from.
