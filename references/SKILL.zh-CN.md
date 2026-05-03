# 大项目工作流 Skill 中文阅读版

> Codex 加载的契约是 `SKILL.md`（英文）。本文件只是给中文读者用的镜像版，
> 行文比英文 SKILL.md 简短，便于人快速浏览。

## 定位

`big-project-workflow` 是一个 **薄编排层**，跑在 [Trellis](https://github.com/mindfold-ai/trellis)
之上：

- Trellis 负责：`.trellis/spec/`、`.trellis/tasks/`、`.trellis/workspace/`、
  `.trellis/workflow.md`、SessionStart hook。
- 本 skill 负责：非系统盘 bootstrap、Claude→Codex 划交、安全边界。
- 详细 checklist 放 `references/`，按需加载。

## 工具分工

| 工具 | 负责 |
|------|------|
| **Trellis** | 项目记忆（spec / tasks / workspace / workflow） |
| **Claude Code CLI** | Stage 1 — Project Brief、需求问卷与回答、PRD、specs、Roadmap、kickoff |
| **Codex** | Stage 2 — 实现、验证、调试、文档更新、review |

## 适用 / 不适用

适用：新产品、多模块项目、涉及数据库 / API / LLM / 部署的项目、需要 PRD/spec/roadmap 的项目、需要 Claude 先写文档再让 Codex 实现的项目。

不适用：单文件小修、简单问答、文案润色、用户明确要求的一次性快速原型。

## Phase 0：现有项目检查

如果用户在已有 repo 里调用这个 skill，先 inspect：`AGENTS.md`、`README.md`、依赖文件、`docs/`、`.trellis/*`、`.claude/`、`.codex/`、tests、`.env.example`。然后报告：Trellis 是否已有、PRD/spec/roadmap 是否已有、tests 和验证命令是否已有、当前应该跑哪个阶段。

路由：缺关键 Stage 1 文档 → 跑 Stage 1；齐了且有 kickoff → 跑 Stage 2；只缺验证 → 先补 smoke check。

## 初始化项目（Bootstrap）

新项目尽量放在非系统盘。Windows 上脚本默认拒绝系统盘，除非传 `--allow-system-drive`。

PowerShell：

```powershell
$SkillRoot = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME "skills/big-project-workflow"
} else {
  Join-Path $HOME ".codex/skills/big-project-workflow"
}

python (Join-Path $SkillRoot "scripts/bootstrap.py") `
  --root "<非系统盘>/codex-projects" `
  --name "<project-slug>" `
  --developer "<开发者名>" `
  --brief "用一段话描述项目目标" `
  --trellis-version latest
```

Bash：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/big-project-workflow"

python3 "$SKILL_ROOT/scripts/bootstrap.py" \
  --root "$HOME/codex-projects" \
  --name "<project-slug>" \
  --developer "<开发者名>" \
  --brief "用一段话描述项目目标" \
  --trellis-version latest
```

脚本会创建项目目录、`git init`、`trellis init --codex -u <developer> -y`，然后把 `assets/templates/` 里的 4 份模板渲染到项目目录。如果 `trellis` 不在 PATH，脚本会打印安装命令然后干净退出，**不会** 偷偷给你装 npm 包。

### 输出语言

`--language` 控制渲染出来的文档和 next-steps 提示的语言。默认 `auto`：依次看 `BIG_PROJECT_LANGUAGE` / `LANG` / `LC_ALL` / `LANGUAGE` 环境变量和系统 locale，命中中文 locale 就用 `zh-CN`，否则 `en`。可以显式传 `--language en` 或 `--language zh-CN`。要加新语言就在 `assets/templates/` 里放一份 `<template>.<lang>.md`，渲染器会优先用本地化版本，缺失时回退英文。

## Stage 1：Claude 写文档

**在项目根运行交互式 Claude Code**（**不是** `claude -p` 管道模式）：

```powershell
cd <project-path>
claude
```

```bash
cd <project-path>
claude
```

进入 Claude Code 会话后说：

> 读 `docs/claude/00-prd-spec-prompt.md`，按它执行 Stage 1。

为什么必须交互式：Stage 1 的核心是结构化需求问卷，需要人答题。`claude -p` headless 模式没有用户，会把所有题默默用 `(default assumption)` 填掉，整个工作流的核心价值就废了。

要选规划模型，在会话里用 `/model`。优先用 Opus 级 + 1M context（例如 `claude-opus-4-7[1m]`）；具体型号会随时间变，所以 prompt 里没写死。

Claude 写 / 更新：`docs/PROJECT_BRIEF.md`、`docs/REQUIREMENTS_QUESTIONNAIRE.md`、`docs/REQUIREMENTS_ANSWERS.md`、`docs/PRD.md`、`docs/ROADMAP.md`、`.trellis/spec/*`（按需）、`.trellis/tasks/001-implementation-kickoff.md`、`docs/codex/00-implementation-handoff.md`。

每份文档的字段细清单见 `references/handoff-flow.md`，按需加载。

### 需求问卷（Stage 1 的核心增量）

写 PRD 之前必须先生成结构化问卷。这是这套工作流相对裸 Trellis 最大的价值。

- 题量按规模分级：
  - **Tiny**（单脚本、smoke test、一次性小工具）：10-20 题
  - **小项目**：30-60 题
  - **中项目**：80-150 题
  - **大项目**：150-500 题
- 从 brief 推断规模档位；不确定就先问用户再开题。
- 按模块分组。
- 每题四个字段：**问题** / **类型**（单选 / 多选 / 开放 / 边界条件 / 验收标准）/ **为什么重要** / **用户跳过时的默认答案**。
- 必须覆盖：用户、角色权限、核心流程、页面、数据对象、业务规则、边界、admin、API、DB、AI/LLM、prompt fallback、日志分析、安全隐私、测试、部署、out-of-scope。

用户答完（或选择跳过）→ 写 `docs/REQUIREMENTS_ANSWERS.md`，**默认假设**部分用 `(default assumption)` 标注，让 Codex 知道哪些是弱点。

Stage 1 不写产品代码，除非用户明确要求。

## Stage 2：Codex 实现

Claude 完成后让 Codex 读 `docs/codex/00-implementation-handoff.md` 并实现第一个垂直切片：

1. 读上下文（Trellis workflow / PRD / Roadmap / Requirements Answers / kickoff task）。
2. 写代码前先输出 `## Task Plan`（goal/scope/out-of-scope/files/risks/verification/criteria）。
3. **Greenfield 必须先做最小可运行垂直切片**：把 hello-world 路径打通（请求 → handler → DB 或 LLM → 响应 → 断言），再加功能。
4. 一次只做一个任务，不顺手扩。
5. 跑验证（`npm run lint/typecheck/test/build`、`pytest`、`ruff check .`、`mypy .` 等），scope 内修复，无关失败单独报告。
6. 总结：what changed / files / acceptance / verification / known issues / next。

## Review Mode

用户说"review / 审查改动"时，**不要先实施**。读 PRD、specs、diff、验证结果，按严重度输出：

```markdown
## Review Result
Status: Pass / Pass with concerns / Fail

## Critical / Major / Minor issues
## Scope violations
## Missing acceptance criteria
## Verification (command + result)
## Recommended fix order
```

完整模板见 `references/safety-rules.md`。Review 期间默认不直接改代码，除非用户要求。

## 硬规则（Hard Rules）

### 不要太早写代码

中大型项目，下面 7 项齐全前不开实施：Project Brief / Requirements Answers（含明确默认假设）/ PRD / Specs / Roadmap / Acceptance Criteria / Verification Commands。

例外：用户明确要 throwaway prototype / 单独小修 / 项目已有等价文档。

### 安全边界

改动前 `git status`，大改起分支。**不要**：跑破坏性命令（未授权）、删用户文件、出当前 repo、提交密钥、硬编码 API key、改 `.env`（用 `.env.example`）、加大依赖、删测试 / 削断言、绕过 lint/typecheck/build。

可发布文件不要写个人路径、用户名，用 `<project-root>` / `<developer-name>` / `<non-system-drive>` 占位。

### 控制 scope

一次一个任务。不要把任务变成全项目重写。不要在当前任务实现未来 roadmap。

### 假设不阻塞

回答缺失就用明确假设继续推进。只有当未答的问题影响安全 / 成本 / 法律 / 不可逆架构时才停下。

## References（按需加载）

- `references/handoff-flow.md`：Project Brief / PRD / specs / roadmap 字段细清单 + Bad/Good spec 例子。
- `references/safety-rules.md`：详细安全规则、Done Checklist、Review 模板。
- `references/llm-spec-checklist.md`：LLM 项目专属 checklist。

## 发布安全

发布前扫：个人绝对路径、本地用户名、机器专属工具目录、token / API key、私有项目名。示例用占位符。`SKILL.md` 自包含完整流程（不藏指令在 references）。脚本通过命令行参数和环境变量配置。临时目录 smoke test 通过后才删该临时目录。
