# Issue tracker: GitHub

<!-- setup 种子模板：写入业务 repo 后替换尖括号占位，删除不适用的行。 -->

- Repository：<owner/repo>
- 工具：已登录的 `gh` CLI，或当前环境已授权的 GitHub connector。所有命令显式指定 repo（`-R <owner/repo>` 或 `repos/<owner>/<repo>`），避免在 fork 中解析到 upstream。
- Spec：小任务一张 issue 同时承载 spec 与验收；大任务用父 spec issue + 子 issues。

## 初始化就绪标签（仅 setup）

已有 workflow / 标签映射优先。新项目采用下方精简 workflow 时：

1. 查询：`gh api repos/<owner>/<repo>/labels --paginate --jq '.[].name'`。
2. 只有查询成功、确认缺失且用户同意后，才执行 `gh label create ready -R <owner/repo> --color 0E8A16 --description "需求与验收已明确，实施前仍需检查依赖"`；已有同名标签不覆盖。
3. 再次查询核对。创建失败或用户拒绝时，Ready 标签写“不使用”，同步删去状态表达与操作中的 ready 步骤，仍可使用原生 open / closed；不声称 ready 已配置。查询失败不能当作标签不存在。

## 操作

| 操作 | 命令 |
| --- | --- |
| 读取 | `gh issue view <n> -R <owner/repo> --json number,title,body,state,stateReason,labels,assignees,comments` |
| 查重 | `gh issue list -R <owner/repo> --state all --search "<关键词> in:title" --json number,title,state` |
| 新建 | `gh issue create -R <owner/repo> --title "<title>" --body-file <file>`；输出 URL 末尾是编号 |
| 更新正文 | 先重新读取，再 `gh issue edit <n> -R <owner/repo> --body-file <file>` |
| 评论 | `gh issue comment <n> -R <owner/repo> --body-file <file>` |
| 取 database id | `gh api repos/<owner>/<repo>/issues/<n> --jq .id`；子票和依赖 API 用它，不用 `#number` |
| 挂子票 | `gh api -X POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-id>` |
| 列子票 | `gh api repos/<owner>/<repo>/issues/<parent>/sub_issues --jq 'map({number, title, state})'` |
| 加 blocker | `gh api -X POST repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by -F issue_id=<blocker-id>` |
| 读 blocker | `gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by --jq 'map({number, state, state_reason})'`，再读取各 blocker 的本次关闭说明，按完成条件判断 |
| 设置 / 清除就绪 | `gh issue edit <n> -R <owner/repo> --add-label "<ready-label>"` / `--remove-label "<ready-label>"` |
| 推进状态 | 精简 workflow 只管理就绪标记及关闭 / 重开；已有其他 workflow 时记录其 label 或 Project Status 的实际操作 |
| 关闭 | 若含就绪标签，先按“清除就绪”移除；验收交付后 `gh issue close <n> -R <owner/repo> --reason completed --comment "<交付摘要与验收结果>"`；取消则用 `--reason "not planned"` 并说明原因 |
| 重新打开 | 若残留就绪标签，先清除，再 `gh issue reopen <n> -R <owner/repo> --comment "<原因>"`；重新确认需求与验收后才恢复就绪标记 |

Relationships：<native | text>。sub-issue 或依赖 API 不可用（404 / 422 / 未启用）时用文本关系：子票正文顶部写 `Parent: #<parent>`，父票正文维护子票 task list，依赖写 `Blocked by: #<n>, #<n>`。

## Workflow

新项目默认如下；已有 labels 或 Project Status 时，原位记录实际映射与命令，不强制迁移。

- 状态表达：原生 open 且无 ready = 待明确；open + ready = 需求与验收已明确；原生 closed = 已结束。不创建 open / closed 标签。
- Ready 标签：`ready`（或已有的等价标签；不采用则写“不使用”）。只用于单 issue / 子票，不用于父 spec；带 blocker 的票可以 ready，实施前仍须确认依赖满足。
- 完成条件（满足 blocker 的依据）：issue closed，关闭原因是 completed，且本次关闭说明有已验收的交付依据；取消、重复或放弃不自动满足依赖。
- Controller 可执行：实施与 review 进度只在内部记录；通过验收后清除就绪标签并关闭；集成 review 发现未满足契约的 child 时重开并重新确认就绪。
- 需要人工确认：<如关闭父 spec、修改 assignee、改动本次范围外的 issue>
