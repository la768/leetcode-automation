import json

led = json.load(open('run_friend100.json', encoding='utf-8'))
acc = {r['slug'] for r in led['accepted']}
rej = {r['slug'] for r in led['rejected']}
probe = ['add-to-array-form-of-integer', 'button-with-longest-push-time',
         'calculate-digit-sum-of-a-string',
         'check-if-strings-can-be-made-equal-with-operations-i',
         'consecutive-characters', 'count-pairs-that-form-a-complete-day-i',
         'determine-color-of-a-chessboard-square']
for s in probe:
    print(s, '| accepted:', s in acc, '| rejected:', s in rej)

pool = json.load(open('library_all.json', encoding='utf-8'))
solved = {l.strip() for l in open('solved.txt', encoding='utf-8')
          if l.strip() and not l.startswith(('solved:', '='))}
unsolved_pool = [k for k in pool if k not in solved]
b100 = json.load(open('friend_bank100.json', encoding='utf-8'))
b200 = json.load(open('friend_bank200.json', encoding='utf-8'))
print('pool:', len(pool), '| unsolved pool:', len(unsolved_pool))
print('bank100:', len(b100), '| bank200:', len(b200), '| union:', len(set(b100) | set(b200)))
print('pool minus used:', len([k for k in unsolved_pool if k not in set(b100) | set(b200)]))
print('library_unsolved.txt lines:', sum(1 for _ in open('library_unsolved.txt', encoding='utf-8')))
