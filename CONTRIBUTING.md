# Contributing

Thanks for your interest — this is a small, focused skill, and PRs / issues are welcome.

## What this is
An **agent-agnostic skill** that turns any codebase into a private Obsidian "second brain".
- `SKILL.md` — the workflow an AI coding agent follows.
- `scripts/` — the builder (`build_brain.py`, stdlib-only), `graphify_refresh.sh`, `install_cbm.sh`, `graph_sources/`.
- `assets/` — config + note templates + the per-repo README/AGENTS shipped into each brain.
- `references/` — the graph explainer, knowledge-authoring guide, deep-wiki mode.
- `second_brain_cli/` + `pyproject.toml` — the `uvx … second-brain install` entry point.

## Dev setup
- Python 3.10+ and [`uv`](https://docs.astral.sh/uv/).
- Try the installer locally (installs into a throwaway dir):
  ```bash
  CLAUDE_SKILLS_DIR=/tmp/sb-test uvx --from . second-brain install
  ```

## Guidelines
- Keep `scripts/build_brain.py` **stdlib-only and deterministic** (no network/LLM in the build).
- Keep the graph substrate **pluggable** (CBM + Graphify); don't hard-code a repo.
- **No secrets** in committed files. Generated output (`vault/`, `.graphify/`) stays gitignored.
- Update `SKILL.md` + the relevant `references/` doc when you change behavior.

## License
By contributing, you agree your contributions are licensed under the MIT License.
