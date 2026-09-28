# Grill With Docs

## What it does

结合代码查事实，分轮澄清真正需要用户决定的事项，优先展示外部用法与兼容影响。
内置追问、术语整理和按需 ADR，不依赖其他 skill。

## When to reach for it

新功能、接口修改或迁移存在关键歧义，尤其是“功能可行，但最终用法还没有确定”时。

## Common questions

已经回答过的内容不会反复问；内部实现能自主解决的事项不会为了凑流程交回用户。
沿用项目已有 glossary、CONTEXT-MAP 和 ADR 位置，不强制重新 setup。

## It's working if

用户能说清最终怎么用、哪些旧行为保留、哪些明确不做，再进入 to-spec。
