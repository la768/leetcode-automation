import json
solved = set(l.strip() for l in open('solved.txt', encoding='utf-8') if l.strip())
g = json.load(open('solutions_gen1.json', encoding='utf-8'))
FIX = {
'lexicographically-smallest-string-after-a-swap': '''class Solution:
    def getSmallestString(self, s: str) -> str:
        for i in range(len(s) - 1):
            if (ord(s[i]) - 48) % 2 == (ord(s[i + 1]) - 48) % 2 and s[i] > s[i + 1]:
                return s[:i] + s[i + 1] + s[i] + s[i + 2:]
        return s
''',
'longest-unequal-adjacent-groups-subsequence-i': '''from typing import List
class Solution:
    def getLongestSubsequence(self, words: List[str], groups: List[int]) -> List[str]:
        res = []
        for i, gg in enumerate(groups):
            if not res or gg != groups[res[-1]]:
                res.append(i)
        return [words[i] for i in res]
''',
'latest-time-you-can-obtain-after-replacing-characters': '''class Solution:
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
''',
'max-pair-sum-in-an-array': '''from typing import List
from collections import defaultdict
class Solution:
    def maxSum(self, nums: List[int]) -> int:
        groups = defaultdict(list)
        for x in nums:
            m = max(str(x))
            groups[m].append(x)
        best = -1
        for gg in groups.values():
            if len(gg) >= 2:
                gg.sort(reverse=True)
                best = max(best, gg[0] + gg[1])
        return best
''',
'number-of-valid-words-in-a-sentence': '''import re
class Solution:
    def countValidWords(self, sentence: str) -> int:
        cnt = 0
        for tok in sentence.split():
            if re.fullmatch(r'([a-z]+(-[a-z]+)?)?[!.,]?', tok):
                cnt += 1
        return cnt
''',
}
for s, v in FIX.items():
    g[s] = v
json.dump(g, open('solutions_gen1.json', 'w', encoding='utf-8'), indent=1)
print('fix3 unsolved:', [s for s in FIX if s not in solved])
