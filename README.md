# Bingo Skills

面向 agent 日常开发的中文工程工作流技能集。七个手动入口覆盖项目配置、需求澄清、spec、普通 / 快速实施、验收后收尾和 bug 排查；`writing-for-agents` 提供可自动或手动调用的 agent 文档写作参考。

## 安装

使用 `skills` CLI 安装本仓库的全部 skills 到当前用户，供多个项目使用：

```bash
npx skills@latest add imbingox/skills -g
```

项目级安装时去掉 `-g`。只安装部分入口时用 `--skill <name>` 指定，可选项为 `--skill setup`、`--skill grill`、`--skill to-spec`、`--skill implement`、`--skill fast-implement`、`--skill finish`、`--skill diagnosing-bugs`、`--skill writing-for-agents`，例如：

```bash
npx skills@latest add imbingox/skills -g --skill setup --skill implement
```

`fast-implement` 依赖 `implement` 的实现与验证参考。选择部分安装时需同时安装两者，不能假定安装工具会自动补齐：

```bash
npx skills@latest add imbingox/skills -g --skill fast-implement --skill implement
```

其他入口可单独安装，所有工作流均不依赖可选的 `writing-for-agents`。跨 skill 资源按实际安装位置定位；读取参考不会自动启动对应的手动工作流。

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

项目准备使用 issue 工作流时，首次运行一次；直接处理小任务无需先配置：

```text
/setup
```

它会配置当前项目的 issue tracker、领域文档位置和 Codex / Claude statusline，并核对已有开发与验证指引。CLI 配置写入 repo 内的 `.codex/config.toml`、`.claude/settings.json`，Claude 的状态栏脚本也放在项目内；不写用户目录。已有项目配置会保留，缺失项先展示变更、确认后补齐。换 tracker 或 CLI 版本后可以再次运行。

个人项目默认使用 **open → ready → closed**：

- **open**：想法、待澄清或尚未准备实施的任务。
- **ready**：需求和验收已明确，可交给 agent 或自己实施；有 blocker 时仍须先满足依赖。
- **closed**：任务已结束；完成与取消要区分，取消不能被当作已完成的依赖。

GitHub / GitLab 的 open、closed 使用原生状态，只额外建立一个 `ready` 标签；本地 markdown 用 `Status: open | ready | closed`。`setup` 会在确认后补建缺失的 ready 标签，不建立整套 triage 标签。实施和 review 进度由 `implement` 内部管理，无需额外的 `in-progress` / `in-review` 标签；阻塞原因和真实依赖记录在 issue 中，不额外维护 `blocked` 标签。已有项目继续沿用原有约定，不强制迁移。

### 按任务选择路径

不必每个任务走完全部入口。日常按三条路径选择：

| 场景 | 路径 | 信息放在哪里 |
| --- | --- | --- |
| 明确的小任务 | 对话聊清需求和方案 → `fast-implement` → 验收后按需 `finish` | 当前对话，无需 issue 或 spec |
| 一般任务 | `grill` → `to-spec` 确认摘要后建 issue → 新会话 `implement` → 验收后按需 `finish` | issue 正文保存规格，评论保存实施与交接事实 |
| 原因不明的故障 | `diagnosing-bugs` | 复现、实验和根因证据；不要求先建票 |

小任务由当前 agent 实现、自查并运行必要验证；不自动建票、写评论、改标签或关闭 issue：

```text
/fast-implement 修正设置页帮助文案中的错字，不提交
```

需要独立 review 时用 `implement`，即使任务很小也会保留独立审查：

```text
/implement 导出文件名追加当天日期，保持文件内容不变，补文件名测试
```

两个实施入口默认都允许本次范围的本地 commit，不自动 push、merge PR 或部署；可明确要求“不提交”。`fast-implement` 不编排子票，也不能替代项目强制的独立 review；范围扩大时会说明并建议切换入口。普通 `implement` 的 Parent 模式在调用时的当前分支和工作区集成，只为子任务创建独立 worktree；子任务验收后直接合回当前分支，再创建下游子任务。该模式依赖本地 commit 和合入，不支持“不提交”或“不更新当前分支”；用户已有修改阻挡合入时，保留子任务成果并报告。

一般任务先讨论，再用 to-spec 展示 Proposed Changes。每项关键行为变化都带具体的前后示例，用户确认这份摘要后才生成完整 spec 并写入 issue；“只预览”也先确认摘要，再生成完整草稿。比如已确认的导出命名方案可以写成“目录已有 report.csv，再次导出：原来覆盖原文件 → 现在保留原文件并生成 report-2.csv”。新能力则展示当前限制或替代步骤与新用法：

```text
/grill 增加导出功能，兼容现有 API
/to-spec 将已确认需求整理并发布为 issue
```

拿到实际 issue 编号后，新会话执行 `/implement #123`（替换为真实编号）。issue 应包含目标、方案、兼容约束、验收、范围边界和必要指针，新会话无需依赖原对话。普通任务一张 issue 即可；需要多个独立交付切片时才拆父子票，由 `implement` 自动编排。独立 review 与要求的验证通过后，按项目完成条件关闭。

开发验收后，可调用独立的 `finish` 停止本任务的临时验收服务、提交剩余改动并关闭明确的目标任务。它会核对当前交付内容和完成证据，复用已完成的提交 / 关票；没有 issue 也可直接本地收尾，不需要先运行 setup。它不自动 push、merge PR 或部署，也不替代必需的独立 review 和验证。

希望先人工验收、最后统一收尾时，可以明确把提交和关票留到 finish：

```text
/implement #123，提交和关票留到 finish
/finish #123，已验收通过，停止本任务预览服务并提交、关闭任务
```

以上编号替换为真实目标。Leaf 会保留待提交改动；Parent 仍完成编排所需的子任务提交、合入与状态推进，只将父任务关票和剩余收尾留后。`fast-implement` 也支持把提交留到 finish。已有“不提交”“不关票”“保留服务”等限制在 finish 中继续生效，直到用户明确撤回；也可以用 `/finish 只检查` 查看尚缺的收尾条件。

| 入口 | 用途 |
| --- | --- |
| [setup](skills/setup/SKILL.md) | 为当前项目配置工作流、领域文档与开发验证指引。 |
| [grill](skills/grill/SKILL.md) | 澄清需求、外部行为、兼容范围和验收边界。 |
| [to-spec](skills/to-spec/SKILL.md) | 先确认带具体前后示例的 Proposed Changes，再生成 spec 并按需拆票。可说“仅 spec”“只拆票 #123”或“只预览”。 |
| [implement](skills/implement/SKILL.md) | 按 issue、spec 或已明确的小任务实施并完成独立 review；有子票时通过当前 harness 的 sub-agent 自动编排。 |
| [fast-implement](skills/fast-implement/SKILL.md) | 快速完成明确、局部的小任务，当前 agent 自查并验证；依赖 implement 的参考资源。 |
| [finish](skills/finish/SKILL.md) | 开发验收后核对证据、停止临时验收服务、提交剩余修改并按项目配置关闭任务；可单独安装。 |
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
- 主动暂停、受阻或换 session 前，`implement` 将已完成 / 剩余、分支与 worktree、最近验证和下一步简短记录到原 issue 评论或已有本地票；未获写入授权或写入失败时只在对话交接。`fast-implement` 只在对话中交接。两者均不另建进度文件，恢复时先核对实际状态，不盲信旧记录，例如 `/implement 继续 #123`。

七个工作流入口都需要手动调用。`writing-for-agents` 可在编写 agent 文档时自动选用，也可以直接调用：

```text
/writing-for-agents 检查这份 spec 是否能由新 session 独立执行
```

项目的 tracker 位置和操作方式由该项目自己的配置决定。运行 `/setup` 后，`to-spec`、`implement` 和 `finish` 按项目配置管理 issue；缺少远程 tracker 配置时，先运行 `/setup`。快速实施也须满足项目验证要求，不能把自查记为独立 review 通过。

安装参数可查阅 [`skills` CLI 文档](https://github.com/vercel-labs/skills)。
