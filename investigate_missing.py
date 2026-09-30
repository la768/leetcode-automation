"""Why are design-hashmap / design-hashset accepted in the ledger but not
counted by the profile?  Read-only investigation."""
import json
import subprocess

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

led = json.load(open('run_friend100.json', encoding='utf-8'))
target = {'design-hashmap', 'design-hashset'}
for r in led['accepted']:
    if r['slug'] in target:
        print('LEDGER ROW:', json.dumps(r))

r = subprocess.run(['curl.exe', '-s', '--max-time', '30',
                    'https://leetcode.com/api/problems/all/',
                    '-H', 'User-Agent: ' + UA, '-b', 'lc_cookies.txt'],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
d = json.loads(r.stdout)
for p in d['stat_status_pairs']:
    sl = p['stat']['question__title_slug']
    if sl in target:
        print('CATALOG:', sl, '| id:', p['stat']['question_id'],
              '| status:', p['status'], '| paid:', p.get('paid_only'),
              '| locked:', p.get('stat', {}).get('is_new'))

# what does the current check endpoint say for those submission ids?
for r in led['accepted']:
    if r['slug'] in target and r.get('sid'):
        rr = subprocess.run(['curl.exe', '-s', '--max-time', '25',
                            'https://leetcode.com/submissions/detail/%s/check/' % r['sid'],
                             '-H', 'User-Agent: ' + UA,
                             '-H', 'Referer: https://leetcode.com',
                             '-b', 'lc_cookies.txt'],
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
        print('CHECK', r['slug'], r['sid'], '->', rr.stdout[:200])
