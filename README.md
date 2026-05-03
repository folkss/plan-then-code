# Big Project Workflow Skill

**English** | [简体中文](./README.zh-CN.md)

A two-stage AI coding workflow for medium and large projects:
**Claude Code CLI plans, Codex implements, [Trellis](https://github.com/mindfold-ai/trellis)
remembers.** Inspired by a developer's post about a successful
Opus + Codex + Trellis run (the original thread is gone), packaged as a
portable [OpenAI Codex Skill](https://developers.openai.com/codex/skills).

The whole operational contract lives in [`SKILL.md`](./SKILL.md). This
README is for the developer who installs the skill.

## Why this skill

- **Two-stage handoff.** Claude writes Project Brief, requirements
  questionnaire (30-500 questions), PRD, specs, roadmap. Codex reads
  those and implements vertical slices.
- **Real questionnaire, not a wishlist.** The Stage 1 prompt forces a
  structured questionnaire before any PRD writing — by far the biggest
  reason this workflow outperforms ad-hoc prompting.
- **Trellis-native.** No reinventing of `.trellis/spec/` or
  `.trellis/tasks/`; Trellis owns project memory, this skill only
  orchestrates.
- **Safety first.** Refuses system-drive bootstrap on Windows, never commits
  secrets, never weakens tests, uses placeholders in shareable files.
- **Cross-platform.** One Python script, runs on Windows / macOS /
  Linux / WSL.

## Requirements

| Tool | Why |
|------|-----|
| [Codex CLI](https://developers.openai.com/codex/cli/features) | Loads this skill |
| [Claude Code CLI](https://docs.anthropic.com/claude-code) | Stage 1 planning |
| Node.js (LTS) | Trellis runtime |
| [Trellis CLI](https://github.com/mindfold-ai/trellis) | `.trellis/` workspace |
| Python 3.9+ | Bootstrap script |
| Git | Version control |

Install Trellis (pin a version with `--trellis-version` if you want):

```bash
npm install -g @mindfoldhq/trellis@latest
```

If you do not want npm globals on the system drive, configure
`npm config set prefix` to a directory on another drive before
installing.

Enable Codex skill loading per the
[official docs](https://developers.openai.com/codex/skills).

## Install

Clone or download this repository, then copy the folder into your Codex
skills directory:

PowerShell:

```powershell
$SkillRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
Copy-Item -Recurse big-project-workflow-skill (Join-Path $SkillRoot "skills/big-project-workflow")
```

Bash / zsh:

```bash
cp -r big-project-workflow-skill "${CODEX_HOME:-$HOME/.codex}/skills/big-project-workflow"
```

Restart Codex so the skill list refreshes. Trigger it with anything
that mentions a "big project workflow", "PRD", "non-system-drive
project", "Trellis bootstrap", or 大项目工作流.

## Quick Start (3 steps)

### 1. Bootstrap

PowerShell:

```powershell
$SkillRoot = (Join-Path ${env:CODEX_HOME ?? "$HOME/.codex"} "skills/big-project-workflow")

python (Join-Path $SkillRoot "scripts/bootstrap.py") `
  --root "D:\codex-projects" `
  --name "my-project" `
  --developer "<your-name>" `
  --brief "One paragraph about the project goal"
```

Bash / zsh:

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/big-project-workflow"

python3 "$SKILL_ROOT/scripts/bootstrap.py" \
  --root "$HOME/codex-projects" \
  --name "my-project" \
  --developer "<your-name>" \
  --brief "One paragraph about the project goal"
```

### 2. Stage 1 — Claude plans

Open the project in **interactive Claude Code** (not `claude -p` headless
mode — Stage 1 needs you to answer the structured questionnaire):

```powershell
cd D:\codex-projects\my-project
claude
```

```bash
cd ~/codex-projects/my-project
claude
```

In the Claude Code session, say:

> Read `docs/claude/00-prd-spec-prompt.md` and run Stage 1.

Claude inspects the project, confirms the questionnaire size (tiny /
small / medium / large), runs the questionnaire interactively, captures
your answers, then writes PRD / specs / roadmap / kickoff task / Codex
handoff doc. To pick a planning model use `/model` inside the session;
prefer Opus-class with 1M context (e.g. `claude-opus-4-7[1m]`).

### 3. Stage 2 — Codex implements

Open Codex in the project, then ask:

> Read `docs/codex/00-implementation-handoff.md` and implement the
> first vertical slice from the generated roadmap.

Codex outputs a Task Plan, builds the smallest runnable slice, runs
verification, and reports results.

## Bootstrap script flags

| Flag | Default | Notes |
|------|---------|-------|
| `--name` | required | Project folder name |
| `--root` | `BIG_PROJECT_ROOT` env, first non-system drive on Windows, else `~/codex-projects` | Parent folder |
| `--developer` | `TRELLIS_DEVELOPER` env or OS user | Used by Trellis |
| `--brief` | empty | One-paragraph goal embedded in templates |
| `--trellis-version` | `latest` | Used in the printed install hint when Trellis is missing |
| `--platforms` | `codex` | Comma-separated; Trellis 0.4+ generates `.claude/` by default |
| `--trellis-bin` | auto-detect | Explicit path to the trellis binary |
| `--allow-system-drive` | off | Required on Windows when targeting the system drive (e.g. `C:`) |
| `--skip-trellis` | off | Skip the `trellis init` step |
| `--language` | `auto` | Output language for templates and next-steps. `auto` checks `BIG_PROJECT_LANGUAGE` / `LANG` / `LC_ALL` / system locale; Chinese locales map to `zh-CN`, others to `en`. Pass `en` or `zh-CN` to force. |

## Troubleshooting

**`trellis` not found.** The script prints the install command and
exits cleanly. Run `npm install -g @mindfoldhq/trellis@<version>` (or
your preferred version) and re-run the script.

**Project went to the system drive by accident.** The script refuses
system-drive targets on Windows unless `--allow-system-drive` is passed.
Set `BIG_PROJECT_ROOT` to your preferred drive once and forget it.

**`claude` not found.** Install [Claude Code CLI](https://docs.anthropic.com/claude-code).
Stage 1 requires the **interactive** `claude` REPL (not `claude -p`) so
the questionnaire phase has a human to talk to. If you cannot install
Claude Code locally, paste `docs/claude/00-prd-spec-prompt.md` into any
interactive Claude session and follow the same flow.

**Want a different Trellis platform combination.** Use
`--platforms codex,claude,cursor` etc. See
[Trellis docs](https://docs.trytrellis.app/) for the supported flags.

## File map

```
big-project-workflow/
├── SKILL.md                         # The Codex contract (load this)
├── README.md                        # You are here (English)
├── README.zh-CN.md                  # 中文版 README
├── LICENSE                          # MIT
├── agents/openai.yaml               # UI metadata for the Codex skill chip
├── scripts/bootstrap.py             # Cross-platform project bootstrap
├── assets/templates/                # 4 markdown templates the bootstrap renders
└── references/                      # Loaded on demand by Codex / Claude
    ├── handoff-flow.md              # Per-document field checklists + spec examples
    ├── safety-rules.md              # Extended safety + Review Mode template
    ├── llm-spec-checklist.md        # LLM project-specific checklist
    └── SKILL.zh-CN.md               # Chinese reading version of SKILL.md
```

## Publish safety

If you fork or republish this skill, follow the Publish Safety Gate at
the bottom of `SKILL.md`: scan for personal absolute paths, local
usernames, machine-specific tool directories, tokens, API keys, and
private project names. Replace any user-specific value with a
placeholder.

## License

MIT — see [LICENSE](./LICENSE).

## Credits

- Workflow distilled from a developer's shared post about a successful
  Opus + Codex + Trellis run.
- Trellis by [mindfold-ai](https://github.com/mindfold-ai/trellis).
- Codex Skills format by [OpenAI](https://developers.openai.com/codex/skills).
