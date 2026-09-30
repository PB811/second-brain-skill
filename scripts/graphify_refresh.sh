#!/usr/bin/env bash
# graphify_refresh.sh — (re)build the local Graphify code graph, then rebuild the brain.
#
# The HEAVY, on-demand step. Runs a local tree-sitter extraction (no API key,
# nothing leaves the machine) and folds the resulting Obsidian notes into the vault
# via build_brain.py. Lives at <repo>/second-brain/graphify_refresh.sh.
#
# Usage:
#   second-brain/graphify_refresh.sh              # code-only (zero egress)
#   BACKEND=ollama second-brain/graphify_refresh.sh   # also extract docs/PDFs + label, via local Ollama
set -euo pipefail

SB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SB_DIR/.." && pwd)"
OUT_DIR="$SB_DIR/.graphify"
export PATH="$HOME/.local/bin:$PATH"

if ! command -v graphify >/dev/null 2>&1; then
  echo "graphify not found — installing (uv tool install graphifyy)…"
  uv tool install graphifyy
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> extracting code graph from $REPO_DIR (local; .env is auto-skipped)"
if [ -n "${BACKEND:-}" ]; then
  graphify extract "$REPO_DIR" --backend "$BACKEND" --out "$OUT_DIR"
else
  graphify extract "$REPO_DIR" --code-only --no-cluster --out "$OUT_DIR"
fi

echo "==> folding Graphify notes into the vault"
python3 "$SB_DIR/build_brain.py"

echo "==> done. Graph: $OUT_DIR/graphify-out/graph.json"
echo "    Ask it directly, e.g.:"
echo "      graphify query \"how does the main request flow work?\" --graph \"$OUT_DIR/graphify-out/graph.json\""
