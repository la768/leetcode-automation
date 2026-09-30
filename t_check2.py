import json, subprocess, sys
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
sess = ''
for line in open('lc_cookies.txt', encoding='utf-8'):
    if 'LEETCODE_SESSION' in line:
        sess = line.strip().split()[-1]
with open('lc_cookies2.txt', 'a', encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + sess + '\n')
r = subprocess.run(['curl.exe', '-s', '--max-time', '25', 'https://leetcode.com/submissions/detail/' + sys.argv[1] + '/check/', '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com', '-b', 'lc_cookies2.txt'], capture_output=True, text=True, encoding='utf-8', errors='replace')
j = json.loads(r.stdout)
for k in ('status_code', 'status_msg', 'total_correct', 'total_testcases', 'pretty_lang', 'question_id'):
    print(k, ':', j.get(k))
print('compare:', str(j.get('compare_result'))[:100])
