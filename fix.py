import json
c = chr(8203)
d = json.load(open('solutions_big2.json',encoding='utf-8'))
for k in d:
    d[k] = d[k].replace(c, '')
with open('solutions_big2.json','w',encoding='utf-8') as f:
    json.dump(d, f, indent=1)
print('cleaned',len(d))
