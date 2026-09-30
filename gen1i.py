import json
BANK = {}
BANK['sort-even-and-odd-indices-independently'] = '''from typing import List
class Solution:
    def sortEvenOdd(self, nums: List[int]) -> List[int]:
        ev = sorted(nums[0::2])
        od = sorted(nums[1::2], reverse=True)
        out = []
        for i in range(len(nums)):
            out.append(ev[i // 2] if i % 2 == 0 else od[i // 2])
        return out
'''
BANK['rings-and-rods'] = '''class Solution:
    def countPoints(self, rings: str) -> int:
        rods = {}
        for i in range(0, len(rings), 2):
            c, r = rings[i], rings[i + 1]
            rods.setdefault(r, set()).add(c)
        return sum(1 for v in rods.values() if len(v) == 3)
'''
BANK['finding-3-digit-even-numbers'] = '''from typing import List
class Solution:
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        res = set()
        n = len(digits)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if i == j or j == k or i == k: continue
                    if digits[i] == 0: continue
                    if digits[k] % 2: continue
                    res.add(digits[i] * 100 + digits[j] * 10 + digits[k])
        return sorted(res)
'''
BANK['find-target-indices-after-sorting-array'] = '''from typing import List
class Solution:
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        nums.sort()
        return [i for i, x in enumerate(nums) if x == target]
'''
BANK['find-subsequence-of-length-k-with-the-largest-sum'] = '''from typing import List
class Solution:
    def maxSubsequence(self, nums: List[int], k: int) -> List[int]:
        idx = sorted(range(len(nums)), key=lambda i: nums[i], reverse=True)[:k]
        idx.sort()
        return [nums[i] for i in idx]
'''
BANK['two-furthest-houses-with-different-colors'] = '''from typing import List
class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        best = 0
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                if colors[i] != colors[j]:
                    best = max(best, j - i)
        return best
'''
BANK['time-needed-to-buy-tickets'] = '''from typing import List
class Solution:
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        t = 0
        for i, x in enumerate(tickets):
            if i <= k:
                t += min(x, tickets[k])
            else:
                t += min(x, tickets[k] - 1)
        return t
'''
BANK['smallest-index-with-equal-value'] = '''from typing import List
class Solution:
    def smallestEqual(self, nums: List[int]) -> int:
        for i, x in enumerate(nums):
            if i % 10 == x:
                return i
        return -1
'''
BANK['number-of-valid-words-in-a-sentence'] = '''import re
class Solution:
    def countValidWords(self, sentence: str) -> int:
        cnt = 0
        for tok in sentence.split():
            if re.fullmatch(r'([a-z]+(-[a-z]+)?)?[!.,]*', tok):
                cnt += 1
        return cnt
'''
BANK['two-out-of-three'] = '''from typing import List
class Solution:
    def twoOutOfThree(self, nums1: List[int], nums2: List[int], nums3: List[int]) -> List[int]:
        s1, s2, s3 = set(nums1), set(nums2), set(nums3)
        return sorted((s1 & s2) | (s1 & s3) | (s2 & s3))
'''
json.dump(BANK, open('solutions_gen1i.json', 'w', encoding='utf-8'), indent=1)
print('gen1i:', len(BANK))
