# 更新日志

所有值得记录的项目改动都写在这里。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/spec/v2.0.0.html)。

英文版镜像见 [CHANGELOG.md](./CHANGELOG.md)。

## [0.5.0] - 2026-05-05

### 新增

- **可选 Research Gate（接 `codex-autoresearch`）。** `SKILL.md` 和
  中文镜像新增一节，说明 Stage 2 切片开工前何时调用
  `$codex-autoresearch`：陌生 API、认证 / 加密 / 密钥、数据库迁移、
  部署、性能、安全敏感逻辑、LLM provider / tool-use 设计、大依赖升级、
  根因不明的测试失败、或者有明确指标的优化工作。Tiny / 简单切片直接
  跳过。
- **Codex Task Plan 新增 `Research notes:` 字段。**
  `assets/templates/codex-handoff.md` 和中文版的 Task Plan 模板里
  必须填 `Research notes:`：要么指向一次 `codex-autoresearch` 运行，
  要么用一行写清楚为什么不需要 research。
- **README 列出可选依赖。** `README.md` 和 `README.zh-CN.md` 给出
  `$skill-installer install https://github.com/leo-lilinxiao/codex-autoresearch`
  的安装命令，并说明值得用 / 可以跳过的判断标准。

### 为什么有这个版本

Stage 2 涉及陌生领域（认证、第三方 API、性能、LLM provider 行为）的
切片，正式动产线代码前最好先用一次带机械指标的 research loop。
`codex-autoresearch` 本来就为此而生。v0.5.0 把它接成一个显式的 gate，
让 Codex 在难切片上记得用、在简单切片上自觉跳过，避免滥用也避免遗漏。

## [0.4.0] - 2026-05-05

### 新增

- **Project Mode（Q0）。** Stage 1 在生成问卷之前会先问一题：这是
  **single-shot**（一次做完型，全部内容这一轮 ship，没有 v2）还是
  **iterative**（迭代型，多版本，v1 故意做窄）？答案锁定为
  `REQUIREMENTS_ANSWERS.md` 的 Q0，决定后续每一份文档形状。按规模给
  默认：tiny / small → single-shot；medium / large → iterative。改动
  覆盖 `SKILL.md`、中文镜像、两份 `claude-planning-prompt` 模板、
  `references/handoff-flow.md`。

### 变更

- **`PRD.md` § Future Roadmap 仅 iterative 模式有。** Single-shot 模式
  下整段省略（或写 `N/A —— single-shot 项目`）。这消除了之前那种
  "无论项目大小都先切一刀放进 Future Roadmap" 的强迫症，给那些想要
  整个项目一次性做完的用户留出空间。
- **`ROADMAP.md` 任务数由 mode 决定，不是 size。** Single-shot 项目
  的任务覆盖**用户提出的全部功能**（通常 8-20，tiny 项目 3-8）。
  Iterative 项目仍然只覆盖 v1。
- **`PROJECT_BRIEF.md` § "MVP Scope" → § "Scope"**（中英两份模板都改），
  并加注释明确两种模式下含义不同。
- **`PRD.md` § "MVP scope" → § "scope"**，`handoff-flow.md` 字段列表
  现在 20 段（第 4 段是 "project mode"）。
- **Out of Scope 严格指 never-do 项。** Iterative 模式下"以后再做"的
  功能放 Future Roadmap，**不**放 Out of Scope。Single-shot 模式下
  Out of Scope 通常很短甚至为空。

### 为什么有这个版本

之前的设计强迫每个项目都走 MVP / Future Roadmap 切分。对有用户的真实
产品这是对的；但对 smoke test、个人工具、玩具项目，以及一切"这个东西
我整个都要现在做完"的 scope，这套切分制造了人为的截断。Stage 1 现在
先问一题，再据此决定后续规划形状。

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

[0.5.0]: https://github.com/folkss/plan-then-code/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/folkss/plan-then-code/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/folkss/plan-then-code/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/folkss/plan-then-code/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/folkss/plan-then-code/releases/tag/v0.1.0
