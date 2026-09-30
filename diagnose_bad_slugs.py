"""Diagnose the 5 library slugs that have no cached questionId.

Fetches the public problem catalog once and matches each broken key against
real titles, so we can tell slug typos from genuinely missing problems.
Read-only (uses the authenticated jar, no submissions).
"""
import json
import subprocess

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
r = subprocess.run(['curl.exe', '-s', '--max-time', '30',
                    'https://leetcode.com/api/problems/all/',
                    '-H', 'User-Agent: ' + UA, '-b', 'lc_cookies.txt'],
                   capture_output=True, text=True, encoding='utf-8',
                   errors='replace')
d = json.loads(r.stdout)
print('account:', d.get('user_name'), '| solved:', d.get('num_solved'))

solved = {l.strip() for l in open('solved.txt', encoding='utf-8')
          if l.strip() and not l.startswith(('solved:', '='))}

broken = ['arrange-coins', 'construct-rectangle', 'dominant-index',
          'one-bit-and-2-bit-characters', 'sum-of-squares-of-elements-in-array']

words = {
    'arrange-coins': ['arranging coins'],
    'construct-rectangle': ['construct the rectangle'],
    'dominant-index': ['dominant index', 'largest number at least twice'],
    'one-bit-and-2-bit-characters': ['1-bit and 2-bit'],
    'sum-of-squares-of-elements-in-array': ['sum of squares'],
}

for slug in broken:
    hits = []
    for p in d.get('stat_status_pairs') or []:
        t = p['stat']['question__title'].lower()
        if any(w in t for w in words[slug]):
            hits.append((p['stat']['question__title_slug'], p['stat']['question_id'],
                         'ac' if p['status'] == 'ac' else '-'))
    print('=' * 60)
    print('broken key:', slug)
    for s, qid, st in hits:
        print('   real slug:', s, '| id:', qid, '| status:', st,
              '| in solved.txt:', s in solved)
