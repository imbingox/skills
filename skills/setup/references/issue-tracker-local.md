# Issue tracker: Local markdown

<!-- setup 种子模板：写入业务 repo 后替换尖括号占位，删除不适用的行。 -->

- 根目录：`.scratch/`（<纳入 Git | 已 gitignore>）
- 每个需求一个目录：`.scratch/<feature-slug>/`
- Spec：`.scratch/<feature-slug>/spec.md`；小任务只有这一个文件，spec 即 issue
- 子票：`.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 起按依赖顺序编号，一票一文件

每个 spec / 子票文件顶部：

```markdown
Status: draft | ready-for-agent | in-progress | in-review | done
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
- 加 / 读 blocker：写或读 `Blocked by` 行；读 blocker 时再读对应文件的 `Status`。
- 推进状态：只改 `Status:` 行，保留其余内容。
- 关闭：`Status: done`，并在 `## Comments` 追加交付摘要。
- 重新打开：把 `Status` 改回 `in-progress`，在 `## Comments` 说明原因。

## Workflow

- Ready：`Status: ready-for-agent`
- 完成条件（满足 blocker 的依据）：`Status: done`
- Controller 可执行：`in-progress` → `in-review` → `done`；集成 review 发现已完成 child 未满足契约时改回 `in-progress`
- 需要人工确认：<如删除或重命名已有文件>
