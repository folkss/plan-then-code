# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

A Chinese mirror of this file is at [CHANGELOG.zh-CN.md](./CHANGELOG.zh-CN.md).

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

[0.2.0]: https://github.com/folkss/plan-then-code/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/folkss/plan-then-code/releases/tag/v0.1.0
