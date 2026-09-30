"""
second-brain — installer CLI for the second-brain Claude Code skill.

Run without a manual install via uv:
    uvx --from git+https://github.com/PB811/second-brain-skill second-brain install

`install` copies the skill into ~/.claude/skills/second-brain/ (override the target
with the CLAUDE_SKILLS_DIR env var). After installing, open Claude Code in any repo
and say "build a second brain for this repo".
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

SKILL_NAME = "second-brain"
_ITEMS = ["SKILL.md", "scripts", "assets", "references"]

__version__ = "0.1.0"


def _skill_root() -> Path | None:
    """Locate the bundled skill files, whether running from a built wheel or source."""
    # 1) wheel: force-included under second_brain_cli/_skill/
    here = Path(__file__).resolve().parent
    cand = here / "_skill"
    if (cand / "SKILL.md").exists():
        return cand
    # 2) source checkout: repo root (parent of this package dir)
    repo = here.parent
    if (repo / "SKILL.md").exists():
        return repo
    return None


def _skills_dir() -> Path:
    env = os.environ.get("CLAUDE_SKILLS_DIR")
    return Path(env).expanduser() if env else (Path.home() / ".claude" / "skills")


def install() -> int:
    root = _skill_root()
    if root is None:
        print("error: bundled skill files not found", file=sys.stderr)
        return 1
    dest = _skills_dir() / SKILL_NAME
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for item in _ITEMS:
        src = root / item
        if src.is_dir():
            shutil.copytree(src, dest / item)
        elif src.exists():
            shutil.copyfile(src, dest / item)
    print(f"Installed '{SKILL_NAME}' skill -> {dest}")
    print("Next: open Claude Code in any repo and say:")
    print('  "build a second brain for this repo"')
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:]) if argv is None else list(argv)
    cmd = argv[0] if argv else "install"
    if cmd in ("install", "-i", "--install"):
        return install()
    if cmd in ("-h", "--help", "help"):
        print(
            "second-brain — install the Claude Code second-brain skill\n\n"
            "usage:\n"
            "  second-brain install   copy the skill into ~/.claude/skills/ (or $CLAUDE_SKILLS_DIR)\n"
            "  second-brain --help\n\n"
            "then, in any repo, tell Claude Code: 'build a second brain for this repo'"
        )
        return 0
    if cmd in ("-V", "--version", "version"):
        print(__version__)
        return 0
    print(f"unknown command: {cmd}\nTry: second-brain install", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
