"""Screens candidate slugs for python3 support and harvests driver snippets.

LeetCode's catalog contains SQL and "30 Days of JavaScript" problems that are
not answerable in python3, so a bank must be screened before it is submitted:
one GraphQL request per BATCH slugs (aliases), asking for the supported
codeSnippets. Result -> screened.json {slug: {qid, front, title, difficulty,
paid, langs, py3}}. No submission is created.

Usage: python screen.py            # screens candidates_new.json (easy) + library pool
       python screen.py <file.json>  # screens the keys of a {slug: code} bank
"""
import json
import sys
import time
from urllib.parse import quote

import solver_friend as eng

BATCH = 15
OUT = 'screened.json'


def screen(slugs):
    results = {}
    for i in range(0, len(slugs), BATCH):
        chunk = slugs[i:i + BATCH]
        parts = ['q%d:question(titleSlug:"%s"){questionId questionFrontendId title '
                 'difficulty isPaidOnly codeSnippets{langSlug code}}' % (j, s)
                 for j, s in enumerate(chunk)]
        q = quote('query{' + ' '.join(parts) + '}', safe='')
        r = eng.curl('https://leetcode.com/graphql/?query=' + q, jar=eng.JAR)
        data = (r.get('data') or {})
        for j, s in enumerate(chunk):
            qd = data.get('q%d' % j)
            if not qd:
                results[s] = {'qid': None}
                continue
            langs = [cs.get('langSlug') for cs in (qd.get('codeSnippets') or [])]
            py3 = next((cs.get('code') for cs in (qd.get('codeSnippets') or [])
                        if cs.get('langSlug') == 'python3'), None)
            results[s] = {'qid': qd.get('questionId'), 'front': qd.get('questionFrontendId'),
                          'title': qd.get('title'), 'difficulty': qd.get('difficulty'),
                          'paid': qd.get('isPaidOnly'), 'langs': langs, 'py3': py3}
        print('  screened %d/%d' % (min(i + BATCH, len(slugs)), len(slugs)), flush=True)
        time.sleep(0.4)
    return results


if __name__ == '__main__':
    if len(sys.argv) > 1:
        bank = json.load(open(sys.argv[1], encoding='utf-8'))
        pool = sorted(bank)
    else:
        cand = json.load(open('candidates_new.json', encoding='utf-8'))
        merged = json.load(open('library_merged.json', encoding='utf-8'))
        uns = {l.strip() for l in open('unsolved_easy.txt', encoding='utf-8') if l.strip()}
        uns |= {l.strip() for l in open('unsolved_medium.txt', encoding='utf-8') if l.strip()}
        easy_no_code = [s for s, d in cand.items() if d == 'Easy']
        lib_ready = sorted(k for k in merged if k in uns)
        pool = lib_ready + easy_no_code

    old = {}
    try:
        old = json.load(open(OUT, encoding='utf-8'))
    except Exception:
        pass
    todo = [s for s in pool if s not in old or not old[s].get('langs')]
    print('pool:', len(pool), '| already screened:', len(pool) - len(todo), '| to do:', len(todo))
    res = screen(todo)
    old.update(res)
    json.dump(old, open(OUT, 'w', encoding='utf-8'), indent=1)

    ok = [s for s in pool if (old.get(s) or {}).get('py3')]
    nolang = [s for s in pool if (old.get(s) or {}).get('langs') and not (old.get(s) or {}).get('py3')]
    missing = [s for s in pool if not (old.get(s) or {}).get('langs')]
    print('python3-capable:', len(ok), '| no-python3:', len(nolang), '| no-snippet/unknown slug:', len(missing))
    print('unknown slugs:', missing[:20])
    print('no-python3 sample:', nolang[:20])
