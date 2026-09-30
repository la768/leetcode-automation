"""Candidate bank = every banked solution whose slug is still unsolved here."""
import json

full = json.load(open('library_full.json', encoding='utf-8'))
uns = {l.strip() for l in open('unsolved_easy.txt', encoding='utf-8') if l.strip()}
uns |= {l.strip() for l in open('unsolved_medium.txt', encoding='utf-8') if l.strip()}
cand = {k: v for k, v in full.items() if k in uns}
json.dump(cand, open('cand_full.json', 'w', encoding='utf-8'), indent=1)
print('unsolved slugs with banked code:', len(cand))
