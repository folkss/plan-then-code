# Codex Implementation Handoff

## Stage 1 Completeness Gate (run BEFORE anything else)

This is the first thing Codex does in this project. **If any check
below fails, refuse to start implementation** and return the message
in the "Refuse And Hand Back" section. Do not "helpfully" fill in the
missing pieces — Stage 1 belongs to Claude, not Codex (see SKILL.md
Hard Rule "Stage 1 Belongs To Claude").

Checks:

1. `docs/REQUIREMENTS_ANSWERS.md` exists.
2. `docs/REQUIREMENTS_ANSWERS.md` contains **at least one** answer that
   is **not** marked `(default assumption)`. (All-defaults means a real
   user never answered the questionnaire.)
3. `docs/PRD.md` exists and contains more than the bootstrap scaffold
   (look for concrete acceptance criteria, not just TBD lines).
4. `docs/ROADMAP.md` exists and lists at least one concrete vertical
   slice with verification commands.
5. `.trellis/tasks/001-implementation-kickoff.md` exists.

### Refuse And Hand Back

If any check fails, respond with (translate to the user's language):

> Stage 1 is not complete. Specifically, the following checks failed:
>
> - <list which of the 5 checks failed and why>
>
> Stage 1 is interactive Claude Code's job, not mine. To finish it:
>
>     cd <project-path>
>     claude
>
> Then in Claude Code say: *"Read `docs/claude/00-prd-spec-prompt.md`
> and run Stage 1."* Come back to Codex when Stage 1 is genuinely done
> and I'll start the first vertical slice.

Do **not** attempt to author or refine the missing Stage 1 documents
yourself. That is the failure mode this gate exists to prevent.

## Read First (only after the gate passes)

After Claude finishes Stage 1 planning, Codex reads from these files
(in order) before touching code:

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

## Optional Research Gate (before the Task Plan)

Before editing code for each roadmap slice, decide whether this task
needs `codex-autoresearch`.

Use `$codex-autoresearch` when the slice involves unfamiliar third-party
APIs, auth/encryption/secrets, database migrations, deployment,
performance, security-sensitive behavior, LLM provider/tool-use design,
large dependency upgrades, unclear failing tests, or optimization with a
measurable metric. Skip it for straightforward slices where the PRD and
specs are already concrete.

If research is needed:

1. State the narrow research goal and the metric / verification command.
2. Invoke `$codex-autoresearch` (foreground for short runs, background
   for long experiment loops).
3. Read the research result / `autoresearch-results/` summary.
4. Add `Research notes:` to the Task Plan before editing production code.

If research is not needed, write `Research notes: Not needed — <one-line
reason>` in the Task Plan. Do not use research as a way to broaden scope.

## Before Editing Any Code: Output A Task Plan

```markdown
## Task Plan
- Task:
- Goal:
- Scope:
- Out of Scope:
- Files to inspect:
- Files likely to change:
- Research notes:
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
