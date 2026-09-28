# Issue tracker

Issue tracker 是每个业务项目自己的配置，由 `/setup` 在当前 repo 初始化 / 校验，不是全局共享配置。

authoritative 文件：

```text
docs/agents/issue-tracker.md
```

它至少应说明：

- tracker provider 和明确 target；
- read / write 方式；
- spec / ticket 规则；
- parent / child 表达；
- blockers / dependencies 表达；
- 项目现有 workflow states / labels / project fields；
- 哪个状态 / 动作代表 blocker 已满足；
- Controller 允许执行的状态转换。

已有配置继续有效，不强制迁移为固定 schema，也不删除旧的 triage / domain 文件。

后续：

```text
to-spec    → 读取配置，决定 issue 发布位置和关系
implement  → 读取配置，决定 workflow state 和 completion semantics
```

缺少该配置时，`to-spec` / `implement` 应提示先运行 `/setup`，而不是猜 repo、tracker 或状态机。

只预览时不写远端。工具不可用时保留草稿 / 报告阻塞，不能假装创建成功或静默换平台。
