# CLI configuration reference

Setup 只管理少量可明确归属的用户级配置，默认是 status line。

## General

- Existing user configuration wins.
- Missing config may be proposed.
- Backup before write.
- Parse, merge, validate; never replace a whole config just to add one key.
- Secrets are out of scope.
- Managed / organization policy wins over user preferences.

## Codex

User config: `~/.codex/config.toml`.

Codex currently supports a native TUI footer configured under `[tui].status_line`. Prefer native status-line items over an external renderer.

Because item names evolve, check the installed client / current schema before writing. If a recommended item is unavailable, omit it.

## Claude Code

User config: `~/.claude/settings.json`.

Claude Code statusLine is command-based. The bundled renderer reads JSON from stdin and prints one line. It intentionally tolerates absent optional fields and does not access credentials.

If the user already has a `statusLine`, do not replace it automatically.

## Default layout

Codex 推荐值按以下顺序排列：

```toml
[tui]
status_line = ["model-with-reasoning", "context-remaining", "current-dir", "git-branch", "permissions"]
```

Claude renderer 尽量保持同样的顺序，各项用 ` · ` 分隔：

| 显示项 | Claude 数据来源 / 行为 |
| --- | --- |
| 模型 / 推理强度 | `model.display_name`（回退 `model.id`）与 `effort.level`；effort 缺失时只显示模型。 |
| 剩余上下文 | `context_window.remaining_percentage`；缺失时由 `used_percentage` 计算，显示 `ctx 72% left`。 |
| 当前目录 | `workspace.current_dir`，回退 `cwd`；显示目录名。 |
| Git 分支 | 在当前目录只读查询 Git；detached HEAD 显示短 SHA，非 Git 目录省略。 |
| 权限 | 仅当输入明确提供非空字符串 `permission_mode` 时显示 `permissions <mode>`；缺失时省略。 |

Claude 官方字段表目前未列出 `permission_mode`；本机检查的 Claude Code 2.1.119 也未将实时权限模式传给 statusline。因此通常只显示前四项，不保证与 Codex 五项完全等价。兼容输入中明确提供的权限字段，不添加 hooks 或根据 `settings.json` 的默认权限冒充实时会话状态。

不再默认显示 5h / 7d 额度。输入字段缺失时不显示占位假值。
这些是缺失配置时的默认模板；已有配置仍保留，用户明确要求替换时才按其授权范围备份并更新。

参考：[Codex config reference](https://developers.openai.com/codex/config-reference/)、[Claude statusline fields](https://code.claude.com/docs/en/statusline)。
