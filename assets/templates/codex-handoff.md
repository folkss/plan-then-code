# Codex Implementation Handoff

After Claude finishes Stage 1 planning, Codex reads from these files (in
order) before touching code:

1. `PROJECT_BRIEF.md`, `AGENTS.md`
2. `.trellis/workflow.md`, relevant `.trellis/spec/*`
3. `docs/PROJECT_BRIEF.md`
4. `docs/REQUIREMENTS_ANSWERS.md` — note `(default assumption)` markers
5. `docs/PRD.md`
6. `docs/ROADMAP.md`
7. `.trellis/tasks/001-implementation-kickoff.md`

## Default Execution

Start with `.trellis/tasks/001-implementation-kickoff.md` and the first
vertical slice from `docs/ROADMAP.md`. Inspect the repo, confirm the generated
docs are coherent, then implement the smallest runnable scaffold.

## Before Editing Any Code: Output A Task Plan

```markdown
## Task Plan
- Task:
- Goal:
- Scope:
- Out of Scope:
- Files to inspect:
- Files likely to change:
- Risks:
- Verification commands:
- Acceptance criteria:
```

## Greenfield Rule

For a brand-new project, build the **smallest runnable vertical slice**
before expanding features. Hello-world path through the stack first
(request → handler → DB or LLM → response → assertion), then layer on.
Do not try to ship many features in the first task.

## Implementation Loop

1. Inspect the relevant files.
2. Implement one focused task.
3. Run verification.
4. Fix failures within scope. If a failure is unrelated, report it
   separately rather than fixing it inline.
5. Summarize: what changed, files changed, acceptance status,
   verification results, known issues, next task.

## Verification Commands Cookbook

Common Node:

```bash
npm run lint
npm run typecheck
npm run test
npm run build
```

Common Python:

```bash
pytest
ruff check .
mypy .
```

If commands are unknown, inspect package scripts (`package.json`,
`pyproject.toml`, `Makefile`) and infer. If a verification command is
missing entirely, add a minimal smoke check as part of the task.

## Boundary Reminders

- One task at a time. Do not turn a task into a project-wide rewrite.
- Do not implement future-roadmap features inside the current task.
- Do not delete tests or weaken assertions to pass checks.
- Do not commit secrets. Do not edit `.env`; create `.env.example` instead.
- Stay inside the repo unless the user explicitly requests otherwise.

For the full safety + done checklist, load `references/safety-rules.md`
on demand. If the user asks for a code review instead of an
implementation, switch to Review Mode (also in `references/safety-rules.md`)
and do not implement first.

## Project: {{name}}
