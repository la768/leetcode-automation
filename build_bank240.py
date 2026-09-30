"""Builds friend_bank240.json for the 240-new-Accepted campaign.

Order: locally validated authored solutions first (judge_local green), then the
remaining banked solutions from other campaigns. Account-restricted slugs and
anything without python3 support are excluded.
"""
import json

RESTRICTED = {'design-hashmap', 'design-hashset'}
AUTHORED = ['solutions_a%d.json' % i for i in range(1, 12)]

uns = {l.strip() for l in open('unsolved_easy.txt', encoding='utf-8') if l.strip()}
uns |= {l.strip() for l in open('unsolved_medium.txt', encoding='utf-8') if l.strip()}
solved = {l.strip() for l in open('solved.txt', encoding='utf-8')
          if l.strip() and not l.startswith(('solved:', '='))}
scr = json.load(open('screened.json', encoding='utf-8'))
cand = json.load(open('cand_full.json', encoding='utf-8'))

authored = {}
for f in AUTHORED:
    authored.update(json.load(open(f, encoding='utf-8')))

bank = {}
for slug, code in authored.items():
    if slug in uns and slug not in solved and slug not in RESTRICTED:
        s = scr.get(slug) or {}
        if s.get('py3') and not s.get('paid'):
            bank[slug] = code
n_auth = len(bank)
for slug, code in cand.items():
    if slug in bank or slug in RESTRICTED or slug in solved:
        continue
    s = scr.get(slug) or {}
    if not s.get('py3') or s.get('paid'):
        continue
    bank[slug] = code

json.dump(bank, open('friend_bank240.json', 'w', encoding='utf-8'), indent=1)
print('authored (judge-validated) :', n_auth)
print('library top-up             :', len(bank) - n_auth)
print('friend_bank240 total       :', len(bank))
print('spare over the 240 target  :', len(bank) - 240)
bad = [k for k in bank if any(ord(c) > 127 for c in bank[k])]
print('non-ascii entries:', bad)
