# Bingo Skills

独立维护的中文工程工作流技能集。部分方法与实现源自 [mattpocock/skills](https://github.com/mattpocock/skills)，保留原 MIT 许可、版权和来源；不以兼容或同步其完整技能集为目标。
中文优先，面向日常 agent 开发：先确认怎么用、兼容什么，再让 agent 实现。

吸收 Ponytail 的核心准则，按本项目的契约、兼容与验证纪律调整：

- 先理解问题和真实调用链，再判断是否需要新增代码。
- 优先复用已有代码、标准库、平台原生能力和已安装依赖。
- 只为当前需求增加复杂性，不为假想未来预留抽象、配置或框架。
- 修复根因，覆盖受影响路径，不只掩盖报告中的症状。
- 选择清晰、易维护的最小充分实现，不以最少行数为目标。
- 满足验收并完成必要验证后停止扩展，不削减明确需求、兼容或安全保障。

六个 skill 直接位于 `skills/<name>/`。本页说明安装与使用，执行细节和模板随各 skill 打包。

## 使用方式

每个 repo 首次运行一次：

```text
/setup
```

之后需求开发走：

```text
grill → to-spec → implement
```

| 入口 | 做什么 |
| --- | --- |
| [setup](skills/setup/SKILL.md) | 每 repo 一次：配置 issue tracker / workflow / domain docs，并幂等检查本机 Codex / Claude statusline。 |
| [grill](skills/grill/SKILL.md) | 澄清需求、外部接口和兼容约束，必要时记录 glossary / ADR。 |
| [to-spec](skills/to-spec/SKILL.md) | 顶部 Proposed Changes，下面完整 spec；小任务一张 issue，大任务父 spec + 子 tickets。 |
| [implement](skills/implement/SKILL.md) | Leaf 自动实现 + 独立 review；Parent 自动编排 child issue DAG、独立 review 每个子票并做最终 integration review。 |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 直接从 bug 症状开始，复现、定位、修复与回归验证；支持只排查。 |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | 编写或审查 agent 指令文档：skill、AGENTS.md、spec、tickets 和任务 prompt；允许自动触发。 |

五个工作流入口均为 user-invoked；另有一个可自动或手动调用的 writing-for-agents。domain modeling、codebase-design、测试和 code review 的必要纪律已收进日常入口，不需要单独安装或调用。模块设计原则由 grill 和 implement 按需读取各自随包参考。

防止过度设计的约束同样内置：`grill` 检查是否已有更简单的达成方式，`to-spec` 固定当前范围，`implement` 与 review 检查新增复杂性的依据，`diagnosing-bugs` 控制根因修复范围。无需额外安装 ponytail；精简以满足已确认需求为前提，不按代码行数评价，也不削减兼容、安全或必要测试。

发现 bug 可直接调用 `/diagnosing-bugs <症状 / 日志 / 失败测试>`，不需要先写 spec、建 issue 或运行 setup。仅调查时说“只排查”；该入口不自动更新 tracker，也不套用 implement 的 DAG 编排流程。

`implement` 自动选择 Leaf / Parent，不需要额外模式开关。Parent 编排和 review 细节按需读取随包参考；Leaf 完成独立 review 与最终验证后提交目标范围修改，再按项目规则推进状态。用户明确要求不提交时遵从，提交不包含 push、merge 或部署。

`implement` 中由 Controller 独占 issue workflow state，Implementer / Reviewer 只报告事实；具体状态与终态动作由当前项目的 issue tracker 配置决定，所有实现都必须经过独立 reviewer 才能进入完成状态。

需求或接口仍有歧义时先用 `grill`：分轮确认使用方式、兼容范围和验收边界；已回答的问题不重复询问，也不会直接开始实现。

`writing-for-agents` 安装后可在编写上述 agent 文档时自动选用，也可手动调用 `/writing-for-agents 检查这份 spec 是否能由新 session 独立执行`。自动选择由客户端和模型决定，不保证每次触发；五个工作流入口不依赖它，仍可单独安装使用。

## 实施与排查

```text
/implement #123                  # 自动识别单票或父票，执行实现与独立 review
/implement spec.md 不提交         # 保留本地修改；需要 commit 的完成条件仍不能跳过
/diagnosing-bugs 保存后刷新，配置恢复默认了，帮我排查修复
/diagnosing-bugs 只排查：升级后导出明显变慢
```

`implement` 默认由一个独立 Reviewer 分别检查 Standards 与 Spec，复杂改动可拆成两位；任一轴失败都修复并复审。没有独立 reviewer 能力时可以实现和测试，但报告“等待独立 review”，不推进完成状态。

Parent 只在依赖已验收且对应代码可用后派发下游；无 blocker 不等于一定并行，还要满足修改范围低重叠和 workspace 隔离。全部 child 完成后仍需组合层 review 与验证。

`diagnosing-bugs` 从未知原因的症状开始，默认完成诊断与范围内修复；“只排查”只给根因、证据和建议。无法复现时报告已尝试的方法和缺失证据，不凭猜测修改。修复后重跑原始场景并清理临时探针。

## Setup 的边界

`/setup` 是 **run once per repo**。更换 tracker、调整 workflow 或换新机器时可以重新校验，已有且一致的配置保持 no-op。

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

Project setup 优先沿用项目说明指向的 tracker / domain 配置；没有既有配置时才默认写入 `docs/agents/issue-tracker.md` 与 `docs/agents/domain.md`。`CLAUDE.md` / `AGENTS.md` 中的简短指针指向实际配置位置，不强制迁移。

默认 statusline 对齐为模型 / 推理强度、剩余上下文、当前目录、Git 分支、权限。Claude 缺失实时权限字段时省略该项；不再默认显示 5h / 7d 额度。

CLI 配置属于用户级。已有 statusline 一律保留；只有缺失时才展示最小 diff、确认、备份并 merge。重复运行应该是 no-op。

领域文档示例已随 skill 打包：`setup` 提供单 / 多 context 布局和 domain 配置模板；`grill` 提供术语建模方法及 CONTEXT / CONTEXT-MAP / ADR 模板。已有项目格式优先，按需创建。

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
  --skill grill \
  --skill to-spec \
  --skill implement \
  --skill diagnosing-bugs \
  --skill writing-for-agents
```

需要项目级安装时去掉 `-g`。仅检查清单：

```bash
npx skills@latest add imbingox/skills --list
```

安装完成后进入每个 repo 执行一次 `/setup`。

安装和移除参数参考 [skills CLI 官方文档](https://github.com/vercel-labs/skills)。
不要同时保留 Matt 集合和本项目的同名技能副本；先确认安装来源和作用域，再替换。

## Issue tracker

Issue / spec 放在哪里由每个业务项目自己的 `docs/agents/issue-tracker.md` 或项目说明指向的已有等价配置定义，不放在 skills repo。
`setup` 负责初始化 / 校验它；`to-spec` 和 `implement` 只消费它，不自行猜发布目标或 workflow。

配置至少明确 provider / target、读写方式、父子关系、阻塞依赖、现有状态与完成条件，以及 Controller 可执行的状态转换。已有配置和人工编辑保留，不强制 schema 迁移。

`to-spec` 远程发布、`implement` 写 tracker 状态前需要明确配置；缺失时提示 `/setup`，不猜目标。只预览和不涉及 tracker 的本地实施可独立进行。工具不可用或部分发布失败时报告真实结果，不假报成功。

## 从完整 Matt 集合迁移

- `grill-with-docs` 已重命名为 `grill`；安装与调用使用新名称，旧安装副本需自行移除。
- 独立 `to-tickets` 已移除，改用 `to-spec` 默认流程或“只拆票”模式。
- 恢复了一个精简的 `setup`，但仍是 run once per repo；它不恢复 Matt 的全量 triage / router 流程。
- `diagnosing-bugs` 保留为独立手动入口；`codebase-design` 吸收到现有设计与实施流程，不再单独安装。
- 其他不常用 skill 及对应说明从当前树移除；需要时再从 upstream / Git 历史择取。
- 已安装的旧副本不会因为仓库提交而自动清理。

在每台设备先查看已安装清单，备份自己改过的文件，然后仅移除确实不再需要的条目：

```bash
npx skills@latest list -g
npx skills@latest remove to-tickets -g
```

不要批量删除整个 skills 目录。

## 维护

维护和推送目标：`git@github.com:imbingox/skills.git`。

修改 prompt 时同步本页与插件清单；保持各 skill 的调用策略。变更历史通过 Git 查看，不单独维护 changelog。
仓库维护规则只保存在 `AGENTS.md`。Claude Code v2.1.277+ 支持直接读取；默认模式下，当前目录或祖先目录的 CLAUDE.md 会优先，可用 `/context` 核对实际加载文件。参见 [Claude Code 文档](https://code.claude.com/docs/en/memory#agents-md)。

插件版本仅在 `.claude-plugin/plugin.json` 中手动维护，不再使用 Changesets、npm 发布依赖或自动版本 PR。安装使用上文的 skills CLI；`.claude-plugin/` 保留 Claude Code 插件安装能力。
运行 `python3 scripts/check-skills.py` 检查入口清单、frontmatter、打包引用与文档链接。
静态检查不等于 agent 实际行为验收；真实输出仍需用自己的任务检验。
