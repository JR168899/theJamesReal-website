import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const sandbox={window:{}};vm.createContext(sandbox);
for(const f of ['voice-pairs.js','english-voice-routing.js'])vm.runInContext(fs.readFileSync('dist/'+f,'utf8'),sandbox);
const routing=sandbox.window.JREnglishVoiceRouting,pairs=sandbox.window.JR_ENGLISH_SPEAKERS;
let cards=0,actions=0,maleTurns=0;const counts={};
for(const file of fs.readdirSync('dist/data/english-levels').filter(f=>/^2026-.*\.json$/.test(f))){
 for(const [level,unit] of Object.entries(JSON.parse(fs.readFileSync('dist/data/english-levels/'+file)))){
  const pair=pairs[level];counts[level]=(counts[level]||0)+unit.cards.length;
  for(const c of unit.cards){
   assert.deepEqual(JSON.parse(JSON.stringify(pair)),c.speakers,c.id+' pair');
   assert(!/(^|\n)[AB]:/.test(c.conversation||''),c.id+' anonymous labels');
   const turns=routing.turns(c);
   for(const t of turns){
    if(t.voice.startsWith('am_')){assert.equal(t.name,pair.partner.name);assert.equal(t.role,'partner');assert(!routing.isNarrative(c));maleTurns++;}
    else assert.equal(t.name,pair.teacher.name);
   }
   const sections=Object.entries(c).filter(([k,v])=>['meaning','notes','example','quoteBackground','quoteCloserLook','exercise'].includes(k)&&v).map(([k,v])=>[k,v]);
   if(c.conversation)sections.push(['Conversation',c.conversation]);
   for(const action of ['speak-title','speak-conversation','speak-all']){
    const segments=routing.segments(c,action,sections,c.exercise);actions++;
    if(action==='speak-title'||routing.isNarrative(c))assert(segments.every(s=>s.voice===pair.teacher.voice),c.id+' female-only '+action);
    for(const s of segments){assert.equal(s.pace,pair.teacher.pace);if(s.voice.startsWith('am_')){assert.equal(s.role,'partner');assert.equal(s.voice,pair.partner.voice);assert(turns.some(t=>t.role==='partner'&&t.text.includes(s.text)));}}
    if(!routing.isNarrative(c)&&c.conversation&&action!=='speak-title')assert(segments.some(s=>s.voice===pair.partner.voice),c.id+' missing B');
   }
   for(const key of ['poster','downloadPoster']){const svg=fs.readFileSync('dist/'+c[key],'utf8');assert(!/>[AB]:/.test(svg),c.id+' SVG labels');if(c.conversation){assert(svg.includes(pair.teacher.name+':'),c.id+' teacher name');assert(svg.includes(pair.partner.name+':'),c.id+' partner name');}}
   cards++;
  }
 }
}
assert.equal(cards,24090);assert.equal(actions,72270);console.log(JSON.stringify({passed:true,cards,actions,maleTurns,levels:counts,policy:'Female narration; male voice only for dialogue B; Quote and Essay female only.'}));
