"""
CBM substrate — codebase-memory-mcp (agent-driven, optional).

CBM is queried at runtime by the AGENT via MCP tools, NOT by a plain Python
script (there is no local CLI to shell out to). So this module only records the
contract; the actual work happens when an agent follows ../AGENTS.md:

  list_projects() / index_status(project)   -> is this repo indexed?
  index_repository(...)                      -> index it if not
  get_architecture(project)                  -> packages/counts
  search_graph(name_pattern|label|qn_pattern) -> find funcs/classes/routes
  trace_path(function_name, mode=...)        -> call chains / data flow
  get_code_snippet(qualified_name)           -> source
  detect_changes(project)                    -> what moved (drives on-demand regen)

The agent writes CBM-derived notes into knowledge/code/ (committed, reviewed),
which the deterministic builder then copies into the vault.

The project id is per-repo; it lives in brain.config.json -> graph_source.cbm.project
(codebase-memory names projects after the repo path). Do NOT hardcode it here.
"""

# Filled per-repo in brain.config.json; None here on purpose (generic skill).
PROJECT = None
AGENT_DRIVEN = True
