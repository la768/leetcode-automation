import json,subprocess
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
r=subprocess.run(['curl.exe','-s','--max-time','40','https://leetcode.com/api/problems/all/','-H','User-Agent: '+UA,'-b','lc_cookies.txt'],capture_output=True,text=True,encoding='utf-8',errors='replace')
d=json.loads(r.stdout)
qids={}
try: qids=json.load(open('qids.json',encoding='utf-8'))
except Exception: pass
n=0
for p in d.get('stat_status_pairs',[]):
    st=p.get('stat',{})
    slug=st.get('question__title_slug')
    qid=st.get('question_id')
    if slug and qid and slug not in qids:
        qids[slug]=str(qid); n+=1
json.dump(qids,open('qids.json','w',encoding='utf-8'))
print('added',n,'total',len(qids))
print('arrange-coins:',qids.get('arrange-coins'),'dominant-index:',qids.get('dominant-index'))
