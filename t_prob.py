import json, subprocess, sys
from urllib.parse import quote
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
sess = ''
for line in open('lc_cookies.txt', encoding='utf-8'):
    if 'LEETCODE_SESSION' in line:
        sess = line.strip().split()[-1]
with open('lc_cookies2.txt', 'a', encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + sess + '\n')
slug = sys.argv[1]
body = json.dumps({'query': 'query q($t:String!){question(titleSlug:$t){content hints}}', 'variables': {'t': slug}})
r = subprocess.run(['curl.exe', '-s', '--max-time', '25', 'https://leetcode.com/graphql/', '-X', 'POST', '-H', 'Content-Type: application/json', '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com', '-b', 'lc_cookies2.txt', '--data', body], capture_output=True, text=True, encoding='utf-8', errors='replace')
d = json.loads(r.stdout)
q = (d.get('data') or {}).get('question') or {}
import re
c = re.sub('<[^>]+>', ' ', q.get('content') or '')
c = re.sub(r'&nbsp;', ' ', c)
print(c[:2500])
