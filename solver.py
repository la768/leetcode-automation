import json, time, subprocess, sys, os
from urllib.parse import quote

# Session token is read from lc_cookies.txt (see lc_cookies.txt.example).
# NEVER hardcode or commit your LEETCODE_SESSION token - it grants full
# access to the LeetCode account it belongs to.
def _load_session():
    if not os.path.exists('lc_cookies.txt'):
        raise SystemExit('lc_cookies.txt not found - copy lc_cookies.txt.example and paste your own LEETCODE_SESSION (see START-HERE.md section 2)')
    for line in open('lc_cookies.txt', encoding='utf-8'):
        parts = line.split()
        if len(parts) >= 7 and parts[5] == 'LEETCODE_SESSION' and not line.startswith('#'):
            return parts[6]
    raise SystemExit('No LEETCODE_SESSION row in lc_cookies.txt - paste your token there first (see lc_cookies.txt.example)')

SESSION = _load_session()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def curl_json(url, extra=None, method='GET', data=None, cookiejar=None):
    cmd = ['curl.exe', '-s', url, '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com']
    if cookiejar: cmd += ['-b', cookiejar]
    if extra: cmd += extra
    if method == 'POST' and data is not None:
        cmd += ['-X', 'POST', '-H', 'Content-Type: application/json', '--data', data]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        return json.loads(r.stdout)
    except Exception:
        print(f'  RAW RESP: {r.stdout[:200]!r} ERR: {r.stderr[:100]!r}', flush=True)
        return {}

# 1) get csrf token via cookie jar (WITH session cookie so token binds to the session)
subprocess.run(['curl.exe', '-s', 'https://leetcode.com/', '-H', 'User-Agent: ' + UA, '-b', f'LEETCODE_SESSION={SESSION}', '-c', 'lc_cookies.txt'], capture_output=True)
# append session cookie into the jar
with open('lc_cookies.txt', 'a', encoding='utf-8') as f:
    f.write(f'leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t{SESSION}\n')
csrf = ''
for line in open('lc_cookies.txt', encoding='utf-8'):
    if 'csrftoken' in line: csrf = line.strip().split()[-1]
print('csrf obtained:', bool(csrf))

c = f'csrftoken={csrf}; LEETCODE_SESSION={SESSION}'
COMMON = ['-b', 'lc_cookies.txt', '-H', 'X-Requested-With: XMLHttpRequest', '-H', 'Origin: https://leetcode.com']

def get_question_id(slug):
    query = quote(f'query{{question(titleSlug:"{slug}"){{questionId}}}}', safe='')
    q = curl_json(f'https://leetcode.com/graphql/?query={query}', cookiejar=c)
    qd = (q.get('data') or {}).get('question')
    return qd['questionId'] if qd else None

def refresh_csrf():
    global csrf, c
    subprocess.run(['curl.exe', '-s', 'https://leetcode.com/', '-H', 'User-Agent: ' + UA, '-b', f'LEETCODE_SESSION={SESSION}', '-c', 'lc_cookies.txt'], capture_output=True)
    with open('lc_cookies.txt', 'a', encoding='utf-8') as f:
        f.write(f'leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t{SESSION}\n')
    csrf = ''
    for line in open('lc_cookies.txt', encoding='utf-8'):
        if 'csrftoken' in line: csrf = line.strip().split()[-1]
    c = f'csrftoken={csrf}; LEETCODE_SESSION={SESSION}'
    COMMON[2] = '-H'
    # rebuild headers with fresh token handled inside submit
    return csrf

def submit(slug, code):
    global csrf, c
    refresh_csrf()
    qid = get_question_id(slug)
    if not qid:
        print('  premium/unavailable, skipping', flush=True); return 'SKIPPED'
    body = json.dumps({'lang': 'python3', 'question_id': qid, 'typed_code': code})
    r = curl_json(f'https://leetcode.com/problems/{slug}/submit/', extra=COMMON + ['-H', f'X-CSRFToken: {csrf}', '-H', f'Referer: https://leetcode.com/problems/{slug}/'], method='POST', data=body)
    if 'submission_id' not in r:
        # csrf may have rotated -> refresh and retry once
        refresh_csrf()
        r = curl_json(f'https://leetcode.com/problems/{slug}/submit/', extra=COMMON + ['-H', f'X-CSRFToken: {csrf}', '-H', f'Referer: https://leetcode.com/problems/{slug}/'], method='POST', data=body)
    sid = r.get('submission_id')
    if not sid:
        print(f'  submit failed: {r}', flush=True); return None
    for _ in range(8):
        time.sleep(3)
        res = curl_json(f'https://leetcode.com/submissions/detail/{sid}/check/', extra=COMMON)
        st = res.get('state')
        if st == 'FINISHED':
            return res.get('status_msg', 'UNKNOWN')
        time.sleep(3)
    # fallback: check global status
    time.sleep(8)
    ap = curl_json('https://leetcode.com/api/problems/all/', extra=COMMON)
    for p in (ap.get('stat_status_pairs') or []):
        if p['stat']['question__title_slug'] == slug:
            return 'Accepted (slow judge)' if p['status'] == 'ac' else 'PENDING/UNKNOWN'
    return 'TIMEOUT'

SOLUTIONS = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'solutions.json', encoding='utf-8'))

allp = curl_json('https://leetcode.com/api/problems/all/', extra=COMMON)
status = {p['stat']['question__title_slug']: p['status'] for p in (allp.get('stat_status_pairs') or [])}
print(f'START: solved={allp.get("num_solved", "?")}', flush=True)

accepted = 0
only = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != 'x' else None
for i, (slug, code) in enumerate(SOLUTIONS.items()):
    if only and slug != only: continue
    if status.get(slug) == 'ac':
        print(f'[{i+1}] {slug}: already solved, skip', flush=True); continue
    v = submit(slug, code)
    print(f'[{i+1}] {slug}: {v}', flush=True)
    if v == 'Accepted': accepted += 1
    time.sleep(3)

allp2 = curl_json('https://leetcode.com/api/problems/all/', extra=COMMON)
print(f'END: solved={allp2.get("num_solved", "?")} (accepted in this run: {accepted})', flush=True)
