---
name: implement
description: "按已确认的 issue / spec 或明确的小任务实施。Leaf 自动实现并交给独立 reviewer；Parent 自动编排子 issue DAG、独立 review 每个子票并做最终 integration review。支持中断续跑，Controller 独占 workflow state。"
disable-model-invocation: true
---

# Implement

实现用户指定的 issue / spec，或直接接受目标、兼容边界和验收已明确的小任务；不把实施阶段变成重新设计需求的机会。默认用中文报告，保留项目已有技术标识符。
小任务可直接进入 Leaf mode，不强制先运行 grill / to-spec / setup 或创建 issue；在当前对话简要记录已确认的目标与验收，缺少关键决策时先问，不自行补产品行为。简短路径不减免独立 review、验证或原有授权边界。

> **Controller 管状态，Implementer 写代码，Reviewer 独立验收。** 每份实现都由没有参与该实现的独立 reviewer agent 审查；只有 Controller 可以改变 issue workflow state。

## 1. 读取目标并自动选择模式

读取项目 `AGENTS.md` / `CLAUDE.md`、相关 glossary / ADR、目标 issue / spec 全文及评论，以及项目 tracker 配置（项目说明指向的文件，其次 `docs/agents/issue-tracker.md`）。读取 issue、列子票、读 blocker、推进状态和关闭都按该配置中的操作执行；配置只有自然语言描述、缺少具体命令时（例如旧版 setup 生成的配置），按其描述用对应 provider 的标准工具执行，并建议重跑 `/setup` 补齐；不因此阻塞。目标在远程 tracker 上但找不到配置时，不写任何状态，提示先运行 `/setup`；不要自行猜 repo 或状态机。

读取 `Proposed Changes`（旧 spec 没有也正常）、完整验收条件、父子关系和真实 blockers；直接文本任务只读取存在的材料，不补造 spec / tracker。续跑时先按第 6 节核对交接与实际状态，然后自动选择：

- **Leaf mode**：目标没有需要编排的 child issues，直接实现当前目标。
- **Parent mode**：目标有 child issues，读取 [orchestration.md](references/orchestration.md)，当前 session 作为 Controller，用当前 harness 的 sub-agent 完成整组编排，无需用户额外开启。

已有 issue graph 是已确认的执行计划：默认**不重新拆票、不重排需求、不自行新增产品决策**。
发现 blocker 错误、子票无法独立完成、spec 与代码事实冲突，或必须改变 external contract 时，暂停受影响分支并向用户说明。

## 2. Workflow state 的唯一 owner

当前 `/implement <target>` session 是 **Controller**，也是目标及本次编排范围内 child issues 唯一的 workflow-state writer。状态、labels、终态和完成条件都来自 tracker 配置，不由本 skill 发明；没有中间状态时只在内部记录进度。

- Implementer 只返回实现事实、commit 和验证结果；Reviewer 只返回 verdict 和 findings。两者都不 close issue、不改状态、不解除 blocker。
- 一个 issue 只有在独立 review 通过、要求的 verification 通过、交付内容与审查内容一致后，才推进到完成状态。
- 每次写 tracker 前重读该对象及其依赖 / 状态，只提交本次必要的最小变更，写后读回核对。人工改动使计划或状态转换失效时，暂停受影响分支并说明，不用旧快照覆盖；写入失败时如实报告，不假报推进成功。

用户要求“不改 tracker / 不关 issue”时照做，review gate 不变，并报告本来会执行的状态转换。

## 3. Leaf mode

主 session 同时是 Controller 和 Implementer；**Reviewer 必须是独立 sub-agent**。

1. 按项目配置核对实施就绪、确认 blockers 已满足；未配置就绪标记时直接核对需求与验收，不自行要求标签。需求尚未明确时暂停，不因用户给了编号就猜测实现。记录起点 commit、当前分支和已有的未提交修改。
2. 配置有对应状态时，标记 in-progress。
3. 按第 4 节实现，持续运行相关测试 / typecheck。
4. 配置有对应状态时标记 in-review；读取 [review.md](references/review.md)，启动未参与实现的独立 Reviewer。
5. 任一轴不通过：修复后交给独立 Reviewer 复审。
6. 两轴通过后运行最终 verification，把本次目标范围的修改提交到当前分支并记录 commit。提交失败不能宣告已交付；commit hook 改变内容时，补做受影响的 review 与验证。
7. 按 tracker 配置推进完成状态。

用户明确要求“不提交”时保留未提交修改并如实报告；若完成条件要求 commit，则不推进终态。
当前 harness 无法启动独立 reviewer agent 时，可以完成实现和测试，但报告“等待独立 review”，不推进完成状态。

## 4. 实现纪律

本节同时约束 Parent mode 中的 Implementer sub-agent。

选择最小充分实现：

- 先读相关代码、真实调用链和约束，再判断是否需要新增代码；不能用小 diff 代替理解问题。
- 先复用项目已有实现，再看标准库、平台原生能力和已安装依赖；检查围绕当前任务，不扩展成全库审计。
- 确实存在缺口才新增代码或依赖。新增通用层、工厂、配置项或扩展点要有当前用例或明确约束支撑；单一实现本身不是删除已有接口的理由，已有隔离边界、测试 seam 和项目约定仍可能需要它。
- 以完整满足契约为前提减少维护负担，不追求最少行数；不牺牲可读性、信任边界校验、安全、可访问性、防数据丢失处理和必要验证。
- 验收满足且 review / verification 通过后停止扩展，不顺手重构相邻模块。

测试与开发指引：

- 实施前核对本次涉及的开发说明、manifest、lockfile、任务脚本和 CI，确认命令、工作目录与环境前置条件；不每次扫描全项目。说明与实际入口冲突时先查明原因，不能用过时命令、编造脚本或跳过失败检查制造通过。
- 写测试前读取 [tdd.md](references/tdd.md)，能 TDD 时按垂直切片：`一条行为测试 → 因目标行为缺失而失败 → 最小实现使其通过 → 下一条`。修 bug 先写能复现问题的 regression test。
- 覆盖关键成功、失败、兼容 / migration 和异步状态路径，不要求穷举边界。纯文档、配置或无法合理 TDD 的工作用静态检查 / smoke test，并说明验证限制。
- 按改动范围选检查：单模块跑相关测试 / typecheck，跨模块或接口改动覆盖两侧与契约，构建 / 依赖改动检查构建；完成前仍运行项目明确要求的全量 gate。没有测试或环境不支持时报告缺口，没实际运行的检查不能记为通过。
- 新增技术栈、改变启动 / 测试 / 构建方式时，本次交付包含必要的验证入口、原开发说明及受影响的已有 CI 同步。命令事实留在项目脚本中，指引只补来源、选择规则与前置条件，不另建注册表；保留仍在使用的旧技术栈检查，无需重跑 setup。
- 完成前核对新增 / 修改的入口确实可用，说明已运行的验证和剩余限制；不为完善指引另起测试框架或 CI 改造项目，也不借更新说明降低原有验收要求。

涉及模块 / interface 设计、依赖组织、测试 seam 或重构时，读取并应用 [codebase-design.md](references/codebase-design.md)，不改变已确认 spec。

## 5. External contract 不得偷偷改变

保持已确认的 API、CLI、UI、config/env、输入输出、错误、默认值、完成语义、旧数据与 migration 承诺。
实现必须改变这些 contract 时，不让 Implementer 自行拍板。Controller 暂停受影响分支，说明原 contract、为什么不可行、proposed change 和 compatibility / migration 影响；取得用户确认并更新 spec 后再继续。

未经单独授权不访问生产凭据、真实账户，不下实盘订单，不运行破坏性迁移或生产发布。

## 6. Git 与交接

保护开始前已有的用户修改，不把无关工作纳入 commit。多个 sub-agent 不同时写同一个 working tree。

`/implement` 授权本次目标范围内的本地 commit 和必要的 issue workflow transitions，但**不自动授权** push、merge PR、production deploy / migration、修改目标图之外的 issue，或改写已确认 spec。

### 暂停与恢复

主动暂停、受阻或准备换 session 时，由 Controller 留一份简短交接，而不是持续追加执行流水账：

- 已完成与剩余工作，保留未决决策和 blocker。
- repo、分支 / worktree、原始起点与当前 commit；本轮及用户原有未提交改动分别说明。
- 最近验证的命令、工作目录、结果与对应 commit / 未提交工作区范围；review 是否通过、覆盖到哪里。
- 尚在运行的 sub-agent / 外部任务，以及下一步动作或需要用户决定的事项。

有已授权的目标时，按项目配置追加原 issue 评论或已有本地票；写前重读、写后核对，保留人工内容。Implementer / Reviewer 只向 Controller 返回事实，不自行写 tracker。没有票、缺配置、用户要求“不改 tracker”或写入失败时，只在当前对话交接并说明未持久化，不自动建票或另建进度文件；记录前脱敏，不为交接强行提交或清理未完成 worktree。无法在进程被强制终止前保证留下记录。

恢复时重读目标、最新评论、项目配置和交接，核对分支、worktree、当前 diff 及运行中的任务，避免重复派发。旧记录只是线索；代码、依赖或环境改变时重跑受影响验证，review 必须覆盖实际交付内容。保留原始起点，不把当前 HEAD 当成新起点；基线或状态无法核实时先说明并确认，不根据旧的“完成”直接推进状态。

### 最终报告

- 完成 / 未完成的目标或 issues；
- 每份 review 与 parent integration review 的结果；
- external contract / compatibility 的实际变化；
- verification 证据；
- commits 与集成分支；
- 任何未解决或未验证事项。
