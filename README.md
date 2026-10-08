# Bingo Skills

[Matt 的 skills](https://github.com/mattpocock/skills) 的中文增强层。日常开发直接用 Matt 原版，本仓库只补两处：

- `spec`：包装 Matt 的 `to-spec` 与 `to-tickets`，一次调用写 spec 并按规模拆票。写入前先确认带具体 Before → After 示例的 Proposed Changes，spec 顶部保留这份给人审阅的摘要。
- `finish`：开发验收后收尾，停止本任务的临时服务、提交剩余修改并按项目配置关闭任务。Matt 的 `implement` 结束于 commit，不关票。

## 安装

先安装 Matt 的 skills，两种方式选一种，不要同时装：

```bash
# Claude Code 插件
claude plugin install mattpocock-skills
# 或 skills.sh（Codex 等其他 agent）
npx skills@latest add mattpocock/skills
```

`spec` 运行时读取 Matt 的 `to-spec` 与 `to-tickets`，只装部分 Matt skills 时须包含这两个。

再安装本仓库：

```bash
npx skills@latest add imbingox/skills -g
```

项目级安装时去掉 `-g`；只装一个入口时加 `--skill spec` 或 `--skill finish`。Claude Code 也可以通过插件 marketplace 安装：

```bash
claude plugin marketplace add imbingox/skills
claude plugin install bingo-skills@imbingox
```

## 使用

一般任务的流程：

```text
/grill-with-docs 增加导出功能，兼容现有 API                ← Matt
/spec 将已确认需求整理并发布为 issue                         ← 本仓库
/implement #123                                              ← Matt；多票用 /implement-spec #120
/finish #123，已验收通过，停止本任务预览服务并提交、关闭任务  ← 本仓库
```

以上编号替换为真实 issue。能在一个会话内完成的小任务，按 Matt 的建议直接 `/implement`，不必写 spec。

### spec

`spec` 先在对话中展示 Proposed Changes，确认后才生成完整 spec 并写入 tracker。摘要放在 spec 顶部，供人两分钟内审完；正文沿用 Matt 的 spec 模板，供执行 agent 使用。例如：

```markdown
## Proposed Changes
### What changes
- 重复导出不再覆盖：已有 report.csv 时再次导出，Before：覆盖 report.csv → After：保留原文件，生成 report-2.csv
### Contract & Compatibility
- 导出 API 参数不变；返回的文件名可能带序号，依赖固定文件名的调用方需调整
### Decisions
- 选追加序号而非时间戳：文件名更短，排序稳定
### Test seams
- 导出 API：同名文件已存在时，返回的文件名与目录内容
### Not doing / Open
- 不做：清理历史导出文件
```

spec 的规则：

- seams 和拆分在同一轮确认，确认前不写入任何东西。
- 决策旁写明被否决的方案，Out of Scope 列出真正拒绝的事，假设与待定项单列；有重大待定项时不标就绪。
- User Stories 只覆盖关键行为，不追求数量。
- 一个会话内能完成的任务只发一张 issue；需要多个交付切片时保留父 spec 并拆子票。每张子票带上父 spec 已确认的 seams，发布前核对父 spec 的每项验收都落到某张票上。

可以说“仅 spec”“只拆票 #123”或“只预览”。tracker 位置与就绪标签按项目配置执行，缺少配置时先运行 `/setup-matt-pocock-skills`；Matt 的 skills 未安装时，`spec` 会停止并提示安装。

### finish

验收后调用 `finish`。它核对当前交付内容与完成证据，停止能确认属于本任务的临时服务，只提交本次范围的修改，再按项目配置关闭明确的目标任务。已提交或已关闭的部分会复用，不重复操作；没有 issue 时只做本地收尾。

```text
/finish #123，已验收通过，停止本任务预览服务并提交、关闭任务
/finish 只检查
```

“不提交”“不关票”“保留服务”等已有限制继续生效，直到明确撤回。`finish` 不自动 push、merge PR 或部署，也不替代必需的独立 review 和验证。

## 入口

| 入口 | 用途 |
| --- | --- |
| [spec](skills/spec/SKILL.md) | 包装 Matt 的 to-spec 与 to-tickets：先确认带具体前后示例的 Proposed Changes，再生成便于审阅的 spec 并按需拆票。 |
| [finish](skills/finish/SKILL.md) | 开发验收后核对证据、停止临时验收服务、提交剩余修改并按项目配置关闭任务；可单独安装。 |

两个入口都需要手动调用。安装参数可查阅 [`skills` CLI 文档](https://github.com/vercel-labs/skills)。
