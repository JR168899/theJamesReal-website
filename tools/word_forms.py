"""Reviewed inflection patterns for the stored vocabulary bank."""
UNCOUNTABLE=set('affection attention candy character commensality continuity equanimity equivocation folklore freedom friction frugality generosity gratitude hospitality intentionality interdependence luck phenology pluralism polysemy progress prosperity provenance rain reciprocity reflexivity renewal resilience resonance serendipity solicitude stewardship subsidiarity symbolism syncretism teleology water work'.split())
IRREGULAR_NOUNS={'leaf':'leaves','shelf':'shelves','symbiosis':'symbioses'}
IRREGULAR_VERBS={'choose':('chooses','chose','chosen','choosing'),'grow':('grows','grew','grown','growing'),'hear':('hears','heard','heard','hearing'),'wrap':('wraps','wrapped','wrapped','wrapping')}
ADJECTIVES={
'accountable':'accountability','adaptable':'adaptability','auspicious':'auspiciousness','charitable':'charity','circumspect':'circumspection','civic':'civics','coherent':'coherence','communal':'community','considerate':'consideration','consistent':'consistency','contextual':'context','convivial':'conviviality','deliberate':'deliberation','discerning':'discernment','durable':'durability','evocative':'evocation','familiar':'familiarity','flexible':'flexibility','fresh':'freshness','functional':'function','hermeneutic':'hermeneutics','implicit':'implication','incremental':'increment','ineffable':'ineffability','intergenerational':'generation','intersubjective':'intersubjectivity','liminal':'liminality','patient':'patience','platonic':'Platonism','practical':'practicality','provisional':'provisionality','quiet':'quietness','realistic':'realism','receptive':'receptivity','retrospective':'retrospect','subtle':'subtlety','sustainable':'sustainability','tidy':'tidiness','uncanny':'uncanniness'}
COMPARE={'fresh':('fresher','freshest'),'quiet':('quieter','quietest'),'tidy':('tidier','tidiest'),'subtle':('subtler','subtlest')}
GRADABLE=set('adaptable charitable circumspect coherent considerate consistent convivial discerning durable evocative familiar flexible patient practical realistic receptive sustainable uncanny'.split())
def plural(w):
 if w in IRREGULAR_NOUNS:return IRREGULAR_NOUNS[w]
 if w.endswith('y') and w[-2] not in 'aeiou':return w[:-1]+'ies'
 if w.endswith(('s','x','z','ch','sh')):return w+'es'
 return w+'s'
def forms(word,pos):
 if 'verb' in pos:
  if word in IRREGULAR_VERBS:third,past,part,ing=IRREGULAR_VERBS[word]
  else:
   third=plural(word)
   past=word[:-1]+'ied' if word.endswith('y') and word[-2] not in 'aeiou' else word+'d' if word.endswith('e') else word+'ed'
   part=past;ing=word[:-1]+'ing' if word.endswith('e') and not word.endswith('ee') else word+'ing'
  return f'{word} · {third} · {past} · {part} · {ing} (base · third person · past · past participle · -ing)'
 if word=='platonic':return 'Adjective: platonic; noun phrase: platonic affection.'
 if 'adjective' in pos:
  if word in COMPARE:a,b=COMPARE[word];return f'{word} · {a} · {b}; noun: {ADJECTIVES[word]}'
  if word in GRADABLE:return f'{word} · more {word} · most {word}; noun: {ADJECTIVES[word]}'
  return f'Adjective: {word}; related noun: {ADJECTIVES[word]}'
 if word=='candy':return 'Usually uncountable: candy; countable pieces or types: candies.'
 if word in UNCOUNTABLE:return f'Usually uncountable: {word}; no regular plural in this sense.'
 return f'Singular: {word}; plural: {plural(word)}.'
