import json, subprocess, sys, time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
SLUG = sys.argv[1]
BANK = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'friend_bank200.json', encoding='utf-8'))
code = BANK[SLUG]
qids = json.load(open('qids.json', encoding='utf-8'))
qid = qids.get(SLUG)

sess = ''
for line in open('lc_cookies.txt', encoding='utf-8'):
    if 'LEETCODE_SESSION' in line:
        sess = line.strip().split('\t')[-1]
with open('lc_cookies2.txt', 'a', encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + sess + '\n')
csrf = ''
for line in open('lc_cookies2.txt', encoding='utf-8'):
    if 'csrftoken' in line:
        csrf = line.strip().split()[-1]

body = json.dumps({'lang': 'python3', 'question_id': qid, 'typed_code': code})
r = subprocess.run(['curl.exe', '-s', '--max-time', '30',
                    'https://leetcode.com/problems/' + SLUG + '/submit/', '-X', 'POST',
                    '-H', 'User-Agent: ' + UA, '-H', 'X-Requested-With: XMLHttpRequest',
                    '-H', 'Origin: https://leetcode.com', '-H', 'X-CSRFToken: ' + csrf,
                    '-H', 'Referer: https://leetcode.com/problems/' + SLUG + '/',
                    '-b', 'lc_cookies2.txt', '--data', body],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
try:
    sid = json.loads(r.stdout).get('submission_id')
except Exception:
    print('SUBMIT FAILED:', r.stdout[:200]); sys.exit(1)
print('sid:', sid)
time.sleep(6)
r2 = subprocess.run(['curl.exe', '-s', '--max-time', '25',
                     'https://leetcode.com/submissions/detail/' + str(sid) + '/check/',
                     '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com',
                     '-b', 'lc_cookies2.txt'],
                    capture_output=True, text=True, encoding='utf-8', errors='replace')
j = json.loads(r2.stdout)
print('code:', j.get('status_code'), j.get('status_msg'))
print('correct/total:', j.get('total_correct'), '/', j.get('total_testcases'))
print('runtime_error:', str(j.get('runtime_error'))[:300])
print('last_testcase:', str(j.get('last_testcase'))[:200])
print('expected:', str(j.get('expected_output'))[:200])
print('code_output:', str(j.get('code_output'))[:200])
