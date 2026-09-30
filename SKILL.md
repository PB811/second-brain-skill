---
name: second-brain
description: >-
  Build a reusable, private "second brain" knowledge base for ANY codebase — a generated
  Obsidian vault backed by two code-graph substrates (codebase-memory-mcp + Graphify). Use
  this whenever the user wants to understand, onboard onto, document, or map a codebase;
  create a knowledge base, second brain, wiki, or Obsidian vault for a repo; visualize the
  code as a graph; or make a codebase queryable by AI agents. Trigger on phrases like
  "second brain", "codebase brain", "repo knowledge base", "obsidian for this repo", "code
  knowledge graph", "map the codebase", "onboard me to this repo", or "graphify" — even if
  the user doesn't name the skill. Always begins AND ends by explaining what each graph
  (CBM vs Graphify; Obsidian graph view vs Canvas vs HTML) actually shows.
---

# Second Brain

Generate a repo-agnostic **second brain**: a committed *builder* (the recipe) that produces
a private, gitignored **Obsidian vault** (the output) from the codebase. Two graph
substrates feed it — **CBM** (codebase-memory-mcp, agent-queried, optional) and **Graphify**
(`graphifyy`, local tree-sitter, portable). Curated markdown notes carry the meaning on top.

**Bundled resources** (in this skill dir):
- `scripts/build_brain.py`, `scripts/graphify_refresh.sh`, `scripts/graph_sources/` — the builder.
- `assets/` — `brain.config.template.json`, `gitignore.template`, `README.md`, `AGENTS.md`,
  `templates/` (flow/decision/runbook note templates).
- `references/graph-explainer.md` — the canonical "what each graph means" (used at start & end).
- `references/knowledge-authoring.md` — how to write the per-repo knowledge notes.

Work in the user's current repo (`cwd`). Do everything under `<repo>/second-brain/`.

---

## Step 0 — Explain the graphs (REQUIRED, do this FIRST)

Before building anything, tell the user what they're going to get and, crucially, **what
each graph means** — people constantly conflate them. Read `references/graph-explainer.md`
and give a short version: the two substrates (CBM = the graph Claude queries, invisible;
Graphify = the graph you see) and the three openable views (Obsidian graph view, Graphify
Canvas, Graphify HTML). Keep it to a few sentences unless they want more.

## Step 1 — Scaffold `<repo>/second-brain/`

Create the folder and copy the builder in (from this skill's dir — call it `$SKILL`):
- `scripts/build_brain.py`      → `second-brain/build_brain.py`
- `scripts/graphify_refresh.sh` → `second-brain/graphify_refresh.sh` (make executable)
- `scripts/graph_sources/`      → `second-brain/graph_sources/`
- `assets/templates/`           → `second-brain/templates/`
- `assets/README.md`            → `second-brain/README.md`
- `assets/AGENTS.md`            → `second-brain/AGENTS.md`
- `assets/gitignore.template`   → `second-brain/.gitignore`
- `assets/graphifyignore.template` → ensure `second-brain/` is listed in `<repo>/.graphifyignore`
  (create it from the template if absent, else append the line) so Graphify does not index the
  scaffold's own machinery — otherwise `build_brain.py`/`graph_sources/*` show up as graph nodes.
- `assets/brain.config.template.json` → `second-brain/brain.config.json`, then fill:
  - `{{PROJECT_TITLE}}` = a short repo name/title.
  - `{{PROJECT_DESCRIPTION}}` = one line on what the repo does.
  - `{{CBM_PROJECT_OR_NULL}}` = the CBM project id (Step 2) or `null`.
  - Adjust `route_scan`: keep for Python/FastAPI-style repos; for other stacks set
    `patterns` (see examples in `build_brain.py`) or `enabled: false`. Tune `include_globs`.

## Step 2 — Wire CBM (install it if missing)

CBM (`codebase-memory-mcp`) is a public single static binary that runs as an MCP server.

- **If the codebase-memory MCP tools are already available:** use them —
  `list_projects()` and match `root_path` to the repo to get the project id (or
  `index_status(project)`; `index_repository(...)` if not indexed). Put the id into
  `brain.config.json → graph_source.cbm.project`.
- **If CBM is NOT available:** install + register it with `scripts/install_cbm.sh` (npm or
  the official installer, then `codebase-memory-mcp install`). **Important:** CBM is an MCP
  *server*, so it only connects after the agent (Claude Code) **restarts** — you cannot query
  it in the same run. So: run the installer, tell the user to restart and later say "Index this
  project", set `cbm.project` in the config anyway (predict the id from the repo path, e.g.
  `home-<user>-...-<repo>`), and **continue this run on Graphify** (Step 3), which needs no
  restart. CBM then enriches future runs/queries.

CBM is optional-but-recommended: Graphify alone produces a complete brain; CBM adds the
live, agent-queried call-graph on top.

## Step 3 — Wire Graphify (the portable baseline)

- Ensure installed: `uv tool install graphifyy` (provides `graphify` + `graphify-mcp`;
  binaries in `~/.local/bin`). It's already there if `graphify --version` works.
- Build the graph locally (zero egress; `.env` auto-skipped):
  `second-brain/graphify_refresh.sh` — this runs `graphify extract . --code-only` into
  `second-brain/.graphify/` AND then runs `build_brain.py`.
  (Equivalent manual: `graphify extract <repo> --code-only --no-cluster --out second-brain/.graphify`.)

## Step 4 — Author the starter knowledge

Read `references/knowledge-authoring.md`. Using the graphs (CBM `trace_path` / `search_graph`,
or `graphify query` / `graphify explain` / `graphify god-nodes`), write a small, high-value
set of `knowledge/` notes for THIS repo: `architecture/overview.md`, a `flows/<name>.md` per
major path, `reference/glossary.md`, `decisions/0001-graph-substrate.md`, plus `business/`,
`ops/`, and 1-2 `code/` notes as warranted. Ground every claim in `file:line`. No secrets.

## Step 5 — Build

`python3 second-brain/build_brain.py` → generates `second-brain/vault/` (curated notes +
auto-scanned routes + folded Graphify notes + MOCs + `00-Home`). Report the note count.

## Step 6 — (optional) HTML views + a query demo

- `graphify export html --graph second-brain/.graphify/graphify-out/graph.json`
  (also `graphify tree` and `graphify export callflow-html` for tree + mermaid views).
- Demo the Q&A: `graphify query "<a real question about this repo>" --graph <graph.json>`.

## Step 7 — Explain the graphs AGAIN (REQUIRED, do this at the END)

Close by recapping, from `references/graph-explainer.md`:
- **What was generated** and where (`second-brain/vault/`, note count).
- **How to open each view**: Obsidian graph view (open the vault → `Ctrl/Cmd+G`), the
  Graphify Canvas (`vault/graphify/graph.canvas`), and the Graphify HTML
  (`second-brain/.graphify/graphify-out/graph.html`).
- **What each shows** (CBM invisible-but-queryable; Graphify visible; curated = meaning).
- **How to refresh** (`graphify_refresh.sh`) and **how to query in Obsidian** (Local REST
  API MCP + Smart Connections/Copilot — see the generated `README.md`).

---

## Notes

- **Committed vs generated.** Only the recipe commits; `vault/` and `.graphify/` are
  gitignored. Verify before any commit that neither stages. If the user wants it committed
  and they're on a shared/default branch, create a branch first. Follow the user's commit
  attribution rules (e.g. a CLAUDE.md/memory rule may forbid `Co-Authored-By`).
- **Security.** Nothing secret in `knowledge/` (committed). Graphify's `--code-only` is local
  and auto-skips `.env`; only use a `BACKEND=ollama` (local) for the doc/PDF layer to keep
  content off the cloud.
- **Genericity.** Graphify covers ~36 languages; CBM is optional. For non-web repos, turn off
  `route_scan`. Keep the knowledge set lean — a dozen strong notes beat a hundred thin ones.
- **Freshness is on-demand.** Re-run `build_brain.py` (light) any time; re-run
  `graphify_refresh.sh` (heavy) to rebuild the code graph; use CBM `detect_changes` to target
  what moved.
