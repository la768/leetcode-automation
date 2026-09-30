"""Re-asserts ledger invariants:
  - no slug appears twice in `accepted`
  - no slug appears twice in `rejected` (keep the newest row)
  - no slug is in both lists (accepted wins)
  - rows are sorted by timestamp
Idempotent; run after any manual ledger surgery.
"""
import json
import os

LEDGER = os.environ.get('LEDGER_FILE', 'run_friend100.json')
doc = json.load(open(LEDGER, encoding='utf-8'))

seen, acc = set(), []
for row in doc['accepted']:
    if row['slug'] not in seen:
        seen.add(row['slug'])
        acc.append(row)
acc.sort(key=lambda r: r.get('ts', ''))

rej_seen, rej = set(), []
for row in reversed(doc['rejected']):
    if row['slug'] in seen or row['slug'] in rej_seen:
        continue
    rej_seen.add(row['slug'])
    rej.append(row)
rej.sort(key=lambda r: r.get('ts', ''))

doc['accepted'], doc['rejected'] = acc, rej
json.dump(doc, open(LEDGER, 'w', encoding='utf-8'), indent=1)
print('accepted:', len(acc), '| rejected:', len(rej), '| target:', doc['target'])
print('rejected slugs:', sorted(rej_seen))
