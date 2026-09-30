"""Coverage report for the next campaign: which unsolved slugs already have code?"""
import json
import os

def load(path):
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception as e:
        print('  (cannot load', path, '-', e, ')')
        return {}

solved = {l.strip() for l in open('solved.txt', encoding='utf-8')
          if l.strip() and not l.startswith(('solved:', '='))}
uns_easy = {l.strip() for l in open('unsolved_easy.txt', encoding='utf-8') if l.strip()}
uns_med = {l.strip() for l in open('unsolved_medium.txt', encoding='utf-8') if l.strip()}
uns = uns_easy | uns_med
print('solved:', len(solved), '| unsolved easy:', len(uns_easy), '| medium:', len(uns_med), '| union:', len(uns))
print('overlap solved&unsolved:', len(solved & uns))

stores = {}
for f in ['library_all.json', 'solutions_extra.json', 'solutions_fix2.json',
          'solutions_y1.json', 'solutions_y2.json', 'solutions_y3.json', 'solutions_y4.json',
          'SOLUTIONS_MASTER.json']:
    if os.path.exists(f):
        d = load(f)
        stores[f] = d
        print('%-24s entries: %d | still-unsolved: %d | solved: %d | not-a-real-slug?: %d'
              % (f, len(d), len([k for k in d if k in uns]),
                 len([k for k in d if k in solved]), len([k for k in d if k not in uns and k not in solved])))

merged = {}
for f, d in stores.items():
    for k, v in d.items():
        merged.setdefault(k, v)
json.dump(merged, open('library_merged.json', 'w', encoding='utf-8'), indent=1)
print('merged library:', len(merged))
ready_easy = sorted(k for k in merged if k in uns_easy)
ready_med = sorted(k for k in merged if k in uns_med)
print('READY to submit from library: easy=%d medium=%d total=%d'
      % (len(ready_easy), len(ready_med), len(ready_easy) + len(ready_med)))
print('ready medium sample:', ready_med[:15])
print('ready easy sample:', ready_easy[:15])
