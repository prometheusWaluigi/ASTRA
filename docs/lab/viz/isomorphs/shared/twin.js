/* Isomorph Lab — twin-worlds engine.
 * One dynamical core drives two side-by-side panels. Sliders move the shared
 * skeleton; each world keeps its own parameter offset (the "gauge difference"
 * between the two papers/concepts being compared).
 * Source of truth: experiments/isomorph_twins.js — copied to
 * private-wiki/viz/isomorphs/shared/twin.js by isomorph_lab.py build_viz.
 */
import * as THREE from 'three';

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
function mulberry32(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;
  let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;
  return((t^(t>>>14))>>>0)/4294967296}}

/* ------------------------------------------------ world mount ---------- */
function mount(canvas){
  const renderer = new THREE.WebGLRenderer({canvas, antialias:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1.15, 1.15, 1.15, -1.15, 0.1, 10);
  camera.position.z = 1;
  return {renderer, scene, camera};
}
function fit(mount_, canvas){
  const w = canvas.clientWidth || 512;
  renderer_fit(mount_.renderer, w);
}
function renderer_fit(renderer, w){ renderer.setSize(w, w, false); }

function gridTexture(n){
  const data = new Uint8Array(n*n*4);
  const tex = new THREE.DataTexture(data, n, n, THREE.RGBAFormat);
  tex.needsUpdate = true;
  tex.magFilter = THREE.NearestFilter; tex.minFilter = THREE.NearestFilter;
  const mat = new THREE.MeshBasicMaterial({map:tex});
  const geo = new THREE.PlaneGeometry(2.2, 2.2);
  return {data, tex, mesh:new THREE.Mesh(geo, mat)};
}

/* ------------------------------------------------ cores ---------------- */

function makeKuramoto(params, rng){
  const N = 200;
  const theta = new Float32Array(N);
  const omegaBase = new Float32Array(N);
  for(let i=0;i<N;i++){theta[i]=rng()*Math.PI*2;
    omegaBase[i]=(rng()+rng()+rng()-1.5)*2;}
  const pos = new Float32Array(N*3), col = new Float32Array(N*3);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos,3));
  geo.setAttribute('color', new THREE.BufferAttribute(col,3));
  const pts = new THREE.Points(geo, new THREE.PointsMaterial({
    size:0.03, vertexColors:true, transparent:true, opacity:0.95}));
  // order-parameter vector
  const ogeo = new THREE.BufferGeometry();
  ogeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6),3));
  const vec = new THREE.Line(ogeo, new THREE.LineBasicMaterial({color:0xffffff}));
  return {
    objects:[pts, vec],
    step(dt,p){
      const K=p.coupling, a=p.frustration, spread=p.spread;
      const d = new Float32Array(N);
      for(let i=0;i<N;i++){
        let s=0;
        for(let j=0;j<N;j++) s+=Math.sin(theta[j]-theta[i]-a);
        d[i]=omegaBase[i]*spread + (K/N)*s;
      }
      for(let i=0;i<N;i++) theta[i]+=d[i]*Math.min(dt,0.05)*2.2;
      let mx=0,my=0;
      for(let i=0;i<N;i++){
        pos[i*3]=Math.cos(theta[i]); pos[i*3+1]=Math.sin(theta[i]); pos[i*3+2]=0;
        const h=(theta[i]%(Math.PI*2)+Math.PI*2)%(Math.PI*2)/(Math.PI*2);
        const c=new THREE.Color().setHSL(h,0.85,0.6);
        col[i*3]=c.r; col[i*3+1]=c.g; col[i*3+2]=c.b;
        mx+=Math.cos(theta[i]); my+=Math.sin(theta[i]);
      }
      const op=geo.attributes.position, oc=geo.attributes.color;
      op.needsUpdate=true; oc.needsUpdate=true;
      const v=ogeo.attributes.position.array;
      v[0]=0;v[1]=0;v[2]=0;v[3]=mx/N;v[4]=my/N;v[5]=0;
      ogeo.attributes.position.needsUpdate=true;
    }};
}

function makeGrayScott(params, rng){
  const n=128; const u=new Float32Array(n*n), v=new Float32Array(n*n);
  const u2=new Float32Array(n*n), v2=new Float32Array(n*n);
  u.fill(1);
  for(let s=0;s<14;s++){
    const cx=Math.floor(rng()*n), cy=Math.floor(rng()*n), r=3+Math.floor(rng()*4);
    for(let y=-r;y<=r;y++)for(let x=-r;x<=r;x++){
      const i=((cy+y+n)%n)*n+((cx+x+n)%n);
      if(x*x+y*y<=r*r){u[i]=0.5;v[i]=0.25+rng()*0.1;}}}
  const gt = gridTexture(n);
  const Du=0.16, Dv=0.08;
  function substep(F,k){
    for(let y=0;y<n;y++)for(let x=0;x<n;x++){
      const i=y*n+x;
      const l=y*n+((x-1+n)%n), r=y*n+((x+1)%n);
      const up=((y-1+n)%n)*n+x, dn=((y+1)%n)*n+x;
      const lu=u[l]+u[r]+u[up]+u[dn]-4*u[i];
      const lv=v[l]+v[r]+v[up]+v[dn]-4*v[i];
      const uvv=u[i]*v[i]*v[i];
      u2[i]=u[i]+(Du*lu-uvv+F*(1-u[i]));
      v2[i]=v[i]+(Dv*lv+uvv-(F+k)*v[i]);
    }
    u.set(u2); v.set(v2);
  }
  return {objects:[gt.mesh],
    step(dt,p){
      for(let s=0;s<8;s++) substep(p.feed,p.kill);
      const d=gt.data;
      for(let i=0;i<n*n;i++){
        const val=v[i];
        const c1=[4,6,14], c2=[140,240,200];
        d[i*4]=c1[0]+(c2[0]-c1[0])*val;
        d[i*4+1]=c1[1]+(c2[1]-c1[1])*val;
        d[i*4+2]=c1[2]+(c2[2]-c1[2])*val;
        d[i*4+3]=255;
      }
      gt.tex.needsUpdate=true;
    }};
}

function makeCascade(params, rng){
  const N=110;
  let edges=[], adj=[], active=new Uint8Array(N), born=new Int32Array(N);
  function build(rewire){
    edges=[]; adj=Array.from({length:N},()=>[]);
    for(let i=0;i<N;i++)for(let k=1;k<=2;k++){
      let j=(i+k)%N;
      if(rng()<rewire) j=Math.floor(rng()*N);
      if(j===i) continue;
      edges.push([i,j]); adj[i].push(j); adj[j].push(i);}
    active.fill(0); born.fill(-1);
    for(let s=0;s<3;s++){const i=Math.floor(rng()*N);active[i]=1;born[i]=0;}
  }
  build(params.rewire);
  const pos=new Float32Array(N*3), col=new Float32Array(N*3);
  const nodeXY=[];
  for(let i=0;i<N;i++){
    const a=i/N*Math.PI*2, r=0.82+rng()*0.14;
    nodeXY.push([Math.cos(a)*r,Math.sin(a)*r]);
    pos[i*3]=nodeXY[i][0];pos[i*3+1]=nodeXY[i][1];}
  const epos=new Float32Array(edges.length*6);
  edges.forEach((e,k)=>{epos[k*6]=nodeXY[e[0]][0];epos[k*6+1]=nodeXY[e[0]][1];
    epos[k*6+3]=nodeXY[e[1]][0];epos[k*6+4]=nodeXY[e[1]][1];});
  const egeo=new THREE.BufferGeometry();
  egeo.setAttribute('position',new THREE.BufferAttribute(epos,3));
  const lines=new THREE.LineSegments(egeo,new THREE.LineBasicMaterial({
    color:0x2a4a66,transparent:true,opacity:0.35}));
  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
  geo.setAttribute('color',new THREE.BufferAttribute(col,3));
  const pts=new THREE.Points(geo,new THREE.PointsMaterial({size:0.055,vertexColors:true}));
  let t=0;
  return {objects:[lines,pts],
    rebuild(p){build(p.rewire);t=0;
      const ep=egeo.attributes.position.array;
      edges.forEach((e,k)=>{ep[k*6]=nodeXY[e[0]][0];ep[k*6+1]=nodeXY[e[0]][1];
        ep[k*6+3]=nodeXY[e[1]][0];ep[k*6+4]=nodeXY[e[1]][1];});
      egeo.attributes.position.needsUpdate=true;},
    step(dt,p){
      t+=dt;
      const next=new Uint8Array(active);
      for(let i=0;i<N;i++){
        if(active[i])continue;
        let on=0;for(const j of adj[i])on+=active[j];
        if(adj[i].length&&on/adj[i].length>=p.theta){next[i]=1;born[i]=t;}
      }
      active=next;
      for(let i=0;i<N;i++){
        let c;
        if(!active[i])c=[0.12,0.16,0.24];
        else{const age=Math.min(1,(t-born[i])/6);
          c=[1-age*0.5,0.75-age*0.3,0.35];}
        col[i*3]=c[0];col[i*3+1]=c[1];col[i*3+2]=c[2];}
      geo.attributes.color.needsUpdate=true;
    }};
}

function makeBridge(params, rng){
  const P=130, TRAIL=34, STEPS=480;
  const parts=[];
  function spawn(p_){
    const spread=p_.endpoint_spread;
    const T=STEPS*(0.6+rng()*0.8);
    const W=new Float32Array(STEPS+1);
    for(let s=1;s<=STEPS;s++)W[s]=W[s-1]+(rng()*2-1)*0.055;
    return {x0:-1+rng()*0.15, x1:1-rng()*0.15,
      y0:(rng()*2-1)*0.8, y1:(rng()*2-1)*spread*1.6,
      W,T,t:rng()*T, trail:new Float32Array(TRAIL*2)};
  }
  for(let i=0;i<P;i++)parts.push(spawn(params));
  const pos=new Float32Array(P*TRAIL*3), col=new Float32Array(P*TRAIL*3);
  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
  geo.setAttribute('color',new THREE.BufferAttribute(col,3));
  const pts=new THREE.Points(geo,new THREE.PointsMaterial({
    size:0.018,vertexColors:true,transparent:true,opacity:0.85}));
  return {objects:[pts],
    step(dt,p){
      for(const q of parts){
        q.t+=dt*60;
        if(q.t>q.T){const fresh=spawn(p);Object.assign(q,fresh);}
        for(let h=TRAIL-1;h>0;h--){
          q.trail[h*2]=q.trail[(h-1)*2];q.trail[h*2+1]=q.trail[(h-1)*2+1];}
        const tau=Math.min(1,q.t/q.T);
        const i=Math.min(STEPS,Math.floor(q.t));
        const wT=q.W[STEPS], wi=q.W[i];
        const x=q.x0+(q.x1-q.x0)*tau;
        const y=q.y0+(q.y1-q.y0)*tau+p.noise*(wi-tau*wT)*0.4
              +p.drift*tau*(1-tau)*0.6;
        q.trail[0]=x;q.trail[1]=y;
      }
      let k=0;
      for(let pi=0;pi<P;pi++){const q=parts[pi];
        for(let h=0;h<TRAIL;h++){
          pos[k*3]=q.trail[h*2];pos[k*3+1]=q.trail[h*2+1];pos[k*3+2]=0;
          const f=1-h/TRAIL;
          col[k*3]=0.3+0.6*f;col[k*3+1]=0.55+0.35*f;col[k*3+2]=0.9*f+0.1;
          k++;}}
      geo.attributes.position.needsUpdate=true;
      geo.attributes.color.needsUpdate=true;
    }};
}

function makeSpiral(params, rng){
  const n=96;
  let state=new Uint8Array(n*n), next=new Uint8Array(n*n);
  function seedCells(p){
    state.fill(0);
    for(let s=0;s<5;s++){
      const cx=Math.floor(rng()*n),cy=Math.floor(rng()*n);
      for(let y=-2;y<=2;y++)for(let x=-2;x<=2;x++){
        const i=((cy+y+n)%n)*n+((cx+x+n)%n);
        if(rng()<0.6)state[i]=1+Math.floor(rng()*2);}}}
  seedCells(params);
  const gt=gridTexture(n);
  return {objects:[gt.mesh],
    step(dt,p){
      const S=Math.round(p.states), T=Math.round(p.threshold), moore=p.neighborhood>0.5;
      for(let y=0;y<n;y++)for(let x=0;x<n;x++){
        const i=y*n+x, s=state[i];
        if(s===0){
          let on=0;
          const offs=moore?8:4;
          for(let o=0;o<offs;o++){
            const dx=moore?[1,-1,0,0,1,1,-1,-1][o]:[1,-1,0,0][o];
            const dy=moore?[0,0,1,-1,1,-1,1,-1][o]:[0,0,1,-1][o];
            const j=((y+dy+n)%n)*n+((x+dx+n)%n);
            if(state[j]>=1&&state[j]<=T)on++;}
          next[i]=on>=T?1:0;
        } else next[i]=(s+1)%S;
      }
      const tmp=state;state=next;next=tmp;
      const d=gt.data;
      for(let i=0;i<n*n;i++){
        const s=state[i];
        let r=4,g=6,b=14;
        if(s===1){r=255;g=220;b=120;}
        else if(s>1){const f=s/Math.round(p.states);
          r=30+80*f;g=60+60*f;b=160-80*f;}
        d[i*4]=r;d[i*4+1]=g;d[i*4+2]=b;d[i*4+3]=255;}
      gt.tex.needsUpdate=true;
    }};
}

const CORES = {kuramoto:makeKuramoto, "gray-scott":makeGrayScott,
               cascade:makeCascade, bridge:makeBridge, spiral:makeSpiral};
const BOUNDS = {
  kuramoto:{coupling:[0,4],frustration:[-1.5,1.5],spread:[0.1,3]},
  "gray-scott":{feed:[0.02,0.08],kill:[0.045,0.07]},
  cascade:{theta:[0.05,0.6],rewire:[0,0.5]},
  bridge:{noise:[0.2,3],endpoint_spread:[0,1],drift:[-1,1]},
  spiral:{threshold:[1,4],states:[4,16],neighborhood:[0,1]}};

/* ------------------------------------------------ bootstrap ------------ */

export function startTwinWorlds(spec){
  const make=CORES[spec.core]||makeKuramoto;
  const bounds=BOUNDS[spec.core]||BOUNDS.kuramoto;
  const rngA=mulberry32(1234), rngB=mulberry32(98765);
  const canvasA=document.getElementById('world-a');
  const canvasB=document.getElementById('world-b');
  const mA=mount(canvasA), mB=mount(canvasB);
  const wA=make(spec.params_a,rngA), wB=make(spec.params_b,rngB);
  for(const o of wA.objects)mA.scene.add(o);
  for(const o of wB.objects)mB.scene.add(o);
  document.getElementById('label-a').textContent=spec.label_a||'world A';
  document.getElementById('label-b').textContent=spec.label_b||'world B';
  const base=Object.assign({},spec.params_a);
  const delta={};
  for(const k of Object.keys(bounds))
    delta[k]=(spec.params_b[k]??base[k])-(spec.params_a[k]??base[k]);
  function eff(off){const p={};
    for(const k of Object.keys(bounds))
      p[k]=clamp(base[k]+(off?delta[k]:0),bounds[k][0],bounds[k][1]);
    return p;}
  const controls=document.getElementById('controls');
  const reads={};
  for(const key of Object.keys(bounds)){
    const [lo,hi]=bounds[key];
    const label=document.createElement('label');
    label.textContent=key+' ';
    const input=document.createElement('input');
    input.type='range';input.min=lo;input.max=hi;
    input.step=(hi-lo)/200;input.value=base[key];
    const val=document.createElement('span');
    val.textContent=Number(base[key]).toFixed(3);
    input.oninput=()=>{base[key]=parseFloat(input.value);
      val.textContent=Number(base[key]).toFixed(3);paramsLine();};
    label.append(input,val);controls.append(label);
    reads[key]=val;}
  const reset=document.createElement('button');
  reset.textContent='reset worlds';controls.append(reset);
  reset.onclick=()=>location.reload();
  function paramsLine(){
    const pa=eff(false),pb=eff(true);
    document.getElementById('params-a').textContent=
      'A: '+Object.entries(pa).map(([k,v])=>`${k}=${v}`).join(' ');
    document.getElementById('params-b').textContent=
      'B: '+Object.entries(pb).map(([k,v])=>`${k}=${v}`).join(' ');
    if(wA.rebuild)wA.rebuild(pa);if(wB.rebuild)wB.rebuild(pb);}
  paramsLine();
  function resize(){
    [ [mA,canvasA],[mB,canvasB] ].forEach(([m,c])=>{
      const w=c.clientWidth||512;m.renderer.setSize(w,w,false);});}
  window.addEventListener('resize',resize);resize();
  let last=performance.now();
  function frame(now){
    const dt=Math.min(0.1,(now-last)/1000);last=now;
    const pa=eff(false),pb=eff(true);
    wA.step(dt,pa);wB.step(dt,pb);
    mA.renderer.render(mA.scene,mA.camera);
    mB.renderer.render(mB.scene,mB.camera);
    requestAnimationFrame(frame);}
  requestAnimationFrame(frame);
}
