"""Report editorial repetition separately from structural release checks."""
from pathlib import Path
import json,re,collections
root=Path(__file__).resolve().parents[1];groups={k:collections.Counter() for k in ['targets','dialogues','prompts','essays']};cards=stories=0;photoDays=0;examples={}
def norm(v):return re.sub(r'\s+',' ',str(v or '').lower()).strip()
for p in sorted((root/'dist/data/english-levels').glob('2026-*.json')):
 data=json.loads(p.read_text());dayPhotos=[]
 for level,u in data.items():
  for c in u['cards']:
   cards+=1;stories+=bool(c.get('quoteBackground'));groups['targets'][(c['type'],norm(c['title']))]+=1
   copy=c.get('conversation','')
   for role in ['teacher','partner']:
    name=c.get('speakers',{}).get(role,{}).get('name','')
    if name:copy=re.sub(r'(^|\n)'+re.escape(name)+r':',r'\1'+('A:' if role=='teacher' else 'B:'),copy)
   if copy:groups['dialogues'][norm(copy)]+=1
   groups['prompts'][norm(c.get('exercise'))]+=1
   if c['type']=='essay':groups['essays'][norm(' '.join(c.get('paragraphs',[])))]+=1
   dayPhotos.append(c.get('photoCredit',{}).get('asset'))
 if len(set(dayPhotos))<len(dayPhotos):photoDays+=1
report={'cards':cards,'quoteMiniReadings':stories,'quoteMiniReadingsRemaining':2190-stories,'daysWithCrossLevelPhotoReuse':photoDays,'repetition':{k:{'distinct':len(v),'repeatedGroups':sum(n>1 for n in v.values()),'repeatedOccurrencesAfterFirst':sum(n-1 for n in v.values())} for k,v in groups.items()},'note':'Counts concern teaching titles and complete dialogue/prompt/essay reuse, not natural recurrence of learned words.'}
(root/'../../outputs/everyday-english-content-review.json').resolve().write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
