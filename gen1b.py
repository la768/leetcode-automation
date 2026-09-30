import json
BANK = {}
BANK['zigzag-grid-traversal-with-skip'] = '''from typing import List
class Solution:
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
        res = []
        take = True
        for r, row in enumerate(grid):
            cols = row if r % 2 == 0 else row[::-1]
            for v in cols:
                if take: res.append(v)
                take = not take
        return res
'''
BANK['minimum-operations-to-make-columns-strictly-increasing'] = '''from typing import List
class Solution:
    def minimumOperations(self, grid: List[List[int]]) -> int:
        ops = 0
        for c in range(len(grid[0])):
            for r in range(1, len(grid)):
                need = grid[r - 1][c] + 1
                if grid[r][c] < need:
                    ops += need - grid[r][c]
                    grid[r][c] = need
        return ops
'''
BANK['substring-matching-pattern'] = '''class Solution:
    def hasMatch(self, s: str, p: str) -> bool:
        pre, _, suf = p.partition('*')
        i = s.find(pre)
        if i < 0: return False
        return s.find(suf, i + len(pre)) >= 0
'''
BANK['smallest-number-with-all-set-bits'] = '''class Solution:
    def smallestNumber(self, n: int) -> int:
        b = 1
        while (1 << b) - 1 < n:
            b += 1
        return (1 << b) - 1
'''
BANK['minimum-number-of-operations-to-make-elements-in-array-distinct'] = '''from typing import List
class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        ops = 0
        i = 0
        while i < len(nums):
            if len(set(nums[i:])) == len(nums[i:]):
                break
            i += 3
            ops += 1
        return ops
'''
BANK['minimum-operations-to-make-array-values-equal-to-k'] = '''from typing import List
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return len(set(x for x in nums if x > k))
'''
BANK['find-the-original-typed-string-i'] = '''class Solution:
    def possibleStringCount(self, word: str) -> int:
        total = 1
        run = 1
        for i in range(1, len(word)):
            if word[i] == word[i - 1]:
                run += 1
            else:
                total += run - 1
                run = 1
        total += run - 1
        return total
'''
BANK['adjacent-increasing-subarrays-detection-i'] = '''from typing import List
class Solution:
    def hasIncreasingSubarrays(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        def inc(a, b):
            return all(nums[i] < nums[i + 1] for i in range(a, b))
        for a in range(0, n - 2 * k + 1):
            if inc(a, a + k - 1) and inc(a + k, a + 2 * k - 1):
                return True
        return False
'''
BANK['minimum-element-after-replacement-with-digit-sum'] = '''from typing import List
class Solution:
    def minElement(self, nums: List[int]) -> int:
        def ds(x):
            return sum(int(c) for c in str(x))
        return min(ds(x) for x in nums)
'''
BANK['check-balanced-string'] = '''class Solution:
    def isBalanced(self, num: str) -> bool:
        a = sum(int(c) for c in num[0::2])
        b = sum(int(c) for c in num[1::2])
        return a == b
'''
json.dump(BANK, open('solutions_gen1b.json', 'w', encoding='utf-8'), indent=1)
print('gen1b:', len(BANK))
