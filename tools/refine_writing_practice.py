"""Vary writing assignments around the existing four-paragraph graded models."""
from pathlib import Path
from datetime import date
import json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
topics={t['id']:t for t in json.loads((ROOT/'content/course-topics.json').read_text())}
topics.update({t['id']:t for t in json.loads((ROOT/'content/holiday-calendar.json').read_text())})
def cap(s):return s[0].upper()+s[1:]
def lower(s):return s[0].lower()+s[1:]
def clause(s):return s.rstrip('.')
original_topic={'Lunch with a friend':'table','A picnic that works for everyone':'table','Growing something together':'garden','A good plan makes room for people':'work','Making disagreement productive':'conversation','The limits of consensus':'conversation','One quiet morning':'year','Ten minutes for myself':'year','A routine that fits':'year','Designing a day with breathing room':'year','Making room for what matters':'year','The unmeasured afternoon':'year'}
for p in sorted((D/'data/english-levels').glob('*.json')):
 data=json.loads(p.read_text());stage=(date.fromisoformat(p.stem)-date(2026,1,1)).days%7
 for level,u in data.items():
  c=u['cards'][-1];assert c['type']=='essay'
  if p.stem=='2026-10-31' and level=='C1':continue
  tid=u.get('topicId') or original_topic[c['title']];t=topics[tid]
  act=t['action'];r1=clause(t['reason1']);r2=clause(t['reason2']);e1=clause(t['example1']);e2=clause(t['example2']);s1=t['simple1'];s2=t['simple2']
  # Seven different writing purposes, attached to this lesson's actual subject.
  prompts=[f'Propose a practical way to {act}. Develop two distinct improvements and give a concrete example of each.',f'Write about an attempt to {act} that did not go as planned. Explain two lessons, each supported by a specific incident.',f'Compare two ways to {act}: a rigid plan and one that allows adjustment. Assess one advantage and one limitation.',f'Persuade a group to change how they {act}. Support your recommendation with two different reasons and a practical example of each.',f'Identify two obstacles that could arise when people {act}. Explain a workable response to each, rather than merely listing the problems.',f'Discuss the claim that more preparation always helps people {act}. Support a qualified position with two concrete examples.',f'Write guidance for someone who wants to {act} for the first time. Explain two useful choices and why they matter.']
  if level in ['A1','A2']:
   prompts=[f'Write about how you can {act}. Give two small steps.',f'Tell a friend about a time you tried to {act}. What did you do? What would you change?',f'Explain two ways to {act}. Which do you like better?',f'Ask a friend to help you {act}. Explain two things you can do together.',f'You want to {act}, but one thing is difficult. Say what it is and give two ways to help.',f'Describe a small change that helps you {act}. Give two examples.',f'Give a new learner two simple tips about how to {act}.']
  c['exercise']=prompts[stage]+' Use four short paragraphs: introduction, two developed points, and conclusion.'
  c['answer']='One possible outline: introduce the situation; discuss '+r1+' with an example; discuss '+r2+' with a different example; conclude by connecting the two points.'
  if level in ['A1','A2']:c['answer']='One possible outline: say what you want to do; explain the first step; explain a different second step; say why the two steps help.'
  c['structure']='State a clear main idea; develop two different points with examples; bring them together in the conclusion.'
 p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
print('Seven writing purposes applied across all levels; approved C1 sample preserved.')
