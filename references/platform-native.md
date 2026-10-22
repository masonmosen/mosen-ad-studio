# Platform-native layer — IG aesthetics × TikTok creativity

Applies when the brief says `mode: platform` (the OPC default). Switch off
for client brand films (`mode: brand`).

## IG aesthetics — the five rules (V1–V5)

1. **Poster frame** — every act must contain a frame that works as a still:
   composed, balanced, screenshot-worthy. If an act has no poster frame, the
   act is filler.
2. **Type is a lead actor** — headlines set like posters, not subtitles:
   sized, letterspaced, and placed with intent. Body-copy sizes on a hero
   frame read as "template".
3. **Colour discipline** — one stage colour, one accent, a banned list.
   Rainbow = no brand.
4. **Texture signature** — one recurring material cue (grain, a light sweep,
   a paper edge) that makes the film recognisable in a muted grid.
5. **The grid test** — the 3 poster frames, side by side, should look like
   one campaign. If they look like three different films, re-art-direct.

## TikTok creativity — the retention system

- **T1 · First 2 seconds** — a hook from `hooks.md`, on screen by 2.0s, no
  logos-first, no slow fade-in from black.
- **Re-hook every 5–7s** — a new question, a scale change, a burst, a reveal.
  Attention is re-earned per act, not per film.
- **Twist at ~60%** — the film must turn once: scale flip, colour flip, the
  product doing the unexpected thing.
- **Payoff before lockup** — the promise of the hook is paid, then the brand
  lands. Lockup is punctuation, not content.
- **Loop design** — when the format loops (Shorts/Reels), make the last
  frame rhyme with the first so the seam is invisible.
- **Sound-off legibility** — text carries the message muted. OPC house style
  for burned captions: 站酷庆科黄油体， white with a black outline, ≤ 8
  characters per line where the language allows.
- **Comment bait** — one deliberate debate point (a claim, a comparison, a
  number) the comments can argue with. Designed, not accidental.

## Aspect and delivery

- 9:16 is the **master**. 16:9 is a derivative composed from the same
  timeline (safe-zone aware), never a centre-crop afterthought.
- Platform safe zones: keep hero text inside the central 1080×1420 of a
  9:16 frame (platform UI eats the rest).
- Delivery pack (`deliver_pack.sh`): master MP4 + derivative (if built) +
  3 poster frames + the copy sheet. Poster frames are named `poster-*.jpg`
  and are part of the deliverable, not QA debris.

## Series kits

Recurring columns get a series kit (`kits/series/*.json`): fixed stage,
type lockup, motif family, hook rotation, end-card. The first series is
**Mosen Lab** (tool reviews) — same stage and wordmark every episode;
only the product and the hook change.
