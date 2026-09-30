import json
BANK = {}
BANK['minimum-moves-to-convert-string'] = '''class Solution:
    def minimumMoves(self, s: str) -> int:
        i = 0
        moves = 0
        while i < len(s):
            if s[i] == 'X':
                moves += 1
                i += 3
            else:
                i += 1
        return moves
'''
BANK['maximum-difference-between-increasing-elements'] = '''from typing import List
class Solution:
    def maximumDifference(self, nums: List[int]) -> int:
        best = -1
        m = nums[0]
        for x in nums[1:]:
            if x > m:
                best = max(best, x - m)
            m = min(m, x)
        return best
'''
BANK['reverse-prefix-of-word'] = '''class Solution:
    def reversePrefix(self, word: str, ch: str) -> str:
        i = word.find(ch)
        if i < 0: return word
        return word[:i + 1][::-1] + word[i + 1:]
'''
BANK['find-the-middle-index-in-array'] = '''from typing import List
class Solution:
    def findMiddleIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        left = 0
        for i, x in enumerate(nums):
            if left == total - left - x:
                return i
            left += x
        return -1
'''
BANK['minimum-time-to-type-word-using-special-typewriter'] = '''class Solution:
    def minTimeToType(self, word: str) -> int:
        cur = 'a'
        t = 0
        for c in word:
            d = abs(ord(c) - ord(cur))
            t += min(d, 26 - d) + 1
            cur = c
        return t
'''
BANK['maximum-odd-binary-number'] = '''class Solution:
    def maximumOddBinaryNumber(self, s: str) -> str:
        ones = s.count('1')
        return '1' * (ones - 1) + '0' * (len(s) - ones) + '1'
'''
BANK['count-distinct-numbers-on-board'] = '''class Solution:
    def distinctIntegers(self, n: int) -> int:
        return max(1, n - 1)
'''
BANK['apply-operations-to-an-array'] = '''from typing import List
class Solution:
    def applyOperations(self, nums: List[int]) -> List[int]:
        for i in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                nums[i] *= 2
                nums[i + 1] = 0
        out = [x for x in nums if x != 0]
        return out + [0] * (len(nums) - len(out))
'''
BANK['number-of-senior-citizens'] = '''from typing import List
class Solution:
    def countSeniors(self, details: List[str]) -> int:
        return sum(1 for d in details if int(d[11:13]) > 60)
'''
BANK['count-the-digits-that-divide-a-number'] = '''class Solution:
    def countDigits(self, num: int) -> int:
        return sum(1 for c in str(num) if num % int(c) == 0)
'''
BANK['separate-the-digits-in-an-array'] = '''from typing import List
class Solution:
    def separateDigits(self, nums: List[int]) -> List[int]:
        out = []
        for x in nums:
            out.extend(int(c) for c in str(x))
        return out
'''
BANK['find-the-array-concatenation-value'] = '''from typing import List
class Solution:
    def findTheArrayConcVal(self, nums: List[int]) -> int:
        i, j = 0, len(nums) - 1
        total = 0
        while i < j:
            total += int(str(nums[i]) + str(nums[j]))
            i += 1
            j -= 1
        if i == j:
            total += nums[i]
        return total
'''
BANK['sum-of-squares-of-elements-in-array'] = '''from typing import List
class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        n = len(nums)
        return sum(nums[i] * nums[i] for i in range(n) if n % (i + 1) == 0)
'''
BANK['check-if-matrix-is-x-matrix'] = '''from typing import List
class Solution:
    def checkXMatrix(self, grid: List[List[int]]) -> bool:
        n = len(grid)
        for i in range(n):
            for j in range(n):
                diag = (i == j) or (i + j == n - 1)
                if diag and grid[i][j] == 0:
                    return False
                if not diag and grid[i][j] != 0:
                    return False
        return True
'''
BANK['capitalize-the-title'] = '''class Solution:
    def capitalizeTitle(self, title: str) -> str:
        out = []
        for w in title.split():
            if len(w) <= 2:
                out.append(w.lower())
            else:
                out.append(w[0].upper() + w[1:].lower())
        return ' '.join(out)
'''
BANK['determine-if-string-halves-are-alike'] = '''class Solution:
    def halvesAreAlike(self, s: str) -> bool:
        v = set('aeiouAEIOU')
        n = len(s) // 2
        a = sum(1 for c in s[:n] if c in v)
        b = sum(1 for c in s[n:] if c in v)
        return a == b
'''
BANK['count-items-matching-a-rule'] = '''from typing import List
class Solution:
    def countMatches(self, items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
        idx = {'type': 0, 'color': 1, 'name': 2}[ruleKey]
        return sum(1 for it in items if it[idx] == ruleValue)
'''
BANK['destination-city'] = '''from typing import List
class Solution:
    def destCity(self, paths: List[List[str]]) -> str:
        starts = set(a for a, b in paths)
        for a, b in paths:
            if b not in starts:
                return b
        return ''
'''
json.dump(BANK, open('solutions_gen1j.json', 'w', encoding='utf-8'), indent=1)
print('gen1j:', len(BANK))
