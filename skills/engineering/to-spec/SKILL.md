---
name: to-spec
description: "将当前对话整理为可执行 spec 并发布到项目 issue tracker；不重新访谈，优先用 Proposed Changes 让人快速确认计划中的外部变化与兼容性。"
disable-model-invocation: true
---

这个 skill 根据当前对话上下文和对代码库的理解生成 spec。

**不要重新采访用户。** 只综合已经讨论、确认或可以从代码库中直接验证的内容。不要为了“补完整 spec”自行创造新的重要产品决策、接口语义或兼容策略。

核心原则：

> **Proposed Changes 写给人看；其余 spec 写给执行 agent 看。**

spec 首先要让人能快速判断“准备改什么、以后怎么用、旧东西会不会坏”，其次才是为实现 agent 保存完整决策上下文。

如果项目的 issue tracker 和 triage label vocabulary 尚未配置，告诉用户运行 `/setup-matt-pocock-skills`。

## Process

1. 如果尚未了解代码库，先探索当前实现状态。

   - 全文使用项目已有的 domain glossary。
   - 尊重相关 ADR 和既有公共接口。
   - 特别检查本次改动涉及的 external/public surface：API、CLI、配置、UI、schema、错误语义、状态语义、持久化格式、跨进程/跨服务协议等。
   - 检查现有调用方和兼容性约束，不要只从新实现角度设计接口。

2. 确定测试 seam。

   - 优先复用已有 seam，而不是新增 seam。
   - 使用尽可能高层、稳定、可观察的 seam。
   - 测试应验证外部行为，而不是实现细节。
   - 如果对话中已经明确测试方式，不要重复询问。
   - 只有当测试 seam 存在会显著改变实现或验收方式的歧义时，才向用户确认。

3. 使用下面的模板生成 spec，并发布到项目 issue tracker。

   - 应用 `ready-for-agent` triage label；无需额外 triage。
   - `Proposed Changes` 必须位于最顶部。
   - `Proposed Changes` 通常控制在约 **10–20 行**，优先可扫读性，不追求完整。
   - 不要把内部架构、模块拆分、文件路径等实现细节塞进 `Proposed Changes`。
   - 如果某项没有变化，明确写 `None`，不要为了填模板制造内容。

<spec-template>

## Proposed Changes

这一部分描述**计划发生的变化**，不是已经完成的 changelog。

目标是让用户在不阅读后续完整 spec 的情况下，快速确认以下四件事：

1. 改了什么？
2. 用户 / 调用方以后怎么使用？
3. 旧行为、旧接口、旧数据是否仍兼容？
4. 行为前后最关键的区别是什么？

### What changes

只写最重要的用户可见或调用方可见变化。

优先描述行为和结果，不描述内部实现方式。

如果没有用户可见或调用方可见变化，写：

`None`

### External contract

列出对 public/external surface 的计划变更，例如：

- HTTP / RPC API
- public Python / TypeScript API
- CLI
- config / env
- UI 操作和用户输入
- request / response schema
- error / status / empty-state semantics
- Snapshot / event / message / protocol
- 持久化格式中被其他组件依赖的部分

重点写最终“怎么调用、怎么输入、会得到什么”。

如果 external contract 不变，写：

`None`

### Compatibility

明确说明本次变化对现有使用方式的影响，包括适用项：

- backward compatibility
- breaking changes
- 默认行为变化
- 字段新增 / 删除 / 改名
- deprecated / removed behavior
- migration requirements
- 旧数据是否仍可读取
- 旧调用方是否仍可工作
- “调用方式兼容，但行为语义变化”这类容易遗漏的情况

不要只写 `compatible`；如果存在语义变化，要明确指出变化是什么。

如果没有兼容性影响，写：

`None`

### Before → After

当行为有明显变化时，用最短、最直观的形式展示。

例如：

`Before: stopped → worker exits`

`After: stopped → cancel → confirm completion → worker exits`

这部分不是必填。没有有意义的前后差异时写：

`None`

---

## Problem Statement

从用户视角描述当前面对的问题。

## Solution

从用户视角描述解决方案。

不要在这里重复 `Proposed Changes` 的逐条内容；这里解释整体方案及为什么这样解决问题。

## User Stories

使用编号列表记录 user stories。

每条格式：

1. As an <actor>, I want a <feature>, so that <benefit>

列表应覆盖该功能的重要行为、失败路径、边界和兼容要求，但不要为了“数量多”重复同一语义。

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

## Implementation Decisions

记录已经做出的实现决策，可以包括：

- 将构建 / 修改的模块
- 模块 interface 的变化
- 技术澄清
- 架构决策
- schema changes
- API contracts
- compatibility / migration decisions
- specific interactions

这里可以详细记录 `Proposed Changes` 中已经摘要过的 contract，但不得与顶部摘要矛盾。

**不要写具体文件路径或普通实现代码片段。** 它们很容易过期。

例外：如果 prototype 产生了比文字更精确地表达已确认决策的片段（例如 state machine、reducer、schema、type shape），可以内联最小的 decision-rich 部分，并简单注明来自 prototype。不要粘贴完整 demo。

## Testing Decisions

记录测试决策，包括：

- 什么是 good test：验证 external behavior，不绑定 implementation details
- 哪些模块 / seam 会被测试
- 代码库中可以参考的 prior art
- 对 `External contract` 和 `Compatibility` 中关键承诺的验收方式
- breaking / migration 场景如何验证（如适用）

## Out of Scope

明确本 spec 不包含的内容。

尤其写出那些“很容易顺手做，但这次不做”的 adjacent work，避免 agent 擅自扩大范围。

## Further Notes

记录其他有助于后续实现和交接的信息。

不要在这里埋新的关键产品决策；关键外部变化必须出现在 `Proposed Changes`，关键实现决策必须出现在 `Implementation Decisions`。

</spec-template>
