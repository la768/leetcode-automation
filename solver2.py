import json, time, subprocess, sys, os
from urllib.parse import quote

def read_session():
    for line in open('lc_cookies.txt', encoding='utf-8'):
        if 'LEETCODE_SESSION' in line:
            return line.strip().split('\t')[-1]
    return ''

SESSION = read_session()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def curl(url, extra=None, method='GET', data=None, jar=None):
    cmd = ['curl.exe','-s','--max-time','25',url,'-H','User-Agent: '+UA,'-H','Referer: https://leetcode.com']
    if jar: cmd += ['-b',jar]
    if extra: cmd += extra
    if method=='POST' and data is not None:
        cmd += ['-X','POST','-H','Content-Type: application/json','--data',data]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    try: return json.loads(r.stdout)
    except Exception: return {}

JAR = 'lc_cookies2.txt'
# refresh jar once, bind session
subprocess.run(['curl.exe','-s','https://leetcode.com/','-H','User-Agent: '+UA,'-b','lc_cookies.txt','-c',JAR], capture_output=True)
with open(JAR,'a',encoding='utf-8') as f:
    f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t'+SESSION+'\n')
csrf=''
for line in open(JAR, encoding='utf-8'):
    if 'csrftoken' in line: csrf=line.strip().split()[-1]
print('csrf:', bool(csrf), flush=True)

def refresh_csrf():
    global csrf
    subprocess.run(['curl.exe','-s','https://leetcode.com/','-H','User-Agent: '+UA,'-b','lc_cookies.txt','-c',JAR], capture_output=True)
    with open(JAR,'a',encoding='utf-8') as f:
        f.write('leetcode.com\tFALSE\t/\tTRUE\t0\tLEETCODE_SESSION\t'+SESSION+'\n')
    csrf=''
    for line in open(JAR, encoding='utf-8'):
        if 'csrftoken' in line: csrf=line.strip().split()[-1]
    return csrf

QIDS={}
if os.path.exists('qids.json'):
    try: QIDS=json.load(open('qids.json',encoding='utf-8'))
    except: QIDS={}

def get_qid(slug):
    if slug in QIDS: return QIDS[slug]
    q=quote('query{question(titleSlug:"'+slug+'"){questionId}}', safe='')
    r=curl('https://leetcode.com/graphql/?query='+q, jar=JAR)
    qd=(r.get('data') or {}).get('question')
    qid=qd['questionId'] if qd else None
    if qid:
        QIDS[slug]=qid
        json.dump(QIDS,open('qids.json','w',encoding='utf-8'))
    return qid

def get_verdict_recent(slug):
    q=quote('query{recentAcSubmissionList(username:"lavcha",limit:15){titleSlug statusDisplay}}', safe='')
    r=curl('https://leetcode.com/graphql/?query='+q, jar=JAR)
    lst=((r.get('data') or {}).get('recentAcSubmissionList')) or []
    for s in lst:
        if s.get('titleSlug')==slug:
            return s.get('statusDisplay')
    return None

def submit(slug, code):
    qid=get_qid(slug)
    if not qid:
        print('  no qid (premium?), skip', flush=True); return 'SKIPPED'
    body=json.dumps({'lang':'python3','question_id':qid,'typed_code':code})
    # retry loop for empty/rate-limited responses
    r={}; sid=None
    for attempt in range(4):
        extra=['-b',JAR,'-H','X-Requested-With: XMLHttpRequest','-H','Origin: https://leetcode.com','-H','X-CSRFToken: '+csrf,'-H','Referer: https://leetcode.com/problems/'+slug+'/']
        r=curl('https://leetcode.com/problems/'+slug+'/submit/', extra=extra, method='POST', data=body, jar=JAR)
        sid=r.get('submission_id')
        if sid: break
        if attempt < 3:
            time.sleep(3 + attempt*3)
    if not sid:
        print('  submit failed after retries: '+str(r)[:150], flush=True); return None
    # poll via recent list, lightweight (fast path for Accepted)
    for _ in range(5):
        time.sleep(1.5)
        v=get_verdict_recent(slug)
        if v: return v
    # then definitive check endpoint (catches Wrong Answer / Runtime Error too)
    for _ in range(14):
        time.sleep(2)
        res=curl('https://leetcode.com/submissions/detail/'+str(sid)+'/check/', jar=JAR)
        sc=res.get('status_code')
        if res.get('state')=='FINISHED' or sc is not None:
            return {10:'Accepted',11:'Wrong Answer',12:'Memory Limit Exceeded',13:'Output Limit Exceeded',14:'Time Limit Exceeded',15:'Runtime Error',20:'Compile Error'}.get(sc, res.get('status_msg','UNKNOWN'))
    return 'TIMEOUT'

SOL=json.load(open(sys.argv[2] if len(sys.argv)>2 else 'solutions_all.json', encoding='utf-8'))
# Golden rule: read the local solved ledger, do NOT re-query the catalog for skip logic
SOLVED=set()
if os.path.exists('solved.txt'):
    for line in open('solved.txt', encoding='utf-8'):
        line=line.strip()
        if line and not line.startswith(('LEETCODE','Generated','Total','=')):
            SOLVED.add(line)
allp=curl('https://leetcode.com/api/problems/all/', jar=JAR)
status={p['stat']['question__title_slug']:p['status'] for p in (allp.get('stat_status_pairs') or [])}
print('START solved:', allp.get('num_solved','?'), '| ledger size:', len(SOLVED), flush=True)

accept=0
cap=int(sys.argv[3]) if len(sys.argv)>3 else 50
only=sys.argv[1] if len(sys.argv)>1 and sys.argv[1]!='x' else None
for i,(slug,code) in enumerate(SOL.items()):
    if only and slug!=only: continue
    if accept>=cap: print('reached cap', cap, flush=True); break
    if slug in SOLVED or status.get(slug)=='ac':
        print(f'[{i+1}] {slug}: already solved skip', flush=True); continue
    v=submit(slug, code)
    print(f'[{i+1}] {slug}: {v}', flush=True)
    if v=='Accepted': accept+=1
    time.sleep(1.5)
allp2=curl('https://leetcode.com/api/problems/all/', jar=JAR)
print('END solved:', allp2.get('num_solved','?'), 'accepted this run:', accept, flush=True)