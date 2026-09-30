"""Merges EVERY solution bank in the workspace into library_full.json.

Earlier campaigns only merged library_all + SOLUTIONS_MASTER + y1-y4 + extras,
so a lot of authored code is sitting in the per-batch files (solutions_gen1*,
solutions_big*, solutions_new*, solutions_b*, solutions_c, ...). This script
finds all of them, keeps the first definition of a slug (with provenance), and
reports how many of those slugs are still unsolved for the friend account.
"""
import glob
import json
import os

SKIP = {'qids.json', 'screened.json', 'specs.json', 'candidates_new.json',
        'library_merged.json', 'library_full.json', 'authoring_pool.json',
        'login_status.json', 'package.json', 'package-lock.json',
        'run_friend100.json', 'friend_bank100.json', 'friend_bank200.json',
        'run_friend240.json'}

files = []
for pat in ['*.json']:
    files += glob.glob(pat)
files = sorted(f for f in files if os.path.basename(f) not in SKIP)

merged = {}
prov = {}
for f in files:
    try:
        d = json.load(open(f, encoding='utf-8'))
    except Exception:
        continue
    if not isinstance(d, dict) or not d:
        continue
    if not any(isinstance(v, str) and ('class ' in v or 'def ' in v) for v in d.values()):
        continue
    added = 0
    for k, v in d.items():
        if not isinstance(v, str) or 'class ' not in v:
            continue
        if k not in merged:
            merged[k] = v
            prov[k] = f
            added += 1
    print('%-28s +%3d (total %d)' % (f, added, len(merged)))

json.dump(merged, open('library_full.json', 'w', encoding='utf-8'), indent=1)
json.dump(prov, open('library_full_prov.json', 'w', encoding='utf-8'), indent=1)

solved = {l.strip() for l in open('solved.txt', encoding='utf-8')
          if l.strip() and not l.startswith(('solved:', '='))}
uns = {l.strip() for l in open('unsolved_easy.txt', encoding='utf-8') if l.strip()}
uns |= {l.strip() for l in open('unsolved_medium.txt', encoding='utf-8') if l.strip()}
cand = [k for k in merged if k in uns]
print('\nALL banks: %d slugs | still unsolved: %d | solved: %d | unknown: %d'
      % (len(merged), len(cand), len([k for k in merged if k in solved]),
         len([k for k in merged if k not in uns and k not in solved])))
