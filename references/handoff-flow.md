# Handoff Flow Detail

Load this file on demand when generating Stage 1 documents. The main
`SKILL.md` only lists the document set; the full per-document field
checklists live here so the skill stays compact.

## docs/PROJECT_BRIEF.md (11 sections)

- project name
- one-sentence purpose
- target users
- user scenarios
- MVP scope
- explicit out-of-scope
- technology preferences
- deployment target
- known constraints
- open questions
- assumptions to verify

## docs/REQUIREMENTS_QUESTIONNAIRE.md

See SKILL.md "Stage 1 — Requirements Questionnaire" for the rules. Group
by module, four fields per question (question / type / why / default),
counts scaled by project size (30-60 / 80-150 / 150-500).

## docs/REQUIREMENTS_ANSWERS.md

Mirror the questionnaire structure. Mark each answer as either
`(user-confirmed)` or `(default assumption)`. Do not silently fill in
defaults — the marker is what lets Codex know which decisions are weak.

## docs/PRD.md (19 sections)

1. project background
2. product goals
3. target users
4. MVP scope
5. in scope
6. out of scope (strict)
7. user stories
8. main flows
9. page / interface list
10. functional modules
11. business rules
12. data objects
13. rough API list
14. AI / LLM workflow (when relevant)
15. analytics / dashboard metrics (when relevant)
16. non-functional requirements
17. acceptance criteria
18. risks and fallback strategy
19. future roadmap

Each functional module includes:

- description
- user story
- inputs
- outputs
- business rules
- edge cases
- acceptance criteria

## .trellis/spec/* (10 candidate files, generate only what the project needs)

- `architecture/architecture-spec.md`
- `frontend/frontend-spec.md`
- `backend/backend-spec.md`
- `database/database-spec.md`
- `api/api-spec.md`
- `llm/llm-spec.md`
- `prompt/prompt-spec.md`
- `testing/testing-spec.md`
- `deployment/deployment-spec.md`
- `security/security-spec.md`

Each spec includes:

- scope
- directory structure conventions
- naming rules
- data structures
- API contracts
- error handling
- validation rules
- logging rules
- edge cases
- forbidden patterns
- examples or pseudocode
- verification commands
- acceptance criteria

## docs/ROADMAP.md (8-20 tasks, 12 fields each)

- task ID
- title
- goal
- dependencies
- scope
- out of scope
- likely files / directories
- implementation steps
- acceptance criteria
- verification commands
- risks
- rollback plan

Prefer vertical slices over horizontal refactors.

Good task: `Task 06: Knowledge-base retrieval plus LLM answer generation`

Bad task: `Build all backend and frontend.`

## Bad spec vs Good spec

The bar for a spec is concreteness. A spec must be enforceable mechanically.

Bad spec:

```text
Code should be clean and maintainable.
```

Good spec:

```text
All API responses use the envelope:

{
  "success": boolean,
  "data": object | null,
  "error": {
    "code": string,
    "message": string
  } | null
}

Validation errors return success=false with error.code in the set
{INVALID_INPUT, MISSING_FIELD, OUT_OF_RANGE}. HTTP status follows the
error code (400 for validation, 401 for auth, 5xx only for server faults).
```

Bad spec:

```text
The retrieval should be fast.
```

Good spec:

```text
Retrieval p95 latency under 800ms for queries up to 32 tokens against an
index of <= 1M chunks. Cache hits must round-trip under 80ms. On cache
miss, fall back to the cold-path within 1.5s; beyond 1.5s respond with
{success:false, error:{code:"RETRIEVAL_TIMEOUT"}}.
```

When in doubt, write a spec rule that a test could check.

## .trellis/tasks/001-implementation-kickoff.md

- task ID and title
- goal
- scope (paths / modules)
- out of scope
- files likely to change
- implementation steps (smallest runnable slice first)
- acceptance criteria
- verification commands
- risks and rollback
- estimated effort (optional)

## docs/codex/00-implementation-handoff.md

The skill ships a default template for this file. Adjust it for the
specific project: update the read-first list, name the verification
command for the first slice, and link to the task.
