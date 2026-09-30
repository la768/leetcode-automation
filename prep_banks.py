import json

BAD = [chr(c) for c in (8203, 8204, 8205, 65279, 160, 8232, 8233, 8199, 8288)]


def clean(s):
    for b in BAD:
        s = s.replace(b, '')
    return s


unsolved = set()
for line in open('unsolved.txt', encoding='utf-8'):
    line = line.strip()
    if line and not line.startswith(('unsolved:', '=')):
        unsolved.add(line)

solved = set()
for line in open('solved.txt', encoding='utf-8'):
    line = line.strip()
    if line and not line.startswith(('solved:', '=')):
        solved.add(line)

total = 0
for f in ['solutions_y1.json', 'solutions_y2.json', 'solutions_y3.json', 'solutions_y4.json']:
    raw = open(f, encoding='utf-8').read()
    if any(b in raw for b in BAD):
        fixed = clean(raw)
        json.loads(fixed)
        open(f, 'w', encoding='utf-8').write(fixed)
        raw = fixed
        print('STRIPPED hidden chars from', f)
    d = json.loads(raw)
    nonascii = [k for k, v in d.items() if any(ord(c) > 127 for c in k + v)]
    notin = [k for k in d if k not in unsolved]
    insol = [k for k in d if k in solved]
    print(f, 'entries:', len(d), '| non-ascii:', len(nonascii), '| not-in-unsolved:', len(notin), '| already-solved:', len(insol))
    if nonascii:
        print('   BAD:', nonascii)
    if notin:
        print('   NOT-UNSOLVED:', notin)
    if insol:
        print('   ALREADY-SOLVED:', insol)
    total += len(d)
print('TOTAL candidates:', total)