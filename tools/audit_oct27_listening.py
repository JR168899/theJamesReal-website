"""Validate only the approved single-day listening trial, without touching other lessons."""
from pathlib import Path
import json,re,wave
r=Path(__file__).resolve().parents[1];d=r/'dist';day='2026-10-27'
pairs=json.loads((r/'content/voice-pairs.json').read_text());units=json.loads((d/f'data/english-levels/{day}.json').read_text());rates=dict(zip(['A1','A2','B1','B2','C1','C2'],[.75,.8,.85,.9,.95,1]))
files=cards=0
for level,unit in units.items():
 pair=pairs[level];assert len(unit['cards'])==11
 manifest=json.loads((d/f'assets/lesson-audio/{day}/{level}/manifest.json').read_text());assert len(manifest['cards'])==11
 for v in pair.values():assert v['pace']==rates[level]
 for card in unit['cards']:
  assert card['speakers']==pair
  assert not re.search(r'(^|\n)[AB]:',card.get('conversation',''))
  for key in ['poster','downloadPoster']:
   source=(d/card[key]).read_text()
   assert not re.search(r'>[AB]:',source)
  recording=manifest['cards'][card['id']]
  if card.get('conversation'):
   assert recording['turns'][0]['name']==pair['teacher']['name']
   assert {t['name'] for t in recording['turns']}=={v['name'] for v in pair.values()}
  if card.get('quoteBackground'):
   assert recording['readingVoice']==pair['teacher']['voice'] and recording['readingVoice'].startswith('af_')
   assert recording['readingPace']==rates[level]
   assert not card.get('conversation') and 'conversation' not in recording
  for key in ['title','conversation','reading']:
   if key not in recording:continue
   with wave.open(str(d/recording[key])) as wav:
    assert wav.getnframes()>0 and wav.getsampwidth()==2 and wav.getnchannels()==1
    duration=wav.getnframes()/wav.getframerate()
    if key=='conversation':assert recording['turns'][-1]['start']<duration
   files+=1
  cards+=1
print(f'PASS: {cards} cards, six graded voice pairs, {files} prepared recordings. Scope: {day} only.')
