import json
BANK = {}
BANK['find-the-k-th-character-in-string-game-i'] = '''class Solution:
    def kthCharacter(self, k: int) -> str:
        word = 'a'
        while len(word) < k:
            nxt = ''.join(chr((ord(c) - 97 + 1) % 26 + 97) for c in word)
            word += nxt
        return word[k - 1]
'''
BANK['the-two-sneaky-numbers-of-digitville'] = '''from typing import List
from collections import Counter
class Solution:
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        c = Counter(nums)
        return [x for x, v in c.items() if v >= 2][:2]
'''
BANK['find-the-key-of-the-numbers'] = '''class Solution:
    def generateKey(self, num1: int, num2: int, num3: int) -> int:
        a, b, c = str(num1).zfill(4), str(num2).zfill(4), str(num3).zfill(4)
        return int(''.join(str(min(a[i], b[i], c[i])) for i in range(4)))
'''
BANK['convert-date-to-binary'] = '''class Solution:
    def convertDateToBinary(self, date: str) -> str:
        y, m, d = date.split('-')
        return '-'.join(bin(int(x))[2:] for x in (y, m, d))
'''
BANK['snake-in-matrix'] = '''from typing import List
class Solution:
    def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
        r = c = 0
        for cmd in commands:
            if cmd == 'UP': r -= 1
            elif cmd == 'DOWN': r += 1
            elif cmd == 'LEFT': c -= 1
            else: c += 1
        return r * n + c
'''
BANK['number-of-bit-changes-to-make-two-integers-equal'] = '''class Solution:
    def minChanges(self, n: int, k: int) -> int:
        if n | k != n: return -1
        return bin(n & ~k).count('1')
'''
BANK['lexicographically-smallest-string-after-a-swap'] = '''class Solution:
    def smallestString(self, s: str) -> str:
        for i in range(len(s) - 1):
            if (ord(s[i]) - 48) % 2 == (ord(s[i + 1]) - 48) % 2:
                return s[:i] + s[i + 1] + s[i] + s[i + 2:]
        return s
'''
BANK['minimum-average-of-smallest-and-largest-elements'] = '''from typing import List
class Solution:
    def minimumAverage(self, nums: List[int]) -> float:
        nums.sort()
        vals = [(nums[i] + nums[len(nums) - 1 - i]) / 2 for i in range(len(nums) // 2)]
        return min(vals)
'''
BANK['maximum-height-of-a-triangle'] = '''class Solution:
    def maxHeightOfTriangle(self, red: int, blue: int) -> int:
        def sim(a, b):
            h = 0
            row = 1
            while True:
                if row % 2 == 1:
                    if a >= row:
                        a -= row
                    else:
                        break
                else:
                    if b >= row:
                        b -= row
                    else:
                        break
                h += 1
                row += 1
            return h
        return max(sim(red, blue), sim(blue, red))
'''
BANK['find-the-encrypted-string'] = '''class Solution:
    def getEncryptedString(self, s: str, k: int) -> str:
        n = len(s)
        return ''.join(s[(i + k) % n] for i in range(n))
'''
json.dump(BANK, open('solutions_gen1c.json', 'w', encoding='utf-8'), indent=1)
print('gen1c:', len(BANK))
