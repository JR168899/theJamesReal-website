import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const memory=new Map(),storage={getItem:k=>memory.get(k)||null,setItem:(k,v)=>memory.set(k,v)};
const context={window:{localStorage:storage},Intl,Date};vm.createContext(context);vm.runInContext(fs.readFileSync('dist/english-selection.js','utf8'),context);const s=context.window.JREnglishSelection;
const dates=Array.from({length:365},(_,i)=>new Date(Date.UTC(2026,0,i+1)).toISOString().slice(0,10));
const now=new Date('2026-10-29T06:59:00Z'),params=x=>new URLSearchParams(x);
assert.equal(s.today(now),'2026-10-28');assert.equal(s.today(new Date('2026-10-29T07:01:00Z')),'2026-10-29');
assert.equal(s.today(new Date('2026-11-02T07:59:00Z')),'2026-11-01');assert.equal(s.today(new Date('2026-11-02T08:01:00Z')),'2026-11-02');
assert.equal(s.initial(params(''),dates,storage,now).date,'2026-10-28');assert.equal(s.initial(params(''),dates,storage,now).level,'A1');
for(const level of ['A1','A2','B1','B2','C1','C2']){assert(s.remember(level,storage));assert.equal(s.initial(params(''),dates,storage,now).level,level);}
assert.equal(s.initial(params('jr-date=2026-05-21&jr-level=B2'),dates,storage,now).date,'2026-05-21');assert.equal(s.initial(params('jr-date=2026-05-21&jr-level=B2'),dates,storage,now).level,'B2');assert.equal(s.initial(params('jr-date=2026-05-21'),dates,storage,now).followToday,false);
assert.equal(s.initial(params('jr-date=bad&jr-level=bad'),dates,storage,now).date,'2026-10-28');assert.equal(s.initial(params('jr-level=bad'),dates,storage,now).level,'C2');
const denied={getItem(){throw Error('denied');},setItem(){throw Error('denied');}};assert.equal(s.remembered(denied),'A1');assert.equal(s.remember('B2',denied),false);assert.equal(s.remember('X1',storage),false);
assert.equal(s.availableToday(dates,new Date('2027-01-05T12:00:00Z')),'2026-12-31');assert.equal(s.availableToday(dates,new Date('2025-12-01T12:00:00Z')),'2026-01-01');
console.log('PASS: Pacific midnight/DST, today default, all six remembered levels, explicit archive links, invalid input, unavailable storage and archive boundaries.');
