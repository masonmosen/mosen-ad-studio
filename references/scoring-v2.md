# Scoring v2 — the motif system

The upstream scoring workflow (`scoring.md`, `score_lib.py`,
`score_template.py`) still applies. v2 adds composition rules so the music
is *about the product*, not a groove generator keeping time.

## M1 · One motif, three appearances

Design a motif of 2–4 notes or one unmistakable texture (a droplet's
chirp-down, a lock's three blips, a metal click cell). Schedule it:

1. **Teaser** — inside the first 3 seconds, partial or quiet
2. **Full form** — at the signature moment, complete and loudest
3. **Resolve** — at the lockup, settled (often lower, warmer, with a tail)

If a listener can't hum the film afterwards, there was no motif.

## M2 · Signature sound from the product

Derive the motif from the product's own behaviour: a stabiliser's lock beep,
a cream's droplet, a tool's detent click. Stock "whoosh packs" are banned
as the motif (they may still serve as utility accents).

## M3 · Chord sections

≥ 2 distinct chord sections across the film (e.g. bed in Am, signature in
F). One loop from 0:00 to the end is a demo, not a score.

## M4 · The vacuum drop

Before the biggest reveal, pull the bed out for 0.3–0.5s. Silence is the
loudest accent you own. Place the drop in the shot list's sync points so
picture and sound agree on the frame.

## M5 · Contrast

RMS of the loudest 3 seconds ≥ 1.6 × RMS of the quietest 3 seconds. A flat
mix at a constant level reads as "background music" no matter how good the
notes are.

## M6 · Accent every boundary

Every act boundary and signature transition carries one audible accent —
impact, thud, click, riser, whoosh, or a motif hit — aligned to the picture
cut within 40ms. List them in the shot list's sync points; if a boundary
has no accent, it isn't a boundary yet.

## Voiceover films

- Record/generate the VO **first**; measure phrase boundaries with silence
  detection (`ffmpeg -af silencedetect`) and cut picture on the phrases.
- The bed ducks by arrangement, not by hope: sparser texture and lower gain
  under speech, hits only in the gaps and on the cuts.
- Loudness: normalise components separately, mix, then verify the final
  muxed file. Transient motifs (clicks) sit ~25 dB above the integrated
  level — limit them before the loudnorm or the loudnorm will refuse to
  raise the mix (see `production-lessons.md`).
