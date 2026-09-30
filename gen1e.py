import json
BANK = {}
BANK['maximum-length-substring-with-two-occurrences'] = '''from collections import Counter
class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        best = 0
        for i in range(len(s)):
            c = Counter()
            for j in range(i, len(s)):
                c[s[j]] += 1
                if c[s[j]] > 2: break
                best = max(best, j - i + 1)
        return best
'''
BANK['modify-the-matrix'] = '''from typing import List
class Solution:
    def modifiedMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        rows, cols = len(matrix), len(matrix[0])
        colmax = [max(matrix[r][c] for r in range(rows)) for c in range(cols)]
        out = [[colmax[c] if matrix[r][c] == -1 else matrix[r][c] for c in range(cols)] for r in range(rows)]
        return out
'''
BANK['split-the-array'] = '''from typing import List
from collections import Counter
class Solution:
    def isPossibleToSplit(self, nums: List[int]) -> bool:
        return max(Counter(nums).values()) <= 2
'''
BANK['maximum-number-of-operations-with-the-same-score-i'] = '''from typing import List
class Solution:
    def maxOperations(self, nums: List[int]) -> int:
        if len(nums) < 2: return 0
        score = nums[0] + nums[1]
        ops = 0
        while len(nums) >= 2 and nums[0] + nums[1] == score:
            nums = nums[2:]
            ops += 1
        return ops
'''
BANK['smallest-missing-integer-greater-than-sequential-prefix-sum'] = '''from typing import List
class Solution:
    def missingInteger(self, nums: List[int]) -> int:
        total = nums[0]
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] + 1:
                total += nums[i]
            else:
                break
        s = set(nums)
        while total in s:
            total += 1
        return total
'''
BANK['matrix-similarity-after-cyclic-shifts'] = '''from typing import List
class Solution:
    def areSimilar(self, mat: List[List[int]], k: int) -> bool:
        n = len(mat[0])
        k %= n
        if k == 0: return True
        for r, row in enumerate(mat):
            if r % 2 == 0:
                shifted = row[k:] + row[:k]
            else:
                shifted = row[-k:] + row[:-k]
            if shifted != row:
                return False
        return True
'''
BANK['make-three-strings-equal'] = '''class Solution:
    def minimumMoves(self, s1: str, s2: str, s3: str) -> int:
        p = 0
        while p < len(s1) and p < len(s2) and p < len(s3) and s1[p] == s2[p] == s3[p]:
            p += 1
        if p == 0: return -1
        return (len(s1) - p) + (len(s2) - p) + (len(s3) - p)
'''
BANK['find-words-containing-character'] = '''from typing import List
class Solution:
    def findWordsContaining(self, words: List[str], x: str) -> List[int]:
        return [i for i, w in enumerate(words) if x in w]
'''
BANK['maximum-strong-pair-xor-i'] = '''from typing import List
class Solution:
    def maxStrongPairXor(self, nums: List[int]) -> int:
        best = 0
        for x in nums:
            for y in nums:
                if abs(x - y) <= min(x, y):
                    best = max(best, x ^ y)
        return best
'''
BANK['minimum-sum-of-mountain-triplets-i'] = '''from typing import List
class Solution:
    def minimumSum(self, nums: List[int]) -> int:
        n = len(nums)
        pref = [float('inf')] * n
        suf = [float('inf')] * n
        m = nums[0]
        for i in range(1, n):
            pref[i] = m
            m = min(m, nums[i])
        m = nums[-1]
        for i in range(n - 2, -1, -1):
            suf[i] = m
            m = min(m, nums[i])
        best = float('inf')
        for j in range(1, n - 1):
            if nums[j] > pref[j] and nums[j] > suf[j]:
                best = min(best, pref[j] + nums[j] + suf[j])
        return best if best != float('inf') else -1
'''
json.dump(BANK, open('solutions_gen1e.json', 'w', encoding='utf-8'), indent=1)
print('gen1e:', len(BANK))
