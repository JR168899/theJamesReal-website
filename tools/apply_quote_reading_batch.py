"""Apply only explicitly authored, source-checked quote readings; never synthesize filler."""
from pathlib import Path
import json,re,sys,importlib.util
R=Path(__file__).resolve().parents[1];D=R/'dist'
batchPath=Path(sys.argv[1]) if len(sys.argv)>1 else R/'content/quote-reading-batch-001.json'
B=json.loads(batchPath.read_text());batchId=B.get('id',batchPath.stem);day=B['date'];path=D/f'data/english-levels/{day}.json';data=json.loads(path.read_text());catalog=json.loads((R/'content/photo-catalog.json').read_text());photos=json.loads((R/'content/photo-assignments.json').read_text())
for lev,new in B['cards'].items():
 c=next(c for c in data[lev]['cards'] if c['type']=='reflection')
 used={x.get('photoCredit',{}).get('sourceURL') for x in data[lev]['cards'] if x['id']!=c['id']}
 photo=dict(catalog[new['photoScene']]);assert photo['sourceURL'] not in used,(lev,'photo repeat')
 c.update({k:v for k,v in new.items() if not k.startswith('photo')});
 if not new.get('quoteEventYear'):
  c.pop('quoteEventYear',None);c.pop('quoteEventLabel',None)
 c['quoteDateLabel']='Published';c['attribution']=c['quoteSpeaker']+' · '+c['quoteAuthor']+' · '+c['quoteWork']+' · Published '+str(c['quoteYear'])
 if c.get('quoteEventYear'):c['attribution']+=' · First performed '+str(c['quoteEventYear'])
 for key in ['meaning','synonyms','synonymNote','example','notes','conversation','displayTitle']:c.pop(key,None)
 c['readingVoiceRole']='teacher';c['quoteFormatVersion']='mini-reading-v1';c['editorialReview']={'batch':batchId,'sourceChecked':True,'levelReviewed':True}
 c['photoCredit']={k:photo[k] for k in ['asset','sourceURL','credit','licenseURL']};c['photoCredit'].update({'scene':new['photoScene'],'caption':new['photoCaption'],'orientation':'landscape','selection':'Reviewed reading-context photograph'})
 c['illustration']=photo['asset'];c['illustrationAlt']=new['photoCaption'];photos[c['id']]=dict(c['photoCredit'],fit='cover')
path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n');(R/'content/photo-assignments.json').write_text(json.dumps(photos,ensure_ascii=False,separators=(',',':'))+'\n')
sys.path.insert(0,str(R/'tools'));from restore_card_format import render
stats=[]
for lev in B['cards']:
 unit=data[lev]
 c=next(c for c in unit['cards'] if c['type']=='reflection')
 for answer,key in [(False,'poster'),(True,'downloadPoster')]:
  svg,stat=render(c,day,lev,answer);(D/c[key]).write_text(svg);stats.append(stat)
(R/'content'/f'{batchPath.stem}-layout.json').write_text(json.dumps(stats,indent=2))
queuePath=R/'content/quote-revision-queue.json';queue=json.loads(queuePath.read_text())
for row in queue:
 if row['date']==day and row['level'] in B['cards']:
  if row['status']!='published':row['status']='authored-layout-checked'
  row['batch']=batchId
queuePath.write_text(json.dumps(queue,separators=(',',':'))+'\n')
ledgerPath=R/'content/quote-source-ledger.json';ledger=json.loads(ledgerPath.read_text());ledger=[e for e in ledger if not(e['date']==day and e['level'] in B['cards'])]
for lev in B['cards']:
 c=next(x for x in data[lev]['cards'] if x['type']=='reflection')
 ledger.append({'date':day,'level':lev,'target':' '.join(re.findall(r"[\w']+",c['title'].casefold())),'author':c['quoteAuthor'],'speaker':c['quoteSpeaker'],'source':c['quoteSourceURL'],'voiceRole':'teacher'})
assert len({e['target'] for e in ledger})==len(ledger),'Duplicate authored quotation'
ledgerPath.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
progressPath=R/'content/quote-reading-progress.json';progress=json.loads(progressPath.read_text());authored=sum(e['status']!='pending' for e in queue);progress.update({'authoredAndLayoutChecked':authored,'published':sum(e['status']=='published' for e in queue),'archived':sum(e['driveStatus']=='verified' for e in queue),'remaining':2190-authored})
if not any(b['id']==batchId for b in progress['batches']):progress['batches'].append({'id':batchId,'date':day,'levels':list(B['cards']),'status':'authored-and-layout-checked'})
progressPath.write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n');print('Applied and rendered',len(B['cards']),'mini-readings. Authored:',authored,'/ 2190')
