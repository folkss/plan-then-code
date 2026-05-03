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


def render(template_name: str, variables: dict[str, str]) -> str:
    template_path = TEMPLATES_DIR / f"{template_name}.md"
    if not template_path.exists():
        raise SystemExit(f"Template not found: {template_path}")
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


def write_project_files(project: Path, args: argparse.Namespace) -> dict[str, bool]:
    today = _dt.date.today().isoformat()
    variables = {
        "name": args.name,
        "brief": (args.brief.strip() or "TBD. Replace this with the project goal."),
        "developer": args.developer or default_developer(),
        "date": today,
    }

    written: dict[str, bool] = {}

    project_brief = project / "docs" / "PROJECT_BRIEF.md"
    written[str(project_brief)] = write_if_missing(
        project_brief, render("project-brief", variables)
    )

    claude_prompt = project / "docs" / "claude" / "00-prd-spec-prompt.md"
    written[str(claude_prompt)] = write_if_missing(
        claude_prompt, render("claude-planning-prompt", variables)
    )

    codex_handoff = project / "docs" / "codex" / "00-implementation-handoff.md"
    written[str(codex_handoff)] = write_if_missing(
        codex_handoff, render("codex-handoff", variables)
    )

    tasks_dir = project / ".trellis" / "tasks"
    if tasks_dir.exists():
        launch_task = tasks_dir / "000-project-launch.md"
        written[str(launch_task)] = write_if_missing(
            launch_task, render("launch-task", variables)
        )

    return written


def report(project: Path, trellis_status: str | None, args: argparse.Namespace,
           written: dict[str, bool]) -> None:
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
    print(f"  Claude:  {'detected' if (project / '.claude').exists() else 'not present'}")
    print(f"  Codex:   {'detected' if (project / '.codex').exists() else 'not present'}")
    print()
    print("Files:")
    for path, was_new in written.items():
        marker = "+" if was_new else "·"
        print(f"  {marker} {path}")
    print()
    print("Next steps:")
    print("  1. Stage 1 (Claude planning):")
    print("     PowerShell: Get-Content .\\docs\\claude\\00-prd-spec-prompt.md -Raw |"
          " claude -p --model opus --permission-mode acceptEdits")
    print("     Bash:       cat docs/claude/00-prd-spec-prompt.md |"
          " claude -p --model opus --permission-mode acceptEdits")
    print("  2. Stage 2 (Codex implementation): ask Codex to read"
          " docs/codex/00-implementation-handoff.md and implement the first slice.")


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser() if args.root else default_root()
    developer = args.developer or default_developer()
    project = (root / args.name).resolve()

    if is_system_drive(project) and not args.allow_system_drive:
        raise SystemExit(
            f"Refusing to create project on the system drive: {project}\n"
            "Pass --root with a non-system-drive folder, set BIG_PROJECT_ROOT, "
            "or pass --allow-system-drive only if you really mean it."
        )

    project.mkdir(parents=True, exist_ok=True)

    init_git(project)
    trellis_status = init_trellis(project, args, developer)
    written = write_project_files(project, args)
    report(project, trellis_status, args, written)


if __name__ == "__main__":
    main()
