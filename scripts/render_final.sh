#!/usr/bin/env bash
# Final render (high quality). Run from the project root:
#   scripts/render_final.sh            # renders ./film, draft = render_draft.sh
# Environment is the proven recipe — see references/production-lessons.md.
# CHROME_WRAPPER / HEADLESS_WRAPPER point at local no-sandbox chrome wrappers.
set -e
FILM_DIR="${1:-film}"
cd "$FILM_DIR"
mkdir -p renders .render-tmp
HYPERFRAMES_BROWSER_PATH="${CHROME_WRAPPER:-$HOME/workspace/tools/chrome-nosandbox.sh}" \
PRODUCER_HEADLESS_SHELL_PATH="${HEADLESS_WRAPPER:-$HOME/workspace/tools/headless-shell-nosandbox.sh}" \
PRODUCER_TMP_PROJECT_DIR="$PWD/.render-tmp" TMPDIR="$PWD/.render-tmp" \
PRODUCER_BROWSER_GPU_MODE=software \
npx --yes hyperframes@0.8.78 render . -q high --fps 30
echo "render submitted — the file lands 1-2 min after the completion line; ffprobe before use."
