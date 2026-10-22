#!/usr/bin/env python3
"""Rhythm gate (Studio v1.1, prototype thresholds).

Parses a shot-list.md and checks the rhythm rules that can be judged from
paper: R1 act-length contrast, sync-point coverage (M6), signature exits.

  python3 rhythm_audit.py shot-list.md

Act lines must carry time ranges, e.g.
  - s1 HOOK (0.00-2.45) — ...
Times may use '-' or '–'. Voiceover-driven films: if the shot list declares
'VO-anchored' anywhere, R1 contrast is reported as a warning instead of a
failure (the read dictates the grid; see references/scoring-v2.md).
"""
import re
import statistics
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: rhythm_audit.py <shot-list.md>")
        return 2
    text = open(sys.argv[1], encoding="utf-8").read()

    ranges = []
    for m in re.finditer(r"\((\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\)", text):
        a, b = float(m.group(1)), float(m.group(2))
        if b > a:
            ranges.append(b - a)
    if len(ranges) < 4:
        # table format: | A1 | 0–2.34 | ... |
        ranges = []
        for line in text.splitlines():
            if re.match(r"\s*\|\s*[As]\d", line):
                for m in re.finditer(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", line):
                    a, b = float(m.group(1)), float(m.group(2))
                    if b > a:
                        ranges.append(b - a)
    vo_anchored = "vo-anchored" in text.lower() or "VO 锚定" in text
    sync_pts = len(re.findall(r"(?im)^\s*-\s*SP\d+", text))
    sig_exits = len(re.findall(r"(?im)^.*\bexit\b.*\bsignature\b", text))
    has_sig = re.search(r"(?im)^[\s*\-\]*\**signature transition\**\s*[:：]", text)

    fails = []
    print(f"rhythm_audit  {sys.argv[1]}  (prototype)\n")
    if len(ranges) >= 4:
        med = statistics.median(ranges)
        longest, shortest = max(ranges), min(ranges)
        r_long, r_short = longest / med, shortest / med
        ok = r_long >= 1.8 and r_short <= 0.45
        line = (f"  {'PASS' if ok else 'FAIL'}  R1 act contrast        "
                f"longest {r_long:.2f}x / shortest {r_short:.2f}x median "
                f"(need >=1.80x / <=0.45x)  acts: "
                + "/".join(f"{d:g}" for d in ranges))
        if not ok and vo_anchored:
            print(line.replace("FAIL", "WARN") + "  [VO-anchored grid]")
        else:
            print(line)
            if not ok:
                fails.append("R1 act contrast")
    else:
        print(f"  FAIL  R1 act contrast        only {len(ranges)} act ranges parsed (need >= 4)")
        fails.append("R1 act ranges")

    ok = sync_pts >= max(3, len(ranges) - 1)
    print(f"  {'PASS' if ok else 'FAIL'}  M6 sync points         {sync_pts} listed "
          f"(need >= {max(3, len(ranges) - 1)}: one per boundary)")
    if not ok:
        fails.append("M6 sync points")

    ok = bool(has_sig) and sig_exits >= 3
    print(f"  {'PASS' if ok else 'FAIL'}  signature exits        {sig_exits} "
          f"(need >= 3, with the transition named)")
    if not ok:
        fails.append("signature exits")

    print(f"\n  {len(fails)} failed" + (" — " + ", ".join(fails) if fails else " — rhythm clear"))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
