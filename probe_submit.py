"""Check whether the LeetCode /submit/ endpoint is currently accepting posts.

Does one real submit attempt against a banked problem so the answer reflects
the exact same code path the solver uses.
"""
import json
import time

import solver_friend as eng

slug = 'power-of-two'
code = ('class Solution:\n'
        '    def isPowerOfTwo(self, n: int) -> bool:\n'
        '        return n > 0 and (n & (n - 1)) == 0\n')

qid, _ = eng.get_qid(slug)
body = json.dumps({'lang': 'python3', 'question_id': qid, 'typed_code': code})
extra = ['-b', eng.JAR, '-H', 'X-Requested-With: XMLHttpRequest',
         '-H', 'Origin: https://leetcode.com', '-H', 'X-CSRFToken: ' + eng.csrf,
         '-H', 'Referer: https://leetcode.com/problems/' + slug + '/']

status, r = eng.curl_full('https://leetcode.com/problems/' + slug + '/submit/',
                          extra=extra, method='POST', data=body, jar=eng.JAR)
print('status :', status)
print('sid    :', r.get('submission_id'))

if status == 200 and r.get('submission_id'):
    sid = r['submission_id']
    for _ in range(6):
        time.sleep(1.5)
        v = eng.get_verdict_recent(slug)
        if v:
            print('verdict:', v)
            break
    else:
        print('verdict: (timed out waiting for poll)')
