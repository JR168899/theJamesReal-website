import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const sharp=require(process.env.JR_SHARP_MODULE||'/Users/jr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=new URL('../',import.meta.url),batchPath=process.argv[2]||'content/quote-reading-batch-001.json',batch=JSON.parse(await readFile(new URL(batchPath,root),'utf8')),day=batch.date,data=JSON.parse(await readFile(new URL(`dist/data/english-levels/${day}.json`,root),'utf8'));
const output=new URL('../../../outputs/'+batchPath.split('/').pop().replace('.json','')+'/',import.meta.url);await mkdir(output,{recursive:true});
for(const level of Object.keys(batch.cards)){const u=data[level];
 const c=u.cards.find(x=>x.type==='reflection'),photo=await readFile(new URL('dist/'+c.photoCredit.asset,root));
 let svg=await readFile(new URL('dist/'+c.downloadPoster,root),'utf8');svg=svg.replaceAll('__JR_PHOTO__','data:image/jpeg;base64,'+photo.toString('base64'));
 const name=['Everyday English',level,day,'Quote','01'].join(' - ')+'.png';
 await sharp(Buffer.from(svg)).png().toFile(fileURLToPath(new URL(name,output)));console.log('Exported',level);
}
