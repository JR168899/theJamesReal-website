import {KokoroTTS} from './kokoro-local.mjs';
import {env} from '@huggingface/transformers';

env.allowRemoteModels=false;
env.allowLocalModels=true;
env.localModelPath=new URL('./model/',import.meta.url).href;
env.useBrowserCache=true;
env.backends.onnx.wasm.wasmPaths=new URL('./runtime/',import.meta.url).href;
env.backends.onnx.wasm.numThreads=1;
env.backends.onnx.wasm.proxy=false;
const allowed=new Set(['af_heart','af_bella','af_sky','af_aoede','af_kore','af_sarah','am_puck','am_fenrir','am_michael','am_echo','am_onyx','am_liam']);
let engine,queue=Promise.resolve(),generation=0;
function prepare(){
 if(!engine){
  self.postMessage({type:'loading'});
  engine=KokoroTTS.from_pretrained('kokoro',{dtype:'q8',device:'wasm'}).catch(error=>{engine=null;throw error;});
 }
 return engine;
}
self.onmessage=({data})=>{
 if(data.type==='cancel'){generation=data.generation;return;}
 if(data.type!=='generate')return;
 generation=Math.max(generation,data.generation);
 queue=queue.catch(()=>{}).then(async()=>{
  const {id,text,voice,pace,pitch}=data;
  try{
   if(data.generation!==generation){self.postMessage({id,type:'cancelled'});return;}
   if(!allowed.has(voice)||typeof text!=='string'||text.length>400)throw Error('Invalid voice request');
   const tts=await prepare();
   if(data.generation!==generation){self.postMessage({id,type:'cancelled'});return;}
   const ratio=2**((pitch||0)/12);
   const audio=await tts.generate(text,{voice,speed:(pace||1)/ratio});
   const pcm=audio.audio;let peak=0,squares=0;
   for(const sample of pcm){peak=Math.max(peak,Math.abs(sample));squares+=sample*sample;}
   const rms=Math.sqrt(squares/Math.max(pcm.length,1));
   const gain=Math.min(0.95/Math.max(peak,0.001),0.13/Math.max(rms,0.001),2);
   for(let i=0;i<pcm.length;i++)pcm[i]*=gain;
   if(data.generation!==generation){self.postMessage({id,type:'cancelled'});return;}
   self.postMessage({id,type:'audio',pcm,rate:audio.sampling_rate,ratio,voice},[pcm.buffer]);
  }catch(error){self.postMessage({id,type:'error',message:String(error.message||error)});}
 });
};
