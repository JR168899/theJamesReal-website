/* Fixed-voice listening trial is confined to the October 27 edition. */
(function(){
 const date=new URLSearchParams(location.search).get('jr-date')||window.jrToday?.()||new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
 const trial=date==='2026-10-27';
 document.write('<script src="'+(trial?'english-listening-preview.js?v=oct27-six2':'english-levels.js?v=20261026-editorial')+'"><\/script>');
 document.addEventListener('change',event=>{
  if(!event.target.matches('#jr-english [data-jr-date]'))return;
  if(!window.JR_ENGLISH_DATES?.includes(event.target.value))return;
  if((event.target.value==='2026-10-27')===trial)return;
  const url=new URL(location.href);url.searchParams.set('jr-date',event.target.value);url.hash='english';event.stopImmediatePropagation();location.assign(url);
 },true);
})();
