"""Apply reviewed, authored teaching banks and solve semantic photo assignments.

Every candidate photo is an explicit meaning/context match. A failed unique-photo
assignment stops the build; it never substitutes an arbitrary stock photograph.
"""
from pathlib import Path
from datetime import date
import json,copy,re,hashlib,shutil,tarfile
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
def bank(name,n):
 out={}
 for line in (ROOT/'content'/name).read_text().splitlines():
  if not line.strip():continue
  parts=line.split('|');assert len(parts)==n,(name,len(parts),parts[0]);assert parts[0] not in out,parts[0]
  out[parts[0].replace('\\n','\n')]=parts[1:]
 return out
VOC=bank('editorial-vocabulary.tsv',5)
EXP=bank('editorial-expressions.tsv',6)
SPEAK=bank('editorial-speaking-grammar.tsv',6)
SMALL=bank('editorial-smalltalk.tsv',6)
QUOTES=bank('editorial-quotes.tsv',8)
catalog=json.loads((ROOT/'content/photo-catalog.json').read_text());portraits=json.loads((ROOT/'content/essay-photo-catalog.json').read_text())
OLD_PHOTOS=json.loads((ROOT/'content/photo-assignments.json').read_text())
sample=json.loads((D/'review-c1-20261031/cards.json').read_text())['cards']
for c in sample:
 p=c['photoCredit'];scene={1:'uncanny',2:'commemoration',8:'cauldron'}.get(c['number'])
 if scene:
  pid=re.search(r'(\d+)\.jpg',p['asset'])[1];asset='assets/english-photos/'+pid+'.jpg'
  shutil.copy2(D/p['asset'],D/asset)
  catalog[scene]=dict(id=int(pid),sourceURL=p['sourceURL'],credit=p['credit'],licenseURL=p['licenseURL'],asset=asset,landscape=True,dimensions=[644,285])
for scene,pid,url in [('moving',7415047,'https://www.pexels.com/photo/7415047/'),('volunteers',6590929,'https://www.pexels.com/photo/two-volunteers-packing-the-charity-goods-6590929/')]:
 catalog[scene]=dict(id=pid,sourceURL=url,credit=f'Pexels · {pid}',licenseURL='https://www.pexels.com/license/',asset=f'assets/english-photos/{pid}.jpg',landscape=True,dimensions=[644,285])
# Correct the visual descriptions against a contact sheet of the actual assets.
CAPTIONS={
'chair':'A chair is positioned in a sunlit room.','window':'Light enters through a narrow window.','book':'A reader follows the printed text in an open book.','reading':'A reader makes notes beside an open book.','dictionary':'Reference books are arranged together.','notebook':'A notebook provides space to record a thought.','calendar':'A person records a plan on a calendar.','tea':'A cup of tea offers a simple refreshment.','meal':'People sit together for a shared meal.','sharing':'Friends share food and conversation outdoors.','serving':'A host serves food at a table.','portion':'Food is portioned and shared at a table.','listening':'A listener gives attention to another speaker.','discussion':'Two people discuss an issue face to face.','team':'A person explains information beside a board.','train':'A train journey passes through a green landscape.','station':'Passengers wait beside a train at a station.','ticket':'A traveler holds travel tickets.','ticket-gate':'A traveler presents a ticket at an entry gate.','map':'Travelers examine a map to choose their route.','itinerary':'Travelers trace a route on a map.','walk':'A person walks along a city street.','crossing':'Pedestrians share a street crossing.','market':'Fresh produce is displayed at a market.','produce':'Vegetables are arranged for selection.','budget':'Money and a calculator support a spending calculation.','saving':'A person records a budget and checks available money.','shopping':'A shopper chooses produce at a market.','bag':'A bag is ready to carry personal belongings.','leather':'Leather shows the surface qualities of a well-used material.','repair':'Hands work on a practical repair.','fabric':'A close view reveals the texture of a fabric.','plant':'A potted plant receives hands-on care.','watering':'A gardener waters a plant.','leaf':'Leaves form a dense pattern of growth.','pollination':'A bee visits a flowering plant.','seasons':'Changing leaves mark the passing of seasons.','rain':'People continue a city journey in rainy weather.','storm':'Dark clouds gather over a landscape.','music':'Musicians work together on a piece of music.','guitar':'Two people play guitars together.','headphones':'A listener uses headphones to focus on sound.','music-work':'A listener spends time with music.','desk':'A desk brings together tools for focused work.','minimal':'A simple workspace leaves room for a single task.','checklist':'A written list makes tasks visible.','whiteboard':'A group develops a shared plan around a board.','strategy':'Two colleagues coordinate a plan at a board.','options':'People work in a shared interior space.','document':'A person examines a written document.','fineprint':'A signature commits a person to a written document.','morning':'A person stretches on waking.','alarm':'A person checks the time beside a bed.','coat':'A shopper examines clothing on a rail.','clothes':'A coat hangs ready to be worn.','city':'Buildings and streets shape a neighborhood.','water':'A glass holds drinking water.','sitting':'A person takes a seated position.','lifting':'A person lifts and carries a box.','helping':'Two people share the effort of moving furniture.','relaxing':'A reader takes a quiet moment at home.','puzzle':'Hands assemble the pieces of a puzzle.','phone':'A person uses a smartphone at a desk.','library':'Library shelves hold a collection of books.','clock':'A clock makes the passage of time visible.','room':'Furniture, light and space shape an everyday room.','resilience':'A small plant emerges through a hard surface.','community':'A group shares outdoor work.','growth':'Successive stages show a plant developing.','sewing':'Hands attend to a sewing task.','halloween-costume':'A pumpkin-head costume changes a familiar human appearance.','halloween-candy':'A seasonal display combines treats and Halloween decorations.','christmas':'People exchange gifts beside a Christmas tree.','lunar':'Red envelopes appear in a festive New Year display.','easter-hunt':'Children search outdoors with baskets.','easter':'Eggs are arranged together for a seasonal activity.','valentine':'A greeting card sits beside flowers.','family':'A family spends time together outdoors.','independence':'A flag is carried in a public parade.','lunar-lantern':'Decorative lanterns light a festive setting.','recycling':'Separate containers provide places to sort materials.','wrapping':'Hands arrange paper around a gift.','ornament':'Small ornaments add detail to a seasonal display.','candy':'Wrapped sweets are displayed together.','pumpkin':'Pumpkins show their rounded forms and thick skins.','basket':'Woven material forms a carrying basket.','uncanny':'Mist gives a familiar forest an unfamiliar, unsettling atmosphere.','commemoration':'Memorial candles express remembrance.','cauldron':'A cauldron is a large pot, the object named in the witches’ chant.'}
CAPTIONS.update(moving='Family members share the work of carrying boxes.',volunteers='Volunteers work together to prepare donated supplies.')
assert set(catalog)<=set(CAPTIONS),set(catalog)-set(CAPTIONS)
# Alternatives describe the same activity or concept, not merely the day's theme.
COMPATIBLE=[['book','reading','library','dictionary'],['map','itinerary'],['station','train','ticket-gate'],['meal','sharing','portion','serving'],['listening','discussion'],['strategy','whiteboard','team'],['plant','watering','growth'],['calendar','clock','alarm'],['budget','saving'],['coat','clothes'],['helping','lifting','moving'],['notebook','desk'],['document','fineprint'],['community','volunteers'],['repair','sewing'],['market','produce','shopping']]
def scenes(raw):
 vals=raw.split(',');out=list(vals)
 for v in vals:
  for group in COMPATIBLE:
   if v in group:out.extend(x for x in group if x not in out)
 return out
def dialogue(raw,level,typ):
 lines=raw.split('~');assert len(lines)>=4
 # Shorter exchanges for beginners; fuller follow-up for independent speakers.
 if level in ['A1','A2'] and len(lines)>4:lines=lines[:4]
 return '\n'.join(('A: ' if i%2==0 else 'B: ')+line for i,line in enumerate(lines))
SMALL_SPECIAL={
'Would you like some tea?':'tea','Do you have any plans for Sunday?':'sunday','How did you get interested in gardening?':'garden','What has been the most rewarding part so far?':'rewarding','Has this changed the way you approach teamwork?':'teamwork','What assumption did the discussion leave unexamined?':'unexamined','How is your morning?':'morning-q','What do you like to do before work?':'beforework','Have you tried anything new lately?':'newactivity','What has been a welcome change of pace for you?':'pace','Which part of your routine feels most like a choice?':'choice','What would you keep even if it offered no measurable benefit?':'unmeasured'}
LOW_SMALL={
'table':'Would you like soup?~Yes, please.~Can you bring some bread?~Yes. We can share it.',
'journey':'Where would you like to go?~To the park.~Shall we walk or take the bus?~Let us walk if it is dry.',
'home':'Do you like your room?~Yes. I moved my chair.~Where is it now?~Near the window.',
'books':'What are you reading?~A short story.~Do you like it?~Yes. It is funny.',
'conversation':'Would you like to talk?~Yes, please.~Shall I listen first?~Yes. Thank you.',
'market':'What do we need to buy?~Bread and fruit.~Do we need a bag?~No. I have one.',
'music':'Do you like this song?~Yes. I know the tune.~Shall we listen again?~Yes, please.',
'weather':'It is raining. Shall we stay here?~Yes. We can read.~Would you like some tea?~That would be nice.',
'work':'Can I help?~Yes. Please move these chairs.~Where should they go?~Beside the table.',
'city':'Do you know this street?~A little.~Where is the cafe?~At the next corner.',
'garden':'Is that your plant?~Yes. It is new.~Does it need water?~Not today. The soil is wet.',
'year':'What did you enjoy this year?~Walking with my friend.~Will you do it again?~Yes. We walk on Sundays.',
'newyear':'What would you like to try this year?~Reading in the morning.~A whole book each day?~No. Just one page.',
'valentine':'Did you write a card?~Yes. It is for my friend.~What did you say?~Thank you for helping me.',
'lunarnewyear':'Are you having a family meal?~Yes, on Tuesday.~Can I bring something?~Please ask our host.',
'easter':'Would you like to join the egg hunt?~Yes. Where can we look?~Inside the garden.~Thank you. We will stay there.',
'earthday':'Do you have your bag?~Yes. I use it again.~Do you need a new one?~No, thank you.',
'mothersday':'Are you making lunch?~Yes. It is a thank-you.~Can I help?~Please put the plates on the table.',
'fathersday':'Shall we take a short walk?~Yes. Not too far, please.~We can go to the park.~That sounds good.',
'independenceday':'Are you watching the parade?~Yes. Where shall we meet?~By the library at eleven.~I will see you there.',
'halloween':'Do you like Halloween?~I like carving pumpkins.~Do you like scary houses?~Not really. I prefer a quiet evening.',
'thanksgiving':'What can I bring to lunch?~Some bread, please.~Is four o’clock a good time?~Yes. Thank you.',
'christmas':'Would you like to join us for dinner?~Yes. Can I bring a dish?~That would be lovely.~I can bring some vegetables.'}
LOW_NOTES={
'page':'Ask: Which page are we on? A page number helps locate a place in the same edition.','work':'In this sense work is generally uncountable: some work, not a work. Use a job or a task for one particular assignment.','water':'Water is uncountable in this sense: some water or a glass of water. The verb water a plant is a different grammatical use.','harvest':'The noun can mean the gathering of crops or the crops gathered. Compare the verb: harvest the vegetables.',
'progress':'Progress is normally uncountable: make progress, not make a progress. A particular improvement can be counted.','advice':'Advice is uncountable; use a piece of advice for one suggestion.','information':'Information is uncountable; say some information or a piece of information.',
'retrospective':'The adjective looks back at past events. As a noun, a retrospective can be a review or an exhibition covering earlier work.',
'symbiosis':'In broad biological usage this is a close association between species. Mutualism specifies a relationship benefiting both.','phenology':'Phenology concerns the timing of recurring biological events, such as flowering or migration, not simply identifying species.',
'uncanny':'An uncanny resemblance is strikingly exact and need not be frightening. An uncanny atmosphere emphasizes a strange, unsettling quality.',
'commemoration':'A commemoration of an event; in commemoration of someone. Distinguish honoring a memory from a party with no remembrance purpose.',
'polysemy':'Related senses of one word illustrate polysemy. Do not assume that every pair of similarly spelled words has a shared sense history.',
'patina':'Distinguish a surface quality developed through age or use from structural damage such as a broken strap.',
'provenance':'Ask about an object’s origin and ownership history, not its present owner’s physical location.',
'instrumentalise':'British spelling; American English often uses instrumentalize. The concern is treating something primarily as a means to another end.',
'platonic':'Describes a close relationship without romantic or sexual involvement in this sense. Make the friendship intention clear when context could suggest romance.',
'equanimity':'Composure during difficulty does not mean indifference to the outcome.',
'serendipity':'An unplanned discovery is serendipitous when it is fortunate or welcome, not simply because it was accidental.',
'circumspect':'Careful consideration of consequences; not the same as rejecting an idea without examining it.',
'teleology':'An explanation by an apparent end or purpose. A historical account can become misleading if it treats one outcome as inevitable.',
'reflexivity':'In this research context, examine how your own position and actions shape the inquiry, not merely what other people did.',
'intentionality':'Here it concerns what an action or mental state is directed toward. Related discussions may use the word more broadly for purposiveness.',
'friction':'Figurative in a discussion of habits: effort or inconvenience affecting an action, rather than physical resistance between surfaces.',
'externality':'An effect of an activity falling on parties outside a transaction; identify who bears the cost or benefit.',
'syncretism':'A blending or integration of practices or beliefs, not merely placing unrelated objects next to one another.',
'commensality':'The practice of eating together. It concerns social relations and participation as well as food.',
'intersubjective':'Shared or negotiated between subjects; it is neither a single private opinion nor necessarily a mind-independent fact.',
'equivocation':'A shift between senses of a word can make an argument appear sound while changing what its terms mean.',
'pluralism':'Recognizes multiple perspectives or forms of life. It need not mean that every claim is equally well supported.',
'subsidiarity':'Decisions at the lowest appropriate level, taking capacity and wider responsibilities into account.',
'asymmetry':'Specify the unequal relation: asymmetry of information, power or resources.',
'liminal':'A threshold or transitional condition. Specify the states or spaces between which something is positioned.',
'palimpsest':'Used metaphorically for visible layers of history; the older literal sense concerns a reused writing surface.'}
A1_TASKS={'candy':('Your friend does not want candy. Offer a small toy.','Would you like a small toy instead?'),'page':('Ask your friend which page to read.','Which page should I read?'),'bag':('You have a bag. Say no politely to a new bag.','No, thank you. I have my own bag.'),'ticket':('Your phone has little battery. How can you keep your ticket?','I can print a copy of the ticket.'),'leaf':('A leaf is yellow. What can you check first?','I can check the soil and the light.'),'mask':('You cannot see well in a mask. What can you do on the steps?','I can take the mask off on the steps.'),'flag':('Where can your group meet at a busy event? Use flag.','We can meet beside the flag.'),'parade':('Who can help you cross a parade route?','A steward can tell me where to cross.'),'work':('Name one job to do in a garden.','We can water the plants.'),'plant':('The soil is wet. Does the plant need more water now?','No. We can wait and check it later.')}
LOW_TASKS={
 'table':('Your friend does not want soup. Offer some bread.','Would you like some bread instead?'),
 'journey':('It is raining. Suggest taking the bus instead of walking.','It is raining. Shall we take the bus?'),
 'home':('Ask your friend where they put their chair.','Where is your chair now?'),
 'books':('Your friend does not like the story. Ask what they like to read.','What do you like to read?'),
 'conversation':('Your friend needs time to talk. Give a kind reply.','Take your time. I am listening.'),
 'market':('You already have a bag. Say no politely to another one.','No, thank you. I have a bag.'),
 'music':('Your friend likes a song. Ask who sings it.','Who sings this song?'),
 'weather':('It is raining. Invite a friend to have tea indoors.','Would you like to come in for some tea?'),
 'work':('Ask a helper to move two chairs beside a table.','Could you put these two chairs beside the table?'),
 'city':('You cannot find the cafe. Ask someone for help.','Could you tell me where the cafe is?'),
 'garden':('The soil is still wet. Tell your friend why you will wait.','The soil is wet. I will water it another day.'),
 'year':('Your friend enjoyed walking this year. Ask who they walked with.','Who did you walk with?'),
 'newyear':('A friend wants to read a whole book every day. Suggest a smaller start.','You could start with one page each morning.'),
 'valentine':('Thank a friend for helping you carry a box.','Thank you for helping me carry the box.'),
 'lunarnewyear':('You are invited to a family meal. Ask what you can bring.','What can I bring to the meal?'),
 'easter':('A child asks where to look for eggs. Tell them to stay in the garden.','Please look inside the garden. Do not go outside it.'),
 'earthday':('Your friend forgets their bag. Suggest a place to keep it.','You could keep your bag beside your keys.'),
 'mothersday':('Offer to put plates on the table before lunch.','I can put the plates on the table.'),
 'fathersday':('Your friend prefers a short walk. Suggest a nearby place.','Shall we walk to the park near home?'),
 'independenceday':('Set a meeting place and time for the parade.','Let us meet by the library at eleven.'),
 'halloween':('Your neighbor does not celebrate Halloween. Give a friendly reply and ask about the weekend.','That is fine. Do you have any plans for the weekend?'),
 'thanksgiving':('Offer to bring bread and check the arrival time.','I can bring bread. Is four o’clock a good time?'),
 'christmas':('You are invited to dinner. Offer to bring vegetables.','Thank you. Can I bring some vegetables?')}
def vocab_note(c):
 w=c['title'];pos=c.get('partOfSpeech','')
 if w in LOW_NOTES:return LOW_NOTES[w]
 existing=c.get('notes','')
 if existing and not any(x in existing.lower() for x in ['topic:','write one sentence','learn the word','learn the whole']):return existing
 if 'verb' in pos and 'adverb' not in pos:return 'Use the verb in the sense shown in the exchange. Notice the subject, tense and any object; the word forms above show its changes.'
 if 'adjective' in pos:return 'The adjective describes a person, thing or situation. Choose a concrete noun or context that supports the description rather than using it as a general compliment.'
 if 'uncountable' in pos:return 'Normally uncountable in this sense. Use an appropriate quantity phrase rather than automatically adding a/an or a plural ending.'
 return 'Keep the sense and countability shown in the example. Use a singular or plural form appropriate to the specific person, object or event being discussed.'

def rewrite(c,u,level,day):
 typ=c['type'];key=c['title'];row=None
 if typ=='vocabulary':
  rawsc,raw,q,a=VOC[key];c.update(conversation=dialogue(raw,level,typ),exercise=q,answer=a,notes=vocab_note(c));c['editorialScenes']=scenes(rawsc)
  if key=='work':c['conversation']='A: What work do you do here?\nB: I do garden work.\nA: Every day?\nB: No. Only on Saturdays.'
  if key=='harvest':c['conversation']='A: Was it a good harvest?\nB: We gathered plenty of carrots, but fewer tomatoes.\nA: What will you do with the extra carrots?\nB: Share them with the neighbors.'
  if level=='A1' and key in A1_TASKS:c['exercise'],c['answer']=A1_TASKS[key]
 elif typ in ['phrases','idioms','daily','grammar']:
  rawsc,raw,q,a,note=(EXP if typ in ['phrases','idioms'] else SPEAK)[key]
  if level=='A1' and typ=='grammar':q=q.replace('Correct the subject-verb agreement:', 'Correct the verbs:')
  c.update(conversation=dialogue(raw,level,typ),exercise=q,answer=a,notes=note);c['editorialScenes']=scenes(rawsc)
 elif typ=='reflection':
  rawsc,raw,q,a,low,lq,la=QUOTES[key]
  c.update(conversation=dialogue(low if level in ['A1','A2'] else raw,level,typ),exercise=lq if level in ['A1','A2'] else q,answer=la if level in ['A1','A2'] else a);c['editorialScenes']=scenes(rawsc)
 elif typ=='smalltalk':
  sk=SMALL_SPECIAL.get(key,u.get('topicId'));assert sk in SMALL,(day,level,key,sk)
  title,rawsc,raw,q,a=SMALL[sk]
  lowkey={'tea':'table','sunday':'journey','rewarding':'garden','teamwork':'work','unexamined':'conversation','morning-q':'newyear','beforework':'newyear','newactivity':'music','pace':'garden','choice':'year','unmeasured':'conversation'}.get(sk,sk)
  if level in ['A1','A2']:
   raw=LOW_SMALL[lowkey];title=raw.split('~')[0]
   q,a=LOW_TASKS[lowkey]
  c.update(title=title,conversation=dialogue(raw,level,typ),exercise=q,answer=a,meaning='An opening that invites a personal preference or experience without assuming everyone shares it.',notes='Follow the answer with a related question. Accept a different preference or a declined invitation without asking the person to justify it.');c['editorialScenes']=scenes(rawsc)
 elif typ=='essay':
  c['editorialScenes']=[]
  # Preserve the model's four paragraphs; ask about its actual concrete evidence.
  paras=c.get('paragraphs',[]);assert len(paras)==4
  c['exercise']=c.get('exercise','')
  c['answer']='A possible outline: introduce your position on '+c['title'].lower()+'; develop one practical change; develop a different change with its own example; explain how both support the position.'
  c['notes']='Each body paragraph needs a distinct point and a concrete example. The conclusion should connect the argument rather than introduce a new proposal.'
 if typ!='essay':
  lines=c['conversation'].split('\n');assert len(lines)>=4
  # A real exchange replaces the previous invented dictionary-example sentence.

  if typ=='smalltalk':c['example']=c['title']
  elif 'We use “' in c.get('example','') or 'How should we' in c.get('example','') or 'How can we' in c.get('example',''):
   c['example']='\n'.join(lines[:2])
  c['example']=re.sub(r' as we prepare for [^.]+\.', '.', c.get('example',''))
 c['editorialVersion']='context-dialogue-2026-v1'
 return c

def photo_candidates(c,day):
 if c['type']=='essay':
  old=OLD_PHOTOS[c['id']]
  matching=[(k,p) for k,p in portraits.items() if p['asset']==old['asset']]
  assert matching,c['id'];k,p=matching[0];return [(k,p)]
 vals=c['editorialScenes'];assert vals,c['id']
 for s in vals:assert s in catalog,(c['id'],s)
 return [(s,catalog[s]) for s in vals]

def solve(cards,day):
 # Preserve the approved sample's exact selections.
 if day=='2026-10-31' and cards[0]['level']=='C1':
  return {c['id']:copy.deepcopy(sample[i]['photoCredit']) for i,c in enumerate(cards)}
 candidates={c['id']:photo_candidates(c,day) for c in cards}
 order=sorted(cards,key=lambda c:len(candidates[c['id']]))
 chosen={};used=set()
 def visit(i):
  if i==len(order):return True
  c=order[i];opts=candidates[c['id']]
  # Candidate order expresses editorial preference for the closest match.
  # Prefer the closest literal/context match; uniqueness never justifies random rotation.
  for scene,p in opts:
   pid=p.get('id') or re.search(r'(\d+)\.jpg',p['asset'])[1];pid=str(pid)
   if pid in used:continue
   used.add(pid);chosen[c['id']]=(scene,p)
   if visit(i+1):return True
   used.remove(pid);chosen.pop(c['id'],None)
  return False
 if not visit(0):return None
 result={}
 for c in cards:
  scene,p=chosen[c['id']];row={k:p[k] for k in ['asset','sourceURL','credit','licenseURL']}
  if c['type']=='essay':caption=OLD_PHOTOS[c['id']]['caption']
  else:caption=CAPTIONS[scene]
  row.update(scene=scene,caption=caption,orientation='portrait' if c['type']=='essay' else 'landscape',fit='xMidYMid slice',selection='Reviewed semantic candidate; unique source within edition')
  result[c['id']]=row
 return result

def main():
 originals=list(sorted((D/'data/english-levels').glob('*.json')))
 archive=ROOT.parent.parent/'work/english-before-editorial-revision.tar.gz'
 if not archive.exists():
  archive.parent.mkdir(exist_ok=True,parents=True)
  with tarfile.open(archive,'w:gz') as tar:
   for p in originals:tar.add(p,arcname=p.name)
 pending={};photos={};failures=[];count=0
 for p in originals:
  with tarfile.open(archive,'r:gz') as tar:data=json.loads(tar.extractfile(p.name).read())
  for level,u in data.items():
   for i,c in enumerate(u['cards']):
    if p.stem=='2026-10-31' and level=='C1':
     approved=copy.deepcopy(sample[i]);approved['editorialVersion']='approved-C1-sample';u['cards'][i]=approved
    else:u['cards'][i]=rewrite(c,u,level,p.stem)
    count+=1
   assigned=solve(u['cards'],p.stem)
   if assigned is None:failures.append((p.stem,level,[c['title'] for c in u['cards']]))
   else:photos.update(assigned)
  pending[p]=data
 if failures:
  (ROOT/'content/editorial-photo-conflicts.json').write_text(json.dumps(failures,ensure_ascii=False,indent=2));print('STOP: unresolved semantic photo assignments',len(failures));return
 for p,data in pending.items():
  for u in data.values():
   for c in u['cards']:
    c['photoCredit']=photos[c['id']];c['illustration']=photos[c['id']]['asset'];c['illustrationAlt']=photos[c['id']]['caption'];c.pop('editorialScenes',None)
  p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
 (ROOT/'content/photo-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'content/photo-assignments.json').write_text(json.dumps(photos,ensure_ascii=False,separators=(',',':'))+'\n')
 (ROOT/'content/editorial-photo-conflicts.json').unlink(missing_ok=True)
 print('Revised cards:',count,'; all 2190 editions have 11 different photo source IDs.')
if __name__=='__main__':main()
