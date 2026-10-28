"""Check authored Quote readings without treating legacy pending cards as complete."""
import json,re,wave,collections,struct
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'dist'
def audio_seconds(path):
 if path.suffix=='.wav':
  with wave.open(str(path)) as w:return w.getnframes()/w.getframerate()
 raw=path.read_bytes();assert raw[4:8]==b'ftyp' and b'mdat' in raw and len(raw)>1000,(path,'invalid MP4 audio')
 def boxes(start,end):
  cursor=start
  while cursor+8<=end:
   size,kind=struct.unpack_from('>I4s',raw,cursor);header=8
   if size==1:size=struct.unpack_from('>Q',raw,cursor+8)[0];header=16
   if size==0:size=end-cursor
   assert size>=header and cursor+size<=end,(path,'truncated MP4 atom')
   begin=cursor+header;stop=cursor+size
   if kind==b'mdhd':
    version=raw[begin]
    if version==0:scale,length=struct.unpack_from('>II',raw,begin+12)
    else:scale=struct.unpack_from('>I',raw,begin+20)[0];length=struct.unpack_from('>Q',raw,begin+24)[0]
    yield length/scale
   elif kind in [b'moov',b'trak',b'mdia']:yield from boxes(begin,stop)
   cursor=stop
 durations=list(boxes(0,len(raw)));assert durations,(path,'missing audio duration');return max(durations)
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
 assert audio_seconds(D/a['reading'])>15
 assert c.get('quoteAudio',{}).get('voice')==a['readingVoice']
 reviewed+=1
print(f'PASS: {reviewed} sourced mini-readings with female audio. Remaining: {2190-reviewed}. Whole-year release is not complete.')
