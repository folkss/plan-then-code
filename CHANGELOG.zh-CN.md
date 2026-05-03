# 更新日志

所有值得记录的项目改动都写在这里。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/spec/v2.0.0.html)。

英文版镜像见 [CHANGELOG.md](./CHANGELOG.md)。

## [0.3.0] - 2026-05-04

### 新增

- **硬规则：Stage 1 是 Claude 的活，Codex 必须拒写。** `SKILL.md` 和
  中文镜像里加了一节，列出 Codex 严禁编写或细化的七份 Stage 1 文档，
  并给出标准的拒绝回复模板。用户说"帮我把工作流跑通"、"问卷用默认值
  填快点"、"Claude 不在你直接搞" 等情况，Codex 必须按模板拒绝。
- **Stage 1 完整性闸门** 加进了 `assets/templates/codex-handoff.md`
  和中文版。Codex 启动 Stage 2 前跑五项检查 —— 文件存在性，外加一项
  硬约束：`REQUIREMENTS_ANSWERS.md` 里**至少有一条**答案不是
  `(default assumption)`。任意一项失败立即拒绝 Stage 2，把用户交还
  给交互式 Claude Code。

### 修复

- `bootstrap.py` 报告里的 `Claude: detected / not present` 这行容易
  误导（它检测的是项目下的 `.claude/` 目录，**不是** PATH 上的
  `claude` CLI）。现在拆成两行：`Claude CLI: <路径或 NOT on PATH>`
  和 `.claude/ dir: present/absent`。消除了之前让 Codex 拿
  "Claude 不在我自己干" 当借口的误信号。

### 为什么有这个版本

前两轮 smoke test 显示：即使我们把 SKILL 切到交互式 Claude 指引，
Codex 仍然绕过 Stage 1，自填默认答案后径直冲进 Stage 2。之前的指令
只教了 Claude 该怎么做；这一版补上缺的那块 —— 教 **Codex** 必须拒
做 Stage 1，并加一道 Codex 跨入 Stage 2 前必过的程序性闸门。

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

[0.3.0]: https://github.com/folkss/plan-then-code/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/folkss/plan-then-code/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/folkss/plan-then-code/releases/tag/v0.1.0
