"""Prepare stored daily editions. No network, generation API, or old-file deletion.
Uses a deliberately labelled spiral curriculum: twelve themes revisited with
new practice prompts; review is not represented as newly authored source text.
"""
from pathlib import Path
from datetime import date,timedelta
import json,copy,hashlib
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
TOPICS=json.loads((ROOT/'content/course-topics.json').read_text())
LEVELS=['A1','A2','B1','B2','C1','C2'];START=date(2026,10,6);END=date(2026,12,31)
s=(DIST/'english-levels-data.js').read_text();ORIGINAL=json.loads(s[s.index('{'):s.rindex('}')+1])
PHRASES=[
 [('sit down','take a seat','Please sit down here.'),('pick up','lift something','Please pick up the bag.')],
 [('get ready','prepare yourself','We get ready before we leave.'),('find out','learn a fact','Let us find out what we need.')],
 [('work out','find a solution','We can work out a plan together.'),('look into','examine or investigate','We should look into another option.')],
 [('follow through','complete what you have agreed to do','A good plan matters only if we follow through.'),('weigh up','consider advantages and disadvantages','We weigh up the choices before deciding.')],
 [('factor in','include something when making a judgement','We factor in the time other people need.'),('iron out','resolve small difficulties','We can iron out the details before we begin.')],
 [('bear out','support or confirm a claim','The experience did not bear out our initial assumption.'),('dispense with','manage without something unnecessary','We can dispense with a rule that serves no useful purpose.')]
]
IDIOMS=[
 [('a helping hand','help from another person','Can you give me a helping hand?'),('take your time','do something without hurrying','Take your time; we can wait.')],
 [('on the same page','in agreement or sharing an understanding','Are we on the same page about the plan?'),('a piece of cake','something very easy; informal','The first step was a piece of cake.')],
 [('play it by ear','decide what to do as events develop','We have a rough plan, but we can play it by ear.'),('get the ball rolling','start an activity','One question can get the ball rolling.')],
 [('strike a balance','find a suitable middle position','We need to strike a balance between planning and freedom.'),('leave no stone unturned','try every reasonable possibility','We left no stone unturned while looking for a solution.')],
 [('the devil is in the details','small details can cause important difficulties','The broad idea is sound, but the devil is in the details.'),('a double-edged sword','something with both benefits and disadvantages','A fixed routine can be a double-edged sword.')],
 [('cut the Gordian knot','solve a complex problem with a decisive and direct action','A simpler agreement cut the Gordian knot.'),('a curate’s egg','something with both good and bad parts; chiefly British','The elaborate arrangement was a curate’s egg.')]
]
GRAMMAR=[('Present simple','Use the base verb after I, you, we and they. Add -s or -es after he, she and it.','We make a plan. She makes a plan.','Choose: She make / makes a plan.','makes'),('Going to for plans','Use am, is or are + going to + base verb for an intended future action.','We are going to make a plan.','Complete: We ___ going to make a plan.','are'),('First conditional','Use if + present simple and will + base verb for a possible future result.','If we leave early, we will have more time.','Complete: If we leave early, we ___ have more time.','will'),('Although and despite','Use although before a clause. Use despite before a noun or an -ing form.','Although it was difficult, we continued. Despite the difficulty, we continued.','Choose: Despite / Although the difficulty, we continued.','Despite'),('Inversion after only then','Put an auxiliary before the subject when Only then begins a sentence in this pattern.','Only then did we understand the problem.','Complete: Only then ___ we understand the problem.','did'),('Concessive fronting','An adjective can precede as + subject + verb to concede a point in formal writing.','Useful as the plan was, it could not anticipate every circumstance.','Rewrite with concessive fronting: Although the plan was useful, it had limits.','Useful as the plan was, it had limits.')]
STAGES=['Notice','Understand','Use','Compare','Explain','Apply','Review']
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n')
def essay(t,li):
 r1,r2,e1,e2=t['reason1'],t['reason2'],t['example1'],t['example2'];act=t['action'];name=t['title']
 if li==0:return [f'I like to {act}. Two small things help me.',f'First, {t["simple1"]}',f'Next, {t["simple2"]}',f'These two things help us. We can {act} and enjoy our time together.']
 if li==1:return [f'When we {act}, a little care can make the experience better. Planning and thinking about other people both help.',f'First, {r1}. For example, {e1}. This is a small thing that makes the day easier.',f'Second, {r2}. For example, {e2}. We do not need a perfect day to do this well.',f'We can {act} more easily when we prepare and notice other people. These simple steps give us a useful place to start.']
 if li==2:return [f'There is more than one way to {act}. In my experience, practical preparation and attention to others are two useful starting points.',f'One reason is that {r1}. For instance, {e1}. This prevents a small difficulty from taking over the experience. It also leaves us more time to notice what is happening.',f'Another reason is that {r2}. For example, {e2}. This approach recognises that the experience belongs to more than one person and that different people may need different things.',f'These examples show why preparation and consideration work well together. We do not have to control every detail. We can make a sensible arrangement and remain ready to respond.']
 if li==3:return [f'A good way to {act} combines practical structure with an awareness of other people. Neither a rigid plan nor complete improvisation is sufficient on its own; both need to be judged in context.',f'The practical case is straightforward: {r1}. Consider how {e1}. The benefit is not merely efficiency. A modest arrangement prevents avoidable confusion, leaving attention available for the activity itself rather than for problems that could have been anticipated.',f'Consideration adds a second, equally important dimension: {r2}. In this situation, {e2}. A decision can be convenient for one person while creating difficulty for another, so its value depends partly on whose needs it recognises.',f'The most useful approach therefore brings structure and consideration together. Preparation establishes a workable starting point; attention to other people keeps it responsive. Success should be assessed by how well the arrangement serves the experience, rather than by how closely events follow the original plan.']
 if li==4:return [f'The decision to {act} may appear ordinary, yet it exposes a recurring tension between arrangements that make life manageable and experiences that resist being prescribed. A defensible approach combines proportionate preparation with a willingness to reconsider whose interests a plan serves.',f'Preparation has value because {r1}. In the present case, {e1}. Such an intervention is modest, but that modesty is its strength: it removes a foreseeable obstacle without claiming to determine the entire experience. Structure is useful to the extent that it releases attention rather than consuming it.',f'That argument requires a qualification, however: {r2}. For instance, {e2}. An arrangement that appears efficient from one standpoint may impose costs elsewhere. Listening to those affected is therefore not an optional gesture of goodwill; it supplies information without which the plan cannot be adequately evaluated.',f'The resulting principle is one of proportion. Preparation deserves support when it clarifies responsibilities and protects time, while responsiveness prevents it from hardening into an end in itself. To judge the experience well is to examine both what the arrangement enables and what it may inadvertently exclude.']
 return [f'To {act} is to negotiate a familiar but frequently obscured relationship between intentional design and the contingencies of shared experience. The question is not whether arrangements are desirable, but what authority they should acquire. A credible position supports preparation while withholding the assumption that procedural coherence is equivalent to human value.',f'There is a substantive case for structure: {r1}. Here, {e1}. The arrangement earns its legitimacy through the specific difficulty it alleviates, not through its conformity to an abstract ideal of order. Its success is consequently conditional. Once the intervention demands more attention than the obstacle it removes, the original justification begins to unravel.',f'An assessment confined to that practical benefit would nevertheless be incomplete, since {r2}. In concrete terms, {e2}. This introduces a problem of perspective: whose convenience supplies the standard against which improvement is measured? An apparently neutral procedure may privilege the preferences of its designer. Attentiveness to others makes that asymmetry visible and creates grounds for revision.',f'What emerges is a qualified defence of planning, rather than a celebration of either control or spontaneity. Arrangements can sustain an experience without exhausting its meaning. Their authority should remain answerable to the people and circumstances they affect; otherwise, a means of making life more habitable risks becoming the criterion to which life must conform.']
def make_unit(day,t,li,stage):
 level=LEVELS[li];words=t['words'][li];cards=[]
 def add(typ,title,meaning,example='',exercise='',answer='',**extra):
  n=len(cards)+1;c=dict(id=f'{day}-{level}-{n}',type=typ,number=n,title=title,meaning=meaning,example=example,exercise=exercise,answer=answer,level=level,conversation='',notes='',structure='',highlights=[],partOfSpeech='',ipa='',wordForms='',synonyms=[],synonymNote='',topicId=t['id'],visualSubject=t['object'],**extra);cards.append(c);return c
 for i in range(2):
  w,meaning=words[i*2:i*2+2];other=words[(1-i)*2]
  # Definition questions avoid invented collocations or unsupported pronunciation.
  c=add('vocabulary',w,meaning,exercise=f'Which word means “{meaning}”: {w} or {other}?',answer=w)
  c['notes']=f'Topic: {t["title"]}. Write one sentence using this word. Check that your sentence keeps the meaning shown above.'
  c['conversation']=f'A: What does “{w}” mean?\nB: It means {meaning}.\nA: Can we use it {t["place"]}?\nB: Yes. Let us think of a clear example.'
  c['visualSubject']=w
 for title,meaning,ex in PHRASES[li]:
  c=add('phrases',title,meaning,ex,f'Explain “{title}” in your own words, then use it in a sentence about {t["title"].lower()}.',f'It means to {meaning}. Example: {ex}')
  c['notes']='Keep the particle with the verb. Check a dictionary before changing its object or word order.'
  c['conversation']=f'A: How can we {t["action"]}?\nB: {ex}\nA: That gives us a starting point.'
 for title,meaning,ex in IDIOMS[li]:
  c=add('idioms',title,meaning,ex,f'What does “{title}” mean in this example? {ex}',meaning[0].upper()+meaning[1:]+'.')
  c['notes']='Learn the whole expression. It is figurative language, so a word-for-word interpretation may be misleading.'
 daily=['Could you help me, please?','Could you explain that again?','Let me check that I understand.','Would you mind if we considered another option?','I see your point, although I would qualify it slightly.','I would distinguish between the intention and its consequences.'][li]
 add('daily',daily,'A useful way to keep an everyday conversation clear and considerate.',f'A: How should we {t["action"]}?\nB: {daily}',f'When might you say “{daily}”?',f'You could say it {t["place"]}, when you want to ask for help or make your understanding clear.')
 q=['Small things can help.','A little care can make a day easier.','Small choices matter to other people.','A small decision matters when it helps someone else.','Consideration becomes visible through practical decisions.','The significance of a decision is not exhausted by its efficiency.'][li]
 add('reflection',q,'An original James Real learning reflection on practical consideration.',f'For example, {t["example2"]}.','Which action in today’s topic illustrates this reflection?',t['example2'][0].upper()+t['example2'][1:]+'.',attribution='James Real learning reflection')
 title,meaning,ex,question,answer=GRAMMAR[li];add('grammar',title,meaning,ex,question,answer)
 opener=f'How do you usually {t["action"]}?';reply=['I make a small plan.','I get ready first, and I ask a friend to help.','I start with a simple plan, but I can change it.','I try to prepare without deciding every detail in advance.','I make practical arrangements, while leaving room for other people’s preferences.','I treat the plan as provisional, rather than assuming that its coherence guarantees a good experience.'][li]
 c=add('smalltalk',opener,'An open question that invites a person to describe a familiar experience.',exercise='Write a reply of your own, then ask one related question.',answer=f'{reply} What works best for you?');c['conversation']=f'A: {opener}\nB: {reply}\nA: What has helped you most?\nB: For example, {t["example1"]}.'
 paras=essay(t,li);c=add('essay',t['title'],'A four-paragraph model with a main idea, two developed points, and a conclusion.',exercise='What two reasons support the main idea? Explain one example.',answer=f'The two reasons are that {t["reason1"]} and that {t["reason2"]}. One example is that {t["example1"]}.');c.update(paragraphs=paras,paragraphRoles=['Introduction — state the main idea','Body 1 — reason and example','Body 2 — second reason and example','Conclusion — connect both reasons'],structure='State a focused main idea. Develop one supporting reason in each body paragraph, with a concrete example. Conclude by connecting the two reasons without introducing a new argument.',notes='Use the structure as a model; write about an experience of your own.')
 # Seven practice lenses explicitly make the revisiting a review sequence.
 for c in cards:
  base=c['exercise'];base_answer=c['answer'];prompts=[base,'Explain the meaning before looking at the model answer. '+base,'Make a sentence of your own, then answer: '+base,'Compare your first answer with this question: '+base,'Explain your reasoning to a partner. '+base,'Apply the idea to a real situation, then answer: '+base,'Review without reading the example first. '+base];c['exercise']=(([base,'Read, then answer. '+base,'Try it. '+base,'Look again. '+base,'Tell a friend. '+base,'Your example. '+base,'Try without help. '+base][stage]) if li<2 else prompts[stage]);c['answer']=base_answer;c['practiceStage']=STAGES[stage]
 return dict(date=day,level=level,theme=t['title']+' · '+STAGES[stage],cards=cards,preparedAt='2026-10-24',source='James Real prepared spiral curriculum; repeated topics are deliberate review, not new daily source material.',topicId=t['id'],practiceStage=STAGES[stage])
def main():
 editions={};d=START;index=0
 while d<=END:
  key=d.isoformat();units=copy.deepcopy(ORIGINAL.get(key))
  if units is None:
   topic=TOPICS[min(index//7,len(TOPICS)-1)];stage=index%7;units={l:make_unit(key,topic,i,stage) for i,l in enumerate(LEVELS)}
  editions[key]=units;save(DIST/'data/english-levels'/f'{key}.json',units);d+=timedelta(days=1);index+=1
 save(DIST/'data/english-levels-index.json',dict(dates=list(editions),levels=LEVELS,through=END.isoformat(),preparedAt='2026-10-24',design='Twelve themes with seven practice lenses and explicit review.'))
 # Original recipe files remain byte-for-byte unchanged. New editions are
 # transparent selections from that library, not 20 fabricated new recipes.
 originals={p.stem:json.loads(p.read_text()) for p in (DIST/'data/recipes-archive').glob('*.json')}
 library=[];seen=set()
 for day,e in sorted(originals.items()):
  for r in e['recipes']:
   if r['title'] not in seen:library.append((day,r));seen.add(r['title'])
 cuisines=list(dict.fromkeys(r['cuisine'] for _,r in library));d=min(date.fromisoformat(x) for x in originals);dates=[]
 while d<=END:
  key=d.isoformat();dates.append(key)
  if key not in originals:
   offset=(d-START).days;rows=[]
   for cuisine in cuisines:
    for meal in ['Main','Snack']:
     options=[(day,r) for day,r in library if r['cuisine']==cuisine and r['meal']==meal]
     if not options:continue
     source,r=options[offset%len(options)];r=copy.deepcopy(r);r['originalEdition']=source;rows.append(r)
   save(DIST/'data/recipes-archive'/f'{key}.json',dict(date=key,recipes=rows,preparedAt='2026-10-24',selectionNote='A dated selection from the preserved recipe library. Recipes repeat across dates; original quantities and methods are retained.'))
  d+=timedelta(days=1)
 history=json.loads((DIST/'data/daily-history.json').read_text());save(DIST/'data/calendar-index.json',dict(recipes=dates,english=list(editions),through=END.isoformat(),recipeLibraryCount=len(library),englishCardCount=sum(len(u['cards']) for e in editions.values() for u in e.values())))
 save(ROOT/'content/recipe-library.json',[dict(originalEdition=day,**r) for day,r in library]);print(json.dumps(dict(englishDays=len(editions),englishCards=len(editions)*66,recipeDays=len(dates),recipeLibrary=len(library),end=str(END))))
if __name__=='__main__':main()
