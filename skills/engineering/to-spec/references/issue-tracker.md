# Issue tracker configuration

Tracker 是每个业务项目的配置，不是必须额外安装的 skill。
沿用项目现有的 `docs/agents/issue-tracker.md`；也读取 AGENTS.md / CLAUDE.md 指向的等价文件，以及已有的 triage label / domain docs 配置。
这些文件继续支持自然语言说明，不要求迁移为新 schema，不删除旧项目配置。

## 解析目标

优先使用用户明确指定的目标，其次是项目配置。用真实仓库 remote 和可用的已授权工具核对 owner/repo 或项目。
fork 同时存在 origin/upstream 时不能把公开上游误当写入目标；也不能把安装本 skill 的仓库当业务项目。
缺少配置且上下文不能确定目标时，只确认缺失的目标信息，不强制跑 setup 流程。
可以先准备草稿；明确发布目标和授权前不远程写入，不静默改用另一平台。

GitHub、GitLab、Linear 或其他 tracker 继续遵循已有项目配置，使用该环境确实可用的 connector 或已认证 CLI。
连接不可用时保留草稿并说明未发布，不要求用户提供 token 到聊天或公开文件。

## 读取与写入

读取 issue 的完整正文、评论、标签、父子关系和阻塞状态；不是只凭搜索摘要决定实施。
更新前重读现有内容，保留非本次管理的正文、标签、状态和人工编辑。不能把陈旧副本整篇覆盖回去。
新建前检查目标项目中已有相关票；优先使用已知 URL / ID，避免重复 spec 和重复 tickets。
本地 tracker 也需先读文件并保留已有内容，不能覆盖同名票。
发布只产生计划，不代表实现完成。除非用户明确要求，不关闭父票、不替别人变更负责人或擅自迁移 tracker。

## 标签与关系

复用项目已有的标签名称和状态含义，不引入完整 triage 状态机。
仅对已定需求、可供实现的单 issue / 子票应用项目配置的 ready-for-agent；没有约定时不擅自创建该标签。
有明确 blockers 的票可以表示“规格就绪”，但必须保留 blockers，不能说“现在就能开始”。
重大未决接口 / 兼容决策不能带 ready-for-agent 发布；父 spec 不是默认的实施票。
原生 Parent / dependency 能力以工具实际支持为准，不支持时使用清楚的文本链接，不假装原生关系创建成功。

## 可选的项目配置示例

仅在用户要求配置或同意初始化后，写入业务项目的 `docs/agents/issue-tracker.md`；不覆盖已有配置。
下面是内容示例，不是要原样保留的占位值：

```markdown
# Issue tracker
- Tracker：GitHub Issues
- Repository：<明确的 owner/repo>
- Read / write：使用当前环境已授权的 GitHub connector 或 gh CLI。
- Spec：小任务单 issue；大任务父 spec + 子 tickets。
- Labels：<已有的实施就绪标签，或不用标签>
- Dependencies：优先原生关系，不支持时用 Parent / Blocked by 文本。
```

选择本地 Markdown 时记录业务项目自己的路径。现有 labels、domain glossary、ADR 位置保持不变。
不要因为 setup 命令已删除就重建或删除这些配置。
