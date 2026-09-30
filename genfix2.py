import json
solved = set(l.strip() for l in open('solved.txt', encoding='utf-8') if l.strip())
g = json.load(open('solutions_gen1.json', encoding='utf-8'))
FIX = {
'find-closest-person': '''from typing import List
class Solution:
    def findClosest(self, x: int, y: int, z: int) -> int:
        dx = abs(x - z); dy = abs(y - z)
        if dx < dy: return 1
        if dy < dx: return 2
        return 0
''',
'lexicographically-smallest-string-after-a-swap': '''class Solution:
    def getSmallestString(self, s: str) -> str:
        for i in range(len(s) - 1):
            if (ord(s[i]) - 48) % 2 == (ord(s[i + 1]) - 48) % 2:
                return s[:i] + s[i + 1] + s[i] + s[i + 2:]
        return s
''',
'make-three-strings-equal': '''class Solution:
    def findMinimumOperations(self, s1: str, s2: str, s3: str) -> int:
        p = 0
        while p < len(s1) and p < len(s2) and p < len(s3) and s1[p] == s2[p] == s3[p]:
            p += 1
        if p == 0: return -1
        return (len(s1) - p) + (len(s2) - p) + (len(s3) - p)
''',
'maximum-strong-pair-xor-i': '''from typing import List
class Solution:
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        best = 0
        for x in nums:
            for y in nums:
                if abs(x - y) <= min(x, y):
                    best = max(best, x ^ y)
        return best
''',
'longest-unequal-adjacent-groups-subsequence-i': '''from typing import List
class Solution:
    def getLongestSubsequence(self, words: List[str], groups: List[int]) -> List[int]:
        res = []
        for i, gg in enumerate(groups):
            if not res or gg != groups[res[-1]]:
                res.append(i)
        return res
''',
'latest-time-you-can-obtain-after-replacing-characters': '''class Solution:
    def findLatestTime(self, s: str) -> str:
        h, m = s.split(':')
        if h == '??':
            h = '11'
        elif h[0] == '?':
            h = ('1' + h[1]) if h[1] in '01' else ('0' + h[1])
        elif h[1] == '?':
            h = h[0] + '1'
        if m == '??':
            m = '59'
        elif m[0] == '?':
            m = '5' + m[1]
        elif m[1] == '?':
            m = m[0] + '9'
        return h + ':' + m
''',
'sum-of-squares-of-special-elements': '''from typing import List
class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        n = len(nums)
        return sum(nums[i] * nums[i] for i in range(n) if n % (i + 1) == 0)
''',
}
for s, v in FIX.items():
    g[s] = v
json.dump(g, open('solutions_gen1.json', 'w', encoding='utf-8'), indent=1)
remaining = [s for s in FIX if s not in solved]
print('fixes:', len(FIX), '| still unsolved:', remaining)
