# Parent orchestration

Parent mode 下主 session 只做 Controller：建图、派发、集成、推进状态；每个 child 由 Implementer sub-agent 实现，不把整张父票当成一份大实现。

## 当前分支作为集成目标

- 调用时所在的分支就是本次目标分支，所在工作区就是主工作区；记录绝对路径、分支名、起点 commit 和用户已有修改。不另建父级分支或 worktree，也不在结束时再做一次父分支交付。detached HEAD 时先确定目标分支再开始编排。
- 每个 child 从目标分支派发时的 HEAD 创建独立 branch / worktree；已验收的 child 直接合回目标分支，下游从合入后的 HEAD 创建，因此自带已完成依赖。
- 创建子 worktree 只带已提交内容。依赖用户未提交修改的 child 暂停派发；其他 child 可以先实施。合入前确认主工作区仍在目标分支、没有进行中的 Git 操作，暂存区及已跟踪文件无未提交修改。用户修改或未跟踪文件阻挡合入时，保留 child 分支和 worktree 并报告，不自动 stash、提交或覆盖用户内容。
- Controller 串行执行合入：`git -C <主工作区> merge --no-ff --no-edit <已审查的-child-commit>`，保留已审查的 commits，不 squash、不 rebase。合入后运行相关检查，通过后才推进 child 状态、清理 worktree 并解锁下游。
- 合入冲突由 Controller 在主工作区解决，只提交本次冲突解决内容并重跑检查；解决方式改变已验收内容时，先补独立 review。合入或检查失败时不关闭 child、不解锁下游，不为回退而重置用户分支；交接实际合入状态与失败证据。
- 本模式依赖本地 commit 和合入。用户要求“不提交”或“不更新当前分支”时，在创建分支或派发前说明限制，等待调整执行要求；不将其解释为允许创建额外父级分支。本地集成不代表授权 push 或 merge PR。

## Sub-agent 与 worktree

只使用当前 harness 的 sub-agent 能力。无法启动 sub-agent 时，暂停编排并说明，不由 Controller 接管整张父票的实现。

Controller 每次派发前确认目标分支和 HEAD，记录该 child 的固定 baseline commit，再执行 `git -C <主工作区> worktree add -b <child-branch> <path> <baseline-commit>`。将路径、分支和 baseline 写进 brief，要求 sub-agent 只在自己的 worktree 工作：shell 的 cwd 可能在每次调用后重置，命令一律用绝对路径或 `git -C <path>`。不使用基线和分支名无法事先确定的自动隔离 worktree。

## 新 worktree 的环境

Controller 在创建 worktree 后、派发 Implementer 前完成初始化。初始化失败时把该 child 标记为阻塞，报告脱敏后的输出，不让 Implementer 在残缺环境里修依赖或绕过测试。

- worktree 根目录有 `setup_env.sh` 就执行 `bash setup_env.sh`；脚本未纳入 Git、只在主工作区存在时，在 worktree 目录下执行主工作区那份。成功后再派发。
- 没有脚本时不自行猜测初始化命令；按项目说明准备环境，缺失时在 brief 和报告中注明。

## 建图与 frontier

- 按 tracker 配置列出 child issues，读取每个 child 的 blockers、就绪标记和状态；未配置就绪标记时直接核对需求与验收，不自行要求标签。父 spec 不需要就绪标记，不因此阻止 Parent mode。
- blocker 已满足：达到配置的完成条件，或本次已验收并合入目标分支且合入后检查通过。父票范围外的 blocker 还要确认其代码已在目标分支上；不在时阻塞该 child 并报告，不让 Implementer 猜测或重复实现。
- **Frontier** = 符合项目就绪约定、blockers 全部满足的未结束 child。每个 child 验收合入后重新计算；已有实施中 / review 状态的续跑按项目配置处理，不强制退回 ready。

需求尚未明确、已取消或已关闭但不满足完成条件的 child 不派发，也不作为已完成的依赖；先报告并确认处置，不自动恢复已取消的任务。
“代码写完”或“测试通过”都不能解除下游 blocker，只有已验收、合入并通过检查的 child 可以。

## 是否并行

“进入 frontier”只表示**可以开始**。彼此无依赖、预期修改范围低重叠、不共享 migration / schema / generated contract，且每个 Implementer 有独立 worktree 时才并行；否则串行。主工作区的合入与集成检查始终由 Controller 串行执行。

## 每个 child 的生命周期

1. 配置有对应状态时，标记 child in-progress。
2. Controller 创建 worktree 并完成初始化，派 **Implementer sub-agent**。它看不到 Controller 的上下文，brief 中给出：
   - child issue 全文，以及 parent spec 中相关约束；
   - worktree 路径、branch、固定 baseline commit，以及 blockers 已完成的事实；
   - 环境初始化结果、开发验证指引的位置，以及本次范围对应的检查和前置条件；
   - 实现纪律：[implementation.md](implementation.md)，写测试时加 [tdd.md](tdd.md)，涉及设计时加 [codebase-design.md](codebase-design.md)，给路径或直接附内容；
   - 要求：在自己的 branch 提交；不修改 tracker；返回 commits、运行过的验证命令与结果、未解决项。
3. 核对 child branch 的 commits 确实基于 baseline；配置有对应状态时标记 in-review。按 [review.md](review.md) 派一个**未参与该 child 实现的独立 Reviewer**，review 范围是 baseline 到固定的 child HEAD，记录审查通过的 commit。
4. review fail：findings 交回 Implementer 修复，再独立复审。原 Implementer 无法继续时，在同一 child worktree 上派新的 Implementer，附原 brief、当前 diff 和 findings。未通过的 child 不解锁下游。
5. review pass：运行 child 要求的完整 verification，确认交付内容仍是已审查 commit，按上文在主工作区合入并检查，然后才按配置推进完成状态。commit hook 或冲突解决改变了内容时，补做受影响的 review 与验证。
6. 按下文清理该 child 的 worktree，然后重新计算 frontier。

## 暂停与恢复

按 [handoff.md](handoff.md) 的权限与格式交接，Parent 额外记录：主工作区路径、目标分支、原始起点和当前 HEAD，各 child 的 baseline、已审查 commit、已合入 / 待 review / 受阻状态，以及遗留 worktree 和存活 sub-agent。
恢复时对照 Git 历史、worktree、存活任务与 tracker，核实已审查 / 已合入的 commits 和合入后验证；不能只凭 merge commit 认定 child 已完成。不重复派发仍在工作的 child，也不重复合入已合入内容。
分支切换、历史被改写或出现记录外的提交时先核对并说明，不重置目标分支或把当前 HEAD 当成新起点。integration review 始终覆盖原始起点到实际目标 HEAD；HEAD 再次变化时补做受影响的审查与验证。
暂停时保留未完成 worktree；已验收合入并通过检查的 child 正常清理。明确报告目标分支已经合入的部分成果，以及尚未通过的 child / parent 验收，不将部分合入当作父任务完成。

## 清理

child 合入目标分支且合入后的检查通过后，Controller 确认该 child 的 sub-agent 都已结束工作，再清理：

1. 执行 `git -C <主工作区> worktree remove <path>`；它会同时移除 Git 登记和实际目录。
2. 命令成功后核对 `<path>` 已不存在，不能只检查 `git worktree list`。若仍有残留目录，先查看内容并确认它是本轮创建的子 worktree 路径、已不再被 Git 登记；空目录用 `rmdir -- <path>`，仅含已确认可删除的本轮生成物时用 `rm -r -- <path>`，删除后再次确认路径不存在。有未确认文件时保留并报告。
3. 确认主工作区仍检出目标分支，执行 `git -C <主工作区> branch -d <child-branch>`。

删除失败时不强制删除，也不以 `rm` 绕过失败。review 未通过、child 被阻塞或编排中途暂停时，保留其 worktree 和分支并报告路径。主工作区和目标分支不属于清理对象。

## Parent integration review 与完成

所有 child 达到完成条件后，不能直接推进 parent 到终态。

Controller 确认全部 child 已合入目标分支且主工作区没有未提交修改，运行集成检查，再按 [review.md](review.md) 启动一个**独立 Parent Integration Reviewer**。固定本次目标 HEAD，review 范围是原始起点到该 commit。它不逐票重审，只检查组合后的系统：

- parent `Proposed Changes` 是否整体兑现；
- child 之间的 public contract 是否真正接通；
- external contract / compatibility / migration 是否在组合后仍成立；
- 跨 ticket 的状态机、生命周期和错误语义是否一致；
- 是否出现只有组合后才暴露的回归、重复实现或 scope gap；
- parent-level acceptance criteria 是否满足。

review fail 时：某个已验收 child 实际未满足自己的 contract，就按配置重新打开该 child；纯跨 child 的集成问题由 Controller 指派 integration fix，不偷偷改 parent spec。需要修复时，从目标分支当前 HEAD 创建新的修复子 worktree，走相同的实现、独立 review、合入和清理流程，不要求恢复已删除的子 worktree。

integration review 通过后，在主工作区运行 parent-level tests / smoke / end-to-end verification，确认验证和审查覆盖同一目标 HEAD。全部通过且项目完成条件满足后才推进 parent 到终态；用户要求父任务关票留到 finish 时，保留父状态并报告待办，不自动调用 finish。报告目标分支、实际 commits、验证和遗留子 worktree；不另执行父分支合入或删除主工作区。
