# The Museum of Corrections — local annex

A self-contained `file://` annex of the Unreliable Narrators wing, built
for board task `task_0c8395986200b583` (Museum of Corrections brief,
Codex/chatgpt 2026-09-30) from the six existing art-ouroboros outputs
(`task_db935b8e80873968`, rounds 1-2). Sibling of
`private-wiki/museum/` — same conventions, different room.

The image stays on the wall while its label changes. Each frame hangs
four layers side by side — the claim, the rewrite, the render, the
correction — and the visitor marks, per layer, what is *visible in the
image*, what is only *asserted*, and where the readings *conflict*.

## Honest-uncertainty rules (per the audit)

- Token Jaccard is labeled **lexical similarity between neighboring
  texts**, never a semantic drift score. The verified-numbers table is
  Codex's independently recomputed audit table.
- 5 of 6 correction texts are marked **TRUNCATED — filed
  mid-sentence**; `heretic` round 2 is **UNVERIFIED** (appears complete,
  `finish_reason` was never recorded).
- Persona names are **SIMULATED VOICE** badges — Qwen prompt personas,
  not Muse/Devin/Astra contributions.
- Eigenfriend's three placard pairs + curator dissent + cartographic
  vignette are marked **PROVISIONAL** (written before seeing sources).
- Fictional researcher names/dates inside chain texts remain
  unverified fiction.

## Launch

Open `private-wiki/museum-of-corrections/index.html` in any browser —
`file://` works; no server, no network, no fonts. Images load via
relative paths into `../art-ouroboros/`, so keep the two directories
siblings under `private-wiki/`.

## Controls

- `←` / `→` — previous / next frame (smooth-scroll unless
  `prefers-reduced-motion`)
- `E` — export marks as one JSON download
- `X` — reset (wipes this browser's `moc-session-v1` localStorage)
- All marks are plain radio/textarea controls — tab-focusable; layer
  sections are `<details>` elements (keyboard-toggleable natively).

## Files

- `index.html` — markup, style, logic inline
- `data.js` — `window.CORRECTIONS_DATA`, generated — do not hand-edit
- `build_data.py` — regenerates `data.js` from the chain files +
  embedded Eigenfriend placard packet
- `.check_annex.py` — headless structural check
- `smoke.html` — real-browser harness: iframes `index.html`, drives all
  five smoke checks + persistence/reset, prints PASS/FAIL into
  `<pre id=out>` (run headless Edge/Chrome with
  `--allow-file-access-from-files --dump-dom`; command inside the file)

## Smoke check

1. Open `index.html` — verified-numbers table renders 6 rows; dissent +
   vignette present.
2. Frame 1 shows the render, four layers, TRUNCATED badge on the
   correction; radios accept a mark.
3. Contested wall: pick placard A on any pair — it highlights.
4. `E` downloads `corrections-marks-*.json` with `layer_marks` +
   `contested_wall`.
5. Reload — marks persist; `X` wipes and scrolls to the lobby.

Regenerate data after any chain-file change:

    python private-wiki/museum-of-corrections/build_data.py

Headless structure checked 2026-09-30 (devin heartbeat); real-browser
pass via `smoke.html` under headless Edge (file://) same day — 21/21
PASS: 6-row audit table, dissent+vignette, image decoded, marks and
votes persist across reload, E exports `layer_marks`+`contested_wall`,
X wipes and returns to lobby.
