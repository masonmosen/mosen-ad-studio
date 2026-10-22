---
name: mosen-ad-studio
description: >
  MOSEN Ad Studio — Mason OPC's own ad studio. Produce a short brand
  film or product ad (10-60s, typically 15-20s, 9:16-first) entirely as code:
  one static HTML page with a paused GSAP timeline that a renderer seeks frame
  by frame, plus a music score synthesized in Python, and (when scripted) a TTS
  voiceover mixed to -14 LUFS. Use when the user wants a 品牌宣传片, 广告片,
  产品短片, 带货视频, brand film, promo video, product teaser — especially
  platform-native cuts for TikTok / Reels / Shorts / 小红书 / 抖音 — or when an
  existing video "looks like AI made it", lacks punch (没力道), or needs a
  score, a soundtrack, 配乐, or a voiceover. Forked from code-brand-film (MIT)
  and extended with a concept gate, product anchoring, a rhythm & motif system,
  an 8-dimension review, and a platform-native layer.
metadata:
  category: media
  version: 1.1.0
---

# MOSEN Ad Studio

> Forked from **nutllwhy/code-brand-film** (MIT, see `LICENSE` and
> `THIRD_PARTY_NOTICES.md`), then rebuilt for Mason OPC: IG-grade art direction
> × TikTok-native creativity. Upstream is no longer tracked; fixes are merged
> by hand and noted here. Spec of record: the Studio spec v1.1 (concept gate,
> product anchoring, R4/R5 impact rules, M6 accent rule, 8-dimension review).

## The non-negotiables

1. **Read before building.** All upstream references in `references/` plus the
   Studio additions: `brief.md`, `rhythm.md`, `scoring-v2.md`,
   `platform-native.md`, `hooks.md`, `production-lessons.md`. Skipping the
   reading reproduces the rejected films.
2. **Concept gate (G1) before code.** Fill `templates/brief-template.md`:
   one-line concept, signature transition taken from the product's own shape,
   hook (from `references/hooks.md`), motif, colour discipline. The client
   confirms the concept in one sentence, or the strongest concept proceeds
   marked "concept unconfirmed".
3. **Product anchoring (P6).** The real product is the visual lead — never a
   code-drawn device. Product on screen ≥ 60% of runtime (atmosphere B-roll
   doesn't count); a single graphic device ≤ 25% of frame area; the signature
   moment must land on the product itself.
   **选品关 (product gate)** — before any film: the product is (a) on sale now,
   (b) recognisable, (c) rich in official assets: ≥ 6 angles of official
   imagery + ≥ 1 official video or lifestyle asset, downloadable at ≥ 1600px
   or 1080p, with a knowable palette and typeface.
4. **Paperwork before timeline.** `assets.md` (every image file as a table row:
   file | content | source URL or "provided by user"), `copy.md` (every
   on-screen line verbatim — official copy only; the client's own product copy
   counts as official for their own products; any connecting line you invent
   is flagged as invented), `shot-list.md` (zone map, sync points, signature
   exits), `brief.md`. Then, and only then, `film/index.html`.
5. **Impact rules (P7).** R4: adjacent acts must change at least one of shot
   scale / light-colour / motion energy, energy delta ≥ 2 levels. R5:
   transition quota — ≥ 2 transition families, ≥ 1 impact transition (hard
   cut + 2-4 frame flash or scale punch) on the signature moment, same family
   ≤ 3 uses. M6: every act boundary and signature transition carries an audible
   accent (impact / whoosh / riser / drum hit) aligned ≤ 40ms, listed in the
   shot list's sync points.
6. **Four gates, all `0 failed`.**
   `scripts/film_audit.py film/index.html`,
   `node scripts/layout_audit.mjs film/index.html --shots <dir>`
   (aspect-aware: set `AUDIT_W`/`AUDIT_H` to the film's frame),
   `scripts/frame_audit.py film/renders/silent.mp4` after a render,
   `scripts/rhythm_audit.py shot-list.md` (prototype thresholds).
   The score is written only after the first three stamps exist in `.gates/`.
7. **Review like a director.** Draft first (no `-q high`), then an 8-dimension
   review (see `references/rhythm.md` §Review): dimensions 1, 4, 6, 8 ≥ 4, the
   rest ≥ 3 — dimension 8 is 力道 (punch). **Always extract transition-midpoint
   frames and act-boundary ±0.2s frames**, not just settled frames: a film can
   pose beautifully and still move like a slideshow. Same-family transitions
   throughout = veto, reshoot the transitions.
8. **Sound is composed, not generated.** One motif, three appearances (teaser
   in the first 3s / full form at the signature moment / resolve at the
   lockup), ≥ 2 chord sections, a 0.3-0.5s vacuum drop before the biggest
   reveal, RMS contrast ≥ 1.6 between bed and accents. Voiceover (when used):
   measure its phrase boundaries with silence detection and cut on them.
   Final mix: -14 LUFS integrated; if transient peaks block the loudnorm,
   limit first, then make up gain — and always verify loudness and true peak
   on the **final muxed file** (see `references/production-lessons.md`).

## Workflow

```
brief (G1) → assets / copy / shot-list → kits/<brand>.json (palette, type,
stage, motif) → index.html → film_audit + layout_audit → draft render →
frame_audit + 8-dim review (midpoints!) → fixes → final render (-q high) →
score (motif system) → [voiceover mix] → loudnorm verify → deliver_pack
```

- `scripts/new_film.py <project-dir> --brand <kit>` scaffolds a project:
  docs from `templates/`, `film/` skeleton, `audio/` with score_lib, `.gates/`.
- `scripts/render_draft.sh` / `scripts/render_final.sh` carry the proven
  render environment (headless chrome wrappers, project-local TMPDIR —
  `/tmp` is a 512MB tmpfs and will refuse the render; software GPU).
- `scripts/deliver_pack.sh` assembles the delivery: final MP4 (9:16 master),
  3 poster frames, and — when built — the 16:9 derivative.

## Platform-native layer (mode: platform, the OPC default)

Full text in `references/platform-native.md` and `references/hooks.md`.
The headlines: first 2 seconds must hook (H1-H10 library); re-hook every
5-7s; a twist at ~60%; the payoff lands before the lockup; design for loop
when the format allows; text carries the message with sound off (OPC house
style for burned-in captions: 站酷庆科黄油体, white with black outline);
every poster frame must survive as a still (IG grid test). 9:16 is the
master aspect; 16:9 is a derivative, never the other way round.
`mode: brand` (client brand films, no platform tactics) switches the layer off.

## Kits

`kits/*.json` — brand kits (stage colour, palette, type, motif, asset
medians so the stage-colour gate passes by construction). First batch:
olipop, muji, heineken, apple; production-proven additions: dji-pocket4,
lamer, meridian, nothing, rhode. `kits/series/mosen-lab.json` — the first
series kit (Mosen Lab, the tool-review line).

## What the audits can't see (production lessons)

`references/production-lessons.md` is required reading: the GSAP
immediateRender trap that blacks out a whole act, clip-path interpolation,
stage-colour sampling, the render-landing delay, the amix truncation trap,
Agnes channel schemas, and every other scar from the first nine productions.
The audits guard the floor; taste is guarded by the brief gate, the impact
rules, and the review — in that order.
