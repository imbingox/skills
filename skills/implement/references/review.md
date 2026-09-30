# Independent review

Leaf、每个 child 和 parent integration 都由未参与相应实现 / 集成修改的独立 Reviewer 检查。Reviewer 只报告，不修改代码或 tracker；修复交回 Implementer。改编自 Matt 的 code-review skill。

## 分工

默认一个独立 Reviewer 分别给出 Standards 和 Spec 两轴结论。改动较大、跨多个领域或约束复杂时，Controller 可以并行派两个 Reviewer 各负责一轴；小票不必启动两份审查。
两轴都通过才算 review pass；任一轴不通过都修复后复审，不以另一轴通过抵消。
无法启动独立 Reviewer 时报告“等待独立 review”，不推进完成状态。

## Controller 提供的输入

Reviewer 看不到 Controller 的上下文，所需材料都写进 brief：

- 本参考的路径或内容，以及 workspace 与分支。
- 固定的 diff 范围。Leaf 在提交前 review：`git diff <起点 commit>`（含已暂存与未暂存改动）加本次新增的未跟踪文件；开始前已有的用户修改不算本次成果。Parent child 已在自己的 branch 提交：`git diff <baseline>...<child-commit>` 和 `git log --oneline <baseline>..<child-commit>`；Parent integration 用 `git diff <编排起点> <固定的目标分支-commit>`，在主工作区审查该版本，不能把未提交修改当作交付内容。
- 目标 spec / issue 全文、验收条件、Proposed Changes 和相关 parent 约束。
- 项目编码约定来源（如 AGENTS.md、CONTRIBUTING.md）、相关 glossary / ADR、已运行的检查及结果。
- 涉及模块设计时附上 [codebase-design.md](codebase-design.md)。

派发前 Controller 确认基线可解析（`git rev-parse <baseline>`）且 diff 非空。Reviewer 发现缺少 diff、验收条件或 workspace 不可访问时报告 blocked，不默认通过。

## Standards

- **项目明文规则**：违反即 finding，引用规则出处；lint / formatter 已强制的不重复报告。
- **新增复杂性**：是否重复已有代码、标准库或平台能力，是否引入没有当前用途的依赖、配置或扩展层。精简 finding 要给出位置、当前需求依据和行为等价的替代；不能仅凭单一调用方或能少几行判 fail，也不能以精简为由删除必要校验和测试。只看本次 diff 及其影响。
- **测试**：是否经 public seam 观察行为，有无 [tdd.md](tdd.md) 中的反模式。

## 阻塞与建议

正确性缺陷、验收或兼容承诺遗漏、项目明文规则违规，以及有具体影响的复杂性或测试问题才作为阻塞 finding。每项给出位置、依据和实际影响；有未解决的阻塞 finding 则该轴 fail，缺少必要输入或证据而无法判断则 blocked。
命名偏好、可选重构和没有实际影响依据的代码坏味道仅作建议，不导致 fail，不要求为通过 review 扩大范围。两轴各自无阻塞问题且有足够依据时为 pass。

## Spec

逐条核对验收条件，以及外部契约、默认值、错误语义与兼容承诺是否兑现。报告缺失或部分实现、看似实现但有误、spec 没要求的行为（scope creep），每条引用 spec 原文和 diff 位置。

## 返回格式

两轴分开报告，每轴约 400 字以内；不合并、不跨轴排序，因为一轴通过可能掩盖另一轴的问题。

```text
Reviewed: workspace / baseline / commit 或未提交 diff 范围
Standards: pass | fail | blocked
Findings: 阻塞 / 建议、严重程度、文件位置、规则依据、影响
Spec: pass | fail | blocked
Findings: 阻塞 / 建议、严重程度、文件位置、spec 原文、影响
Verification gaps: 未运行或无法验证的检查
```

复审时检查原 findings 是否解决，以及修复带来的新变化。review pass 不替代 Controller 的最终 verification。

## Parent integration

输入包含 parent 验收要求、各 child 的交付记录和目标分支上的实际内容。按 [orchestration.md](orchestration.md) 的检查清单审查组合后的接口衔接、生命周期、错误与迁移语义及整体范围，不逐票重审；仍分别报告 Standards 和 Spec。
