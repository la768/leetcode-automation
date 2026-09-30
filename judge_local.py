"""Mini-judge: runs authored solutions against the official LeetCode examples.

Reads specs.json (statement metadata + exampleTestcases + Output lines parsed
from `content`) and one or more {slug: code} banks. For each problem it
instantiates the class the driver will use, calls the method the driver will
call, and compares the return value with the statement's expected output.
No submission is created; this is the cheap validation loop.

Usage: python judge_local.py solutions_a1.json [solutions_a2.json ...]
"""
import ast
import html
import json
import re
import sys

specs = json.load(open('specs.json', encoding='utf-8'))
banks = {}
for f in sys.argv[1:] or ['solutions_a1.json']:
    banks.update(json.load(open(f, encoding='utf-8')))
print('judging', len(banks), 'solutions')


def expected_outputs(content):
    c = content or ''
    out = re.findall(r'Output:?\s*</strong>\s*([^<\n]+)', c)
    if len(out) < 2:
        out = re.findall(r'Output:?\s*([^<\n]+)', c)
    return [html.unescape(o).strip() for o in out]


def parse_arg(s):
    """Returns (ok, value)."""
    s = html.unescape(s.strip())
    lit = (s.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
    try:
        return True, ast.literal_eval(lit)
    except Exception:
        return False, None


def parse_examples(ex, nparams):
    lines = [l for l in (ex or '').split('\n')]
    if nparams <= 0:
        return []
    groups = [lines[i:i + nparams] for i in range(0, len(lines), nparams)]
    return [g for g in groups if len(g) == nparams]


def norm(x):
    if isinstance(x, bool):
        return x
    if isinstance(x, float):
        return round(x, 5)
    return x


def parse_expected(s):
    s = s.strip()
    try:
        return ast.literal_eval(s.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
    except Exception:
        return s


passed, failed, skipped = [], [], []
skipped_examples = 0
for slug, code in sorted(banks.items()):
    spec = specs.get(slug)
    if not spec or not spec.get('meta') or not spec.get('content'):
        skipped.append((slug, 'no spec'))
        continue
    meta = json.loads(spec['meta'])
    method = meta.get('name')
    params = [p['name'] for p in meta.get('params') or []]
    examples = parse_examples(spec.get('examples'), len(params))
    outs = expected_outputs(spec.get('content'))
    if not examples or not outs:
        skipped.append((slug, 'no parseable examples (%d in, %d out)' % (len(examples), len(outs))))
        continue
    ns = {}
    try:
        exec(code, ns)
    except Exception as e:
        failed.append((slug, 'exec error: %r' % (e,)))
        continue
    cls = ns.get('Solution')
    if cls is None:
        classes = [ns[n] for n in ns if isinstance(ns[n], type) and n != 'Solution']
        if not classes:
            failed.append((slug, 'no class defined'))
            continue
        cls = classes[0]
    bad = []
    for i, grp in enumerate(examples):
        args, ok = [], True
        for a in grp:
            good, val = parse_arg(a)
            if not good:
                ok = False
                break
            args.append(val)
        if not ok:
            bad.append('ex%d: unparseable args %r' % (i + 1, grp))
            continue
        if i >= len(outs):
            bad.append('ex%d: no expected output' % (i + 1))
            continue
        want = parse_expected(outs[i])
        if outs[i].strip() == '':
            skipped_examples += 1
            continue
        try:
            got = getattr(cls(), method)(*args)
        except Exception as e:
            bad.append('ex%d: raised %r' % (i + 1, e))
            continue
        if got is None and args and isinstance(args[0], (list, str)):
            got = args[0]  # in-place problems (move-zeroes, reverse-string) mutate arg 0
        if norm(got) != norm(want):
            if isinstance(want, list) and isinstance(got, list) and all(
                    isinstance(a, list) for a in want + got):
                if [sorted(x) for x in got] == [sorted(x) for x in want]:
                    continue
            bad.append('ex%d: got %r want %r' % (i + 1, got, want))
    if bad:
        failed.append((slug, '; '.join(bad)))
    else:
        passed.append((slug, len(examples)))

print('\n== PASS (%d) ==' % len(passed))
for s, n in passed:
    print('  %s (%d examples)' % (s, n))
print('\n== FAIL (%d) ==' % len(failed))
for s, why in failed:
    print('  %s : %s' % (s, why))
print('\n== SKIP (%d) ==' % len(skipped))
for s, why in skipped:
    print('  %s (%s)' % (s, why))
