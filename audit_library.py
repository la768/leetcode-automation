import json, glob
from collections import defaultdict

BANK_FILES = sorted(glob.glob("solutions*.json")) + ["SOLUTIONS_MASTER.json"]
solved = {l.strip() for l in open("solved.txt", encoding="utf-8")
          if l.strip() and not l.startswith(("solved:", "="))}

seen = defaultdict(list)   # slug -> bank files
codes = {}                 # slug -> first-seen code
total = 0
for f in BANK_FILES:
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        print(f, "ERR", repr(e)[:80])
        continue
    if not isinstance(d, dict):
        print(f, "not a slug->code dict, skipped")
        continue
    total += len(d)
    for slug, code in d.items():
        seen[slug].append(f)
        codes.setdefault(slug, code)

# drop non-code/debug keys
def looks_like_code(v):
    return isinstance(v, str) and ("class " in v or "def " in v)

noncode = sorted(s for s in seen if not looks_like_code(codes[s]))
pool = {s: codes[s] for s in seen if looks_like_code(codes[s])}

already = sorted(s for s in pool if s in solved)
unsolved = sorted(s for s in pool if s not in solved)
dupes = sorted(s for s in pool if len(seen[s]) > 1)

print("BANK FILES            :", len([f for f in BANK_FILES if f != 'SOLUTIONS_MASTER.json']), "+ master")
print("TOTAL ENTRIES         :", total)
print("UNIQUE CODE SLUGS     :", len(pool))
print("NON-CODE KEYS DROPPED :", len(noncode), noncode[:10])
print("ALREADY SOLVED        :", len(already))
print("GENUINELY UNSOLVED    :", len(unsolved))
print("DUPLICATE SLUGS       :", len(dupes))

# verify every candidate has a cached qid (fast, offline)
try:
    qids = json.load(open("qids.json", encoding="utf-8"))
except FileNotFoundError:
    qids = {}
no_qid = [s for s in unsolved if s not in qids]
print("WITHOUT CACHED QID    :", len(no_qid), no_qid[:15])

json.dump(pool, open("library_all.json", "w", encoding="utf-8"))
open("library_unsolved.txt", "w", encoding="utf-8").write("\n".join(unsolved) + "\n")
open("library_solved.txt", "w", encoding="utf-8").write("\n".join(already) + "\n")
print("wrote library_all.json / library_unsolved.txt / library_solved.txt")
