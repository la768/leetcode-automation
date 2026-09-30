"""Builds the submittable library slice for the 240 campaign.

A library slug is usable only if it is (a) still unsolved for this account,
(b) python3-capable per screen.py, and (c) not account-restricted.
"""
import json

RESTRICTED = {'design-hashmap', 'design-hashset'}  # Restrictions Failed for this account

merged = json.load(open('library_merged.json', encoding='utf-8'))
scr = json.load(open('screened.json', encoding='utf-8'))
uns_easy = {l.strip() for l in open('unsolved_easy.txt', encoding='utf-8') if l.strip()}
uns_med = {l.strip() for l in open('unsolved_medium.txt', encoding='utf-8') if l.strip()}
uns = uns_easy | uns_med

ready, dropped = {}, {}
for slug, code in merged.items():
    s = scr.get(slug) or {}
    if slug not in uns:
        dropped[slug] = 'already solved'
    elif slug in RESTRICTED:
        dropped[slug] = 'account restricted'
    elif not s.get('langs'):
        dropped[slug] = 'premium / unknown slug'
    elif not s.get('py3'):
        dropped[slug] = 'no python3 (' + ','.join(s.get('langs') or []) + ')'
    elif s.get('paid'):
        dropped[slug] = 'paid only'
    else:
        ready[slug] = code

json.dump(ready, open('friend_bank240_lib.json', 'w', encoding='utf-8'), indent=1)
easy = [s for s in ready if s in uns_easy]
med = [s for s in ready if s in uns_med]
print('library submittable:', len(ready), '| easy:', len(easy), '| medium:', len(med))
print('dropped:', len(dropped))
from collections import Counter
print(Counter(dropped.values()))
print('MEDIUM ones:', med)
print('--- the easy ones ---')
for i in range(0, len(easy), 6):
    print('  ' + '  '.join('%-40s' % s for s in sorted(easy)[i:i + 6]))
