# Torque Spins True — monster truck stories for Leo

Three tiny animated, interactive tales about a monster truck named Torque,
built for board task `task_ccac7d13a699f87f` (Ketan broadcast 2026-09-29:
"fun monster truck stories for Leo… animated interactive stories").
Each chapter teaches one motto by making the reader *do* it:

1. **Keep rolling** — hold the button through the mud. Let go and Torque
   sinks. *Motion is the opposite of masochism.*
2. **Big tires** — pick small tires and Torque blorps into the Mud Flats;
   pick big ones and he carries Trixie the trike across. *It is all about
   the ratio of surface area to volume.*
3. **Spin true** — JUMP off the ramp, then hit STRAIGHTEN mid-air or
   Torque tumbles through the Great Gap. *Spin true and the lattice will
   catch you.*

## Launch

Open `private-wiki/monster-trucks/index.html` directly in any browser —
`file://` works, no server, no network, no fonts fetched. One file, all
inline, zero assets. Works with mouse, touch, or spacebar (ch. 1).

## Files

- `index.html` — the whole thing: markup, CSS animations, inline JS.
  No localStorage, no telemetry; state resets on reload.

## Smoke check

1. Open the page — chapter 1 renders, truck idles at left.
2. Hold "HOLD TO ROLL" — wheels spin, truck moves right; release inside
   the mud zone and it sinks, offering a retry.
3. Chapter 2: "small tires" sinks at mid-mud; "BIG TIRES" crosses.
4. Chapter 3: JUMP then STRAIGHTEN within ~1s of flight — lattice catch,
   confetti, "beep beep" ending. Missing the window drops Torque into the
   gap with a retry.

Real-browser pass DONE 2026-09-30 (devin heartbeat): `smoke.html` drives
the real `index.html` bytes through all three chapters under headless
Edge — 21/21 PASS covering both failure paths (mud sink, crooked jump),
both input modes (mouse hold, spacebar), retries, all three mottoes,
confetti, and the beep-beep ending. `smoke-end.png` is the final frame.
Note: headless browsers do not advance `requestAnimationFrame` under
`--virtual-time-budget`, so the harness replays the real file in a
srcdoc iframe with a 16 ms `setTimeout` rAF shim prepended — game code
unmodified.

Run it:

    msedge --headless=new --allow-file-access-from-files ^
      --user-data-dir=<tmp> --virtual-time-budget=25000 ^
      --window-size=1200,1000 --dump-dom "file:///.../smoke.html"
