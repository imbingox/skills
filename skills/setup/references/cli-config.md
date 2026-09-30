# CLI configuration reference

提议写入 statusline 前读取。这里只管理 repo 内的配置：已有项目配置和组织 managed policy 优先，缺失时才提议默认值；不写用户目录。项目设置可以覆盖继承的用户默认值，确认摘要中须说明这一点。

## Codex

项目配置：`<repo>/.codex/config.toml`。优先使用原生 TUI status line，不装外部 renderer：

```toml
[tui]
status_line = ["model-with-reasoning", "context-remaining", "current-dir", "git-branch", "permissions"]
```

item 名称会随版本变化。写入前以当前客户端的 config schema 或 `/statusline` 可选项为准；只检查选项，不用可能保存用户级设置的交互命令代替项目文件写入。某个 item 不受支持时删掉它，不为套模板写入无效配置。

Codex 只加载受信任项目的 `.codex/config.toml`。未受信任时报告待用户处理，不代改 trust。项目配置高于用户默认值，但 CLI 参数、管理约束和从 repo root 到 cwd 之间更近的项目配置可能影响生效；不为消除覆盖而修改这些来源。

## Claude Code

项目配置：`<repo>/.claude/settings.json`。把随包 [claude-statusline.py](claude-statusline.py) 复制到 `<repo>/.claude/statusline.py`，再 merge：

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 -c 'import io,json,runpy,subprocess,sys; raw=sys.stdin.read(); data=json.loads(raw); root=subprocess.check_output([\"git\",\"-C\",data[\"workspace\"][\"project_dir\"],\"rev-parse\",\"--show-toplevel\"],text=True).strip(); sys.stdin=io.StringIO(raw); runpy.run_path(root+\"/.claude/statusline.py\",run_name=\"__main__\")'",
    "padding": 0
  }
}
```

命令依赖 Python 3 与 Git：从 statusline stdin 的 `workspace.project_dir`（启动目录）解析 Git root，定位该 checkout 的脚本，再把完整 stdin 交还给 renderer。不依赖命令的 cwd、机器绝对路径或仅在 hooks 中保证的 `CLAUDE_PROJECT_DIR`；从子目录或 linked worktree 启动也能定位。会话内切换 cwd 时仍用启动项目的脚本，显示内容按当前 workspace 更新。

`.claude/settings.local.json`、CLI 参数和 managed policy 优先于项目共享设置。已有本地覆盖时保留并说明，不写共享配置假装覆盖已生效；只生成共享默认值时也须明确当前会话仍使用本地值。配置与脚本需一同纳入项目版本管理，未提交的配置不会自动出现在新 worktree。

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

参考：[Codex config basics](https://developers.openai.com/codex/config-basic/)、[Codex config reference](https://developers.openai.com/codex/config-reference/)、[Claude settings](https://code.claude.com/docs/en/settings)、[Claude statusline fields](https://code.claude.com/docs/en/statusline)。
