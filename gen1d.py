import json
BANK = {}
BANK['find-the-child-who-has-the-ball-after-k-seconds'] = '''class Solution:
    def numberOfChild(self, n: int, k: int) -> int:
        p = k % (2 * (n - 1))
        return p if p <= n - 1 else 2 * (n - 1) - p
'''
BANK['find-the-number-of-good-pairs-i'] = '''from typing import List
class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        cnt = 0
        for a in nums1:
            for b in nums2:
                if a % (b * k) == 0:
                    cnt += 1
        return cnt
'''
BANK['special-array-i'] = '''from typing import List
class Solution:
    def isArraySpecial(self, nums: List[int]) -> bool:
        return all((a % 2) != (b % 2) for a, b in zip(nums, nums[1:]))
'''
BANK['find-the-xor-of-numbers-which-appear-twice'] = '''from typing import List
from collections import Counter
class Solution:
    def duplicateNumbersXOR(self, nums: List[int]) -> int:
        c = Counter(nums)
        res = 0
        for x, v in c.items():
            if v == 2: res ^= x
        return res
'''
BANK['permutation-difference-between-two-strings'] = '''class Solution:
    def findPermutationDifference(self, s: str, t: str) -> int:
        pos = {c: i for i, c in enumerate(t)}
        return sum(abs(i - pos[c]) for i, c in enumerate(s))
'''
BANK['count-the-number-of-special-characters-i'] = '''class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        lo = set(c for c in word if c.islower())
        up = set(c for c in word if c.isupper())
        return sum(1 for c in lo if c.upper() in up)
'''
BANK['valid-word'] = '''class Solution:
    def isValid(self, word: str) -> bool:
        if len(word) < 3: return False
        if not word.isalnum(): return False
        v = any(c in 'aeiouAEIOU' for c in word)
        co = any(c.isalpha() and c not in 'aeiouAEIOU' for c in word)
        return v and co
'''
BANK['longest-strictly-increasing-or-strictly-decreasing-subarray'] = '''from typing import List
class Solution:
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        best = 1
        inc = dec = 1
        for i in range(1, n):
            if nums[i] > nums[i - 1]:
                inc += 1; dec = 1
            elif nums[i] < nums[i - 1]:
                dec += 1; inc = 1
            else:
                inc = dec = 1
            best = max(best, inc, dec)
        return best
'''
BANK['find-the-sum-of-encrypted-integers'] = '''from typing import List
class Solution:
    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        total = 0
        for x in nums:
            s = str(x)
            m = max(s)
            total += int(m * len(s))
        return total
'''
BANK['latest-time-you-can-obtain-after-replacing-characters'] = '''class Solution:
    def findLatestTime(self, s: str) -> str:
        h, m = s.split(':')
        if h == '??':
            h = '11'
        elif h[0] == '?':
            h = '1' + h[1]
        elif h[1] == '?':
            h = h[0] + '1'
        if m == '??':
            m = '59'
        elif m[0] == '?':
            m = '5' + m[1]
        elif m[1] == '?':
            m = m[0] + '9'
        return h + ':' + m
'''
json.dump(BANK, open('solutions_gen1d.json', 'w', encoding='utf-8'), indent=1)
print('gen1d:', len(BANK))
