# Issue tracker: GitHub

<!-- setup 种子模板：写入业务 repo 后替换尖括号占位，删除不适用的行。 -->

- Repository：<owner/repo>
- 工具：已登录的 `gh` CLI，或当前环境已授权的 GitHub connector。所有命令显式指定 repo（`-R <owner/repo>` 或 `repos/<owner>/<repo>`），避免在 fork 中解析到 upstream。
- Spec：小任务一张 issue 同时承载 spec 与验收；大任务用父 spec issue + 子 issues。

## 操作

| 操作 | 命令 |
| --- | --- |
| 读取 | `gh issue view <n> -R <owner/repo> --json number,title,body,state,labels,assignees,comments` |
| 查重 | `gh issue list -R <owner/repo> --state all --search "<关键词> in:title" --json number,title,state` |
| 新建 | `gh issue create -R <owner/repo> --title "<title>" --body-file <file>`；输出 URL 末尾是编号 |
| 更新正文 | 先重新读取，再 `gh issue edit <n> -R <owner/repo> --body-file <file>` |
| 评论 | `gh issue comment <n> -R <owner/repo> --body-file <file>` |
| 取 database id | `gh api repos/<owner>/<repo>/issues/<n> --jq .id`；子票和依赖 API 用它，不用 `#number` |
| 挂子票 | `gh api -X POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-id>` |
| 列子票 | `gh api repos/<owner>/<repo>/issues/<parent>/sub_issues --jq 'map({number, title, state})'` |
| 加 blocker | `gh api -X POST repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by -F issue_id=<blocker-id>` |
| 读 blocker | `gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by --jq 'map({number, state})'` |
| 推进状态 | 按下方 Workflow 的状态表达：改 label 用 `gh issue edit <n> -R <owner/repo> --add-label "<label>" --remove-label "<label>"`；Project Status 用 `gh project item-edit` |
| 关闭 | `gh issue close <n> -R <owner/repo> --comment "<交付摘要>"` |
| 重新打开 | `gh issue reopen <n> -R <owner/repo> --comment "<原因>"` |

Relationships：<native | text>。sub-issue 或依赖 API 不可用（404 / 422 / 未启用）时用文本关系：子票正文顶部写 `Parent: #<parent>`，父票正文维护子票 task list，依赖写 `Blocked by: #<n>, #<n>`。

## Workflow

- 状态表达：<仅 open / closed；或已有 labels，如 `in-progress`、`in-review`；或 Project <编号> 的 Status 字段及选项名>
- Ready 标签：<已有的实施就绪 label，如 `ready-for-agent`；没有则写“不使用”>
- 完成条件（满足 blocker 的依据）：issue closed<；若项目用其他终态，写明>
- Controller 可执行：<按状态表达推进 in-progress / in-review；review 与验证通过后关闭 issue；集成 review 发现已关闭 child 未满足契约时重新打开>
- 需要人工确认：<如关闭父 spec、修改 assignee、改动本次范围外的 issue>
