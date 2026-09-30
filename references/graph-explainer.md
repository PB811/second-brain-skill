# Graph explainer — say this at the START and again at the END

This second brain has **three graph renderings plus one invisible substrate**. People
routinely confuse them, so explain them clearly. Adapt the wording to the user; keep the
distinctions.

## The two substrates (where the knowledge comes from)
- **CBM — codebase-memory-mcp** (optional, only where that MCP exists). A *code* knowledge
  graph: functions, classes, routes, call chains, data flow. **Agent-queryable, not
  visual** — the agent queries it (`search_graph`, `trace_path`, `detect_changes`); it has
  no notes or HTML you open. Think: "the graph Claude reads for you."
- **Graphify** (`graphifyy`, the portable baseline). *Also* a code graph (tree-sitter), but
  it **exports to files you can see**: Obsidian notes, an Obsidian Canvas, and standalone
  HTML. It captures functions/classes **plus docstrings**. Think: "the graph you look at."

> Neither tool *understands business logic* on its own — both give structural facts. The
> "why" and the human-readable flows live in the curated `knowledge/` notes + an LLM
> reasoning over the graph.

## The three things you can actually open
1. **Obsidian Graph View** (built-in) — renders the **note-link graph**: every `[[wikilink]]`
   between notes in the vault. Because Graphify's code notes are folded into the vault, this
   view is mostly *the Graphify code graph expressed as notes*, plus the curated knowledge
   notes. Open the vault → graph icon / `Ctrl/Cmd+G`.
2. **Graphify `graph.canvas`** — Graphify's code graph as an **Obsidian Canvas** (spatial
   board). Open `vault/graphify/graph.canvas` inside Obsidian.
3. **Graphify HTML** — Graphify's own **browser** visualizations, independent of Obsidian:
   `graph.html` (interactive force-directed), `GRAPH_TREE.html` (collapsible tree),
   `graphify-callflow.html` (mermaid call-flow). In `second-brain/.graphify/graphify-out/`.

## One-liner to leave them with
> **CBM = the graph Claude queries (invisible). Graphify = the graph you see (Obsidian
> notes + Canvas + HTML). The curated notes = the meaning on top.**
