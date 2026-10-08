# Ticket 增量规则

拆票时与 Matt `to-tickets` 原文一起使用；本文件只写增量，冲突时以本文件为准。
spec 记录整体目标与约束；ticket 是一次可独立验证的实施切片。拆票不能改掉父 spec 的外部契约。

## 切分

- 沿用 Matt 的 vertical slice、prefactor 先行和 expand–contract 规则。不为套用 expand–contract 擅自新增永久兼容层；父 spec 已允许 breaking change 时遵守其迁移方式。
- 依赖只记录真实前置条件，不无理由串成一条链。
- 拆分表与 Proposed Changes 同轮确认，替代 Matt 的单独 quiz。已确认的拆分直接沿用，不增加未经确认的接口字段、默认值、兼容策略或实现范围。

## 每票正文

在 Matt issue 模板（Parent / What to build / Acceptance criteria / Blocked by）顶部增加：

```markdown
## Proposed Changes
- Change：本票交付的外部行为。
- Contract / Compatibility：本票涉及的契约与兼容承诺，或 None。
- Before → After：同一具体输入 / 操作在本票交付前后的可观察结果。
- Seams：本票验收使用的、父 spec 已确认的 seam。
```

- 摘要通常 2–5 行，不复制父 spec 的整段摘要或全文，只保留本票所需的约束与父引用。
- 发布前逐条核对：父 spec 的每项关键验收承诺（含兼容、迁移、错误与状态语义）都落到某票或明确的集成验收中；有遗漏先补票或补验收。
- 父 spec 不设就绪标记。发布顺序、关系表达和查重见 [issue-tracker.md](issue-tracker.md)；本地 tracker 的路径与文件头按项目配置，一票一文件。
