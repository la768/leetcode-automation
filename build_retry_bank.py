"""Writes friend_bank_retry.json = code for every slug currently in the
campaign ledger's `rejected` list (transient submit failures, WA/RE fixes).
The driver does not skip rejected slugs, so re-running it with this bank
re-attempts exactly those problems.

`solutions_fix*.json` files are overlaid on top of the main bank so a rejected
slug that we have since corrected is re-submitted with the corrected code
(originals in friend_bank240.json are left untouched).

Usage: python build_retry_bank.py [ledger]
"""
import glob
import json
import os
import sys

LEDGER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('LEDGER_FILE', 'run_friend240.json')
BANK = 'friend_bank240.json'
FIXES = sorted(glob.glob('solutions_fix*.json'))
OUT = 'friend_bank_retry.json'

doc = json.load(open(LEDGER, encoding='utf-8'))
bank = json.load(open(BANK, encoding='utf-8'))
fixes = {}
for f in FIXES:
    fixes.update(json.load(open(f, encoding='utf-8')))

slugs = [r['slug'] for r in doc['rejected']]
out = {}
missing = []
patched = []
for s in slugs:
    if s in fixes:
        out[s] = fixes[s]
        patched.append(s)
    elif s in bank:
        out[s] = bank[s]
    else:
        missing.append(s)
json.dump(out, open(OUT, 'w', encoding='utf-8'), indent=1)
print('rejected slugs :', len(slugs), '| distinct:', len(set(slugs)))
print('banked code    :', len(out), '| using fixes:', patched)
print('fix files seen :', FIXES)
print('no code found  :', missing)
print('wrote', OUT)
