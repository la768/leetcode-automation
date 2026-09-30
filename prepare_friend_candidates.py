import json

BANK_FILES = ['solutions_y1.json', 'solutions_y2.json', 'solutions_y3.json', 'solutions_y4.json']

with open('solved.txt', encoding='utf-8') as f:
    solved = {l.strip() for l in f if l.strip() and not l.startswith(('solved:', '='))}

banks = {}
for path in BANK_FILES:
    with open(path, encoding='utf-8') as f:
        banks[path] = json.load(f)

total_entries = sum(len(d) for d in banks.values())
per_bank = {p: len(d) for p, d in banks.items()}

all_slugs = []
avail = {}  # slug -> list of bank files containing it
for path, d in banks.items():
    for slug, code in d.items():
        all_slugs.append(slug)
        avail.setdefault(slug, []).append(path)

dupes = sorted(s for s, ps in avail.items() if len(ps) > 1)
unique = set(avail)

already = sorted(s for s in unique if s in solved)
genuinely_unsolved = sorted(s for s in unique if s not in solved)

invalid = []
qid_index = {}
try:
    with open('qids.json', encoding='utf-8') as f:
        qid_index = json.load(f)
    for s in genuinely_unsolved:
        if not isinstance(banks[[p for p in BANK_FILES if s in banks[p]][0]][s], str):
            invalid.append(s)
        elif s not in qid_index:
            invalid.append(s + ' [no cached qid]')
except FileNotFoundError:
    print('NOTE: qids.json not present; cached-qid check skipped.')

with open('friend_candidates.json', 'w', encoding='utf-8') as f:
    json.dump({s: banks[[p for p in BANK_FILES if s in banks[p]][0]][s] for s in genuinely_unsolved},
              f, indent=1)

print('BANK ENTRIES TOTAL :', total_entries, per_bank)
print('UNIQUE BANK SLUGS  :', len(unique))
print('DUPLICATE SLUGS    :', len(dupes), dupes if dupes else '')
print('ALREADY SOLVED     :', len(already), already if already else '')
print('GENUINELY UNSOLVED :', len(genuinely_unsolved))
print('INVALID/NO-QID     :', len(invalid), invalid if invalid else '')
print('candidate bank -> friend_candidates.json')
