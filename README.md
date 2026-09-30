# Bingo Skills

面向 agent 日常开发的中文工程工作流技能集。五个手动入口覆盖项目配置、需求澄清、spec、实施和 bug 排查；`writing-for-agents` 提供可自动或手动调用的 agent 文档写作参考。

## 安装

使用 `skills` CLI 安装本仓库的全部 skills 到当前用户，供多个项目使用：

```bash
npx skills@latest add imbingox/skills -g
```

项目级安装时去掉 `-g`。只安装部分入口时用 `--skill <name>` 指定，可选项为 `--skill setup`、`--skill grill`、`--skill to-spec`、`--skill implement`、`--skill diagnosing-bugs`、`--skill writing-for-agents`，例如：

```bash
npx skills@latest add imbingox/skills -g --skill setup --skill implement
```

查看可安装清单：

```bash
npx skills@latest add imbingox/skills --list
```

Claude Code 也可以通过插件 marketplace 安装：

```bash
claude plugin marketplace add imbingox/skills
claude plugin install bingo-skills@imbingox
```

## 使用

每个项目首次配置工作流时运行一次：

```text
/setup
```

它会配置当前项目的 issue tracker、领域文档位置和 Codex / Claude statusline，并核对已有开发与验证指引。CLI 配置写入 repo 内的 `.codex/config.toml`、`.claude/settings.json`，Claude 的状态栏脚本也放在项目内；不写用户目录。已有项目配置会保留，缺失项先展示变更、确认后补齐。换 tracker 或 CLI 版本后可以再次运行。

个人项目默认使用 **open → ready → closed**：

- **open**：想法、待澄清或尚未准备实施的任务。
- **ready**：需求和验收已明确，可交给 agent 或自己实施；有 blocker 时仍须先满足依赖。
- **closed**：任务已结束；完成与取消要区分，取消不能被当作已完成的依赖。

GitHub / GitLab 的 open、closed 使用原生状态，只额外建立一个 `ready` 标签；本地 markdown 用 `Status: open | ready | closed`。`setup` 会在确认后补建缺失的 ready 标签，不建立整套 triage 标签。实施和 review 进度由 `implement` 内部管理，无需额外的 `in-progress` / `in-review` 标签。已有项目继续沿用原有约定，不强制迁移。

### 按任务选择路径

不必每个任务走完全部入口。目标、兼容边界和验收已明确的小任务可直接实施，无需先建票或运行 setup；只是省去重复澄清和文档，不省去独立 review 与验证：

```text
/implement 导出文件名追加当天日期，保持文件内容不变，补文件名测试
```

有未决需求先用 `grill`；需要固化决策时用 `to-spec`，需要多个独立交付切片时再拆票：

```text
/grill 增加导出功能，兼容现有 API
/to-spec
/implement #123
```

| 入口 | 用途 |
| --- | --- |
| [setup](skills/setup/SKILL.md) | 为当前项目配置工作流、领域文档与开发验证指引。 |
| [grill](skills/grill/SKILL.md) | 澄清需求、外部行为、兼容范围和验收边界。 |
| [to-spec](skills/to-spec/SKILL.md) | 固化需求为 spec，并按规模决定是否拆成子 tickets。可说“仅 spec”“只拆票 #123”或“只预览”。 |
| [implement](skills/implement/SKILL.md) | 按 issue、spec 或已明确的小任务实施并完成独立 review；有子票时通过当前 harness 的 sub-agent 自动编排。 |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 从症状开始复现、定位和修复；可说“只排查”以仅输出根因与证据。 |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | 编写或审查 skill、项目指令、spec、tickets 和 agent prompt；可自动触发，也可手动调用。 |

发现 bug 时可直接调用排查入口，不必先运行 `/setup`：

```text
/diagnosing-bugs 保存后刷新，配置恢复默认了
/diagnosing-bugs 只排查：升级后导出明显变慢
```

### 个人项目的节奏

- 想法先留在 open，只需写清“解决什么问题、为什么值得做、做到什么程度就够了”；准备实施时再补齐验收，不急着写完整 spec。
- ready 只放近期准备做的任务；建议同时推进一个主要需求。该需求内部的子票仍可自动编排，不必为优先级或处理中再加标签。
- 开发与验证指引放在项目原有 README / AGENTS / CLAUDE 中，能从脚本查明的命令不另建注册表。新增技术栈或改变命令时，由那次实施同步维护原指引和受影响的已有 CI；例如 Python 增加 TS 前端，要补前端检查但保留 Python 检查，无需重跑 setup。
- 主动暂停、受阻或换 session 前，`implement` 会留下已完成 / 剩余、分支与 worktree、最近验证和下一步的简短交接。优先写原 issue 评论或已有本地票；未获写入授权或写入失败时只在对话交接，不另建进度文件。恢复仍用同一目标，例如 `/implement 继续 #123`，先核对实际状态，不盲信旧记录。

五个工作流入口都需要手动调用。`writing-for-agents` 可在编写 agent 文档时自动选用，也可以直接调用：

```text
/writing-for-agents 检查这份 spec 是否能由新 session 独立执行
```

项目的 tracker 位置和操作方式由该项目自己的配置决定。运行 `/setup` 后，`to-spec` 和 `implement` 会按项目配置处理 tracker；缺少远程 tracker 配置时，先运行 `/setup`。每个入口可单独安装，工作流不依赖 `writing-for-agents`。

安装参数可查阅 [`skills` CLI 文档](https://github.com/vercel-labs/skills)。
