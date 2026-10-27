"""Restore supplied October 15 card specification, with stored graded content.
Run using the bundled Python with Pillow. No network or generation API is used.
The original source archive is never modified.
"""
from pathlib import Path
import json, re, html, importlib.util, base64
from functools import lru_cache
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
PHOTOS=json.loads((ROOT/'content/photo-assignments.json').read_text()) if (ROOT/'content/photo-assignments.json').exists() else {}
REF={}
for line in (ROOT/'content/word-reference.tsv').read_text().splitlines():
 if line.strip():
  word,ipa,pos,syn,example=line.split('|');REF[word]={'ipa':'/'+ipa+'/','partOfSpeech':pos,'synonyms':syn.split('; '),'example':example}
spec=importlib.util.spec_from_file_location('oldart',ROOT/'tools/build_illustrations.py');art=importlib.util.module_from_spec(spec);spec.loader.exec_module(art)
P={'vocabulary':('Vocabulary','#efd6d5','#382d2e','#9b4f53'),'phrases':('Phrasal verbs','#f1dfcf','#3d3028','#96633f'),'idioms':('Idioms & slang','#efe6bd','#383426','#806c27'),'daily':('Life phrases','#dce6d8','#2d382e','#526f4f'),'reflection':('Quote','#dce5ee','#2c3540','#4e6e8b'),'grammar':('Grammar','#e7dfec','#382f40','#7b628c'),'smalltalk':('Small talk','#e3e1df','#353331','#5f5b58'),'essay':('Essay','#f1eadc','#37322b','#81735e')}
E=lambda s:html.escape(str(s),quote=True)
def text(v):return '\n'.join(str(x) for x in v) if isinstance(v,list) else str(v or '').replace('\\n','\n')
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
CACHE={}
def font(size,bold=False):
 key=(round(size),bold)
 if key not in CACHE:CACHE[key]=ImageFont.truetype(BOLD if bold else FONT,key[0])
 return CACHE[key]
@lru_cache(maxsize=250000)
def measure(copy,size,bold=False):return font(size,bold).getlength(copy)
@lru_cache(maxsize=60000)
def wrap(copy,size,width,bold=False):
 out=[];space=measure(' ',size,bold)
 for para in text(copy).split('\n'):
  current='';used=0
  for word in para.split():
   ww=measure(word,size,bold)
   if used+(space if current else 0)+ww<=width:
    current=(current+' '+word).strip();used+=(space if used else 0)+ww
   else:
    if current:out.append(current)
    current=word;used=ww
    while used>width:
     cut=1
     while cut<len(current) and measure(current[:cut+1],size,bold)<=width:cut+=1
     out.append(current[:cut]);current=current[cut:];used=measure(current,size,bold)
  out.append(current)
 return out

def comic(card):
 photo=PHOTOS.get(card['id'])
 if photo:
  raw='__JR_PHOTO__'
  caption=wrap(photo['caption'],12,636)
  assert len(caption)<=2,(card['id'],'photo caption overflow')
  lines=''.join(f'<tspan x="12" y="{305+i*14}">{E(line)}</tspan>' for i,line in enumerate(caption))
  return f'<svg xmlns="http://www.w3.org/2000/svg" width="660" height="338" viewBox="0 0 660 338"><title>{E(photo["caption"])}</title><rect width="660" height="338" fill="#faf8f1"/><image x="0" y="0" width="660" height="292" preserveAspectRatio="xMidYMid slice" href="{raw}"/><text font-family="Arial, sans-serif" font-size="12" fill="#454545">{lines}</text><a href="{E(photo["sourceURL"])}"><text x="12" y="333" font-family="Arial, sans-serif" font-size="10" fill="#676767">{E(photo["credit"])}</text></a></svg>'

 key=art.subject(card)
 # Original, round-faced characters and clean, expressive Japanese family-manga
 # linework. The object/scene is selected from the actual lesson, not randomly.
 obj=art.ICONS.get(key,art.ICONS['book'])
 for old,new in {'#d9a67a':'#ffb84e','#a8bbaa':'#5db8ed','#d4a581':'#ffc650','#b2ccd0':'#b8e8ff','#9db8a0':'#83cf6e','#a7bfc6':'#59baf1','#dfc590':'#ffe16d','#a6bac0':'#76c6f3','#d0b079':'#e9b465','#b7a3bf':'#d59bea','#c7a1a3':'#f78da0','#b7bec8':'#7fc4ef','#c6b8a5':'#f5c488'}.items():obj=obj.replace(old,new)
 v=card['number']%3;shirt=['#54b8ec','#f5c64e','#f48f91'][v]
 person=f'''<g stroke="#252b35" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M107 226L93 261M173 226L188 251L222 237" fill="none"/><path d="M112 267V308L91 310M162 267V308L183 310" fill="none"/><path d="M103 219Q140 195 177 219L169 272H111Z" fill="{shirt}"/><path d="M126 216L140 232L154 216" fill="white"/><ellipse cx="140" cy="165" rx="48" ry="51" fill="#ffdab4"/><path d="M94 156Q83 103 133 108Q183 102 190 150L172 140L165 147L146 131L130 143L117 136L110 151Z" fill="#33343c"/><ellipse cx="126" cy="162" rx="12" ry="16" fill="white" stroke-width="2.5"/><ellipse cx="153" cy="162" rx="12" ry="16" fill="white" stroke-width="2.5"/><ellipse cx="130" cy="165" rx="4" ry="7" fill="#252b35" stroke="none"/><ellipse cx="149" cy="165" rx="4" ry="7" fill="#252b35" stroke="none"/><path d="M139 169L135 178L144 178M122 188Q141 209 162 187Z" fill="white"/><path d="M115 149L128 147M152 147L164 151" fill="none"/><ellipse cx="107" cy="182" rx="8" ry="4" fill="#f7a58f" stroke="none"/><ellipse cx="174" cy="181" rx="8" ry="4" fill="#f7a58f" stroke="none"/></g>'''
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="660" height="338" viewBox="0 0 660 338"><title>{E(card['title'])}</title><desc>Original family-manga illustration: {E(key)}, related to {E(card['title'])}.</desc><defs><pattern id="dots" width="13" height="13" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".7" fill="#a5b8c6" opacity=".22"/></pattern></defs><rect width="660" height="338" fill="#fffdf6"/><rect x="12" y="12" width="636" height="314" rx="3" fill="#f2f9fc" stroke="#b9cbd1"/><path d="M13 278Q170 251 330 278T647 275V325H13Z" fill="#e5efda"/><rect x="13" y="13" width="634" height="312" fill="url(#dots)"/><ellipse cx="151" cy="315" rx="83" ry="8" fill="#cad7cd"/>{person}<g transform="translate(445 176) scale(1.15)" stroke="#252b35" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round" fill="none">{obj}</g><path d="M226 134L238 121M239 151L258 148M531 92L540 81" stroke="#5ba9c9" stroke-width="3" stroke-linecap="round"/></svg>'''

def enrich(c,lev):
 typ=c['type']
 if typ=='reflection' and c.get('quoteBackground'):
  for key in ['meaning','synonyms','synonymNote','example','notes','conversation','displayTitle']:c.pop(key,None)
  c['readingVoiceRole']='teacher'
  return c
 if typ=='essay' and c.get('paragraphs'):c['paragraphs']=[re.sub(r'\b(First|Next|Second), (We|Our|This|The)\b',lambda m:m[1]+', '+m[2].lower(),p) for p in c['paragraphs']]
 meaning=text(c.get('meaning'));title=c['title'];example=text(c.get('example'))
 if typ=='phrases':
  separable={'bear out':('bear something out','bear out something'),'bring along':('bring something along','bring along something'),'carve out':('carve something out','carve out something'),'factor in':('factor something in','factor in something'),'find out':('find something out','find out something'),'iron out':('iron something out','iron out something'),'map out':('map something out','map out something'),'pick up':('pick something up','pick up something'),'put on':('put something on','put on something'),'set aside':('set something aside','set aside something'),'weigh up':('weigh something up','weigh up something'),'work out':('work something out','work out something')}
  if title in separable:c['displayTitle']='\n'.join(separable[title])
 if typ=='vocabulary':
  assert title in REF,('Missing word reference',title)
  ref=REF[title]
  for field in ['ipa','partOfSpeech','synonyms','example']:
   if not c.get(field):c[field]=ref[field]
  if not c.get('wordForms'):c['wordForms']=ref['partOfSpeech'].capitalize()+'. Learn the word in the sense shown below.'
 if typ in ['phrases','idioms','daily','reflection'] and not c.get('synonyms'):
  c['synonyms']=[meaning.rstrip('.')]
 if not c.get('example'):
  examples={'daily':title,'reflection':'As we worked together, we remembered: “'+title+'”','grammar':text(c.get('answer')),'smalltalk':title}
  c['example']=examples.get(typ,'We use “'+title+'” when we discuss this idea.')
 if not c.get('notes'):
  notes={'idioms':'Use this expression as a whole. Its meaning depends on the situation, not on the separate words.','daily':'Use this phrase in a friendly conversation. Listen to the reply before asking your next question.','reflection':'This is an original James Real learning reflection. Explain the idea in your own words rather than treating it as a factual rule.','smalltalk':'Ask this as a genuine question. Listen to the answer, then ask a related follow-up.','grammar':'Read the example together with the rule. Notice the verb form and keep the same pattern in your own sentence.'}
  c['notes']=notes.get(typ,'Use this expression in the sense shown in the example.')
 if typ!='essay' and not c.get('conversation'):
  if typ=='grammar':c['conversation']='A: Could you give me an example?\nB: '+text(c['example'])+'\nA: Which pattern does that use?\nB: '+meaning
  elif typ=='smalltalk':c['conversation']='A: '+title+'\nB: I would like to hear more about that.\nA: What interests you most?\nB: Let us start with your experience.'
  else:c['conversation']='A: How would you express this idea?\nB: '+title+'\nA: What does that mean here?\nB: '+meaning
 if typ!='essay' and len(text(c.get('conversation')).split('\n'))==3:c['conversation']=text(c['conversation'])+'\nB: Let us try it together.'
 c['formatVersion']='landscape-portrait-photos-v2';c['illustrationAlt']='Original family-manga scene illustrating '+title+'.'
 from word_forms import forms
 if typ=='vocabulary':c['wordForms']=forms(title,c['partOfSpeech'])
 from refine_teaching_fields import refine
 c=refine(c)
 if c['id'] in PHOTOS:c['photoCredit']={k:v for k,v in PHOTOS[c['id']].items() if k!='fit'};c['illustrationAlt']=PHOTOS[c['id']]['caption']
 return c

def label(copy,x,y,size=16):return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="700" fill="#8c8981">{E(copy)}</text>'
def block(lines,x,y,size,leading,bold=False,color='#37322b'):
 return f'<text font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">'+''.join(f'<tspan x="{x}" y="{y+i*leading}">{E(l)}</tspan>' for i,l in enumerate(lines))+'</text>'

def rows(c,answer):
 if c['type']=='reflection' and c.get('quoteBackground'):
  question=text(c.get('exercise'))
  if answer:question+=' (Model: '+text(c.get('answer'))+')'
  return [('The story',text(c['quoteBackground'])),('A closer look',text(c['quoteCloserLook'])),('Your turn',question)]
 r=[]
 for field,title in [('meaning','Meaning'),('synonyms','Synonyms'),('example','In context'),('notes','Usage note'),('conversation','Conversation')]:
  if field=='synonyms' and c['type'] not in ['vocabulary','phrases','idioms','daily','reflection']:continue
  value='; '.join(c[field]) if field=='synonyms' and isinstance(c.get(field),list) else text(c.get(field))
  if field=='synonyms' and c.get('synonymNote'):value+=' · '+text(c['synonymNote'])
  assert value,(c['id'],field)
  r.append((title,value))
 q=re.split(r'\n?Model Answer\s*:',text(c.get('exercise')),flags=re.I)[0].strip()
 if answer:q+=' (Model: '+text(c.get('answer'))+')'
 r.append(('Your turn',q));return r

def render(c,day,lev,answer):
 typ=c['type'];name,bg,fg,border=P[typ];essay=typ=='essay';W,H=(1434,660) if essay else (660,1434);edge=14 if essay else 7;inset=24 if essay else 12
 parts=[f'<rect width="{W}" height="{H}" fill="#f7f4eb"/>',f'<rect x="{edge}" y="{edge}" width="{W-2*edge}" height="{H-2*edge}" rx="{10 if essay else 5}" fill="{bg}" stroke="{border}" stroke-width="{5 if essay else 2.5}"/>',f'<rect x="{inset}" y="{inset}" width="{W-2*inset}" height="{H-2*inset}" rx="3" fill="none" stroke="#f7f1e5" stroke-width="{10 if essay else 5}"/>']
 x=42 if essay else 28;headerY=42 if essay else 55
 category='Phrasal verb' if typ=='phrases' else name
 heading='Everyday English - '+lev+' - '+day.replace('-','/')+' - '+category+' - '+str(c['categoryNumber']).zfill(2)
 parts.append(block([heading],x,headerY,22 if essay else 15,18,True,fg))
 if essay:
  photo=PHOTOS[c['id']];raw='__JR_PHOTO__'
  parts.append(f'<g aria-label="Essay portrait photograph"><rect x="1066" y="96" width="328" height="488" fill="#faf8f1" stroke="{border}" stroke-width="2"/><image x="1070" y="100" width="320" height="480" preserveAspectRatio="xMidYMid slice" href="{raw}"/></g>')
  parts.append(block(wrap(photo['caption'],12,320),1070,601,12,15,False,fg))
  parts.append(f'<a href="{E(photo["sourceURL"])}">'+block([photo['credit']],1070,640,11,13,False,fg)+'</a>')
  title=wrap(c['title'],36,1000,True);parts.append(block(title,42,90,36,42,True,fg))
  roleNames=['INTRODUCTION','DEVELOP THE IDEA','EXAMPLE & REFLECTION','CONCLUSION']
  # Preserve the existing four-paragraph learning structure; never convert it
  # into columns or truncate it to fit the landscape canvas.

  for size in range(32,14,-1):
   y=max(126,66+len(title)*40+26);bs=[];leading=size*1.17
   for i,p in enumerate(c['paragraphs']):
    width=1000;ls=wrap(p,size,width);bs.append((i,ls,y));y+=18+len(ls)*leading+15
   guide='BUILD YOUR OWN · '+text(c.get('structure'))
   if c.get('notes'):guide+=' '+text(c['notes'])
   prompt=text(c['exercise'])
   if answer:prompt+=' (Model: '+text(c.get('answer'))+')'
   footerSize=min(18,size);footerLeading=footerSize*1.22;footer=wrap(guide+'\n'+prompt,footerSize,1000);bottom=y+len(footer)*footerLeading
   if bottom<=622:break
  assert bottom<=622,(c['id'],'essay overflow',bottom)
  for i,ls,y0 in bs:
   parts.append(label(str(i+1)+' · '+roleNames[i],42,y0,17));parts.append(block(ls,42,y0+size+5,size,leading,False,fg))
  parts.append(block(footer,42,y+footerSize,footerSize,footerLeading,False,fg))
 else:
  artwork=comic(c)
  artwork=re.sub(r'<svg[^>]*>','<svg x="28" y="80" width="604" height="310" viewBox="0 0 660 338">',artwork,count=1);parts.append(artwork)
  r=rows(c,answer)
  for step in range(101):
   scale=1.1-step*.005;ts=max(36,min(50,46*scale));size=28*scale;leading=35*scale;lab=16*scale;gap=29*scale
   titles=wrap(c.get('displayTitle',c['title']),ts,604,True);y=432+len(titles)*ts*1.25;meta=[]
   if typ=='reflection' and c.get('quoteAuthor'):
    copy=c.get('attribution') or c['quoteAuthor']+' · '+c['quoteWork']+' · Published '+str(c['quoteYear'])
    ls=wrap(copy,20*scale,604);meta.append((ls,y,20*scale));y+=len(ls)*24*scale
   if typ=='vocabulary':
    for copy,sz in [('US '+text(c['ipa'])+'   '+text(c['partOfSpeech']),28*scale),(text(c.get('wordForms')),22*scale)]:
     ls=wrap(copy,sz,604);meta.append((ls,y,sz));y+=len(ls)*sz*1.22
   y+=35*scale;bs=[]
   for title,copy in r:
    if title=='Your turn':y=max(y,1244)
    ls=wrap(copy,size,604);bs.append((title,ls,y));y+=lab*1.15+len(ls)*leading+gap
   bottom=y-gap
   if bottom<=1388:break
  assert bottom<=1388,(c['id'],'portrait overflow',bottom)
  parts.append(block(titles,28,432+ts,ts,ts*1.25,True,fg))
  for ls,y0,sz in meta:parts.append(block(ls,28,y0+sz,sz,sz*1.22,False,fg))
  for title,ls,y0 in bs:parts.append(label(title.upper(),28,y0+lab,lab));parts.append(block(ls,28,y0+lab*1.15+size,size,leading,False,fg))
  assert all('\n' not in line for _,ls,_ in bs for line in ls)
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>{E(c["title"])}</title>'+''.join(parts)+'</svg>',{'id':c['id'],'answer':answer,'bottom':round(bottom,1),'font':round(size,2)}

def main():
 stats=[];count=0;orig={}
 for p in sorted((D/'data/english-levels').glob('*.json')):
  data=json.loads(p.read_text())
  for lev,u in data.items():
   for ci,c in enumerate(u['cards']):
    c=enrich(c,lev);u['cards'][ci]=c
    assert c['id'] in PHOTOS,('Missing photo',c['id'])
    c['illustration']=PHOTOS[c['id']]['asset']
    folder=D/'data/english-cards'/p.stem/lev;folder.mkdir(parents=True,exist_ok=True)
    for answer,suffix in [(False,''),(True,'-download')]:
     svg,stat=render(c,p.stem,lev,answer);target=folder/(str(c['number']).zfill(2)+suffix+'.svg');target.write_text(svg);stats.append(stat)
     c['downloadPoster' if answer else 'poster']='data/english-cards/'+str(target.relative_to(D/'data/english-cards'))
    count+=1
  p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
  print('Completed',p.stem,flush=True)
 (ROOT/'content/card-format-audit.json').write_text(json.dumps({'cards':count,'renders':len(stats),'reference':'User-supplied October 15 2026 cards','results':stats},separators=(',',':')))
 print('Restored cards:',count,'SVG variants:',len(stats),'smallest portrait font:',min(x['font'] for x in stats if x['id'].split('-')[-1]!='11'))
if __name__=='__main__':main()
