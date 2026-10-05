# Poetry Moon Rally

Open `index.html` in a browser. Jump with Space, the up arrow, a tap on the scene, or the Jump button. Collect eight words by jumping the craters; your finish screen assembles your poem. R or Start again resets. Audio is optional and starts from its own player.

This is an original artistic response to the lab's Torque monster-truck stories and poetry/music experiments. The moon imagery and poem are newly authored for this batch. There are no external assets or network requests. The instrumental is deterministic CPU synthesis, not an AI model sample or a vocal song. The 24-second video is a separate procedural animation, not a recording of game play. No GPU slot was used.

`experiments/poetry_moon_rally.py` regenerates the mono WAV, H.264/AAC MP4, preview still, and output hashes using Python's standard library and ffmpeg. Seed 1002, 24 seconds, 480×270 at 12 FPS; see `provenance.json`.

Verification: `node verify.cjs` exercises the actual game logic, including all crater misses, reset, all eight successful collections and both finish paths. ffprobe confirms the 24-second video and audio streams. The preview still was visually inspected. Browser visual smoke check is separately recorded in `browser-smoke.txt` when available.

A separate ACE-Step song request is queued at `private-wiki/song-lab/torque-poetry-moon-20261002`. The CPU-only user service `poetry-moon-followon-20261002.service` waits at most 25 minutes for that result, verifies its WAV hash, renders `torque-poetry-moon.mp4`, decodes it fully, copies the WAV and adds a video link here. It exits on song error or deadline; systemd caps the service at 30 minutes. Inspect `followon-status.json` and `torque-poetry-moon-provenance.json` for outcome. The animation accompanies the song without claiming lyric or beat alignment. Listening review is still required.
