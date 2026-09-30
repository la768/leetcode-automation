"""Read-only: fetch the official python3 driver signature for given slugs.

Uses the public GraphQL questions endpoint with the logged-in jar (no
submission is created). Prints sectionTitle, questionId, and the python3
codeSnippet so we can spot driver/method-name mismatches.
"""
import json
import sys
from urllib.parse import quote

import solver_friend as eng

slugs = sys.argv[1:] or ['add-to-array-form-of-integer',
                         'button-with-longest-push-time',
                         'calculate-digit-sum-of-a-string',
                         'check-if-strings-can-be-made-equal-with-operations-i',
                         'consecutive-characters',
                         'count-pairs-that-form-a-complete-day-i',
                         'determine-color-of-a-chessboard-square',
                         'arrange-coins',
                         'construct-rectangle']

for slug in slugs:
    q = quote('query{question(titleSlug:"%s"){questionId questionFrontendId title '
              'difficulty isPaidOnly codeSnippets{langSlug code}}}' % slug, safe='')
    r = eng.curl('https://leetcode.com/graphql/?query=' + q, jar=eng.JAR)
    qd = (r.get('data') or {}).get('question') or {}
    print('=' * 70)
    print(slug, '| id:', qd.get('questionId'), '| front:', qd.get('questionFrontendId'),
          '|', qd.get('title'), '|', qd.get('difficulty'), '| paid:', qd.get('isPaidOnly'))
    for cs in qd.get('codeSnippets') or []:
        if cs.get('langSlug') == 'python3':
            print(cs.get('code'))
