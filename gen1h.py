import json
BANK = {}
BANK['minimum-hours-of-training-to-win-a-competition'] = '''from typing import List
class Solution:
    def minNumberOfHours(self, initialEnergy: int, initialExperience: int, energy: List[int], experience: List[int]) -> int:
        hours = 0
        if sum(energy) >= initialEnergy:
            hours += sum(energy) + 1 - initialEnergy
        exp = initialExperience
        for e in experience:
            if exp <= e:
                hours += e - exp + 1
                exp = e + 1
            exp += e
        return hours
'''
BANK['largest-local-values-in-a-matrix'] = '''from typing import List
class Solution:
    def largestLocal(self, grid: List[List[int]]) -> List[List[int]]:
        n = len(grid)
        out = [[0] * (n - 2) for _ in range(n - 2)]
        for r in range(n - 2):
            for c in range(n - 2):
                out[r][c] = max(grid[i][j] for i in range(r, r + 3) for j in range(c, c + 3))
        return out
'''
BANK['merge-similar-items'] = '''from typing import List
class Solution:
    def mergeSimilarItems(self, items1: List[List[int]], items2: List[List[int]]) -> List[List[int]]:
        from collections import defaultdict
        w = defaultdict(int)
        for v, wt in items1: w[v] += wt
        for v, wt in items2: w[v] += wt
        return sorted(w.items())
'''
BANK['number-of-arithmetic-triplets'] = '''from typing import List
class Solution:
    def arithmeticTriplets(self, nums: List[int], diff: int) -> int:
        s = set(nums)
        return sum(1 for x in nums if x + diff in s and x + 2 * diff in s)
'''
BANK['make-array-zero-by-subtracting-equal-amounts'] = '''from typing import List
class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        return len(set(x for x in nums if x > 0))
'''
BANK['first-letter-to-appear-twice'] = '''class Solution:
    def repeatedCharacter(self, s: str) -> str:
        seen = set()
        for c in s:
            if c in seen: return c
            seen.add(c)
        return ''
'''
BANK['maximum-number-of-pairs-in-array'] = '''from typing import List
from collections import Counter
class Solution:
    def numberOfPairs(self, nums: List[int]) -> List[int]:
        c = Counter(nums)
        pairs = sum(v // 2 for v in c.values())
        leftover = sum(v % 2 for v in c.values())
        return [pairs, leftover]
'''
BANK['minimum-amount-of-time-to-fill-cups'] = '''from typing import List
class Solution:
    def fillCups(self, amount: List[int]) -> int:
        import math
        return max(max(amount), math.ceil(sum(amount) / 2))
'''
BANK['strong-password-checker-ii'] = '''class Solution:
    def strongPasswordCheckerII(self, password: str) -> bool:
        if len(password) < 8: return False
        if not any(c.islower() for c in password): return False
        if not any(c.isupper() for c in password): return False
        if not any(c.isdigit() for c in password): return False
        if not any(not c.isalnum() for c in password): return False
        return all(a != b for a, b in zip(password, password[1:]))
'''
BANK['root-equals-sum-of-children'] = '''from typing import Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def checkTree(self, root: Optional[TreeNode]) -> bool:
        return root.val == root.left.val + root.right.val
'''
BANK['percentage-of-letter-in-string'] = '''class Solution:
    def percentageLetter(self, s: str, letter: str) -> int:
        return s.count(letter) * 100 // len(s)
'''
BANK['largest-3-same-digit-number-in-string'] = '''class Solution:
    def largestGoodInteger(self, num: str) -> str:
        best = ''
        for i in range(len(num) - 2):
            if num[i] == num[i + 1] == num[i + 2]:
                if not best or num[i:i + 3] > best:
                    best = num[i:i + 3]
        return best
'''
BANK['minimum-number-of-operations-to-convert-time'] = '''class Solution:
    def convertTime(self, current: str, correct: str) -> int:
        h1, m1 = map(int, current.split(':'))
        h2, m2 = map(int, correct.split(':'))
        d = (h2 * 60 + m2) - (h1 * 60 + m1)
        ops = 0
        for step in (60, 15, 5, 1):
            ops += d // step
            d %= step
        return ops
'''
BANK['intersection-of-multiple-arrays'] = '''from typing import List
class Solution:
    def intersection(self, nums: List[List[int]]) -> List[int]:
        from collections import Counter
        c = Counter(nums[0])
        for arr in nums[1:]:
            c = Counter({k: v for k, v in c.items() if k in arr})
        return sorted(c)
'''
BANK['largest-number-after-digit-swaps-by-parity'] = '''class Solution:
    def largestInteger(self, num: int) -> int:
        s = str(num)
        odd = sorted([c for c in s if (ord(c) - 48) % 2 == 1], reverse=True)
        even = sorted([c for c in s if (ord(c) - 48) % 2 == 0], reverse=True)
        io = ie = 0
        out = []
        for c in s:
            if (ord(c) - 48) % 2 == 1:
                out.append(odd[io]); io += 1
            else:
                out.append(even[ie]); ie += 1
        return int(''.join(out))
'''
BANK['minimum-sum-of-four-digit-number-after-splitting-digits'] = '''class Solution:
    def minimumSum(self, num: int) -> int:
        d = sorted(str(num))
        return int(d[0] + d[2]) + int(d[1] + d[3])
'''
BANK['minimum-bit-flips-to-convert-number'] = '''class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        return bin(start ^ goal).count('1')
'''
json.dump(BANK, open('solutions_gen1h.json', 'w', encoding='utf-8'), indent=1)
print('gen1h:', len(BANK))
