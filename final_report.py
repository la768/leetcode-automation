"""Prints the final state of a campaign ledger (default: run_friend100.json).

Usage: python final_report.py            -> 300-campaign ledger
       $env:LEDGER_FILE='run_friend240.json'; python final_report.py
Read-only.
"""
import json
import os
import time

LEDGER = os.environ.get('LEDGER_FILE', 'run_friend100.json')
led = json.load(open(LEDGER, encoding='utf-8'))
acc = led['accepted']
rej = led['rejected']

print('ledger           :', LEDGER)
print('start_solved     :', led['start_solved'], '| target:', led['target'])
print('accepted         :', len({r['slug'] for r in acc}), '| rejected:', len(rej))
print('profile should be:', led['start_solved'] + len({r['slug'] for r in acc}))

if acc:
    ts = [r['ts'] for r in acc]
    print('first accepted   :', min(ts), '| last:', max(ts))
    gaps = []
    secs = [time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')) for t in ts]
    for i in range(1, len(secs)):
        d = secs[i] - secs[i - 1]
        if d < 600:            # ignore restarts / overnight breaks
            gaps.append(d)
    if gaps:
        gaps.sort()
        print('per-accept median: %.1fs (n=%d)' % (gaps[len(gaps) // 2], len(gaps)))

banks = {}
for r in acc:
    banks[r.get('source_bank', '?')] = banks.get(r.get('source_bank', '?'), 0) + 1
print('accepted by bank :', banks)

print('--- still not accepted ---')
for r in rej:
    print('  ', r['ts'], r['slug'], '|', r['verdict'], '| sid', r['sid'])
