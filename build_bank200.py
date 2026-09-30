import json
import re

pool = json.load(open('library_all.json', encoding='utf-8'))
fix = json.load(open('solutions_fix1.json', encoding='utf-8'))
solved_now = {l.strip() for l in open('solved.txt', encoding='utf-8')
              if l.strip() and not l.startswith(('solved:', '='))}
noqid = {'arrange-coins', 'construct-rectangle', 'dominant-index',
         'one-bit-and-2-bit-characters', 'sum-of-squares-of-elements-in-array'}

n = 0
for k in fix:
    if k in pool and k not in solved_now:
        # fix1 file predates the solutions_fix1 driver-name corrections;
        # keep its logic but ensure the current verified driver names below.
        pool[k] = fix[k]
        n += 1
print('fix1 overrides applied:', n)

# Verified driver method names (from check-endpoint AttributeError messages):
renames = {
    'find-closest-person': 'findClosest',
    'lexicographically-smallest-string-after-a-swap': 'getSmallestString',
    'make-three-strings-equal': 'findMinimumOperations',
    'maximum-strong-pair-xor-i': 'maximumStrongPairXor',
    'longest-unequal-adjacent-groups-subsequence-i': 'getLongestSubsequence',
    'max-pair-sum-in-an-array': 'maxSum',
}
patched = 0
for slug, want in renames.items():
    code = pool.get(slug)
    if not code or slug in solved_now:
        continue
    code2 = re.sub(r'def \w+\(self', 'def ' + want + '(self', code, count=1)
    if code2 != code:
        pool[slug] = code2
        patched += 1
print('method renames patched:', patched)

# gen1 logic fixes (verified in prior session; bank first-seen order
# may hold the pre-fix variant):
latest = '''class Solution:
    def findLatestTime(self, s: str) -> str:
        h, m = s.split(':')
        if h == '??':
            h = '11'
        elif h[0] == '?':
            h = ('1' + h[1]) if h[1] in '01' else ('0' + h[1])
        elif h[1] == '?':
            h = (h[0] + '9') if h[0] == '0' else (h[0] + '1')
        if m == '??':
            m = '59'
        elif m[0] == '?':
            m = '5' + m[1]
        elif m[1] == '?':
            m = m[0] + '9'
        return h + ':' + m
'''
if 'latest-time-you-can-obtain-after-replacing-characters' in pool:
    pool['latest-time-you-can-obtain-after-replacing-characters'] = latest

longest = '''from typing import List
class Solution:
    def getLongestSubsequence(self, words: List[str], groups: List[int]) -> List[str]:
        res = []
        for i, gg in enumerate(groups):
            if not res or gg != groups[res[-1]]:
                res.append(i)
        return [words[i] for i in res]
'''
if 'longest-unequal-adjacent-groups-subsequence-i' in pool:
    pool['longest-unequal-adjacent-groups-subsequence-i'] = longest

validwords = '''import re
class Solution:
    def countValidWords(self, sentence: str) -> int:
        cnt = 0
        for tok in sentence.split():
            if re.fullmatch(r'([a-z]+(-[a-z]+)?)?[!.,]?', tok):
                cnt += 1
        return cnt
'''
if 'number-of-valid-words-in-a-sentence' in pool:
    pool['number-of-valid-words-in-a-sentence'] = validwords

bank = {k: v for k, v in pool.items() if k not in solved_now and k not in noqid}
items = list(bank.items())[:210]
json.dump(dict(items), open('friend_bank200.json', 'w', encoding='utf-8'))
print('friend_bank200:', len(items))
bad = [k for k, v in items if any(ord(c) > 127 for c in v)]
print('non-ascii:', bad)
