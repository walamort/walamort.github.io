"""Build-independent regression checks; run from the repository root."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json, subprocess

ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.refs=[];self.ids=[];self.h1=0;self.ld=[];self.in_ld=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag in ('a','img','script','link'):
            u=a.get('href',a.get('src',''))
            if u:self.refs.append(u)
        if tag=='script':self.in_ld=a.get('type')=='application/ld+json'
    def handle_data(self,data):
        if self.in_ld:self.ld.append(json.loads(data))
    def handle_endtag(self,tag):
        if tag=='script':self.in_ld=False

files=[p for p in ROOT.rglob('*.html') if '.git' not in p.parts and '_fuente' not in p.parts]
pages={p:Page(p.read_text(encoding='utf-8')) for p in files}
issues=[]
for p,page in pages.items():
    dup=[v for v,n in Counter(page.ids).items() if n>1]
    if dup:issues.append(f'{p.relative_to(ROOT)} duplicate IDs: {dup}')
    for ref in page.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=((ROOT/unquote(u.path.lstrip('/'))) if u.path.startswith('/') else (p.parent/unquote(u.path))).resolve() if u.path else p
        if target.is_dir():target=target/'index.html'
        if not target.exists():issues.append(f'{p.relative_to(ROOT)} missing {ref}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            issues.append(f'{p.relative_to(ROOT)} missing fragment {ref}')
home=(ROOT/'index.html').read_text(encoding='utf-8')
before=subprocess.check_output(['git','show','HEAD:index.html'],cwd=ROOT,text=True,encoding='utf-8')
def payments(text):
    return Counter(ref for ref in Page(text).refs if 'pay.hotmart.com/' in ref)
assert payments(home)==payments(before),'Existing checkout links changed'
for rel in ('academia/index.html','academia/exploracion-instrumentos-del-mundo/index.html'):
    page=pages[ROOT/rel];assert page.h1==1;assert not any('pay.hotmart.com' in ref for ref in page.refs)
assert not issues,'\n'.join(issues)
print(f'PASS: {len(pages)} HTML pages; local files and fragments; unique IDs; JSON-LD; {sum(payments(home).values())} original Hotmart links preserved; course payments absent.')
