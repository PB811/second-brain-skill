# Deep wiki mode

Two authoring depths for the `knowledge/` layer:

- **Lean (default)** — ~a dozen high-value notes (overview, key flows, glossary, ADRs). The
  Graphify export already gives exhaustive per-symbol coverage; lean notes are the *map a
  human reads first*. Fast, cheap.
- **Deep** — a DeepWiki-style **multi-page wiki** authored from the graph. Use when the user
  asks for a "deep wiki", "full wiki", "document everything", or is onboarding a large /
  unfamiliar codebase and wants depth over speed.

## When to pick deep
The user says so, OR the repo is large/unfamiliar and they want thorough documentation.
Deep mode costs more time + tokens — say so before you commit to it.

## How to author a deep wiki (from the graph, grounded)
1. **Get the map of subsystems, not functions.** The per-function notes already exist in
   `vault/graphify/`. Deep pages are per **subsystem / module / cluster**:
   - Graphify: `graphify god-nodes` (architectural hubs), and run a *clustered* extract
     (drop `--no-cluster`; optionally `cluster-only` + `label --backend ollama` to name
     communities locally). Communities ≈ subsystems.
   - CBM: `get_architecture`, then `search_graph(qn_pattern=...)` per folder/module.
2. **One page per subsystem** in `knowledge/wiki/<subsystem>.md`. Each page:
   - purpose + responsibilities; key classes/functions with `file:line`;
   - how it connects to other subsystems (inbound/outbound), a **mermaid** diagram;
   - notable decisions, gotchas, entry points.
3. **Keep the lean notes too** — overview, flows, ADRs, glossary — and have `overview.md`
   link to every wiki page (so the graph view + MOCs stay navigable).
4. **Ground every claim** in `file:line` (CBM `trace_path` / `get_code_snippet`, or
   `graphify explain "<node>"`). No secrets. Link liberally.
5. Rebuild: `python3 second-brain/build_brain.py`.

## Stop rule
Scale page count to the repo. Stop when another page adds little — depth, not bulk. A great
deep wiki is a set of subsystem maps a new engineer could onboard from in an afternoon.
