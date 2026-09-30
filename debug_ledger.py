import json

led = json.load(open('run_friend100.json', encoding='utf-8'))
probe = {'add-to-array-form-of-integer', 'button-with-longest-push-time',
         'calculate-digit-sum-of-a-string',
         'check-if-strings-can-be-made-equal-with-operations-i',
         'consecutive-characters'}
print('--- accepted rows for the 5 re-checked slugs ---')
for r in led['accepted']:
    if r['slug'] in probe:
        print(' ', r['slug'], '|', r['ts'], '| sid:', r['sid'],
              '| bank:', r.get('source_bank'))
print('--- rejected rows for the same ---')
for r in led['rejected']:
    if r['slug'] in probe:
        print(' ', r['slug'], '|', r['ts'], '| sid:', r['sid'],
              '| bank:', r.get('source_bank'))
print('accepted total:', len(led['accepted']), '| target:', led['target'])
print('first accepted ts:', led['accepted'][0]['ts'], '| last:', led['accepted'][-1]['ts'])
