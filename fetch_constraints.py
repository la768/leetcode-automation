import re
from urllib.parse import quote

import solver_friend as eng

for slug in ['calculate-digit-sum-of-a-string', 'button-with-longest-push-time',
             'check-if-strings-can-be-made-equal-with-operations-i']:
    q = quote('query{question(titleSlug:"%s"){content}}' % slug, safe='')
    r = eng.curl('https://leetcode.com/graphql/?query=' + q, jar=eng.JAR)
    c = ((r.get('data') or {}).get('question') or {}).get('content', '')
    txt = re.sub('<[^>]+>', ' ', c)
    txt = txt.replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
    print('=' * 70)
    print(slug)
    print(txt[-900:])
