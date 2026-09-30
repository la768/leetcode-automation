import solver_friend as eng
import run_ledger
import json, time, sys, os

DAILY_TARGET = int(os.environ.get('DAILY_TARGET', '100'))
BANK = sys.argv[2] if len(sys.argv) > 2 else 'friend_candidates.json'
BANK_SOURCES = {}
SOL = eng.load_bank(BANK)
for slug in SOL:
    BANK_SOURCES.setdefault(slug, BANK)

gate = eng.curl('https://leetcode.com/api/problems/all/', jar=eng.JAR)
if gate.get('user_name') != eng.ACCOUNT:
    print('ABORT: active account is', repr(gate.get('user_name')), 'expected', repr(eng.ACCOUNT), flush=True)
    sys.exit(2)
print('ACTIVE ACCOUNT:', eng.ACCOUNT, '| solved:', gate.get('num_solved', '?'), flush=True)

SOLVED = set()
if os.path.exists('solved.txt'):
    for line in open('solved.txt', encoding='utf-8'):
        line = line.strip()
        if line and not line.startswith(('LEETCODE', 'Generated', 'Total', '=', 'solved', 'unsolved')):
            SOLVED.add(line)
status = {p['stat']['question__title_slug']: p['status'] for p in (gate.get('stat_status_pairs') or [])}
print('START solved:', gate.get('num_solved', '?'), '| ledger size:', len(SOLVED), flush=True)

doc = run_ledger.load()
accept = run_ledger.count(doc)
done_today = {r.get('slug') for r in doc['accepted']}
print('already accepted today:', accept, '/', DAILY_TARGET, flush=True)
only = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != 'x' else None
for i, (slug, code) in enumerate(SOL.items()):
    if accept >= DAILY_TARGET:
        print('reached daily target', DAILY_TARGET, flush=True)
        break
    if only and slug != only:
        continue
    if slug in done_today:
        print(f'[{i+1}] {slug}: accepted earlier today, skip', flush=True)
        continue
    if slug in SOLVED or status.get(slug) == 'ac':
        print(f'[{i+1}] {slug}: already solved skip', flush=True)
        continue
    v, sid, title = eng.submit(slug, code)
    print(f'[{i+1}] {slug}: {v}', flush=True)
    if eng.RATE_LIMITED['consecutive'] >= eng.RATE_LIMIT_ABORT:
        print('ABORT: %d consecutive rate-limited submits; account is throttled.'
              % eng.RATE_LIMITED['consecutive'], flush=True)
        print('       Stopping now to avoid burning the whole bank. '
              'Resume after the limit clears.', flush=True)
        break
    entry = {'slug': slug, 'title': title, 'qid': eng.QIDS.get(slug, ''),
             'source_bank': BANK_SOURCES.get(slug, BANK),
             'verdict': v, 'sid': sid}
    if v == 'Accepted':
        doc = run_ledger.record(entry, True)
        accept = run_ledger.count(doc)
        print(f'  -> accepted today: {accept}/{DAILY_TARGET}', flush=True)
    else:
        run_ledger.record(entry, False)
    time.sleep(1.5)
print('END accepted today:', accept, '/', DAILY_TARGET, flush=True)
