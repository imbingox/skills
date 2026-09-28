# Implement

## What it does

`implement` 自动识别 Leaf issue 与 Parent issue。

Leaf 下主 session 实现，独立 reviewer sub-agent 验收；Parent 下主 session 作为 Controller / Orchestrator，按 blockers 计算 frontier，编排 child implementers 与独立 child reviewers，最后再做独立 parent integration review。

核心规则是：**Controller 管 issue workflow state，Implementer 写代码，Reviewer 独立验收。** 具体状态名称和终态动作来自项目的 issue tracker 配置；只有 review 与 required verification 都通过，Controller 才能执行该 tracker 定义的完成转换。

## When to reach for it

需求和 external contract 已通过 spec / issue 确认，准备开始实际开发时。

对单一 issue 直接运行；对父 issue 也直接运行，不需要另写 orchestration prompt。父票已有 child graph 时，`implement` 会消费已有 DAG，而不是重新拆票。依赖远程 issue workflow 但 repo 尚未配置 tracker 时先运行 `/setup`。

## Common questions

**谁改 issue 状态？** 只有当前 Controller。Implementer 和 Reviewer 只报告事实，不改 authoritative workflow state；状态名、labels、project field 或 close 动作都按项目 tracker 配置执行。

**Leaf 也要独立 review 吗？** 要。主 session 可以同时是 Controller + Implementer，但 Reviewer 必须是没有参与实现的独立 sub-agent。

**Parent 什么时候解锁下游？** child 必须 implementation 完成、独立 review 通过且 verification 通过，并达到 tracker 定义的完成条件后才解锁 blocker。

**所有 ready child 都并行吗？** 不会。DAG 决定能否开始，代码修改范围和 workspace 隔离决定是否安全并行。

**没有 sub-agent 能力怎么办？** 可以实现和测试，但没有独立 review 就不能自动推进到 tracker 定义的完成状态。

## It's working if

你只需要调用一次 `implement <issue>`：

- Leaf 会完成实现 → 独立 review → Controller 完成状态；
- Parent 会持续消费 frontier → child implement/review → 解锁下一批 → parent integration review → parent-level verification；
- 任何 review fail 都回到实现阶段，不会提前关闭 issue；
- external contract 和 compatibility 不会在实现阶段被 agent 静默改变。
