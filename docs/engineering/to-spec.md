# To Spec

## What it does

同一个入口固化 spec 并按规模拆票。最顶部是约 10–20 行 Proposed Changes，突出外部行为、契约与兼容性。
小任务一张 issue；大任务父 spec + 可独立验证的子 tickets。规格和执行切片职责不混用。

## When to reach for it

讨论已经明确，需要让下一轮 agent 接手实施时。也可给已有 spec 补拆票。

## Common questions

“仅 spec”不拆票；“只拆票 #123”不重写父 spec；“只预览”不发布。
已有拆分不重复确认，新的拆分与契约未决点集中展示，不重开需求访谈。
沿用项目 tracker 配置，单独安装 to-spec 也包含所有必要参考文件。

## It's working if

顶部能看出这次准备怎么改、怎么用、旧东西会不会坏，子票覆盖全部关键验收承诺且无重复创建。
