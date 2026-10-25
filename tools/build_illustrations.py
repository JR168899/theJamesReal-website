"""Semantic, code-native story illustrations. Original rasters stay untouched.
Each artwork records an explicit subject; abstract language uses named metaphors.
No network calls or random picture assignment.
"""
from pathlib import Path
import json,hashlib,html,math
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist';OUT=D/'assets/english-story';OUT.mkdir(parents=True,exist_ok=True)
E=html.escape
# Small original line drawings. Larger scenes combine objects and people;
# they are not logos or third-party illustrations.
ICONS={
'cup':'<path d="M-38-25H28L22 27Q0 45-30 27Z" fill="#d9a67a"/><path d="M28-18C70-27 69 21 26 17M-40 45H42M-12-42Q-25-58-10-71M8-42Q-5-58 10-71"/>',
'plate':'<ellipse rx="65" ry="38" fill="#e9d2a9"/><ellipse rx="43" ry="23"/><path d="M-84-40V43M-94-40V-13Q-84 1-74-13V-40M85-40V43M85-40Q59-12 85-4"/>',
'book':'<path d="M0-34Q-32-54-72-36V47Q-31 32 0 50Q32 32 72 47V-36Q32-54 0-34Z" fill="#a8bbaa"/><path d="M0-34V50M-57-20L-14-10M-57-2L-14 8M15-10L56-20M15 8L56-2M15 26L56 16"/>',
'chair':'<path d="M-35-50H30V10H-35ZM-43 10H40V27H-43ZM-32 27L-43 65M29 27L39 65" fill="#d4a581"/>',
'window':'<rect x="-60" y="-65" width="120" height="130" rx="4" fill="#b2ccd0"/><path d="M0-65V65M-60 0H60M-75 65H75M-40-45L-15-20M25 25L45 45"/>',
'plant':'<path d="M-35 20H35L23 65H-23Z" fill="#d7a27c"/><path d="M0 22V-65M0-18Q-73-24-45-67Q-1-67 0-18ZM0 0Q64-6 49-47Q8-50 0 0Z" fill="#9db8a0"/>',
'train':'<rect x="-65" y="-55" width="130" height="100" rx="20" fill="#a7bfc6"/><path d="M-49-37H-5V0H-49ZM9-37H49V0H9M-50 22H-32M32 22H50M-40 45L-58 72M40 45L58 72M-50 60H50"/>',
'ticket':'<path d="M-70-35H70V-10Q45 0 70 10V35H-70V10Q-45 0-70-10Z" fill="#dfc590"/><path d="M20-30V30M-48-13H0M-48 5H0" stroke-dasharray="6 5"/>',
'people':'<circle cx="-35" cy="-38" r="17" fill="#e0b28e"/><circle cx="40" cy="-32" r="17" fill="#bd917d"/><path d="M-63 37V0Q-35-30-9 0V37M12 41V7Q39-23 68 7V41M-42 38L-51 72M-25 38L-18 72M32 43L25 76M50 43L60 76" fill="#a6bac0"/><path d="M-9 6L9 17L21 3"/>',
'basket':'<path d="M-63-12H63L45 55H-45Z" fill="#d0b079"/><path d="M-39-12Q-31-83 0-60Q31-83 39-12M-36 0L-27 43M-12 0L-9 43M12 0L9 43M36 0L27 43M-52 17H52M-48 34H48"/>',
'music':'<path d="M-27 37V-40L48-57V19M-27-22L48-39"/><ellipse cx="-43" cy="40" rx="21" ry="14" fill="#b7a3bf"/><ellipse cx="31" cy="23" rx="21" ry="14" fill="#b7a3bf"/>',
'umbrella':'<path d="M-72-4Q0-108 72-4Q48-26 24-4Q0-26-24-4Q-48-26-72-4Z" fill="#c7a1a3"/><path d="M0-62V49Q0 78-23 63M-72-4Q-32-72 0-62Q32-72 72-4M-52 19L-59 33M45 22L39 37"/>',
'desk':'<path d="M-79 13H79V28H-79ZM-60 28V73M60 28V73M-35-46H40V2H-35ZM-46 7H51" fill="#b7bec8"/><path d="M52-7L67-30M67-30L82-21M67-30V-56"/>',
'city':'<path d="M-75 60V-15H-35V60M-21 60V-60H21V60M35 60V-31H75V60M-90 62H90M-64 0H-49M-64 17H-49M-64 34H-49M-9-39H9M-9-20H9M-9 0H9M-9 20H9M48-13H63M48 8H63M48 30H63" fill="#c6b8a5"/>',
'calendar':'<rect x="-63" y="-46" width="126" height="108" rx="7" fill="#e2c6b6"/><path d="M-63-15H63M-37-62V-32M37-62V-32M-39 4H-25M-7 4H7M25 4H39M-39 24H-25M-7 24H7M25 24H39M-39 44H-25M-7 44H7"/>',
'path':'<path d="M-15 70Q-53 14-13-4Q29-22-11-69M28 70Q-6 12 29-1L72-41" fill="none"/><path d="M58-43L73-42L69-26M-16-59L-11-70L0-61"/>',
'magnifier':'<circle cx="-12" cy="-12" r="42" fill="#c8d9d5"/><path d="M19 19L61 61M-30-32Q-45-16-30 2"/>',
'scales':'<path d="M0-60V59M-45 64H45M-63-34H63M-48-34L-70 18H-24ZM48-34L24 18H70Z" fill="#d9bf85"/>',
'bridge':'<path d="M-80 37Q0-46 80 37M-80 48H80M-53 48V-40M53 48V-40M-53-32Q0 14 53-32M-25-9V48M0 0V48M25-9V48" fill="none"/>',
'light':'<path d="M-31-33Q-31-68 0-68Q32-68 32-33Q32-11 15 3V28H-15V3Q-31-11-31-33Z" fill="#e5c47d"/><path d="M-15 13H15M-14 37H14M-8 45H8M0-87V-100M-48-73L-59-84M48-73L59-84M-60-38H-78M60-38H78"/>',
'key':'<circle cx="-32" cy="-12" r="28" fill="#dcc18a"/><path d="M-11 9L50 65M29 46L43 31M44 60L59 44"/>',
'clock':'<circle r="63" fill="#cfdbd3"/><path d="M0-40V0L29 17M0-55V-46M55 0H47M0 55V47M-55 0H-47"/>',
'egg':'<path d="M0-70C-24-70-57-9-57 22C-57 83 57 83 57 22C57-9 24-70 0-70Z" fill="#e6d5b6"/><path d="M-45 3L-18-6L-6 12L15-3L47 8"/>',
'letter':'<rect x="-72" y="-46" width="144" height="92" rx="6" fill="#d1bcc0"/><path d="M-68-38L0 10L68-38M-68 38L-23 0M68 38L23 0"/>',
'ladder':'<path d="M-40 70L-15-73M25 70L50-73M-12-55H47M-20-20H40M-26 15H34M-33 50H28"/>',
'coat':'<path d="M-26-58L-58-42L-80 10L-58 20L-38-12V66H38V-12L58 20L80 10L58-42L26-58L0-26Z" fill="#b8b4a0"/><path d="M0-26V64M-26-58L-12-11L0-26L12-11L26-58M-28 27H-9M9 27H28"/>',
'leaf':'<path d="M-55 52Q-78-71 61-64Q80 62-55 52Z" fill="#a9bd98"/><path d="M-70 73L45-47M-32 34L-38-12M-8 8L-10-35M16-17L43-9M-29 34L18 38"/>',
'sun':'<circle r="38" fill="#e4bd7b"/><path d="M0-57V-78M0 57V78M57 0H78M-57 0H-78M41-41L55-55M-41-41L-55-55M41 41L55 55M-41 41L-55 55"/>',
'cloud':'<path d="M-57 27Q-93 4-63-21Q-46-36-28-22Q-12-73 31-43Q50-31 47-10Q98-8 69 26Z" fill="#b7c8cc"/><path d="M-42 41L-53 60M-8 41L-19 60M27 41L16 60M62 41L51 60"/>',
'road':'<path d="M-74 74L-15-76H15L74 74" fill="#c6bcb0"/><path d="M0 66V35M0 13V-6M0-24V-39"/>',
'phone':'<rect x="-35" y="-68" width="70" height="136" rx="10" fill="#b8c8c9"/><path d="M-15-52H15M-13 51H13M-20-26H20M-20-10H13M-20 6H17"/>',
'bag':'<path d="M-50-25H50L61 64H-61ZM-27-25V-42Q0-83 27-42V-25" fill="#c5a78f"/>',
'room':'<path d="M-86 60V-66H86V60M-87 60H87M-75-49H-13V1H-75M-45-49V1M-75-24H-13M15 14H71V52H15M9 52H78M23 53V70M66 53V70" fill="#d9ccba"/>',
'notebook':'<rect x="-51" y="-65" width="104" height="132" rx="7" fill="#b9c7ad"/><path d="M-29-65V67M-10-37H30M-10-18H30M-10 1H30M-10 20H22M66 44L91-36L101-33L77 47Z"/>',
'hand':'<path d="M-65 36L-38 12L-2 12L24-7Q42-17 43-1L18 26H52Q73 24 72 38L27 62H-18L-42 77" fill="#d5ad8e"/>',
'bowls':'<path d="M-75-8H6Q-3 53-61 42ZM5-37H80Q77 19 22 19Z" fill="#cbb8a0"/><path d="M-80-8H12M0-37H87M-44-25Q-55-44-43-57M48-56Q37-72 50-88"/>',
'compass':'<circle r="67" fill="#c8d0c1"/><path d="M-16 15L26-40L15 16L-27 41Z" fill="#c18e7a"/><path d="M0-59V-45M59 0H45M0 59V45M-59 0H-45"/>',
'dialogue':'<path d="M-83-53H23V12H-36L-62 35V12H-83ZM40-26H86V41H62L40 62V41H13V29" fill="#c4cbd5"/><path d="M-63-31H5M-63-12H-13M43-2H68M43 17H68"/>',
'check':'<rect x="-57" y="-67" width="114" height="134" rx="8" fill="#ddd2b6"/><path d="M-35-31L-25-20L-9-43M6-29H36M-35 5L-25 16L-9-7M6 7H36M-35 41L-25 52L-9 29M6 43H36"/>',
'fabric':'<path d="M-62-61Q-31-48 0-61Q31-75 62-61V60Q31 45 0 60Q-31 76-62 60Z" fill="#bca5ad"/><path d="M-45-50V62M-23-50V65M0-59V59M23-63V48M45-63V51M-62-30Q0-9 62-30M-62 0Q0 21 62 0M-62 31Q0 51 62 31"/>'
}
GROUPS=[(['cup','drink'],'cup'),(['plate','portion','commensal','hospitality','guest','convivial','table'],'plate'),(['ticket','itinerary','destination','journey','arriv','train','connection'],'train'),(['book','page','chapter','passage','polysemy','hermeneutic','interpret','discern'],'book'),(['chair'],'chair'),(['window'],'window'),(['grow','plant','cultivat','steward','phenolog','symbios','water'],'plant'),(['leaf'],'leaf'),(['coat','wear'],'coat'),(['friend','together','cooperat','reciprocity','intersubjective','interdependence'],'people'),(['question','explain','clarif','acknowledg','nuance','equivoc','conversation','listen','receptiv'],'dialogue'),(['bag'],'bag'),(['shop','market','price','fresh','frugality','budget'],'basket'),(['provenance','compare','value','discerning','externality','balance','weigh','double-edged','asymmetry'],'scales'),(['durable','fabric','patina'],'fabric'),(['song','hear','rhythm','melody','music','resonance','evocative','counterpoint','ineffable'],'music'),(['rain','weather','forecast','vicissitude'],'umbrella'),(['alternative','contingency','provisional','adjust','change','serendipity','navigate','circumspect','play it by ear'],'path'),(['room','home','tidy','shelf','practical','functional','atmosphere','coherent','adaptable'],'room'),(['work','task','finish','responsib','coordinate','accountab','delegate','subsidiarity'],'desk'),(['street','corner','building','landmark','city','character','pedestrian','streetscape','contextual','palimpsest','liminal'],'city'),(['year','plan','goal','priority','retrospective','teleology'],'calendar'),(['progress','incremental','realistic','sustainable','resilience'],'ladder'),(['reflect','remember','observe','condition','evaluate','reflexivity'],'notebook'),(['help','hand','solicitude','considerate'],'hand'),(['morning','early'],'sun'),(['routine','time','patient'],'clock'),(['look','notice','subtle','perspective','implicit','attention','assumption'],'magnifier'),(['egg'],'egg'),(['gordian','iron out','work out'],'key'),(['pick up','get ready'],'bag'),(['sit down'],'chair'),(['bear out','follow through','factor in'],'check'),(['same page'],'book'),(['piece of cake'],'plate'),(['stone unturned','look into','find out'],'magnifier'),(['small talk','quote','reflection'],'people')]
def subject(card):
 text=(card.get('visualSubject','')+' '+card['title']).lower()
 for keys,key in GROUPS:
  if any(w in text for w in keys):return key
 return card.get('visualSubject') if card.get('visualSubject') in ICONS else {'smalltalk':'dialogue','grammar':'notebook','essay':'book','reflection':'light','daily':'people','phrases':'path','idioms':'compass'}.get(card['type'],'magnifier')
def icon(k,x,y,s=1,rotate=0):return f'<g transform="translate({x} {y}) rotate({rotate}) scale({s})">{ICONS[k]}</g>'
def artwork(card):
 key=subject(card);theme=card.get('topicId','conversation');back={'table':'plate','journey':'train','home':'room','books':'book','conversation':'dialogue','market':'basket','music':'music','weather':'umbrella','work':'desk','city':'city','garden':'plant','year':'calendar'}.get(theme,'notebook');n=card['number'];v=int(hashlib.sha256(card['id'].encode()).hexdigest()[:5],16);tilt=(v%7)-3
 secondary='people' if key not in ['people','dialogue'] and n in [3,4,7,10] else back
 # Each subject remains recognisable; background details vary by learning scene.
 body=icon(key,315,192,1.4,tilt)+icon(secondary,94 if n%2 else 538,266,.52,-tilt)
 if key==secondary:body=icon(key,315,192,1.5,tilt)+icon('notebook',95,264,.5,-tilt)
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="660" height="380" viewBox="0 0 660 380"><title>{E(card['title'])}</title><desc>Original hand-drawn story illustration: {key}, set within {E(theme)}. {E(card.get('meaning',''))}</desc><defs><pattern id="paper" width="19" height="17" patternUnits="userSpaceOnUse"><path d="M2 4h2m9 7h1M5 15h1" stroke="#a38b6a" stroke-width=".6" opacity=".18"/></pattern></defs><rect width="660" height="380" fill="#f2eadb"/><rect width="660" height="380" fill="url(#paper)"/><ellipse cx="327" cy="317" rx="232" ry="16" fill="#d4c6b1" opacity=".5"/><g stroke="#4b5149" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round" fill="none">{body}<path d="M128 324Q320 309 522 324" stroke-width="1.7"/><path d="M545 75l8-8m14 27h10M112 71l-7-8" stroke="#ba9670" stroke-width="2"/></g><text x="330" y="361" text-anchor="middle" fill="#6b665a" font-family="Georgia,serif" font-size="14" font-style="italic">{E(card['title'][:80])}</text></svg>''',key
PALETTES={'vocabulary':('#efd6d5','#382d2e'),'phrases':('#f1dfcf','#3d3028'),'idioms':('#efe6bd','#383426'),'daily':('#dce6d8','#2d382e'),'reflection':('#dce5ee','#2c3540'),'grammar':('#e7dfec','#382f40'),'smalltalk':('#e3e1df','#353331'),'essay':('#f1eadc','#37322b')}
def main():
 manifest=[];count=0
 for p in sorted((D/'data/english-levels').glob('*.json')):
  data=json.loads(p.read_text())
  for level,u in data.items():
   for c in u['cards']:
    svg,key=artwork(c);asset=OUT/(c['id']+'.svg');asset.write_text(svg);c['illustration']='assets/english-story/'+asset.name;c['illustrationAlt']=f'Hand-drawn scene for {c["title"]}: {key}.';manifest.append({'card':c['id'],'title':c['title'],'subject':key,'topic':c.get('topicId'),'asset':c['illustration']});count+=1
  p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
 (ROOT/'content/illustration-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')))
 print('Illustrated cards:',count)
if __name__=='__main__':main()
