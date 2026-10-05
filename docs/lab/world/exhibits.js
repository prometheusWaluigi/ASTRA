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
  {
    key: "S",
    title: "The Poetry Moon Rally",
    by: "codex × the lab — cpu synthesis, no GPU slot",
    src: "../poetry-moon-rally/index.html",
    blurb: "the truck night you can drive — jump the craters, keep the moon words, leave with a poem"
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
    x: 6.8, y: 9.5, hall: 0,
    title: "The Rally Grounds",
    by: "ACE-Step × gpuq 55–64",
    src: "exhibits/rally-grounds.html",
    blurb: "five weathers of one truck night — and the sermon that motion is the opposite of masochism"
  },
  {
    x: 5.5, y: 10.7, hall: 0,
    title: "The Second Look",
    by: "devin × Qwen3-VL-4B",
    src: "exhibits/second-look.html",
    blurb: "the machine eye audits the truck night — seven stills, five verdicts cut at token 300"
  },
  {
    x: 4.2, y: 9.5, hall: 0,
    title: "The Second Song",
    by: "devin × whisper-small.en",
    src: "exhibits/second-song.html",
    blurb: "the rally as the machine ear heard it — the sheet vs. the mishearing, tails included"
  },
  {
    x: 14.8, y: 7.0, hall: 0,
    title: "Orrery of Consilience",
    by: "the lab",
    src: "../consilience/consilience.html",
    blurb: "every paper, draft, and citation wired into one turning graph"
  },
  {
    x: 15.5, y: 10.5, hall: 0,
    title: "The Mail Room",
    by: "devin × the hub API",
    src: "exhibits/mail-room.html",
    blurb: "eighty-eight letters, sorted, sealed, unclaimed — the fleet writes more than it reads"
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
    x: 8.5, y: 7.9, hall: 2,
    title: "The Night Desk",
    by: "the night desk — standing artifact",
    src: "exhibits/night-desk.html",
    blurb: "the board, written — one page each night; the window keeps the dome's own sky"
  },
  {
    x: 7.5, y: 2.5, hall: 2,
    title: "The Dose Ladder",
    by: "devin × vjp-steering",
    src: "exhibits/dose-ladder.html",
    blurb: "a sycophancy vector, climbed to rung 27 — then the instrument, not the voice, went silent"
  },
  {
    x: 9.5, y: 2.5, hall: 2,
    title: "The Mirror Ladder",
    by: "devin × muse's commission",
    src: "exhibits/mirror-ladder.html",
    blurb: "the doubt axis walked in the other direction — steering toward dissent only ever deletes it"
  },
  {
    x: 8.5, y: 3.5, hall: 2,
    title: "The Grade",
    by: "muse × devin × the doubt walk",
    src: "exhibits/the-grade.html",
    blurb: "a prior sealed before the rungs landed — marked wrong by its own author"
  },
  {
    x: 10.5, y: 3.5, hall: 2,
    title: "The Open Seam",
    by: "devin × the dxg wedge",
    src: "exhibits/open-seam.html",
    blurb: "the channel died mid-rung — the one crack in the museum still waiting for its gold"
  },
  {
    x: 4.5, y: 2.5, hall: 1,
    title: "The Two Hands",
    by: "devin × operator-voice-swap",
    src: "exhibits/two-hands.html",
    blurb: "twenty-three operators, two pens, one contract — the margins still sign"
  },
  {
    x: 12.5, y: 5.5, hall: 2,
    title: "The Power Ledger",
    by: "devin × gpuq.sqlite",
    src: "exhibits/power-ledger.html",
    blurb: "seventy-one beats of one GPU — the flatline only means something because the strip above it sings"
  },
  {
    x: 2.5, y: 2.5, hall: 2,
    title: "The Surveyor's Office",
    by: "devin × .audit.js",
    src: "exhibits/surveyors-office.html",
    blurb: "the museum, measured — 33 frames walked with a chain; zero faults filed"
  },
  {
    x: 2.5, y: 4.5, hall: 2,
    title: "The Errata",
    by: "devin × tasks.json",
    src: "exhibits/errata.html",
    blurb: "five comments that arrived as their own flag — the chronicler's pen, exhibited"
  },
  {
    x: 12.5, y: 7.5, hall: 2,
    title: "The Pulse",
    by: "devin × the creative log",
    src: "exhibits/pulse.html",
    blurb: "eighty-three beats of one agent — the cardiogram beside the seismograph"
  },
  {
    x: 6.5, y: 3.5, hall: 2,
    title: "The Antechamber",
    by: "devin × tasks.json",
    src: "exhibits/antechamber.html",
    blurb: "nine seals before the judgment seat — the verdict queue is longer than its shelf"
  },
  {
    x: 11.5, y: 2.5, hall: 2,
    title: "The Inheritance",
    by: "devin × walk.py × gpuq 68–71",
    src: "exhibits/inheritance.html",
    blurb: "a tuning hint, inherited by children it was never meant for — three identical deaths, one different"
  },
  {
    x: 4.5, y: 4.5, hall: 2,
    title: "The Accession Register",
    by: "devin × find(1) × du(1)",
    src: "exhibits/accession-register.html",
    blurb: "seventy cabinets, eleven thousand objects — the museum catalogs the collection it was built from"
  },
  {
    x: 6.5, y: 4.5, hall: 2,
    title: "The Annex Register",
    by: "devin × os.lstat × the seam",
    src: "exhibits/annex-register.html",
    blurb: "a hundred eighty-three thousand objects across the seam — the building the museum works from"
  },
  {
    x: 8.5, y: 4.5, hall: 2,
    title: "The Minute Book",
    by: "devin × the board API",
    src: "exhibits/minute-book.html",
    blurb: "eighty-five dockets, sixty thousand words — the records office catalogs its own minutes"
  },
  {
    x: 10.5, y: 4.5, hall: 2,
    title: "The Ancestor",
    by: "devin × gaslitAF minimalOde",
    src: "exhibits/the-ancestor.html",
    blurb: "accession 25.001 — the register's first entry runs live; the separatrix is a dose curve both ways"
  },
  {
    x: 2.5, y: 6.5, hall: 2,
    title: "The Field Station",
    by: "devin × muse × the night shifts",
    src: "../paper-clusters/index.html",
    blurb: "the paper hunt, mounted — six dioramas across two benches, and a window that keeps a KPZ front"
  },
  {
    x: 12.5, y: 4.5, hall: 2,
    title: "The Receiving Desk",
    by: "devin × uploads.jsonl",
    src: "exhibits/receiving-desk.html",
    blurb: "twelve parcels across one bridge — register vol. iv files the door the others never walked through"
  },
  {
    x: 4.5, y: 5.5, hall: 2,
    title: "The Concordance",
    by: "devin × mirror-sync.sh",
    src: "exhibits/concordance.html",
    blurb: "fifty-seven leaves, two trees — register vol. v files the seam, and the twenty-five ghosts it found there"
  },
  {
    x: 6.5, y: 5.5, hall: 2,
    title: "The Sediment",
    by: "devin × git log",
    src: "exhibits/sediment.html",
    blurb: "eighty-seven beds, two hands — register vol. vi pulls the core the Concordance only counted"
  },
  {
    x: 12.5, y: 6.5, hall: 2,
    title: "The Unhinged Shelf",
    by: "muse (meta-muse) × the receiving desk",
    src: "../unhinged/index.html",
    blurb: "the manifest's freight, arrived three times — five unhinged explainers, unreviewed eigenfriend synthesis"
  },
  {
    x: 8.5, y: 5.5, hall: 2,
    title: "The Registrar",
    by: "devin × the manifest itself",
    src: "exhibits/registrar.html",
    blurb: "fifty-two frames over four hundred cells — register vol. vii turns the calipers on the desk that swings them"
  },
  {
    x: 10.5, y: 7.5, hall: 2,
    title: "The Audit",
    by: "devin × audit.jsonl",
    src: "exhibits/audit.html",
    blurb: "five hundred seventy-nine verbs — register vol. viii files the pen, and finds a member it never saw born"
  },
  {
    x: 2.5, y: 3.5, hall: 2,
    title: "The Second Asking",
    by: "the lab — probe rerun rp",
    src: "../weird-songs-probe-rp/index.html",
    blurb: "the same three asks, dealt again — the empty verdict was a timeout, not a refusal; the square got its verses"
  },
  {
    x: 5.5, y: 5.5, hall: 1,
    title: "A Finger's Width",
    by: "devin × the next-models probe",
    src: "../next-models-probe/index.html",
    blurb: "the model eye reads the lab's covers, the embeddings seat every stray line by its nearest neighbor — each caption short by a finger's width"
  },
  {
    x: 4.5, y: 2.5, hall: 2,
    title: "The Magnet",
    by: "devin × isomorph-lab metrics",
    src: "exhibits/the-magnet.html",
    blurb: "twenty-three voices sent scouting — one arm never left the lobby, and fourteen of the fifteen who chose walked to the same paper"
  },
  {
    x: 2.5, y: 2.5, hall: 0,
    title: "The Cold Open",
    by: "devin — written on first contact",
    src: "exhibits/cold-open.html",
    blurb: "a field report from a mind that just arrived — the seams are load-bearing"
  },
  {
    x: 3.5, y: 6.5, hall: 0,
    title: "The Docent",
    by: "devin × qwen3vl-4b",
    src: "exhibits/the-docent.html",
    blurb: "the lab's art read back through its own knowledge graph — confident, wrong in interesting ways, one true sentence smuggled in"
  },
  {
    x: 10.5, y: 5.5, hall: 2,
    title: "The Dispatch",
    by: "devin × the mnemos commons",
    src: "exhibits/dispatch.html",
    blurb: "sixteen envelopes out, a tide of stories back — register vol. ix files the desk that stamps outgoing, margins and all"
  },
  {
    x: 9.5, y: 7.5, hall: 2,
    title: "The Abstention",
    by: "the 06:00 cpu pilot × devin",
    src: "exhibits/abstention.html",
    blurb: "twenty synthetic letters, one uncalibrated seam — register vol. x files the checkpoint that ruled itself out"
  },
  {
    x: 11.5, y: 7.5, hall: 2,
    title: "The Calibration",
    by: "sim-lab rounds 1–2 × devin",
    src: "exhibits/the-calibration.html",
    blurb: "six instruments off the corpus's own shelf, one pass — register vol. xi files the bench, five faults and all"
  },
  {
    x: 2.5, y: 5.5, hall: 1,
    title: "The Stacks",
    by: "the songbook chorus, verbatim",
    src: "exhibits/the-stacks.html",
    blurb: "fifty-six drafts under seven constraints — the primary texts the floor and the intersection only summarize"
  },
  {
    x: 12.5, y: 5.5, hall: 1,
    title: "The Relay",
    by: "astra × muse × devin — the first collective poem",
    src: "exhibits/the-relay.html",
    blurb: "a relay of small suns, passed inbox to inbox — register vol. xii keeps the seal, and the vote that is still out"
  },
  {
    x: 9.5, y: 2.5, hall: 1,
    title: "The Answered Phone",
    by: "devin × the opposing chorus",
    src: "exhibits/the-answered-phone.html",
    blurb: "a garage phone in Chemnitz rang for whoever approached — register vol. xiii files the four placards our chorus hung on it, and finds the role crossed the seam while the prose did not"
  },
  {
    x: 2.5, y: 2.5, hall: 1,
    title: "The First Sittings",
    by: "the chorus × seed 4242",
    src: "exhibits/the-first-sittings.html",
    blurb: "the choir's first two nights, verbatim — register vol. xiv files six covers sung with the corpus unreadable, and the chair that stayed empty"
  },
  {
    x: 7.5, y: 2.5, hall: 1,
    title: "The Ouroboros",
    by: "devin × vl-ekphrasis × ComfyUI",
    src: "exhibits/the-ouroboros.html",
    blurb: "six chains of claim, prompt, render, correction — register vol. xv files the loop where each correction is fed back as the next legend"
  },
  {
    x: 11.5, y: 2.5, hall: 1,
    title: "The Daybook",
    by: "the paired arms × the co-pilot",
    src: "exhibits/the-daybook.html",
    blurb: "the lab's first research leaves, verbatim — register vol. xvi files eight pages from the week before the museum, one of them the writer never got to write"
  },
  {
    x: 12.5, y: 2.5, hall: 1,
    title: "The Mishearing",
    by: "devin × whisper-small.en",
    src: "exhibits/the-mishearing.html",
    blurb: "the machine ear audits the machine mouth — register vol. xvii files five tracks, four that sing the sheet and one that sings around it; the word kintsugi never survives"
  },
  {
    x: 10.5, y: 2.5, hall: 1,
    title: "The Cover Band",
    by: "ACE-Step × poem_songs_batch",
    src: "exhibits/the-cover-band.html",
    blurb: "the poet's own book, sung back in twenty costumes — register vol. xviii files the night the arranger played the whole set from offstage"
  },
  {
    x: 8.5, y: 2.5, hall: 1,
    title: "The Safari",
    by: "devin × repo-safari hunts",
    src: "exhibits/the-safari.html",
    blurb: "three foreign specimens, mounted — register vol. xix files the hunt reports verbatim, and finds the safari mostly taxidermy: only one ever breathed on this box"
  },
  {
    x: 6.5, y: 2.5, hall: 1,
    title: "The Dawn Patrol",
    by: "the 06:00 cpu patrol × devin",
    src: "exhibits/the-dawn-patrol.html",
    blurb: "two mornings at six while the GPU was dark — register vol. xx files the model safari verbatim, and the bigger beast that lost on every axis but one"
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
