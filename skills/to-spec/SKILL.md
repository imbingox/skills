---
name: to-spec
description: "将已讨论的需求整理为 Proposed Changes + 完整 spec，并按规模生成单 issue 或父 spec 与子 tickets；也支持仅 spec、只拆票。"
disable-model-invocation: true
---

# To Spec

合并“写 spec”和“按需拆票”的操作入口，不混淆两类产物的职责。
**Proposed Changes 写给人看；完整 spec 和 tickets 给执行 agent 使用。**
默认中文正文、英文结构标题。不要重新做完整访谈，不凭空补接口、默认值或兼容策略，不开始实现。
本 skill 的参考文件随目录一起安装，不依赖其他 skill。

## 输入与模式

- 默认：固化当前需求，再按规模选择单 issue 或父 spec + 子 tickets。
- “仅 spec” / “不拆票”：只生成或更新 spec。
- “只拆票 <issue / 路径>”：读取已有 spec 后补拆 tickets，不重写父 spec 的决策。此模式替代原独立 to-tickets。
- “只预览” / “不要发布”：只返回草稿，不写 tracker，也不修改项目配置。

这些是自然语言用法，不是承诺存在的 CLI 参数解析器。

## Process

### 1. 收集现有事实与决策

读取用户指定的 issue / 文件全文、相关评论、父子票及依赖；按项目 AGENTS.md / CLAUDE.md、domain glossary 和 ADR 理解代码。
区分已确认决策、可验证的现状和未决事项。检查现有 API、CLI、UI、config/env、schema、错误与状态语义、消息协议和持久化格式的调用方。
测试优先使用已约定、已有且稳定的高层 public seam。不要重复确认已经同意的验收方式。

tracker 的读取、配置兼容与发布规则见 [issue-tracker.md](references/issue-tracker.md)。发布前必须读取。若当前 repo 缺少 `docs/agents/issue-tracker.md` 或等价明确配置，停止远程发布并提示先运行 `/setup`；不要猜发布目标。
有重大未决决策时明确标为待确认，不把猜测写成已定事实，也不标 ready-for-agent。

### 2. 先写 Proposed Changes

放在 spec 正文最顶部，通常约 10–20 行。优先外部行为，不写模块拆分或内部实现流水账。
必须覆盖以下四项；没有变化才写 None，尚未查明不能写 None。

```markdown
## Proposed Changes
### What changes
- 计划带来的关键用户 / 调用方可见变化。
### External contract
- 最终怎么输入、调用、配置，以及得到什么输出或错误。
### Compatibility
- 哪些保持不变，哪些 breaking，默认行为与迁移要求是什么。
### Before → After
- 旧用法 / 行为 → 新用法 / 行为；无有意义差异时写 None。
```

接口变化优先给最小 Before → After 输入输出示例。例子必须来自已确认契约，不能把示意文案偷偷变成真实字段或枚举。
“入口兼容但完成语义改变”必须明确写出；兼容旧格式不等于旧消费者一定兼容。
长度是目标，不是删掉关键 breaking change 的理由。完整 schema 和详细样例放在下文，顶部不重复。

### 3. 固化完整 spec

保留以下结构，按复杂度控制篇幅，不为了填模板重复内容：

- Problem Statement：用户遇到的问题。
- Solution：整体方案及边界。
- User Stories：覆盖关键行为、失败路径和兼容要求；用“作为…，希望…，以便…”的编号列表，不追求数量。
- Implementation Decisions：已定的模块边界、API/schema、交互与迁移决策；不指定尚未确认的文件路径或实现代码。允许已确认的最小契约样例和 prototype 中能精确表达决策的片段。
- Testing Decisions：public seam、既有测试参考和可观察的验收方式；覆盖顶部的外部契约与兼容承诺。
- Out of Scope：明确不做的相邻工作。
- Further Notes：补充信息，不在这里藏新决策。

在 Testing Decisions 中给出可勾选的验收条件。顶部和完整 spec 必须一致；只拆票模式沿用原 spec，不强制改模板。

将最小充分方案固化为边界：新增依赖、通用层、配置项或扩展点必须能对应当前验收条件或已确认约束，不把未来可能性升级为本次要求。已讨论但暂不需要的能力放入 Out of Scope；有明确重访触发条件时一并记录，不另造路线图。发现已确认方案可能过重时提出具体简化建议，不在整理 spec 或拆票时擅自改写决策。

### 4. 按规模决定是否拆票

一个 fresh context 内可完成、可独立验证且无独立交付阶段的任务：**一张 issue 同时承载 spec 和验收，不再创建重复实施票。**
需要多个独立交付切片或多个 session 的任务：保留父 spec，并按 [tickets.md](references/tickets.md) 生成子票。
只有需要拆票时才读取该文件。按可验收行为切片，不机械地按前端 / 后端 / 测试拆分。

把 Proposed Changes 和简短的拆分表放在一起供用户确认。已经确认过的决策或拆分不要再次提问。
若出现新的拆分方案或重大契约未决点，先展示并等待确认；用户明确授权直接发布且没有重大未决决策时，可以直接发布。
不因为进入拆票阶段而重新发起整套需求访谈。

### 5. 发布并核对

按 tracker 规则发布。单 issue 不另建父票；多票先建父 spec，再按依赖顺序建子票。
重跑前查现有票，避免重复；只拆票模式不自动关闭、改写或重新创建父 spec。
发布后读回并核对正文、真实链接与依赖。说明哪些已发布、哪些尚未发布或仍被阻塞。
只对已明确可交给 agent 的实施票按项目约定加标签；父 spec 不自动标 ready-for-agent。
ready-for-agent 不代表依赖已经完成，也不构成生产访问、真实交易、部署或数据迁移授权。
