# Project configuration reference

项目说明指向的已有 tracker 配置（缺失时默认 `docs/agents/issue-tracker.md`）是当前业务 repo 的 tracker 契约，供 `to-spec` 和 `implement` 读取。

推荐保持自然语言、短小、可人工维护，不强制 schema。

## GitHub 示例

```markdown
# Issue tracker

- Provider: GitHub Issues
- Repository: owner/repo
- Read/write: authenticated GitHub connector or gh CLI
- Spec: small work uses one issue; large work uses parent spec + child issues
- Parent/child: GitHub sub-issues when available; otherwise explicit Parent links
- Blockers: native issue dependencies when available; otherwise explicit Blocked by links
- Workflow: use the repository's existing labels / project status; do not invent new labels
- Completion condition: closed, unless the repository's existing project workflow defines another accepted terminal state
- Controller writes workflow state; implementers/reviewers do not
```

## Linear 示例

记录 team/project、真实 workflow states、parent/sub-issue 和 blockers 的当前表达方式，以及哪一个 state 表示 blocker 已满足。

## Local markdown 示例

记录 issue 根目录、命名方式、状态字段和依赖表达。完成条件必须明确，例如 `Status: done`。

## Rules

- fork 有 origin / upstream 时核对写入目标，不能把上游误当业务 tracker。
- 不存 credentials。
- 不把 skill 自己的 repo 当业务 tracker。
- 保留已有人工约定；只补缺失语义。
- tracker 不支持原生 parent / dependency 时可以用清楚的文本关系，但不要假装创建了原生关系。
