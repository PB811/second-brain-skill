#!/usr/bin/env bash
# install_cbm.sh — install + register codebase-memory-mcp (CBM), the second graph
# substrate. CBM is an MCP server, so after a FRESH install you must RESTART your
# agent before it connects. Idempotent.
#
# CBM = a single static binary (162 languages, zero deps). Public:
#   https://github.com/DeusData/codebase-memory-mcp
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"

if command -v codebase-memory-mcp >/dev/null 2>&1; then
  echo "CBM already installed: $(command -v codebase-memory-mcp)"
else
  echo "Installing codebase-memory-mcp…"
  if command -v npm >/dev/null 2>&1; then
    npm install -g codebase-memory-mcp
  else
    # Official installer (macOS/Linux). Review it first if you prefer:
    #   https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh
    curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
  fi
  export PATH="$HOME/.local/bin:$PATH"
fi

# Register CBM with the local coding agents (writes the MCP config).
codebase-memory-mcp install || true

echo
echo "==> CBM installed + registered."
echo "    RESTART your agent so the CBM MCP connects, then say:"
echo "      'Index this project'"
echo "    Until the restart, the second brain still builds fully on Graphify."
