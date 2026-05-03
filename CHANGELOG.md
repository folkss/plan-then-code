# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

A Chinese mirror of this file is at [CHANGELOG.zh-CN.md](./CHANGELOG.zh-CN.md).

## [0.3.0] - 2026-05-04

### Added

- **Hard Rule: Stage 1 Belongs To Claude (Codex Must Refuse).** New
  section in `SKILL.md` (and the Chinese mirror) listing the seven
  Stage 1 documents Codex must never author or refine, plus a verbatim
  refuse template Codex returns when the user asks it to "test the
  workflow end-to-end", "fill the questionnaire with defaults",
  "Claude isn't available so just do it", or any equivalent.
- **Stage 1 Completeness Gate** in
  `assets/templates/codex-handoff.md` (and the Chinese variant). Five
  checks Codex runs before starting Stage 2 — file existence, plus a
  hard requirement that `REQUIREMENTS_ANSWERS.md` contains at least
  one non-`(default assumption)` line. Failing any check refuses the
  Stage 2 start and hands the user back to interactive Claude Code.

### Fixed

- `bootstrap.py` report: the misleading `Claude: detected / not
  present` line (which actually checked for a `.claude/` directory in
  the project, not the `claude` CLI on PATH) is split into two clear
  rows: `Claude CLI: <path or NOT on PATH>` and `.claude/ dir:
  present/absent`. This removes a false signal that previously let
  Codex justify self-filling Stage 1 with "Claude isn't available."

### Why this version exists

Two prior smoke-test runs showed that even after switching the SKILL
to interactive-Claude instructions, Codex still bypassed Stage 1 and
self-filled the questionnaire with all-default answers, then went on
to ship Stage 2. The instructions told Claude how to behave; this
release adds the missing piece — instructions that tell **Codex** to
refuse Stage 1 work outright and a programmatic gate Codex hits before
Stage 2.

## [0.2.0] - 2026-05-04

### Changed (BREAKING)

- **Stage 1 now runs in an interactive `claude` REPL, not `claude -p`
  headless mode.** The previous design piped the planning prompt to
  `claude -p`, which has no human on the other end — so the structured
  questionnaire (the workflow's core value-add) silently filled itself
  with `(default assumption)` for every item. After this change, the
  bootstrap output, `SKILL.md`, READMEs, and references all instruct
  the user to open Claude Code interactively.
- **Hardcoded `--model opus` advice removed.** Use `/model` inside the
  Claude session; advisory copy now suggests Opus-class with 1M
  context (e.g. `claude-opus-4-7[1m]`) without pinning a specific
  identifier.

### Added

- `bootstrap.py --language auto|en|zh-CN` flag. `auto` (default)
  checks `BIG_PROJECT_LANGUAGE`, `LANG`, `LC_ALL`, `LANGUAGE`, then
  the system locale; Chinese locales map to `zh-CN`, everything else
  to `en`.
- Localized template fallback. The renderer tries
  `<template>.<language>.md` first and falls back to
  `<template>.md`. Adding a new language is just "drop another file."
- Chinese variants of the four bundled templates:
  `assets/templates/{project-brief,codex-handoff,launch-task,claude-planning-prompt}.zh-CN.md`.
- "Tiny" project tier (10-20 questions, 6-8 modules) for
  single-script / smoke-test / throwaway-tool projects, alongside the
  existing small / medium / large tiers.
- Localized `Next steps` block in the bootstrap report (Chinese when
  language resolves to `zh-CN`, English otherwise).

### Fixed

- Headless-mode workflow no longer silently default-fills the
  questionnaire with no user input. The instructions now refuse that
  path explicitly.

## [0.1.0] - Initial release

- Two-stage Claude → Codex workflow with Trellis-backed memory.
- Cross-platform Python bootstrap script (`scripts/bootstrap.py`).
- Four English templates: project-brief, claude-planning-prompt,
  codex-handoff, launch-task.
- `SKILL.md` (English contract), README, Chinese reading mirrors.

[0.3.0]: https://github.com/folkss/plan-then-code/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/folkss/plan-then-code/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/folkss/plan-then-code/releases/tag/v0.1.0
