"""
Pluggable Layer-1 graph substrates for the second brain.

- `cbm`      — codebase-memory-mcp: MCP-native, queried live by the AGENT
               (search_graph / trace_path / detect_changes). Not called from a
               plain script; see cbm.py + ../AGENTS.md. Optional (only where the
               codebase-memory MCP is available).
- `graphify` — local tree-sitter code graph (the `graphify` CLI, pip: graphifyy).
               Portable baseline: extract -> export Obsidian notes into the vault.

Both can be active. CBM is the agent's live query substrate where present;
Graphify is the portable, self-contained one. See Decisions/0001.
"""
