# Bingo Skills

基于 [mattpocock/skills](https://github.com/mattpocock/skills) 的公开精简 fork，保留原 MIT 许可与来源。
中文优先，面向日常 agent 开发：先确认怎么用、兼容什么，再让 agent 实现。

## 日常流程

```text
grill-with-docs → to-spec → implement
```

| 入口 | 做什么 |
| --- | --- |
| [grill-with-docs](skills/engineering/grill-with-docs/SKILL.md) | 澄清需求、外部接口和兼容约束，必要时记录 glossary / ADR。 |
| [to-spec](skills/engineering/to-spec/SKILL.md) | 顶部 Proposed Changes，下面完整 spec；小任务一张 issue，大任务父 spec + 子 tickets。 |
| [implement](skills/engineering/implement/SKILL.md) | 按 spec / ticket 实施，内置行为测试和 Standards / Spec 双轴自审。 |

只导出这三个 skill。追问、domain modeling、测试和 code review 的必要规则已收进对应入口，不需要单独安装依赖。

## Spec 与 tickets 合并的是操作，不是职责

spec 保存整体目标、外部契约和已确认决策；ticket 是可独立验证的实施切片。
默认一次 to-spec 完成固化与按需拆票，不重新开一轮需求访谈，也不为小改动制造父子票。

```text
to-spec                  # 固化需求，按规模选择单 issue 或父 spec + 子票
to-spec 仅 spec           # 本次不拆票
to-spec 只拆票 #123        # 给已有 spec 补拆票，不改父 spec 决策
to-spec 只预览            # 不写 tracker
```

以上是自然语言调用示例，不是 CLI flags；用所用 agent 的 skill 调用入口传入这些指令。
Proposed Changes 通常约 10–20 行，突出 What changes、External contract、Compatibility、Before → After。

## 安装到多设备 / 多项目

在每台设备执行，全局安装后可供该设备的多个项目使用：

```bash
npx skills@latest add imbingox/skills -g --skill grill-with-docs to-spec implement
```

需要项目级安装时去掉 `-g`。可按安装器提示选择 agent；仅检查清单用：

```bash
npx skills@latest add imbingox/skills --list
```

安装和移除参数参考 [skills CLI 官方文档](https://github.com/vercel-labs/skills)。
不要同时保留上游和此 fork 的同名技能副本；先确认安装来源和作用域，再替换。

## Issue tracker 是项目配置

继续读取各业务项目已有的 `docs/agents/issue-tracker.md`，以及其 label / domain docs 配置，不要求重跑 setup。
新项目只需明确 tracker、目标仓库 / 项目与现有约定；没有可解析的目标时先给草稿，不静默发布。
配置说明见 [Issue tracker](docs/issue-tracker.md)。GitHub / GitLab / Linear / 本地 Markdown 沿用项目已有选择。

## 从完整 Matt 集合迁移

- 独立 `to-tickets` 已移除，改用 `to-spec` 默认流程或“只拆票”模式。
- 独立 setup 入口已移除，**项目已有配置文件保留不动**。
- 其他不常用 skill 及对应说明从当前树移除；需要时再从 upstream / Git 历史择取，不保持全量镜像。
- `grill-with-docs`、`to-spec`、`implement` 名称不变。已安装的旧副本不会因为这次仓库提交而替你清理。

在每台设备先查看已安装清单，备份自己改过的文件，然后仅移除确实不再需要的条目：

```bash
npx skills@latest list -g
npx skills@latest remove to-tickets -g
```

项目级安装需要在对应项目去掉 `-g` 处理。不要批量删除整个 skills 目录。
Claude 插件清单也只导出三项，fork 插件名为 `bingo-skills`，不冒用上游插件身份。主要安装方式仍是上面的 skills CLI。

## 维护

修改 prompt 时同步本页、[说明文档](docs/engineering/to-spec.md)与插件清单；保留 user-invoked 元数据。
运行 `python3 scripts/check-skills.py` 检查入口清单、frontmatter、打包引用与文档链接。
静态检查不等于 agent 实际行为验收；真实输出仍需用自己的任务检验。
上游历史与维护基础设施暂保留；后续能力按实际需要吸收，不自动恢复全量技能。
