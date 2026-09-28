# Issue tracker: GitLab

<!-- setup 种子模板：写入业务 repo 后替换尖括号占位，删除不适用的行。 -->

- Project：<group/project>
- 工具：已登录的 `glab` CLI，或当前环境已授权的 GitLab connector。所有命令显式指定 project（`-R <group/project>`；`glab api` 路径用 URL 编码的 `<group%2Fproject>`），避免在 fork 中解析到上游。
- Spec：小任务一张 issue 同时承载 spec 与验收；大任务用父 spec issue + 子 issues。

## 操作

| 操作 | 命令 |
| --- | --- |
| 读取 | `glab issue view <n> -R <group/project> --comments`；机器可读用 `-F json` |
| 查重 | `glab issue list -R <group/project> --all --search "<关键词>" -F json` |
| 新建 | `glab issue create -R <group/project> --title "<title>" --description "$(cat <file>)" --yes` |
| 更新正文 | 先重新读取，再 `glab issue update <n> -R <group/project> --description "$(cat <file>)"` |
| 评论 | `glab issue note <n> -R <group/project> --message "..."` |
| 挂子票 / 列子票 | 子票描述顶部写 `Parent: #<parent>`，父票描述维护子票 task list；列子票时读父票 task list |
| 加 blocker | `glab issue note <n> -R <group/project> --message "/blocked_by #<blocker>"`（需 Premium 及以上）；否则在描述顶部写 `Blocked by: #<n>, #<n>` |
| 读 blocker | `glab api projects/<group%2Fproject>/issues/<n>/links`，取 `link_type` 为 `is_blocked_by` 的项；文本关系则读 `Blocked by` 行 |
| 推进状态 | 按下方 Workflow 的状态表达：`glab issue update <n> -R <group/project> --label "<label>" --unlabel "<label>"` |
| 关闭 | 先 `glab issue note <n> -R <group/project> --message "<交付摘要>"`，再 `glab issue close <n> -R <group/project>` |
| 重新打开 | `glab issue reopen <n> -R <group/project>`，再用 note 说明原因 |

Blockers：<native | text>。

## Workflow

- 状态表达：<仅 open / closed；或已有 scoped labels，如 `workflow::in-progress`；或 board 列>
- Ready 标签：<已有的实施就绪 label；没有则写“不使用”>
- 完成条件（满足 blocker 的依据）：issue closed<；若项目用其他终态，写明>
- Controller 可执行：<按状态表达推进；review 与验证通过后关闭 issue；集成 review 发现已关闭 child 未满足契约时重新打开>
- 需要人工确认：<如关闭父 spec、修改 assignee、改动本次范围外的 issue>
