# Authoring the per-repo knowledge notes

The generated Graphify notes cover *code structure*. The curated `knowledge/` notes carry
the **meaning** — the flows, the "why", the business logic, the runbooks. Write a small,
high-value starter set by reading THIS codebase through the graphs; do not invent.

## Ground rules
- **Source of truth is `knowledge/`.** Write notes there, never into `vault/` (generated).
  Rebuild with `python3 second-brain/build_brain.py` after edits.
- **No secrets in `knowledge/`** — it's committed. Credentials/PII stay out.
- **Ground every code claim** in the graph or the source (`qualified_name` / `file:line`).
  Do not guess. If unsure, write the note and mark the spot "verify".
- Markdown + `[[wikilinks]]` + mermaid. Link liberally; a `[[note]]` that doesn't exist yet
  is a fine TODO marker.

## Starter set to aim for (scale to the repo's size)
Use the templates in the skill's `assets/templates/`.
- `architecture/overview.md` — what the system is, its stack, a mermaid of the top-level
  shape, and a table of the main components with `file:line`.
- `flows/<name>.md` — one per major end-to-end path. Derive the call chain from the graph
  (`trace_path` on CBM, or `graphify query` / `graphify explain`), then narrate it.
- `business/*.md` — domain rules that aren't obvious from code (enums, formats, policies).
- `decisions/0001-graph-substrate.md` — record the CBM+Graphify choice for this repo.
- `reference/glossary.md` — the repo's domain + system vocabulary.
- `ops/*.md` — runbooks for anything operational (deploy, migrations, incidents).
- `code/*.md` — 1-2 notes distilled from the code graph (hubs, entrypoints, `god-nodes`).

## How to derive flows from each substrate
- **CBM present:** `get_architecture`, `search_graph(label="Route"|"Class")`,
  `trace_path("<entry>", mode=calls|data_flow)`, `get_code_snippet(qn)`.
- **Graphify:** `graphify query "<question>" --graph .../graph.json`,
  `graphify explain "<node>"`, `graphify god-nodes`, `graphify affected "<node>"`.
- Cross-check the two — they surface different things (e.g. queues/consumers vs HTTP routes).

## Keep it lean
A dozen strong notes beat a hundred thin ones. The Graphify export already gives exhaustive
per-symbol coverage; the curated notes should be the map a human reads first.
