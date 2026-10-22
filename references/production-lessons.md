# Production lessons — scars from the first nine productions

Read before every build. Each entry cost at least one render.

## Page structure & GSAP

- **The root wrapper is load-bearing.** The page needs
  `<div id="root" data-composition-id data-start="0" data-duration
  data-width data-height>` around everything; scenes themselves carry no
  `data-start/duration`. Without the wrapper the renderer's seek window
  computes to ≤ 0 and video elements silently render zero frames.
- **Register the timeline twice**: `window.__timelines["main"]` *and*
  `window.__timelines["<composition-id>"]`. Only "main" renders — with a
  45s sub-timeline timeout warning and a much slower capture.
- **immediateRender poisons second appearances.** A `fromTo` for an
  element's *second* entrance writes its FROM values (e.g. `opacity: 0`)
  onto the element at timeline build time, killing its *first* entrance —
  whole acts render black. Fix: give the first entrance explicit opacity on
  both ends, or add `immediateRender: false` to the second `fromTo`.
  Review must include mid-act frames; settled frames won't show it.
- Same trap, smaller: a container with CSS `opacity: 0` whose children are
  the only things tweened stays invisible forever. Put the initial state on
  the elements that actually tween.
- **No `repeat: -1` on the master timeline** (duration becomes infinite and
  the layout audit never finishes). Loops are finite or single-pass; yoyo
  tweens ≤ 3 per film.
- **clip-path**: CSS `polygon()` takes commas *between* points and spaces
  *inside* them. GSAP does not interpolate clip-path strings under seek —
  animate an object (`{r: 0}` + `onUpdate` writing `el.style.clipPath`
  yourself), the same pattern as number count-ups.
- A five-pointed star that must cover 1920×1080 needs R ≥ ~3150 (the
  chord's closest approach is ~0.35R). Use 3400. Scale the math per frame.

## Audits — how they actually judge

- film_audit thresholds scale with duration (k = duration/15). Tweens are
  counted by regex over `tl.(to|from|fromTo|set)`; literal-bound `for` loops
  and literal-array `forEach` are expanded by the counter — write per-letter
  and per-item animations that way. Camera moves count only tweens on
  `#cam<digit>` selectors, and camera *layers* are elements with class
  `cam`. Timed-event buckets scale with k too — late-film tweens need
  literal end times or the last bucket starves.
- The film_audit copy check compares normalised text: an HTML `&amp;`
  survives as the letters "amp". Use a raw `&` in on-screen text.
- assets.md sources are read from **table rows** — every image gets a
  `| file | content | source |` row, or it counts as unsourced.
- Stage colour: each image's border ring is sampled; if ≥ 60% is one flat
  colour, that colour must appear as a `background:` declaration inside a
  `<style>` block (inline styles don't count). Transparent product shots:
  flood the transparent pixels' RGB to the stage colour, keep alpha.
- IDs containing ring/focus/capture/bracket/cursor, or classes with
  "corner", trip the HUD/furniture detector. Name ripple elements `rip`,
  not `ring`.
- layout_audit measures the *metrics box*, larger than the glyphs: leave
  ≥ 35px between stacked text lines, and remember a camera scale `s` moves
  the left edge to `centre + (x − centre) × s` — check the 48px safe area
  at the *maximum* scale the act reaches, not the settled one.
- frame_audit's motion floor (median ≥ 0.025 of pixels changing per 0.1s)
  fails quiet luxury films: every act needs a *continuous* move — a slow
  full-frame push of 3–6%/s on a textured image, or a drifting depth layer.
  Entry animations alone don't carry the median.

## Rendering

- Proven recipe in `scripts/render_final.sh`: background process (detached
  `nohup`/`setsid` launches get reaped by the runtime), project-local
  TMPDIR (`/tmp` is a 512MB tmpfs), browser GPU in software mode.
- The finished file lands 1–2 minutes *after* the completion notice.
  `ffprobe` before concluding anything; `renders/work-*/video-only.mp4`
  without a moov atom is an intermediate, not a deliverable.
- Never pass `-o <name>` to the renderer — a leftover transaction marker
  once ate a finished render. Take the timestamped default name and copy
  it to `silent.mp4` yourself.
- Official videos with sparse keyframes (> 2.5s apart) freeze under seek.
  Re-encode every incoming video first: `-g 30 -keyint_min 30 +faststart`.

## Sound & mix

- `score_lib.pad()` takes **note-name strings** (`['D3','F3']`) — it calls
  `hz()` internally. Passing pre-computed floats raises TypeError. `sub()`
  and `bell()` take frequencies.
- Never chain `score.py && render` in one command — a score crash then
  silently cancels the render. Run paid/long steps separately, verify each.
- `ffmpeg amix duration=first` truncates to the **first** input. Put the
  longest track first (the 20s bed, not the 17.9s VO) — or the film loses
  its tail (a 20s film shipped at 18.3s once).
- Transient motifs (clicks, ticks) peak ~25 dB above the integrated level;
  two-pass linear loudnorm then refuses gain and the mix lands ~1.5 LU
  quiet. Limit first (fast attack, ceiling ~−3 dB to leave AAC headroom),
  then make up gain from measured values. Always verify I and TP on the
  **final muxed mp4** — AAC raises true peak by ~1 dB over the WAV.
- Loudnorm's printed JSON: extract it by brace-matching from `"input_i"`;
  naive `rindex('{')` slicing breaks on the log's other braces.

## Generated imagery in the pipeline

- Agnes (the zero-cost house channel): image 2.5-flash takes
  `{model, prompt, size}`; video 2.5-flash is a *different* schema —
  `{model, prompt, image?, mode}` with `mode` required
  (`text`/`keyframe`/`reference`) and no width/height/frames fields.
  The stock CLI's poll does a single GET with no retry — poll resiliently
  yourself, and expect the gateway to hang for tens of minutes at a time
  rather than fail; retry later, never in a tight loop.
- Reference images with non-ASCII filenames are rejected upstream (400).
  Rename to ASCII before any upload.
- A person's reference photo is chosen from the asset guide, never guessed
  from a similar-looking filename in a media library.
