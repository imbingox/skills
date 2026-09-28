---
name: setup
description: "Run once per repo: configure the project's issue tracker and domain-doc locations, then idempotently check Codex / Claude CLI statusline defaults without overwriting existing user configuration."
disable-model-invocation: true
---

# Setup

每个 repo 首次使用本套 skills 时运行一次：

`/setup`

它只有一个入口，但处理两个层次：

1. **Project setup**：当前 repo 的 tracker、workflow 和 domain docs，必须完成。
2. **CLI environment check**：当前机器的 Codex / Claude 配置，幂等检查；已有用户配置优先，缺失时才提议补齐。

不要把这两层拆成两个用户命令。重复运行必须安全。

## 1. Explore first

先读取当前 repo，不假设：

- `git remote -v`、`.git/config` 和 repo root；
- `AGENTS.md` / `CLAUDE.md`；
- `docs/agents/`、`CONTEXT.md`、`CONTEXT-MAP.md`、已有 ADR 目录；
- 当前 tracker 线索：GitHub / GitLab remote、Linear 配置、本地 issue 文件等；
- 已有 `docs/agents/issue-tracker.md` / `domain.md`。

同时只读检查本机：

- `command -v codex`、`codex --version`、`~/.codex/config.toml`；
- `command -v claude`、`claude --version`、`~/.claude/settings.json`；
- 已有 statusline / TUI 配置。

不要读取、打印或写入 API key、token、cookie 等 secrets。

## 2. Project setup: issue tracker

项目配置是后续 `to-spec` 和 `implement` 的 authoritative source。

优先顺序：

1. 已有 `docs/agents/issue-tracker.md`：保留并校验，只补缺少的关键语义。
2. 用户已经明确指定 tracker：使用用户选择。
3. 可以从 repo remote 明确推断：提出推荐值供用户确认。
4. 仍不明确：只问 tracker / target 这一项，不猜。

至少记录：

- provider：GitHub / GitLab / Linear / local markdown / other；
- target：明确的 repository / project / 本地目录；
- read / write 方式：当前环境可用且已授权的 connector / CLI；
- spec / ticket 规则：小任务单 issue，大任务 parent spec + child issues；
- parent-child 如何表达；
- blockers / dependencies 如何表达；
- workflow state：项目已经存在的状态、labels、project fields、assignee 约定；
- **completion condition**：什么状态或动作代表一个 issue 已满足 blocker；
- 更新/关闭规则：哪些动作 `implement` 的 Controller 可以执行，哪些需要人工确认。

**不要为了适配本 skill 发明新的 workflow vocabulary。**
如果 tracker 只有 open / closed，就记录 open / closed；如果有 Project Status / Linear states，就记录真实状态。

参考模板见 [project-config.md](references/project-config.md)。

## 3. Project setup: domain docs

记录到 `docs/agents/domain.md`：

- glossary / domain context 的位置；
- ADR 位置与编号约定；
- single-context 或 multi-context。

默认 single-context；只有 repo 已经呈现明显多 context 结构时才使用 map。
不要为了 setup 创建空 `CONTEXT.md` 或空 ADR 目录；需要记录第一个术语 / 决策时再创建。

## 4. Add a small project pointer

在 repo 已有的 `CLAUDE.md` 或 `AGENTS.md` 中维护一个简短的 `## Agent workflow` 区块，指向：

- `docs/agents/issue-tracker.md`
- `docs/agents/domain.md`

如果两个都存在，优先修改当前项目已经作为主说明文件使用的那个；不能判断时让用户选一个。
不要复制整份 tracker 配置到这里，也不要覆盖周围人工内容。

## 5. CLI environment check

CLI 设置是**用户 / 机器级**，不是 repo 配置。每次 `/setup` 都检查，但仅在缺失时提议写入。

### Codex CLI

Codex 用户配置位于 `~/.codex/config.toml`。

如果已经存在 `[tui].status_line`，保留原值。

如果 Codex 已安装且 status line 未配置，推荐使用原生 TUI status line：

```toml
[tui]
status_line = [
  "model-with-reasoning",
  "current-dir",
  "git-branch",
  "context-remaining",
  "five-hour-limit",
  "weekly-limit",
]
```

先检查当前 Codex 版本是否接受这些 item；优先使用当前客户端的 `/statusline` / config schema 作为事实来源。某个 item 不支持时删掉该 item，不为了套模板破坏配置。

只 merge `tui.status_line`，不替换整个 `[tui]` 或 `config.toml`。

### Claude Code

Claude 用户配置位于 `~/.claude/settings.json`。

如果已经存在 `statusLine`，保留原值。

如果 Claude 已安装且 statusLine 缺失，推荐：

1. 将本 skill 内的 [claude-statusline.py](references/claude-statusline.py) 复制到 `~/.claude/statusline.py`；
2. merge 以下字段到已有 settings JSON：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py",
    "padding": 0
  }
}
```

该 renderer 对缺失字段容错，展示 model / effort、repo + branch、context remaining、5h / 7d remaining（字段可用时）。

### Safety for user-level writes

对 `~/.codex` / `~/.claude` 的任何写入：

- 先展示将修改的文件和最小 diff；
- 取得用户一次明确确认；
- 写前创建 timestamped backup；
- parse 后再写，不能用字符串替换破坏 TOML / JSON；
- 只 merge 本 skill 管理的 key；
- 写后重新 parse 并核对；
- 已有 statusline 永不自动替换。

用户拒绝机器级修改时，Project setup 仍然可以完成。

更多兼容原则见 [cli-config.md](references/cli-config.md)。

## 6. Confirm and write

在第一次实际写入前，用一个紧凑摘要展示：

- Project tracker target；
- workflow completion condition；
- domain docs layout；
- Codex statusline：existing / proposed / unavailable；
- Claude statusline：existing / proposed / unavailable。

用户确认后执行写入。

如果全部已有且一致，不要为了流程重复询问，报告 no-op 即可。

## 7. Done

完成后报告：

- 创建 / 更新了哪些 repo 文件；
- tracker target 与完成状态语义；
- Codex / Claude 哪些用户级配置被保留、补齐或跳过；
- backup 路径（如发生用户级写入）；
- 未完成项。

后续日常流程只有：

`grill-with-docs → to-spec → implement`

如果 `to-spec` / `implement` 找不到项目 tracker 配置，应提示先运行 `/setup`，不要猜发布目标。
