# Codex 实施划交

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
