"""Poll the submit endpoint until LeetCode stops returning 429, then launch
the top-up run automatically.

Usage:
    python watch_and_run.py <bank> <logfile> [poll_seconds] [max_minutes]
"""
import json
import os
import subprocess
import sys
import time

import solver_friend as eng

PROBE_SLUG = 'power-of-two'
PROBE_CODE = ('class Solution:\n'
              '    def isPowerOfTwo(self, n: int) -> bool:\n'
              '        return n > 0 and (n & (n - 1)) == 0\n')

bank = sys.argv[1] if len(sys.argv) > 1 else 'friend_bank_unsolved.json'
logfile = sys.argv[2] if len(sys.argv) > 2 else 'friend240_topup.log'
poll = int(sys.argv[3]) if len(sys.argv) > 3 else 120
max_minutes = int(sys.argv[4]) if len(sys.argv) > 4 else 180

deadline = time.time() + max_minutes * 60
qid, _ = eng.get_qid(PROBE_SLUG)


def probe():
    """Return the HTTP status of a real submit attempt for the probe slug."""
    body = json.dumps({'lang': 'python3', 'question_id': qid, 'typed_code': PROBE_CODE})
    extra = ['-b', eng.JAR, '-H', 'X-Requested-With: XMLHttpRequest',
             '-H', 'Origin: https://leetcode.com', '-H', 'X-CSRFToken: ' + eng.csrf,
             '-H', 'Referer: https://leetcode.com/problems/' + PROBE_SLUG + '/']
    return eng.curl_full('https://leetcode.com/problems/' + PROBE_SLUG + '/submit/',
                         extra=extra, method='POST', data=body, jar=eng.JAR)


def wait_for_verdict(slug):
    for _ in range(8):
        time.sleep(1.5)
        v = eng.get_verdict_recent(slug)
        if v:
            return v
    return 'TIMEOUT'


print('watching for the rate limit to clear (every %ds, max %d min)'
      % (poll, max_minutes), flush=True)

while time.time() < deadline:
    status, r = probe()
    print('%s status=%s' % (time.strftime('%H:%M:%S'), status), flush=True)

    if status == 200 and r.get('submission_id'):
        print('limit cleared; probe verdict: %s' % wait_for_verdict(PROBE_SLUG), flush=True)
        break

    if status == 403:
        print('CSRF rejected, refreshing token', flush=True)
        eng.refresh_csrf()

    time.sleep(poll)
else:
    print('gave up waiting after %d minutes' % max_minutes, flush=True)
    sys.exit(1)

print('launching solver on %s -> %s' % (bank, logfile), flush=True)
env = dict(os.environ)
env['DAILY_TARGET'] = '240'
env.setdefault('LEDGER_FILE', 'run_friend240.json')

with open(logfile, 'a', encoding='utf-8') as out:
    rc = subprocess.call(
        [sys.executable, 'solver_friend_main.py', 'x', bank],
        stdout=out, stderr=subprocess.STDOUT, env=env)

print('solver exited with code %s' % rc, flush=True)
