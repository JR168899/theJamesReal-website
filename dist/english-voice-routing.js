/* One role policy for every level and date. Only dialogue B uses the male voice. */
(function(){
 'use strict';
 const asText=v=>Array.isArray(v)?v.join(' '):String(v||'');
 const narrative=c=>['reflection','quote','essay'].includes(c.type||c.image);
 function pairFor(card){
  const level=card.level||/-(A1|A2|B1|B2|C1|C2)-/.exec(card.id||'')?.[1];
  const pair=window.JR_ENGLISH_SPEAKERS?.[level];
  if(!pair||!pair.teacher.voice.startsWith('af_')||!pair.partner.voice.startsWith('am_'))throw Error('Invalid lesson voice pair');
  return pair;
 }
 function turns(card){
  const pair=pairFor(card),old=card.speakers;
  return asText(card.conversation).replace(/\\n/g,'\n').split('\n').filter(s=>s.trim()).map(line=>{
   const match=/^\s*([^:]+):\s*(.*)$/.exec(line),name=match?.[1].trim();
   const male=!narrative(card)&&['B',pair.partner.name,old?.partner?.name].filter(Boolean).includes(name);
   return {role:male?'partner':'teacher',...pair[male?'partner':'teacher'],text:match?match[2]:line};
  });
 }
 function segments(card,action,sections=[],exercise=''){
  const pair=pairFor(card),out=[];
  function add(copy,speaker=pair.teacher){
   let chunk='';for(const word of asText(copy).split(/\s+/).filter(Boolean)){
    if(chunk&&chunk.length+word.length+1>220){out.push({...speaker,text:chunk});chunk='';}chunk+=(chunk?' ':'')+word;
   }if(chunk)out.push({...speaker,text:chunk});
  }
  function dialogue(){for(const turn of turns(card))add(turn.text,turn);}
  if(action==='speak-title')add(card.title);
  else if(action==='speak-conversation')dialogue();
  else if((card.type||card.image)==='essay'){
   [card.title,...(card.paragraphs||[]).map(asText),card.structure,exercise].filter(Boolean).forEach(x=>add(x));
  }else{
   add(card.title);if((card.type||card.image)==='vocabulary'){add(card.partOfSpeech);add(card.wordForms);}if(card.quoteBackground)add(card.attribution);
   for(const [label,copy] of sections){add(label+'.');if(label==='Conversation')dialogue();else add(copy);}
  }
  return out;
 }
 window.JREnglishVoiceRouting=Object.freeze({pairFor,turns,segments,isNarrative:narrative});
})();
