# CLI configuration reference

提议写入 statusline 前读取。已有用户配置和组织 managed policy 优先；这里只是缺失时的默认值。

## Codex

用户配置：`~/.codex/config.toml`。优先使用原生 TUI status line，不装外部 renderer：

```toml
[tui]
status_line = ["model-with-reasoning", "context-remaining", "current-dir", "git-branch", "permissions"]
```

item 名称会随版本变化。写入前以当前客户端的 `/statusline` 或 config schema 为准；某个 item 不受支持时删掉它，不为套模板写入无效配置。

## Claude Code

用户配置：`~/.claude/settings.json`。statusLine 是命令式的：把随包 [claude-statusline.py](claude-statusline.py) 复制到 `~/.claude/statusline.py`，再 merge：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py",
    "padding": 0
  }
}
```

renderer 从 stdin 读取 JSON，输出一行，各项用 ` · ` 分隔，顺序尽量与 Codex 一致。缺失字段直接省略，不显示占位值，不访问凭据或网络：

| 显示项 | Claude 数据来源 / 行为 |
| --- | --- |
| 模型 / 推理强度 | `model.display_name`（回退 `model.id`）与 `effort.level`；effort 缺失时只显示模型。 |
| 剩余上下文 | `context_window.remaining_percentage`；缺失时由 `used_percentage` 计算，显示 `ctx 72% left`。 |
| 当前目录 | `workspace.current_dir`，回退 `cwd`；显示目录名。 |
| Git 分支 | 在当前目录只读查询 Git；detached HEAD 显示短 SHA，非 Git 目录省略。 |
| 权限 | 仅当输入提供非空字符串 `permission_mode` 时显示 `permissions <mode>`。 |

Claude 官方 statusline 字段表目前未列出实时权限模式，所以通常只显示前四项。不要为补齐这一项添加 hooks，或用 `settings.json` 的默认权限冒充当前会话状态。
不默认显示 5h / 7d 额度。

参考：[Codex config reference](https://developers.openai.com/codex/config-reference/)、[Claude statusline fields](https://code.claude.com/docs/en/statusline)。
