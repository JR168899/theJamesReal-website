"""Apply the confirmed female lead/male dialogue-B policy without changing lessons."""
from pathlib import Path
import json,re,importlib.util
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
spec=importlib.util.spec_from_file_location('card_format',ROOT/'tools/restore_card_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
pairs=json.loads((ROOT/'content/voice-pairs.json').read_text());report={'cards':0,'renamedConversations':0,'renderedPosters':0,'levels':{},'layoutErrors':[]}
for p in sorted((D/'data/english-levels').glob('2026-*.json')):
 data=json.loads(p.read_text())
 for level,unit in data.items():
  pair=pairs[level];report['levels'].setdefault(level,0)
  for c in unit['cards']:
   before=json.dumps(c,ensure_ascii=False);original=c.get('conversation','');updated=re.sub(r'(^|\n)A:\s*',lambda m:m[1]+pair['teacher']['name']+': ',original)
   updated=re.sub(r'(^|\n)B:\s*',lambda m:m[1]+pair['partner']['name']+': ',updated)
   if original: c['conversation']=updated
   for key in ['meaning','example','notes','exercise','answer','structure','quoteBackground','quoteCloserLook']:
    if isinstance(c.get(key),str):
     c[key]=re.sub(r'(^|\n)A:\s*',lambda m:m[1]+pair['teacher']['name']+': ',c[key])
     c[key]=re.sub(r'(^|\n)B:\s*',lambda m:m[1]+pair['partner']['name']+': ',c[key])
   c['speakers']=pair;c['voiceRuleVersion']='female-lead-male-dialogue-b-v1'
   c['readingVoiceRole']='teacher' if c['type'] in ['reflection','essay'] else 'teacher-with-dialogue-partner'
   if before!=json.dumps(c,ensure_ascii=False):
    report['renamedConversations']+=1
    for answer,key in [(False,'poster'),(True,'downloadPoster')]:
     svg,layout=fmt.render(c,p.stem,level,answer);(D/c[key]).write_text(svg);report['renderedPosters']+=1
   report['cards']+=1;report['levels'][level]+=1
 p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
 print('Updated',p.stem,flush=True)
(ROOT/'content/voice-role-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
