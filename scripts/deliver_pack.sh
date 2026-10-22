#!/usr/bin/env bash
# Assemble the delivery pack: final MP4 + 3 poster frames.
#   scripts/deliver_pack.sh <project-dir> <final.mp4> <t1> <t2> <t3>
set -e
PROJ="$1"; FINAL="$2"; T1="$3"; T2="$4"; T3="$5"
OUT="$PROJ/delivery"
mkdir -p "$OUT"
cp "$FINAL" "$OUT/"
i=1
for t in "$T1" "$T2" "$T3"; do
  ffmpeg -y -v error -i "$FINAL" -ss "$t" -frames:v 1 "$OUT/poster-$i.jpg"
  i=$((i+1))
done
cp "$PROJ/copy.md" "$OUT/copy-sheet.md" 2>/dev/null || true
echo "delivery pack at $OUT:"
ls -la "$OUT"
