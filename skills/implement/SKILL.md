---
name: implement
description: "按已确认的 issue / spec 实施。Leaf 自动实现并交给独立 reviewer；Parent 自动编排子 issue DAG、独立 review 每个子票并做最终 integration review。Controller 独占 workflow state。"
disable-model-invocation: true
---

# Implement

实现用户指定的 issue / spec，不把实施阶段变成重新设计需求的机会。
默认用中文报告，保留项目已有技术标识符。

核心模型：

> **Controller 管状态，Implementer 写代码，Reviewer 独立验收。**

> **每份实现都必须由没有参与该实现的独立 reviewer agent 审查；只有 Controller 可以改变 issue workflow state。**

## 1. 读取目标并自动选择模式

先读取项目的 `AGENTS.md` / `CLAUDE.md`、相关 glossary / ADR、目标 issue / spec 全文及评论，以及项目现有 `docs/agents/issue-tracker.md` 或等价 tracker 配置。若目标依赖远程 issue workflow 但当前 repo 没有明确 tracker 配置，停止状态写入并提示先运行 `/setup`；不要自行猜 repo 或状态机。

读取 `Proposed Changes`、完整验收条件、父子关系和真实 blockers。旧 spec 没有 `Proposed Changes` 也正常支持。

自动判断：

- **Leaf mode**：目标没有需要编排的 child issues，直接实现当前目标。
- **Parent mode**：目标存在 child issues / ticket graph，当前 session 成为 orchestrator，消费已有 DAG。

已有 issue graph 是已确认的执行计划。Implement 阶段默认**不重新拆票、不重排需求、不自行新增产品决策**。
如果发现 blocker 错误、子票无法独立完成、spec 与代码事实冲突，或必须改变 external contract，暂停受影响分支并向用户说明。

## 2. Workflow state 的唯一 owner

当前 `/implement <target>` session 是 **Controller**。

Controller 是目标 issue 及本次编排范围内 child issues 的唯一 workflow-state writer。**具体状态机、labels、assignee、open/closed 语义和终态名称必须来自项目的 issue tracker 配置，不由本 skill 发明。**

- Implementer 只返回实现事实、commit 和验证结果。
- Reviewer 只返回 review verdict 和 findings。
- Implementer / Reviewer 都不得自行 close issue、标 done、解除 blocker 或修改 authoritative workflow state。
- Controller 只有在独立 review 通过并完成要求的 verification 后，才可把对应 issue推进到 tracker 定义的下一合法状态或终态。
- Parent 只有在所有 child 达到 tracker 定义的完成条件、最终 integration review 通过且 parent-level verification 通过后，才可推进到 parent 的终态。

每次更新 tracker 对象前，Controller 必须重新读取该对象、相关评论及当前依赖 / 状态，保留人工编辑和无关字段，只提交本次必要的最小变更。若发现人工改变了需求、blockers 或状态，使原计划或状态转换失效，暂停受影响分支并说明冲突，不用旧快照覆盖。写入后读回核对；失败或并发冲突时先重读再决定是否重试，不能假报状态推进成功。

按项目现有状态机执行合法转换，不发明 labels 或状态；没有中间状态时只在内部记录进度，完成后执行配置定义的终态动作。

用户显式要求“不改 tracker / 不关 issue”时，以用户要求为准，但仍执行相同 review gate，并报告本来会发生的状态转换。

## 3. Leaf mode

Leaf mode 下，主 session 同时承担 Controller 与 Implementer；**Reviewer 必须是独立 sub-agent**。

流程：

1. Controller 确认 blockers 已满足，记录实施起点 commit、当前分支和已有工作区修改。
2. 如项目有对应状态约定，标记目标为 in-progress。
3. 主 session 按 spec 实现，并持续做相关测试 / typecheck。
4. 实现完成后按项目约定进入 review 阶段，读取 [review.md](references/review.md)，启动未参与实现的独立 Reviewer，分别检查 Standards 和 Spec。
5. 任一轴不通过：将 findings 交回 Implementer 修复，再独立复审。
6. 两轴通过后运行最终 verification，再提交本次目标范围的修改到当前工作分支，记录 commit。提交失败不能宣告已交付；commit hook 若改变内容，补做受影响的 review 与验证。
7. Controller 核对最终交付与已审查 / 验证内容一致后，按 tracker 配置推进完成状态。

用户明确要求“不提交”时保留未提交修改并如实报告；若项目完成条件要求 commit，则不能推进终态。不访问 tracker 的本地 spec 只报告实现、review 与验证结果。

如果当前 harness 无法启动独立 reviewer agent，可以完成实现和测试，但**不得把 issue 推进到 tracker 定义的完成状态**；明确报告“等待独立 review”。

## 4. Parent mode

目标有 child issues / DAG 时自动读取 [orchestration.md](references/orchestration.md)，继续完成整组编排，无需用户额外开启模式。
Controller 负责 frontier、隔离 workspace、已验收依赖代码交付、child review 和最终 integration review；每个 child 由 sub-agent 实现。状态完成不能替代依赖代码可用。

## 5. 实现纪律：行为测试优先

涉及模块 / interface 设计、依赖组织、测试 seam 或重构时，Implementer 与相应 Reviewer 必须读取并应用本 skill 的 [codebase-design.md](references/codebase-design.md)。Controller 派发这些任务时附上该参考内容或可访问路径；不要求用户手动调用，不改变已确认 spec。

尽可能按：

`一条行为测试 → 因目标行为缺失而失败 → 最小实现使其通过 → 下一条行为`

修 bug 先建立能复现问题的 regression test。

测试通过 public seam 观察结果，不绑定 private helpers、内部调用次数或类拆分。期望值来自独立样例或 spec，不在断言里复制实现公式。

覆盖关键成功、失败、兼容 / migration 和异步状态路径；不要求穷举所有边界。纯文档、配置或无法合理 TDD 的工作使用相应静态检查 / smoke test，并说明验证限制。

持续运行相关小范围测试与 typecheck；每个 child 完成前跑其要求的完整检查，parent 最后再跑组合层 verification。没实际运行的检查不能记为通过。

## 6. External contract 不得偷偷改变

保持已确认的 API、CLI、UI、config/env、输入输出、错误、默认值、完成语义、旧数据与 migration 承诺。

发现实现必须改变这些 contract 时，不让 implementer 自行拍板。Controller 暂停受影响分支，说明：

- 原 contract；
- 为什么不可行；
- proposed change；
- compatibility / migration 影响。

取得用户确认并更新 spec 后再继续。

未经单独授权不访问生产凭据、真实账户，不下实盘订单，不运行破坏性迁移或生产发布。

## 7. Git 与交接

保护开始前已有的用户修改，不把无关工作纳入 commit。

并行 child 优先各自独立 worktree / branch；Implementer 只提交自己的工作。Controller 负责集成，不让多个 sub-agent 同时写一个 working tree。

`/implement` 授权本次目标范围内必要的 issue workflow transitions，但**不自动授权**：

- push 到远端；
- merge PR；
- production deploy / migration；
- 修改目标图之外的 issue；
- 改写已确认 spec。

最终报告：

- 完成 / 未完成的 issues；
- child review 与 parent integration review 结果；
- external contract / compatibility 的实际变化；
- verification 证据；
- commits / integration commit；
- 任何未解决或未验证事项。
