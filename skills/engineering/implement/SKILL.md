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

下面只是一套**内部概念状态**，用于 Controller 推理，不代表 tracker 必须真的存在这些名字：

`ready → in-progress → in-review → accepted`

review fail 时：

`in-review → in-progress`

真正写回 tracker 时，读取 `docs/agents/issue-tracker.md` 或等价配置，将这些阶段映射到项目现有的状态、labels、assignee、project field、open/closed 等机制。**不要为了这个 skill 擅自创建新的 workflow vocabulary。**

如果 tracker 没有中间状态，Controller 可以只在内部维护 `in-progress / in-review / accepted`，最终只执行配置里定义的终态动作。

用户显式要求“不改 tracker / 不关 issue”时，以用户要求为准，但仍执行相同 review gate，并报告本来会发生的状态转换。

## 3. Leaf mode

Leaf mode 下，主 session 同时承担 Controller 与 Implementer；**Reviewer 必须是独立 sub-agent**。

流程：

1. Controller 确认 blockers 已满足，记录实施起点 commit、当前分支和已有工作区修改。
2. 如项目有对应状态约定，标记目标为 in-progress。
3. 主 session 按 spec 实现，并持续做相关测试 / typecheck。
4. 实现完成后进入 in-review，启动独立 Reviewer sub-agent。
5. Reviewer 做 **Standards + Spec** 双轴检查：
   - Standards：项目约定、命名、重复逻辑、边界、过度抽象、测试是否绑定实现细节。
   - Spec：验收条件是否完整实现、`Proposed Changes` / external contract / compatibility 是否兑现、是否 scope creep。
6. review fail：Controller 将 findings 交回当前 Implementer 修复，然后重新 review。
7. review pass：Controller 运行最终 verification；通过后按 tracker 配置推进到该 issue 的完成状态。

如果当前 harness 无法启动独立 reviewer agent，可以完成实现和测试，但**不得把 issue 推进到 tracker 定义的完成状态**；明确报告“等待独立 review”。

## 4. Parent mode: 执行 child issue DAG

Parent mode 下，主 session只做 Controller / Orchestrator，不直接把整张父票当成一份大实现。

### 4.1 建图与 frontier

- 从 tracker 读取 child issues、blocking edges 和状态。
- 已达到 tracker 定义的完成状态、或已被 Controller 明确 accepted 的 child，视为已满足。
- **Frontier** = 当前所有 blockers 均已满足的未完成 child。
- 每轮 child 状态变化后重新计算 frontier。

### 4.2 是否并行

“无 blocker”只表示**可以开始**，不代表一定并行。

只有同时满足以下条件才并行：

- dependency independent；
- 预期修改范围低重叠；
- 可以给每个 implementer 独立 branch / worktree / workspace，避免多个 agent 同时写同一 working tree。

修改范围明显重叠、共享 migration / schema / generated contract 容易冲突，或无法隔离 workspace 时，串行执行。

### 4.3 每个 child 的生命周期

对 frontier 中选中的每个 child：

1. Controller 标记 child in-progress（如果 tracker 有对应约定）。
2. 派 **Implementer sub-agent**，给它：
   - child issue 全文；
   - parent spec 中相关约束；
   - blockers 的已完成事实；
   - 独立 workspace / branch 信息；
   - 禁止修改 issue workflow state 的规则。
3. Implementer 按 public seam 实现、测试、提交，并返回 commit / diff 范围 / 验证结果 / 未解决项。
4. Controller 标记 in-review，并派一个**没有参与该 child 实现的独立 Reviewer sub-agent**。
5. Reviewer 基于 child spec、parent 约束和实际 diff 做 Standards + Spec review。
6. review fail：Controller 把 findings 交回**原 Implementer**修复，再进入独立 review；child 不解锁 downstream。
7. review pass + child verification pass：Controller 按 tracker 配置推进 child 到其完成状态。
8. 重新计算 frontier，继续下一轮。

只有达到 **accepted / tracker-complete** 条件的 child 才能解除下游 blocker；“代码写完”或“测试通过”都不够。

## 5. Parent integration review

所有 child 达到 tracker 定义的完成条件后，不能直接把 parent 推进到终态。

Controller 先将各 child 成果集成到目标分支 / workspace，并启动一个**独立 Parent Integration Reviewer**。它不重复逐行审每个 child，而重点检查组合后的系统：

- parent `Proposed Changes` 是否整体兑现；
- child 之间的 public contract 是否真正接通；
- external contract / compatibility / migration 是否在组合后仍成立；
- 跨 ticket 状态机、生命周期和错误语义是否一致；
- 是否出现只有组合后才暴露的回归、重复实现或 scope gap；
- parent-level acceptance criteria 是否满足。

review fail 时：

- 如果问题说明某个已 accepted child 实际未满足自己的 contract，Controller 重新打开 / 退回该 child，并交给原 Implementer 修复；
- 如果是纯跨 child integration 问题，由 Controller 指派 integration fix，不能偷偷改 parent spec。

integration review 通过后，运行 parent-level tests / smoke / end-to-end verification。全部通过后，Controller 才可按 tracker 配置推进 parent 到终态。

## 6. 实现纪律：行为测试优先

尽可能按：

`一条行为测试 → 因目标行为缺失而失败 → 最小实现使其通过 → 下一条行为`

修 bug 先建立能复现问题的 regression test。

测试通过 public seam 观察结果，不绑定 private helpers、内部调用次数或类拆分。期望值来自独立样例或 spec，不在断言里复制实现公式。

覆盖关键成功、失败、兼容 / migration 和异步状态路径；不要求穷举所有边界。纯文档、配置或无法合理 TDD 的工作使用相应静态检查 / smoke test，并说明验证限制。

持续运行相关小范围测试与 typecheck；每个 child 完成前跑其要求的完整检查，parent 最后再跑组合层 verification。没实际运行的检查不能记为通过。

## 7. External contract 不得偷偷改变

保持已确认的 API、CLI、UI、config/env、输入输出、错误、默认值、完成语义、旧数据与 migration 承诺。

发现实现必须改变这些 contract 时，不让 implementer 自行拍板。Controller 暂停受影响分支，说明：

- 原 contract；
- 为什么不可行；
- proposed change；
- compatibility / migration 影响。

取得用户确认并更新 spec 后再继续。

未经单独授权不访问生产凭据、真实账户，不下实盘订单，不运行破坏性迁移或生产发布。

## 8. Git 与交接

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
