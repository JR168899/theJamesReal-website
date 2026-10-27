/* Same-origin, on-device named speech. No lesson text is sent to a voice API. */
(function(){
 'use strict';
 let worker=null,context=null,source=null,generation=0,serial=0,loading=null;
 const pending=new Map(),cache=new Map(),recordings=new Map();
 let turnTimers=[];
 function connect(){
  if(worker)return worker;
  worker=new Worker(new URL('assets/voice-engine/worker.js?v=20261026-named1',document.baseURI),{type:'module'});
  worker.onmessage=({data})=>{
   if(data.type==='loading'){if(loading)loading();return;}
   const item=pending.get(data.id);if(!item)return;pending.delete(data.id);
   if(data.type==='audio')item.resolve(data);
   else item.reject(new Error(data.type==='cancelled'?'cancelled':data.message||'Voice unavailable'));
  };
  worker.onerror=()=>{
   for(const p of pending.values())p.reject(new Error('The selected voices could not load.'));
   pending.clear();worker.terminate();worker=null;
  };
  return worker;
 }
 function stop(){
  generation++;loading=null;
  turnTimers.forEach(clearTimeout);turnTimers=[];
  if(worker)worker.postMessage({type:'cancel',generation});
  if(source){const previous=source;source=null;try{previous.stop();}catch(_){}}
 }
 function request(segment,epoch){
  const key=[segment.voice,segment.pace,segment.pitch,segment.text].join('\0');
  if(cache.has(key))return Promise.resolve(cache.get(key));
  const id=++serial;
  const promise=new Promise((resolve,reject)=>{
   pending.set(id,{resolve,reject});connect().postMessage({type:'generate',id,generation:epoch,...segment});
  });
  return promise.then(audio=>{if(cache.size>=48)cache.delete(cache.keys().next().value);cache.set(key,audio);return audio;});
 }
 async function play(segments,callbacks={}){
  stop();const epoch=generation;
  try{
   const Audio=window.AudioContext||window.webkitAudioContext;
   if(!Audio||!window.Worker)throw new Error('This browser cannot play the selected voices.');
   context=context||new Audio();await context.resume();
   if(epoch!==generation)return;
   loading=callbacks.onLoading||null;
   let next=request(segments[0],epoch);
   for(let i=0;i<segments.length;i++){
    const audio=await next;if(epoch!==generation)return;
    // Generate the next turn while the current speaker is talking.
    next=i+1<segments.length?request(segments[i+1],epoch):null;
    if(next)next.catch(()=>{});
    if(callbacks.onSpeaker)callbacks.onSpeaker(segments[i].name);
    const buffer=context.createBuffer(1,audio.pcm.length,audio.rate);buffer.copyToChannel(audio.pcm,0);
    await new Promise(resolve=>{
     const current=context.createBufferSource();current.buffer=buffer;current.playbackRate.value=audio.ratio;
     current.connect(context.destination);source=current;
     current.onended=()=>{current.disconnect();if(source===current)source=null;resolve();};current.start();
    });
    if(epoch!==generation)return;
   }
   loading=null;if(callbacks.onFinished)callbacks.onFinished();
  }catch(error){if(epoch===generation&&callbacks.onError)callbacks.onError(error);}
 }
 function prepareFile(url){
  if(!recordings.has(url)){
   const promise=fetch(url).then(response=>{if(!response.ok)throw Error('Recording unavailable');return response.arrayBuffer();}).then(bytes=>{
    const Decoder=window.OfflineAudioContext||window.webkitOfflineAudioContext;
    return new Decoder(1,1,24000).decodeAudioData(bytes);
   });
   recordings.set(url,promise);promise.catch(()=>recordings.delete(url));
  }
  return recordings.get(url);
 }
 async function playFile(url,callbacks={},turns=[]){
  stop();const epoch=generation;
  try{
   const Audio=window.AudioContext||window.webkitAudioContext;
   context=context||new Audio();await context.resume();
   const buffer=await prepareFile(url);if(epoch!==generation)return;
   const current=context.createBufferSource();current.buffer=buffer;current.connect(context.destination);source=current;
   current.onended=()=>{current.disconnect();if(source===current)source=null;if(epoch===generation&&callbacks.onFinished)callbacks.onFinished();};
   current.start();
   if(turns.length)turns.forEach(turn=>{if(turn.start===0){callbacks.onSpeaker?.(turn.name);return;}turnTimers.push(setTimeout(()=>{if(epoch===generation)callbacks.onSpeaker?.(turn.name);},turn.start*1000));});
   else callbacks.onSpeaker?.('Aoede');
  }catch(error){if(epoch===generation)callbacks.onError?.(error);}
 }
 window.JRVoicePlayer=Object.freeze({play,stop,prepareFile,playFile});
})();
