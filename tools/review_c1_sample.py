"""Build an isolated eleven-card editorial sample; never overwrite daily editions."""
from pathlib import Path
import sys,json,copy,base64,importlib.util,re,html
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist';OUT=D/'review-c1-20261031';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'tools'))
import restore_card_format as renderer
unit=copy.deepcopy(json.loads((D/'data/english-levels/2026-10-31.json').read_text())['C1'])
cards=unit['cards']
def revise(n,**kw):cards[n-1].update(kw)
revise(1,
 meaning='Strange and difficult to explain, often in a way that makes you feel uneasy.',
 example='In the fog, the familiar path had an uncanny stillness, as if the whole forest were holding its breath.',
 synonyms=['eerie','strangely unsettling'],synonymNote='Eerie emphasizes unease; uncanny can also describe a startling resemblance or ability.',
 notes='Use uncanny before a noun or after seem, feel or look. An uncanny resemblance is strikingly exact; it need not be frightening.',
 conversation='A: This is the path we walked yesterday, isn’t it?\nB: Yes, but the fog makes it feel uncanny. I can barely see the next tree.\nA: And there’s not a sound. Shall we head back?\nB: Let’s. I’d rather take the road while it’s still light.',
 exercise='Choose the more natural use of uncanny and explain why: (a) The twins, who had never met, used exactly the same unusual expressions. (b) The bus arrived at its advertised time.',
 answer='(a). Their unexpectedly exact similarity is difficult to explain. A bus arriving on schedule is ordinary, so uncanny would usually be inappropriate.')
revise(2,
 meaning='An act or event held to honor the memory of a person or a past event.',
 example='The neighborhood held a candlelit commemoration for residents who had died during the previous year.',
 synonyms=['remembrance','memorial observance'],synonymNote='A celebration may be joyful; a commemoration centers on remembering and honoring.',
 notes='Common patterns: a commemoration of an event; a ceremony in commemoration of someone. Do not assume Halloween and remembrance observances are the same tradition.',
 conversation='A: Are the candles part of the costume festival?\nB: No. They’re for a separate commemoration in the square.\nA: Is it appropriate for visitors to attend?\nB: Yes. The organizers ask people to keep their voices low and leave the candles undisturbed.',
 exercise='An invitation reads: “Come to our commemoration—a loud costume contest with prizes!” What expectation does commemoration create, and which word better fits the advertised event?',
 answer='Commemoration suggests honoring a person or past event. Celebration or party better fits the costume contest, unless remembrance is genuinely its purpose.')
revise(3,
 meaning='Include a relevant cost, condition or amount of time in a calculation or decision.',
 example='When choosing our departure time, we factored in the walk to the venue and the queue at the entrance.',
 notes='Separable: factor the delay in / factor in the delay. Put a pronoun in the middle: factor it in. Often used when planning or estimating.',
 conversation='A: The lantern walk starts at seven thirty. Leaving at seven twenty should be fine.\nB: Have you factored in the fifteen-minute walk?\nA: I hadn’t—and the organizers expect a ten-minute queue.\nB: Then let’s work backward from the start time.',
 exercise='The walk starts at 7:30. Getting there takes 15 minutes and entry takes another 10. What is the latest departure time? Explain your calculation in one sentence using factor in.',
 answer='We should leave by 7:05 because we need to factor in both the fifteen-minute walk and the ten-minute queue.')
revise(4,
 meaning='Resolve practical problems or disagreements so that an arrangement can work smoothly.',
 example='The coordinators met to iron out an overlap in the volunteers’ shifts before opening night.',
 notes='Separable: iron out the problems / iron the problems out; iron them out. Use it for resolving difficulties, not simply discovering them.',
 conversation='A: Two volunteers are booked for the early shift, but nobody is staying until closing.\nB: We need to iron that out before we send the rota.\nA: I can move to the late shift if someone covers the first half hour.\nB: I’ll cover it. That leaves us staffed throughout.',
 exercise='Replace the vague reply “We’ll deal with it” with a specific two-sentence update using iron out. The problem: two volunteers have been assigned the same shift and the closing shift is empty.',
 answer='We’ve ironed out the overlap by moving one volunteer to the closing shift. The early team will cover the first half hour until the replacement arrives.')
revise(5,
 meaning='A plan that appears straightforward may depend on small, easily overlooked details.',
 example='The costume contest sounded open to everyone, but the devil was in the details: entrants needed to register before noon.',
 notes='Often used as a warning after broad agreement with a proposal. It draws attention to implementation; it does not mean every plan is doomed.',
 conversation='A: Entry is free, so we can register when we get there.\nB: Read the small print. Registration closes at noon.\nA: Ah, the devil is in the details. I only noticed “free entry.”\nB: We still have twenty minutes. Let’s register now.',
 exercise='Which overlooked detail best justifies this idiom? A: The poster is orange. B: Registration closes six hours before the contest. C: The event has a cheerful name. Give one practical consequence.',
 answer='B. Someone arriving at the contest without registering earlier could be unable to enter, even though admission is free.')
revise(6,
 meaning='Something that brings an advantage while also creating a related disadvantage or risk.',
 example='Posting the party photos online is a double-edged sword: it spreads the word, but guests may lose control of where their images appear.',
 notes='Name both edges: a benefit and a cost of the same thing. Two unrelated complaints do not demonstrate the idiom.',
 conversation='A: Last year’s photos brought in twice as many visitors. We should post everything again.\nB: Publicity is a double-edged sword. Some guests don’t want their children’s faces online.\nA: Could we use close-ups of the decorations instead?\nB: Yes, and ask permission before including anyone identifiable.',
 exercise='Complete this balanced assessment with one benefit and one drawback: “A public event hashtag is a double-edged sword: ___, yet ___.” Keep both points connected to public visibility.',
 answer='A public event hashtag is a double-edged sword: it helps people discover the event, yet it can expose participants’ photos to strangers.')
revise(7,
 meaning='A polite way to accept the main part of an argument while limiting or refining one of its claims.',
 example='“I see your point, although I would qualify it slightly. Bright lighting helps people find the entrance, but flashing lights are not necessary.”',
 notes='Qualify means limit or make more precise here. Follow the phrase with an actual qualification; without one, it can sound evasive or overly formal.',
 conversation='A: A good Halloween event needs to be frightening from beginning to end.\nB: I see your point, although I would qualify it slightly. A family event also needs a quiet place to take a break.\nA: Wouldn’t that spoil the atmosphere?\nB: Not if it’s separate from the main attraction. Guests could choose how much intensity they want.',
 exercise='A colleague claims, “Every part of the event must be scary.” Respond with the target phrase, preserve the useful part of the idea, and add one clear limitation.',
 answer='I see your point, although I would qualify it slightly. A spooky atmosphere suits the main attraction, but a quiet area would let guests step away when they need to.')
revise(8,
 meaning='A rhythmic chant that creates a supernatural atmosphere in a scene from Macbeth.',
 example='During rehearsal, the actors stressed “Double, double” and the repeated b sounds to give the witches’ chant its driving rhythm.',
 synonyms=['a spell-like chant','a rhythmic incantation'],synonymNote='These describe the kind of speech; they are not substitute quotations.',
 notes='Macbeth, Act 4, Scene 1; first published in the First Folio (1623). The speakers are the witches, not Shakespeare speaking personally. Toil means hard work; a cauldron is a large pot.',
 conversation='A: Shall I whisper the whole line to make it sound sinister?\nB: Try stressing “Double, double” first. The repetition gives it a pulse.\nA: And make “burn” and “bubble” sharper?\nB: Exactly. Let the sounds create the tension rather than simply making your voice louder.',
 exercise='You are directing this line for a school performance. Identify one repetition and one repeated consonant sound. Explain how you would use them in delivery.',
 answer='Repeat and stress “Double, double” to establish a pulse. Emphasize the b sound in “burn” and “bubble” to make the chant feel insistent and spell-like.')
revise(9,
 meaning='When Only then opens a clause meaning “not until that moment,” place the auxiliary before the subject.',
 example='I tried walking in the full costume. Only then did I realize that the mask blocked my view.',
 notes='Past simple: Only then did + subject + base verb. Past perfect: Only then had + subject + past participle. No inversion in “I only then realized…”; this fronted pattern is more emphatic.',
 conversation='A: Did the costume work when you tried it on?\nB: It looked fine in the mirror. Then I tried going down the steps.\nA: What happened?\nB: Only then did I realize I couldn’t see my feet through the mask.',
 exercise='Rewrite as one sentence beginning Only then: “We tested the costume in the dark. At that moment, we noticed that the sleeves covered the reflective strips.”',
 answer='Only then did we notice that the sleeves covered the reflective strips. Use notice, not noticed, after did.')
revise(10,
 meaning='An open invitation to share Halloween preferences without assuming that the other person celebrates it.',
 example='“What would you like to do for Halloween—if you’re doing anything this year?”',
 notes='Offer a low-pressure follow-up. If someone says they do not celebrate, accept the answer and move to another topic rather than asking them to justify it.',
 conversation='A: What would you like to do for Halloween, if you’re doing anything this year?\nB: Something low-key. I’m not really into haunted houses.\nA: Same here. How about carving a pumpkin and making dinner?\nB: That sounds more like me. Have you ever managed one of those elaborate designs?\nA: Once. It looked impressive for about ten minutes before it collapsed.\nB: Then let’s start with a face we can actually finish.',
 exercise='Your neighbor replies, “I don’t celebrate Halloween, actually.” Write a friendly response that acknowledges this and smoothly opens a different topic.',
 answer='Of course. Are you doing anything nice this weekend instead?')
revise(11,
 title='A little room to choose',
 paragraphs=[
 'A memorable Halloween gathering does not have to frighten every guest equally. At our neighborhood event, the aim was to create a lively evening without making participation feel like a test of courage. We found that clear choices, rather than an ever more elaborate spectacle, made the event welcoming.',
 'First, we made the different experiences easy to identify. A lantern-lit route led to the main attraction, while a quieter room offered pumpkin carving and warm drinks. A volunteer explained both options at the entrance. Guests could change their minds without having to explain themselves, which mattered more than any promise that the event was suitable for everyone.',
 'Choice also depended on details that were easy to miss during planning. Only when we tested a costume outside did we notice how much the mask restricted the wearer’s view. We adjusted it before opening and checked that the route remained clear. At the refreshment table, ingredient labels and a non-food treat gave guests another practical way to decide what suited them.',
 'The evening succeeded because its atmosphere invited people in while its arrangements let them remain in control. Preparation did not remove the surprise or playfulness; it removed avoidable pressure. Next year, we would keep the same principle: make the possibilities clear, pay attention to the small obstacles, and leave people a little room to choose.'
 ],
 exercise='Plan a four-paragraph essay about an event you would improve. State one main idea; develop two distinct changes with concrete examples; conclude by explaining what those changes achieve together.',
 answer='Introduction: make a school fair easier to navigate. Body 1: clear signs and a staffed entrance. Body 2: a quiet seating area away from the stage. Conclusion: better guidance and a place to pause help more guests enjoy the same event.',
 notes='Each body paragraph needs a distinct supporting point and a concrete example. The conclusion draws the argument together without introducing a third proposal.',
 structure='Introduce a clear position; develop two different supporting points with examples; conclude with their shared value.')

# Keep the landscape essay comfortably readable beside its fixed portrait frame.
revise(11, paragraphs=[
'A welcoming Halloween event gives people choices rather than testing everyone’s courage. At our neighborhood gathering, we wanted a lively atmosphere without pressuring guests to enjoy the same activities. Clear options and careful preparation proved more useful than an increasingly elaborate spectacle.',
'First, we made two experiences easy to identify. A lantern-lit route led to the main attraction; a quieter room offered pumpkin carving and warm drinks. Volunteers explained both at the entrance, allowing guests to change their minds without having to justify their preferences.',
'Practical details mattered just as much. Only when we tested a costume outside did we notice that its mask restricted the wearer’s view. We adjusted it and checked the route for obstacles. Ingredient labels and non-food treats also helped guests decide what suited them.',
'The event worked because its atmosphere invited participation while its arrangements preserved a sense of control. Preparation did not remove the surprise; it removed avoidable pressure. Next year, we would retain that balance: make the possibilities clear, anticipate small obstacles, and leave people room to choose.'
], structure='State a position; develop two distinct points with concrete examples; draw them together in the conclusion.',
exercise='Outline four paragraphs improving a school fair. Include two different changes, a concrete example for each, and a conclusion linking their benefits.',
answer='Introduction: a more welcoming fair. Body 1: clear signs at the entrance. Body 2: quiet seating away from the stage. Conclusion: better guidance and choice help guests enjoy themselves.')

catalog=json.loads((ROOT/'content/photo-catalog.json').read_text());portraits=json.loads((ROOT/'content/essay-photo-catalog.json').read_text())
new=[('uncanny',5288094,'https://www.pexels.com/photo/tall-trees-in-the-forest-covered-in-fog-5288094/','Mist makes the familiar forest difficult to recognize.'),('commemoration',29190201,'https://www.pexels.com/photo/votive-candles-illuminating-a-memorial-tribute-29190201/','Memorial candles express remembrance rather than a costume celebration.'),('cauldron',33635613,'https://www.pexels.com/photo/vintage-cauldron-on-rustic-background-showcasing-age-33635613/','A cauldron is a large cooking pot: the central object in the witches’ chant.')]
for scene,pid,url,caption in new:
 im=Image.open(f'/tmp/jr-c1-photos/{pid}.jpg').convert('RGB');assert im.width>im.height
 im=ImageOps.fit(im,(644,285),Image.Resampling.LANCZOS);im.save(OUT/f'{pid}.jpg',quality=88)
 catalog[scene]={'asset':str((OUT/f'{pid}.jpg').relative_to(D)),'sourceURL':url,'credit':f'Pexels · {pid}','licenseURL':'https://www.pexels.com/license/','caption':caption}
scenes=['uncanny','commemoration','map','strategy','document','phone','discussion','cauldron','halloween-costume','pumpkin','halloween-costume']
captions=[new[0][3],new[1][3],'A route takes time; a departure plan must allow for the journey.','Coordinators work through an arrangement together.','Small print can contain a condition that changes the whole plan.','Online sharing offers visibility but can reduce control over an image.','A discussion leaves room to agree while adding a reservation.','A cauldron is a large cooking pot: the central object in the witches’ chant.','Trying a costume on is only the first step; it must also work in motion.','Pumpkin carving offers a quieter alternative to a haunted attraction.','A distinctive costume can be part of an evening with room for different preferences.']
stats=[];manifest=[]
for i,c in enumerate(cards):
 photo=copy.deepcopy((portraits if i==10 else catalog)[scenes[i]])
 photo.update(caption=captions[i],orientation='portrait' if i==10 else 'landscape')
 renderer.PHOTOS[c['id']]=photo;c['photoCredit']=photo;c['illustration']=photo['asset'];c['illustrationAlt']=photo['caption']
 category='Phrasal verb' if c['type']=='phrases' else renderer.P[c['type']][0]
 name=f'Everyday English - C1 - 2026-10-31 - {category} - {c["categoryNumber"]:02}'
 photo_uri='data:image/jpeg;base64,'+base64.b64encode((D/photo['asset']).read_bytes()).decode()
 for answer,suffix in [(False,''),(True,'-download')]:
  svg,stat=renderer.render(c,'2026-10-31','C1',answer)
  old=f'Everyday English - C1 - 2026/10/31 - {c["categoryNumber"]:02} - {category}'
  newtitle=f'Everyday English - C1 - 2026/10/31 - {category} - {c["categoryNumber"]:02}'
  svg=svg.replace(html.escape(old,quote=True),html.escape(newtitle,quote=True)).replace('__JR_PHOTO__',photo_uri)
  (OUT/f'{i+1:02}{suffix}.svg').write_text(svg);stats.append(stat)
 manifest.append({'number':i+1,'title':c['title'],'category':category,'filename':name+'.png','sourceURL':photo['sourceURL'],'skill':c['exercise']})
assert len({c['photoCredit']['asset'] for c in cards})==11
(OUT/'cards.json').write_text(json.dumps(unit,ensure_ascii=False,indent=2))
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(OUT/'layout-audit.json').write_text(json.dumps(stats,indent=2))
items=[]
for i,row in enumerate(manifest):
 items.append(f'<article id="card-{i+1}"><h2>{i+1:02} · {html.escape(row["category"])} — {html.escape(row["title"])}</h2><img loading="lazy" src="{i+1:02}.png" alt="{html.escape(row["title"])}"><details><summary>Reveal model answer</summary><p>{html.escape(cards[i]["answer"])}</p></details><p><a href="{i+1:02}-download.png" download="{html.escape(row["filename"])}">Download PNG with model answer</a> · <a href="{row["sourceURL"]}" target="_blank" rel="noopener">Photo source</a></p></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1"><title>C1 · October 31 · Eleven-card review</title><style>body{margin:0;background:#111510;color:#eee6d6;font:17px/1.6 Arial,sans-serif}main{max-width:1120px;margin:auto;padding:36px 20px}h1{font:42px Georgia;color:#d9c38e}h2{font-size:21px}a{color:#d9c38e}nav{display:flex;flex-wrap:wrap;gap:16px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}article{background:#1b2119;padding:16px;border:1px solid #514b37;border-radius:4px}article img{display:block;width:100%;height:auto}article:last-child{grid-column:1/-1}details{padding:12px 0}header{margin-bottom:30px}@media(max-width:700px){.grid{grid-template-columns:1fr}h1{font-size:34px}}@media print{body{background:white}article{break-after:page}.grid{display:block}}</style><main><header><p>EVERYDAY ENGLISH / EDITORIAL SAMPLE</p><h1>C1 · October 31, 2026</h1><p>Eleven cards. Eleven different photographs. Context-led conversations and varied practice.</p><p>Model answers stay hidden until opened. Downloaded cards include the answers.</p><nav><a href="C1-2026-10-31-eleven-cards.zip">Download all eleven PNG cards</a>'''+''.join(f'<a href="#card-{n}">{n:02}</a>' for n in range(1,12))+'''</nav></header><section class="grid">'''+''.join(items)+'''</section></main></html>'''
(OUT/'index.html').write_text(page)
print('Built isolated sample:',len(cards),'cards; 11 unique source photos; layout checks passed.')
