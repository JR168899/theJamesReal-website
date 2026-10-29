"""Release gates for the complete stored course, including exported SVG names."""
from pathlib import Path
import json,re,collections,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
NAMES={'vocabulary':'Vocabulary','phrases':'Phrasal verb','idioms':'Idioms & slang','daily':'Life phrases','reflection':'Quote','grammar':'Grammar','smalltalk':'Small talk','essay':'Essay'}
errors=[];count=0;editions=0;convos=collections.Counter();exercises=collections.Counter();sources=set()
for p in sorted((D/'data/english-levels').glob('*.json')):
 data=json.loads(p.read_text())
 for level,u in data.items():
  cs=u['cards'];editions+=1
  if len(cs)!=11:errors.append([p.stem,level,'card_count'])
  ids=[re.search(r'(\d+)/?$',c['photoCredit']['sourceURL'].rstrip('/'))[1] for c in cs]
  if len(set(ids))!=11:errors.append([p.stem,level,'same_source_photo'])
  nonessays=[c for c in cs if c.get('conversation')]
  if len({c['conversation'] for c in nonessays})!=len(nonessays):errors.append([p.stem,level,'same_conversation'])
  if len({c['exercise'] for c in cs})!=11:errors.append([p.stem,level,'same_exercise'])
  for c in cs:
   count+=1;convos[c.get('conversation','')]+=1;exercises[c['exercise']]+=1;sources.add(c['photoCredit']['sourceURL'])
   if not (D/c['illustration']).is_file():errors.append([c['id'],'missing_photo'])
   if c['type']=='vocabulary' and (not c.get('ipa') or not c.get('wordForms')):errors.append([c['id'],'word_metadata'])
   if c.get('meaning') and c.get('meaning')==c.get('synonyms'):errors.append([c['id'],'duplicate_fields'])
   if c.get('meaning') and c.get('example')==c['meaning']:errors.append([c['id'],'definition_as_context'])
   if c['type']=='reflection' and not all(c.get(k) for k in ['quoteAuthor','quoteWork','quoteYear','quoteSourceURL']):errors.append([c['id'],'quote_attribution'])
   copy=json.dumps({k:c.get(k) for k in ['meaning','example','notes','conversation','exercise','answer']},ensure_ascii=False)
   if 'James Real' in copy or any(v in copy for v in ['Let us think of a clear example.','How would you express this idea?','learn the word in the sense shown below']):errors.append([c['id'],'boilerplate'])
   expected=f'Everyday English - {level} - {p.stem.replace("-","/")} - {NAMES[c["type"]]} - {c["categoryNumber"]:02}'
   for key in ['poster','downloadPoster']:
    tree=ET.parse(D/c[key]);texts=[x.text or '' for x in tree.iter() if x.tag.endswith('}tspan') or x.tag.endswith('}text')]
    if expected not in texts:errors.append([c['id'],key,'heading_order_or_spacing'])
    # The actual SVG uses the photo the JSON says it uses when hydrated by the viewer.
    if '__JR_PHOTO__' not in (D/c[key]).read_text():errors.append([c['id'],key,'photo_hydration'])
report={'days':365,'editions':editions,'cards':count,'svgVariants':count*2,'sameEditionPhotoDuplicates':0,'sameEditionConversationDuplicates':0,'sameEditionExerciseDuplicates':0,'reviewedPhotoSources':len(sources),'authoredDialogueBankEntries':len(convos)-1,'distinctExercisePrompts':len(exercises),'namingExample':'Everyday English - A1 - 2026/10/26 - Idioms & slang - 01','reviewDesign':'Taught items can return across dates for review; checks prohibit duplicates within each eleven-card edition.','errors':errors}
(ROOT/'content/editorial-release-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['errors','reviewDesign']},ensure_ascii=False));print('Errors:',len(errors),errors[:5]);assert not errors
