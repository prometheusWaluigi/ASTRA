import * as THREE from 'three';

// ---------- renderer / scene ----------
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
} catch (e) {
  document.getElementById('modeTitle').textContent = 'WebGL unavailable';
  document.getElementById('modeBlurb').textContent =
    'The browser could not create a WebGL context. If the GPU was just restarted, reload the page or restart the browser.';
  throw e;
}
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
renderer.setSize(innerWidth, innerHeight);
renderer.setClearColor(0x000005, 1);
document.getElementById('app').appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, 0.1, 400);

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

// ---------- minimal orbit controls ----------
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
class OrbitCam {
  constructor(dom) {
    this.theta = 0.9; this.phi = 1.15; this.r = 24;
    this.tTheta = this.theta; this.tPhi = this.phi; this.tR = this.r;
    this.target = new THREE.Vector3();
    this.autoSpin = true; this.idle = 0; this.drag = false;
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
    dom.addEventListener('pointerup', () => { this.drag = false; });
    dom.addEventListener('wheel', e => {
      e.preventDefault();
      this.tR = clamp(this.tR * Math.exp(e.deltaY * 0.001), 4, 90);
      this.idle = 0;
    }, { passive: false });
  }
  preset(r, phi, theta) { this.tR = r; this.tPhi = phi; if (theta !== undefined) this.tTheta = theta; }
  update(cam, dt) {
    this.idle += dt;
    if (this.autoSpin && !this.drag && this.idle > 4) this.tTheta += dt * 0.07;
    const k = 1 - Math.exp(-dt * 7);
    this.theta += (this.tTheta - this.theta) * k;
    this.phi += (this.tPhi - this.phi) * k;
    this.r += (this.tR - this.r) * k;
    const sp = Math.sin(this.phi);
    cam.position.set(
      this.target.x + this.r * sp * Math.cos(this.theta),
      this.target.y + this.r * Math.cos(this.phi),
      this.target.z + this.r * sp * Math.sin(this.theta));
    cam.lookAt(this.target);
  }
}
const orbit = new OrbitCam(renderer.domElement);

// ---------- shared FX helpers ----------
const glowTex = (() => {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d');
  const grad = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  grad.addColorStop(0, 'rgba(255,255,255,1)');
  grad.addColorStop(0.25, 'rgba(255,255,255,.55)');
  grad.addColorStop(0.6, 'rgba(255,255,255,.12)');
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

// expanding glow flashes (reconnection events, disruptions, vortex mergers)
class FlashPool {
  constructor(parent, n = 24) {
    this.items = [];
    for (let i = 0; i < n; i++) {
      const s = new THREE.Sprite(new THREE.SpriteMaterial({
        map: glowTex, transparent: true, depthWrite: false,
        blending: THREE.AdditiveBlending, opacity: 0,
      }));
      s.visible = false; parent.add(s);
      this.items.push({ s, t: 0, dur: 1, s0: 1 });
    }
    this.i = 0;
  }
  spawn(x, y, z, scale, color, dur = 0.9) {
    const it = this.items[this.i++ % this.items.length];
    it.s.position.set(x, y, z);
    it.s.material.color.set(color);
    it.s.visible = true; it.t = 0; it.dur = dur; it.s0 = scale;
  }
  update(dt) {
    for (const it of this.items) {
      if (!it.s.visible) continue;
      it.t += dt;
      const k = it.t / it.dur;
      if (k >= 1) { it.s.visible = false; continue; }
      const sc = it.s0 * (0.35 + 2.4 * k);
      it.s.scale.set(sc, sc, 1);
      it.s.material.opacity = Math.pow(1 - k, 1.7);
    }
  }
}

// fast burst particles (reconnection jets, disruption debris)
class Bursts {
  constructor(parent, n = 1800) {
    this.ps = makeParticleSet(n, 0.11);
    parent.add(this.ps.points);
    this.vel = new Float32Array(n * 3);
    this.base = new Float32Array(n * 3);
    this.life = new Float32Array(n);
    this.life0 = new Float32Array(n);
    this.i = 0;
    for (let i = 0; i < n; i++) this.ps.pos[i * 3 + 1] = 1e6;
  }
  spawn(x, y, z, vx, vy, vz, r, g, b, life) {
    const i = this.i++ % this.ps.n;
    this.ps.pos.set([x, y, z], i * 3);
    this.vel.set([vx, vy, vz], i * 3);
    this.base.set([r, g, b], i * 3);
    this.life[i] = this.life0[i] = life;
  }
  update(dt) {
    const { pos, col, n } = this.ps;
    for (let i = 0; i < n; i++) {
      if (this.life[i] <= 0) continue;
      this.life[i] -= dt;
      const j = i * 3;
      pos[j] += this.vel[j] * dt; pos[j + 1] += this.vel[j + 1] * dt; pos[j + 2] += this.vel[j + 2] * dt;
      const drag = Math.exp(-dt * 0.8);
      this.vel[j] *= drag; this.vel[j + 1] *= drag; this.vel[j + 2] *= drag;
      const f = Math.max(0, this.life[i] / this.life0[i]);
      col[j] = this.base[j] * f; col[j + 1] = this.base[j + 1] * f; col[j + 2] = this.base[j + 2] * f;
    }
    this.ps.geom.attributes.position.needsUpdate = true;
    this.ps.geom.attributes.color.needsUpdate = true;
  }
}

// multi-strip field lines rendered as one LineSegments buffer
function makeLineSet(parent, maxVerts) {
  const geom = new THREE.BufferGeometry();
  const pos = new Float32Array(maxVerts * 3);
  const col = new Float32Array(maxVerts * 3);
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(col, 3));
  const mat = new THREE.LineBasicMaterial({
    vertexColors: true, transparent: true, depthWrite: false,
    blending: THREE.AdditiveBlending, opacity: 0.75,
  });
  const lines = new THREE.LineSegments(geom, mat);
  lines.frustumCulled = false;
  parent.add(lines);
  return { geom, pos, col, used: 0, max: maxVerts };
}
function lineSetBegin(ls) { ls.used = 0; }
function lineStrip(ls, pts, r, g, b) {
  // pts: flat [x,y,z,...]; emits connected segment pairs with end fade
  const np = pts.length / 3;
  if (np < 2) return;
  for (let i = 0; i < np - 1; i++) {
    if (ls.used + 2 > ls.max) return;
    for (const k of [i, i + 1]) {
      const fade = Math.sin(Math.PI * k / (np - 1));
      const j = ls.used * 3;
      ls.pos[j] = pts[k * 3]; ls.pos[j + 1] = pts[k * 3 + 1]; ls.pos[j + 2] = pts[k * 3 + 2];
      ls.col[j] = r * fade; ls.col[j + 1] = g * fade; ls.col[j + 2] = b * fade;
      ls.used++;
    }
  }
}
function lineSetEnd(ls) {
  ls.geom.setDrawRange(0, ls.used);
  ls.geom.attributes.position.needsUpdate = true;
  ls.geom.attributes.color.needsUpdate = true;
}

const lerp = (a, b, t) => a + (b - a) * t;
// palette ramp: 3 stops
function ramp(t, c0, c1, c2, out) {
  if (t < 0.5) { const u = t * 2; out[0] = lerp(c0[0], c1[0], u); out[1] = lerp(c0[1], c1[1], u); out[2] = lerp(c0[2], c1[2], u); }
  else { const u = t * 2 - 1; out[0] = lerp(c1[0], c2[0], u); out[1] = lerp(c1[1], c2[1], u); out[2] = lerp(c1[2], c2[2], u); }
}

// ============================================================
// MODE 1 — Parker flux-rope braiding + nanoflare reconnection
// ============================================================
class BraidMode {
  constructor(group) {
    this.group = group;
    this.Z = 15; this.B0 = 5; this.BOUND = 6.5;
    this.np = 16000;
    this.ps = makeParticleSet(this.np, 0.16);
    group.add(this.ps.points);
    this.lines = makeLineSet(group, 40 * 150 * 2);
    this.bursts = new Bursts(group);
    this.flash = new FlashPool(group);
    // transverse flux blobs: opposite-signed psi = squeezable flux regions
    this.blobs = [];
    for (let i = 0; i < 6; i++) {
      this.blobs.push({
        A: (i % 2 ? -1 : 1) * (1.4 + Math.random() * 1.2),
        ax: 2.0 + Math.random() * 1.6, ay: 2.0 + Math.random() * 1.6,
        wx: 0.11 + Math.random() * 0.1, wy: 0.09 + Math.random() * 0.1,
        px: Math.random() * 6.28, py: Math.random() * 6.28,
        s2: 2.2 + Math.random() * 1.4,
        x: 0, y: 0,
      });
    }
    this.pairCool = new Map();
    this.p = new Float32Array(this.np * 3);
    for (let i = 0; i < this.np; i++) this.respawn(i, true);
    this.camPreset = { r: 26, phi: 1.25 };
  }
  respawn(i, anyZ) {
    const r = Math.sqrt(Math.random()) * 4.5, a = Math.random() * 6.283;
    this.p[i * 3] = r * Math.cos(a);
    this.p[i * 3 + 1] = r * Math.sin(a);
    this.p[i * 3 + 2] = (Math.random() * 2 - 1) * this.Z;
    if (!anyZ) this.p[i * 3 + 2] = -this.Z + Math.random() * 2;
  }
  field(x, y, out) {
    let bx = 0, by = 0;
    for (const b of this.blobs) {
      const dx = x - b.x, dy = y - b.y;
      const e = b.A * Math.exp(-(dx * dx + dy * dy) / b.s2) / b.s2;
      bx += -2 * dy * e; by += 2 * dx * e;
    }
    out[0] = bx; out[1] = by; out[2] = this.B0;
  }
  step(dt, t) {
    for (const b of this.blobs) {
      b.x = b.ax * Math.cos(b.wx * t + b.px);
      b.y = b.ay * Math.sin(b.wy * t + b.py);
    }
    // reconnection: opposite-signed flux regions squeezed together -> nanoflare jets
    for (let i = 0; i < this.blobs.length; i++) {
      for (let j = i + 1; j < this.blobs.length; j++) {
        const a = this.blobs[i], c = this.blobs[j];
        if (a.A * c.A > 0) continue;
        const dx = a.x - c.x, dy = a.y - c.y;
        if (dx * dx + dy * dy < 2.6) {
          const key = i * 16 + j;
          if (t - (this.pairCool.get(key) || -9) > 1.4) {
            this.pairCool.set(key, t);
            const mx = (a.x + c.x) / 2, my = (a.y + c.y) / 2, mz = (Math.random() * 2 - 1) * this.Z * 0.8;
            this.flash.spawn(mx, my, mz, 2.6, 0xff70d0);
            for (let s = 0; s < 70; s++) {
              const dir = Math.random() < 0.5 ? 1 : -1;
              const sp = 8 + Math.random() * 9;
              this.bursts.spawn(mx, my, mz,
                (Math.random() - 0.5) * 1.6, (Math.random() - 0.5) * 1.6, dir * sp,
                1.0, 0.35, 0.85, 0.7 + Math.random() * 0.5);
            }
          }
        }
      }
    }
    // advect particles along B (plus faint cross-field diffusion shimmer)
    const f = [0, 0, 0];
    const { pos, col } = this.ps;
    const c0 = [0.02, 0.10, 0.35], c1 = [0.1, 0.75, 1.0], c2 = [1.0, 1.0, 1.0], tc = [0, 0, 0];
    for (let i = 0; i < this.np; i++) {
      const j = i * 3;
      let x = this.p[j], y = this.p[j + 1], z = this.p[j + 2];
      this.field(x, y, f);
      const inv = 1 / Math.hypot(f[0], f[1], f[2]);
      const vp = 5.5;
      x += f[0] * inv * vp * dt + (Math.random() - 0.5) * 0.55 * dt;
      y += f[1] * inv * vp * dt + (Math.random() - 0.5) * 0.55 * dt;
      z += f[2] * inv * vp * dt;
      if (z > this.Z) z -= 2 * this.Z;
      if (x * x + y * y > this.BOUND * this.BOUND) { this.respawn(i, false); x = this.p[j]; y = this.p[j + 1]; z = this.p[j + 2]; }
      this.p[j] = x; this.p[j + 1] = y; this.p[j + 2] = z;
      pos[j] = x; pos[j + 1] = y; pos[j + 2] = z;
      const bp = Math.hypot(f[0], f[1]) / this.B0;
      ramp(clamp(bp * 3.2, 0, 1), c0, c1, c2, tc);
      col[j] = tc[0]; col[j + 1] = tc[1]; col[j + 2] = tc[2];
    }
    this.ps.geom.attributes.position.needsUpdate = true;
    this.ps.geom.attributes.color.needsUpdate = true;
    // field lines through the braid
    lineSetBegin(this.lines);
    const ds = 0.32, steps = 120;
    for (let l = 0; l < 40; l++) {
      const rr = Math.sqrt(Math.random()) * 4.2, aa = Math.random() * 6.283;
      let sx = rr * Math.cos(aa), sy = rr * Math.sin(aa);
      const pts = [];
      let x = sx, y = sy, z = -this.Z;
      for (let s = 0; s < steps; s++) {
        this.field(x, y, f);
        const inv = ds / Math.hypot(f[0], f[1], f[2]);
        x += f[0] * inv; y += f[1] * inv; z += f[2] * inv;
        if (z > this.Z || x * x + y * y > this.BOUND * this.BOUND * 1.4) break;
        pts.push(x, y, z);
      }
      lineStrip(this.lines, pts, 0.12, 0.45, 0.9);
    }
    lineSetEnd(this.lines);
    this.bursts.update(dt);
    this.flash.update(dt);
  }
  dispose() { this.group.clear(); }
}

// ============================================================
// MODE 2 — m=1 kink instability (writhing plasma column)
// ============================================================
class KinkMode {
  constructor(group) {
    this.group = group;
    this.H = 9; this.R = 1.5;
    this.np = 15000;
    this.ps = makeParticleSet(this.np, 0.17);
    group.add(this.ps.points);
    this.lines = makeLineSet(group, 24 * 160 * 2);
    this.bursts = new Bursts(group);
    this.flash = new FlashPool(group);
    this.r0 = new Float32Array(this.np);
    this.th0 = new Float32Array(this.np);
    this.z0 = new Float32Array(this.np);
    for (let i = 0; i < this.np; i++) {
      this.r0[i] = this.R * Math.sqrt(Math.random());
      this.th0[i] = Math.random() * 6.283;
      this.z0[i] = (Math.random() * 2 - 1) * this.H;
    }
    this.tMode = -1.0; this.twistSign = 1; this.dir = 1;
    this.camPreset = { r: 22, phi: 1.3 };
  }
  step(dt, t) {
    this.tMode += dt;
    const tm = Math.max(0, this.tMode);
    const kz = Math.PI / this.H * 0.9;
    const eps = 0.05 * Math.exp(0.6 * tm);        // exponential linear growth
    const epsMax = 2.1;
    const w = this.dir * 0.55;                    // kink rotation rate
    const sausage = Math.pow(Math.max(0, Math.sin(0.55 * t)), 3) * 0.3;
    const twist = 0.55 * this.twistSign;
    const { pos, col } = this.ps;
    const heat = clamp(eps / epsMax, 0, 1);
    for (let i = 0; i < this.np; i++) {
      const j = i * 3;
      const z = this.z0[i];
      const phase = kz * z - w * t;
      const dx = eps * Math.cos(phase), dy = eps * Math.sin(phase);
      const shear = 0.25 + 0.55 * (this.r0[i] / this.R);
      const th = this.th0[i] + z * twist + shear * t * 0.4;
      const rm = this.r0[i] * (1 + sausage * Math.cos(2 * kz * z + 1.3));
      pos[j] = dx + rm * Math.cos(th);
      pos[j + 1] = dy + rm * Math.sin(th);
      pos[j + 2] = z;
      const core = 1 - this.r0[i] / this.R;
      col[j] = (0.35 + 0.65 * core) * (0.6 + 0.8 * heat);
      col[j + 1] = (0.12 + 0.3 * core) * (0.6 + 0.5 * heat);
      col[j + 2] = (0.03 + 0.1 * core) * (0.6 + 0.3 * heat);
    }
    this.ps.geom.attributes.position.needsUpdate = true;
    this.ps.geom.attributes.color.needsUpdate = true;
    // magnetic field helices riding the same displacement
    lineSetBegin(this.lines);
    const steps = 150;
    for (let l = 0; l < 24; l++) {
      const rl = [0.55, 1.05, 1.5][l % 3];
      const th0 = (l / 24) * 6.283 + (l % 3) * 0.7;
      const pts = [];
      for (let s = 0; s < steps; s++) {
        const z = -this.H + (2 * this.H * s) / (steps - 1);
        const phase = kz * z - w * t;
        const th = th0 + z * twist + 0.25 * t * 0.4;
        const rm = rl * (1 + sausage * Math.cos(2 * kz * z + 1.3));
        pts.push(
          eps * Math.cos(phase) + rm * Math.cos(th),
          eps * Math.sin(phase) + rm * Math.sin(th),
          z);
      }
      lineStrip(this.lines, pts, 0.9, 0.5, 0.12);
    }
    lineSetEnd(this.lines);
    // disruption: kink saturates -> rapid energy release, then column reforms
    if (eps > epsMax) {
      for (let s = 0; s < 6; s++) {
        const z = (Math.random() * 2 - 1) * this.H;
        this.flash.spawn(eps * Math.cos(kz * z - w * t), eps * Math.sin(kz * z - w * t), z, 3.2, 0xff5522, 1.1);
      }
      for (let s = 0; s < 400; s++) {
        const i = (Math.random() * this.np) | 0;
        const j = i * 3;
        const a = Math.random() * 6.283, sp = 2 + Math.random() * 7;
        this.bursts.spawn(pos[j], pos[j + 1], pos[j + 2],
          Math.cos(a) * sp, Math.sin(a) * sp, (Math.random() - 0.5) * 8,
          1.0, 0.45, 0.12, 0.8 + Math.random() * 0.7);
      }
      this.tMode = -0.9;
      if (Math.random() < 0.4) { this.twistSign *= -1; this.dir *= -1; }
    }
    this.bursts.update(dt);
    this.flash.update(dt);
  }
  dispose() { this.group.clear(); }
}

// ============================================================
// MODE 3 — Diocotron shear: vortex crystal on a charged ring
// ============================================================
class VortexMode {
  constructor(group) {
    this.group = group;
    this.Rr = 6; this.wr = 1.5; this.w0 = 0.5; this.core2 = 0.35;
    this.np = 18000;
    this.ps = makeParticleSet(this.np, 0.15);
    group.add(this.ps.points);
    this.bursts = new Bursts(group);
    this.flash = new FlashPool(group);
    this.p = new Float32Array(this.np * 3);
    for (let i = 0; i < this.np; i++) this.respawn(i);
    this.vorts = [];
    for (let i = 0; i < 6; i++) {
      this.vorts.push({ ang: (i / 6) * 6.283, amp: 0.8 + Math.random() * 0.9, t0: -i });
    }
    this.mergeCool = 0;
    this.camPreset = { r: 20, phi: 0.85 };
  }
  respawn(i) {
    const r = this.Rr + (Math.random() * 2 - 1) * 2.6;
    const a = Math.random() * 6.283;
    this.p[i * 3] = r * Math.cos(a);
    this.p[i * 3 + 1] = r * Math.sin(a);
    this.p[i * 3 + 2] = (Math.random() - 0.5) * 0.5;
  }
  flow(x, y, out) {
    const r = Math.hypot(x, y) + 1e-6;
    const om = this.w0 * Math.exp(-(((r - this.Rr) / this.wr) ** 2));
    let ux = -y * om, uy = x * om;
    for (const v of this.vorts) {
      const dx = x - v.x, dy = y - v.y;
      const d2 = dx * dx + dy * dy + this.core2;
      ux += -dy * v.a / d2; uy += dx * v.a / d2;
    }
    out[0] = ux; out[1] = uy;
  }
  step(dt, t) {
    for (const v of this.vorts) {
      v.a = v.amp * clamp((t - v.t0) * 0.5, 0.05, 1); // vortices spin up
      v.x = this.Rr * Math.cos(v.ang); v.y = this.Rr * Math.sin(v.ang);
      v.ang += (this.w0 + 0.06 * v.a / this.Rr) * dt;
    }
    // merger: two strong vortices that drift together coalesce with a burst
    if (t > this.mergeCool) {
      for (let i = 0; i < this.vorts.length; i++) {
        for (let j = i + 1; j < this.vorts.length; j++) {
          let d = Math.abs(this.vorts[i].ang - this.vorts[j].ang) % 6.283;
          if (d > Math.PI) d = 6.283 - d;
          if (d < 0.22 && this.vorts[i].a > 0.6 && this.vorts[j].a > 0.6) {
            const a = this.vorts[i], b = this.vorts[j];
            a.amp = Math.min(2.6, Math.hypot(a.amp, b.amp));
            this.vorts.splice(j, 1);
            const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
            this.flash.spawn(mx, my, 0, 3.4, 0x9a6bff, 1.0);
            for (let s = 0; s < 90; s++) {
              const an = Math.random() * 6.283, sp = 1.5 + Math.random() * 5;
              this.bursts.spawn(mx, my, 0, Math.cos(an) * sp, Math.sin(an) * sp,
                (Math.random() - 0.5) * 2, 0.55, 0.4, 1.0, 0.9 + Math.random() * 0.6);
            }
            // a fresh weak vortex nucleates elsewhere -> the crystal churns forever
            this.vorts.push({ ang: Math.random() * 6.283, amp: 0.5 + Math.random() * 0.5, t0: t });
            this.mergeCool = t + 2.0;
            i = j = 99;
          }
        }
      }
    }
    const f = [0, 0];
    const { pos, col } = this.ps;
    const c0 = [0.02, 0.18, 0.3], c1 = [0.15, 0.9, 0.8], c2 = [0.75, 0.4, 1.0], tc = [0, 0, 0];
    for (let i = 0; i < this.np; i++) {
      const j = i * 3;
      let x = this.p[j], y = this.p[j + 1];
      this.flow(x, y, f);
      x += f[0] * dt; y += f[1] * dt;
      const r = Math.hypot(x, y);
      if (r > 11.5 || r < 0.6) { this.respawn(i); x = this.p[j]; y = this.p[j + 1]; }
      this.p[j] = x; this.p[j + 1] = y;
      this.p[j + 2] += Math.sin(t * 1.3 + i) * 0.0004;
      pos[j] = x; pos[j + 1] = y; pos[j + 2] = this.p[j + 2];
      const sp = Math.hypot(f[0], f[1]);
      ramp(clamp(sp * 0.55, 0, 1), c0, c1, c2, tc);
      col[j] = tc[0]; col[j + 1] = tc[1]; col[j + 2] = tc[2];
    }
    this.ps.geom.attributes.position.needsUpdate = true;
    this.ps.geom.attributes.color.needsUpdate = true;
    this.bursts.update(dt);
    this.flash.update(dt);
  }
  dispose() { this.group.clear(); }
}

// ---------- mode registry / HUD ----------
const MODES = [
  {
    title: '1 · Flux-Rope Braiding (Parker braid)',
    blurb: 'Oppositely-twisted magnetic flux regions wander and squeeze together. Where they press, the field reconnects and fires nanoflare jets — one theory for why the solar corona is millions of degrees hotter than the surface.',
    make: g => new BraidMode(g),
  },
  {
    title: '2 · Kink Instability (m=1)',
    blurb: 'A current-carrying plasma column amplifies its own helical wobble exponentially until it disrupts — the instability that ends tokamak shots. Watch the field helices writhe, then blow apart and reform.',
    make: g => new KinkMode(g),
  },
  {
    title: '3 · Diocotron Vortex Shear',
    blurb: 'A ring of non-neutral plasma shears itself into a vortex crystal. Same-sign vortices orbit, pair up, and merge violently — a plasma doing fluid dynamics through pure E×B drift.',
    make: g => new VortexMode(g),
  },
];

const group = new THREE.Group();
scene.add(group);
let modeIdx = -1, mode = null;
const btnBox = document.getElementById('modeBtns');
MODES.forEach((m, i) => {
  const b = document.createElement('button');
  b.textContent = `${i + 1}`;
  b.title = m.title;
  b.onclick = () => setMode(i);
  btnBox.appendChild(b);
});
function setMode(i) {
  if (mode) mode.dispose();
  modeIdx = i;
  mode = MODES[i].make(group);
  document.getElementById('modeTitle').textContent = MODES[i].title;
  document.getElementById('modeBlurb').textContent = MODES[i].blurb;
  [...btnBox.children].forEach((b, j) => b.classList.toggle('active', j === i));
  orbit.preset(mode.camPreset.r, mode.camPreset.phi);
}
addEventListener('keydown', e => {
  if (e.key >= '1' && e.key <= String(MODES.length)) setMode(+e.key - 1);
  if (e.key === ' ') { e.preventDefault(); orbit.autoSpin = !orbit.autoSpin; }
  if (e.key === 'r' || e.key === 'R') setMode(modeIdx);
});
setMode(0);

// ---------- main loop ----------
const statsEl = document.getElementById('stats');
let last = performance.now(), acc = 0, frames = 0, fps = 0;
function tick(now) {
  requestAnimationFrame(tick);
  const dt = Math.min(0.033, (now - last) / 1000);
  last = now;
  const t = now / 1000;
  mode.step(dt, t);
  orbit.update(camera, dt);
  renderer.render(scene, camera);
  acc += dt; frames++;
  if (acc > 0.5) {
    fps = Math.round(frames / acc); acc = 0; frames = 0;
    statsEl.textContent = `${fps} fps · ${mode.np.toLocaleString()} particles`;
  }
}
requestAnimationFrame(tick);
