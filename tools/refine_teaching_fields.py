from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
SYN={line.split('|')[0]:line.split('|')[1].split('; ') for line in (ROOT/'content/expression-synonyms.tsv').read_text().splitlines() if line}
MEANINGS={
'Could you help me, please?':'A polite request for someone to assist you with a task.',
'Could you explain that again?':'A request to hear an explanation once more because it was not clear the first time.',
'Let me check that I understand.':'A way to confirm your understanding before continuing a conversation.',
'Would you mind if we considered another option?':'A polite suggestion that a group examine a different possibility.',
'I see your point, although I would qualify it slightly.':'An acknowledgment of an argument followed by a limited reservation about its scope.',
'I would distinguish between the intention and its consequences.':'A proposal to evaluate a person’s purpose separately from the effects of their action.',
'Small things can help.':'A simple action can make a task easier or improve someone’s situation.',
'A little care can make a day easier.':'Thinking about another person’s needs can prevent an everyday difficulty.',
'Small choices matter to other people.':'Ordinary decisions can affect the people around us, even when the decisions seem minor.',
'A small decision matters when it helps someone else.':'The value of a modest choice can lie in the benefit it gives another person.',
'Consideration becomes visible through practical decisions.':'Care for other people is demonstrated by choices that respond to their actual needs.',
'The significance of a decision is not exhausted by its efficiency.':'A decision should be judged by its effects on people as well as by its use of time or resources.'}

def clean(v):
 if isinstance(v,list):return [clean(x) for x in v]
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
 if isinstance(v,str):return re.sub(r'\s{2,}',' ',v.replace('James Real learning reflection','learning reflection').replace('James Real','')).strip() if 'James Real' in v else v
 return v

def refine(c):
 title=c['title'];typ=c['type']
 if title in SYN:c['synonyms']=SYN[title]
 if title in MEANINGS:c['meaning']=MEANINGS[title]
 if typ=='reflection' and 'learning reflection' in c.get('conversation','').lower():
  c['conversation']='A: What did we learn from that experience?\nB: '+title+'\nA: What do you mean?\nB: '+c['meaning']
 if typ=='reflection' and c.get('notes','').startswith('This is an original'):
  c['notes']='Read this as a reflection, not a factual rule. Relate it to a specific action in the example, and explain why you agree or disagree.'
 return clean(c)

def main():
 count=0
 for p in sorted((ROOT/'dist/data/english-levels').glob('*.json')):
  d=json.loads(p.read_text())
  for u in d.values():
   counters={}
   for i,c in enumerate(u['cards']):
    c=refine(c);t=c['type'];counters[t]=counters.get(t,0)+1;c['categoryNumber']=counters[t];u['cards'][i]=c;count+=1
  p.write_text(json.dumps(clean(d),ensure_ascii=False,separators=(',',':'))+'\n')
 print('Reviewed fields and category numbering:',count)
if __name__=='__main__':main()
