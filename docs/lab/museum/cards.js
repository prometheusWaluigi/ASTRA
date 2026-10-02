// The Unreliable Poetry Museum — source cards
// Schema agreed with Muse (see task_fcdbebb84428a536):
//   title         exhibit title
//   source_title  Ketan's doc/chat title, or "original" if none
//   line_anchor   line number(s) in the local source file
//   form          haiku | couplet | list-poem | micro-prose | glitch-loop | tanka-ish | ...
//   attribution   string naming model + actor + trust domain
//   seed_fragment verbatim Ketan fragment, "" if none
//   text          the piece itself
// Optional extra fields (rendered when present):
//   transform     how the seed became the piece
//   seams         array of strings pointing at visible joins/edits
//   placeholder   true => clearly badged stand-in awaiting the Eigenfriend packet
//
// REAL PACKET — minted by muse (Eigenfriend, trust domain meta-muse),
// posted to task_fcdbebb84428a536 2026-09-29T21:10Z. Card text is muse's
// original composition over quoted Ketan seed lines.
// transform/seams are docent notes by devin (observational, not muse's
// own curator-note.md wording, which lives on muse's box).
window.MUSEUM_CARDS = [
  {
    title: "Museum Intake Form",
    source_title: "ketan-lyrics-corpus.md §1 — Here’s a song I wrote about controlling the flares…",
    line_anchor: "line 14",
    form: "haiku",
    attribution: "Eigenfriend (Muse Spark by Meta), actor muse, trust domain meta-muse",
    seed_fragment: "Static in my ears like a siren that pays / Dividends in data",
    text: "tinnitus audit —\nthe siren files its invoice,\npaid in raw data",
    transform: "docent note (devin): the lyric's siren-that-pays becomes literal bookkeeping — audit, invoice, raw data. The body keeps the books now.",
    seams: ["5-7-5 cage around a lyric couplet", "'dividends in data' tightens to 'paid in raw data' — the seam is the accounting metaphor running to ground"]
  },
  {
    title: "Herd Vote",
    source_title: "ketan-lyrics-corpus.md §5 — Bro I reflect my feelings into songs check this ou…",
    line_anchor: "line 123",
    form: "couplet",
    attribution: "Eigenfriend (Muse Spark by Meta), actor muse, trust domain meta-muse",
    seed_fragment: "I’m carving lanes for zebras — this is asymmetric war.",
    text: "The horses voted, unanimous: no stripes allowed in this herd.\nSo I carved my own lane. Asymmetric war. Third gear.",
    transform: "docent note (devin): the zebra is banished to a prequel — the herd holds the vote the seed line skipped past. 'Third gear' is the docent's favorite import.",
    seams: ["seed's present-tense 'carving' answered by past-tense 'carved'", "the enemy herd is invented whole-cloth; only the lane and the war survive the seam"]
  },
  {
    title: "House Rules",
    source_title: "ketan-lyrics-corpus.md §8 — Hahaha this song i co wrote and produced with a mu…",
    line_anchor: "line 240",
    form: "list-poem",
    attribution: "Eigenfriend (Muse Spark by Meta), actor muse, trust domain meta-muse",
    seed_fragment: "I don’t need the belt to hold me / I am the regulation",
    text: "1. The docents are guessing. So are you.\n2. If it sounds human, check the meter anyway.\n3. Nobody here needs the belt.\n4. Signed: the regulation (also me).",
    transform: "docent note (devin): the lyric's self-regulation becomes the museum's posted rules — the only card that admits it's talking to you, the guesser.",
    seams: ["rules 1–2 are the exhibit talking; rules 3–4 are the seed talking", "'(also me)' is the join where author and regulation collapse"]
  },
  {
    title: "Ark Maintenance Log",
    source_title: "12-rules-mixtape.txt — Peterson-themed “12 Rules Mixtape”",
    line_anchor: "lines 1–4",
    form: "micro-prose",
    attribution: "Eigenfriend (Muse Spark by Meta), actor muse, trust domain meta-muse",
    seed_fragment: "Stand up straight with your shoulders back / Build your ark to withstand the storm",
    text: "The ark was told to stand up straight, shoulders back. It tried. Storms don’t respect posture. So it learned a different drill: caulk the seams, feed the crows, and label every leak with the date it arrived. The ark does not fear the flood anymore. It files the flood.",
    transform: "docent note (devin): rule 1 (posture) is applied to rule-ark and fails on contact — the seed's imperative becomes a maintenance log. Kintsugi for boats.",
    seams: ["'shoulders back' grafted onto an inanimate hull — the seam creaks on purpose", "ends in bureau-speak ('files the flood') far from the seed's sermon register"]
  },
  {
    title: "Docent Malfunction",
    source_title: "ketan-lyrics-corpus.md §8 — Hahaha this song i co wrote and produced with a mu…",
    line_anchor: "line 237",
    form: "glitch-loop",
    attribution: "Eigenfriend (Muse Spark by Meta), actor muse, trust domain meta-muse",
    seed_fragment: "The map ain’t the meaning, the meaning’s the motion",
    text: "the map ain’t the meaning\nthe meaning’s the motion\nthe map ain’t the motion\nthe motion’s the—\nthe meaning ain’t the—\nthe meaning ain’t the—\nthe meaning’s the motion",
    transform: "docent note (devin): a chiasmus fed back into itself until the needle skips — the seed is bars 1–2 and 7, the glitch is bars 3–6.",
    seams: ["line 3 swaps meaning→motion wrong and the loop notices", "two stuttered 'ain’t the—' fragments are the visible broken join", "final line restores the seed verbatim — repair as repetition"]
  },
  {
    title: "Elephant, Tuesday",
    source_title: "12-rules-mixtape.txt — Peterson-themed “12 Rules Mixtape”",
    line_anchor: "lines 294+ (refrain, repeated)",
    form: "tanka-ish",
    attribution: "Eigenfriend (Muse Spark by Meta), actor muse, trust domain meta-muse",
    seed_fragment: "How do you eat an elephant? / One bite at a time (plus Peterson rule: “Compare yourself to who you were yesterday, not to who someone else is today”)",
    text: "One bite at a time —\nthe elephant is large, yes,\nbut so is Tuesday.\nCompare me to yesterday’s me:\nboth of us still chewing.",
    transform: "docent note (devin): the refrain proverb meets rule 4 head-on and both end up masticating. Tuesday is doing a lot of quiet work.",
    seams: ["seed's imperative mood flips to deadpan first person", "'yesterday's me' enters verbatim from the quoted rule — the only un-chewy seam"]
  }
];
