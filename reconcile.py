"""Reconciles the ledger against the live LeetCode profile.

Compares (a) solved.txt snapshot, (b) the 300 accepted-today slugs in the
ledger, and (c) the live /api/problems/all/ status flags, and reports any
slug the ledger believes is accepted but the profile does not count.
Read-only.
"""
import json
import os
import subprocess

LEDGER = os.environ.get('LEDGER_FILE', 'run_friend100.json')

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
r = subprocess.run(['curl.exe', '-s', '--max-time', '30',
                    'https://leetcode.com/api/problems/all/',
                    '-H', 'User-Agent: ' + UA, '-b', 'lc_cookies.txt'],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
d = json.loads(r.stdout)
live_ac = {p['stat']['question__title_slug'] for p in d['stat_status_pairs']
           if p['status'] == 'ac'}
print('account:', d.get('user_name'), '| num_solved (API):', d.get('num_solved'))
print('live ac count:', len(live_ac))

snap = {l.strip() for l in open('solved.txt', encoding='utf-8')
        if l.strip() and not l.startswith(('solved:', '='))}
print('solved.txt snapshot size:', len(snap))

led = json.load(open(LEDGER, encoding='utf-8'))
acc_today = [r['slug'] for r in led['accepted']]
print('accepted today (ledger, distinct):', len(set(acc_today)),
      '| duplicates:', len(acc_today) - len(set(acc_today)))

missing = [s for s in acc_today if s not in live_ac]
print('ledger-accepted but NOT ac in profile:', missing)

extra = [s for s in live_ac if s not in snap and s not in set(acc_today)]
print('ac in profile but in neither snapshot nor ledger:', extra)

print('snapshot + accepted-today =', len(snap | set(acc_today)),
      '| union with live =', len(snap | set(acc_today) | live_ac))
