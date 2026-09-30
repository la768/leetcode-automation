"""Prints banked solution code for slugs. Usage: python show_code.py <bank> <slug> [<slug> ...]"""
import json
import sys

bank = sys.argv[1]
slugs = sys.argv[2:]
code = json.load(open(bank, encoding='utf-8'))
for s in slugs:
    print('=' * 12, s, '=' * 12)
    print(code.get(s, '<<not in bank>>'))
