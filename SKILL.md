---
name: big-project-workflow
description: "Two-stage AI coding workflow controller for medium and large projects: Claude Code CLI does product planning (project brief, requirements questionnaire, PRD, specs, roadmap), Codex implements vertical slices from those documents. Trellis owns specs/tasks/workspace memory; this skill orchestrates the Claude→Codex handoff and enforces safety boundaries. Use when the user mentions 大项目工作流, large/medium project, new SaaS, multi-module system, requirements questionnaire, Claude Code CLI planning, Codex implementation handoff, Trellis bootstrap, non-system-drive project, or vertical slice. Skip for: single-file edits, casual Q&A, copy polish, throwaway prototypes, or tasks the user explicitly wants done fast without process."
---

# Big Project Workflow

A thin orchestrator on top of [Trellis](https://github.com/mindfold-ai/trellis).
Trellis owns specs, tasks, workspace journals, and the workflow lifecycle.
This skill adds: non-system-drive bootstrap, a structured Claude→Codex
handoff (with a real requirements questionnaire), and safety boundaries.
Detailed checklists live in `references/` and load on demand.

## Tool Contract

| Tool | Owns |
|------|------|
| **Trellis** | `.trellis/spec/`, `.trellis/tasks/`, `.trellis/workspace/`, `.trellis/workflow.md`, SessionStart hook |
| **Claude Code CLI** | Stage 1 — project brief, requirements questionnaire & answers, PRD, specs, roadmap, kickoff task |
| **Codex** | Stage 2 — implementation, verification, debugging, doc updates, review |

## Use / Do Not Use

Use for new products, multi-module apps, projects involving
database/API/LLM/deployment decisions, large refactors that need scope and
verification, and any workflow where Claude writes documents first and Codex
implements afterward.

Do not use for tiny one-file fixes, casual Q&A, copy polish, or quick
throwaway prototypes when the user explicitly wants speed over process.

## Phase 0: Inspect Current State (existing repo)

If the user invokes the skill in an existing repository, inspect before
creating or editing any workflow document. Read these anchors when present:

- `AGENTS.md`, `README.md`
- package files (`package.json`, `pyproject.toml`, `requirements.txt`, ...)
- `docs/`
- `.trellis/`, `.trellis/workflow.md`, `.trellis/spec/`, `.trellis/tasks/`,
  `.trellis/workspace/`
- `.claude/`, `.codex/`
- tests, `.env.example`

Then report:

- current repository state,
- whether Trellis exists,
- whether PRD/spec/roadmap exist,
- whether tests and verification commands exist,
- which phase should run next.

Routing: if key Stage 1 documents are missing, run Stage 1. If they are
present and a kickoff task exists, run Stage 2. If only verification is
missing, add a smoke check first.

## Bootstrap A New Project

For a new project, prefer a **non-system drive**. On Windows the script
refuses system-drive targets unless `--allow-system-drive` is passed.

PowerShell:

```powershell
$SkillRoot = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME "skills/big-project-workflow"
} else {
  Join-Path $HOME ".codex/skills/big-project-workflow"
}

python (Join-Path $SkillRoot "scripts/bootstrap.py") `
  --root "<non-system-drive>/codex-projects" `
  --name "<project-slug>" `
  --developer "<developer-name>" `
  --brief "One paragraph describing the project goal" `
  --trellis-version latest
```

Bash / zsh:

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/big-project-workflow"

python3 "$SKILL_ROOT/scripts/bootstrap.py" \
  --root "$HOME/codex-projects" \
  --name "<project-slug>" \
  --developer "<developer-name>" \
  --brief "One paragraph describing the project goal" \
  --trellis-version latest
```

The script creates the project folder, runs `git init`, runs
`trellis init --codex -u <developer> -y` (default), and renders the four
templates from `assets/templates/` into the project. If `trellis` is not
on `PATH`, the script prints the install command and exits cleanly — it
does **not** silently install npm packages.

### Output language

Pass `--language en` or `--language zh-CN` to control the language of the
rendered templates and the bootstrap `Next steps` hint. Default is
`auto`, which checks `BIG_PROJECT_LANGUAGE`, then `LANG` / `LC_ALL` /
`LANGUAGE` env vars, then the system locale, mapping any Chinese locale
to `zh-CN` and everything else to `en`. To add a new language, drop a
`<template>.<lang>.md` file next to the existing English template; the
renderer prefers the localized variant when present and falls back to
English otherwise.

## Stage 1: Claude Plans

Run from the project root inside an **interactive** Claude Code session.
Do not use `claude -p` (headless / print mode) — Stage 1 produces a
structured questionnaire that needs a human to answer it. Headless mode
silently fills every answer with `(default assumption)`, defeating the
core value of this workflow.

PowerShell:

```powershell
cd <project-path>
claude
```

Bash / zsh:

```bash
cd <project-path>
claude
```

In the Claude Code session, say:

> Read `docs/claude/00-prd-spec-prompt.md` and run Stage 1.

Claude inspects the project, asks you to confirm scope and the
questionnaire size, runs the questionnaire interactively, and only
then writes the PRD / specs / roadmap / kickoff task / handoff doc.

To pick a planning model, use `/model` inside the session. Prefer
Opus-class with 1M context (e.g. `claude-opus-4-7[1m]`); the exact
identifier changes over time, and the bundled prompt does not pin one.

Claude writes or updates the Stage 1 document set:

- `docs/PROJECT_BRIEF.md`
- `docs/REQUIREMENTS_QUESTIONNAIRE.md`
- `docs/REQUIREMENTS_ANSWERS.md`
- `docs/PRD.md`
- `docs/ROADMAP.md`
- `.trellis/spec/*` (only the tiers the project actually needs)
- `.trellis/tasks/001-implementation-kickoff.md`
- `docs/codex/00-implementation-handoff.md`

Detailed per-document field lists are in `references/handoff-flow.md` —
load on demand, do not memorize.

### Stage 1 — Requirements Questionnaire (THE core value-add)

Before writing the PRD, generate a structured questionnaire. This is the
single largest reason this workflow outperforms ad-hoc prompting.

- Question count by project size:
  - **Tiny project** (single script, smoke test, throwaway tool):
    10-20 questions
  - **Small project**: 30-60 questions
  - **Medium project**: 80-150 questions
  - **Large project**: 150-500 questions
- Pick the band from the brief; if unsure, ask the user before generating.
- Group by module.
- Each question carries four fields: **question**, **type**
  (single-choice / multi-choice / open / boundary condition / acceptance
  criterion), **why it matters**, **default if user skips**.
- Cover, when relevant: target users, roles & permissions, core user
  journeys, pages/interfaces, data objects, business rules, edge cases,
  admin/backoffice, API design, database design, AI/LLM integration,
  prompt & fallback rules, logging & analytics, security & privacy,
  testing, deployment, out-of-scope boundaries.

After the user answers (or chooses to skip), write
`docs/REQUIREMENTS_ANSWERS.md`. Mark each defaulted item with
`(default assumption)` so Codex can see where the gaps are.

Claude does not implement product code in Stage 1 unless the user
explicitly asks.

## Stage 2: Codex Implements

After Claude finishes, ask Codex:

```text
Read docs/codex/00-implementation-handoff.md and implement the first
vertical slice from the generated roadmap.
```

Codex follows the handoff doc:

1. Read context (Trellis workflow, PRD, roadmap, requirements answers,
   kickoff task).
2. Output a `## Task Plan` block (goal / scope / out-of-scope / files /
   risks / verification / acceptance criteria) **before** editing code.
3. For greenfield projects, build the **smallest runnable vertical slice**
   first — request → handler → DB or LLM → response → assertion — before
   layering on features.
4. Implement one focused task. Do not absorb future-roadmap work.
5. Run verification (`npm run lint/typecheck/test/build`, `pytest`,
   `ruff check .`, `mypy .`, or whatever the project ships). Fix in
   scope; report unrelated failures separately.
6. Summarize: what changed, files changed, acceptance status, verification
   results, known issues, next task.

## Review Mode

When the user asks for a review (rather than an implementation), do not
implement first. Read PRD, specs, the diff, and verification output;
lead with findings by severity.

Output structure (full template in `references/safety-rules.md`):

```markdown
## Review Result
Status: Pass / Pass with concerns / Fail

## Critical / Major / Minor issues
## Scope violations
## Missing acceptance criteria
## Verification (command + result)
## Recommended fix order
```

If the diff lacks tests, the best status is "Pass with concerns" with
the missing verification flagged under Major. Do not silently apply
fixes during review unless the user requests it.

## Hard Rules

### Do Not Code Too Early

For medium or large projects, do not implement product code until these
exist or are explicitly substituted by equivalent existing files:

- Project Brief
- Requirements Answers (or confirmed default assumptions)
- PRD
- Technical Specs
- Roadmap or task list
- Acceptance Criteria
- Verification Commands

Exceptions:

- the user explicitly requests a throwaway prototype,
- the task is a small independent edit,
- the project already has equivalent docs.

### Safety Boundaries

Before important changes, run `git status`. Prefer a feature branch for
non-trivial work. Do **not**:

- run destructive commands without explicit approval,
- delete user files unless the task requires it,
- edit outside the current repo unless explicitly asked,
- commit secrets or hardcode API keys,
- edit `.env` (create `.env.example` instead),
- add large dependencies without justification,
- delete tests or weaken assertions to pass checks.

For shareable files, use placeholders (`<project-root>`,
`<developer-name>`, `<non-system-drive>`) instead of personal paths or
usernames. Full discipline lives in `references/safety-rules.md`.

### Control Scope

One task at a time. Do not turn one task into a project-wide rewrite
unless the user approves. Do not implement future-roadmap features
inside the current task.

### Don't Block On Assumptions

If an answer is missing, draft an explicit assumption and continue. Stop
only when the missing answer affects safety, cost, legal risk, or
irreversible architecture.

## Optional References

Load these only when the situation calls for them:

- `references/handoff-flow.md` — full per-document field checklists for
  Project Brief / PRD / specs / roadmap, plus Bad/Good spec examples.
- `references/safety-rules.md` — extended safety, Done Checklist, Review
  Mode template.
- `references/llm-spec-checklist.md` — LLM project checklist (provider
  abstraction, prompt templates, guardrails, evals, tests).
- `references/SKILL.zh-CN.md` — Chinese reading version. Codex loads this
  English file as the contract; the Chinese file is for humans.

## Bundled Resources

- `scripts/bootstrap.py` — cross-platform project bootstrap.
- `assets/templates/` — Markdown templates the bootstrap script renders.
- `agents/openai.yaml` — UI metadata for Codex skill chips.

## Publish Safety Gate

Before publishing this skill repository:

- scan for personal absolute paths, local usernames, machine-specific
  tool directories, tokens, API keys, and private project names,
- keep examples generic and replace user-specific values with placeholders,
- ensure `SKILL.md` contains the complete operational workflow (no hidden
  instructions in references),
- keep scripts parameterized via CLI arguments and environment variables,
- run a smoke bootstrap in a temp folder and remove only the verified
  temp folder afterward.
