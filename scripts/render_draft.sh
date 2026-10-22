#!/usr/bin/env bash
# Draft render (fast, for the 8-dimension review). Run from the project root:
#   scripts/render_draft.sh
set -e
FILM_DIR="${1:-film}"
cd "$FILM_DIR"
mkdir -p renders .render-tmp
HYPERFRAMES_BROWSER_PATH="${CHROME_WRAPPER:-$HOME/workspace/tools/chrome-nosandbox.sh}" \
PRODUCER_HEADLESS_SHELL_PATH="${HEADLESS_WRAPPER:-$HOME/workspace/tools/headless-shell-nosandbox.sh}" \
PRODUCER_TMP_PROJECT_DIR="$PWD/.render-tmp" TMPDIR="$PWD/.render-tmp" \
PRODUCER_BROWSER_GPU_MODE=software \
npx --yes hyperframes@0.8.78 render . --fps 30
echo "draft submitted — ffprobe the landed file before reviewing."
