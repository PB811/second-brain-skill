# Second Brain

A reproducible knowledge base for this repository. Think of it as **"docker compose for a
second brain"**: the *recipe* lives in git; each developer or agent builds their own private
Obsidian vault from it with one command.

## The model

| Path | Committed? | Role |
| --- | --- | --- |
| `second-brain/knowledge/` | yes (sanitized, no secrets) | **Source of truth.** Curated + agent-generated markdown notes. Edit here. |
| `second-brain/build_brain.py` + `brain.config.json` + `graph_sources/` + `templates/` | yes | The **builder** (the "compose file"). |
| `second-brain/AGENTS.md` | yes | How an agent refreshes the code notes from the graph. |
| `second-brain/vault/` | no (gitignored) | **Generated Obsidian vault.** Open THIS in Obsidian. Private. |
| `second-brain/.graphify/` | no (gitignored) | Graphify's code graph + HTML visualizations. |

Editing rule: **change notes in `knowledge/`, then rebuild.** `vault/` is disposable output.

## Build it (any dev, any agent, one command)
```bash
python3 second-brain/build_brain.py
```
Python 3.10+ stdlib only — no MCP, no LLM, no network. Then open `second-brain/vault/` as a
vault in Obsidian → start at `00-Home`.

## Query it — two ways
1. **Claude Code ↔ vault** via the Obsidian *Local REST API* plugin (v5+):
   ```bash
   claude mcp add --transport http obsidian https://127.0.0.1:27124/mcp/ \
     --header "Authorization: Bearer <YOUR_OBSIDIAN_API_KEY>"
   ```
2. **In-Obsidian chat** — Smart Connections (RAG over the vault) and/or Copilot. Point at a
   local model (Ollama) to keep repo content off cloud APIs.

## Graph substrates
- **CBM** (`codebase-memory-mcp`) — agent-queried code graph. A public single static binary
  (162 languages). If it's missing, the skill installs + registers it via
  `second-brain/install_cbm.sh` (or manually: `npm i -g codebase-memory-mcp && codebase-memory-mcp install`).
  **It's an MCP server, so restart Claude Code after installing**, then say "Index this project".
- **Graphify** (`graphifyy`) — local tree-sitter graph; Obsidian notes + Canvas + HTML.
  Refresh: `second-brain/graphify_refresh.sh` (code-only = zero egress; `.env` auto-skipped).
  Ask it: `graphify query "<q>" --graph second-brain/.graphify/graphify-out/graph.json`.

Both run on **Python + `uv`** on the machine (that's what Graphify needs, and CBM is a binary);
the analyzed project can be **any language**. CBM is optional — Graphify alone is a full brain.

## Security
Never put secrets, live credentials, customer data, or PII in `knowledge/` (it's committed).
Sensitive ops notes belong in the gitignored `vault/` only.
