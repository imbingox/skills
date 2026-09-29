# Bingo Skills

面向 agent 日常开发的中文工程工作流技能集。五个手动入口覆盖项目配置、需求澄清、spec、实施和 bug 排查；`writing-for-agents` 提供可自动或手动调用的 agent 文档写作参考。

## 安装

使用 `skills` CLI 安装本仓库的全部 skills 到当前用户，供多个项目使用：

```bash
npx skills@latest add imbingox/skills -g
```

项目级安装时去掉 `-g`。只安装部分入口时用 `--skill <name>` 指定，可选项为 `--skill setup`、`--skill grill`、`--skill to-spec`、`--skill implement`、`--skill diagnosing-bugs`、`--skill writing-for-agents`，例如：

```bash
npx skills@latest add imbingox/skills -g --skill setup --skill implement
```

查看可安装清单：

```bash
npx skills@latest add imbingox/skills --list
```

Claude Code 也可以通过插件 marketplace 安装：

```bash
claude plugin marketplace add imbingox/skills
claude plugin install bingo-skills@imbingox
```

## 使用

每个项目首次使用时运行一次：

```text
/setup
```

它会配置当前项目的 issue tracker 和领域文档位置，并检查本机 Codex / Claude statusline；已有配置会保留，缺失的机器级配置会先提议补齐。换 tracker 或换机器后可以再次运行。

日常需求推荐按以下顺序调用：

```text
/grill 增加导出功能，兼容现有 API
/to-spec
/implement #123
```

| 入口 | 用途 |
| --- | --- |
| [setup](skills/setup/SKILL.md) | 为当前项目配置工作流和领域文档。 |
| [grill](skills/grill/SKILL.md) | 澄清需求、外部行为、兼容范围和验收边界。 |
| [to-spec](skills/to-spec/SKILL.md) | 固化需求为 spec，并按规模决定是否拆成子 tickets。可说“仅 spec”“只拆票 #123”或“只预览”。 |
| [implement](skills/implement/SKILL.md) | 按 issue 或 spec 实施并完成独立 review；有子票时自动编排。 |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 从症状开始复现、定位和修复；可说“只排查”以仅输出根因与证据。 |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | 编写或审查 skill、项目指令、spec、tickets 和 agent prompt；可自动触发，也可手动调用。 |

发现 bug 时可直接调用排查入口，不必先运行 `/setup`：

```text
/diagnosing-bugs 保存后刷新，配置恢复默认了
/diagnosing-bugs 只排查：升级后导出明显变慢
```

五个工作流入口都需要手动调用。`writing-for-agents` 可在编写 agent 文档时自动选用，也可以直接调用：

```text
/writing-for-agents 检查这份 spec 是否能由新 session 独立执行
```

项目的 tracker 位置和操作方式由该项目自己的配置决定。运行 `/setup` 后，`to-spec` 和 `implement` 会按项目配置处理 tracker；缺少远程 tracker 配置时，先运行 `/setup`。每个入口可单独安装，工作流不依赖 `writing-for-agents`。

安装参数可查阅 [`skills` CLI 文档](https://github.com/vercel-labs/skills)。
