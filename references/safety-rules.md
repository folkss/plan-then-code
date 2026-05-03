# Safety Rules And Done Checklist

Load this file on demand when executing a non-trivial task or when the
user asks for a review. The main `SKILL.md` only lists the hardest
prohibitions; the full discipline lives here.

## Define Done For Every Task

Every implementation task should declare, before code is written:

- goal
- scope
- out of scope
- files likely to change
- acceptance criteria
- verification commands
- risks
- rollback plan

If a task lacks any of these, derive them or stop and ask.

## Verifiable Progress

Every implementation task must have a mechanical verification path. At
least one of:

- lint
- typecheck
- unit tests
- integration tests
- e2e tests
- build
- smoke test
- custom scripts
- API contract tests

If the project has no verification at all, the first engineering task is
to add a minimal smoke check or test harness — do not skip this.

## Safety Boundaries (full)

Before important changes:

- Run `git status`. Stash or commit unrelated changes first.
- Prefer a feature branch for non-trivial work.
- Do not run destructive commands without explicit user approval
  (e.g. `git reset --hard`, `rm -rf`, `DROP TABLE`).
- Do not delete user files unless the task requires it.
- Do not edit outside the current repository unless explicitly asked.
- Do not commit secrets. Do not hardcode API keys or tokens.
- Do not edit `.env`. Create or update `.env.example` instead.
- Do not add large dependencies without justification.
- Do not delete tests or weaken assertions to pass checks.
- Do not bypass typecheck / lint / build.
- Do not write personal absolute paths, local usernames, or private
  project names into shareable files. Use placeholders such as
  `<project-root>`, `<developer-name>`, `<non-system-drive>`.

## Done Checklist (per task)

```markdown
- [ ] PRD acceptance criteria satisfied
- [ ] Relevant specs followed
- [ ] Lint passed
- [ ] Typecheck passed
- [ ] Tests passed
- [ ] Build passed
- [ ] Manual smoke test completed when applicable
- [ ] No unrelated files changed
- [ ] No secrets committed
- [ ] Docs updated when needed
```

Explain any unchecked item. A task is not "done" because code was
written; it is done only when verification has passed (or its failure is
clearly explained), scope was respected, and durable lessons were
captured.

## Review Mode

When the user asks for a review (rather than an implementation), do not
implement first. Read the PRD, the relevant specs, the diff, and the
verification result. Lead with findings by severity.

Output format:

```markdown
## Review Result

Status: Pass / Pass with concerns / Fail

## Critical issues
- ...

## Major issues
- ...

## Minor issues
- ...

## Scope violations
- ...

## Missing acceptance criteria
- ...

## Verification
- Command:
- Result:

## Recommended fix order
1. ...
2. ...
3. ...
```

If the diff lacks tests, mark it as "Pass with concerns" at best, and
list the missing verification under Major issues. Do not silently fix
problems during review — reviews are advisory unless the user asks you
to apply the fixes.

## Spec / Journal Updates (when applicable)

After tested work, capture **durable** knowledge. Only put reusable
rules into specs. Do not pollute shared specs with one-off task details.

If the project uses Trellis, the canonical locations are:

- `.trellis/spec/` for reusable engineering rules
- `.trellis/workspace/<developer>/` for per-developer journals

The skill does not prescribe a journal template — defer to Trellis's
`/trellis-record-session` flow. If that is unavailable, a minimal
journal entry covers: date, task, goal, decisions, implementation
summary, verification, problems, reusable lessons, next task.
