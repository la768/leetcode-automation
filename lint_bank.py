"""Static lint for a {slug: code} bank, run BEFORE submitting.

ERRORS (these always cost a submission):
  - syntax errors (a stray/missing paren -> LeetCode "Runtime Error")
  - `class Solution` missing AND no other class defined at all

INFO (usually fine, listed for review):
  - a design-style problem (class name != Solution: NumArray, StockSpanner, ...)
    -- correct as long as the name matches the problem's metaData.name
  - bare typing names (List/Dict/...) without an import: LeetCode's python3
    prelude does `from typing import *`, so this is normally harmless (100+
    entries like this were Accepted in the 240 campaign); we add the explicit
    import only when a slug actually Runtime-Errors.

Usage: python lint_bank.py friend_bank240.json [more banks ...]
Exit code 1 if any ERROR is found. Read-only.
"""
import glob
import json
import re
import sys

TYPING_NAMES = re.compile(r'\b(List|Dict|Tuple|Optional|Set)\[')
CLASS_DEF = re.compile(r'^\s*class\s+(\w+)', re.M)


def typing_imports(code):
    return (('from typing import' in code) or ('import typing' in code)
            or ('List =' in code))


def main(banks):
    errors = 0
    infos = 0
    total = 0
    for bank in banks:
        code = json.load(open(bank, encoding='utf-8'))
        for slug, src in code.items():
            total += 1
            problems = []
            try:
                compile(src, slug, 'exec')
            except SyntaxError as exc:
                problems.append('SYNTAX: %s (line %s)' % (exc.msg, exc.lineno))
            classes = CLASS_DEF.findall(src)
            if not classes:
                problems.append('no class defined at all')
            if problems:
                errors += 1
                print('[ERROR] %-55s %s' % (slug, '; '.join(problems)))
            elif 'Solution' not in classes:
                infos += 1
                print('[info ] %-55s design class %s' % (slug, classes))
            elif TYPING_NAMES.search(src) and not typing_imports(src):
                infos += 1
    print('linted %d entries across %d bank(s) | errors: %d | info-only: %d'
          % (total, len(banks), errors, infos))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or ['friend_bank240.json']))
