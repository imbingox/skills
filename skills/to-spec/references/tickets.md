# Ticket decomposition

此文件是 to-spec 的内置参考，不是独立 skill。
spec 记录整体目标与约束；ticket 是一次可独立验证的实施切片。拆票不能改掉父 spec 的外部契约。

## 切分规则

每票打通当前目标所需的完整路径，例如输入、状态、API、UI 与测试；不是要求每个任务都必须包含所有层。
每票在一个 fresh context 内可理解和实施，完成后能展示或验证自身交付物。
仅当预重构确实解除后续阻碍时单独拆票，不制造无交付意义的脚手架票。
依赖只记录真实前置条件，不能把所有票无理由串成一条链。

广泛的机械重构可以例外：需要保持兼容时采用 expand → 分批 migrate → contract。
不要为了套该模式擅自新增永久兼容层。父 spec 已允许 breaking change 时，遵守其迁移方式。
分批无法独立保持验证通过时，明确共同 integration branch 和最终集成验收票，不能假称每批可独立发布。

## 先给人看的拆分

| Ticket | 交付行为 | Blocked by |
| --- | --- | --- |
| T1 | 一个可独立验证的结果 | None |
| T2 | 下一个结果 | T1 |

与 Proposed Changes 一起确认粒度和必要依赖，不另开一轮完整访谈。
已确认的拆分直接沿用；拆分不能增加未经确认的接口字段、默认值、兼容策略或实现范围。

## 每票正文

```markdown
## Proposed Changes
- Change：本票交付的外部行为。
- Contract / Compatibility：本票涉及的契约与兼容承诺，或 None。

## Parent
<父 spec 的真实引用；没有父 spec 时省略>

## What to build
<本票的端到端交付，以及不包含的相邻工作>

## Acceptance criteria
- [ ] <可观察、可验证的结果>
- [ ] <适用的失败路径与兼容场景>

## Blocked by
<真实阻塞票的引用，或 None>
```

子票摘要通常 2–5 行，不把父 spec 的 10–20 行摘要复制到每张子票。
子票保留本票所需的约束与父引用，不复制整篇父文档。
每个父 spec 的关键验收承诺必须落到某票或明确的集成验收中；不得因拆票遗漏兼容、迁移、错误或状态语义。

发布顺序、关系表达和查重见 [issue-tracker.md](issue-tracker.md)。本地 tracker 的路径与文件头按项目配置，一票一文件。
