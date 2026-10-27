import {readFile,writeFile,mkdir,copyFile,readdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {dirname,resolve,join} from 'node:path';
import {createHash} from 'node:crypto';
import {build} from 'esbuild';
const here=dirname(fileURLToPath(import.meta.url)),root=resolve(here,'../..'),out=join(root,'dist/assets/voice-engine');
await mkdir(out,{recursive:true});
const entry=fileURLToPath(import.meta.resolve('kokoro-js'));
let source=await readFile(entry,'utf8');
const remote='`https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main/voices/${e}.bin`';
if(!source.includes(remote))throw Error('Upstream voice loader changed; review local asset patch');
source=source.replace(remote,'new URL("./voices/"+e+".bin",import.meta.url).href');
await writeFile(join(here,'kokoro-local.mjs'),source);
await build({entryPoints:[join(here,'worker.mjs')],outfile:join(out,'worker.js'),bundle:true,format:'esm',platform:'browser',target:'es2022',minify:true,legalComments:'eof',plugins:[{name:'node-only-stubs',setup(b){b.onResolve({filter:/^(path|fs\/promises)$/},args=>({path:args.path,namespace:'empty-node'}));b.onLoad({filter:/.*/,namespace:'empty-node'},()=>({contents:'export default {};',loader:'js'}));}}]});
const voices=['af_heart','af_bella','af_sky','af_aoede','af_kore','af_sarah','am_puck','am_fenrir','am_michael','am_echo','am_onyx','am_liam'];
const kokoroRoot=resolve(dirname(entry),'..');
await mkdir(join(out,'voices'),{recursive:true});
for(const v of voices)await copyFile(join(kokoroRoot,'voices',v+'.bin'),join(out,'voices',v+'.bin'));
const ortRoot=resolve(here,'node_modules/onnxruntime-web/dist');
await mkdir(join(out,'runtime'),{recursive:true});
for(const f of await readdir(ortRoot))if(/^ort-wasm.*\.(wasm|mjs)$/.test(f))await copyFile(join(ortRoot,f),join(out,'runtime',f));
const seed=process.env.JR_KOKORO_MODEL_CACHE||resolve(root,'../../work/voice-preview/node_modules/@huggingface/transformers/.cache/onnx-community/Kokoro-82M-v1.0-ONNX');
const files=['config.json','tokenizer_config.json','tokenizer.json','onnx/model_quantized.onnx'];
await mkdir(join(out,'model/kokoro/onnx'),{recursive:true});
const hashes={};
for(const file of files){
 const bytes=await readFile(join(seed,file));
 await writeFile(join(out,'model/kokoro',file),bytes);hashes[file]=createHash('sha256').update(bytes).digest('hex');
}
await mkdir(join(out,'licenses'),{recursive:true});
for(const pkg of ['kokoro-js','phonemizer','@huggingface/transformers']){
 const path=resolve(here,'node_modules',pkg,'LICENSE');await copyFile(path,join(out,'licenses',pkg.replaceAll('/','-')+'-LICENSE.txt'));
}
await copyFile(join(here,'onnxruntime-LICENSE.txt'),join(out,'licenses/onnxruntime-LICENSE.txt'));
await writeFile(join(out,'NOTICE.txt'),'Kokoro JS 1.2.1; Transformers.js; phonemizer; ONNX Runtime Web.\nKokoro-82M model: https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX\nModel/voice origins: https://huggingface.co/hexgrad/Kokoro-82M\nThe Kokoro voice loader is modified to load same-origin voice assets.\nWorker source and build instructions: tools/browser-voices in this public repository.\nThird-party licenses are provided in licenses/.\n');
await writeFile(join(out,'manifest.json'),JSON.stringify({model:'Kokoro-82M-v1.0-ONNX',dtype:'q8',voices,hashes},null,2));
console.log('Built same-origin, twelve-voice browser engine.');
