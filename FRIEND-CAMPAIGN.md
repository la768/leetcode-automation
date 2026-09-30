# Friend campaign — leetcode.com/u/shailaendranms

Status: **COMPLETE** (2026-09-26 04:36 UTC+2)

| metric | value |
|---|---|
| profile `num_solved` before the campaign | 103 |
| profile `num_solved` now | **403** |
| accepted today (ledger `run_friend100.json`) | **300** (target 300) |
| accepted-today slugs that the profile does not count | 0 (verified by `reconcile.py`) |
| unsolved slugs still left (easy / medium) | 658 / 2041 (`unsolved.txt`) |

Two runs produced the 300: the original 100-problem run, then a 200-problem bank
(`friend_bank200.json`) under `DAILY_TARGET=300`. The `solved.txt` snapshot now
lists exactly 403 slugs (`python regen_ledgers_fresh.py lc_cookies.txt`).

## Files (account-scoped)

| file | purpose |
|---|---|
| `solver_friend.py` | engine: session, qid cache, submit, verdict + `verify_accepted()` guard |
| `solver_friend_main.py` | driver: account gate, skip logic, ledger writes, `DAILY_TARGET` |
| `run_ledger.py` / `run_friend100.json` | daily counter + per-problem evidence (`start_solved`, `target`, `accepted`, `rejected`) |
| `friend_bank200.json` | the 200-problem bank actually run (bank100 is a 536-slug superset built earlier) |
| `friend_bank_fix.json` | corrected solutions for previously-rejected slugs (`solutions_fix2.json`) |
| `friend_bank_topup.json` | 85 extra genuinely-unsolved slugs, unused (bank never ran dry) |
| `reconcile.py` | diffs ledger vs live `/api/problems/all/` — run after every campaign |
| `ledger_invariants.py` | de-dupes / re-sorts the ledger, enforces "never in both lists" |
| `verify_fix2.py` | offline brute-force test of every fixed solution (0 failures) |
| `fetch_snippets.py` | prints the official python3 driver signature for a slug (null ⇒ fake slug) |
| `diagnose_bad_slugs.py` | maps the 5 fake library slugs to their real counterparts |
| `final_report.py` | one-screen campaign summary |

## Why problems failed, and what was done (this is the interesting part)

| slug | first verdict | root cause | fix |
|---|---|---|---|
| `add-to-array-form-of-integer` | Runtime Error | `int(''.join(map(str, num))) + k` hits Python 3.11's **4300-digit int↔str limit** on the long test cases | column addition, no int() round-trip |
| `consecutive-characters` | Runtime Error | the library entry carried LeetCode **2414**'s driver name (`longestContinuousSubstring`, `ord(c)==ord(prev)+1`) under the **1446** slug → harness `AttributeError` | renamed to `maxPower` and count runs of the *same* character |
| `button-with-longest-push-time` | Wrong Answer | ties for the longest hold must return the **smallest index**; the code kept the first-seen one | add the tie-break |
| `calculate-digit-sum-of-a-string` | Wrong Answer | returned `int(s)` while the driver wants `str` (`789 != "789"`) | return `s` |
| `check-if-strings-can-be-made-equal-with-operations-i` | Wrong Answer | only swaps with `j - i == 2` are legal, so even/odd positions are separate permutations; the code compared whole-string counters | compare `sorted(s[0::2])` and `sorted(s[1::2])` |
| `count-pairs-that-form-a-complete-day-i` | Wrong Answer | the complementary-pair loop already visits each pair once, but the answer was divided by 2 | drop the `// 2` |
| `determine-color-of-a-chessboard-square` | Wrong Answer | parity test inverted (`a1` must be dark/false) | `(ord(c)-97 + rank) % 2 == 0` |
| `arrange-coins`, `construct-rectangle` | SKIPPED (no qid) | **slug typos** in the library key — those problems do not exist; the real slugs `arranging-coins` / `construct-the-rectangle` were already solved, so nothing to do | documented; also re-keyed `sum-of-squares-of-elements-in-array` → `sum-of-squares-of-special-elements` (a real, previously-unsolved problem, banked in `solutions_extra.json`) |
| `design-hashmap`, `design-hashset` | **falsely** accepted, then `Restrictions Failed` | LeetCode refuses the submission for this account; the recent-AC poller mis-reported it as Accepted and the ledger grew while `num_solved` did not | added `verify_accepted()` — every Accepted verdict is re-checked against `questionSubmissionList(questionSlug:,offset:0,limit:5)`; ledger rows moved to `rejected`; guard validated live on `design-hashset` |

All 7 code-level failures were fixed, verified offline (`verify_fix2.py`, 0
failures) and re-submitted successfully. Every accepted-today slug was matched
against the live profile; the two false positives are the only drift that ever
existed and are now corrected (ledger `accepted` = 300, `rejected` = 4).

Extra submissions during debugging (do not affect the count): 2 for
`count-pairs-that-form-a-complete-day-i` (diagnosis) and 1 for `design-hashset`
(guard validation).

## Resuming / extending

```powershell
python check_login.py                     # must print user_name shailaendranms
$env:DAILY_TARGET='400'                   # accepted-today ceiling for this run
Start-Process python -ArgumentList 'solver_friend_main.py','x','friend_bank_topup.json' `
  -RedirectStandardOutput 'friend_topup_run.log' -WindowStyle Hidden
python reconcile.py                       # afterwards: ledger vs profile, must be empty
python regen_ledgers_fresh.py lc_cookies.txt
```

Notes: the bank is submitted sequentially with a 1.5 s cooldown (parallel submits
trip LeetCode's rate limiter); `friend_bank_topup.json` holds 85 unused unsolved
slugs and is regenerated by `python build_banks.py`.
