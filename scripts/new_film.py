#!/usr/bin/env python3
"""Scaffold a MOSEN Ad Studio project (prototype — spec M4 will harden this).

  python3 new_film.py <project-dir> [--brand <kit-name>] [--seconds 20]

Creates:
  <dir>/brief.md, shot-list.md      from templates/ (brief prefilled from kit)
  <dir>/assets.md, copy.md          starter stubs (table format — the audit
                                    reads sources from table rows)
  <dir>/film/{assets/fonts,renders} + hyperframes.json + package.json
  <dir>/audio/score_lib.py, score_template.py
  <dir>/qa/, <dir>/.gates/
Prints the remaining manual steps (gsap, fonts, assets) as a checklist.
"""
import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--brand", default="")
    ap.add_argument("--seconds", type=int, default=20)
    args = ap.parse_args()

    root = os.path.abspath(args.project)
    if os.path.exists(root) and os.listdir(root):
        print(f"refusing to scaffold into non-empty dir: {root}")
        return 1
    for d in ("film/assets/fonts", "film/renders", "audio", "qa", ".gates"):
        os.makedirs(os.path.join(root, d), exist_ok=True)

    kit = {}
    if args.brand:
        kp = os.path.join(SKILL, "kits", f"{args.brand}.json")
        if not os.path.exists(kp):
            print(f"kit not found: {kp}")
            return 1
        kit = json.load(open(kp, encoding="utf-8"))

    brief = open(os.path.join(SKILL, "templates/brief-template.md"), encoding="utf-8").read()
    brief = brief.replace("<product>", kit.get("product", "<product>"))
    if kit:
        brief = brief.replace("<#hex, sampled from the product's own imagery>",
                              kit.get("stage", "<#hex>"))
        brief = brief.replace("<#hex>", kit.get("accent", "<#hex>"))
        brief = brief.replace("<2–4 notes or one texture, from the product's own behaviour>",
                              kit.get("motif", "<motif>"))
        brief = brief.replace("<name — one move taken from the product's shape/behaviour; carries ≥3 exits>",
                              kit.get("signature", "<signature transition>"))
    open(os.path.join(root, "brief.md"), "w", encoding="utf-8").write(brief)

    shots = open(os.path.join(SKILL, "templates/shot-list-template.md"), encoding="utf-8").read()
    shots = shots.replace("<product>", kit.get("product", "<product>"))
    shots = shots.replace("<seconds>", str(args.seconds))
    if kit:
        shots = shots.replace("Signature transition: <name>",
                              f"Signature transition: {kit.get('signature', '<name>')}")
    open(os.path.join(root, "shot-list.md"), "w", encoding="utf-8").write(shots)

    open(os.path.join(root, "assets.md"), "w", encoding="utf-8").write(
        f"# Assets — {kit.get('product', '<product>')}\n\n"
        "| file | content | source |\n| --- | --- | --- |\n"
        "| logo.<ext> | primary wordmark | <official URL or 'provided by user'> |\n\n"
        "## Logo\nLogo check — right product: · current version: · variant: · "
        "untouched: · resolution: ·\n\n"
        f"## Stage\n{kit.get('stage', '<#hex>')} (kit median; must appear as a "
        "background: declaration in the film's <style>)\n")
    open(os.path.join(root, "copy.md"), "w", encoding="utf-8").write(
        "# Copy — verbatim only\n\n## As written\n- <official line>\n")

    for f in ("score_lib.py", "score_template.py"):
        shutil.copy(os.path.join(SKILL, "scripts", f), os.path.join(root, "audio", f))
    ex = os.path.join(SKILL, "examples/office-agent/film")
    for f in ("hyperframes.json", "package.json"):
        src = os.path.join(ex, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(root, "film", f))

    print(f"scaffolded {root}" + (f" (kit: {args.brand})" if args.brand else ""))
    print("""manual steps:
  1. drop gsap.min.js into film/assets/ and the brand fonts (woff2) into film/assets/fonts/
  2. fill brief.md -> G1 confirm -> assets.md (table rows!) -> copy.md -> shot-list.md
  3. build film/index.html (read references/production-lessons.md first)
  4. gates: film_audit -> layout_audit (AUDIT_W/H!) -> draft -> frame_audit -> rhythm_audit""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
