# solver_friend.py — shared submit/verdict/session engine for the friend campaign.
# Imported by solver_friend_main.py; run that file, not this one.
import json, time, subprocess, sys, os
from urllib.parse import quote

ACCOUNT = 'shailaendranms'
BANK_SOURCES = {}

# Set by submit() when a slug exhausts its retries against a Cloudflare 429.
# The driver checks this so a throttled account halts instead of grinding
# through the whole bank one doomed slug at a time.
RATE_LIMITED = {'consecutive': 0, 'total': 0}
RATE_LIMIT_ABORT = 3


def load_bank(path):
    d = json.load(open(path, encoding='utf-8'))
    for slug in d:
        BANK_SOURCES.setdefault(slug, path)
    return d


def read_session():
    for line in open('lc_cookies.txt', encoding='utf-8'):
        if 'LEETCODE_SESSION' in line:
            return line.strip().split('\t')[-1]
    return ''


SESSION = read_session()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def curl_status(url, extra=None, method='GET', data=None, jar=None):
    """Backwards-compatible status-only probe (no body)."""
    return curl_full(url, extra=extra, method=method, data=data, jar=jar)[0]


def curl_full(url, extra=None, method='GET', data=None, jar=None):
    """Single request returning (http_status, parsed_json).

    Uses a '-w' sentinel so the status code and the body come back from ONE
    request. Probing the status separately would mean POSTing the submission
    twice, which risks consuming a second submission slot.
    """
    sentinel = '@@HTTP_STATUS@@'
    cmd = ['curl.exe', '-s', '-w', '\n' + sentinel + '%{http_code}', '--max-time', '25',
           url, '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com']
    if jar:
        cmd += ['-b', jar]
    if extra:
        cmd += extra
    if method == 'POST' and data is not None:
        cmd += ['-X', 'POST', '-H', 'Content-Type: application/json', '--data', data]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = r.stdout
    if sentinel not in out:
        return 0, {}
    body, _, code = out.rpartition(sentinel)
    try:
        return int(code.strip()[:3]), json.loads(body)
    except Exception:
        return int(code.strip()[:3]) if code.strip()[:3].isdigit() else 0, {}


def curl(url, extra=None, method='GET', data=None, jar=None):
    cmd = ['curl.exe', '-s', '--max-time', '25', url, '-H', 'User-Agent: ' + UA, '-H', 'Referer: https://leetcode.com']
    if jar:
        cmd += ['-b', jar]
    if extra:
        cmd += extra
    if method == 'POST' and data is not None:
        cmd += ['-X', 'POST', '-H', 'Content-Type: application/json', '--data', data]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        return json.loads(r.stdout)
    except Exception:
        return {}


JAR = 'lc_cookies2.txt'
subprocess.run(['curl.exe', '-s', 'https://leetcode.com/', '-H', 'User-Agent: ' + UA, '-b', 'lc_cookies.txt', '-c', JAR], capture_output=True)
with open(JAR, 'a', encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + SESSION + '\n')
csrf = ''
for line in open(JAR, encoding='utf-8'):
    if 'csrftoken' in line:
        csrf = line.strip().split()[-1]
print('csrf:', bool(csrf), flush=True)


def refresh_csrf():
    global csrf
    subprocess.run(['curl.exe', '-s', 'https://leetcode.com/', '-H', 'User-Agent: ' + UA, '-b', 'lc_cookies.txt', '-c', JAR], capture_output=True)
    with open(JAR, 'a', encoding='utf-8') as f:
        f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t' + SESSION + '\n')
    csrf = ''
    for line in open(JAR, encoding='utf-8'):
        if 'csrftoken' in line:
            csrf = line.strip().split()[-1]
    return csrf


QIDS = {}
if os.path.exists('qids.json'):
    try:
        QIDS = json.load(open('qids.json', encoding='utf-8'))
    except Exception:
        QIDS = {}


def get_qid(slug):
    if slug in QIDS:
        return QIDS[slug], ''
    q = quote('query{question(titleSlug:"' + slug + '"){questionId questionTitle}}', safe='')
    r = curl('https://leetcode.com/graphql/?query=' + q, jar=JAR)
    qd = (r.get('data') or {}).get('question')
    qid = qd['questionId'] if qd else None
    if qid:
        QIDS[slug] = qid
        json.dump(QIDS, open('qids.json', 'w', encoding='utf-8'))
    return qid, (qd or {}).get('questionTitle', '')


def get_verdict_recent(slug):
    q = quote('query{recentAcSubmissionList(username:"' + ACCOUNT + '",limit:15){titleSlug statusDisplay}}', safe='')
    r = curl('https://leetcode.com/graphql/?query=' + q, jar=JAR)
    lst = ((r.get('data') or {}).get('recentAcSubmissionList')) or []
    for s in lst:
        if s.get('titleSlug') == slug:
            return s.get('statusDisplay')
    return None


def verify_accepted(slug, sid):
    """Guard against false-positive verdicts.

    LeetCode answers restricted submissions with a submission_id whose real
    statusDisplay is "Restrictions Failed" (seen on design-hashmap /
    design-hashset on 2026-09-26), and the recent-list poller can report that
    as Accepted. Ask the account's own submission history what the newest
    submission for this slug really was.
    """
    q = quote('query{questionSubmissionList(questionSlug:"' + slug + '",offset:0,'
              'limit:5){submissions{id statusDisplay}}}', safe='')
    r = curl('https://leetcode.com/graphql/?query=' + q, jar=JAR)
    subs = (((r.get('data') or {}).get('questionSubmissionList') or {})
            .get('submissions') or [])
    if not subs:
        return None
    if sid and str(subs[0].get('id')) != str(sid):
        return None  # history has moved on; trust the poller
    return subs[0].get('statusDisplay')


def _finalize(v, slug, sid, title):
    """Cross-check an Accepted verdict against the account's own history."""
    if v == 'Accepted':
        real = verify_accepted(slug, sid)
        if real and real != 'Accepted':
            print('  !! verdict was %s but history says %r' % (v, real), flush=True)
            return real, sid, title
    return v, sid, title


def submit(slug, code):
    qid, title = get_qid(slug)
    if not qid:
        print('  no qid (premium?), skip', flush=True)
        return 'SKIPPED', None, title
    body = json.dumps({'lang': 'python3', 'question_id': qid, 'typed_code': code})
    r = {}
    sid = None
    rate_limited = False
    for attempt in range(5):
        extra = ['-b', JAR, '-H', 'X-Requested-With: XMLHttpRequest', '-H', 'Origin: https://leetcode.com',
                 '-H', 'X-CSRFToken: ' + csrf, '-H', 'Referer: https://leetcode.com/problems/' + slug + '/']
        status, r = curl_full('https://leetcode.com/problems/' + slug + '/submit/',
                               extra=extra, method='POST', data=body, jar=JAR)
        sid = r.get('submission_id')
        if sid:
            break
        if attempt >= 4:
            break
        if status == 429:
            rate_limited = True
            wait = 90 + attempt * 60
            print('  rate limited (429), sleeping %ds' % wait, flush=True)
            time.sleep(wait)
        elif status == 403:
            # Stale CSRF token - refresh and retry immediately.
            print('  CSRF rejected (403), refreshing token', flush=True)
            refresh_csrf()
            time.sleep(2)
        else:
            time.sleep(5 + attempt * 5)
    if not sid:
        if rate_limited:
            RATE_LIMITED['consecutive'] += 1
            RATE_LIMITED['total'] += 1
            print('  submit blocked: still rate limited after retries '
                  '(consecutive=%d)' % RATE_LIMITED['consecutive'], flush=True)
        else:
            RATE_LIMITED['consecutive'] = 0
            print('  submit failed after retries: ' + str(r)[:150], flush=True)
        return None, None, title
    RATE_LIMITED['consecutive'] = 0
    for _ in range(5):
        time.sleep(1.5)
        v = get_verdict_recent(slug)
        if v:
            return _finalize(v, slug, sid, title)
    for _ in range(14):
        time.sleep(2)
        res = curl('https://leetcode.com/submissions/detail/' + str(sid) + '/check/', jar=JAR)
        sc = res.get('status_code')
        if res.get('state') == 'FINISHED' or sc is not None:
            v = ({10: 'Accepted', 11: 'Wrong Answer', 12: 'Memory Limit Exceeded', 13: 'Output Limit Exceeded',
                  14: 'Time Limit Exceeded', 15: 'Runtime Error', 20: 'Compile Error'}.get(sc, res.get('status_msg', 'UNKNOWN')))
            return _finalize(v, slug, sid, title)
    return 'TIMEOUT', sid, title
