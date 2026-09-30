"""Read the account's own submission history for two suspicious slugs."""
from urllib.parse import quote

import solver_friend as eng

for slug in ['design-hashmap', 'design-hashset', 'maximum-average-subarray-i']:
    q = quote('query{questionSubmissionList(questionSlug:"%s",offset:0,limit:5)'
              '{submissions{id statusDisplay lang timestamp}}}' % slug, safe='')
    r = eng.curl('https://leetcode.com/graphql/?query=' + q, jar=eng.JAR)
    subs = (((r.get('data') or {}).get('questionSubmissionList') or {})
            .get('submissions') or [])
    print('=' * 60)
    print(slug)
    for s in subs:
        print('   id:', s.get('id'), '|', s.get('statusDisplay'), '|', s.get('lang'),
              '| ts:', s.get('timestamp'))
    if not subs:
        print('   (no submissions)', str(r)[:200])
