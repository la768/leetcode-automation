"""Local brute-force verification of solutions_fix2.json (no submissions).

Run:  python verify_fix2.py
Every fixed solution is executed against a naive reference implementation on
random + edge inputs. Prints PASS/FAIL per problem.
"""
import json
import random
import itertools

FIX = json.load(open('solutions_fix2.json', encoding='utf-8'))
fails = []


def load(slug):
    ns = {}
    exec(FIX[slug], ns)
    return ns['Solution']()


def check(name, got, want, extra=''):
    ok = got == want
    print(('PASS ' if ok else 'FAIL ') + name, '| got', got, '| want', want, extra)
    if not ok:
        fails.append(name)


# ---- 989 add-to-array-form-of-integer -------------------------------------
s = load('add-to-array-form-of-integer')
for num, k in [([1, 2, 0, 0], 34), ([2, 7, 4], 181), ([2, 1, 5], 806),
               ([9, 9, 9], 1), ([0], 23), ([1] + [0] * 60, 1)]:
    check('addToArrayForm ' + str(num[:4]) + '...+' + str(k),
          s.addToArrayForm(list(num), k),
          [int(d) for d in str(int(''.join(map(str, num))) + k)])
# the digit-limit stress case (5000 digits) must not raise
big = [9] * 5000
r = s.addToArrayForm(list(big), 1)
check('addToArrayForm 5000 nines +1', (len(r), r[0], r[-1]), (5001, 1, 0))

# ---- 3386 button-with-longest-push-time -----------------------------------
sl = load('button-with-longest-push-time')


def ref_button(ev):
    dur = [ev[0][1]] + [ev[i][1] - ev[i - 1][1] for i in range(1, len(ev))]
    best = max(dur)
    return min(ev[i][0] for i in range(len(ev)) if dur[i] == best)


for ev in [[[1, 2], [2, 5], [3, 9], [1, 15]], [[10, 5], [1, 7]],
           [[9, 6], [3, 6]], [[1, 4], [10, 6], [2, 6]]]:
    check('buttonWithLongestTime ' + str(ev), sl.buttonWithLongestTime([list(e) for e in ev]),
          ref_button(ev))
for _ in range(300):
    n = random.randint(1, 6)
    times = sorted(random.sample(range(0, 40), n)) or [0]
    ev = [[random.randint(1, 4), t] for t in times]
    ev[0][1] = random.randint(0, 3)
    if sl.buttonWithLongestTime([list(e) for e in ev]) != ref_button(ev):
        check('button random ' + str(ev), sl.buttonWithLongestTime([list(e) for e in ev]),
              ref_button(ev))
        break
else:
    print('PASS buttonWithLongestTime 300 random cases')

# ---- 2243 calculate-digit-sum-of-a-string ---------------------------------
sd = load('calculate-digit-sum-of-a-string')


def ref_digit(s, k):
    while len(s) > k:
        s = ''.join(str(sum(int(c) for c in s[i:i + k])) for i in range(0, len(s), k))
    return s


for s, k in [('11111222223', 3), ('00000000', 3), ('1', 5),
             ('999999999', 4), ('1234', 2)]:
    check('digitSum(%s, %d)' % (s, k), sd.digitSum(s, k), ref_digit(s, k))
    check('digitSum type is str', isinstance(sd.digitSum(s, k), str), True)

# ---- 2839 check-if-strings-can-be-made-equal-with-operations-i ------------
sc = load('check-if-strings-can-be-made-equal-with-operations-i')


def ref_canbe(s1, s2):
    # exhaustive: allowed moves are swaps (i, i+2) inside either string
    seen, stack = {s1}, [s1]
    while stack:
        cur = stack.pop()
        for i in range(len(cur) - 2):
            nxt = list(cur)
            nxt[i], nxt[i + 2] = nxt[i + 2], nxt[i]
            nxt = ''.join(nxt)
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return s2 in seen


cases = [('abcd', 'cdab'), ('abcd', 'dacb'), ('ab', 'ba'), ('aa', 'bb'),
         ('abcde', 'cdeab'), ('abcd', 'badc'), ('aabb', 'bbaa')]
for a, b in cases:
    check('canBeEqual(%s,%s)' % (a, b), sc.canBeEqual(a, b), ref_canbe(a, b))
random.seed(7)
for _ in range(400):
    n = random.choice([1, 2, 3, 4])
    a = ''.join(random.choice('ab') for _ in range(n))
    b = ''.join(random.choice('ab') for _ in range(n))
    if sc.canBeEqual(a, b) != ref_canbe(a, b):
        check('canBeEqual random (%s,%s)' % (a, b), sc.canBeEqual(a, b), ref_canbe(a, b))
        break
else:
    print('PASS canBeEqual 400 random cases')

# ---- 1446 consecutive-characters ------------------------------------------
sp = load('consecutive-characters')


def ref_maxpower(s):
    best = cur = 0
    for i, ch in enumerate(s):
        cur = cur + 1 if i and ch == s[i - 1] else 1
        best = max(best, cur)
    return best


for s in ['leetcode', 'abbcccddddeeeeedcba', 'a', 'aa', 'abcd', 'abccdde']:
    check('maxPower(%s)' % s, sp.maxPower(s), ref_maxpower(s))

# ---- 3184 count-pairs-that-form-a-complete-day-i --------------------------
cp = load('count-pairs-that-form-a-complete-day-i')


def ref_pairs(hours):
    return sum(1 for i in range(len(hours)) for j in range(i + 1, len(hours))
               if (hours[i] + hours[j]) % 24 == 0)


for h in [[12, 12, 30, 24, 24], [72, 48, 24, 3], [1, 23, 47], [1, 2, 3], [24]]:
    check('countCompleteDayPairs ' + str(h), cp.countCompleteDayPairs(list(h)), ref_pairs(h))
random.seed(11)
for _ in range(400):
    n = random.randint(0, 12)
    h = [random.randint(1, 100) for _ in range(n)]
    if cp.countCompleteDayPairs(list(h)) != ref_pairs(h):
        check('countCompleteDayPairs random ' + str(h),
              cp.countCompleteDayPairs(list(h)), ref_pairs(h))
        break
else:
    print('PASS countCompleteDayPairs 400 random cases')

# ---- 1812 determine-color-of-a-chessboard-square --------------------------
sq = load('determine-color-of-a-chessboard-square')
# truth table: a1 is dark -> False; colour alternates along file and rank
truth = {}
for f, c in enumerate('abcdefgh'):
    for r in range(1, 9):
        truth[c + str(r)] = (f + r) % 2 == 0
bad = [k for k, v in truth.items() if sq.squareIsWhite(k) != v]
check('squareIsWhite a1', sq.squareIsWhite('a1'), False)
check('squareIsWhite h3', sq.squareIsWhite('h3'), True)
check('squareIsWhite b1', sq.squareIsWhite('b1'), True)
check('squareIsWhite 64-square table', bad, [])

print()
print('TOTAL FAILURES:', len(fails), fails)
