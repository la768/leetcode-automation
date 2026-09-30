"""Rebuilds solutions_a11.json robustly (avoids hand-editing JSON escapes)."""
import json

S = {}

S['remove-digit-from-number-to-maximize-result'] = '''class Solution:
    def removeDigit(self, number: str, digit: str) -> str:
        best = ''
        for i, c in enumerate(number):
            if c == digit:
                cand = number[:i] + number[i + 1:]
                if cand > best:
                    best = cand
        return best'''

S['remove-one-element-to-make-the-array-strictly-increasing'] = '''class Solution:
    def canBeIncreasing(self, nums: list[int]) -> bool:
        n = len(nums)
        for skip in range(n):
            prev = None
            ok = True
            for i in range(n):
                if i == skip:
                    continue
                if prev is not None and nums[i] <= prev:
                    ok = False
                    break
                prev = nums[i]
            if ok:
                return True
        return False'''

S['replace-all-s-to-avoid-consecutive-repeating-characters'] = '''class Solution:
    def modifyString(self, s: str) -> str:
        a = list(s)
        for i in range(len(a)):
            if a[i] == '?':
                for x in 'abc':
                    if (i == 0 or a[i - 1] != x) and (i + 1 == len(a) or a[i + 1] != x):
                        a[i] = x
                        break
        return ''.join(a)'''

S['second-largest-digit-in-a-string'] = '''class Solution:
    def secondHighest(self, s: str) -> int:
        ds = sorted({int(c) for c in s if c.isdigit()})
        return ds[-2] if len(ds) >= 2 else -1'''

S['special-array-with-x-elements-greater-than-or-equal-x'] = '''class Solution:
    def specialArray(self, nums: list[int]) -> int:
        n = len(nums)
        for x in range(1, n + 1):
            cnt = 0
            for v in nums:
                if v >= x:
                    cnt += 1
            if cnt == x:
                return x
        return -1'''

S['string-matching-in-an-array'] = '''class Solution:
    def stringMatching(self, words: list[str]) -> list[str]:
        out = []
        for i, w in enumerate(words):
            for j, o in enumerate(words):
                if i != j and w in o:
                    out.append(w)
                    break
        return out'''

S['surface-area-of-3d-shapes'] = '''class Solution:
    def surfaceArea(self, grid: list[list[int]]) -> int:
        n = len(grid)
        area = 0
        for i in range(n):
            for j in range(n):
                if grid[i][j]:
                    area += 2 + 4 * grid[i][j]
                    if i:
                        area -= 2 * min(grid[i][j], grid[i - 1][j])
                    if j:
                        area -= 2 * min(grid[i][j], grid[i][j - 1])
        return area'''

S['number-of-valid-words-in-a-sentence'] = '''class Solution:
    def countValidWords(self, sentence: str) -> int:
        cnt = 0
        for w in sentence.split():
            ok = True
            hyphen = 0
            for i, c in enumerate(w):
                if c.isdigit():
                    ok = False
                    break
                if c == '-':
                    hyphen += 1
                    if hyphen > 1 or i == 0 or i == len(w) - 1:
                        ok = False
                        break
                    if not (w[i - 1].islower() and w[i + 1].islower()):
                        ok = False
                        break
                elif c in '!.,':
                    if i != len(w) - 1:
                        ok = False
                        break
                elif not c.islower():
                    ok = False
                    break
            if ok:
                cnt += 1
        return cnt'''

S['reformat-date'] = '''class Solution:
    def reformatDate(self, date: str) -> str:
        parts = date.split()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        day = parts[0][:-2]
        m = months.index(parts[1]) + 1
        return parts[2] + '-' + str(m).zfill(2) + '-' + day.zfill(2)'''

S['reformat-phone-number'] = '''class Solution:
    def reformatNumber(self, number: str) -> str:
        d = [c for c in number if c.isdigit()]
        out = []
        while len(d) > 4:
            out.append(''.join(d[:3]))
            d = d[3:]
        if len(d) == 4:
            out.append(''.join(d[:2]))
            out.append(''.join(d[2:]))
        else:
            out.append(''.join(d))
        return '-'.join(out)'''

S['reformat-the-string'] = '''class Solution:
    def reformat(self, s: str) -> str:
        letters = [c for c in s if c.isalpha()]
        digits = [c for c in s if c.isdigit()]
        if abs(len(letters) - len(digits)) > 1:
            return ''
        if len(letters) < len(digits):
            letters, digits = digits, letters
        out = []
        for i in range(len(digits)):
            out.append(letters[i])
            out.append(digits[i])
        if len(letters) > len(digits):
            out.append(letters[-1])
        return ''.join(out)'''

json.dump(S, open('solutions_a11.json', 'w', encoding='utf-8'), indent=1)
print('wrote solutions_a11.json with', len(S), 'entries')
