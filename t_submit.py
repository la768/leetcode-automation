import json, subprocess, time, sys
from urllib.parse import quote
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
SLUG = sys.argv[1] if len(sys.argv) > 1 else 'two-out-of-three'
BANK = json.load(open('solutions_gen1.json', encoding='utf-8'))
code = BANK[SLUG]
qids = json.load(open('qids.json', encoding='utf-8'))
qid = qids.get(SLUG)
print('qid:', qid)
# refresh jar + csrf
subprocess.run(['curl.exe', '-s', 'https://leetcode.com/', '-H', 'User-Agent: ' + UA, '-b', 'lc_cookies.txt', '-c', 'lc_cookies2.txt'], capture_output=True)
sess = ''
for line in open('lc_cookies.txt', encoding='utf-8'):
    if 'LEETCODE_SESSION' in line:
        sess = line.strip().split()[-1]
with open('lc_cookies2.txt', 'a', encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + sess + '\n')
csrf = ''
for line in open('lc_cookies2.txt', encoding='utf-8'):
    if 'csrftoken' in line:
        csrf = line.strip().split()[-1]
print('csrf ok:', bool(csrf))
body = json.dumps({'lang': 'python3', 'question_id': qid, 'typed_code': code})
r = subprocess.run(['curl.exe', '-s', '--max-time', '30', 'https://leetcode.com/problems/' + SLUG + '/submit/', '-X', 'POST', '-H', 'User-Agent: ' + UA, '-H', 'X-Requested-With: XMLHttpRequest', '-H', 'Origin: https://leetcode.com', '-H', 'X-CSRFToken: ' + csrf, '-H', 'Referer: https://leetcode.com/problems/' + SLUG + '/', '-b', 'lc_cookies2.txt', '--data', body], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('SUBMIT RAW:', r.stdout[:300])
try:
    sid = json.loads(r.stdout).get('submission_id')
except Exception:
    sid = None
print('sid:', sid)
for _ in range(8):
    time.sleep(2)
    if not sid: break
    r2 = subprocess.run(['curl.exe', '-s', '--max-time', '25', 'https://leetcode.com/submissions/detail/' + str(sid) + '/check/', '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com', '-b', 'lc_cookies2.txt'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = r2.stdout[:400]
    try:
        j = json.loads(r2.stdout)
        print('CHECK:', j.get('status_code'), j.get('status_msg'), '| runtime:', j.get('status_runtime'))
        print('task_fail:', str(j.get('task_fail_message'))[:200])
        print('compile:', str(j.get('compile_error'))[:200])
        print('runtime:', str(j.get('runtime_error'))[:200])
    except Exception:
        print('CHECK RAW:', out)
    if 'FINISHED' in out: break
