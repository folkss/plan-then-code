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
counts scaled by project size:

- Tiny (single script, smoke test, throwaway tool): 10-20 questions.
  6-8 modules is usually enough — drop irrelevant tiers (admin, RBAC,
  API design, DB design) when the project does not have one.
- Small: 30-60 questions
- Medium: 80-150 questions
- Large: 150-500 questions

Output language follows the project's bootstrap-time `--language`
setting (default auto-detects from system locale). Code identifiers,
HTTP method names, and other language-agnostic tokens stay English even
in localized docs.

## docs/REQUIREMENTS_ANSWERS.md

Mirror the questionnaire structure. Mark each answer as either
`(user-confirmed)` or `(default assumption)`. Do not silently fill in
defaults — the marker is what lets Codex know which decisions are weak.

## docs/PRD.md (20 sections)

1. project background
2. product goals
3. target users
4. **project mode** (single-shot or iterative — locked from
   `REQUIREMENTS_ANSWERS.md` Q0; controls sections 5 / 6 / 20)
5. **scope** (single-shot: all features the user wants; iterative: v1
   features only)
6. in scope (concrete, exhaustive list within "scope")
7. out of scope (strict; items NEVER to be done. In iterative mode,
   "deferred for later" goes to section 20, not here)
8. user stories
9. main flows
10. page / interface list
11. functional modules
12. business rules
13. data objects
14. rough API list
15. AI / LLM workflow (when relevant)
16. analytics / dashboard metrics (when relevant)
17. non-functional requirements
18. acceptance criteria
19. risks and fallback strategy
20. future roadmap (**iterative mode only** — list deferred features.
    In single-shot mode, omit this section or write "N/A — single-shot
    project")

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

## docs/ROADMAP.md (vertical-slice tasks, 12 fields each)

Task count depends on Project Mode (locked in `REQUIREMENTS_ANSWERS.md`
Q0):

- **single-shot**: tasks must cover *every* feature the user asked for.
  Task count is whatever the project needs — typical 8-20, tiny
  projects can be 3-8.
- **iterative**: tasks cover v1 only. Future-roadmap items have no
  task entries here. Typical 8-20.

Each task carries:

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
