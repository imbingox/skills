# Parent orchestration

Parent mode 下，主 session只做 Controller / Orchestrator，不直接把整张父票当成一份大实现。

## 建图与 frontier

- 从 tracker 读取 child issues、blocking edges 和状态。
- 已达到 tracker 定义的完成状态、或已被 Controller 明确 accepted 的 child，视为已满足。
- **Frontier** = 当前所有 blockers 均已满足的未完成 child。
- 每轮 child 状态变化后重新计算 frontier。

## 是否并行

“无 blocker”只表示**可以开始**，不代表一定并行。

只有同时满足以下条件才并行：

- dependency independent；
- 预期修改范围低重叠；
- 可以给每个 implementer 独立 branch / worktree / workspace，避免多个 agent 同时写同一 working tree。

修改范围明显重叠、共享 migration / schema / generated contract 容易冲突，或无法隔离 workspace 时，串行执行。

## 每个 child 的生命周期

对 frontier 中选中的每个 child，Controller **先准备依赖代码，再派发**：

- 记录每个已验收 blocker 的实现 commit / 集成 commit，包括本次开始前已完成的依赖。状态已完成不等于代码已在当前基线。
- 在受控的本地集成分支准备包含全部已验收依赖成果的基线，再从该基线创建 child workspace；串行复用 workspace 也要先核对依赖代码已存在。不得提前混入未验收 child 的成果。
- 核对依赖实现确实可见，记录基线 commit 与依赖 commits 的对应关系，并交给 Implementer 和 Reviewer。依赖成果缺失或无法定位时阻塞该 child，不让它猜测或重复实现。
- 集成发生冲突时先解决并运行相关验证；若改变了已验收行为，需要独立 review 后再派发。此处本地集成不代表授权 push 或 merge PR。

用户要求“不提交”时，不自动取消编排：使用隔离的文件快照或 patch 传递已验收依赖，记录来源基线与内容标识，Reviewer 检查相同内容。无法可靠传递时暂停依赖分支，不假造 commit；若 tracker 完成条件要求 commit，则不能推进终态。

基线准备好后：

1. Controller 标记 child in-progress（如果 tracker 有对应约定）。
2. 派 **Implementer sub-agent**，给它：
   - child issue 全文；
   - parent spec 中相关约束；
   - blockers 的已完成事实、依赖 commits 和已准备好的基线 commit；
   - 独立 workspace / branch 信息；
   - 禁止修改 issue workflow state 的规则。
3. Implementer 按入口的实现纪律完成实现与测试，返回 workspace、基线 / diff 范围、已有 commits、验证结果和未解决项。
4. Controller 标记 in-review，并派一个**没有参与该 child 实现的独立 Reviewer sub-agent**。
5. 按 [review.md](review.md) 做 Standards + Spec review；Controller 给 Reviewer 提供该参考、child spec、parent 约束、依赖基线和实际 diff。
6. review fail：Controller 把 findings 交回**原 Implementer**修复，再进入独立 review；child 不解锁 downstream。
7. review pass 后执行 child 最终 verification；通过后由 Implementer 提交本 child 的修改，Controller 核对最终 commit 对应已审查 / 验证的内容，再按 tracker 配置推进完成状态。提交失败不能宣告已交付；commit hook 若改变内容，补做受影响的 review 与验证。
8. 记录已验收成果的 commits，重新计算 frontier；每个下游派发前都执行上述基线准备，不能只传递状态已完成的信息。

只有达到 **accepted / tracker-complete** 条件的 child 才能解除下游 blocker；“代码写完”或“测试通过”都不够。

## Parent integration review

所有 child 达到 tracker 定义的完成条件后，不能直接把 parent 推进到终态。

Controller 确认全部 child 的已验收成果均已集成到目标分支 / workspace（包括此前为下游准备的依赖基线），补齐剩余成果并运行相关集成检查，再按 [review.md](review.md) 启动一个**独立 Parent Integration Reviewer**。它不重复逐行审每个 child，而重点检查组合后的系统：

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
