"""Corrects the ledger after a false-positive verdict was discovered.

design-hashmap / design-hashset were recorded as Accepted, but LeetCode's own
submission history shows  statusDisplay == "Restrictions Failed"  for both
submission ids, and the profile does not count them. Move those rows from
`accepted` to `rejected` so the ledger matches reality. Idempotent.
"""
import json

LEDGER = 'run_friend100.json'
BAD = {'design-hashmap': 2153395980, 'design-hashset': 2153396093}

doc = json.load(open(LEDGER, encoding='utf-8'))
keep, moved = [], []
for row in doc['accepted']:
    if row['slug'] in BAD and row.get('sid') == BAD[row['slug']]:
        row = dict(row)
        row['verdict'] = 'Restrictions Failed'
        row['accepted_today'] = False
        row['note'] = ('LeetCode rejected the submission as '
                       '"Restrictions Failed"; the verdict poller had '
                       'mis-reported Accepted. Not counted by the profile.')
        moved.append(row)
    else:
        keep.append(row)

if moved:
    doc['accepted'] = keep
    have = {r['slug'] for r in doc['rejected']}
    for row in moved:
        if row['slug'] not in have:
            doc['rejected'].append(row)
    json.dump(doc, open(LEDGER, 'w', encoding='utf-8'), indent=1)

print('moved to rejected:', len(moved), [r['slug'] for r in moved])
print('accepted now:', len(doc['accepted']), '| rejected now:', len(doc['rejected']))
