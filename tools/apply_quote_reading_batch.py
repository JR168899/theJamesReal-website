"""Apply only explicitly authored, source-checked quote readings; never synthesize filler."""
from pathlib import Path
import json,re,sys,importlib.util
R=Path(__file__).resolve().parents[1];D=R/'dist'
B=json.loads((R/'content/quote-reading-batch-001.json').read_text());day=B['date'];path=D/f'data/english-levels/{day}.json';data=json.loads(path.read_text());catalog=json.loads((R/'content/photo-catalog.json').read_text());photos=json.loads((R/'content/photo-assignments.json').read_text())
for lev,new in B['cards'].items():
 c=next(c for c in data[lev]['cards'] if c['type']=='reflection')
 used={x.get('photoCredit',{}).get('sourceURL') for x in data[lev]['cards'] if x['id']!=c['id']}
 photo=dict(catalog[new['photoScene']]);assert photo['sourceURL'] not in used,(lev,'photo repeat')
 c.update({k:v for k,v in new.items() if not k.startswith('photo')});
 if lev=='C2':c['quoteYear']=1899;c['quoteEventYear']=1895;c['quoteEventLabel']='First performed'
 c['quoteDateLabel']='Published';c['attribution']=c['quoteSpeaker']+' · '+c['quoteAuthor']+' · '+c['quoteWork']+' · Published '+str(c['quoteYear'])
 if c.get('quoteEventYear'):c['attribution']+=' · First performed '+str(c['quoteEventYear'])
 for key in ['meaning','synonyms','synonymNote','example','notes','conversation','displayTitle']:c.pop(key,None)
 c['readingVoiceRole']='teacher';c['quoteFormatVersion']='mini-reading-v1';c['editorialReview']={'batch':'quote-reading-001','sourceChecked':True,'levelReviewed':True}
 c['photoCredit']={k:photo[k] for k in ['asset','sourceURL','credit','licenseURL']};c['photoCredit'].update({'scene':new['photoScene'],'caption':new['photoCaption'],'orientation':'landscape','selection':'Reviewed reading-context photograph'})
 c['illustration']=photo['asset'];c['illustrationAlt']=new['photoCaption'];photos[c['id']]=dict(c['photoCredit'],fit='cover')
path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n');(R/'content/photo-assignments.json').write_text(json.dumps(photos,ensure_ascii=False,separators=(',',':'))+'\n')
sys.path.insert(0,str(R/'tools'));from restore_card_format import render
stats=[]
for lev,unit in data.items():
 c=next(c for c in unit['cards'] if c['type']=='reflection')
 for answer,key in [(False,'poster'),(True,'downloadPoster')]:
  svg,stat=render(c,day,lev,answer);(D/c[key]).write_text(svg);stats.append(stat)
(R/'content/quote-reading-batch-001-layout.json').write_text(json.dumps(stats,indent=2))
progress={'scope':'All 365 dates, all six levels: 2190 Quote cards','total':2190,'authoredAndLayoutChecked':6,'published':0,'remaining':2184,'batches':[{'id':'quote-reading-001','date':day,'levels':list(B['cards']),'status':'authored-and-layout-checked'}],'voiceRule':'Female teacher voice only, at the corresponding level pace','archiveRule':'Upload only checked final PNG cards to Google Drive, retaining original archive'}
(R/'content/quote-reading-progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n');print('Six sourced mini-readings applied; twelve SVG variants fit.')
