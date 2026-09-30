"""Builds the post-run banks:

  friend_bank_fix.json    - the previously rejected slugs, with corrected code
                            (originals in the library are left untouched;
                            fixes live in solutions_fix2.json)
  friend_bank_topup.json  - extra genuinely-unsolved library slugs, only used
                            if the main bank runs out before the daily target

Run:  python build_banks.py
"""
import json

BROKEN = {'arrange-coins', 'construct-rectangle', 'dominant-index',
          'one-bit-and-2-bit-characters',
          'sum-of-squares-of-elements-in-array'}

FIX = json.load(open('solutions_fix2.json', encoding='utf-8'))
pool = json.load(open('library_all.json', encoding='utf-8'))
solved_now = {l.strip() for l in open('solved.txt', encoding='utf-8')
              if l.strip() and not l.startswith(('solved:', '='))}
used = set(json.load(open('friend_bank200.json', encoding='utf-8')))

# Which rejected slugs are actually resubmittable right now?
ledger = json.load(open('run_friend100.json', encoding='utf-8'))
already_ok = {r['slug'] for r in ledger['accepted']}
fix_bank = {s: c for s, c in FIX.items() if s not in solved_now and s not in already_ok}
json.dump(fix_bank, open('friend_bank_fix.json', 'w', encoding='utf-8'), indent=1)
print('friend_bank_fix:', len(fix_bank), sorted(fix_bank))

# NOTE: 'arrange-coins' / 'construct-rectangle' were slug typos in the library;
# the real slugs (arranging-coins, construct-the-rectangle) are already solved,
# so they are correctly excluded here and need no submission.

topup = {k: v for k, v in pool.items()
         if k not in solved_now and k not in already_ok
         and k not in used and k not in fix_bank and k not in BROKEN}
extra = json.load(open('solutions_extra.json', encoding='utf-8'))
for slug, code in extra.items():
    if slug not in already_ok and slug not in topup:
        topup[slug] = code
# keep the freshly authored extras inside the slice, then the library items
ordered = list(extra.items()) + [(k, v) for k, v in topup.items() if k not in extra]
items = ordered[:85]
json.dump(dict(items), open('friend_bank_topup.json', 'w', encoding='utf-8'), indent=1)
print('friend_bank_topup:', len(items))
print('first:', [k for k, _ in items[:8]])
