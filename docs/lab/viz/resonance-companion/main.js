'use strict';
const $=id=>document.getElementById(id),M=Resonance;
const ink='#203d3c',teal='#24716b',rust='#a14d2f',line='#ced3c8';
const fmt=(v,n=3)=>(Math.abs(v)<.0000001?0:v).toFixed(n);
const text=(x,y,s,extra='')=>`<text x="${x}" y="${y}" ${extra}>${s}</text>`;
const path=(points,color,dash='')=>`<path d="${points.map((p,i)=>(i?'L':'M')+p.map(v=>v.toFixed(2)).join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="1.8" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;
let result,loopResult,settings;
function renderHarmonic(){
  settings={mode:$('mode').value,delta:+$('delta').value,k:+$('coupling').value,kick:+$('kick').value};
  const coupled=settings.mode==='coupled';$('coupling').disabled=!coupled;
  $('coupling-help').textContent=coupled?'Restoring strength in the chosen phase equation.':'No coupling in constructed mode.';
  for(const [id,v] of [['delta',settings.delta],['coupling',coupled?settings.k:0],['kick',settings.kick]])$(id+'-v').textContent=fmt(v,2);
  result=M.simulate(settings);const {out,T}=result;
  const samples=out.filter((s,i)=>i%5===0||i===out.length-1),x=t=>48+680*t/T;
  let g='';
  const chart=(top,height,min,max,label,series)=>{
    const y=v=>top+height-(v-min)/(max-min)*height;
    g+=text(48,top-10,label,'font-weight="600"');
    for(let j=0;j<=2;j++){
      const v=min+(max-min)*j/2,yy=y(v);g+=`<line x1="48" y1="${yy}" x2="728" y2="${yy}" stroke="${line}"/>`+text(4,yy+4,fmt(v,1));
    }
    g+=`<rect x="558" y="${top}" width="170" height="${height}" fill="${teal}" opacity=".05"/>`;
    for(const [fn,color,dash] of series)g+=path(samples.map(s=>[x(s.t),y(fn(s))]),color,dash);
    if(settings.kick)g+=`<line x1="${x(result.kickTime)}" y1="${top}" x2="${x(result.kickTime)}" y2="${top+height}" stroke="${rust}" stroke-dasharray="3 4"/>`;
  };
  chart(28,82,-1,1,'Signal amplitude',[[s=>Math.sin(s.slow),teal],[s=>Math.sin(s.fast),rust,'5 3']]);
  chart(150,62,0,1,'Ordinary alignment r(t)',[[s=>s.r,ink]]);
  let lo=Math.min(...out.map(s=>s.p))/M.TAU,hi=Math.max(...out.map(s=>s.p))/M.TAU;
  if(hi-lo<1){const m=(hi+lo)/2;lo=m-.5;hi=m+.5;}
  chart(254,92,lo,hi,'Unwrapped mismatch ψ / 2π (turns)',[[s=>s.p/M.TAU,teal]]);
  for(let j=0;j<=4;j++)g+=text(48+680*j/4,370,String(j*3),'text-anchor="middle"');
  g+=text(388,394,'Time / 2π · slow-reference cycles; shaded region = statistics','text-anchor="middle"');
  $('traces').innerHTML=g;
  $('R').textContent=fmt(result.R);$('r').textContent=fmt(result.meanR);$('drift').textContent=fmt(result.drift);$('slips').textContent=result.crossings;
  const d=Math.abs(settings.delta),k=settings.k;
  let finding;
  if(!coupled)finding=settings.delta===0?'Exact 2:1 organization, without interaction. R₂,₁ stays 1 in the final window while ordinary alignment oscillates. A kick changes the relation; nothing restores it.':'These are detuned constructed clocks. Their mismatch drifts with Δ; no restoring interaction has been introduced.';
  else if(k===0&&d===0)finding='Neutral agreement: the mismatch stays wherever it is placed. With K = 0 there is no restoring link.';
  else if(d<k)finding=`The equation admits a stable mismatch ψ* = ${fmt(Math.asin(settings.delta/k))} rad (mod 2π). A small kick relaxes toward it. The finite-window statistics may still include a slow transient.`;
  else if(Math.abs(d-k)<1e-9)finding='At the boundary: the fixed point is marginal, with slow approach and no finite linear restoring rate. A short record is especially ambiguous here.';
  else finding=`Beyond the boundary, mismatch winds. Predicted long-time drift: ${fmt(Math.sign(settings.delta)*Math.sqrt(d*d-k*k))} rad / time. The displayed finite-window estimate need not equal that asymptotic value.`;
  $('interpretation').textContent=finding;
  const xx=d=>220+d*110,yy=k=>207-k*108;
  $('boundary').innerHTML=`<path d="M55 45 L220 207 L385 45Z" fill="#d9e5d8" stroke="${teal}"/><path d="M55 45V207H385" fill="none" stroke="${line}"/>${text(220,72,'stable locking','text-anchor="middle"')}${text(72,182,'slips')}${text(335,182,'slips')}${text(20,35,'K')}${text(220,245,'Detuning Δ','text-anchor="middle"')}${text(45,224,'−1.5')}${text(215,224,'0')}${text(375,224,'1.5')}${text(22,52,'1.5')}<circle cx="${xx(settings.delta)}" cy="${yy(coupled?k:0)}" r="6" fill="${rust}" stroke="#f4f0e7" stroke-width="2"/>`;
}
function renderLoop(){
  const f=[1,2,3].map(i=>+$('f'+i).value),flux=+$('flux').value,gauge=$('gauge').checked;
  [1,2,3].forEach((i)=>$('f'+i+'-v').textContent=fmt(f[i-1],1));$('flux-v').textContent=fmt(flux,2);
  loopResult=M.loop(f,flux);
  const pts=[[130,280],[350,62],[570,280]],labels=[[173,158],[464,158],[350,318]];
  const phases=gauge?loopResult.prime:[.2,1.1,-.5];
  let g=`<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="${teal}"/></marker></defs>`;
  pts.forEach(([x,y],i)=>{
    const [x2,y2]=pts[(i+1)%3],dx=x2-x,dy=y2-y,len=Math.hypot(dx,dy);
    g+=`<line x1="${x+dx*34/len}" y1="${y+dy*34/len}" x2="${x2-dx*40/len}" y2="${y2-dy*40/len}" stroke="${teal}" stroke-width="1.6" marker-end="url(#arrow)"/>`;
    const [lx,ly]=labels[i];g+=`<rect x="${lx-64}" y="${ly-18}" width="128" height="29" fill="#f4f0e7"/>`+text(lx,ly,`${gauge?'β':'α'}${i+1}${(i+1)%3+1} = ${fmt(gauge?flux/3:loopResult.a[i],2)}`,'text-anchor="middle"');
    g+=`<circle cx="${x}" cy="${y}" r="27" fill="#f4f0e7" stroke="${line}"/><line x1="${x}" y1="${y}" x2="${x+22*Math.cos(phases[i])}" y2="${y-22*Math.sin(phases[i])}" stroke="${rust}" stroke-width="2"/>`+text(x,y+47,`node ${i+1}`,'text-anchor="middle"');
  });
  g+=text(350,222,`Φ = ${fmt(loopResult.holonomy,2)} rad`,'text-anchor="middle" style="font:26px Georgia"')+text(350,246,'loop sum modulo 2π','text-anchor="middle"');
  $('loop').innerHTML=g;$('loop-title').textContent=gauge?'Node offsets absorbed · loop phase remains':'Local offsets, closed path';
  $('loop-finding').textContent=Math.abs(flux)<1e-8?'Every local difference cancels. The loop returns zero, even when the three edge labels look very different.':`The loop retains ${fmt(flux,2)} radians. Changing the node offsets cannot erase it. No phase assignment can make all three edge arguments zero modulo 2π.`;
  $('coordinate-readout').textContent=`Same physical state, different coordinates: r(θ) = ${fmt(loopResult.rawR)}; r(θ′) = ${fmt(loopResult.primeR)}. Invariant edge arguments modulo 2π: (${loopResult.residual.map(x=>fmt(x,2)).join(', ')}) rad.`;
}
const presets={constructed:['constructed',0,0,0],locked:['coupled',.35,.8,1.8],slips:['coupled',1.2,.6,0]};
function preset(name){const [mode,d,k,kick]=presets[name];$('mode').value=mode;$('delta').value=d;$('coupling').value=k;$('kick').value=kick;document.querySelectorAll('[data-preset]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.preset===name)));renderHarmonic();}
document.querySelectorAll('[data-preset]').forEach(b=>b.onclick=()=>preset(b.dataset.preset));
['mode','delta','coupling','kick'].forEach(id=>$(id).addEventListener('input',()=>{document.querySelectorAll('[data-preset]').forEach(b=>b.setAttribute('aria-pressed','false'));renderHarmonic();}));
['f1','f2','f3','flux','gauge'].forEach(id=>$(id).addEventListener('input',renderLoop));
$('reset').onclick=()=>preset('constructed');$('loop-reset').onclick=()=>{['.6','-.8','.2'].forEach((v,i)=>$('f'+(i+1)).value=v);$('flux').value=0;$('gauge').checked=false;renderLoop();};
$('print').onclick=()=>window.print();
function summarySVG(){
  const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  const f=[1,2,3].map(i=>fmt(+$('f'+i).value,1)).join(', ');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1380" viewBox="0 0 1000 1380"><style>text{font-family:Arial,sans-serif;fill:${ink};font-size:15px}</style><rect width="1000" height="1380" fill="#f4f0e7"/>${text(65,65,'FIELD NOTE / 02 · CODEX · SYNTHETIC MATHEMATICS')}${text(65,138,'What a rhythm keeps.','style="font:64px Georgia"')}${text(65,180,'Harmony is a relation. Coupling is a mechanism. Test the difference.')}${text(65,225,escape(`${settings.mode}; Δ=${fmt(settings.delta,2)}; K=${fmt(settings.mode==='coupled'?settings.k:0,2)}; fast phase kick=${fmt(settings.kick,2)} rad`))}<svg x="60" y="250" width="875" height="472" viewBox="0 0 760 410">${$('traces').innerHTML}</svg>${text(65,758,`Final-window R₂,₁=${fmt(result.R)}; mean r=${fmt(result.meanR)}; drift=${fmt(result.drift)} rad/time; crossings=${result.crossings}`)}${text(65,788,'RK4, dt ≤ 0.02; t = 0…24π. Statistics: 18π…24π. Finite windows can hide slow slips.')}${text(65,837,'A closed path keeps what local names cannot erase.','style="font:28px Georgia"')}<svg x="65" y="860" width="490" height="273" viewBox="0 0 700 390">${$('loop').innerHTML}</svg>${text(565,915,`Offsets: (${f}) rad`)}${text(565,950,`Loop phase: ${fmt(loopResult.holonomy,2)} rad`)}${text(565,985,`Coordinates: ${$('gauge').checked?'offsets absorbed':'original'}`)}${text(565,1030,'αᵢⱼ = fᵢ − fⱼ + Φ/3')}${text(565,1065,'θ′ᵢ = θᵢ + fᵢ; loop sum = Φ')}${text(65,1180,'Independent clocks, common drive and waveform harmonics can mimic a locked relation.')}${text(65,1210,'Plasma comparison: a shared method, not evidence of identical mechanisms or consciousness.')}${text(65,1240,'The paper’s collapse quantities are normalized proxies, not measured collapse times.')}${text(65,1280,'Reading: Singh, Hameroff & Bandyopadhyay · doi:10.1016/j.chaos.2026.119151')}${text(65,1310,'Codex guest companion for Retrofractal-Kintsugi · 27 September 2026 · local review draft')}${text(65,1340,'Original illustrations; no author datasets, calibration, reproduction or endorsement.')}</svg>`;
}
$('export').onclick=()=>{const blob=new Blob([summarySVG()],{type:'image/svg+xml;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='what-a-rhythm-keeps.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('export-status').textContent='Illustrated summary prepared with the current settings.';};
renderHarmonic();renderLoop();
