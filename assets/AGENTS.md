# AGENTS.md — how an agent maintains this second brain

You are an AI coding agent asked to build, refresh, or query this repo's
second brain. Read this first.

## Ground rules
- **Source of truth is `knowledge/`.** Write notes there, never directly into `vault/`
  (it's generated and gitignored). After editing, run `python3 second-brain/build_brain.py`.
- **No secrets in `knowledge/`.** It is committed. Keep credentials, customer data, and PII
  out. Sensitive ops detail goes only in the private `vault/`.
- **Ground every code claim in the graph or the source** — do not guess file/line refs.
- Notes are markdown with `[[wikilinks]]` and mermaid. Link liberally.

## Layer 1 — code structure (the graph)
Substrates are pluggable (`brain.config.json → graph_source`).

**CBM (codebase-memory-mcp)** — if the MCP is available. Project id in
`brain.config.json → graph_source.cbm.project`. Prefer over Read/grep:
- `get_architecture(project)`, `search_graph(name_pattern|label|qn_pattern)`,
  `trace_path(fn, mode=calls|data_flow|cross_service)`, `get_code_snippet(qn)`,
  `search_code(pattern)`, `detect_changes(project)` (drives on-demand regen),
  `index_repository(...)` if unindexed.

**Graphify** — the portable substrate (`graphifyy`):
- Refresh the graph (heavy, on-demand): `second-brain/graphify_refresh.sh` (code-only, zero
  egress). Or `graphify update <repo>` for an LLM-free incremental refresh.
- Its Obsidian notes + `graph.canvas` are folded into `vault/graphify/` by `build_brain.py`.
- Query it: `graphify query "<q>" --graph second-brain/.graphify/graphify-out/graph.json`,
  `graphify explain "<node>"`, `graphify affected "<node>"`, `graphify god-nodes`.
- Adapter: `second-brain/graph_sources/graphify.py`.

## Refreshing the CODE notes (on-demand)
1. `detect_changes(project)` (CBM) or `graphify update` to see what moved.
2. Re-derive structure for affected flows/modules via `trace_path` / `graphify query`.
3. Update the matching note in `knowledge/code/` or `knowledge/flows/` — keep the mermaid +
   the `qualified_name → file:line` table accurate.
4. `python3 second-brain/build_brain.py` to regenerate the vault.

## Note types (see the skill's templates)
- **flow** — an end-to-end pipeline (mermaid + step table + decision points).
- **decision (ADR)** — a choice with context/options/consequence (numbered).
- **runbook** — an ops procedure (steps + commands + rollback).

## When queried ("how does X work?")
Answer from the vault notes first; fall back to the code graph to verify or fill gaps; if
you learn something durable, write it back into `knowledge/` and rebuild.
