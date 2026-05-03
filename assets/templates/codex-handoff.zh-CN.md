# Codex 实施划交

## Stage 1 完整性闸门（在做任何事之前先跑）

Codex 进入这个项目的第一件事就是这一关。**任何一项检查不过，立刻拒绝
启动实施**，按下面"拒绝并交回"的模板回复。**不要**"顺手"把缺失的部分填
上 —— Stage 1 是 Claude 的活，不是 Codex 的（见 SKILL.md 硬规则
"Stage 1 是 Claude 的活，Codex 必须拒写"）。

检查项：

1. `docs/REQUIREMENTS_ANSWERS.md` 存在。
2. `docs/REQUIREMENTS_ANSWERS.md` 里**至少有一条**答案**不是** `(default assumption)`。
   （全是默认值意味着没有真人答过题。）
3. `docs/PRD.md` 存在，且超出 bootstrap 脚手架（有具体的 acceptance
   criteria，不只是 TBD 行）。
4. `docs/ROADMAP.md` 存在，且至少列出一个带验证命令的具体垂直切片。
5. `.trellis/tasks/001-implementation-kickoff.md` 存在。

### 拒绝并交回

任意检查失败时，按用户语言回复：

> Stage 1 还没完成。具体卡在以下检查上：
>
> - <列出 5 项中失败的项以及原因>
>
> Stage 1 是交互式 Claude Code 的活，不是我的。要继续：
>
>     cd <project-path>
>     claude
>
> 进入 Claude Code 后说：*"读 `docs/claude/00-prd-spec-prompt.md`，按它
> 执行 Stage 1。"* 等 Stage 1 真的完成后回到 Codex，我开始第一个垂直
> 切片。

**不要**自己写或细化任何 Stage 1 缺失的文档。这个闸门存在的意义就是
拦住这种行为。

## 先读这些（闸门通过之后）

Claude 完成 Stage 1 规划后，Codex 在动代码前**按顺序**读这些文件：

1. `PROJECT_BRIEF.md`、`AGENTS.md`
2. `.trellis/workflow.md`、相关的 `.trellis/spec/*`
3. `docs/PROJECT_BRIEF.md`
4. `docs/REQUIREMENTS_ANSWERS.md` —— 注意 `(default assumption)` 标记
5. `docs/PRD.md`
6. `docs/ROADMAP.md`
7. `.trellis/tasks/001-implementation-kickoff.md`

## 默认执行路径

从 `.trellis/tasks/001-implementation-kickoff.md` 和 `docs/ROADMAP.md` 里
第一个垂直切片开始。先 inspect 仓库、确认生成的文档自洽，再实现最小可运行
脚手架。

## 动任何代码之前：先输出 Task Plan

```markdown
## Task Plan
- Task:
- Goal:
- Scope:
- Out of Scope:
- Files to inspect:
- Files likely to change:
- Risks:
- Verification commands:
- Acceptance criteria:
```

## Greenfield 规则

全新项目必须**先做最小可运行垂直切片**再加功能。先把"hello world"路径打通
（请求 → handler → DB 或 LLM → 响应 → 断言），再分层加功能。**不要**试图在
第一个任务里 ship 很多功能。

## 实施循环

1. Inspect 相关文件。
2. 实现一个聚焦任务。
3. 跑验证。
4. Scope 内修复失败。如果失败和当前任务无关，单独报告，不要顺手改。
5. 总结：改了什么、改了哪些文件、acceptance 状态、验证结果、已知问题、下一任务。

## 验证命令 Cookbook

Node 通用：

```bash
npm run lint
npm run typecheck
npm run test
npm run build
```

Python 通用：

```bash
pytest
ruff check .
mypy .
```

如果不知道项目用什么命令，看 `package.json` / `pyproject.toml` / `Makefile`
里的 scripts。如果完全没有验证命令，把"加一个最小 smoke check"作为这个任务
的一部分。

## 边界提醒

- 一次一个任务。不要把任务变成全项目重写。
- 不要在当前任务里实现未来 roadmap。
- 不要删测试 / 削断言来通过验证。
- 不要提交密钥。不要改 `.env`，改 `.env.example`。
- 待在当前 repo，除非用户明确要求出去。

完整的安全 + done checklist 在 `references/safety-rules.md`，按需加载。
如果用户要的是 review 而不是实施，切到 Review Mode（也在
`references/safety-rules.md` 里），**不要先动代码**。

## 项目：{{name}}
