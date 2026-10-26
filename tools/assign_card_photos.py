"""Explicit meaning/context photo assignments; no random or keyword fallback."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
catalog=json.loads((ROOT/'content/photo-catalog.json').read_text())
portrait_catalog=json.loads((ROOT/'content/essay-photo-catalog.json').read_text())
words={}
for line in (ROOT/'content/photo-word-scenes.tsv').read_text().splitlines():
 scene,heads,cue=line.split('|')
 for head in heads.split(','):
  assert head not in words,head
  words[head]=(scene,cue)
words.update({
'assumption':('options','An initial idea can be checked against the available alternatives.'),
'change':('map','A route can change when a traveler chooses a different direction.'),
'deliberate':('notebook','Writing down a choice gives time to consider it carefully.'),
'disruption':('rain','Rain can interrupt an outdoor plan.'),
'help':('helping','People help by sharing a physical task.'),
'prepare':('serving','Getting food ready is part of preparing a meal.'),
'realistic':('calendar','A workable plan allows enough time for each task.'),
'shelf':('library','Shelves keep books together and within reach of readers.'),
'attention':('listening','Listening closely means giving attention to another person.')
})
for line in (ROOT/'content/holiday-word-reference.tsv').read_text().splitlines():
 if line.strip():
  word,ipa,pos,syn,example,meaning,scene=line.split('|')
  if word in ['gift','wrap']:scene='wrapping'
  if word in ['candy','pumpkin','basket','ornament']:scene=word
  words[word]=(scene,{'halloween-costume':'Halloween dress can transform a familiar appearance.','halloween-candy':'A Halloween display includes treats and festive decorations.','christmas':'Gifts and decorations are part of this Christmas setting.','lunar':'Red envelopes are used in some Lunar New Year traditions.','lunar-lantern':'Decorative lanterns light a festival setting.','easter':'Eggs are arranged in a woven basket.','easter-hunt':'Children search for eggs in a garden.','valentine':'A handmade card expresses a personal greeting.','family':'A family spends time together.','independence':'Flags are carried in a public parade.','recycling':'Separate containers make waste sorting possible.','wrapping':'Hands fold material around a gift.','candy':'Individually wrapped sweets are displayed together.','pumpkin':'Orange pumpkins show their thick skins and rounded shapes.','basket':'A woven basket holds and carries things.','ornament':'Decorative objects add detail to a festive setting.'}.get(scene,example))
words['communal']=('sharing','People share an activity together.')
expressions={}
def group(scene,titles,cue):
 for title in titles.split('|'):expressions[title]=(scene,cue)
group('whiteboard','get the ball rolling','A planning session can set a shared project in motion.')
group('sitting','sit down','A person takes a seat.')
group('lifting','pick up','Lifting a box moves it up from its resting place.')
group('morning','get ready|wake up|a fresh start','A new day begins with getting up and preparing.')
group('dictionary','find out','Reference books help a reader discover information.')
group('puzzle','work out|a piece of cake','A puzzle provides a task to solve.')
group('document','look into|bear out|bear on|leave no stone unturned','Examining information helps someone check an explanation.')
group('checklist','follow through|get around to|stick to|default to|go through the motions|move the goalposts|the tail wagging the dog','A written task list makes actions and requirements visible.')
group('options','weigh up|hold in tension|strike a balance|meet halfway|a curate’s egg','Comparing alternatives helps clarify competing benefits and drawbacks.')
group('budget','factor in|account for|make allowance for|cut back on','A budget helps someone allow for costs and limits.')
group('strategy','iron out|stand back from|iron out the wrinkles|cut the Gordian knot','A shared planning session helps people reconsider and resolve a difficulty.')
group('minimal','dispense with|leave well enough alone|less is more','A simple arrangement leaves out unnecessary additions.')
group('bag','bring along','A bag carries the things someone takes with them.')
group('room','come in','An interior is a space someone can enter.')
group('coat','put on','A coat is clothing someone puts on before going outside.')
group('relaxing','slow down|take your time','A quiet pause creates room to proceed without rushing.')
group('puzzle','take turns','A shared activity can be completed one person at a time.')
group('calendar','make time for|set aside|carve out|lose sight of|spread yourself too thin','A calendar makes time, commitments and priorities visible.')
group('map','map out|play it by ear|see the wood for the trees','A map shows an overall route while leaving choices about the journey.')
group('discussion','check in with|break the ice','A conversation begins by making contact and listening.')
group('growth','build on|step by step|so far, so good','Growth happens through successive stages.')
group('helping','a big help|a helping hand|lend a hand|no problem','Sharing a practical task is a way to offer assistance.')
group('community','many hands make light work|pull your weight','People contribute their effort to a shared task.')
group('walk','a change of pace','A walk can provide a change from an indoor routine.')
group('phone','a double-edged sword','A phone offers useful tools but can also interrupt concentration.')
group('team','on the same page','Working together calls for a shared understanding.')
group('fineprint','the devil is in the detail|the devil is in the details','Small details in a document can have important consequences.')
topic={'table':'meal','journey':'map','home':'room','books':'reading','conversation':'discussion','market':'market','music':'music','weather':'rain','work':'team','city':'city','garden':'plant','year':'calendar'}
topic.update({'newyear':'calendar','valentine':'valentine','lunarnewyear':'lunar','easter':'easter','earthday':'plant','mothersday':'family','fathersday':'family','independenceday':'independence','halloween':'halloween-costume','thanksgiving':'meal','christmas':'christmas'})
legacy={
'Let’s make lunch together.':'meal','I can bring fruit if you bring bread.':'sharing',
'Could we agree on who will do each task?':'whiteboard','What would make this plan workable for everyone?':'team',
'Before we optimise the process, let’s clarify its purpose.':'strategy','Agreement is meaningful only when dissent remains possible.':'discussion',
'I have time for one small thing.':'calendar','I am trying to do one thing at a time.':'notebook',
'I would rather make a small change that I can keep.':'growth','I want my schedule to reflect what matters to me.':'calendar',
'The aim is to make the valued choice easier to repeat.':'checklist','A life cannot be judged solely by the efficiency of its arrangements.':'relaxing',
'A small act can make a good day.':'helping','A shared plan leaves more time to enjoy the day.':'calendar',
'Trust grows when small promises become actions.':'checklist','Clarity is a form of care in a shared project.':'whiteboard',
'Good collaboration makes disagreement usable.':'discussion','A collective voice should not erase the voices that compose it.':'discussion',
'A new day starts with one small step.':'morning','Small changes can make an ordinary day feel new.':'walk',
'The best routine leaves room for real life.':'calendar','Attention gives ordinary moments their texture.':'room',
'What we make convenient quietly shapes what we become.':'checklist','Some moments matter precisely because they ask for no return.':'relaxing',
'We + verb':'meal','Be going to + verb':'calendar','If + present, will + verb':'plant','If we had…, we could…':'team',
'Although / despite':'discussion','Not until… did…':'whiteboard','At + a time':'clock','Adverbs of frequency':'morning',
'Used to + verb':'notebook','Present perfect continuous':'plant','What-cleft sentences':'calendar','Were it not for…':'helping',
'Would you like some tea?':'tea','Do you have any plans for Sunday?':'calendar','How did you get interested in gardening?':'plant',
'What has been the most rewarding part so far?':'community','Has this changed the way you approach teamwork?':'team',
'What assumption did the discussion leave unexamined?':'discussion','How is your morning?':'morning',
'Have you tried anything new lately?':'walk','What do you like to do before work?':'morning',
'What has been a welcome change of pace for you?':'walk','Which part of your routine feels most like a choice?':'calendar',
'What would you keep even if it offered no measurable benefit?':'relaxing',
'Lunch with a friend':'meal','A picnic that works for everyone':'sharing','Growing something together':'plant',
'A good plan makes room for people':'team','Making disagreement productive':'discussion','The limits of consensus':'discussion',
'One quiet morning':'morning','Ten minutes for myself':'relaxing','A routine that fits':'calendar',
'Making room for what matters':'calendar','Designing a day with breathing room':'calendar','The unmeasured afternoon':'relaxing'}
scene_cues={
'meal':'People share a meal and conversation.', 'map':'Travelers look at a map to consider their route.',
'room':'Furniture, light and space shape an everyday room.', 'reading':'Readers spend time with books.',
'discussion':'People exchange their views in a conversation.', 'market':'Fresh food is displayed at a market.',
'music':'People make music together.', 'rain':'People continue their journey in rainy weather.',
'team':'People work together in a shared space.', 'city':'Buildings and streets form a city neighborhood.',
'plant':'A potted plant receives water and care.', 'calendar':'A calendar gives plans a place in time.',
'sharing':'People share food during an outing.', 'whiteboard':'A team uses a whiteboard to explain a plan.',
'strategy':'A shared planning session brings different perspectives together.',
'growth':'A plant develops through successive stages.', 'notebook':'A notebook provides space to record and reflect.',
'checklist':'A written list makes tasks and priorities visible.', 'relaxing':'A reader takes a quiet moment without rushing.',
'helping':'Two people share the effort of moving furniture.', 'morning':'A person wakes and stretches at the start of the day.',
'walk':'A person walks along a city street.', 'clock':'A clock shows the passage of time.',
'community':'People work together on a shared outdoor task.', 'tea':'A cup of tea offers a simple welcome.'}
scene_cues.update({'valentine':'A handmade greeting creates a personal message.','lunar':'Red envelopes are part of a Lunar New Year greeting.','easter':'Eggs are arranged together for a seasonal activity.','family':'A family spends time together.','independence':'A flag is carried at a public celebration.','halloween-costume':'A costume creates a playful Halloween character.','christmas':'Gifts and decorations mark a Christmas gathering.'})
specific={
'Could you help me, please?':('helping','People share the effort of moving something heavy.'),
'Could you explain that again?':('discussion','A conversation gives people a chance to ask for a clearer explanation.'),
'Let me check that I understand.':('whiteboard','A visual explanation can help people check a shared understanding.'),
'Would you mind if we considered another option?':('options','A shared decision can include considering another approach.'),
'I see your point, although I would qualify it slightly.':('discussion','A discussion can include both agreement and a reservation.'),
'I would distinguish between the intention and its consequences.':('document','A written proposal gives people something concrete to examine.'),
'Present simple':('morning','A morning routine provides a context for describing repeated actions.'),
'Going to for plans':('calendar','A calendar gives future intentions a place in time.'),
'First conditional':('map','An early departure can leave travelers more time for their journey.'),
'Although and despite':('rain','Rain provides a context for describing an obstacle and continuing anyway.'),
'Inversion after only then':('puzzle','Solving a problem can lead to a moment of understanding.'),
'Concessive fronting':('calendar','A useful plan can still leave circumstances unanticipated.')}
reflection_scenes=dict(topic,home='plant',work='whiteboard',year='notebook',city='walk',table='sharing')
result={};missing=[]
for p in sorted((D/'data/english-levels').glob('*.json')):
 for level,unit in json.loads(p.read_text()).items():
  for c in unit['cards']:
   title=c['title'];typ=c['type'];tid=c.get('topicId')
   if typ=='vocabulary':pair=words.get(title)
   elif typ in ['phrases','idioms']:pair=expressions.get(title)
   elif typ in ['daily','reflection','grammar','smalltalk','essay'] and c.get('holiday'):
    scene=topic[tid];pair=(scene,scene_cues[scene])
   elif c.get('visualPhotoScene'):
    scene=c['visualPhotoScene'];pair=(scene,scene_cues.get(scene,catalog[scene]['description']))
   elif title in specific:pair=specific[title]
   elif typ=='reflection' and tid in reflection_scenes:
    scene=reflection_scenes[tid];pair=(scene,scene_cues[scene])
   elif tid in topic:
    scene=topic[tid];pair=(scene,scene_cues[scene])
   elif title in legacy:
    scene=legacy[title];pair=(scene,scene_cues[scene])
   else:pair=None
   if not pair:missing.append((typ,title));continue
   scene,cue=pair
   if c['id']=='2026-10-25-A1-9':scene,cue='clothes','Putting belongings away is part of keeping a room tidy.'
   photo=catalog[scene]
   if typ=='essay':
    portrait_scene={'sharing':'meal','whiteboard':'team','strategy':'team','relaxing':'reading','minimal':'room'}.get(scene,scene)
    photo=portrait_catalog[portrait_scene]
    cue={'plant':'Hands cultivate a garden with care.','music':'A musician holds a guitar.','morning':'A quiet morning can begin with a cup of coffee.'}.get(portrait_scene,cue)
    assert photo.get('portrait'),portrait_scene
   else:assert photo.get('landscape'),scene
   result[c['id']]={k:photo[k] for k in ['asset','sourceURL','credit','licenseURL']}
   result[c['id']].update(scene=scene,orientation='portrait' if typ=='essay' else 'landscape',caption=cue,fit='xMidYMid slice',selection='Explicit meaning or lesson-context match')
assert not missing,sorted(set(missing))
(ROOT/'content/photo-assignments.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
(ROOT/'content/photo-coverage-audit.json').write_text(json.dumps({'cards':len(result),'scenes':len(set(x['scene'] for x in result.values())),'missing':0,'landscapeCards':sum(x['orientation']=='landscape' for x in result.values()),'portraitEssays':sum(x['orientation']=='portrait' for x in result.values()),'landscapeSize':[644,285],'essayPhotoSize':[320,480],'scaling':'Aspect-preserving cover crop; no stretching'},indent=2)+'\n')
print('Assigned',len(result),'cards')
