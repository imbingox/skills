---
name: spec
description: "包装 Matt 的 to-spec 与 to-tickets：写入前先确认带具体 Before → After 示例的 Proposed Changes，再生成便于审阅的 spec，并按规模发布单 issue 或父 spec 与子 tickets；也支持仅 spec、只拆票。"
disable-model-invocation: true
---

# Spec

一次调用连续完成 Matt 的 `to-spec` 与 `to-tickets`，并补上给人审阅的一层：**Proposed Changes 写给人看，正文和 tickets 给执行 agent 使用。**
基础流程与模板来自 Matt 原文，本文件只写增量；两者冲突时以本文件为准。默认中文正文、英文结构标题。不重新做完整访谈，不凭空补接口、默认值或兼容策略，不开始实现。

## 依赖：读取 Matt 原文

依赖 `mattpocock/skills` 的 `to-spec` 与 `to-tickets`。两者只能由用户手动触发，**不要用 Skill tool 调用**（会被拦截），直接读取其 `SKILL.md` 文件：

- skills.sh 安装：先查项目 `.agents/skills/`、`.claude/skills/`，再查 `~/.agents/skills/`、`~/.claude/skills/`；用项目 `skills-lock.json` 或 `~/.agents/.skill-lock.json` 中 `source: mattpocock/skills` 的条目确认来源。
- Claude 插件：以 `~/.claude/plugins/installed_plugins.json` 中 `mattpocock-skills` 记录的 `installPath` 为准，读取其下 `skills/engineering/<name>/SKILL.md`。

同名目录可能来自其他来源，来源无法确认时不使用。先读 to-spec；确定拆票（含只拆票模式）时再读 to-tickets。报告实际读取的路径。
找不到时停止，提示安装后重试：`claude plugin install mattpocock-skills`，或 `npx skills@latest add mattpocock/skills --skill to-spec --skill to-tickets`。

## 模式

- 默认：固化当前需求，按规模选择单 issue 或父 spec + 子 tickets。
- “仅 spec” / “不拆票”：只生成或更新 spec。
- “只拆票 <issue / 路径>”：读取已有 spec 后补拆，不重写父 spec 的决策。
- “只预览” / “不要发布”：确认 Proposed Changes 后返回完整草稿，不写文件或 tracker，也不改项目配置。

这些是自然语言用法，不是 CLI 参数。所有模式都先确认、后生成正文与写入。

## 1. 收集事实

在 Matt 的探索步骤之外，检查现有 API、CLI、UI、config/env、schema、错误与状态语义、消息协议和持久化格式的调用方，确认兼容影响。区分已确认决策、可验证的现状和未决事项。

tracker、就绪标记和关系表达按项目配置（项目说明指向的文件，其次 `docs/agents/`）；Matt `/setup-matt-pocock-skills` 生成的配置或项目已有的其他配置都可用。都没有时停止远程发布并提示运行 `/setup-matt-pocock-skills`，不猜目标；只预览不受影响。

## 2. 确认 Proposed Changes

Matt 流程中的 seams 确认和拆分 quiz 合并为这一轮。先在对话中展示，通常 15–25 行；确认前不生成完整 spec / 子票正文，不写入。确认后原样置于 spec 顶部。

```markdown
## Proposed Changes
### What changes
- <关键变化>：<具体输入 / 操作>，Before：<现状结果> → After：<预期结果>
### Contract & Compatibility
- 最终怎么输入、调用、配置，得到什么输出或错误；哪些不变，哪些 breaking，迁移要求
### Decisions
- 选 <X> 而非 <Y>：<一句理由>
### Test seams
- <public seam>：在这里验证什么
### Not doing / Open
- 不做：<讨论中明确拒绝的相邻工作>
- 假设 / 待定：<逐条标明，不写成已定事实>
```

- 每项关键行为变化（含 UI、CLI、工作流和兼容 / 错误语义）都配同一具体场景的 Before → After，不写“更方便”“优化体验”。新增能力的 Before 写当前限制或替代步骤；纯内部改动用具体输入输出说明外部行为不变。现状未查明先核实，不编造。
- 例如需求已确认“重复导出时不覆盖旧文件”：`已有 report.csv 时再次导出，Before：覆盖 report.csv → After：保留原文件，生成 report-2.csv`。这只是写法示例，不要求项目采用该命名。
- 没有变化才写 None，尚未查明不能写 None。“入口兼容但完成语义改变”必须写出；兼容旧格式不等于旧消费者一定兼容。
- Decisions 只写讨论中实际比较过的方案；被否决的方案最能帮审阅者发现错误决策，但不为填格式编造替代方案。
- Test seams 沿用 Matt 原则：优先已有的、最高层的 public seam，越少越好；已同意的验收方式不重复确认。
- 预计拆票时附简短拆分表（Ticket / 交付行为 / Blocked by），一起确认粒度和依赖。只拆票模式展示原 spec 的关键变化（已有的直接复用）和拆分表。
- 长度是目标，不是删掉关键 breaking change 的理由；完整 schema 和详细样例放正文。

明确请用户确认这份摘要。调用本入口、先前的讨论或泛泛要求“直接发布”都不算确认；当前会话已确认同一版本时直接复用。用户提出修改时先修订摘要与示例，对变更部分取得确认；未回复不视为同意。

## 3. 正文

沿用 Matt to-spec 的模板，按以下规则调整，按复杂度控制篇幅：

- 顶部是已确认的 Proposed Changes，与正文保持一致。
- User Stories 覆盖关键行为、失败路径和兼容要求即可，不追求数量；架构或重构类改动可精简，重点放在 Implementation / Testing Decisions。
- Implementation Decisions 中比较过替代方案的决策写明“而非 Y”。可保留新会话独立执行所需的代码 / 文档指针，不指定未确认的文件路径或实现代码。
- Testing Decisions 给出可勾选的验收条件，覆盖顶部的契约与兼容承诺。
- Out of Scope 列出讨论中真正拒绝的事；有明确重访条件时一并记录，不另造路线图。
- 有假设或待定项时加 Open Questions 一节，逐条写明如何解决；有重大待定项的 issue 不能标为就绪。
- 新会话无需原对话即可执行，不能只写“按刚才讨论实现”。发布到 issue 时正文只承载规格，实施与交接事实留给评论。
- 最小充分：新增依赖、通用层、配置项或扩展点必须对应当前验收或已确认约束。发现方案可能过重时提出具体简化建议，不擅自改写决策。
- 需求新增技术栈或改变启动 / 测试 / 构建方式时，验收包含验证入口、原开发指引和受影响已有 CI 的同步，保留仍在使用的旧检查；命令引用真实脚本或标明待实现。

需要改变已确认的行为、契约或范围时，回到第 2 步。

## 4. 按规模拆票

- 一个 fresh context 内可完成、可独立验证且无独立交付阶段：**一张 issue 同时承载 spec 和验收，不另建实施票。**
- 否则保留父 spec，按 Matt to-tickets 切分，并遵守 [tickets.md](references/tickets.md) 的增量规则。

不因进入拆票而重新访谈。若此时才确定要拆票，或拆分有实质变化，先展示拆分表并等待确认。

## 5. 发布并核对

发布前读取 [issue-tracker.md](references/issue-tracker.md)，按其中的查重、写入顺序、读回核对和就绪规则执行；Matt 原文中的标签、本地路径和发布方式以项目配置为准。摘要与拆分已确认、且本次发布已获授权时直接发布，不另加一轮确认。报告已发布、未发布和受阻的项。
