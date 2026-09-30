import json, subprocess, sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
SRC = sys.argv[1] if len(sys.argv) > 1 else 'lc_cookies.txt'
JAR = 'lc_cookies_probe.txt'

subprocess.run(['curl.exe', '-s', '--max-time', '30', 'https://leetcode.com/',
                '-H', 'User-Agent: ' + UA, '-b', SRC, '-c', JAR], capture_output=True)

tok = ''
for line in open(SRC, encoding='utf-8', errors='replace'):
    if 'LEETCODE_SESSION' in line:
        tok = line.strip().split('\t')[-1]

with open(JAR, 'a', encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + tok + '\n')


def get(url):
    r = subprocess.run(['curl.exe', '-s', '--max-time', '30', url,
                        '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com',
                        '-b', JAR], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout


print('cookie file   :', SRC)
print('token length  :', len(tok))
out = get('https://leetcode.com/api/problems/all/')
try:
    d = json.loads(out)
except Exception:
    print('NOT JSON (Cloudflare or network?). Head:', out[:120])
    sys.exit(1)

print('user_name     :', repr(d.get('user_name')))
print('num_solved    :', d.get('num_solved'))
print('ac easy/med/hard:', d.get('ac_easy'), d.get('ac_medium'), d.get('ac_hard'))
if d.get('num_solved'):
    print('RESULT: LOGIN OK - the cookie works, safe to run solver2.py')
else:
    print('RESULT: NOT AUTHENTICATED')
    print('  1. The cookie is expired or was invalidated (logging in again rotates it).')
    print('  2. You may have copied the eyJ... JWT instead of the opaque LEETCODE_SESSION')
    print('     cookie. Run "node get_cookie.js" to extract the correct cookie, or')
    print('     check DevTools -> Application -> Cookies for the LEETCODE_SESSION row.')
    print('  3. Re-copy LEETCODE_SESSION from a browser where you are logged in, then')
    print('     re-run this script BEFORE opening leetcode.com again in that browser.')