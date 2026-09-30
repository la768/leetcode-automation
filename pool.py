"""Lists the unsolved slugs that have NO code in the merged library.

Writes candidates_new.json = {slug: 'Easy'|'Medium'} and prints the easy ones
(those are where fresh solutions get authored for the next campaign).
"""
import json

merged = json.load(open('library_merged.json', encoding='utf-8'))
uns_easy = [l.strip() for l in open('unsolved_easy.txt', encoding='utf-8') if l.strip()]
uns_med = [l.strip() for l in open('unsolved_medium.txt', encoding='utf-8') if l.strip()]

new_easy = [s for s in uns_easy if s not in merged]
new_med = [s for s in uns_med if s not in merged]
cand = {s: 'Easy' for s in new_easy}
cand.update({s: 'Medium' for s in new_med})
json.dump(cand, open('candidates_new.json', 'w', encoding='utf-8'), indent=1)

print('no-code easy:', len(new_easy), '| no-code medium:', len(new_med))
print('--- no-code EASY ---')
for i in range(0, len(new_easy), 6):
    print('  ' + '  '.join('%-42s' % s for s in new_easy[i:i + 6]))
