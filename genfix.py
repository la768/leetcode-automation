import json
FIX = {}
FIX['first-unique-even-element'] = '''from typing import List
from collections import Counter
class Solution:
    def firstUniqueEven(self, nums: List[int]) -> int:
        c = Counter(nums)
        for x in nums:
            if x % 2 == 0 and c[x] == 1: return x
        return -1
'''
FIX['substrings-of-size-three-with-distinct-characters'] = '''class Solution:
    def countGoodSubstrings(self, s: str) -> int:
        return sum(1 for i in range(len(s) - 2) if len(set(s[i:i + 3])) == 3)
'''
FIX['shortest-distance-to-target-string-in-a-circular-array'] = '''from typing import List
class Solution:
    def closestTarget(self, words: List[str], target: str, startIndex: int) -> int:
        n = len(words)
        best = float('inf')
        for i in range(n):
            if words[i] == target:
                d = abs(startIndex - i)
                best = min(best, d, n - d)
        return -1 if best == float('inf') else best
'''
FIX['add-to-array-form-of-integer'] = '''from typing import List
class Solution:
    def addToArrayForm(self, num: List[int], k: int) -> List[int]:
        res = []
        i = len(num) - 1
        carry = k
        while i >= 0 or carry > 0:
            if i >= 0:
                carry += num[i]
                i -= 1
            res.append(carry % 10)
            carry //= 10
        return res[::-1]
'''
FIX['consecutive-characters'] = '''class Solution:
    def maxPower(self, s: str) -> int:
        best = 1
        cur = 1
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                cur += 1
            else:
                cur = 1
            best = max(best, cur)
        return best
'''
FIX['difference-between-element-sum-and-digit-sum-of-an-array'] = '''from typing import List
class Solution:
    def differenceOfSum(self, nums: List[int]) -> int:
        e = sum(nums)
        d = sum(int(c) for x in nums for c in str(x))
        return abs(e - d)
'''
FIX['distribute-elements-into-two-arrays-i'] = '''from typing import List
class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        a1 = [nums[0]]
        a2 = [nums[1]]
        for x in nums[2:]:
            if a1[-1] > a2[-1]:
                a1.append(x)
            else:
                a2.append(x)
        return a1 + a2
'''
FIX['faulty-keyboard'] = '''class Solution:
    def finalString(self, s: str) -> str:
        res = []
        for c in s:
            if c == 'i':
                res.reverse()
            else:
                res.append(c)
        return ''.join(res)
'''
FIX['find-common-elements-between-two-arrays'] = '''from typing import List
class Solution:
    def findIntersectionValues(self, nums1: List[int], nums2: List[int]) -> List[int]:
        s1 = set(nums1)
        s2 = set(nums2)
        return [sum(1 for x in nums1 if x in s2), sum(1 for x in nums2 if x in s1)]
'''
FIX['make-a-square-with-the-same-color'] = '''from typing import List
class Solution:
    def canMakeSquare(self, grid: List[List[str]]) -> bool:
        for i in range(2):
            for j in range(2):
                w = b = 0
                for di in range(2):
                    for dj in range(2):
                        if grid[i + di][j + dj] == 'W':
                            w += 1
                        else:
                            b += 1
                if w >= 3 or b >= 3:
                    return True
        return False
'''
FIX['button-with-longest-push-time'] = '''from typing import List
class Solution:
    def buttonWithLongestTime(self, events: List[List[int]]) -> int:
        best_i = events[0][0]
        best_t = events[0][1]
        for j in range(1, len(events)):
            t = events[j][1] - events[j - 1][1]
            if t > best_t or (t == best_t and events[j][0] < best_i):
                best_t = t
                best_i = events[j][0]
        return best_i
'''
FIX['calculate-digit-sum-of-a-string'] = '''class Solution:
    def digitSum(self, s: str, k: int) -> str:
        while len(s) > k:
            s = ''.join(str(sum(int(c) for c in s[i:i + k])) for i in range(0, len(s), k))
        return s
'''
FIX['check-if-strings-can-be-made-equal-with-operations-i'] = '''class Solution:
    def canBeEqual(self, s1: str, s2: str) -> bool:
        def swp(s, i, j):
            l = list(s)
            l[i], l[j] = l[j], l[i]
            return ''.join(l)
        for a in (s1, swp(s1, 0, 2)):
            for b in (a, swp(a, 1, 3)):
                if b == s2:
                    return True
        return False
'''
b = json.load(open('leftovers.json', encoding='utf-8'))
b.update(FIX)
json.dump(b, open('leftovers.json', 'w', encoding='utf-8'), indent=1)
json.dump(FIX, open('solutions_fix1.json', 'w', encoding='utf-8'), indent=1)
print('fixed:', len(FIX))
