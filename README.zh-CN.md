# Big Project Workflow Skill

[English](./README.md) | **简体中文**

一个面向中大型项目的两阶段 AI 编程工作流：
**Claude Code CLI 写文档，Codex 写代码，[Trellis](https://github.com/mindfold-ai/trellis)
管项目记忆。** 灵感来自一位大佬分享的 Opus + Codex + Trellis 实战经历
（原帖已经看不到了），打包成一个可移植的
[OpenAI Codex Skill](https://developers.openai.com/codex/skills)。

完整的运行契约写在 [`SKILL.md`](./SKILL.md) 里（Codex 加载的就是它）。本 README
面向"装这个 skill 的开发者"。中文阅读版的 SKILL 在
[`references/SKILL.zh-CN.md`](./references/SKILL.zh-CN.md)。

## 这个 skill 解决什么

- **两阶段划交清晰。** Claude 负责写 Project Brief、需求问卷（30-500 题）、
  PRD、specs、Roadmap；Codex 读这些文档实现垂直切片。
- **真问卷，不是愿望清单。** Stage 1 prompt 强制要求在写 PRD 前生成结构化
  问卷 —— 这是这套工作流相对裸 prompt 最大的价值差。
- **不和 Trellis 抢饭碗。** `.trellis/spec/` 和 `.trellis/tasks/` 由 Trellis
  负责；这个 skill 只做编排。
- **安全优先。** Windows 上拒绝往系统盘 bootstrap、不提交密钥、不削测试、
  可发布文件用占位符。
- **跨平台。** 一份 Python 脚本，Windows / macOS / Linux / WSL 通用。

## 依赖

| 工具 | 用途 |
|------|------|
| [Codex CLI](https://developers.openai.com/codex/cli/features) | 加载这个 skill |
| [Claude Code CLI](https://docs.anthropic.com/claude-code) | Stage 1 写文档 |
| Node.js (LTS) | Trellis 运行时 |
| [Trellis CLI](https://github.com/mindfold-ai/trellis) | `.trellis/` 工作区 |
| Python 3.9+ | Bootstrap 脚本 |
| Git | 版本控制 |

安装 Trellis（想锁版本就用 `--trellis-version` 传给 bootstrap）：

```bash
npm install -g @mindfoldhq/trellis@latest
```

如果不想让 npm 全局包装到系统盘，先 `npm config set prefix` 指到其他盘再装。

Codex 的 skill 加载机制按
[官方文档](https://developers.openai.com/codex/skills) 配置即可。

## 安装

把这个仓库 clone 或下载下来，然后把整个目录拷到 Codex 的 skills 目录：

PowerShell：

```powershell
$SkillRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
Copy-Item -Recurse big-project-workflow-skill (Join-Path $SkillRoot "skills/big-project-workflow")
```

Bash / zsh：

```bash
cp -r big-project-workflow-skill "${CODEX_HOME:-$HOME/.codex}/skills/big-project-workflow"
```

重启 Codex，让 skill 列表刷新。在对话里说 "大项目工作流"、"big project
workflow"、"PRD"、"non-system-drive project"、"Trellis bootstrap" 等关键词
就能触发。

## 快速开始（3 步）

### 1. Bootstrap

PowerShell：

```powershell
$SkillRoot = (Join-Path ${env:CODEX_HOME ?? "$HOME/.codex"} "skills/big-project-workflow")

python (Join-Path $SkillRoot "scripts/bootstrap.py") `
  --root "D:\codex-projects" `
  --name "my-project" `
  --developer "<你的名字>" `
  --brief "用一段话描述项目目标"
```

Bash / zsh：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/big-project-workflow"

python3 "$SKILL_ROOT/scripts/bootstrap.py" \
  --root "$HOME/codex-projects" \
  --name "my-project" \
  --developer "<你的名字>" \
  --brief "用一段话描述项目目标"
```

### 2. Stage 1 — Claude 写文档

```powershell
Get-Content .\docs\claude\00-prd-spec-prompt.md -Raw |
  claude -p --model opus --permission-mode acceptEdits
```

```bash
cat docs/claude/00-prd-spec-prompt.md |
  claude -p --model opus --permission-mode acceptEdits
```

Claude 会先生成结构化需求问卷，引导你回答（或显式标默认假设），
然后写 PRD / specs / Roadmap / kickoff task / Codex handoff doc。

### 3. Stage 2 — Codex 实现

在项目里打开 Codex，跟它说：

> 读 `docs/codex/00-implementation-handoff.md`，按生成的 roadmap 实现
> 第一个垂直切片。

Codex 会先输出 Task Plan、做最小可运行垂直切片、跑验证，然后总结。

## Bootstrap 脚本参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--name` | 必填 | 项目目录名 |
| `--root` | `BIG_PROJECT_ROOT` 环境变量；Windows 第一个非系统盘；其他系统 `~/codex-projects` | 父目录 |
| `--developer` | `TRELLIS_DEVELOPER` 环境变量或操作系统用户名 | Trellis 用 |
| `--brief` | 空 | 一段话目标，会写进模板 |
| `--trellis-version` | `latest` | Trellis 不在 PATH 时打印的安装命令版本号 |
| `--platforms` | `codex` | 逗号分隔；Trellis 0.4+ 默认就生成 `.claude/` |
| `--trellis-bin` | 自动查找 | 显式指定 trellis 可执行文件路径 |
| `--allow-system-drive` | 关闭 | Windows 想往系统盘（一般是 `C:`）建项目时必须传 |
| `--skip-trellis` | 关闭 | 跳过 `trellis init` |

## 排查

**`trellis` 找不到。** 脚本会打印安装命令然后干净退出。运行
`npm install -g @mindfoldhq/trellis@<version>` 装上，再跑一次脚本即可。

**项目不小心建到了系统盘。** Windows 上默认就拒绝系统盘，除非传
`--allow-system-drive`。推荐设一次 `BIG_PROJECT_ROOT` 环境变量指到你常用
的盘，以后就不用每次 `--root`。

**`claude` 找不到。** 装 [Claude Code CLI](https://docs.anthropic.com/claude-code)。
Stage 1 也支持交互式 —— 直接打开 `docs/claude/00-prd-spec-prompt.md`
粘到任意 Claude 会话里也行。

**想换 Trellis 平台组合。** 用 `--platforms codex,claude,cursor` 之类。
支持的 flag 见 [Trellis 文档](https://docs.trytrellis.app/)。

## 文件目录

```
big-project-workflow/
├── SKILL.md                         # Codex 加载的契约
├── README.md                        # English README
├── README.zh-CN.md                  # 你正在看这份
├── LICENSE                          # MIT
├── agents/openai.yaml               # Codex skill UI 元信息
├── scripts/bootstrap.py             # 跨平台 bootstrap 脚本
├── assets/templates/                # 4 份模板（bootstrap 用）
└── references/                      # Codex/Claude 按需加载
    ├── handoff-flow.md              # 各文档字段细清单 + spec 例子
    ├── safety-rules.md              # 详细安全规则 + Review 模板
    ├── llm-spec-checklist.md        # LLM 项目专属 checklist
    └── SKILL.zh-CN.md               # SKILL.md 的中文阅读版
```

## 发布安全

如果 fork 或者改了重新发，请按 `SKILL.md` 末尾的 Publish Safety Gate 检查：
扫个人绝对路径、本地用户名、机器专属工具目录、token、API key、私有项目名。
所有用户特定的值都换成占位符（`<project-root>`、`<developer-name>`、
`<non-system-drive>`）。

## License

MIT，见 [LICENSE](./LICENSE)。

## 致谢

- 工作流提炼自一位大佬分享的 Opus + Codex + Trellis 实战经历。
- Trellis 来自 [mindfold-ai](https://github.com/mindfold-ai/trellis)。
- Codex Skills 格式来自 [OpenAI](https://developers.openai.com/codex/skills)。
