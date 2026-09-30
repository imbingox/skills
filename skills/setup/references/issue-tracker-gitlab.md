# Issue tracker: GitLab

<!-- setup 种子模板：写入业务 repo 后替换尖括号占位，删除不适用的行。 -->

- Project：<group/project>
- 工具：已登录的 `glab` CLI，或当前环境已授权的 GitLab connector。所有命令显式指定 project（`-R <group/project>`；`glab api` 路径用 URL 编码的 `<group%2Fproject>`），避免在 fork 中解析到上游。
- Spec：小任务一张 issue 同时承载 spec 与验收；大任务用父 spec issue + 子 issues。

## 初始化就绪标签（仅 setup）

已有 workflow / 标签映射优先。新项目采用下方精简 workflow 时：

1. 查询：`glab api projects/<group%2Fproject>/labels --paginate --jq '.[].name'`。
2. 只有查询成功、确认缺失且用户同意后，才执行 `glab api -X POST projects/<group%2Fproject>/labels -f name=ready -f color='#0E8A16' -f description='需求与验收已明确，实施前仍需检查依赖'`；已有同名标签不覆盖。
3. 再次查询核对。创建失败或用户拒绝时，Ready 标签写“不使用”，同步删去状态表达与操作中的 ready 步骤，仍可使用原生 open / closed；不声称 ready 已配置。查询失败不能当作标签不存在。

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
| 读 blocker | `glab api projects/<group%2Fproject>/issues/<n>/links`，取 `link_type` 为 `is_blocked_by` 的项；文本关系则读 `Blocked by` 行。再读取各 blocker 的状态与本次关闭说明，按完成条件判断 |
| 设置 / 清除就绪 | `glab issue update <n> -R <group/project> --label "<ready-label>"` / `--unlabel "<ready-label>"` |
| 推进状态 | 精简 workflow 只管理就绪标记及关闭 / 重开；已有其他 workflow 时记录其 scoped labels 或 board 列的实际操作 |
| 关闭 | 若含就绪标签，先按“清除就绪”移除；用 `glab issue note <n> -R <group/project> --message "<交付摘要与验收结果；取消则明确写明原因>"` 记录，再 `glab issue close <n> -R <group/project>` |
| 重新打开 | 若残留就绪标签，先清除，再 `glab issue reopen <n> -R <group/project>`，用 note 说明原因；重新确认需求与验收后才恢复就绪标记 |

Blockers：<native | text>。

## Workflow

新项目默认如下；已有 scoped labels 或 board 列时，原位记录实际映射与命令，不强制迁移。

- 状态表达：原生 open 且无 ready = 待明确；open + ready = 需求与验收已明确；原生 closed = 已结束。不创建 open / closed 标签。
- Ready 标签：`ready`（或已有的等价标签；不采用则写“不使用”）。只用于单 issue / 子票，不用于父 spec；带 blocker 的票可以 ready，实施前仍须确认依赖满足。
- 完成条件（满足 blocker 的依据）：issue closed 且本次关闭说明记录已验收的交付；取消、重复或放弃不自动满足依赖。
- Controller 可执行：实施与 review 进度只在内部记录；通过验收后清除就绪标签并关闭；集成 review 发现未满足契约的 child 时重开并重新确认就绪。
- 需要人工确认：<如关闭父 spec、修改 assignee、改动本次范围外的 issue>
