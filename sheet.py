"""Prints a compact authoring sheet: slug | method signature | example I/O.

Signature comes from the official python3 snippet (so the driver will find the
method), examples come from `exampleTestcases` + the statement's Output lines.
"""
import json
import re
import sys

specs = json.load(open('specs.json', encoding='utf-8'))
slugs = sys.argv[1:] or sorted(specs)


def sig(py3):
    if not py3:
        return '(no python3 snippet)'
    lines = [l.strip() for l in py3.split('\n') if l.strip()]
    return ' | '.join(l for l in lines if l.startswith(('class ', 'def ')))


def outputs(content):
    c = content or ''
    out = re.findall(r'Output:?\s*</strong>\s*([^<\n]+)', c)
    if not out:
        out = re.findall(r'Output:?\s*([^<\n]+)', c)
    return [o.strip() for o in out]


for slug in slugs:
    s = specs.get(slug) or {}
    ex = (s.get('examples') or '').split('\n')
    outs = outputs(s.get('content'))
    print('# ' + slug + '  [' + str(s.get('front')) + ' ' + str(s.get('difficulty')) + '] ' + (s.get('title') or ''))
    print('  SIG : ' + sig(s.get('py3')))
    print('  META: ' + (s.get('meta') or '')[:150])
    for i, e in enumerate(ex[:3]):
        print('  IN  : ' + e)
        print('  OUT : ' + (outs[i] if i < len(outs) else '?'))
