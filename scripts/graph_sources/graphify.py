"""
Graphify substrate adapter — wraps the local `graphify` CLI (tree-sitter AST).

Everything here runs locally. `--code-only` uses no API key and nothing leaves the
machine; Graphify also auto-skips files it flags as sensitive (e.g. `.env`).
Install: `uv tool install graphifyy` (provides `graphify` + `graphify-mcp`).
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _local_bin() -> Path:
    return Path.home() / ".local" / "bin"


def graphify_bin() -> str | None:
    found = shutil.which("graphify")
    if found:
        return found
    cand = _local_bin() / "graphify"
    return str(cand) if cand.exists() else None


def _env() -> dict:
    env = os.environ.copy()
    lb = str(_local_bin())
    if lb not in env.get("PATH", ""):
        env["PATH"] = lb + os.pathsep + env.get("PATH", "")
    return env


def is_installed() -> bool:
    return graphify_bin() is not None


def ensure_installed() -> bool:
    """Install via `uv tool install graphifyy` if missing. Returns True if available."""
    if is_installed():
        return True
    uv = shutil.which("uv")
    if uv:
        subprocess.run([uv, "tool", "install", "graphifyy"], check=False, env=_env())
    return is_installed()


def graph_json_path(out_dir: Path) -> Path:
    return out_dir / "graphify-out" / "graph.json"


def extract(repo: Path, out_dir: Path, code_only: bool = True,
            backend: str | None = None) -> Path:
    """Build/refresh the code graph. Returns the graph.json path."""
    b = graphify_bin()
    if not b:
        raise RuntimeError("graphify not installed; run: uv tool install graphifyy")
    cmd = [b, "extract", str(repo), "--no-cluster", "--out", str(out_dir)]
    if code_only:
        cmd.append("--code-only")
    if backend:
        cmd += ["--backend", backend]
    subprocess.run(cmd, check=True, env=_env())
    return graph_json_path(out_dir)


def export_obsidian(graph_json: Path, dest: Path) -> int:
    """Emit Obsidian notes + canvas from an existing graph.json. Returns note count."""
    b = graphify_bin()
    if not b:
        raise RuntimeError("graphify not installed")
    if not graph_json.exists():
        raise FileNotFoundError(f"no graph.json at {graph_json} — run graphify_refresh.sh first")
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [b, "export", "obsidian", "--graph", str(graph_json), "--dir", str(dest)],
        check=True, env=_env(),
    )
    return sum(1 for _ in dest.rglob("*.md"))


def query(graph_json: Path, question: str, budget: int = 2000) -> str:
    """Ask the graph a question (BFS traversal). Returns stdout text."""
    b = graphify_bin()
    if not b:
        raise RuntimeError("graphify not installed")
    r = subprocess.run(
        [b, "query", question, "--graph", str(graph_json), "--budget", str(budget)],
        capture_output=True, text=True, env=_env(),
    )
    return r.stdout
