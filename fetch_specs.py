"""Fetches full specs for authoring: statement content, driver metadata and the
official example test cases. Read-only (no submissions).

Usage: python fetch_specs.py authored_slugs.json   -> specs.json
"""
import json
import sys
import time
from urllib.parse import quote

import solver_friend as eng

BATCH = 8
OUT = 'specs.json'
slugs = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'authored_slugs.json',
                       encoding='utf-8'))

try:
    specs = json.load(open(OUT, encoding='utf-8'))
except Exception:
    specs = {}

todo = [s for s in slugs if s not in specs]
print('slugs:', len(slugs), '| to fetch:', len(todo))
for i in range(0, len(todo), BATCH):
    chunk = todo[i:i + BATCH]
    parts = ['q%d:question(titleSlug:"%s"){questionId questionFrontendId title difficulty '
             'metaData exampleTestcases content '
             'codeSnippets{langSlug code}}' % (j, s) for j, s in enumerate(chunk)]
    q = quote('query{' + ' '.join(parts) + '}', safe='')
    r = eng.curl('https://leetcode.com/graphql/?query=' + q, jar=eng.JAR)
    data = (r.get('data') or {})
    for j, s in enumerate(chunk):
        qd = data.get('q%d' % j)
        if not qd:
            print('  !! no data for', s)
            continue
        py3 = next((cs.get('code') for cs in (qd.get('codeSnippets') or [])
                    if cs.get('langSlug') == 'python3'), None)
        specs[s] = {'qid': qd.get('questionId'), 'front': qd.get('questionFrontendId'),
                    'title': qd.get('title'), 'difficulty': qd.get('difficulty'),
                    'meta': qd.get('metaData'), 'examples': qd.get('exampleTestcases'),
                    'content': qd.get('content'), 'py3': py3}
    json.dump(specs, open(OUT, 'w', encoding='utf-8'), indent=1)
    print('  %d/%d saved' % (min(i + BATCH, len(todo)), len(todo)), flush=True)
    time.sleep(0.4)
print('specs.json entries:', len(specs))
