from pathlib import Path
import json,sys
from urllib.request import Request,urlopen
sys.path.insert(0,str(Path(__file__).parent))
from build_profile import svg,text,write
ROOT=Path(__file__).resolve().parents[1]
def fetch(path):
    with urlopen(Request('https://api.github.com/'+path,headers={'User-Agent':'medradox-profile'}),timeout=30) as r: return json.load(r)
u=fetch('users/medradox'); repos=fetch('users/medradox/repos?per_page=100')
d=json.loads((ROOT/'data/contributions.json').read_text())
stars=sum(r['stargazers_count'] for r in repos)
body=text(28,36,'GITHUB / ATIVIDADE PÚBLICA',16,'#a78bfa')
for i,(label,value) in enumerate([('REPOSITÓRIOS',u['public_repos']),('CONTRIBUIÇÕES',d['total']),('SEGUIDORES',u['followers']),('ESTRELAS',stars)]):
    x=28+i*208
    body+=text(x,91,value,32,'#e9d5ff')+text(x,123,label,11,'#8b949e')
body+=text(28,155,'Contribuições no período do calendário · demais métricas atuais',11,'#8b949e')
write('assets/analytics.svg',svg(860,180,body,'Estatísticas públicas do GitHub'))
languages={}
for repo in repos:
    if not repo['fork']:
        for lang,size in fetch('repos/'+repo['full_name']+'/languages').items(): languages[lang]=languages.get(lang,0)+size
body=text(28,34,'LINGUAGENS / CÓDIGO PÚBLICO',16,'#a78bfa'); total=sum(languages.values())
for i,(lang,size) in enumerate(sorted(languages.items(),key=lambda item:-item[1])[:5]):
    y=72+i*35; pct=size/total*100
    body+=text(28,y,f'{lang} · {pct:.1f}%',13)+f'<rect x="250" y="{y-12}" width="{pct*5.5:.1f}" height="12" rx="6" fill="#818cf8"/>'
body+=text(28,90+min(len(languages),5)*35,'Proporção em bytes; não representa nível de domínio profissional.',11,'#8b949e')
write('assets/languages.svg',svg(860,120+min(len(languages),5)*35,body,'Linguagens nos repositórios públicos'))
