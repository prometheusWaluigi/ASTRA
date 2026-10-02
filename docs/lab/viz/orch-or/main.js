import * as THREE from 'three';

/* ============================================================
   Polyatomic Time Crystals — an interactive reading of
   Singh, Hameroff & Bandyopadhyay, CSF 213 (2026) 119151.
   Live sims are a normalized re-implementation of Model I;
   baked sweeps come from tools/bake_ptc_maps.py.
   ============================================================ */

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const sstep = (t) => t * t * (3 - 2 * t);

// ---------- deterministic rng (mulberry32) ----------
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
// gaussian via box-muller on seeded rng
function gauss(rng) {
  const u = Math.max(rng(), 1e-9), v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

// ---------- renderer ----------
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
} catch (e) {
  document.getElementById('hud').innerHTML = '<b>WebGL unavailable</b>';
  throw e;
}
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
renderer.setSize(innerWidth, innerHeight);
renderer.setClearColor(0x020408, 1);
document.getElementById('app').appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x020408, 0.016);
const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 0.1, 600);

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

// ---------- orbit camera (same ergonomics as plasma-sim) ----------
class OrbitCam {
  constructor(dom) {
    this.theta = 0.8; this.phi = 1.25; this.r = 26;
    this.tTheta = this.theta; this.tPhi = this.phi; this.tR = this.r;
    this.target = new THREE.Vector3();
    this.tTarget = this.target.clone();
    this.drag = false; this.idle = 0;
    dom.style.touchAction = 'none';
    dom.addEventListener('pointerdown', e => {
      this.drag = true; this.lx = e.clientX; this.ly = e.clientY; this.idle = 0;
      dom.setPointerCapture(e.pointerId);
    });
    dom.addEventListener('pointermove', e => {
      if (!this.drag) return;
      this.tTheta -= (e.clientX - this.lx) * 0.005;
      this.tPhi = clamp(this.tPhi - (e.clientY - this.ly) * 0.005, 0.06, Math.PI - 0.06);
      this.lx = e.clientX; this.ly = e.clientY; this.idle = 0;
    });
    addEventListener('pointerup', () => { this.drag = false; });
  }
  preset(r, phi, theta, tx, ty, tz) {
    this.tR = r; this.tPhi = phi;
    if (theta !== undefined) this.tTheta = theta;
    if (tx !== undefined) this.tTarget.set(tx, ty, tz);
  }
  update(cam, dt) {
    this.idle += dt;
    const k = 1 - Math.exp(-dt * 6);
    this.theta += (this.tTheta - this.theta) * k;
    this.phi += (this.tPhi - this.phi) * k;
    this.r += (this.tR - this.r) * k;
    this.target.lerp(this.tTarget, k);
    const sp = Math.sin(this.phi);
    cam.position.set(
      this.target.x + this.r * sp * Math.cos(this.theta),
      this.target.y + this.r * Math.cos(this.phi),
      this.target.z + this.r * sp * Math.sin(this.theta));
    cam.lookAt(this.target);
  }
}
const orbit = new OrbitCam(renderer.domElement);

// ---------- shared helpers ----------
const glowTex = (() => {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d');
  const grad = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  grad.addColorStop(0, 'rgba(255,255,255,1)');
  grad.addColorStop(0.25, 'rgba(255,255,255,.5)');
  grad.addColorStop(0.65, 'rgba(255,255,255,.1)');
  grad.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = grad; g.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
})();

function makeParticleSet(n, size) {
  const geom = new THREE.BufferGeometry();
  const pos = new Float32Array(n * 3);
  const col = new Float32Array(n * 3);
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(col, 3));
  const mat = new THREE.PointsMaterial({
    size, map: glowTex, vertexColors: true, transparent: true,
    depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true,
  });
  const points = new THREE.Points(geom, mat);
  points.frustumCulled = false;
  return { points, geom, pos, col, n };
}

// value->color ramp: deep blue -> cyan -> gold
function heatColor(t, out) {
  const c0 = [0.05, 0.10, 0.30], c1 = [0.10, 0.75, 0.95], c2 = [1.0, 0.78, 0.30];
  if (t < 0.5) { const u = t * 2;
    out[0] = lerp(c0[0], c1[0], u); out[1] = lerp(c0[1], c1[1], u); out[2] = lerp(c0[2], c1[2], u);
  } else { const u = t * 2 - 1;
    out[0] = lerp(c1[0], c2[0], u); out[1] = lerp(c1[1], c2[1], u); out[2] = lerp(c1[2], c2[2], u);
  }
}

// ============================================================
// PTC network model (shared by live scene + map markers)
// N=120 phase oscillators, 3 frequency families, geometry-gated
// cross-band coupling — mirrors tools/bake_ptc_maps.py
// ============================================================
const PTC = (() => {
  const N = 120, FAM = 3, S = 6;
  const rng = mulberry32(20260926);
  const fam = new Int32Array(N);
  const omega0 = new Float32Array(N);
  const centers = [0.80, 1.0, 1.25];
  for (let i = 0; i < N; i++) fam[i] = Math.floor(i * FAM / N);
  for (let i = 0; i < N; i++) omega0[i] = centers[fam[i]] * Math.exp(gauss(rng) * 0.05);
  // sort by frequency so families stay ordered
  const idx = [...Array(N).keys()].sort((a, b) => omega0[a] - omega0[b]);
  const om = new Float32Array(N), fm = new Int32Array(N);
  idx.forEach((src, dst) => { om[dst] = omega0[src]; fm[dst] = fam[src]; });
  for (let i = 0; i < N; i++) { omega0[i] = om[i]; fam[i] = fm[i]; }

  const c = new Float32Array(N), h = new Float32Array(N), piSite = new Uint8Array(N);
  for (let i = 0; i < N; i++) { c[i] = rng(); h[i] = rng(); piSite[i] = rng() < 0.18 ? 1 : 0; }
  const s = fam.slice();                       // sector = frequency family
  const qg = [0.6, -0.35, 0.9];
  const q = new Float32Array(N); for (let i = 0; i < N; i++) q[i] = qg[fam[i]];

  // adjacency: dense intra-band, sparse adjacent-band (paper's M_ij)
  const Msame = new Uint8Array(N * N), Madj = new Uint8Array(N * N);
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
    const df = Math.abs(fam[i] - fam[j]);
    if (df === 0 && rng() < 0.85) { Msame[i * N + j] = Msame[j * N + i] = 1; }
    else if (df === 1 && rng() < 0.22) { Madj[i * N + j] = Madj[j * N + i] = 1; }
  }
  const xi = new Float32Array(N * N);          // fixed phase disorder
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
    const v = gauss(rng); xi[i * N + j] = xi[j * N + i] = v;
  }
  // normalize xi to unit variance
  let m = 0, v2 = 0, cnt = 0;
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) if (i !== j && (Msame[i*N+j]||Madj[i*N+j])) { m += xi[i*N+j]; cnt++; }
  m /= cnt;
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) { xi[i*N+j] -= m; v2 += xi[i*N+j]*xi[i*N+j]; }
  const sd = Math.sqrt(v2 / (N * N));
  for (let i = 0; i < N * N; i++) xi[i] /= sd;

  const Kshape = new Float32Array(N * N), Hij = new Float32Array(N * N),
        Cij = new Float32Array(N * N), Cd = new Float32Array(N * N),
        Hd = new Float32Array(N * N), Sd = new Float32Array(N * N);
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
    const k = i * N + j;
    const lr = Math.log(omega0[i] / omega0[j]);
    Kshape[k] = Math.exp(-(lr * lr) / (2 * 0.30 * 0.30));
    const hd = h[i] - h[j];
    Hij[k] = Math.exp(-Math.abs(hd) / 0.30);
    Cij[k] = (c[i] + c[j]) / 2;
    Cd[k] = c[i] - c[j]; Hd[k] = hd;
    Sd[k] = (s[i] - s[j]) / S;
  }

  const KIN = 1.6, KCROSS = 3.2, BK = 1.6, BE = 1.3, BA = 0.85, BD = 0.40;
  const A0 = 0.10, AK = 0.25, AE = 0.18, AS = 0.30, AA = 0.60, AD = 0.40;
  const TWO_PI = Math.PI * 2;

  const K = new Float32Array(N * N);
  const alpha = new Float32Array(N * N);
  const w = new Float32Array(N);
  const theta = new Float32Array(N);
  const ktmp = new Float32Array(N), th2 = new Float32Array(N), dtmp = new Float32Array(N);
  const params = { kappa: 0.75, eta: 0.8, sigma: 0.5, anes: 0.0, det: 0.0 };

  function rebuild() {
    const { kappa, eta, sigma, anes, det } = params;
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        const k = i * N + j;
        let kv = 0;
        if (Msame[k] || Madj[k]) {
          const gcross = BK * kappa * (0.3 + Cij[k]) + BE * eta * Hij[k]
                       + 3.5 * kappa * eta * (0.3 + Cij[k]);
          kv = Msame[k] ? KIN * Kshape[k] : KCROSS * Kshape[k] * (0.06 + gcross);
          // anesthetic hits pi-pocket edges hardest
          const vul = (piSite[i] || piSite[j]) ? 1.0 : 0.55;
          kv *= (1 - BA * anes * vul) * (1 - BD * Math.abs(det));
        }
        K[k] = kv;
        let a = A0 + AK * kappa * Cd[k] + AE * eta * Hd[k]
              + AS * sigma * TWO_PI * Sd[k] + (AA * anes + AD * det) * xi[k];
        alpha[k] = ((a % TWO_PI) + TWO_PI) % TWO_PI;
      }
      w[i] = omega0[i] * (1 + det * q[i]);
    }
  }

  function initPhases(seed = 1) {
    const r = mulberry32(seed * 7919 + 13);
    for (let i = 0; i < N; i++) theta[i] = r() * TWO_PI;
  }

  // midpoint RK2, dt fixed
  function step(dt) {
    for (let i = 0; i < N; i++) {
      let acc = 0; const thi = theta[i];
      for (let j = 0; j < N; j++) {
        const k = i * N + j;
        if (K[k] !== 0) acc += K[k] * Math.sin(theta[j] - thi - alpha[k]);
      }
      ktmp[i] = w[i] + acc / N;
      th2[i] = thi + 0.5 * dt * ktmp[i];
    }
    for (let i = 0; i < N; i++) {
      let acc = 0; const thi = th2[i];
      for (let j = 0; j < N; j++) {
        const k = i * N + j;
        if (K[k] !== 0) acc += K[k] * Math.sin(th2[j] - thi - alpha[k]);
      }
      dtmp[i] = w[i] + acc / N;
    }
    for (let i = 0; i < N; i++) theta[i] += dt * dtmp[i];
  }

  function orderParam() {
    let x = 0, y = 0;
    for (let i = 0; i < N; i++) { x += Math.cos(theta[i]); y += Math.sin(theta[i]); }
    x /= N; y /= N;
    return { r: Math.hypot(x, y), psi: Math.atan2(y, x) };
  }

  rebuild(); initPhases(1);
  return { N, fam, c, h, piSite, omega0, K, alpha, w, theta, params, rebuild, initPhases, step, orderParam };
})();

// ============================================================
// SCENE 0 — microtubule hero: 13-protofilament tube, pi pockets
// ============================================================
class MicrotubuleScene {
  constructor() {
    this.group = new THREE.Group();
    const PF = 13, DIMERS = 42;
    this.count = PF * DIMERS;
    const geo = new THREE.SphereGeometry(0.16, 10, 10);
    const mat = new THREE.MeshStandardMaterial({
      color: 0x6fa8dc, roughness: 0.4, metalness: 0.3,
      emissive: 0x123a5c, emissiveIntensity: 0.9,
    });
    this.mesh = new THREE.InstancedMesh(geo, mat, this.count);
    const dummy = new THREE.Object3D();
    this.base = [];
    let n = 0;
    for (let p = 0; p < PF; p++) for (let d = 0; d < DIMERS; d++) {
      // 3-start helical arrangement, MT-like pitch
      const a = (p / PF) * Math.PI * 2 + d * 0.148;
      const z = (d - DIMERS / 2) * 0.42 + (p % 3) * 0.14;
      const R = 1.55;
      const pos = new THREE.Vector3(R * Math.cos(a), R * Math.sin(a), z);
      dummy.position.copy(pos); dummy.updateMatrix();
      this.mesh.setMatrixAt(n, dummy.matrix);
      this.base.push(pos);
      const isPi = ((p * 7 + d * 3) % 29) === 0;
      this.mesh.setColorAt(n, new THREE.Color(isPi ? 0xffcf6e : 0x4a86c0));
      n++;
    }
    this.group.add(this.mesh);
    // lumen glow: faint core line of pi-sites
    this.lum = makeParticleSet(200, 0.22);
    for (let i = 0; i < 200; i++) {
      const z = (i / 200 - 0.5) * DIMERS * 0.42;
      const a = i * 2.4;
      this.lum.pos[i * 3] = 1.0 * Math.cos(a); this.lum.pos[i * 3 + 1] = 1.0 * Math.sin(a); this.lum.pos[i * 3 + 2] = z;
      this.lum.col[i * 3] = 1.0; this.lum.col[i * 3 + 1] = 0.75; this.lum.col[i * 3 + 2] = 0.3;
    }
    this.group.add(this.lum.points);
    const key = new THREE.PointLight(0x7fd8ff, 260, 0, 2); key.position.set(8, 6, 6);
    const rim = new THREE.PointLight(0xffcf6e, 140, 0, 2); rim.position.set(-7, -4, -5);
    this.group.add(key, rim, new THREE.AmbientLight(0x33455c, 2.2));
    this.cam = { r: 24, phi: 1.35, theta: 0.6, t: [0, 0, 0] };
  }
  update(dt, t) {
    this.group.rotation.z = t * 0.08;
    this.group.rotation.x = Math.sin(t * 0.11) * 0.12;
    this.lum.points.material.size = 0.18 + 0.06 * Math.sin(t * 2.1);
  }
}

// ============================================================
// SCENE 1 — the resonance ladder: 12 commensurate clock rings
// ============================================================
class LadderScene {
  constructor() {
    this.group = new THREE.Group();
    this.rings = [];
    const NB = 12;
    for (let b = 0; b < NB; b++) {
      const R = 2.2 + b * 0.55;
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(R, 0.02, 6, 140),
        new THREE.MeshBasicMaterial({ color: b < 4 ? 0x2b5f8a : b < 8 ? 0x3f86b8 : 0x7fd8ff,
          transparent: true, opacity: 0.5 }));
      ring.rotation.x = Math.PI / 2 + (b - NB / 2) * 0.02;
      ring.position.z = (b - NB / 2) * 1.9;
      this.group.add(ring);
      // 3 phase beads per ring ("triplet of triplets" nod)
      const beadGeo = new THREE.SphereGeometry(0.09, 8, 8);
      const beads = [];
      for (let k = 0; k < 3; k++) {
        const bead = new THREE.Mesh(beadGeo,
          new THREE.MeshBasicMaterial({ color: 0xffcf6e }));
        ring.add(bead); beads.push(bead);
      }
      // slower rings for low bands (lower = faster bead... invert: low freq
      // = physically slower rotation)
      this.rings.push({ ring, beads, rate: 0.15 * Math.pow(1.35, b), phase: b * 0.7 });
    }
    // connecting threads — commensurate spokes
    const lineMat = new THREE.LineBasicMaterial({ color: 0x3a6a92, transparent: true, opacity: 0.35 });
    for (let k = 0; k < 9; k++) {
      const pts = [];
      for (let b = 0; b < NB; b++) {
        const R = 2.2 + b * 0.55, a = k * (Math.PI * 2 / 9) + b * 0.35;
        pts.push(new THREE.Vector3(R * Math.cos(a), R * Math.sin(a), (b - NB / 2) * 1.9));
      }
      this.group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), lineMat));
    }
    this.cam = { r: 26, phi: 1.2, theta: 0.3, t: [0, 0, 0] };
  }
  update(dt, t) {
    for (const r of this.rings) {
      r.ring.rotation.z = t * 0.03;
      r.beads.forEach((b, k) => {
        const a = t * r.rate + r.phase + k * (Math.PI * 2 / 3);
        const R = r.ring.geometry.parameters.radius;
        b.position.set(R * Math.cos(a), R * Math.sin(a), 0);
      });
    }
    this.group.rotation.y = t * 0.05;
  }
}

// ============================================================
// SCENE 2 — LIVE Kuramoto ensemble on three rings
// ============================================================
class KuramotoScene {
  constructor() {
    this.group = new THREE.Group();
    const N = PTC.N;
    // node positions: 3 tilted rings by family
    this.nodePos = new Float32Array(N * 3);
    this.nodeR = [3.2, 4.6, 6.0];
    const tilt = [0.5, 0.0, -0.5];
    for (let i = 0; i < N; i++) {
      const f = PTC.fam[i];
      const within = i - f * (N / 3);
      const a = (within / (N / 3)) * Math.PI * 2;
      const R = this.nodeR[f];
      const x = R * Math.cos(a), y = R * Math.sin(a) * Math.cos(tilt[f]), z = R * Math.sin(a) * Math.sin(tilt[f]) + (f - 1) * 1.6;
      this.nodePos[i * 3] = x; this.nodePos[i * 3 + 1] = y; this.nodePos[i * 3 + 2] = z;
    }
    this.ps = makeParticleSet(N, 0.34);
    this.ps.pos.set(this.nodePos);
    this.group.add(this.ps.points);
    // phase needles: one LineSegments, 2 verts per node
    const lg = new THREE.BufferGeometry();
    this.npos = new Float32Array(N * 6);
    this.ncol = new Float32Array(N * 6);
    lg.setAttribute('position', new THREE.BufferAttribute(this.npos, 3));
    lg.setAttribute('color', new THREE.BufferAttribute(this.ncol, 3));
    this.needles = new THREE.LineSegments(lg, new THREE.LineBasicMaterial({
      vertexColors: true, transparent: true, opacity: 0.9,
      blending: THREE.AdditiveBlending, depthWrite: false }));
    this.needles.frustumCulled = false;
    this.group.add(this.needles);
    // ring guides
    for (let f = 0; f < 3; f++) {
      const g2 = new THREE.RingGeometry(this.nodeR[f] - 0.02, this.nodeR[f] + 0.02, 128);
      const m2 = new THREE.MeshBasicMaterial({ color: 0x2b5f8a, transparent: true, opacity: 0.35, side: THREE.DoubleSide });
      const rm = new THREE.Mesh(g2, m2);
      rm.rotation.x = tilt[f];            // match node-circle tilt
      rm.position.z = (f - 1) * 1.6;
      this.group.add(rm);
    }
    // mean-field arrow (order parameter)
    const ar = new THREE.BufferGeometry();
    this.apos = new Float32Array(6);
    ar.setAttribute('position', new THREE.BufferAttribute(this.apos, 3));
    this.arrow = new THREE.Line(ar, new THREE.LineBasicMaterial({ color: 0xffcf6e, transparent: true, opacity: 0.95 }));
    this.arrow.frustumCulled = false;
    this.group.add(this.arrow);
    this.head = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 8),
      new THREE.MeshBasicMaterial({ color: 0xffcf6e }));
    this.group.add(this.head);
    this.cam = { r: 19, phi: 1.15, theta: 0.7, t: [0, 0, 0.6] };
    this.acc = 0;
  }
  update(dt, t) {
    // advance the sim a few substeps per frame
    this.acc += dt;
    const sdt = 0.10, maxSteps = 6;
    let n = 0;
    while (this.acc > sdt && n < maxSteps) { PTC.step(sdt); this.acc -= sdt; n++; }
    if (n === maxSteps) this.acc = 0;
    const { r, psi } = PTC.orderParam();
    // needles: phase direction drawn in each node's local tangent plane
    for (let i = 0; i < PTC.N; i++) {
      const j = i * 3, k6 = i * 6;
      const th = PTC.theta[i];
      const f = PTC.fam[i];
      const L = 0.55;
      // tangent dir: rotate ring-tangent by phase around ring normal-ish
      const px = this.nodePos[j], py = this.nodePos[j + 1], pz = this.nodePos[j + 2];
      const tx = -Math.sin(Math.atan2(py, px)) , ty = Math.cos(Math.atan2(py, px));
      const dx = tx * Math.cos(th) - Math.cos(Math.atan2(py, px)) * Math.sin(th) * 0.3;
      const dy = ty * Math.cos(th) - Math.sin(Math.atan2(py, px)) * Math.sin(th) * 0.3;
      const dz = Math.sin(th) * 0.6;
      this.npos[k6] = px; this.npos[k6 + 1] = py; this.npos[k6 + 2] = pz;
      this.npos[k6 + 3] = px + dx * L; this.npos[k6 + 4] = py + dy * L; this.npos[k6 + 5] = pz + dz * L;
      const pi = PTC.piSite[i];
      const glowc = pi ? [1.0, 0.78, 0.3] : [0.4, 0.8, 1.0];
      this.ncol[k6] = glowc[0] * 0.4; this.ncol[k6 + 1] = glowc[1] * 0.4; this.ncol[k6 + 2] = glowc[2] * 0.4;
      this.ncol[k6 + 3] = glowc[0]; this.ncol[k6 + 4] = glowc[1]; this.ncol[k6 + 5] = glowc[2];
      const bright = 0.45 + 0.55 * (0.5 + 0.5 * Math.cos(th - psi));
      this.ps.col[j] = glowc[0] * bright; this.ps.col[j + 1] = glowc[1] * bright; this.ps.col[j + 2] = glowc[2] * bright;
    }
    this.needles.geometry.attributes.position.needsUpdate = true;
    this.needles.geometry.attributes.color.needsUpdate = true;
    this.ps.geom.attributes.color.needsUpdate = true;
    // mean-field arrow in ring-1 plane (scaled by r)
    const R = 8.5 * r;
    this.apos[0] = 0; this.apos[1] = 0; this.apos[2] = 0;
    this.apos[3] = R * Math.cos(psi); this.apos[4] = R * Math.sin(psi); this.apos[5] = 0;
    this.arrow.geometry.attributes.position.needsUpdate = true;
    this.head.position.set(this.apos[3], this.apos[4], this.apos[5]);
    this.head.material.color.setHSL(0.12, 0.9, 0.4 + 0.35 * r);
    document.getElementById('rval').textContent = r.toFixed(3);
    document.getElementById('rbar').style.width = (r * 100).toFixed(1) + '%';
  }
}

// ============================================================
// SCENE 3 — locking map: baked r(kappa, eta) terrain
// ============================================================
class MapScene {
  constructor(data) {
    this.group = new THREE.Group();
    this.data = data;
    this.W = 16;
    const nk = data.kappa.length, ne = data.eta.length;
    this.nk = nk; this.ne = ne;
    const geo = new THREE.PlaneGeometry(this.W, this.W, nk - 1, ne - 1);
    geo.rotateX(-Math.PI / 2);
    const posAttr = geo.attributes.position;
    const colors = new Float32Array(posAttr.count * 3);
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    this.geo = geo;
    this.mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
      vertexColors: true, roughness: 0.7, metalness: 0.2,
      transparent: true, opacity: 0.96,
    }));
    this.group.add(this.mesh);
    const wire = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({
      color: 0x9adfff, wireframe: true, transparent: true, opacity: 0.07 }));
    this.group.add(wire);
    // axis frame
    const axes = new THREE.LineSegments(new THREE.EdgesGeometry(
      new THREE.BoxGeometry(this.W, 0.01, this.W)),
      new THREE.LineBasicMaterial({ color: 0x3a6a92 }));
    axes.position.y = -0.05;
    this.group.add(axes);
    // traveling marker along the diagonal geometric path I(s) (paper Fig 3a)
    this.marker = new THREE.Mesh(new THREE.SphereGeometry(0.28, 12, 12),
      new THREE.MeshBasicMaterial({ color: 0xffcf6e }));
    this.group.add(this.marker);
    // normalized tau_OR contour fan over the same (kappa, eta) plane.
    // Paper's closed form: EG = EG0(1 + gk*k + ge*e + gke*k*e), tau ~ 1/EG.
    const gk = 1.8, ge = 1.5, gke = 3.0;
    const u1 = 1 + gk + ge + gke;
    this.tauLines = [];
    for (const L of [0.25, 0.4, 0.55, 0.7, 0.85]) {
      const uT = u1 / (1 + L * (u1 - 1));   // tau_norm = u1/u in [1, u1]
      const pts = [];
      for (let i2 = 0; i2 <= 80; i2++) {
        const k = i2 / 80;
        const e = (uT - 1 - gk * k) / (ge + gke * k);
        if (e < 0 || e > 1) { pts.push(null); continue; }
        pts.push(new THREE.Vector3((k - 0.5) * this.W, 0, (e - 0.5) * this.W));
      }
      // split into contiguous runs
      let run = [];
      const flush = () => {
        if (run.length > 1) {
          const g2 = new THREE.BufferGeometry().setFromPoints(run);
          const ln = new THREE.Line(g2, new THREE.LineBasicMaterial({
            color: 0xffcf6e, transparent: true, opacity: 0.85 }));
          ln.frustumCulled = false;
          this.group.add(ln);
          this.tauLines.push({ ln, pts: run.map(p => [p.x, p.z]) });
        }
        run = [];
      };
      for (const p of pts) { if (p === null) flush(); else run.push(p); }
      flush();
    }
    const key = new THREE.PointLight(0x7fd8ff, 90, 0, 2); key.position.set(6, 9, 4);
    this.group.add(key, new THREE.AmbientLight(0x334455, 1.2));
    this.morph = 0;
    this.cam = { r: 24, phi: 0.95, theta: -0.7, t: [0, 0, 0] };
  }
  // morph 0 = baseline map, 1 = anesthetic map
  paint(morph) {
    const { r: ra } = this.data, rb = this.data.rAne || this.data.r;
    const posAttr = this.geo.attributes.position;
    const colAttr = this.geo.attributes.color;
    const tmp = [0, 0, 0];
    let i = 0;
    for (let e = 0; e < this.ne; e++) for (let k = 0; k < this.nk; k++, i++) {
      const v = lerp(ra[e][k], rb[e][k], morph);
      posAttr.setY(i, v * 7.0);
      heatColor(clamp((v - 0.3) / 0.7, 0, 1), tmp);
      colAttr.setXYZ(i, tmp[0], tmp[1], tmp[2]);
    }
    posAttr.needsUpdate = true; colAttr.needsUpdate = true;
    this.geo.computeVertexNormals();
  }
  rAt(kappa, eta, morph) {
    const { r: ra } = this.data, rb = this.data.rAne || this.data.r;
    const fx = clamp(kappa, 0, 1) * (this.nk - 1);
    const fz = clamp(eta, 0, 1) * (this.ne - 1);
    const i0 = Math.floor(fx), j0 = Math.floor(fz);
    const i1 = Math.min(i0 + 1, this.nk - 1), j1 = Math.min(j0 + 1, this.ne - 1);
    const u = fx - i0, v = fz - j0;
    const bil = (g) => lerp(lerp(g[j0][i0], g[j0][i1], u), lerp(g[j1][i0], g[j1][i1], u), v);
    return lerp(bil(ra), bil(rb), morph);
  }
  update(dt, t, local) {
    // first half of section = baseline, then morph to anesthetic landscape
    const target = (local === undefined || local < 0.45) ? 0 : 1;
    this.morph += (target - this.morph) * (1 - Math.exp(-dt * 3));
    this.paint(this.morph);
    // marker rides the diagonal I(s): kappa=eta=s, s = t sweep
    const s = (Math.sin(t * 2.2) * 0.5 + 0.5);
    const gx = (s - 0.5) * this.W, gz = (s - 0.5) * this.W;
    this.marker.position.set(gx, this.rAt(s, s, this.morph) * 7.0 + 0.4, gz);
    // drape tau_OR contours on the (possibly morphing) terrain
    for (const { ln, pts } of this.tauLines) {
      const pa = ln.geometry.attributes.position;
      for (let i = 0; i < pts.length; i++) {
        const k = pts[i][0] / this.W + 0.5, e = pts[i][1] / this.W + 0.5;
        pa.setY(i, this.rAt(k, e, this.morph) * 7.0 + 0.09);
      }
      pa.needsUpdate = true;
    }
  }
}

// ============================================================
// SCENE 4 — Diósi–Penrose proxy: density pair + Z(G,X) sheet
// ============================================================
class DPScene {
  constructor() {
    this.group = new THREE.Group();
    // two alternative mass-energy configurations as offset particle ellipsoids
    this.np = 2600;
    this.ps = makeParticleSet(this.np * 2, 0.16);
    const rng = mulberry32(4242);
    this.baseA = new Float32Array(this.np * 3);
    this.baseB = new Float32Array(this.np * 3);
    for (let i = 0; i < this.np; i++) {
      // ellipsoid A
      const a = rng() * 2 * Math.PI, rr = Math.sqrt(rng());
      this.baseA[i * 3] = rr * Math.cos(a) * 3.2;
      this.baseA[i * 3 + 1] = (rng() - 0.5) * 2.2 * (1 - rr * 0.5);
      this.baseA[i * 3 + 2] = rr * Math.sin(a) * 3.2;
      // B: same cloud, shifted+sheared — the "alternative resonance config"
      this.baseB[i * 3] = this.baseA[i * 3] + 1.7 + 0.5 * this.baseA[i * 3 + 1];
      this.baseB[i * 3 + 1] = this.baseA[i * 3 + 1] + 0.4;
      this.baseB[i * 3 + 2] = this.baseA[i * 3 + 2] * 0.92;
    }
    this.group.add(this.ps.points);
    this.group.position.x = -8.5;
    // Z(G,X) hazard surface: Z = 1 - exp(-(lg G + ld(1-X)) t_obs)
    const Gn = 26, Xn = 26, W2 = 13;
    const lg = 2.2, ld = 1.6, tobs = 1.0;
    const geo = new THREE.PlaneGeometry(W2, W2, Gn - 1, Xn - 1);
    geo.rotateX(-Math.PI / 2);
    const pa = geo.attributes.position;
    const cols = new Float32Array(pa.count * 3);
    geo.setAttribute('color', new THREE.BufferAttribute(cols, 3));
    const tmp = [0, 0, 0];
    for (let i = 0; i < pa.count; i++) {
      const G = (pa.getX(i) / W2 + 0.5), X = (pa.getZ(i) / W2 + 0.5);
      const Z = 1 - Math.exp(-(lg * G + ld * (1 - X)) * tobs);
      pa.setY(i, Z * 5.5);
      heatColor(Z, tmp); cols[i * 3] = tmp[0]; cols[i * 3 + 1] = tmp[1]; cols[i * 3 + 2] = tmp[2];
    }
    geo.computeVertexNormals();
    const sheet = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
      vertexColors: true, transparent: true, opacity: 0.9, roughness: 0.6 }));
    sheet.position.set(17, -3.4, 0); // offset to the right of the blobs
    this.group.add(sheet);
    // Z=0.5 ridge: X_th(G) = 1 - (-ln(1-Z)/t - lg G)/ld
    const ridge = [];
    for (let i = 0; i <= 60; i++) {
      const G = i / 60;
      const X = 1 - (-Math.log(0.5) / tobs - lg * G) / ld;
      if (X < -0.05 || X > 1.05) continue;
      ridge.push(new THREE.Vector3((G - 0.5) * W2 + 17,
        (0.5) * 5.5 + 0.08 - 3.4, (X - 0.5) * W2));
    }
    this.group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(ridge),
      new THREE.LineBasicMaterial({ color: 0xffcf6e })));
    const key = new THREE.PointLight(0x7fd8ff, 90, 0, 2); key.position.set(6, 9, 6);
    this.group.add(key, new THREE.AmbientLight(0x334455, 1.2));
    this.cam = { r: 30, phi: 1.1, theta: 0.9, t: [4, 1.5, 0] };
  }
  update(dt, t) {
    // blobs breathe apart / together — E_G lives in the overlap contrast
    const sep = 0.5 + 0.5 * Math.sin(t * 0.5);
    const push = 0.5 + sep * 1.1;
    for (let i = 0; i < this.np; i++) {
      const j = i * 3, j2 = (this.np + i) * 3;
      const wob = 0.06 * Math.sin(t * 1.7 + i * 0.37);
      this.ps.pos[j] = this.baseA[j] * (1 + wob * 0.4);
      this.ps.pos[j + 1] = this.baseA[j + 1] + wob;
      this.ps.pos[j + 2] = this.baseA[j + 2] * (1 + wob * 0.4);
      this.ps.col[j] = 0.5; this.ps.col[j + 1] = 0.85; this.ps.col[j + 2] = 1.0;
      this.ps.pos[j2] = this.baseB[j] + push;
      this.ps.pos[j2 + 1] = this.baseB[j + 1] - wob;
      this.ps.pos[j2 + 2] = this.baseB[j + 2];
      this.ps.col[j2] = 1.0; this.ps.col[j2 + 1] = 0.62; this.ps.col[j2 + 2] = 0.28;
    }
    this.ps.geom.attributes.position.needsUpdate = true;
    this.ps.geom.attributes.color.needsUpdate = true;
  }
}

// ============================================================
// SCENE 5 — perturbation phase diagram (A x delta) + ridge
// ============================================================
class PerturbScene {
  constructor(data) {
    this.group = new THREE.Group();
    const na = data.anes.length, nd = data.det.length;
    const W = 16;
    const geo = new THREE.PlaneGeometry(W, W, na - 1, nd - 1);
    geo.rotateX(-Math.PI / 2);
    const pa = geo.attributes.position;
    const cols = new Float32Array(pa.count * 3);
    geo.setAttribute('color', new THREE.BufferAttribute(cols, 3));
    const tmp = [0, 0, 0];
    let i = 0;
    for (let d = 0; d < nd; d++) for (let a = 0; a < na; a++, i++) {
      const v = data.r[d][a];
      pa.setY(i, v * 7);
      heatColor(clamp((v - 0.2) / 0.75, 0, 1), tmp);
      cols[i * 3] = tmp[0]; cols[i * 3 + 1] = tmp[1]; cols[i * 3 + 2] = tmp[2];
    }
    geo.computeVertexNormals();
    this.group.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
      vertexColors: true, roughness: 0.65, metalness: 0.25 })));
    // marching-squares de-locking ridge at r = 0.5
    const seg = [];
    const val = (d, a) => data.r[d][a];
    const X = (a) => (a / (na - 1) - 0.5) * W;
    const Z = (d) => (d / (nd - 1) - 0.5) * W;
    for (let d = 0; d < nd - 1; d++) for (let a = 0; a < na - 1; a++) {
      const v = [val(d, a), val(d, a + 1), val(d + 1, a + 1), val(d + 1, a)];
      const pts = [[X(a), Z(d)], [X(a + 1), Z(d)], [X(a + 1), Z(d + 1)], [X(a), Z(d + 1)]];
      const cross = [];
      for (let e2 = 0; e2 < 4; e2++) {
        const p = e2, q2 = (e2 + 1) % 4;
        if ((v[p] - 0.5) * (v[q2] - 0.5) < 0) {
          const f = (0.5 - v[p]) / (v[q2] - v[p]);
          cross.push([lerp(pts[p][0], pts[q2][0], f), lerp(pts[p][1], pts[q2][1], f), lerp(v[p], v[q2], f)]);
        }
      }
      for (let c2 = 0; c2 + 1 < cross.length; c2 += 2) {
        seg.push(cross[c2], cross[c2 + 1]);
      }
    }
    const rp = [];
    seg.forEach(([x, z, v]) => rp.push(new THREE.Vector3(x, v * 7 + 0.12, z)));
    this.group.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(rp),
      new THREE.LineBasicMaterial({ color: 0xff5f7e, linewidth: 2 })));
    // a second, golden ridge = tau_OR proxy contours feel — static accent ring
    const key = new THREE.PointLight(0x7fd8ff, 90, 0, 2); key.position.set(6, 10, 4);
    const fill = new THREE.PointLight(0xff5f7e, 40, 0, 2); fill.position.set(-8, 4, -6);
    this.group.add(key, fill, new THREE.AmbientLight(0x334455, 1.3));
    this.cam = { r: 23, phi: 1.0, theta: 0.75, t: [0, 0.5, 0] };
  }
  update(dt, t) { this.group.rotation.y = Math.sin(t * 0.15) * 0.12; }
}

// ============================================================
// SCENE 6 — plasma interlude: kink column + double layers
// ============================================================
class PlasmaScene {
  constructor() {
    this.group = new THREE.Group();
    this.np = 9000;
    this.ps = makeParticleSet(this.np, 0.15);
    this.group.add(this.ps.points);
    this.r0 = new Float32Array(this.np);
    this.th0 = new Float32Array(this.np);
    this.z0 = new Float32Array(this.np);
    this.H = 9; this.R = 1.6;
    for (let i = 0; i < this.np; i++) {
      this.r0[i] = this.R * Math.sqrt(Math.random());
      this.th0[i] = Math.random() * Math.PI * 2;
      this.z0[i] = (Math.random() * 2 - 1) * this.H;
    }
    // double-layer sheets (charge-separated planes — the "locked boundary")
    this.sheets = [];
    for (const z of [-4.5, 0, 4.5]) {
      const g = new THREE.PlaneGeometry(11, 11, 24, 24);
      const m = new THREE.MeshBasicMaterial({ color: 0x7fd8ff, transparent: true,
        opacity: 0.05, wireframe: true });
      const p = new THREE.Mesh(g, m);
      p.position.z = z; p.userData.z0 = z;
      this.group.add(p); this.sheets.push(p);
    }
    // field-line helices
    this.lines = [];
    const lineMat = new THREE.LineBasicMaterial({ color: 0xcc7a3a, transparent: true, opacity: 0.4 });
    for (let l = 0; l < 14; l++) {
      const pts = [];
      for (let s2 = 0; s2 < 120; s2++) {
        const z = -this.H + 2 * this.H * s2 / 119;
        const th = (l / 14) * Math.PI * 2 + z * 0.5;
        pts.push(new THREE.Vector3(2.3 * Math.cos(th), 2.3 * Math.sin(th), z));
      }
      const ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), lineMat);
      this.group.add(ln); this.lines.push(ln);
    }
    this.flash = [];
    this.cam = { r: 24, phi: 1.25, theta: 0.4, t: [0, 0, 0] };
  }
  update(dt, t) {
    const kz = Math.PI / this.H * 0.9;
    const eps = 0.06 + 0.5 * (0.5 + 0.5 * Math.sin(t * 0.4));
    const w = 0.55;
    for (let i = 0; i < this.np; i++) {
      const j = i * 3;
      const z = this.z0[i];
      const phase = kz * z - w * t;
      const shear = 0.25 + 0.55 * (this.r0[i] / this.R);
      const th = this.th0[i] + z * 0.5 + shear * t * 0.35;
      const dx = eps * Math.cos(phase), dy = eps * Math.sin(phase);
      this.ps.pos[j] = dx + this.r0[i] * Math.cos(th);
      this.ps.pos[j + 1] = dy + this.r0[i] * Math.sin(th);
      this.ps.pos[j + 2] = z;
      const core = 1 - this.r0[i] / this.R;
      this.ps.col[j] = (0.4 + 0.6 * core) * (0.7 + 0.5 * eps);
      this.ps.col[j + 1] = (0.15 + 0.3 * core) * (0.7 + 0.3 * eps);
      this.ps.col[j + 2] = 0.12 + 0.15 * core;
    }
    this.ps.geom.attributes.position.needsUpdate = true;
    this.ps.geom.attributes.color.needsUpdate = true;
    // sheets drift like breathing capacitor plates
    for (const s of this.sheets) {
      s.position.z = s.userData.z0 + Math.sin(t * 0.7 + s.userData.z0) * 0.4;
      s.material.opacity = 0.04 + 0.03 * Math.sin(t * 1.1 + s.userData.z0 * 2);
    }
    for (const l of this.lines) l.rotation.z = t * 0.1;
  }
}

// ============================================================
// SCENE 7 — epilogue: settling field + three falsifier fuses
// ============================================================
class EpilogueScene {
  constructor() {
    this.group = new THREE.Group();
    this.np = 1500;
    this.ps = makeParticleSet(this.np, 0.12);
    const rng = mulberry32(99);
    this.base = new Float32Array(this.np * 3);
    for (let i = 0; i < this.np; i++) {
      this.base[i * 3] = (rng() - 0.5) * 30;
      this.base[i * 3 + 1] = (rng() - 0.5) * 18;
      this.base[i * 3 + 2] = (rng() - 0.5) * 30;
      this.ps.col[i * 3] = 0.25; this.ps.col[i * 3 + 1] = 0.4; this.ps.col[i * 3 + 2] = 0.55;
    }
    this.ps.pos.set(this.base);
    this.group.add(this.ps.points);
    // three "fuses" — E1, E2, E3
    this.fuses = [];
    for (let k = 0; k < 3; k++) {
      const x = (k - 1) * 7;
      const pts = [new THREE.Vector3(x, -4, 0), new THREE.Vector3(x, 4, 0)];
      const ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),
        new THREE.LineBasicMaterial({ color: 0xffcf6e }));
      this.group.add(ln);
      const tip = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xffcf6e }));
      tip.position.set(x, -4, 0);
      this.group.add(tip);
      this.fuses.push({ ln, tip, k });
    }
    this.cam = { r: 26, phi: 1.3, theta: 0.5, t: [0, 0, 0] };
  }
  update(dt, t) {
    for (let i = 0; i < this.np; i++) {
      const j = i * 3;
      this.ps.pos[j] = this.base[j] + Math.sin(t * 0.3 + i) * 0.3;
      this.ps.pos[j + 1] = this.base[j + 1] + Math.sin(t * 0.23 + i * 1.7) * 0.5;
    }
    this.ps.geom.attributes.position.needsUpdate = true;
    for (const f of this.fuses) {
      // burning tip crawls upward, fades
      const ph = (t * 0.12 + f.k * 0.33) % 1;
      f.tip.position.y = -4 + 8 * ph;
      const a = 1 - ph;
      f.tip.material.color.setRGB(1, 0.7 * a + 0.2, 0.25);
      f.ln.material.color.setRGB(0.4 + 0.4 * a, 0.32 * a + 0.1, 0.12);
    }
  }
}

// ============================================================
// data loading + fallback
// ============================================================
async function loadMaps() {
  try {
    const res = await fetch('./data/maps.json');
    if (!res.ok) throw new Error(res.status);
    const d = await res.json();
    return {
      kappa: d.lock_map_base.kappa, eta: d.lock_map_base.eta,
      r: d.lock_map_base.r, rAne: d.lock_map_anes.r,
      perturb: d.perturb_map, baked: true,
    };
  } catch (e) {
    // file:// or missing data — synthesize a plausible stand-in (labeled)
    console.warn('maps.json unavailable, using synthetic landscape', e);
    const g = [];
    for (let i = 0; i < 22; i++) g.push(i / 21);
    const mk = (anes) => g.map(e => g.map(k => {
      const drive = 0.55 + 1.6 * k * (0.4 + 0.5) + 1.3 * e * 0.6 + 3.5 * k * e * 0.8;
      return clamp(0.3 + 0.12 * Math.log(drive) * (1 - 0.8 * anes), 0.05, 0.98);
    }));
    return {
      kappa: g, eta: g, r: mk(0), rAne: mk(0.45),
      perturb: { anes: g, det: g.map(x => x - 0.5), r: mk(0).map(row => row.slice()) },
      baked: false,
    };
  }
}

// ============================================================
// scroll orchestration
// ============================================================
const SCENE_ORDER = ['hero', 'chain', 'kuramoto', 'map', 'dp', 'perturb', 'plasma', 'epilogue'];
const SECTION_IDS = ['hero', 'ch-chain', 'ch-kuramoto', 'ch-map', 'ch-dp', 'ch-perturb', 'ch-plasma', 'ch-epilogue'];

const dotsNav = document.getElementById('dots');
SECTION_IDS.forEach((id, i) => {
  const a = document.createElement('a');
  a.href = '#' + id;
  dotsNav.appendChild(a);
});

let scenes = null;

function sectionProgress() {
  // for each section, compute how far through it we are
  const y = scrollY, vh = innerHeight;
  let active = 0, local = 0;
  SECTION_IDS.forEach((id, i) => {
    const el = document.getElementById(id);
    const top = el.offsetTop, hgt = el.offsetHeight;
    if (y + vh * 0.5 >= top && y + vh * 0.5 < top + hgt) {
      active = i;
      local = clamp((y + vh * 0.5 - top) / hgt, 0, 1);
    }
  });
  return { active, local };
}

async function main() {
  const maps = await loadMaps();
  // ?scene=N pins a scene directly (deep link / debugging)
  const sceneParam = new URLSearchParams(location.search).get('scene');
  const pinned = sceneParam !== null
    ? clamp(parseInt(sceneParam, 10), 0, SECTION_IDS.length - 1) : null;
  if (pinned !== null) document.getElementById('spine').style.display = 'none';
  scenes = [
    new MicrotubuleScene(),
    new LadderScene(),
    new KuramotoScene(),
    new MapScene({ kappa: maps.kappa, eta: maps.eta, r: maps.r, rAne: maps.rAne }),
    new DPScene(),
    new PerturbScene(maps.perturb),
    new PlasmaScene(),
    new EpilogueScene(),
  ];
  scenes.forEach(s => { s.group.visible = false; scene.add(s.group); });
  // ambient dust shared by all scenes
  const dust = makeParticleSet(500, 0.09);
  for (let i = 0; i < 500; i++) {
    dust.pos[i * 3] = (Math.random() - 0.5) * 80;
    dust.pos[i * 3 + 1] = (Math.random() - 0.5) * 50;
    dust.pos[i * 3 + 2] = (Math.random() - 0.5) * 80;
    dust.col[i * 3] = 0.10; dust.col[i * 3 + 1] = 0.16; dust.col[i * 3 + 2] = 0.24;
  }
  scene.add(dust.points);

  // live controls wiring
  const bind = (id, vid, key, fmt) => {
    const el2 = document.getElementById(id);
    el2.addEventListener('input', () => {
      const v = parseFloat(el2.value);
      PTC.params[key] = v;
      PTC.rebuild();
      document.getElementById(vid).textContent = v.toFixed(2);
    });
  };
  bind('sAnes', 'vAnes', 'anes'); bind('sDet', 'vDet', 'det');
  bind('sKap', 'vKap', 'kappa'); bind('sEta', 'vEta', 'eta');
  const ctl = document.getElementById('ctl');

  let activeIdx = -1;
  let sceneT = 0;
  const stats = document.getElementById('stats');
  let last = performance.now(), frames = 0, fpsT = 0, fps = 0;

  function frame(now) {
    const dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    sceneT += dt;
    const { active, local } = pinned !== null
      ? { active: pinned, local: sceneT % 1 }
      : sectionProgress();
    if (active !== activeIdx) {
      if (activeIdx >= 0) scenes[activeIdx].group.visible = false;
      activeIdx = active;
      scenes[activeIdx].group.visible = true;
      const c = scenes[activeIdx].cam;
      orbit.preset(c.r, c.phi, c.theta, c.t[0], c.t[1], c.t[2]);
      ctl.classList.toggle('show', SCENE_ORDER[activeIdx] === 'kuramoto');
      [...dotsNav.children].forEach((d, i) => d.classList.toggle('on', i === activeIdx));
    }
    scenes[activeIdx].update(dt, sceneT, local);
    orbit.update(camera, dt);
    renderer.render(scene, camera);
    frames++; fpsT += dt;
    if (fpsT > 0.5) { fps = Math.round(frames / fpsT); frames = 0; fpsT = 0; }
    stats.textContent = `${fps} fps · ${maps.baked ? 'baked sweep data' : 'synthetic preview'} · ${SCENE_ORDER[activeIdx]}`;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
main();
