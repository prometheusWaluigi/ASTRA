/* Original synthetic teaching model. No author data or fitted coefficients. */
(function(root){
  'use strict';
  const TAU=2*Math.PI;
  const wrap=x=>Math.atan2(Math.sin(x),Math.cos(x));
  function step(p,h,d,k){
    const f=x=>d-k*Math.sin(x),a=f(p),b=f(p+h*a/2),c=f(p+h*b/2),e=f(p+h*c);
    return p+h*(a+2*b+2*c+e)/6;
  }
  function simulate({mode='constructed',delta=0,k=0,kick=0,h=.02,T=24*Math.PI}={}){
    const out=[];let p=-.4,slow=0;
    const n=4*Math.ceil(T/h/4),dt=T/n,mid=n/2;
    // slow'=1-K sin(psi)/4; fast'=2-Delta+K sin(psi)/2.
    // Thus psi'=2 slow'-fast'=Delta-K sin(psi).
    for(let i=0;i<=n;i++){
      if(i===mid)p-=kick; // instantaneous positive kick to fast phase
      const t=i*dt,fast=2*slow-p;
      out.push({t,p,slow,fast,r:Math.abs(Math.cos((slow-fast)/2))});
      if(i<n){
        const next=mode==='constructed'?p+delta*dt:step(p,dt,delta,k);
        slow+=dt+(mode==='constructed'?0:(next-p-delta*dt)/4);
        p=next;
      }
    }
    // Equal-spaced, right endpoint excluded: average over the final quarter.
    const tail=out.slice(Math.ceil(n*.75),n);
    const R=Math.hypot(tail.reduce((a,s)=>a+Math.cos(s.p),0),tail.reduce((a,s)=>a+Math.sin(s.p),0))/tail.length;
    const meanR=tail.reduce((a,s)=>a+s.r,0)/tail.length;
    const drift=(out[n].p-tail[0].p)/(T-tail[0].t);
    const turns=(out[n].p-tail[0].p)/TAU;
    let crossings=0;
    for(let i=1;i<tail.length;i++)crossings+=Math.abs(Math.floor((tail[i].p+Math.PI)/TAU)-Math.floor((tail[i-1].p+Math.PI)/TAU));
    const last=tail[tail.length-1];crossings+=Math.abs(Math.floor((out[n].p+Math.PI)/TAU)-Math.floor((last.p+Math.PI)/TAU));
    return {out,R,meanR,drift,turns,crossings,T,dt,kickTime:mid*dt};
  }
  function loop(f,flux,theta=[.2,1.1,-.5]){
    const a=f.map((v,i)=>v-f[(i+1)%3]+flux/3);
    const prime=theta.map((v,i)=>v+f[i]);
    const residual=theta.map((v,i)=>wrap(theta[(i+1)%3]-v-a[i]));
    const order=v=>Math.hypot(v.reduce((s,x)=>s+Math.cos(x),0),v.reduce((s,x)=>s+Math.sin(x),0))/3;
    return {a,prime,residual,sum:a.reduce((s,x)=>s+x,0),holonomy:wrap(a.reduce((s,x)=>s+x,0)),rawR:order(theta),primeR:order(prime)};
  }
  const api={TAU,wrap,step,simulate,loop};
  if(typeof module!=='undefined')module.exports=api;else root.Resonance=api;
})(typeof globalThis!=='undefined'?globalThis:this);
