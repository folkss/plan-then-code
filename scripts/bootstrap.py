#!/usr/bin/env python3
"""Bootstrap a non-system-drive project for the big-project-workflow skill.

Renders the four bundled templates from ``assets/templates/`` into the
target project directory and (optionally) initializes Trellis. The
script never installs npm packages on its own — if ``trellis`` is not on
``PATH`` it prints the install command and exits cleanly.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import getpass
import locale
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_ROOT / "assets" / "templates"


# ---------- helpers ----------------------------------------------------------


def run(command: list[str], cwd: Path) -> None:
    result = subprocess.run(command, cwd=str(cwd), text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(f"Command failed in {cwd}: {' '.join(command)}")


def default_root() -> Path:
    """Pick a sensible non-system project root for the current OS."""
    env_root = os.environ.get("BIG_PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser()

    if os.name == "nt":
        system_letter = (
            os.environ.get("SystemDrive", "C:")
            .rstrip("\\/")
            .upper()[0]
        )
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter == system_letter:
                continue
            drive = Path(f"{letter}:/")
            if drive.exists():
                return drive / "codex-projects"
        return Path.home() / "codex-projects"

    # macOS / Linux / WSL
    return Path.home() / "codex-projects"


def default_developer() -> str:
    return os.environ.get("TRELLIS_DEVELOPER") or getpass.getuser() or "developer"


SUPPORTED_LANGUAGES = ("en", "zh-CN")


def detect_language() -> str:
    """Detect a UI language from env vars / system locale.

    Returns one of ``SUPPORTED_LANGUAGES``. Currently maps any Chinese
    locale to ``zh-CN`` and defaults everything else to ``en``.
    """
    forced = os.environ.get("BIG_PROJECT_LANGUAGE")
    if forced:
        return forced

    for var in ("LC_ALL", "LANG", "LANGUAGE"):
        value = os.environ.get(var, "")
        if value.lower().startswith("zh"):
            return "zh-CN"

    try:
        loc = locale.getlocale()[0] or ""
        if not loc:
            try:
                loc = (locale.getdefaultlocale()[0] or "")  # type: ignore[attr-defined]
            except Exception:
                loc = ""
        loc_lower = loc.lower()
        if "zh" in loc_lower or "chinese" in loc_lower:
            return "zh-CN"
    except Exception:
        pass

    return "en"


def resolve_language(value: str | None) -> str:
    """Map ``--language`` value to a supported code, falling back to detection."""
    if not value or value == "auto":
        return detect_language()
    return value


def find_trellis(explicit: str | None = None) -> str | None:
    if explicit:
        return explicit
    for candidate in ("trellis", "trellis.cmd", "trellis.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    return None


def is_system_drive(path: Path) -> bool:
    """True only on Windows when the resolved path lives on the system drive."""
    if os.name != "nt":
        return False
    system_root = os.environ.get("SystemDrive", "C:").lower().rstrip("\\/")
    anchor = path.resolve().anchor.lower().rstrip("\\/")
    return anchor == system_root


def render(template_name: str, variables: dict[str, str], language: str = "en") -> str:
    """Render a template, preferring a localized variant when one exists.

    Looks for ``<template_name>.<language>.md`` first; falls back to
    ``<template_name>.md`` (the canonical English file).
    """
    candidates: list[Path] = []
    if language and language != "en":
        candidates.append(TEMPLATES_DIR / f"{template_name}.{language}.md")
    candidates.append(TEMPLATES_DIR / f"{template_name}.md")
    template_path = next((p for p in candidates if p.exists()), None)
    if template_path is None:
        raise SystemExit(f"Template not found: {candidates[0]}")
    text = template_path.read_text(encoding="utf-8")
    for key, value in variables.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


# ---------- main -------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Bootstrap a non-system-drive project folder, initialize git and "
            "Trellis, and lay down the Claude→Codex handoff templates."
        )
    )
    parser.add_argument("--name", required=True, help="Project folder name")
    parser.add_argument(
        "--root",
        default=None,
        help=(
            "Parent folder. Defaults to BIG_PROJECT_ROOT, the first non-system "
            "drive on Windows plus 'codex-projects', or '~/codex-projects'."
        ),
    )
    parser.add_argument(
        "--developer",
        default=None,
        help="Trellis developer name. Defaults to TRELLIS_DEVELOPER or the OS user.",
    )
    parser.add_argument("--brief", default="", help="One-paragraph project goal")
    parser.add_argument(
        "--trellis-version",
        default="latest",
        help="Trellis CLI version to install (used only in the printed install hint).",
    )
    parser.add_argument(
        "--platforms",
        default="codex",
        help=(
            "Comma-separated Trellis platform flags (e.g. 'codex' or "
            "'codex,claude'). Trellis 0.4+ generates .claude/ by default, so "
            "'codex' alone is usually enough."
        ),
    )
    parser.add_argument(
        "--trellis-bin", default=None, help="Explicit path to the trellis executable"
    )
    parser.add_argument(
        "--allow-system-drive",
        action="store_true",
        help="Permit a system-drive target on Windows (e.g. C:)",
    )
    parser.add_argument(
        "--skip-trellis", action="store_true", help="Skip the trellis init step"
    )
    parser.add_argument(
        "--language",
        default="auto",
        help=(
            "Output language for generated docs and next-steps hints. "
            "'auto' (default) detects from BIG_PROJECT_LANGUAGE / LANG / "
            "system locale. Explicit values: 'en' or 'zh-CN'."
        ),
    )
    return parser.parse_args()


def init_git(project: Path) -> bool:
    if (project / ".git").exists():
        return False
    run(["git", "init"], project)
    return True


def init_trellis(project: Path, args: argparse.Namespace, developer: str) -> str | None:
    if args.skip_trellis:
        return "skipped"
    trellis = find_trellis(args.trellis_bin)
    if not trellis:
        return None
    if (project / ".trellis").exists():
        return "already-initialized"
    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]
    flags: list[str] = []
    for platform in platforms:
        flags.append(f"--{platform}")
    run([trellis, "init", *flags, "-u", developer, "-y"], project)
    return "initialized"


def write_project_files(
    project: Path, args: argparse.Namespace, language: str
) -> dict[str, bool]:
    today = _dt.date.today().isoformat()
    variables = {
        "name": args.name,
        "brief": (args.brief.strip() or "TBD. Replace this with the project goal."),
        "developer": args.developer or default_developer(),
        "date": today,
        "language": language,
    }

    written: dict[str, bool] = {}

    project_brief = project / "docs" / "PROJECT_BRIEF.md"
    written[str(project_brief)] = write_if_missing(
        project_brief, render("project-brief", variables, language)
    )

    claude_prompt = project / "docs" / "claude" / "00-prd-spec-prompt.md"
    written[str(claude_prompt)] = write_if_missing(
        claude_prompt, render("claude-planning-prompt", variables, language)
    )

    codex_handoff = project / "docs" / "codex" / "00-implementation-handoff.md"
    written[str(codex_handoff)] = write_if_missing(
        codex_handoff, render("codex-handoff", variables, language)
    )

    tasks_dir = project / ".trellis" / "tasks"
    if tasks_dir.exists():
        launch_task = tasks_dir / "000-project-launch.md"
        written[str(launch_task)] = write_if_missing(
            launch_task, render("launch-task", variables, language)
        )

    return written


def report(
    project: Path,
    trellis_status: str | None,
    args: argparse.Namespace,
    written: dict[str, bool],
    language: str,
) -> None:
    print()
    print("=" * 60)
    print(f"Project bootstrapped: {project}")
    print("=" * 60)
    print(f"  Git:    {'initialized' if (project / '.git').exists() else 'missing'}")
    if trellis_status is None:
        print("  Trellis: not found on PATH")
        print(
            f"           Install with: npm install -g "
            f"@mindfoldhq/trellis@{args.trellis_version}"
        )
        print("           Then re-run this script (it will skip the project folder).")
    else:
        print(f"  Trellis: {trellis_status}")
    claude_cli_path = shutil.which("claude")
    if claude_cli_path:
        print(f"  Claude CLI:  {claude_cli_path}")
    else:
        print("  Claude CLI:  NOT on PATH (Stage 1 cannot run without it)")
    print(f"  .claude/ dir: {'present' if (project / '.claude').exists() else 'absent'}")
    print(f"  .codex/ dir:  {'present' if (project / '.codex').exists() else 'absent'}")
    print(f"  Language:    {language}")
    print()
    print("Files:")
    for path, was_new in written.items():
        marker = "+" if was_new else "·"
        print(f"  {marker} {path}")
    print()

    if language == "zh-CN":
        print("后续步骤：")
        print("  1. Stage 1（Claude 写文档）：")
        print(f"     - cd \"{project}\"")
        print("     - 启动交互式 Claude Code：claude")
        print("     - 在 Claude Code 会话里说：")
        print("         读 docs/claude/00-prd-spec-prompt.md，按它执行 Stage 1。")
        print("     注意：不要用 `claude -p` 管道模式 —— 问卷需要交互。")
        print("     如需指定模型，在会话里用 /model 切换（比如 claude-opus-4-7[1m]）。")
        print()
        print("  2. Stage 2（Codex 实现）：回到这个项目下的 Codex，然后说：")
        print("         读 docs/codex/00-implementation-handoff.md，")
        print("         实现 roadmap 里的第一个垂直切片。")
    else:
        print("Next steps:")
        print("  1. Stage 1 (Claude planning):")
        print(f"     - cd \"{project}\"")
        print("     - Start interactive Claude Code: claude")
        print("     - In the Claude Code session, say:")
        print(
            "         Read docs/claude/00-prd-spec-prompt.md and run Stage 1."
        )
        print(
            "     Note: do NOT use `claude -p` headless mode — Stage 1 needs"
        )
        print("     the interactive questionnaire.")
        print(
            "     To pick a model, use /model in the session "
            "(e.g. claude-opus-4-7[1m])."
        )
        print()
        print("  2. Stage 2 (Codex implementation): switch back to Codex in")
        print("     this project, then say:")
        print(
            "         Read docs/codex/00-implementation-handoff.md and"
        )
        print(
            "         implement the first vertical slice from the roadmap."
        )


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser() if args.root else default_root()
    developer = args.developer or default_developer()
    project = (root / args.name).resolve()
    language = resolve_language(args.language)

    if is_system_drive(project) and not args.allow_system_drive:
        raise SystemExit(
            f"Refusing to create project on the system drive: {project}\n"
            "Pass --root with a non-system-drive folder, set BIG_PROJECT_ROOT, "
            "or pass --allow-system-drive only if you really mean it."
        )

    project.mkdir(parents=True, exist_ok=True)

    init_git(project)
    trellis_status = init_trellis(project, args, developer)
    written = write_project_files(project, args, language)
    report(project, trellis_status, args, written, language)


if __name__ == "__main__":
    main()
