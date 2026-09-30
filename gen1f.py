import json
BANK = {}
BANK['subarrays-distinct-element-sum-of-squares-i'] = '''from typing import List
class Solution:
    def sumCounts(self, nums: List[int]) -> int:
        n = len(nums)
        total = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                seen.add(nums[j])
                d = len(seen)
                total += d * d
        return total % (10 ** 9 + 7)
'''
BANK['maximum-value-of-an-ordered-triplet-i'] = '''from typing import List
class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        n = len(nums)
        best = 0
        maxi = nums[0]
        diff = 0
        for k in range(2, n):
            diff = max(diff, maxi - nums[k - 1])
            best = max(best, diff * nums[k])
            maxi = max(maxi, nums[k - 1])
        return best
'''
BANK['longest-unequal-adjacent-groups-subsequence-i'] = '''from typing import List
class Solution:
    def getWordsInLongestSubsequence(self, words: List[str], groups: List[int]) -> List[int]:
        res = []
        last = -1
        for i, g in enumerate(groups):
            if not res or g != last:
                res.append(i)
                last = g
        return res
'''
BANK['minimum-right-shifts-to-sort-the-array'] = '''from typing import List
class Solution:
    def minimumRightShifts(self, nums: List[int]) -> int:
        n = len(nums)
        desc = [i for i in range(1, n) if nums[i] < nums[i - 1]]
        if len(desc) == 0:
            return 0
        if len(desc) > 1:
            return -1
        d = desc[0]
        if nums[0] < nums[-1]:
            return -1
        return n - d
'''
BANK['minimum-operations-to-collect-elements'] = '''from typing import List
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        need = set(range(1, k + 1))
        seen = set()
        ops = 0
        for v in reversed(nums):
            ops += 1
            seen.add(v)
            if need <= seen:
                return ops
        return ops
'''
BANK['points-that-intersect-with-cars'] = '''from typing import List
class Solution:
    def numberOfPoints(self, nums: List[List[int]]) -> int:
        covered = set()
        for a, b in nums:
            for x in range(a, b + 1):
                covered.add(x)
        return len(covered)
'''
BANK['max-pair-sum-in-an-array'] = '''from typing import List
from collections import defaultdict
class Solution:
    def maxPairSum(self, nums: List[int]) -> int:
        groups = defaultdict(list)
        for x in nums:
            m = max(str(x))
            groups[m].append(x)
        best = -1
        for g in groups.values():
            if len(g) >= 2:
                g.sort(reverse=True)
                best = max(best, g[0] + g[1])
        return best
'''
BANK['find-the-losers-of-the-circular-game'] = '''from typing import List
class Solution:
    def circularGameLosers(self, n: int, k: int) -> List[int]:
        got = [False] * (n + 1)
        cur = 1
        got[1] = True
        i = 1
        while True:
            cur = (cur + i * k - 1) % n + 1
            if got[cur]:
                break
            got[cur] = True
            i += 1
        return [x for x in range(2, n + 1) if not got[x]]
'''
BANK['find-the-distinct-difference-array'] = '''from typing import List
class Solution:
    def distinctDifferenceArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = []
        for i in range(n):
            pre = len(set(nums[:i + 1]))
            suf = len(set(nums[i + 1:]))
            res.append(pre - suf)
        return res
'''
BANK['find-the-longest-balanced-substring-of-a-binary-string'] = '''class Solution:
    def findTheLongestBalancedSubstring(self, s: str) -> int:
        best = 0
        i = 0
        n = len(s)
        while i < n:
            z = 0
            while i < n and s[i] == '0':
                z += 1
                i += 1
            o = 0
            while i < n and s[i] == '1':
                o += 1
                i += 1
            best = max(best, 2 * min(z, o))
            if o == 0 and z == 0:
                i += 1
        return best
'''
json.dump(BANK, open('solutions_gen1f.json', 'w', encoding='utf-8'), indent=1)
print('gen1f:', len(BANK))
