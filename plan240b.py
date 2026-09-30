"""Eligible authoring pool: unsolved, no code in the library, python3-capable, free."""
import json

scr = json.load(open('screened.json', encoding='utf-8'))
cand = json.load(open('candidates_new.json', encoding='utf-8'))
out = {}
for slug, diff in cand.items():
    if diff != 'Easy':
        continue
    s = scr.get(slug) or {}
    if s.get('py3') and not s.get('paid'):
        out[slug] = s.get('title')
json.dump(out, open('authoring_pool.json', 'w', encoding='utf-8'), indent=1)
print('eligible easy no-code slugs:', len(out))
for i, slug in enumerate(sorted(out)):
    print('%-46s %s' % (slug, out[slug]), end='\n' if i % 1 == 0 else '')
