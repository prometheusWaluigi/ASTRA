const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/index.html','utf8'), script=html.match(/<script>([\s\S]+)<\/script>/)[1];
const elements={},context=new Proxy({},{get:()=>()=>{}});
const sandbox={document:{querySelector:s=>elements[s]??=(s==='#c'?{getContext:()=>context,addEventListener:()=>{}}:{})},window:{addEventListener:()=>{}},performance:{now:()=>0},requestAnimationFrame:()=>{},Math};
vm.createContext(sandbox);vm.runInContext(script,sandbox);const game=sandbox.window.rally;
for(let i=0;i<1300;i++)game.step(.02);
assert.equal(game.getState().ended,true);assert.equal(game.getState().missed,8);
game.reset();assert.equal(game.getState().x,0);assert.equal(game.getState().words.length,0);
let target=0;const course=[520,950,1400,1820,2240,2650,3080,3470];
for(let i=0;i<1300;i++){const s=game.getState();if(target<8&&s.x>=course[target]-55){game.jump();target++;}game.step(.02);}
assert.equal(game.getState().ended,true);assert.equal(game.getState().words.length,8);assert.equal(game.getState().missed,0);
console.log('PASS: idle course, all crater misses, reset, jump collection of all 8 words, finish.');
