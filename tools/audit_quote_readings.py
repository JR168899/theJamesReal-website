"""Check authored Quote readings without treating legacy pending cards as complete."""
import json,re,wave,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'dist'
canon=lambda x:' '.join(re.findall(r"[\w']+",str(x).casefold().replace('’',"'")))
allquotes=[]
for p in sorted((D/'data/english-levels').glob('*.json')):
 for level,unit in json.loads(p.read_text()).items():
  allquotes.extend((p.stem,level,c) for c in unit['cards'] if c['type']=='reflection')
assert len(allquotes)==2190
counts=collections.Counter(canon(c['title']) for _,_,c in allquotes);reviewed=0
for day,level,c in allquotes:
 if not c.get('quoteBackground'):continue
 assert counts[canon(c['title'])]==1,(c['id'],'repeated quote')
 assert all(c.get(k) for k in ['quoteAuthor','quoteSpeaker','quoteWork','quoteYear','quoteSourceURL','quoteCloserLook','exercise','answer'])
 assert c['readingVoiceRole']=='teacher' and not c.get('conversation')
 assert c['quoteBackground']!=c['quoteCloserLook']
 assert c['editorialReview']['sourceChecked'] and c['editorialReview']['levelReviewed']
 source=(D/c['poster']).read_text();download=(D/c['downloadPoster']).read_text()
 for name in ['THE STORY','A CLOSER LOOK','YOUR TURN']:assert name in source
 for name in ['MEANING','SYNONYMS','CONVERSATION']:assert name not in source
 assert '(Model:' not in source and '(Model:' in download
 m=json.loads((D/f'assets/lesson-audio/{day}/{level}/manifest.json').read_text());a=m['cards'][c['id']];assert a['readingVoice'].startswith('af_') and not a.get('conversation')
 with wave.open(str(D/a['reading'])) as w:assert w.getnframes()/w.getframerate()>15
 reviewed+=1
print(f'PASS: {reviewed} sourced mini-readings with female audio. Remaining: {2190-reviewed}. Whole-year release is not complete.')
