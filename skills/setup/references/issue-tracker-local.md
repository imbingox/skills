# Issue tracker: Local markdown

<!-- setup 种子模板：写入业务 repo 后替换尖括号占位，删除不适用的行。 -->

- 根目录：`.scratch/`（<纳入 Git | 已 gitignore>）
- 每个需求一个目录：`.scratch/<feature-slug>/`
- Spec：`.scratch/<feature-slug>/spec.md`；小任务只有这一个文件，spec 即 issue
- 子票：`.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 起按依赖顺序编号，一票一文件

每个 spec / 子票文件顶部：

```markdown
Status: open | ready | closed
Parent: <../spec.md；没有则省略>
Blocked by: <01, 02；或 None>
```

## 操作

- 读取：读整个文件，包括底部 `## Comments`。
- 查重：列出 `.scratch/` 下已有目录和文件名；同名文件不覆盖。
- 新建：按上面的路径写新文件，目录不存在时创建。
- 更新正文：先重新读取，只改本次管理的段落，保留文件头和 `## Comments`。
- 评论：在文件底部 `## Comments` 下追加带日期的条目。
- 挂子票 / 列子票：子票文件头写 `Parent`；列子票时列出 `issues/` 目录。
- 加 / 读 blocker：写或读 `Blocked by` 行；读 blocker 时再读对应文件的 `Status` 及本次关闭说明，按完成条件判断。
- 推进状态：只改 `Status:` 行，保留其余内容。
- 关闭：`Status: closed`，并在 `## Comments` 追加本次交付摘要与验收结果；取消或重复则明确写明原因，不冒充完成。
- 重新打开：把 `Status` 改回 `open`，在 `## Comments` 说明原因；需求与验收重新确认后才改为 `ready`。

## Workflow

新项目默认如下；已有 `draft` / `ready-for-agent` / `done` 等约定继续沿用，不迁移旧文件。

- 状态表达：`open` 为待明确；`ready` 为需求与验收已明确；`closed` 为已结束。新建为 `open`，父 spec 不标 ready。
- Ready：`Status: ready`；带 blocker 的票可以 ready，实施前仍须确认依赖满足。
- 完成条件（满足 blocker 的依据）：`Status: closed` 且本次关闭说明记录已验收的交付；取消、重复或放弃不自动满足依赖。
- Controller 可执行：实施与 review 进度只在内部记录；通过验收后关闭；集成 review 发现未满足契约的 child 时重开并重新确认就绪。
- 需要人工确认：<如关闭父 spec、删除或重命名已有文件>
