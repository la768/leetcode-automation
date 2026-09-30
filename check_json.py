import glob
import json

for f in sorted(glob.glob('solutions_a*.json')):
    try:
        d = json.load(open(f, encoding='utf-8'))
        print(f, 'OK', len(d))
    except Exception as e:
        print(f, 'BROKEN', e)
