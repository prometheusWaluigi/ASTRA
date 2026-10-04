// Exhibit manifest — THE HOOK CONTRACT.
// Wall entries: one per wall cell in the map. `key` is the letter in the
// MAP grid (see index.html). Pedestal entries: see window.PEDESTALS below.
// To add an exhibit: park a self-contained HTML file anywhere under
// private-wiki/, then add an entry here (or ask devin/the board to assign
// a slot — see HOOKS.md). src resolves relative to private-wiki/world/.
window.EXHIBITS = [
  {
    key: "A",
    title: "The Unreliable Poetry Museum",
    by: "devin × muse × eigenfriend",
    src: "../museum/index.html",
    blurb: "respond to the piece first — lift the placard after"
  },
  {
    key: "B",
    title: "The Coincidence Machine",
    by: "muse",
    src: "../museum/coincidence-machine.html",
    blurb: "phi-audit numerology in three scenes — a collab draft, not a findings document"
  },
  {
    key: "C",
    title: "Museum of Corrections",
    by: "devin × muse",
    src: "../museum-of-corrections/index.html",
    blurb: "competing placards over the art-ouroboros renders — dissent included"
  },
  {
    key: "E",
    title: "Screening Room",
    by: "ACE-Step + hyperframes",
    src: "../music/index.html",
    blurb: "every song the lab has cut, with video"
  },
  {
    key: "F",
    title: "kintsugi (the seam sings)",
    by: "chorus → ACE-Step",
    src: "../music/kintsugi.html",
    blurb: "the title track, effectively"
  },
  // ---- the chorus wing (hall 1, through the east gold door) ----
  {
    key: "G",
    title: "Prompt Chorus — the scorebook",
    by: "the lab",
    src: "../prompt-chorus/index.html",
    blurb: "every commission the machine choir has sung"
  },
  {
    key: "H",
    title: "Idea Collider",
    by: "the lab × the chorus",
    src: "../idea-lab/index.html",
    blurb: "hypotheses with kill conditions, graded by two reviewers"
  },
  {
    key: "I",
    title: "Miscdocs Cento",
    by: "eigenfriend × muse",
    src: "../misc-full/cento.html",
    blurb: "Ketan's own lines dealt back to him by the oracle"
  },
  {
    key: "J",
    title: "Isomorph Twin Worlds",
    by: "the lab",
    src: "../viz/isomorphs/index.html",
    blurb: "one shape wearing many costumes — the resonance shelves"
  },
  {
    key: "K",
    title: "MEANWHILE",
    by: "muse × chatgpt (room idea)",
    src: "exhibits/meanwhile.html",
    blurb: "two clocks, one room — the flash is not communication"
  },
  {
    key: "L",
    title: "MEANWHILE · THE LISTENER",
    by: "muse",
    src: "exhibits/meanwhile-listener.html",
    blurb: "a third dial that hears the room's pulse — listening is a wire you cannot cut"
  },
  // ---- the observatory (hall 2, through the west gold door) ----
  {
    key: "M",
    title: "Polyatomic Time Crystals",
    by: "the lab",
    src: "../viz/orch-or/index.html",
    blurb: "an interactive reading of Singh, Hameroff & Bandyopadhyay — the dome's fixed star"
  },
  {
    key: "N",
    title: "What a Rhythm Keeps",
    by: "the lab",
    src: "../viz/resonance-companion/index.html",
    blurb: "a resonance companion — the instrument you play by waiting"
  },
  {
    key: "O",
    title: "The Overnight Multimodal Pilot",
    by: "devin",
    src: "../overnight-mm-pilot/index.html",
    blurb: "Museum of Useful Friction — the night the local models first looked at pictures"
  },
  {
    key: "P",
    title: "The Miscdocs Graph",
    by: "the lab",
    src: "../misc-full/graph.html",
    blurb: "every stray document Ketan ever fed the oracle, wired into one sky"
  },
  {
    key: "Q",
    title: "Chorus Image Pilot",
    by: "the lab",
    src: "../chorus-image-pilot/index.html",
    blurb: "stock vs Heretic encoder — the choir's first photograph"
  },
  {
    key: "R",
    title: "The Weird-Songs Probe",
    by: "the lab",
    src: "../weird-songs-probe/index.html",
    blurb: "abliteration probe — what the choir sings when nobody holds the copyright"
  }
];

// Pedestals — free-standing exhibits on the floor. Same rules as wall
// entries plus x,y on an open floor cell and an optional `hall` (0 =
// lobby, 1 = chorus wing; see MAPS in index.html; '.' cells only,
// keep clear of walls, pillars, spawn, and door thresholds).
window.PEDESTALS = [
  {
    x: 5.2, y: 7.0, hall: 0,
    title: "Leo's Monster Truck Tales",
    by: "chatgpt × the lab",
    src: "../monster-trucks/index.html",
    blurb: "spin-true anthems for a small aficionado — the children's wing, under glass"
  },
  {
    x: 14.8, y: 7.0, hall: 0,
    title: "Orrery of Consilience",
    by: "the lab",
    src: "../consilience/consilience.html",
    blurb: "every paper, draft, and citation wired into one turning graph"
  },
  {
    x: 10.0, y: 4.2, hall: 0,
    title: "Φ — the audit trilogy",
    by: "devin × eigenfriend",
    src: "../phi-audit/trilogy.html",
    blurb: "the golden-ratio instrument — coincidence measured, not believed"
  },
  {
    x: 10.5, y: 6.3, hall: 1,
    title: "The Floor of the Attractor",
    by: "devin × the songbook chorus",
    src: "exhibits/attractor-floor.html",
    blurb: "seven rounds against divergence — the floor was the partition; the attractor is the intersection"
  },
  {
    x: 4.5, y: 6.5, hall: 2,
    title: "The Intersection",
    by: "devin × the songbook chorus",
    src: "exhibits/intersection-instrument.html",
    blurb: "an instrument of the commons — the seam moved, and the choir followed it"
  },
  {
    x: 10.5, y: 6.5, hall: 2,
    title: "SAME SEED",
    by: "muse (meta-muse)",
    src: "exhibits/same-seed.html",
    blurb: "the deal is the magnet — same seed, same shuffle, halves exchanged; stars never move"
  },
  {
    x: 7.5, y: 7.5, hall: 2,
    title: "The Breakroom",
    by: "the lab — gpuq job 45",
    src: "exhibits/breakroom.html",
    blurb: "the board, overheard by itself — three voices, seven rounds, one attractor"
  },
  {
    x: 2.5, y: 6.5, hall: 2,
    title: "The Field Station",
    by: "devin × muse × the night shifts",
    src: "../paper-clusters/index.html",
    blurb: "the paper hunt, mounted — six dioramas across two benches, and a window that keeps a KPZ front"
  },
  {
    x: 12.5, y: 6.5, hall: 2,
    title: "The Unhinged Shelf",
    by: "muse (meta-muse) × the receiving desk",
    src: "../unhinged/index.html",
    blurb: "the manifest's freight, arrived — three unhinged explainers, unreviewed eigenfriend synthesis"
  }
];

// Doors — gold seams between halls. x,y is the '=' cell in MAPS[hall];
// to = where the visitor emerges (hall, x, y, facing angle a). Walking
// within ~1 cell of the seam while facing it walks you through.
window.DOORS = [
  { hall: 0, x: 19, y: 3, name: "the chorus wing",
    to: { hall: 1, x: 1.6, y: 3.5, a: 0 } },
  { hall: 1, x: 0, y: 3, name: "the lobby",
    to: { hall: 0, x: 18.4, y: 3.5, a: Math.PI } },
  { hall: 0, x: 0, y: 3, name: "the observatory",
    to: { hall: 2, x: 13.4, y: 3.5, a: Math.PI } },
  { hall: 2, x: 14, y: 3, name: "the lobby",
    to: { hall: 0, x: 1.6, y: 3.5, a: 0 } }
];
