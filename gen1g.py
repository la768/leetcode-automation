import json
BANK = {}
BANK['prime-in-diagonal'] = '''from typing import List
class Solution:
    def diagonalPrime(self, nums: List[List[int]]) -> int:
        def isp(x):
            if x < 2: return False
            if x % 2 == 0: return x == 2
            i = 3
            while i * i <= x:
                if x % i == 0: return False
                i += 2
            return True
        best = 0
        n = len(nums)
        for i in range(n):
            for v in (nums[i][i], nums[i][n - 1 - i]):
                if isp(v):
                    best = max(best, v)
        return best
'''
BANK['maximum-difference-by-remapping-a-digit'] = '''class Solution:
    def minMaxDifference(self, num: int) -> int:
        s = str(num)
        mx = s
        for c in s:
            if c != '9':
                mx = s.replace(c, '9')
                break
        mn = s.replace(s[0], '0')
        return int(mx) - int(mn)
'''
BANK['find-the-maximum-divisibility-score'] = '''from typing import List
class Solution:
    def maxDivScore(self, nums: List[int], divisors: List[int]) -> int:
        best_score = -1
        best = 0
        for d in sorted(set(divisors)):
            sc = sum(1 for x in nums if x % d == 0)
            if sc > best_score:
                best_score = sc
                best = d
        return best
'''
BANK['take-gifts-from-the-richest-pile'] = '''from typing import List
import heapq
class Solution:
    def pickGifts(self, gifts: List[int], k: int) -> int:
        h = [-g for g in gifts]
        heapq.heapify(h)
        for _ in range(k):
            g = -heapq.heappop(h)
            heapq.heappush(h, -int(g ** 0.5))
        return -sum(h)
'''
BANK['form-smallest-number-from-two-digit-arrays'] = '''from typing import List
class Solution:
    def minNumber(self, nums1: List[int], nums2: List[int]) -> int:
        s1, s2 = set(nums1), set(nums2)
        common = s1 & s2
        if common: return min(common)
        a, b = min(s1), min(s2)
        return min(a, b) * 10 + max(a, b)
'''
BANK['number-of-unequal-triplets-in-array'] = '''from typing import List
from collections import Counter
class Solution:
    def unequalTriplets(self, nums: List[int]) -> int:
        n = len(nums)
        cnt = Counter(nums)
        res = 0
        left = 0
        for v in cnt.values():
            right = n - left - v
            res += left * v * right
            left += v
        return res
'''
BANK['odd-string-difference'] = '''from typing import List
class Solution:
    def oddString(self, words: List[str]) -> str:
        diffs = []
        for w in words:
            diffs.append(tuple(ord(w[i + 1]) - ord(w[i]) for i in range(len(w) - 1)))
        for i, d in enumerate(diffs):
            others = [d2 for j, d2 in enumerate(diffs) if j != i]
            if d not in others:
                return words[i]
        return ''
'''
BANK['remove-letter-to-equalize-frequency'] = '''from collections import Counter
class Solution:
    def equalFrequency(self, word: str) -> bool:
        c = Counter(word)
        for ch in set(word):
            c[ch] -= 1
            vals = [v for v in c.values() if v > 0]
            if len(set(vals)) == 1:
                return True
            c[ch] += 1
        return False
'''
BANK['the-employee-that-worked-on-the-longest-task'] = '''from typing import List
class Solution:
    def hardestWorker(self, n: int, logs: List[List[int]]) -> int:
        best = -1
        best_id = -1
        prev = 0
        for eid, t in logs:
            d = t - prev
            if d > best or (d == best and eid < best_id):
                best = d
                best_id = eid
            prev = t
        return best_id
'''
BANK['count-days-spent-together'] = '''class Solution:
    def countDaysTogether(self, arriveAlice: str, leaveAlice: str, arriveBob: str, leaveBob: str) -> int:
        md = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        def day(s):
            m, d = s.split('-')
            m, d = int(m), int(d)
            return sum(md[:m - 1]) + d
        start = max(day(arriveAlice), day(arriveBob))
        end = min(day(leaveAlice), day(leaveBob))
        return max(0, end - start + 1)
'''
json.dump(BANK, open('solutions_gen1g.json', 'w', encoding='utf-8'), indent=1)
print('gen1g:', len(BANK))
