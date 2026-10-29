/* Local reading preferences. No account, email or tracking data is stored. */
(function(){
 'use strict';
 const levels=['A1','A2','B1','B2','C1','C2'],key='james-real-english-level-v1';
 function today(now=new Date()){
  const parts=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(now).map(p=>[p.type,p.value]));
  return parts.year+'-'+parts.month+'-'+parts.day;
 }
 function availableToday(dates,now=new Date()){
  const day=today(now),ordered=dates.slice().sort();
  return ordered.filter(d=>d<=day).at(-1)||ordered[0];
 }
 function remembered(storage){try{const value=(storage||window.localStorage).getItem(key);return levels.includes(value)?value:'A1';}catch{return 'A1';}}
 function remember(level,storage){if(!levels.includes(level))return false;try{(storage||window.localStorage).setItem(key,level);return true;}catch{return false;}}
 function initial(params,dates,storage,now=new Date()){
  const requested=params.get('jr-date'),explicit=dates.includes(requested),requestedLevel=params.get('jr-level');
  return {date:explicit?requested:availableToday(dates,now),level:levels.includes(requestedLevel)?requestedLevel:remembered(storage),followToday:!explicit};
 }
 window.JREnglishSelection=Object.freeze({today,availableToday,remembered,remember,initial});
 window.jrToday=today;
})();
