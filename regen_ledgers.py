import json, subprocess, sys, time

UA = 'Mozilla/5.0'
JAR = sys.argv[1] if len(sys.argv) > 1 else 'lc_cookies.txt'

r = subprocess.run(['curl.exe', '-s', '--max-time', '35', 'https://leetcode.com/api/problems/all/',
                    '-H', 'User-Agent: ' + UA, '-b', JAR],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
try:
    dec = json.JSONDecoder()
    d, _ = dec.raw_decode(r.stdout[r.stdout.find('{'):])
except Exception:
    print('FAILED: response was not JSON (Cloudflare or network). Head:', r.stdout[:150])
    sys.exit(1)

if not d.get('num_solved'):
    print('FAILED: not authenticated (num_solved=0). Refresh lc_cookies.txt first.')
    sys.exit(1)

pairs = d.get('stat_status_pairs') or []
stamp = time.strftime('%Y-%m-%d %H:%M')
solved = sorted(p['stat']['question__title_slug'] for p in pairs if p.get('status') == 'ac')
solved_set = set(solved)

with open('solved.txt', 'w', encoding='utf-8') as f:
    f.write('solved: ' + str(len(solved)) + ' | updated: ' + stamp + '\n' + '\n'.join(solved) + '\n')

easy = [p['stat']['question__title_slug'] for p in pairs if p['difficulty']['level'] == 1]
medium = [p['stat']['question__title_slug'] for p in pairs if p['difficulty']['level'] == 2]
uns_easy = sorted(s for s in easy if s not in solved_set)
uns_med = sorted(s for s in medium if s not in solved_set)

with open('unsolved.txt', 'w', encoding='utf-8') as f:
    f.write('unsolved: easy=' + str(len(uns_easy)) + ' | updated: ' + stamp + '\n' + '\n'.join(uns_easy) + '\n')
with open('unsolved_easy.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(uns_easy) + '\n')
with open('unsolved_medium.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(uns_med) + '\n')

print('authenticated as:', d.get('user_name'))
print('num_solved (profile):', d.get('num_solved'), '| solved.txt lines:', len(solved))
print('unsolved easy:', len(uns_easy), '| unsolved medium:', len(uns_med))