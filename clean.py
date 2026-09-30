import json,os,glob
c = chr(8203)
for f in glob.glob('solutions_big*.json'):
    try:
        d=json.load(open(f,encoding='utf-8'))
    except Exception as e:
        print('skip',f,e); continue
    changed=False
    for k in list(d.keys()):
        nk=k.replace(c,'')
        d[nk] = d.pop(k).replace(c,'')
        if nk != k: changed=True
        d[nk] = d[nk].replace(c,'')
    with open(f,'w',encoding='utf-8') as out:
        json.dump(d, out, indent=1)
    print('cleaned',f,len(d))
