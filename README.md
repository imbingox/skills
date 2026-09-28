# Bingo Skills

基于 [mattpocock/skills](https://github.com/mattpocock/skills) 的公开精简 fork，保留原 MIT 许可与来源。
中文优先，面向日常 agent 开发：先确认怎么用、兼容什么，再让 agent 实现。

## 使用方式

每个 repo 首次运行一次：

```text
/setup
```

之后日常只走：

```text
grill-with-docs → to-spec → implement
```

| 入口 | 做什么 |
| --- | --- |
| [setup](skills/engineering/setup/SKILL.md) | 每 repo 一次：配置 issue tracker / workflow / domain docs，并幂等检查本机 Codex / Claude statusline。 |
| [grill-with-docs](skills/engineering/grill-with-docs/SKILL.md) | 澄清需求、外部接口和兼容约束，必要时记录 glossary / ADR。 |
| [to-spec](skills/engineering/to-spec/SKILL.md) | 顶部 Proposed Changes，下面完整 spec；小任务一张 issue，大任务父 spec + 子 tickets。 |
| [implement](skills/engineering/implement/SKILL.md) | Leaf 自动实现 + 独立 review；Parent 自动编排 child issue DAG、独立 review 每个子票并做最终 integration review。 |

只导出这四个 user-invoked skill。domain modeling、测试和 code review 的必要纪律已收进日常入口，不需要单独安装。

`implement` 中由 Controller 独占 issue workflow state，Implementer / Reviewer 只报告事实；具体状态与终态动作由当前项目的 issue tracker 配置决定，所有实现都必须经过独立 reviewer 才能进入完成状态。

## Setup 的边界

`/setup` 仍然是 **run once per repo**。

它一个入口做两层检查：

```text
/setup
├── Project setup              # 当前 repo，必做
│   ├── issue tracker / target
│   ├── parent / child
│   ├── blockers / dependencies
│   ├── workflow states / completion condition
│   └── domain docs / ADR layout
│
└── CLI environment check      # 当前机器，幂等
    ├── Codex CLI statusline
    └── Claude Code statusline
```

Project setup 写入当前业务 repo 的 `docs/agents/issue-tracker.md` 与 `docs/agents/domain.md`，并在已有 `CLAUDE.md` / `AGENTS.md` 中保留简短指针。

CLI 配置属于用户级。已有 statusline 一律保留；只有缺失时才展示最小 diff、确认、备份并 merge。重复运行应该是 no-op。

## Spec 与 tickets

spec 保存整体目标、外部契约和已确认决策；ticket 是可独立验证的实施切片。
默认一次 `to-spec` 完成固化与按需拆票，不重新开一轮需求访谈，也不为小改动制造父子票。

```text
to-spec                  # 固化需求，按规模选择单 issue 或父 spec + 子票
to-spec 仅 spec           # 本次不拆票
to-spec 只拆票 #123        # 给已有 spec 补拆票，不改父 spec 决策
to-spec 只预览            # 不写 tracker
```

以上是自然语言调用示例，不是 CLI flags。
Proposed Changes 通常约 10–20 行，突出 What changes、External contract、Compatibility、Before → After。

## 安装到多设备 / 多项目

在每台设备执行，全局安装后可供该设备的多个项目使用：

```bash
npx skills@latest add imbingox/skills -g \
  --skill setup \
  --skill grill-with-docs \
  --skill to-spec \
  --skill implement
```

需要项目级安装时去掉 `-g`。仅检查清单：

```bash
npx skills@latest add imbingox/skills --list
```

安装完成后进入每个 repo 执行一次 `/setup`。

安装和移除参数参考 [skills CLI 官方文档](https://github.com/vercel-labs/skills)。
不要同时保留上游和此 fork 的同名技能副本；先确认安装来源和作用域，再替换。

## Issue tracker

Issue / spec 放在哪里由每个业务项目自己的 `docs/agents/issue-tracker.md` 定义，不放在 skills repo。
`setup` 负责初始化 / 校验它；`to-spec` 和 `implement` 只消费它，不自行猜发布目标或 workflow。

配置说明见 [Issue tracker](docs/issue-tracker.md)。

## 从完整 Matt 集合迁移

- 独立 `to-tickets` 已移除，改用 `to-spec` 默认流程或“只拆票”模式。
- 恢复了一个精简的 `setup`，但仍是 run once per repo；它不恢复 Matt 的全量 triage / router 流程。
- 其他不常用 skill 及对应说明从当前树移除；需要时再从 upstream / Git 历史择取。
- 已安装的旧副本不会因为仓库提交而自动清理。

在每台设备先查看已安装清单，备份自己改过的文件，然后仅移除确实不再需要的条目：

```bash
npx skills@latest list -g
npx skills@latest remove to-tickets -g
```

不要批量删除整个 skills 目录。

## 维护

修改 prompt 时同步本页、对应 [说明文档](docs/engineering/setup.md) 与插件清单；保留 user-invoked 元数据。
运行 `python3 scripts/check-skills.py` 检查入口清单、frontmatter、打包引用与文档链接。
静态检查不等于 agent 实际行为验收；真实输出仍需用自己的任务检验。
