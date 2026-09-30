"""Read-only diagnosis of rejected rows: re-polls each stored submission id.

Uses /submissions/detail/<sid>/check/ (no new submissions are created).
Prints the judgement reason plus the failing testcase for each rejected slug.
"""
import json
import subprocess
import sys

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

doc = json.load(open('run_friend100.json', encoding='utf-8'))
only = sys.argv[1] if len(sys.argv) > 1 else None

want = ['add-to-array-form-of-integer',
        'button-with-longest-push-time',
        'calculate-digit-sum-of-a-string',
        'check-if-strings-can-be-made-equal-with-operations-i',
        'consecutive-characters',
        'count-pairs-that-form-a-complete-day-i',
        'determine-color-of-a-chessboard-square']

for row in doc['rejected']:
    slug = row['slug']
    if only and slug != only:
        continue
    if not only and slug not in want:
        continue
    sid = row.get('sid')
    print('=' * 70)
    print(slug, '|', row.get('verdict'), '| sid:', sid)
    if not sid:
        print('  (no submission id recorded)')
        continue
    r = subprocess.run(['curl.exe', '-s', '--max-time', '25',
                        'https://leetcode.com/submissions/detail/%s/check/' % sid,
                        '-H', 'User-Agent: ' + UA,
                        '-H', 'Referer: https://leetcode.com',
                        '-b', 'lc_cookies.txt'],
                       capture_output=True, text=True, encoding='utf-8',
                       errors='replace')
    try:
        j = json.loads(r.stdout)
    except Exception:
        print('  check failed:', r.stdout[:150])
        continue
    print('  status_code:', j.get('status_code'), '|', j.get('status_msg'))
    print('  cases passed:', j.get('total_correct'), '/', j.get('total_testcases'))
    if j.get('runtime_error'):
        print('  runtime_error:', str(j['runtime_error'])[:400])
    if j.get('compile_error'):
        print('  compile_error:', str(j['compile_error'])[:400])
    if j.get('full_runtime_error'):
        print('  full_runtime_error:', str(j['full_runtime_error'])[:200])
    if j.get('last_testcase') is not None:
        print('  last_testcase:', str(j.get('last_testcase'))[:300])
    if j.get('expected_output') is not None:
        print('  expected     :', str(j.get('expected_output'))[:300])
    if j.get('code_output') is not None:
        print('  got          :', str(j.get('code_output'))[:300])
