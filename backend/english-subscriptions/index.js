import {neon} from '@neondatabase/serverless';
import {parseTriggerDelivery} from '@neon/functions/triggers';
import {createHash,createHmac,randomBytes,timingSafeEqual} from 'node:crypto';

const SITE='https://www.thejamesreal.com';
const FROM='EverydayEnglish <EverydayEnglish@thejamesreal.com>';
const LEVELS=['A1','A2','B1','B2','C1','C2'];
const db=()=>neon(process.env.DATABASE_URL).query;
const hash=x=>createHash('sha256').update(x).digest('hex');
const sign=email=>createHmac('sha256',process.env.SIGNING_SECRET).update(email).digest('base64url');
const escape=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text=x=>Array.isArray(x)?x.join('; '):String(x??'');
const pacific=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
const base=request=>process.env.PUBLIC_API_URL||new URL(request.url).origin;
const link=(day,level)=>SITE+'/?jr-date='+day+'&jr-level='+level+'#english';
function headers(request){
 const origin=request.headers.get('origin');const h={'Content-Type':'application/json','Cache-Control':'no-store','Vary':'Origin','X-Content-Type-Options':'nosniff'};
 if(origin===SITE||origin==='https://thejamesreal.com'){h['Access-Control-Allow-Origin']=origin;h['Access-Control-Allow-Methods']='POST,GET,OPTIONS';h['Access-Control-Allow-Headers']='Content-Type';}
 return h;
}
const json=(request,value,status=200)=>Response.json(value,{status,headers:headers(request)});
const isAdmin=request=>{
 const expected=process.env.ADMIN_SECRET||'';const got=request.headers.get('authorization')||'';
 return expected.length>20&&Buffer.byteLength(got)===Buffer.byteLength('Bearer '+expected)&&timingSafeEqual(Buffer.from(got),Buffer.from('Bearer '+expected));
};
function page(title,body,status=200){
 return new Response('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>body{font:18px/1.6 system-ui;background:#111610;color:#eee5d2;max-width:620px;margin:60px auto;padding:24px}h1{font:38px Georgia;color:#d2ba7d}button,a{color:#dbc48b}button{background:#252d22;border:1px solid #a18f63;padding:14px 22px;font:inherit;cursor:pointer}label{display:block;margin:12px 0}</style><h1>'+escape(title)+'</h1>'+body+'<p><a href="'+SITE+'/#english">Everyday English</a></p></html>',{status,headers:{'Content-Type':'text/html;charset=utf-8','Cache-Control':'no-store','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'"}});
}
async function sendMail({to,subject,html,text:plain,key,unsubscribe}){
 if(!process.env.RESEND_API_KEY)throw new Error('mail_not_configured');
 const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:'Bearer '+process.env.RESEND_API_KEY,'Content-Type':'application/json','Idempotency-Key':key},body:JSON.stringify({from:FROM,to:[to],reply_to:'JamesReal.Public@gmail.com',subject,html,text:plain,...(unsubscribe?{headers:{'List-Unsubscribe':'<'+unsubscribe+'>','List-Unsubscribe-Post':'List-Unsubscribe=One-Click'}}:{})})});
 if(!response.ok)throw new Error('mail_provider_'+response.status);
 const result=await response.json();return result.id;
}
function shell(title,body,unsubscribe){
 return '<!doctype html><html lang="en"><meta charset="utf-8"><body style="margin:0;background:#121710;font-family:Arial,sans-serif"><table role="presentation" width="100%"><tr><td align="center"><table role="presentation" width="660" style="max-width:100%;background:#f5f0e5"><tr><td style="padding:30px;color:#282d24"><p style="font-size:13px;letter-spacing:2px">EVERYDAY ENGLISH</p><h1 style="font-family:Georgia;font-size:30px">'+escape(title)+'</h1>'+body+(unsubscribe?'<p style="font-size:12px;margin-top:30px">You requested this level of Everyday English. <a href="'+escape(unsubscribe)+'">Manage levels or unsubscribe</a>.</p>':'')+'</td></tr></table></td></tr></table></body></html>';
}
function cardHTML(card,day,level){
 const colors={vocabulary:'#efd6d5',phrases:'#f1dfcf',idioms:'#efe6bd',daily:'#dce6d8',reflection:'#dce5ee',grammar:'#e7dfec',smalltalk:'#e3e1df',essay:'#f1eadc'};
 const names={vocabulary:'Vocabulary',phrases:'Phrasal verb',idioms:'Idioms & slang',daily:'Life phrases',reflection:'Quote',grammar:'Grammar',smalltalk:'Small talk',essay:'Essay'};
 const photo=card.photoCredit;let body='';
 if(photo)body+='<img alt="'+escape(card.illustrationAlt)+'" src="'+SITE+'/'+escape(photo.asset)+'" width="'+(card.type==='essay'?210:560)+'" style="display:block;width:'+(card.type==='essay'?'210px':'100%')+';max-width:100%;height:auto"><p style="font-size:10px"><a href="'+escape(photo.sourceURL)+'">'+escape(photo.credit)+'</a></p>';
 body+='<h2 style="font-size:26px;line-height:1.2">'+escape(card.title).replaceAll('\n','<br>')+'</h2>';
 if(card.ipa)body+='<p>'+escape(card.ipa)+' · '+escape(card.partOfSpeech)+'<br>'+escape(card.wordForms)+'</p>';
 if(card.quoteAuthor)body+='<p style="font-size:14px"><a href="'+escape(card.quoteSourceURL)+'">'+escape(card.quoteAuthor)+' · '+escape(card.quoteWork)+' · Published '+card.quoteYear+'</a></p>';
 if(card.type==='essay'){
  const roles=['INTRODUCTION','DEVELOP THE IDEA','EXAMPLE & REFLECTION','CONCLUSION'];
  card.paragraphs.forEach((p,i)=>{body+='<h3 style="font-size:12px">'+(i+1)+' · '+roles[i]+'</h3><p>'+escape(p)+'</p>';});
 }else{
  for(const[field,title]of [['meaning','Meaning'],['synonyms','Synonyms'],['example','In context'],['notes','Usage note'],['conversation','Conversation']]){
   if(card[field])body+='<h3 style="font-size:12px;text-transform:uppercase;margin-bottom:2px">'+title+'</h3><p style="margin-top:2px;white-space:pre-line">'+escape(text(card[field]))+'</p>';
  }
 }
 body+='<h3 style="font-size:12px">YOUR TURN</h3><p>'+escape(card.exercise)+'</p><p><a href="'+link(day,level)+'">Open the card, listen & check the model answer ↗</a></p>';
 return '<section style="background:'+colors[card.type]+';border:1px solid #948a76;border-radius:4px;margin:24px 0;padding:20px;color:#302e29;line-height:1.5"><p style="font-size:11px">Everyday English - '+level+' - '+day.replaceAll('-','/')+' - '+String(card.categoryNumber).padStart(2,'0')+' - '+names[card.type]+'</p>'+body+'</section>';
}
async function editionEmail(email,level,day,api,key){
 const response=await fetch(SITE+'/data/english-levels/'+day+'.json',{headers:{'Cache-Control':'no-cache'}});
 if(!response.ok)throw new Error('edition_unavailable');
 const unit=(await response.json())[level];if(unit?.cards?.length!==11)throw new Error('edition_incomplete');
 const unsubscribe=api+'/unsubscribe?token='+encodeURIComponent(sign(email));
 const title=level+' · '+day+' · '+unit.theme;
 const intro='<p>Your eleven cards for today are below. Read at your own pace, then try the questions.</p><p><a href="'+link(day,level)+'">Open today’s '+level+' edition & listen ↗</a></p>';
 const html=shell(title,intro+unit.cards.map(c=>cardHTML(c,day,level)).join(''),unsubscribe);
 const plain=title+'\n\n'+unit.cards.map(c=>c.title+'\n'+(c.paragraphs?c.paragraphs.join('\n\n'):c.meaning+'\n'+c.example)).join('\n\n')+'\n\nRead and listen: '+link(day,level)+'\nManage subscription: '+unsubscribe;
 return sendMail({to:email,subject:'Everyday English - '+level+' - '+day.replaceAll('-','/')+' - 11 cards',html,text:plain,key,unsubscribe});
}
async function subscribe(request){
 if(![SITE,'https://thejamesreal.com'].includes(request.headers.get('origin')))return json(request,{error:'origin_not_allowed'},403);
 if(!request.headers.get('content-type')?.includes('application/json'))return json(request,{error:'json_required'},415);
 if(Number(request.headers.get('content-length')||0)>4096)return json(request,{error:'request_too_large'},413);
 const raw=await request.text();if(raw.length>4096)return json(request,{error:'request_too_large'},413);
 const body=JSON.parse(raw);const email=String(body.email||'').trim().toLowerCase();
 const levels=[...new Set(Array.isArray(body.levels)?body.levels:[])].filter(l=>LEVELS.includes(l));
 if(body.website)return json(request,{ok:true,message:'If the address can receive email, a confirmation message will arrive shortly.'});
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||email.length>254||!levels.length||body.consent!==true)return json(request,{error:'Enter a valid email, select a level and confirm your consent.'},400);
 if(!process.env.RESEND_API_KEY)return json(request,{error:'Email subscriptions are temporarily unavailable. Please try again later.'},503);
 const rateHash=hash((request.headers.get('x-forwarded-for')||'unknown').split(',')[0]+process.env.SIGNING_SECRET);
 const counts=await db()("INSERT INTO jamesreal_mail.rate_limits(request_hash,hour) VALUES($1,date_trunc('hour',now())) ON CONFLICT(request_hash,hour) DO UPDATE SET count=rate_limits.count+1 RETURNING count",[rateHash]);
 if(counts[0].count>8)return json(request,{error:'Please wait before requesting another confirmation.'},429);
 const recent=await db()("SELECT count(*)::int AS count FROM jamesreal_mail.requests WHERE email=$1 AND created_at>now()-interval '1 hour'",[email]);
 if(recent[0].count>=3)return json(request,{ok:true,message:'Please check your inbox for the existing confirmation message.'});
 const token=randomBytes(32).toString('base64url');const tokenHash=hash(token);
 await db()("INSERT INTO jamesreal_mail.requests(token_hash,email,levels,expires_at) VALUES($1,$2,$3,now()+interval '24 hours')",[tokenHash,email,levels]);
 const confirm=base(request)+'/confirm?token='+token;
 await sendMail({to:email,subject:'Confirm your Everyday English levels: '+levels.join(', '),key:'confirm-'+tokenHash,html:shell('Confirm your daily practice','<p>You selected '+levels.map(escape).join(', ')+'. Each selected level arrives as a separate email at around 7 a.m. Pacific Time.</p><p><a href="'+confirm+'">Confirm my subscription</a></p><p>This link expires in 24 hours. If you did not request these lessons, ignore this message.</p>'),text:'Confirm '+levels.join(', ')+': '+confirm});
 return json(request,{ok:true,message:'Check your email to confirm your selected levels. Each level will arrive in a separate daily email.'});
}
async function confirmation(request,url){
 const token=url.searchParams.get('token')||'';if(token.length!==43)return page('Link unavailable','<p>Please request a new confirmation link.</p>',400);
 const rows=await db()("SELECT email,levels,used_at FROM jamesreal_mail.requests WHERE token_hash=$1 AND expires_at>now()",[hash(token)]);
 if(!rows.length||rows[0].used_at)return page('Link unavailable','<p>This confirmation has expired or was already used. You can request another link on the website.</p>',410);
 const pending=rows[0];
 if(request.method==='GET')return page('Confirm your levels','<p>Your selected levels: '+pending.levels.map(escape).join(', ')+'. Each level arrives separately.</p><form method="post"><button>Confirm subscription</button></form>');
 if(request.method!=='POST')return new Response('Method not allowed',{status:405});
 const unsubscribeHash=hash(sign(pending.email));
 const saved=await db()("WITH used AS (UPDATE jamesreal_mail.requests SET used_at=now() WHERE token_hash=$1 AND used_at IS NULL AND expires_at>now() RETURNING email,levels) INSERT INTO jamesreal_mail.subscribers(email,levels,active,confirmed_at,unsubscribe_hash) SELECT email,levels,true,now(),$2 FROM used ON CONFLICT(email) DO UPDATE SET levels=EXCLUDED.levels,active=true,confirmed_at=now(),unsubscribe_hash=EXCLUDED.unsubscribe_hash,updated_at=now() RETURNING levels",[hash(token),unsubscribeHash]);
 if(!saved.length)return page('Already used','<p>Please request another confirmation if you need to change your levels.</p>',410);
 return page('You’re subscribed','<p>Your levels: '+saved[0].levels.map(escape).join(', ')+'. Each selected level arrives in its own daily email. You can change levels or unsubscribe using the link in any lesson.</p>');
}
async function unsubscribe(request,url){
 const token=url.searchParams.get('token')||'';if(token.length!==43)return page('Link unavailable','<p>Please use the subscription link in your email.</p>',400);
 const rows=await db()("SELECT id,levels,active FROM jamesreal_mail.subscribers WHERE unsubscribe_hash=$1",[hash(token)]);
 if(!rows.length)return page('Link unavailable','<p>Please use the subscription link in your latest email.</p>',404);
 const sub=rows[0];
 if(request.method==='GET')return page('Manage your practice','<p>Select the levels you want to keep, then save. Clear all levels to unsubscribe.</p><form method="post">'+LEVELS.map(l=>'<label><input type="checkbox" name="levels" value="'+l+'" '+(sub.active&&sub.levels.includes(l)?'checked':'')+'> '+l+'</label>').join('')+'<button>Save preferences</button></form>');
 if(request.method!=='POST')return new Response('Method not allowed',{status:405});
 const body=await request.formData();const oneClick=body.get('List-Unsubscribe')==='One-Click';
 const levels=oneClick?[]:[...new Set(body.getAll('levels'))].filter(l=>LEVELS.includes(l));
 if(levels.length)await db()("UPDATE jamesreal_mail.subscribers SET levels=$2,active=true,updated_at=now() WHERE id=$1",[sub.id,levels]);
 else await db()("UPDATE jamesreal_mail.subscribers SET active=false,updated_at=now() WHERE id=$1",[sub.id]);
 return page(levels.length?'Preferences saved':'You’re unsubscribed','<p>'+(levels.length?'Your selected levels will arrive separately: '+levels.join(', ')+'.':'Daily lessons have stopped. You can subscribe again whenever you wish.')+'</p>');
}
async function dispatch(request,force=false){
 const now=new Date();const hour=Number(new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',hour:'2-digit',hourCycle:'h23'}).format(now));
 if(!force&&(hour<7||hour>=9))return {skipped:'outside_delivery_window'};
 const day=pacific();if(!/^2026-/.test(day))return {skipped:'no_prepared_edition'};
 await db()("INSERT INTO jamesreal_mail.deliveries(subscriber_id,edition_date,level) SELECT s.id,$1::date,l FROM jamesreal_mail.subscribers s CROSS JOIN LATERAL unnest(s.levels) l WHERE s.active ON CONFLICT DO NOTHING",[day]);
 const jobs=await db()("WITH chosen AS (SELECT d.id FROM jamesreal_mail.deliveries d JOIN jamesreal_mail.subscribers s ON s.id=d.subscriber_id WHERE s.active AND d.edition_date=$1::date AND d.status<>'sent' AND d.attempts<5 AND (d.lease_until IS NULL OR d.lease_until<now()) ORDER BY d.level,d.id LIMIT 20 FOR UPDATE OF d SKIP LOCKED) UPDATE jamesreal_mail.deliveries d SET status='sending',attempts=attempts+1,lease_until=now()+interval '10 minutes' FROM chosen WHERE d.id=chosen.id RETURNING d.id,d.subscriber_id,d.level",[day]);
 let sent=0,failed=0;
 for(const job of jobs){
  const rows=await db()("SELECT email FROM jamesreal_mail.subscribers WHERE id=$1 AND active AND $2=ANY(levels)",[job.subscriber_id,job.level]);
  if(!rows.length)continue;
  try{
   const id=await editionEmail(rows[0].email,job.level,day,base(request),'daily-'+job.id);
   await db()("UPDATE jamesreal_mail.deliveries SET status='sent',provider_id=$2,sent_at=now(),lease_until=NULL,last_error=NULL WHERE id=$1",[job.id,id]);sent++;
  }catch(error){
   const safe=/^mail_provider_\d+$|^edition_unavailable$|^edition_incomplete$|^mail_not_configured$/.test(error.message)?error.message:'delivery_error';
   await db()("UPDATE jamesreal_mail.deliveries SET status='failed',last_error=$2,lease_until=now()+interval '15 minutes' WHERE id=$1",[job.id,safe]);failed++;
  }
  await new Promise(resolve=>setTimeout(resolve,600));
 }
 return {date:day,sent,failed};
}
export default {async fetch(request){
 const url=new URL(request.url);
 try{
  if(request.method==='OPTIONS')return new Response(null,{status:204,headers:headers(request)});
  if(url.pathname==='/health')return json(request,{ok:true,mailConfigured:Boolean(process.env.RESEND_API_KEY),signingConfigured:Boolean(process.env.SIGNING_SECRET),sender:FROM,levels:LEVELS,deliveryTime:'07:00 America/Los_Angeles'});
  if(url.pathname==='/subscribe'&&request.method==='POST')return await subscribe(request);
  if(url.pathname==='/confirm')return await confirmation(request,url);
  if(url.pathname==='/unsubscribe')return await unsubscribe(request,url);
  if(url.pathname==='/cron'&&request.method==='POST'){
   const parsed=await parseTriggerDelivery(request);
   if(!parsed.ok||parsed.invocation.type!=='schedule')return json(request,{error:'unauthorized_trigger'},401);
   return json(request,await dispatch(request));
  }
  if(url.pathname==='/admin/run'&&request.method==='POST'){
   if(!isAdmin(request))return json(request,{error:'unauthorized'},401);
   return json(request,await dispatch(request,true));
  }
  if(url.pathname==='/admin/test'&&request.method==='POST'){
   if(!isAdmin(request))return json(request,{error:'unauthorized'},401);
   const day=pacific();let sent=0;const run=randomBytes(12).toString('hex');
   for(const level of LEVELS){await editionEmail('JamesReal.Public@gmail.com',level,day,base(request),'test-'+run+'-'+level);sent++;await new Promise(r=>setTimeout(r,600));}
   return json(request,{ok:true,date:day,sent,levels:LEVELS});
  }
  return json(request,{error:'not_found'},404);
 }catch(error){ const safe=/^mail_provider_\d+$|^edition_unavailable$|^edition_incomplete$|^mail_not_configured$/.test(error.message)?error.message:'request_error'; return json(request,{error:isAdmin(request)?safe:'The request could not be completed. Please try again later.'},500); }
}};
