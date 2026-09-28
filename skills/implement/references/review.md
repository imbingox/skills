# Independent review

Leaf、每个 child 和 parent integration 都必须由未参与相应实现 / 集成修改的独立 Reviewer 检查。Reviewer 只报告，不修改代码或 tracker；修复交回 Implementer。

## 分工

默认一个独立 Reviewer 分别输出 Standards 和 Spec 两轴结论。改动较大、跨多个领域或约束复杂时，Controller 可分配两个独立 Reviewer 各负责一轴；不要求每个小票都启动两份审查。
两轴都通过才算 review pass；任一轴不通过都返回修复后复审，不能以另一轴通过抵消问题。
无法启动独立 Reviewer 时报告“等待独立 review”，不能推进 tracker 完成状态。

## Controller 提供的输入

- 本参考内容或可读取路径、workspace、分支及实现前的基线 commit。
- 准确的 diff 范围：已提交部分，以及本次目标相关的 staged、unstaged 和新增文件。不能只比较 HEAD 而漏掉尚未提交的实现，也不能把原有用户修改算作本次成果。
- 目标 spec / issue 全文、验收标准、Proposed Changes、相关 parent 约束。
- 项目编码约定、相关 glossary / ADR、已运行检查及其结果。
- 涉及模块设计时附上 [codebase-design.md](codebase-design.md)；child 还需依赖基线与对应 commits。

Reviewer 先确认输入和实际内容一致；缺失 diff、验收条件或不可访问 workspace 时报告阻塞，不能默认通过。

## 两轴检查

**Standards**：是否遵守项目约定；检查命名、重复逻辑、职责、错误边界、过度抽象，以及测试是否绑定实现细节。区分明确规则违反与设计建议，不把个人偏好当阻塞项。

**Spec**：验收条件是否完整实现，外部契约、默认值、错误语义与兼容承诺是否兑现；指出缺失、错误实现与 scope creep。结论引用实际 diff 和规格依据。

返回格式：

```text
Reviewed: workspace / baseline / commit 或未提交 diff 范围
Standards: pass | fail | blocked
Findings: 严重程度、文件位置、规则依据、影响
Spec: pass | fail | blocked
Findings: 严重程度、文件位置、验收依据、影响
Verification gaps: 未运行或无法验证的检查
```

修复后检查新 diff 和原 findings 是否解决；修复引入其他变化时一并审查。review pass 不替代 Controller 的最终 verification。

## Parent integration

输入必须包含 parent 验收要求、child 交付记录和集成后的实际内容。重点按 [orchestration.md](orchestration.md) 检查组合后的接口衔接、生命周期、错误与迁移语义及整体范围，不重复逐票审查。仍分别报告 Standards 和 Spec；组合出现缺陷时交回对应 Implementer 或专门的 integration fix，再复审。
