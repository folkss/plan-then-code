# 更新日志

所有值得记录的项目改动都写在这里。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/spec/v2.0.0.html)。

英文版镜像见 [CHANGELOG.md](./CHANGELOG.md)。

## [0.2.0] - 2026-05-04

### 变更（不向后兼容）

- **Stage 1 改为在交互式 `claude` REPL 里跑，不再是 `claude -p`
  headless 模式。** 旧设计把规划 prompt 用管道喂给 `claude -p`，
  管道这头没有用户，结构化问卷（这套工作流的核心价值）每一题都
  被默默用 `(default assumption)` 填掉。这次改动后，bootstrap
  输出、`SKILL.md`、两份 README、references 全部统一指引用户
  在 Claude Code 交互式会话里跑。
- **去掉硬编码的 `--model opus` 建议。** 改成在会话里用 `/model`
  切换；文档建议优先用 Opus 级 + 1M context（比如
  `claude-opus-4-7[1m]`），但不再写死具体型号。

### 新增

- `bootstrap.py --language auto|en|zh-CN` 参数。`auto`（默认）依次
  看 `BIG_PROJECT_LANGUAGE`、`LANG`、`LC_ALL`、`LANGUAGE` 环境
  变量和系统 locale；中文 locale 映射到 `zh-CN`，其他映射到
  `en`。
- 模板本地化回退机制。渲染器先试 `<template>.<language>.md`，
  缺失时回退到 `<template>.md`。加新语言就是"再放一个文件"。
- 四份模板的中文版：
  `assets/templates/{project-brief,codex-handoff,launch-task,claude-planning-prompt}.zh-CN.md`。
- "Tiny" 项目档位（10-20 题、6-8 模块），用于单脚本 / smoke
  test / 一次性小工具，和原有的小 / 中 / 大并列。
- bootstrap 报告里的 `Next steps` 块按 language 出中文或英文。

### 修复

- Headless 模式不会再悄无声息地用默认值填完整份问卷。文档现在
  明确拒绝走 headless 路径。

## [0.1.0] - 首发版本

- Claude → Codex 两阶段工作流，Trellis 负责项目记忆。
- 跨平台 Python bootstrap 脚本（`scripts/bootstrap.py`）。
- 四份英文模板：project-brief、claude-planning-prompt、
  codex-handoff、launch-task。
- `SKILL.md`（英文契约）、README、中文阅读版镜像。

[0.2.0]: https://github.com/folkss/plan-then-code/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/folkss/plan-then-code/releases/tag/v0.1.0
