# Parent orchestration

Parent mode 下主 session 只做 Controller：建图、派发、集成、推进状态；每个 child 由 Implementer sub-agent 实现，不把整张父票当成一份大实现。

本模式依赖本地 commit 来审查与集成。用户要求“不提交”时，在创建分支或派发前说明这一限制，不创建 commit，也不将其解释为“只留集成分支”；等待用户明确允许本地提交或调整任务范围。用户要求“只留集成分支”则允许本地 commit，但不更新当前分支。

## 集成分支与集成 worktree

- 首次执行时记录当前分支、起点 commit 和主工作区已有的未提交修改。这些修改只留在主工作区，不进入任何 worktree 或 commit。
- 首次执行时从当前分支 HEAD 创建本地**集成分支** `implement/<parent>`，并在专门的**集成 worktree** 中检出：`git worktree add -b implement/<parent> <集成 worktree 路径> HEAD`。所有合入和集成检查都在这里进行，不在主工作区执行 checkout 或 merge。
- `implement/<parent>` 已存在或交接表明任务未完成时，先按下文“暂停与恢复”核对，复用已确认的分支与 worktree；不直接重建分支，不把当前 HEAD 重置为起点。
- 每个 child 在从集成分支当前 HEAD 创建的独立 worktree / branch 中实现，创建方式见“Sub-agent 与 worktree”。
- child 验收后，Controller 在集成 worktree 中用 `git merge --no-ff <child-branch>` 合入并运行相关检查，然后才解锁下游。保留已审查的 commits，不 squash、不 rebase，否则后续无法确认合入内容就是审查内容，清理时分支也无法被识别为已合并。
- 下游从合入后的集成分支创建 worktree，因此自带全部已验收依赖；未验收 child 的成果不合入。
- 合入冲突由 Controller 解决并重跑检查；解决方式改变了已验收行为时，先经独立 review 再继续。
- 本地集成不代表授权 push 或 merge PR。

## Sub-agent 与 worktree

只使用当前 harness 的 sub-agent 能力。无法启动 sub-agent 时，暂停编排并说明，不由 Controller 接管整张父票的实现。

worktree 由 Controller 创建：`git worktree add -b <child-branch> <path> implement/<parent>`，再把路径和分支写进 brief，要求 sub-agent 只在该路径内工作：shell 的 cwd 可能在每次调用后重置，命令一律用绝对路径或 `git -C <path>`。不使用 harness 自动创建的隔离 worktree，因为它的基线和分支名无法事先确定。

## 新 worktree 的环境

Controller 在创建 worktree 后、派发 Implementer 前完成初始化。初始化失败时把该 child 标记为阻塞，报告脱敏后的输出，不让 Implementer 在残缺环境里修依赖或绕过测试。

- worktree 根目录有 `setup_env.sh` 就执行 `bash setup_env.sh`；脚本未纳入 Git、只在主工作区存在时，在 worktree 目录下执行主工作区那份。成功后再派发。
- 没有脚本时不自行猜测初始化命令；按项目说明准备环境，缺失时在 brief 和报告中注明。

## 建图与 frontier

- 按 tracker 配置列出 child issues，读取每个 child 的 blockers、就绪标记和状态；未配置就绪标记时直接核对需求与验收，不自行要求标签。父 spec 不需要就绪标记，不因此阻止 Parent mode。
- blocker 已满足：达到配置的完成条件，或本次已验收并合入集成分支。父票范围外的 blocker 还要确认其代码已在集成分支上；不在时阻塞该 child 并报告，不让 Implementer 猜测或重复实现。
- **Frontier** = 符合项目就绪约定、blockers 全部满足的未结束 child。每个 child 验收合入后重新计算；已有实施中 / review 状态的续跑按项目配置处理，不强制退回 ready。

需求尚未明确、已取消或已关闭但不满足完成条件的 child 不派发，也不作为已完成的依赖；先报告并确认处置，不自动恢复已取消的任务。
“代码写完”或“测试通过”都不能解除下游 blocker，只有已验收并合入的 child 可以。

## 是否并行

“进入 frontier”只表示**可以开始**。同时满足以下条件才并行：

- 彼此没有依赖；
- 预期修改范围低重叠，不共享 migration / schema / generated contract；
- 每个 Implementer 有独立 worktree。

否则串行执行。

## 每个 child 的生命周期

1. 配置有对应状态时，标记 child in-progress。
2. Controller 创建 worktree 并完成初始化，派 **Implementer sub-agent**。它看不到 Controller 的上下文，brief 中给出：
   - child issue 全文，以及 parent spec 中相关约束；
   - worktree 路径、branch、基线 commit，以及 blockers 已完成的事实；
   - 环境初始化结果、开发验证指引的位置，以及本次范围对应的检查和前置条件（见上文）；
   - 实现纪律：[implementation.md](implementation.md)，写测试时加 [tdd.md](tdd.md)，涉及设计时加 [codebase-design.md](codebase-design.md)，给路径或直接附内容；
   - 要求：在自己的 branch 提交；不修改 tracker；返回 commits、运行过的验证命令与结果、未解决项。
3. 核对 child branch 的 commits 确实基于基线 commit；配置有对应状态时标记 in-review。按 [review.md](review.md) 派一个**未参与该 child 实现的独立 Reviewer**，review 范围是基线 commit 到 child branch HEAD。
4. review fail：findings 交回 Implementer 修复，再独立复审。原 Implementer 无法继续时，在同一 child worktree 上派新的 Implementer，附原 brief、当前 diff 和 findings。未通过的 child 不解锁下游。
5. review pass：运行 child 要求的完整 verification，在集成 worktree 中合入，确认合入内容就是已审查的内容，再按配置推进完成状态。commit hook 或冲突解决改变了内容时，补做受影响的 review 与验证。
6. 按下文清理该 child 的 worktree，然后重新计算 frontier。

## 暂停与恢复

按入口 SKILL.md 第 6 节的写入权限与格式交接，Parent 额外记录：原始主分支与起点 commit、集成分支及 HEAD、各 child 已合入 / 待 review / 受阻的状态、遗留 worktree 和尚在运行的 sub-agent，以及是否已交付主分支。
恢复时对照 Git 历史、worktree、存活任务与 tracker，核实原始起点和已审查 / 已合入的 commits；不重复派发仍在工作的 child。分支缺失或状态不一致时先说明并确认；integration review 始终覆盖原始起点到当前集成 HEAD，不因换 session 缩短范围。
暂停时保留未完成 worktree；已验收合入的 child 仍按下文正常清理。tracker 已显示完成但代码仅在集成分支的情况，必须明确交接，不能当作已交付主分支。

## 清理

child 合入集成分支且合入后的检查通过后，Controller 确认该 child 的 sub-agent 都已结束工作，再立即清理：

1. 执行 `git worktree remove <path>`；它会同时移除 Git 登记和实际目录。
2. 命令成功后核对 `<path>` 已不存在，不能只检查 `git worktree list`。若仍有残留目录，先查看内容并确认它是本轮创建的 worktree 路径、已不再被 Git 登记；空目录用 `rmdir -- <path>`，仅含已确认可删除的本轮生成物时用 `rm -r -- <path>`，删除后再次确认路径不存在。有未确认文件时保留并报告。
3. 在集成 worktree 中执行 `git branch -d <child-branch>`。在主工作区执行会按当前分支判断是否已合并，因而失败。

删除失败（有未提交内容、分支未被识别为已合并）时不强制删除，也不以 `rm` 绕过失败，保留并在最终报告中列出。review 未通过、child 被阻塞或编排中途暂停时，保留 worktree 和分支并报告路径，方便检查。

## Parent integration review

所有 child 达到完成条件后，不能直接推进 parent 到终态。

Controller 确认全部 child 已合入集成分支，在集成 worktree 中运行集成检查，再按 [review.md](review.md) 启动一个**独立 Parent Integration Reviewer**，review 范围是起点 commit 到集成分支 HEAD。它不逐票重审，只检查组合后的系统：

- parent `Proposed Changes` 是否整体兑现；
- child 之间的 public contract 是否真正接通；
- external contract / compatibility / migration 是否在组合后仍成立；
- 跨 ticket 的状态机、生命周期和错误语义是否一致；
- 是否出现只有组合后才暴露的回归、重复实现或 scope gap；
- parent-level acceptance criteria 是否满足。

review fail 时：某个已验收 child 实际未满足自己的 contract，就按配置重新打开该 child 并交回修复；纯跨 child 的集成问题由 Controller 指派 integration fix，不偷偷改 parent spec。修复后复审。

integration review 通过后，在集成 worktree 中运行 parent-level tests / smoke / end-to-end verification。

## 交付到当前分支

全部通过后：

- **正常模式**：在主工作区执行 `git merge --ff-only implement/<parent>`，把当前分支快进到集成结果。当前分支已前进、或与主工作区的未提交修改冲突时，git 会拒绝：不要强制、不要 stash 用户修改，保留集成分支并报告。
- **“只留集成分支”模式**：结果只留在本地分支 `implement/<parent>`，当前分支不动。

交付成功后删除集成 worktree（`git worktree remove`），按上文清理规则核对实际目录已删除；正常模式下再 `git branch -d implement/<parent>`，“只留集成分支”模式保留该分支。最后核对项目完成条件是否已满足，再按配置推进 parent 到终态；若要求交付当前分支而尚未完成，则保留 parent 状态。核对本次创建的 worktree 都已清理，或已列入报告。

快进失败或处于“只留集成分支”模式时，已按配置完成的 child 在 tracker 上显示完成，代码却只在 `implement/<parent>` 上：最终报告必须明确写出这一点和该分支名。
