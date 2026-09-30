import json, glob
solved = set(l.strip() for l in open('solved.txt', encoding='utf-8') if l.strip())
bank = {}
for f in sorted(glob.glob('solutions_gen1[a-j].json')):
    d = json.load(open(f, encoding='utf-8'))
    for s, v in d.items():
        bank.setdefault(s, v)
final = {s: v for s, v in bank.items() if s not in solved}
json.dump(final, open('solutions_gen1.json', 'w', encoding='utf-8'), indent=1)
print('gen1 total unique:', len(bank), '| unsolved:', len(final))
print(sorted(final))
