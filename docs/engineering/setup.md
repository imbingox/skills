# Setup

## What it does

`/setup` 是每个 repo 一次的 bootstrap 入口。

它首先配置当前项目的 issue tracker、workflow completion condition 和 domain docs；随后幂等检查本机 Codex / Claude statusline。已有用户级 statusline 永远优先，不自动覆盖。

## When to reach for it

- 第一次在一个 repo 使用 `grill-with-docs / to-spec / implement`；
- repo 更换 issue tracker；
- tracker workflow / dependency 表达发生变化；
- 新机器上第一次运行本套 skills。

日常开发不需要反复运行。

## Common questions

**为什么一个 setup 同时碰 repo 和 CLI？** 用户入口保持一个；project setup 是每 repo 必做，CLI 是幂等检查，已配置就 no-op。

**statusline 会覆盖我现有的吗？** 不会。只在缺失时提议添加，写前展示 diff、确认并备份。

**issue 放哪？** 由当前 repo 的 `docs/agents/issue-tracker.md` 定义。后续 `to-spec` 和 `implement` 只消费这个配置，不自己猜。

## It's working if

完成后当前 repo 有明确的 tracker target、parent/dependency 和 completion 语义，domain docs 路径明确；Codex / Claude 已有 statusline 被保留，缺失配置只在用户确认后安全补齐。
