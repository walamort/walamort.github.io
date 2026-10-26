// Independent regression checks for practical constraints; no browser required.
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const src=fs.readFileSync('assets/test-instrumento.js','utf8').split('let index=0;')[0];
const ctx=vm.createContext({});vm.runInContext(src+';globalThis.run=recommend;',ctx);
let count=0;
for(const budget of ['none','low','medium','high','unknown'])
for(const carry of ['pocket','case','home'])
for(const noise of ['headphones','quiet','open'])
for(const sound of ['bright','round','breath','strings','beat','any']){
 const r=ctx.run({budget,carry,noise,sound,goal:'rhythm',gesture:'hands'});
 assert.ok(r.options.length);assert.ok(r.options.every(c=>!c.conflicts.length));
 if(noise==='headphones')assert.ok(r.options.every(c=>c.id==='digital'));
 if(budget==='none')assert.ok(r.options.every(c=>c.cost===0));count++;
}
const home=fs.readFileSync('index.html','utf8');
for(const match of home.matchAll(/<script(?![^>]*type="application\/ld\+json")[^>]*>([\s\S]*?)<\/script>/g))new vm.Script(match[1]);
new vm.Script(fs.readFileSync('assets/test-instrumento.js','utf8'));
console.log(`PASS: ${count} quiz profiles respect budget, volume and portability; changed JavaScript parses.`);
