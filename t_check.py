import json, subprocess, sys
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
sid = sys.argv[1]
sess = ''
for line in open('lc_cookies.txt', encoding='utf-8'):
    if 'LEETCODE_SESSION' in line:
        sess = line.strip().split()[-1]
with open('lc_cookies2.txt', 'a', encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + sess + '\n')
r = subprocess.run(['curl.exe', '-s', '--max-time', '25', 'https://leetcode.com/submissions/detail/' + sid + '/check/', '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com', '-b', 'lc_cookies2.txt'], capture_output=True, text=True, encoding='utf-8', errors='replace')
try:
    j = json.loads(r.stdout)
    print('code:', j.get('status_code'), j.get('status_msg'))
    print('runtime_error:', str(j.get('runtime_error'))[:300])
    print('compile_error:', str(j.get('compile_error'))[:300])
    print('task_fail:', str(j.get('task_fail_message'))[:300])
except Exception:
    print(r.stdout[:300])
