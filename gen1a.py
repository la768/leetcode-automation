import json
BANK = {}
BANK['find-closest-person'] = '''from typing import List
class Solution:
    def findClosestPerson(self, x: int, y: int, z: int) -> int:
        dx = abs(x - z); dy = abs(y - z)
        if dx < dy: return 1
        if dy < dx: return 2
        return 0
'''
BANK['restore-finishing-order'] = '''from typing import List
class Solution:
    def recoverOrder(self, order: List[int], friends: List[int]) -> List[int]:
        fs = set(friends)
        return [x for x in order if x in fs]
'''
BANK['reverse-degree-of-a-string'] = '''class Solution:
    def reverseDegree(self, s: str) -> int:
        total = 0
        for i, c in enumerate(s):
            total += (26 - (ord(c) - 97)) * (i + 1)
        return total
'''
BANK['unique-3-digit-even-numbers'] = '''from typing import List
class Solution:
    def totalNumbers(self, digits: List[int]) -> int:
        res = set()
        n = len(digits)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if len({i, j, k}) < 3: continue
                    if digits[i] == 0: continue
                    if digits[k] % 2: continue
                    res.add(digits[i] * 100 + digits[j] * 10 + digits[k])
        return len(res)
'''
BANK['fruits-into-baskets-ii'] = '''from typing import List
class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        used = [False] * len(baskets)
        unplaced = 0
        for f in fruits:
            ok = False
            for i, b in enumerate(baskets):
                if not used[i] and b >= f:
                    used[i] = True
                    ok = True
                    break
            if not ok: unplaced += 1
        return unplaced
'''
BANK['maximum-unique-subarray-sum-after-deletion'] = '''from typing import List
class Solution:
    def maxSum(self, nums: List[int]) -> int:
        pos = set(x for x in nums if x > 0)
        if pos: return sum(pos)
        return max(nums)
'''
BANK['transform-array-by-parity'] = '''from typing import List
class Solution:
    def transformArray(self, nums: List[int]) -> List[int]:
        return sorted(1 if x % 2 else 0 for x in nums)
'''
BANK['maximum-difference-between-even-and-odd-frequency-i'] = '''from collections import Counter
class Solution:
    def maxDifference(self, s: str) -> int:
        c = Counter(s)
        odds = [v for v in c.values() if v % 2]
        evens = [v for v in c.values() if v % 2 == 0]
        return max(odds) - min(evens)
'''
BANK['find-valid-pair-of-adjacent-digits-in-string'] = '''from collections import Counter
class Solution:
    def findValidPair(self, s: str) -> str:
        c = Counter(s)
        for i in range(len(s) - 1):
            a, b = s[i], s[i + 1]
            if a != b and c[a] == int(a) and c[b] == int(b):
                return s[i:i + 2]
        return ''
'''
BANK['sum-of-variable-length-subarrays'] = '''from typing import List
class Solution:
    def subarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        total = 0
        for i in range(n):
            start = max(0, i - nums[i])
            total += sum(nums[start:i + 1])
        return total
'''
json.dump(BANK, open('solutions_gen1a.json', 'w', encoding='utf-8'), indent=1)
print('gen1a:', len(BANK))
