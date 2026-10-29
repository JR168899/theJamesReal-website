import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const source=fs.readFileSync('dist/english-levels.js','utf8'),start=source.indexOf('  const CRC_TABLE='),end=source.indexOf('  async function prepareCardExports',start),ctx={};vm.createContext(ctx);vm.runInContext(source.slice(start,end)+';this.checksum=crc32;',ctx);
assert.equal(ctx.checksum(Buffer.from('123456789')),0xcbf43926);assert.equal(ctx.checksum(Buffer.alloc(0)),0);
function reference(bytes){let n=0xffffffff;for(const b of bytes){n^=b;for(let j=0;j<8;j++)n=(n>>>1)^((n&1)?0xedb88320:0);}return(n^0xffffffff)>>>0;}
for(const bytes of [Buffer.alloc(1024),Buffer.from(Array.from({length:65536},(_,i)=>i%256))])assert.equal(ctx.checksum(bytes),reference(bytes));
console.log('PASS: ZIP CRC matches standard vector and independent binary reference.');
