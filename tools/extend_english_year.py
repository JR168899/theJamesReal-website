"""Extend stored graded editions across 2026; preserve originals and revision history."""
from pathlib import Path
from datetime import date,timedelta
import json,copy
from build_calendar import make_unit,LEVELS,TOPICS,STAGES,save
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
reference={}
for line in (ROOT/'content/word-reference.tsv').read_text().splitlines():
 if line.strip():
  a=line.split('|');reference[a[0]]=a
holiday_words={}
for line in (ROOT/'content/holiday-word-reference.tsv').read_text().splitlines():
 if line.strip():
  word,ipa,pos,syn,example,meaning,scene=line.split('|')
  holiday_words[word]=dict(meaning=meaning,scene=scene)
  reference[word]=[word,ipa,pos,syn,example]
(ROOT/'content/word-reference.tsv').write_text('\n'.join('|'.join(reference[k]) for k in sorted(reference))+'\n')
base_meanings={row[i]:row[i+1] for t in TOPICS for row in t['words'] for i in [0,2]}
for p in (D/'data/english-levels').glob('*.json'):
 for u in json.loads(p.read_text()).values():
  for c in u['cards']:
   if c['type']=='vocabulary':base_meanings.setdefault(c['title'],c['meaning'])
base_meanings['communal']='shared or used by a group of people'
def topic(key,title,event,action,place,r1,e1,r2,e2,s1,s2,wordpairs,scene):
 return dict(id=key,title=title,event=event,action=action,place=place,object=scene,reason1=r1,example1=e1,reason2=r2,example2=e2,simple1=s1,simple2=s2,words=[[w,holiday_words.get(w,{}).get('meaning',base_meanings.get(w,'')),v,holiday_words.get(v,{}).get('meaning',base_meanings.get(v,''))] for w,v in wordpairs],photoScene=scene)
holidays=[
('2026-01-01',0,topic('newyear','A small start to the new year','New Year’s Day','start a new routine','at the start of the year','a small goal is easier to maintain','we choose ten minutes of reading rather than promise an hour','reviewing progress makes change visible','we note what helped and adjust the next step','We choose one small goal. We can start today.','We write what we did. We can see our progress.',[('year','plan'),('goal','remember'),('habit','progress'),('priority','realistic'),('retrospective','sustainable'),('teleology','reflexivity')],'calendar')),
('2026-02-14',6,topic('valentine','A thoughtful message for Valentine’s Day','Valentine’s Day','send a thoughtful greeting','when sending a greeting','a specific message expresses care more clearly than a grand phrase','we thank a friend for a particular act of kindness','respecting the recipient makes a greeting considerate','we avoid assuming that everyone wants a romantic message','We write a card for a friend. We say thank you.','We ask before sharing a photo. We respect our friend.',[('flower','card'),('invite','prepare'),('appreciate','considerate'),('affection','platonic'),('solicitude','reciprocity'),('interdependence','intersubjective')],'valentine')),
('2026-02-17',2,topic('lunarnewyear','Welcoming the Lunar New Year','Lunar New Year','welcome the new year together','at a Lunar New Year gathering','asking about a custom prevents careless assumptions','we ask the host how their family exchanges greetings','sharing time connects generations','we invite an older relative to explain a family recipe','We give a greeting. We listen to our host.','We eat together. A relative tells us a story.',[('lantern','envelope'),('reunion','luck'),('celebrate','prosperity'),('auspicious','symbolism'),('intergenerational','continuity'),('diaspora','syncretism')],'lunar')),
('2026-04-05',6,topic('easter','An Easter gathering with room for everyone','Easter','prepare an Easter gathering','at an Easter gathering','clear instructions help children join an activity safely','we mark the egg-hunt area and explain which places are out of bounds','recognizing different practices makes the gathering welcoming','we ask families which activities suit them instead of assuming a shared belief','We put eggs in a basket. We explain the game.','We ask what our guests enjoy. Everyone can choose an activity.',[('egg','basket'),('hunt','decorate'),('tradition','considerate'),('renewal','observance'),('symbolism','continuity'),('phenology','syncretism')],'easter')),
('2026-04-22',4,topic('earthday','Earth Day in everyday choices','Earth Day','reduce everyday waste','during an Earth Day activity','changing one repeat purchase can reduce waste over time','we bring a reusable bag and refill a bottle','local knowledge makes shared action more effective','we check the local recycling rules before sorting materials','We use our bag again. We do not need a new one.','We check the signs on the bins. We put each item in the right place.',[('plant','water'),('reuse','recycle'),('responsibility','practical'),('sustainable','stewardship'),('interdependence','externality'),('subsidiarity','symbiosis')],'plant')),
('2026-05-10',3,topic('mothersday','A practical way to say thank you','Mother’s Day','show appreciation through an action','when thanking someone who cares for us','specific thanks recognize work that can go unnoticed','we name one helpful action instead of relying on a general compliment','asking what would help keeps appreciation responsive','we offer to do a task and listen to the answer','We say thank you for one kind thing. We explain why it helped.','We ask what we can do. We help with a task.',[('mother','thank'),('share','prepare'),('appreciate','considerate'),('gratitude','affection'),('solicitude','intergenerational'),('reciprocity','interdependence')],'family')),
('2026-06-21',3,topic('fathersday','Making time for a shared activity','Father’s Day','spend time with someone who cares for us','during a family activity','a simple shared activity creates space for conversation','we choose a short walk that suits everyone’s pace','attention matters more than an elaborate plan','we put our phones away and ask about a familiar memory','We choose a short walk. We have time to talk.','We put our phones away. We listen to each other.',[('father','thank'),('walk','remember'),('appreciate','patient'),('gratitude','receptive'),('intergenerational','solicitude'),('reciprocity','intersubjective')],'family')),
('2026-07-04',4,topic('independenceday','Sharing a public celebration','Independence Day','join a public celebration','at a neighborhood celebration','checking arrangements makes a crowded event easier to navigate','we agree on a meeting place before the parade begins','public enjoyment depends on consideration for others','we keep walkways clear and follow the event’s safety instructions','We choose a place to meet. We can find each other.','We keep the path clear. Other people can pass.',[('flag','parade'),('arrive','prepare'),('freedom','responsibility'),('civic','coordinate'),('externality','contextual'),('subsidiarity','pluralism')],'independence')),
('2026-10-31',5,topic('halloween','A Halloween evening that welcomes everyone','Halloween','prepare a Halloween evening','during a Halloween gathering','planning the route and the costumes helps everyone stay comfortable','we check that costumes allow clear vision and choose a well-lit route','clear choices make sharing treats more considerate','we keep ingredient information available and offer a non-food option','We check our costumes. We can see and walk safely.','We offer a small toy as well as candy. Our guests can choose.',[('mask','candy'),('costume','pumpkin'),('decorate','superstition'),('folklore','ritual'),('uncanny','commemoration'),('liminal','syncretism')],'halloween-costume')),
('2026-11-26',6,topic('thanksgiving','A Thanksgiving table with space to listen','Thanksgiving','share a Thanksgiving meal','at a Thanksgiving gathering','dividing the work makes hosting manageable','we agree beforehand who will cook and who will clear the table','gratitude becomes more meaningful when it is specific','we name a particular kindness and listen to what mattered to another person','We share the work. One person cooks and another clears the table.','We thank someone for a kind action. We listen to their story.',[('plate','guest'),('gratitude','harvest'),('volunteer','invite'),('hospitality','portion'),('convivial','solicitude'),('commensality','reciprocity')],'meal')),
('2026-12-25',6,topic('christmas','A Christmas celebration shaped by care','Christmas','prepare a Christmas gathering','at a Christmas gathering','a modest plan protects time for people rather than purchases','we agree on a small gift budget and reuse wrapping materials','asking about traditions helps guests feel respected','we explain our own customs while leaving room for guests to take part differently','We choose a small gift. We use paper again.','We ask what our guests enjoy. We leave time to talk.',[('gift','tree'),('wrap','ornament'),('tradition','generosity'),('custom','charitable'),('communal','reciprocity'),('commensality','pluralism')],'christmas'))
]
# Communal is already a useful extension, recorded explicitly rather than guessed.
if 'communal' not in reference:
 reference['communal']=['communal','kəˈmjunəl','adjective','shared; collective','The communal meal brings neighbors together.']
 (ROOT/'content/word-reference.tsv').write_text('\n'.join('|'.join(reference[k]) for k in sorted(reference))+'\n')
 for _,_,t in holidays:
  for row in t['words']:
   for i in [0,2]:
    if row[i]=='communal':row[i+1]='shared or used by a group of people'
for _,_,t in holidays:
 for row in t['words']:
  assert row[1] and row[3],row
scheduled={}
for eventday,lead,t in holidays:
 eventdate=date.fromisoformat(eventday)
 for before in range(lead,-1,-1):scheduled[(eventdate-timedelta(days=before)).isoformat()]=(t,lead-before,eventday)
original_days={'2026-10-11','2026-10-12','2026-10-25'}
created=0;seasonal=0;dates=[];d=date(2026,1,1)
while d.year==2026:
 day=d.isoformat();dates.append(day);p=D/'data/english-levels'/f'{day}.json'
 if day in scheduled and day not in original_days:
  t,stage,eventday=scheduled[day]
  if p.exists():
   revision=ROOT/'content/lesson-revisions'/p.name
   if not revision.exists():save(revision,json.loads(p.read_text()))
  units={level:make_unit(day,t,i,stage%7) for i,level in enumerate(LEVELS)}
  for li,(level,u) in enumerate(units.items()):
   u['holiday']=t['event'];u['eventDate']=eventday;u['theme']=t['title']+' · '+STAGES[stage%7]
   for c in u['cards']:
    c['holiday']=t['event']
    if c['type']=='phrases':
     # Keep the taught sense, with the occasion named explicitly in the exercise.
     c['example']=c['example'].rstrip('.')+' as we prepare for '+t['event']+'.' if c['title'] in ['get ready','find out'] else c['example']
     c['exercise']='For '+t['event']+', '+c['exercise'][0].lower()+c['exercise'][1:]
    if c['type']=='smalltalk':
     c['title']='What would you like to do for '+t['event']+'?'
     c['conversation']='A: '+c['title']+'\nB: I would like to '+t['action']+'.\nA: What should we prepare?\nB: For example, '+t['example1']+'.'
    if c['type']=='grammar':
     examples=[('We prepare for '+t['event']+'. She prepares a small activity.','Choose: She prepare / prepares a small activity.','prepares'),('We are going to '+t['action']+'.','Complete: We ___ going to '+t['action']+'.','are'),('If we plan together, we will have more time to '+t['action']+'.','Complete: If we plan together, we ___ have more time.','will'),('Although the preparations took time, we enjoyed '+t['event']+'. Despite the extra work, we had time to talk.','Choose: Although / Despite the extra work, we had time to talk.','Despite'),('Only then did we realize what our guests needed for '+t['event']+'.','Complete: Only then ___ we realize what our guests needed.','did'),('Useful as our plan for '+t['event']+' was, it did not anticipate every preference.','Rewrite using concessive fronting: Although our plan was useful, it had limits.','Useful as our plan was, it had limits.')]
     c['example'],c['exercise'],c['answer']=examples[li]
  save(p,units);seasonal+=1
 elif not p.exists():
  week=(d-date(2026,1,1)).days//7
  topic=TOPICS[week%len(TOPICS)];stage=(d-date(2026,1,1)).days%7
  units={level:make_unit(day,topic,i,stage) for i,level in enumerate(LEVELS)}
  save(p,units);created+=1
 d+=timedelta(days=1)
index=dict(dates=dates,levels=LEVELS,fromDate='2026-01-01',through='2026-12-31',design='Stored graded curriculum with seven practice lenses, spaced review and seasonal units.')
save(D/'data/english-levels-index.json',index)
(D/'english-calendar.js').write_text('/* Stored daily editions. No content generation service. */\nwindow.JR_ENGLISH_DATA={};\nwindow.JR_ENGLISH_DATES='+json.dumps(dates)+';\n')
cal=json.loads((D/'data/calendar-index.json').read_text());cal.update(english=dates,englishCardCount=365*66);save(D/'data/calendar-index.json',cal)
save(ROOT/'content/holiday-calendar.json',[dict(date=eventday,leadDays=lead,**t) for eventday,lead,t in holidays])
save(ROOT/'content/year-coverage-audit.json',dict(days=365,levels=6,cardsPerLevel=11,cards=365*66,newDates=created,seasonalDates=seasonal,preservedOriginalDates=sorted(original_days),holidayCalendarSources=['https://www.timeanddate.com/calendar/?year=2026&country=1','https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/']))
print('Year prepared:',365*66,'cards;',created,'new dates;',seasonal,'seasonal dates')
