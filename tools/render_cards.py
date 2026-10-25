"""Prebuild standalone SVG lesson cards (no fonts, images or APIs from elsewhere)."""
from pathlib import Path
import json,html,textwrap,re
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist';OUT=D/'data/english-cards';OUT.mkdir(parents=True,exist_ok=True)
P={'vocabulary':('#efd6d5','#382d2e'),'phrases':('#f1dfcf','#3d3028'),'idioms':('#efe6bd','#383426'),'daily':('#dce6d8','#2d382e'),'reflection':('#dce5ee','#2c3540'),'grammar':('#e7dfec','#382f40'),'smalltalk':('#e3e1df','#353331'),'essay':('#f1eadc','#37322b')};E=html.escape

def lines(value,width):
 if isinstance(value,list):value=' '.join(value)
 return [line for p in str(value).replace('\\n','\n').split('\n') for line in (textwrap.wrap(p,width,break_long_words=False) or [''])]
def text(value,x,y,size,width,weight='normal',family='Arial',color='#37322b'):
 ls=lines(value,width);markup=f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.38}">{E(l)}</tspan>' for i,l in enumerate(ls))+'</text>';return markup,y+len(ls)*size*1.38

def render(c,day,level):
 bg,fg=P[c['type']];essay=c['type']=='essay';W,H=(1434,660) if essay else (660,1434);parts=[f'<rect width="{W}" height="{H}" fill="{bg}"/>',f'<rect x="15" y="15" width="{W-30}" height="{H-30}" fill="none" stroke="{fg}" stroke-width="1"/>'];a,_=text(f'JAMES REAL / EVERYDAY ENGLISH   {level}   {day}',35,43,13,150,color=fg);parts.append(a)
 a,y=text(c['title'],35,88,30 if not essay else 32,34 if not essay else 74,'bold','Georgia',fg);parts.append(a)
 if essay:
  art=(D/c['illustration']).read_text();art=re.sub(r'<svg[^>]*>', '<svg x="1130" y="53" width="250" height="144" viewBox="0 0 660 380">',art,count=1);parts.append(art);roles=c.get('paragraphRoles',['Introduction','Body 1','Body 2','Conclusion'])
  for i,p in enumerate(c['paragraphs']):
   x=36+i*348;a,yy=text(roles[i],x,210,15,29,'bold',color=fg);parts.append(a);size=next(n for n in [17,16,15,14,13,12] if len(lines(p,int(315/(n*.55))))*n*1.38<280);a,yy=text(p,x,270,size,int(315/(size*.55)),color=fg);parts.append(a);assert yy<560,(c['id'],i,yy)
  a,_=text('YOUR TURN · '+c['exercise'],35,580,15,145,color=fg);parts.append(a)
 else:
  art=(D/c['illustration']).read_text();art=re.sub(r'<svg[^>]*>',f'<svg x="35" y="{y+8}" width="590" height="340" viewBox="0 0 660 380">',art,count=1);parts.append(art);y+=370
  rows=[]
  if c.get('ipa'):rows.append(('US pronunciation',c['ipa']+' '+c.get('partOfSpeech','')))
  for key,label in [('meaning','Meaning'),('wordForms','Word forms'),('example','In context'),('notes','Usage note'),('conversation','Conversation'),('exercise','Your turn')]:
   if c.get(key):rows.append((label,c[key]))
  # Pick a size using the complete text; never silently trim a lesson.
  available=H-70-y
  size=next((n for n in [18,17,16,15,14,13] if sum((len(lines(v,int(565/(n*.54))))*n*1.38+34) for _,v in rows)<available),12)
  for label,value in rows:
   a,y=text(label.upper(),35,y+15,12,70,'bold',color=fg);parts.append(a);a,y=text(value,35,y+8,size,int(565/(size*.54)),color=fg);parts.append(a);y+=12
  assert y<H-38,(c['id'],y)
 a,_=text(f'{c["type"].upper()}   /   {c["number"]:02d} OF 11',35,H-28,11,120,color=fg);parts.append(a)
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>{E(c["title"])}</title>'+''.join(parts)+'</svg>'
count=0
for p in sorted((D/'data/english-levels').glob('*.json')):
 data=json.loads(p.read_text())
 for level,unit in data.items():
  for card in unit['cards']:
   target=OUT/p.stem/level/(str(card['number']).zfill(2)+'.svg');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(render(card,p.stem,level));card['poster']='data/english-cards/'+str(target.relative_to(OUT));count+=1
 p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
print('Prebuilt standalone cards:',count)
