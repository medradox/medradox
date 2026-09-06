from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from datetime import date, timedelta
import json, re, sys, os
ROOT = Path(__file__).resolve().parents[1]
def write(name, text):
    (ROOT / name).write_text(text, encoding='utf-8')
def svg(w, h, body, title):
    if os.getenv('STATIC') == '1':
        body=re.sub(r'animation-delay:[^;"]+;?', '', body)
        body=body.replace('class="reveal"', '').replace('class="type-row"', '')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><style>text{{font-family:monospace}} .reveal{{animation:show .5s both}} @keyframes show{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}} .type-row{{animation:typing .22s both}} @keyframes typing{{from{{clip-path:inset(0 100% 0 0)}}to{{clip-path:inset(0 0 0 0)}}}} @media(prefers-reduced-motion:reduce){{.reveal,.type-row{{animation:none}}}}</style><rect width="{w}" height="{h}" rx="16" fill="#0d1117"/>{body}</svg>'''
def text(x,y,value,size=14,color='#c9d1d9'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(str(value))}</text>'
class Calendar(HTMLParser):
    def __init__(self):
        super().__init__(); self.cells={}; self.labels={}; self.tip=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='td' and a.get('data-date'):
            self.cells[a['id']]={'date':a['data-date'],'level':int(a['data-level'])}
        if tag=='tool-tip': self.tip=a.get('for')
    def handle_data(self,data):
        if self.tip: self.labels[self.tip]=self.labels.get(self.tip,'')+data
    def handle_endtag(self,tag):
        if tag=='tool-tip': self.tip=None
def heatmap():
    req=Request('https://github.com/users/medradox/contributions',headers={'User-Agent':'medradox-profile','Accept-Language':'en-US'})
    with urlopen(req,timeout=30) as response: html=response.read().decode()
    parser=Calendar(); parser.feed(html)
    days=[]
    for key, cell in parser.cells.items():
        label=parser.labels.get(key,'').strip()
        match=re.match(r'(No|[\d,]+) contributions? on ',label)
        if not match: raise ValueError(f'Unrecognized contribution label: {label}')
        cell['count']=0 if match[1]=='No' else int(match[1].replace(',',''))
        if cell['level'] not in range(5): raise ValueError('Unexpected level')
        days.append(cell)
    days.sort(key=lambda d:d['date'])
    if not 350<=len(days)<=378: raise ValueError('Incomplete contribution calendar')
    dates=[date.fromisoformat(d['date']) for d in days]
    if any(b-a!=timedelta(days=1) for a,b in zip(dates,dates[1:])): raise ValueError('Calendar gaps')
    total=sum(d['count'] for d in days)
    write('data/contributions.json',json.dumps({'username':'medradox','total':total,'days':days},indent=2)+'\n')
    start=dates[0]-timedelta(days=(dates[0].weekday()+1)%7)
    palette=['#161b22','#0e4429','#006d32','#26a641','#39d353']
    body=text(26,32,'medradox@github ~ $ ./contributions.sh',16,'#39d353')
    for day,dt in zip(days,dates):
        offset=(dt-start).days; col,row=divmod(offset,7)
        body+=f'<rect class="reveal" style="animation-delay:{(col+row)*.018:.3f}s" x="{26+col*15}" y="{57+row*15}" width="11" height="11" rx="3" fill="{palette[day["level"]]}"><title>{dt}: {day["count"]} contribuições</title></rect>'
    body+=text(26,190,f'{total} contribuições · {dates[0]:%d/%m/%Y} — {dates[-1]:%d/%m/%Y}',13)
    body+=text(26,220,'DADOS PÚBLICOS / ATUALIZAÇÃO DIÁRIA',10,'#8b949e')
    body+=text(646,220,'Menos',10,'#8b949e')
    for i,color in enumerate(palette):
        body+=f'<rect x="{684+i*16}" y="210" width="11" height="11" rx="3" fill="{color}"/>'
    body+=text(774,220,'Mais',10,'#8b949e')
    write('contrib-heatmap.svg',svg(860,240,body,'Calendário de contribuições de André Medrado'))
def identity():
    from PIL import Image, ImageOps, ImageDraw
    im=Image.open(ROOT/'data/professional-portrait.png').convert('RGB')
    im=ImageOps.fit(im,(600,600))
    # Remove only neutral light pixels connected to the outer background.
    mask=Image.new('L',im.size,0)
    mask.putdata([255 if min(px)>130 and max(px)-min(px)<24 else 0 for px in im.getdata()])
    for corner in [(0,0),(599,0),(0,599),(599,599)]:
        if mask.getpixel(corner)==255: ImageDraw.floodfill(mask,corner,128)
    background=mask.point(lambda x:255 if x==128 else 0)
    im.paste((255,255,255),mask=background)
    gray=ImageOps.autocontrast(ImageOps.grayscale(im),cutoff=1)
    gray=gray.point(lambda x:round(255*(x/255)**0.72))
    gray.save(ROOT/'data/source-prepped.png')
    gray=gray.resize((100,53),Image.Resampling.LANCZOS)
    ramp=" .`:-=+*cs#%@"
    body=text(20,30,'medradox ~ $ whoami',13,'#39d353')
    for y in range(gray.height):
        row=''.join(ramp[round((255-gray.getpixel((x,y)))*(len(ramp)-1)/255)] for x in range(gray.width))
        body+=f'<g class="type-row" style="animation-delay:{y*.045:.3f}s"><text x="20" y="{53+y*5.4:.1f}" xml:space="preserve" font-size="5.5" textLength="330" lengthAdjust="spacingAndGlyphs" fill="#c9d1d9">{escape(row)}</text></g>'
    body+=text(20,364,'ANDRÉ MEDRADO',16,'#39d353')
    body+=text(20,385,'Rio de Janeiro, Brasil',11,'#8b949e')
    write('medrado-ascii.svg',svg(370,410,body,'Retrato ASCII animado de André Medrado, baseado na foto aprovada'))
    rows=[('medradox@github','#39d353',21),('────────────────────────────────','#30363d',14),('Analista de Dados & BI','#ffffff',18),('Logística · Transporte · Supply Chain','#8b949e',13),('','#c9d1d9',14),('Stack   Power BI / DAX / SQL Server','#c9d1d9',14),('        Python / Pandas / Power Query','#c9d1d9',14),('Base    Engenharia de Produção','#c9d1d9',14),('Foco    Dados que orientam a operação','#c9d1d9',14),('','#c9d1d9',14),('-87%    Tempo de espera de descarga','#39d353',14),('1.600   Veículos monitorados','#39d353',14),('-15%    Custo de transporte','#39d353',14),('6       Dashboards em produção','#39d353',14)]
    body=''
    for i,(value,color,size) in enumerate(rows):
        body+=f'<g class="reveal" style="animation-delay:{i*.12:.2f}s">{text(24,38+i*25,value,size,color)}</g>'
    write('info-card.svg',svg(490,410,body,'Apresentação profissional de André Medrado'))
if __name__=='__main__':
    if '--identity' in sys.argv: identity()
    else: heatmap()
