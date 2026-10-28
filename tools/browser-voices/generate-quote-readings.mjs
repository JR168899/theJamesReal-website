import {KokoroTTS} from 'kokoro-js';
import {readFile,mkdir,writeFile,access} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const repo=pathToFileURL(resolve(process.cwd())+'/'),batchPath=process.argv[2]||'content/quote-reading-batch-001.json',batch=JSON.parse(await readFile(new URL(batchPath,repo),'utf8')),day=batch.date;
const scratch=resolve(process.env.JR_AUDIO_SCRATCH||'.cache/quote-audio');await mkdir(scratch,{recursive:true});
const tts=await KokoroTTS.from_pretrained('onnx-community/Kokoro-82M-v1.0-ONNX',{dtype:'q8',device:'cpu'});
function clean(pcm,rate,ratio){
 let start=0,end=pcm.length-1;while(start<end&&Math.abs(pcm[start])<.007)start++;while(end>start&&Math.abs(pcm[end])<.007)end--;
 start=Math.max(0,start-Math.round(rate*.035));end=Math.min(pcm.length,end+Math.round(rate*.065));
 const size=Math.ceil((end-start)/ratio),a=new Float32Array(size);let peak=0,sq=0;
 for(let i=0;i<size;i++){let p=start+i*ratio,k=Math.floor(p),f=p-k;a[i]=(pcm[k]||0)*(1-f)+(pcm[k+1]||0)*f;peak=Math.max(peak,Math.abs(a[i]));sq+=a[i]*a[i];}
 const gain=Math.min(.95/Math.max(peak,.001),.13/Math.max(Math.sqrt(sq/size),.001),2);
 for(let i=0;i<size;i++)a[i]*=gain;return a;
}
function wav(chunks,rate,gap=.16){
 const n=chunks.reduce((n,c)=>n+c.length,0)+Math.round(gap*rate)*Math.max(0,chunks.length-1),b=Buffer.alloc(44+n*2);
 b.write('RIFF');b.writeUInt32LE(36+n*2,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(rate,24);b.writeUInt32LE(rate*2,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n*2,40);
 let pos=44;for(let j=0;j<chunks.length;j++){for(const x of chunks[j]){b.writeInt16LE(Math.round(Math.max(-1,Math.min(1,x))*32767),pos);pos+=2;}if(j<chunks.length-1)pos+=Math.round(gap*rate)*2;}return b;
}
async function speak(text,speaker){const ratio=2**((speaker.pitch||0)/12);const a=await tts.generate(text,{voice:speaker.voice,speed:speaker.pace/ratio});return {pcm:clean(a.audio,a.sampling_rate,ratio),rate:a.sampling_rate};}


function split(copy){let out=[],current='';for(const sentence of copy.match(/[^.!?]+[.!?]+|[^.!?]+$/g)||[]){for(const word of sentence.trim().split(/\s+/)){if(current.length+word.length>220){out.push(current);current='';}current+=(current?' ':'')+word;}if(current.length>150){out.push(current);current='';}}if(current)out.push(current);return out;}
const pairs=JSON.parse(await readFile(new URL('content/voice-pairs.json',repo),'utf8'));
for(const level of Object.keys(batch.cards)){
 const dataPath=new URL(`dist/data/english-levels/${day}.json`,repo),data=JSON.parse(await readFile(dataPath,'utf8')),c=data[level].cards.find(x=>x.type==='reflection'),speaker=pairs[level].teacher;
 const pieces=[c.title,c.attribution,'The story. '+c.quoteBackground,'A closer look. '+c.quoteCloserLook,'Your turn. '+c.exercise],hash=createHash('sha256').update(JSON.stringify({pieces,speaker,codec:'aac-mono-48k-v1'})).digest('hex'),base=c.id+'-'+hash.slice(0,12),out=new URL(`dist/assets/lesson-audio/${day}/${level}/`,repo);await mkdir(out,{recursive:true});
 const title=await speak(c.title,speaker),chunks=[];
 for(const piece of pieces)for(const part of split(piece)){const a=await speak(part,speaker);chunks.push(a.pcm);}
 const readingDuration=(chunks.reduce((n,a)=>n+a.length,0)+Math.round(.18*title.rate)*(chunks.length-1))/title.rate;
 for(const [kind,pcm] of [['title',wav([title.pcm],title.rate)],['reading',wav(chunks,title.rate,.18)]]){
  const raw=resolve(scratch,base+'-'+kind+'.wav'),target=fileURLToPath(new URL(base+'-'+kind+'.m4a',out));await writeFile(raw,pcm);
  try{await access(target);}catch{execFileSync('/usr/bin/afconvert',['-f','m4af','-d','aac','-b','48000','-q','127',raw,target]);}
 }
 const entry={title:`assets/lesson-audio/${day}/${level}/${base}-title.m4a`,reading:`assets/lesson-audio/${day}/${level}/${base}-reading.m4a`,readingVoice:speaker.voice,readingPace:speaker.pace,readingDuration,sourceHash:hash};
 let manifest;const mf=new URL('manifest.json',out);try{manifest=JSON.parse(await readFile(mf,'utf8'));}catch{manifest={date:day,level,cards:{}};}
 manifest.cards[c.id]=entry;manifest.version='prepared-quote-reading-v2';await writeFile(mf,JSON.stringify(manifest));
 const latest=JSON.parse(await readFile(dataPath,'utf8')),card=latest[level].cards.find(x=>x.id===c.id);card.quoteAudio={title:entry.title,reading:entry.reading,voice:speaker.voice,name:speaker.name,pace:speaker.pace,sourceHash:hash,duration:readingDuration};card.speakers=pairs[level];await writeFile(dataPath,JSON.stringify(latest)+'\n');console.log('Prepared female AAC reading:',day,level,Math.round(readingDuration)+'s');
}
console.log('Quote narration batch complete');
