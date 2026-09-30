---
name: setup
description: "每个 repo 运行一次：配置项目 tracker、精简 workflow、领域文档位置、开发验证指引和项目级 CLI statusline，不写用户目录。"
disable-model-invocation: true
---

# Setup

每个 repo 首次使用本套 skills 时运行一次：

`/setup`

它在当前 repo 中处理两类配置：

1. **Project workflow**：tracker、workflow 和 domain docs 必须完成；开发与验证指引按已有事实核对并补缺。
2. **Project CLI config**：repo 内的 Codex / Claude statusline，幂等检查；已有项目配置优先，缺失时才提议补齐，不写用户目录。

不要把这两类配置拆成两个用户命令。重复运行必须安全；更换 tracker 或 CLI 版本时可重新运行校验。

## 1. Explore first

先读取当前 repo，不假设：

- `git remote -v`、`.git/config` 和 repo root；
- `AGENTS.md` / `CLAUDE.md`，以及其中已有的 tracker / domain 配置指针及对应文件，包括自定义位置；没有明确指针时再查默认 `docs/agents/issue-tracker.md` / `domain.md`；
- `CONTEXT.md`、`CONTEXT-MAP.md`、已有 ADR 目录；
- README / 项目说明中的开发与验证约定，以及对应的 package manifest、lockfile、任务脚本和 CI 配置；
- tracker 线索：GitHub / GitLab remote、`.scratch/` 等本地 issue 目录、Linear 等其他配置；
- `gh` / `glab` 是否可用及登录状态（`gh auth status`、`glab auth status`）。

优先沿用现有配置位置。若指针失效或多个文件互相冲突，先说明差异并确认 authoritative source，不静默新建第二套配置。

同时只读检查 CLI 及当前 repo 的配置：

- `command -v codex`、`codex --version`、`<repo>/.codex/config.toml`；
- `command -v claude`、`claude --version`、`<repo>/.claude/settings.json`；
- 已有 statusline / TUI 配置、`<repo>/.claude/settings.local.json` 中的覆盖项及 CLI 的配置优先级。

所有项目路径以已确认的 repo root 为准，不在调用时的子目录重复创建配置。仅在排查继承或冲突时只读检查用户级 statusline 字段；不把用户配置整份复制进项目。
不要读取、打印或写入 API key、token、cookie 等 secrets。

## 2. Project setup: issue tracker

项目 tracker 配置是 `to-spec` 和 `implement` 唯一的 tracker 来源：它们按其中的操作发布、读取、推进状态，不自己推断 provider 或命令。

确定 provider：

1. 已有配置：原位保留，对照下面的必需内容只补缺项。
2. 用户已经明确指定：使用用户选择。
3. remote 指向 GitHub / GitLab：推荐对应 provider，请用户确认。
4. 仍不明确：只问 provider / target 这一项，不猜。

新建配置时按 provider 复制模板，替换占位并删除不适用的行：

- GitHub：[issue-tracker-github.md](references/issue-tracker-github.md)
- GitLab：[issue-tracker-gitlab.md](references/issue-tracker-gitlab.md)
- 本地 markdown：[issue-tracker-local.md](references/issue-tracker-local.md)
- 其他（Linear、Jira 等）：请用户用一段话描述工作方式，参照 GitHub 模板的结构写成自然语言。

默认写入 `docs/agents/issue-tracker.md`；用户指定其他路径时使用其路径。

必需内容：

- provider 与明确 target。fork 同时有 origin / upstream 时核对写入目标；不把本 skills 仓库当业务 tracker。
- 操作：读取、查重、新建、更新正文、评论、挂子票 / 列子票、加 / 读 blocker、推进状态、关闭、重新打开；原生父子或依赖关系不可用时的文本表达。
- workflow：状态、就绪标记（label 或本地 `Status` 值）或“不使用”；**completion condition**（什么条件代表 issue 已满足 blocker）；Controller 可执行和需要人工确认的动作。

已有 workflow 原位保留，不重命名或迁移状态和 labels；已有配置明确“不使用” ready 时也保留。没有既有约定的新项目，默认推荐 **open → ready → closed**：远程 tracker 使用原生 open / closed，只补一个 `ready` 标签；本地 markdown 使用模板中的三个 `Status` 值。ready 表示需求与验收已明确，不代表 blocker 已满足；实施和 review 进度只在内部记录，不额外建立中间状态。

先按 provider 模板只读查询已有 labels，展示需要创建的 ready 标签并取得确认，再幂等补建缺项；同名标签含义不同先确认映射，不覆盖人工设置。用户拒绝或无权限创建时，记录 ready“不使用”、保留 open / closed，并报告未创建；不能把不存在的标签写成可用。除这项经确认的默认值外，不自行扩展 workflow vocabulary。关闭不等于完成：取消、重复或放弃的票不能自动满足 blocker，完成条件须包含本次关闭的交付与验收依据。
能只读验证的就验证，例如 `gh repo view <owner/repo>`；不为验证创建测试 issue，配置中不写 credentials。

## 3. Project setup: domain docs

优先读取并更新项目说明指向的已有 domain 配置，其次使用已有 `docs/agents/domain.md`。只有尚无配置时才默认创建 `docs/agents/domain.md`，不迁移已有等价配置。记录：

- glossary / domain context 的位置；
- ADR 位置与编号约定；
- single-context 或 multi-context。

读取 [domain-layout.md](references/domain-layout.md)，按其中的单 / 多 context 目录树和 `domain.md` 示例记录实际位置。已有约定优先，不强制套用示例路径。

默认 single-context；只有 repo 已经呈现明显多 context 结构时才使用 map。
不要为了 setup 创建空 `CONTEXT.md` 或空 ADR 目录；需要记录第一个术语 / 决策时再创建。

## 4. Project instructions and verification

在 repo 已有的 `CLAUDE.md` 或 `AGENTS.md` 中维护一个简短的 `## Agent workflow` 区块，指向本次确认的 tracker 配置和 domain 配置的实际路径。

保留已有有效指针及其组织形式，不为固定区块名重复添加，不把自定义路径改指向默认目录。
两个文件都存在时，修改项目已作为主说明文件使用的那个；不能判断时让用户选一个。两个都不存在时让用户选择创建哪一个。
不要复制整份 tracker 配置到这里，也不要覆盖周围人工内容。

在同一主说明文件中补齐缺失的开发与验证指引；README 等已有有效说明时只指向对应位置，不复制一套命令清单：

- 从实际 manifest、lockfile、任务脚本和 CI 识别包管理器、启动方式及测试 / typecheck / build 入口；记录工作目录和必要的本地服务等前置条件。只问无法识别或互相冲突的部分，不猜不存在的命令。
- 写清不同改动应选哪些检查：单模块跑相关检查，跨模块 / 接口变更覆盖受影响两侧及契约验证，构建 / 依赖变更检查构建；项目明确要求的全量 gate 仍须保留。命令能直接从脚本查明时，文档重点记录选择规则、来源和前置条件。
- 没有自动化测试就如实记录现状及可执行的 smoke / 人工检查；不为了 setup 引入测试框架、改 CI 或执行需要额外授权的安装、服务和远程操作。区分“入口已核对”和“命令已实测”，缺环境或未执行的检查不能写成通过。
- 这不是固定注册表：后续实施新增技术栈、改变启动 / 测试 / 构建方式时，同步更新原说明与受影响的已有 CI，保留仍在使用的旧技术栈检查。由那次变更负责维护，无需重跑 setup，也不把验证命令塞进 tracker 配置。

## 5. Project CLI config

CLI statusline 配置写入**当前 repo**，不写 `~/.codex` / `~/.claude`。每次 `/setup` 都检查，但仅在项目缺失时提议写入；已有用户级设置不迁移、不删除，项目值会在当前 repo 覆盖其默认值。

- Codex：`<repo>/.codex/config.toml` 已有 `[tui].status_line` 时保留原值；已安装且项目未配置时，提议原生 TUI status line。
- Claude Code：`<repo>/.claude/settings.json` 已有 `statusLine` 时保留原值；已安装且项目未配置时，提议把本 skill 的 [claude-statusline.py](references/claude-statusline.py) 复制到 `<repo>/.claude/statusline.py` 并 merge `statusLine` 字段。已有项目脚本先读、比较，不覆盖人工版本。

推荐值、可跨子目录 / worktree 的脚本命令和版本核对方式见 [cli-config.md](references/cli-config.md)；提议写入前读取。默认使用可纳入 Git 的项目配置，让新 checkout / worktree 也能使用；不把个人凭据或整份用户配置带进项目。

对项目 CLI 配置的任何写入：

- 先展示将修改的文件和最小 diff，取得用户一次明确确认；
- 修改已有文件前创建 timestamped backup，放在不纳入 Git 的临时位置，记录路径；
- parse 后 merge 本 skill 管理的 key，不用字符串替换，不替换整个文件或 `[tui]` 表；
- 写后重新 parse 并核对，并从 repo 子目录验证 Claude 脚本可定位；
- 已有项目 statusline 永不自动替换；`.claude/settings.local.json`、更近的 Codex 配置或更高优先级设置覆盖时说明原因，不静默改写；
- Codex 项目未受信任时报告“待用户信任后生效”，不自动修改 trust，也不改写用户级配置绕过限制。

CLI 不可用、版本不支持或用户拒绝该部分修改时，tracker / domain setup 仍然可以完成，报告跳过项。配置文件写入成功不等于已在交互 CLI 中验证生效。

## 6. Confirm and write

在第一次实际写入前，用一个紧凑摘要展示：

- tracker provider / target，以及原生或文本关系；
- workflow completion condition、就绪标记，以及拟补建的 ready 标签（如有）；
- domain docs layout、开发与验证指引的实际位置及缺项；
- Codex 项目 statusline：existing / proposed / unavailable；
- Claude 项目 statusline：existing / proposed / unavailable，以及覆盖或待信任等生效限制。

用户确认后执行写入。如果全部已有且一致，不要为了流程重复询问，报告 no-op 即可。

## 7. Done

完成后报告：

- 创建 / 更新了哪些 repo 文件；
- tracker target、就绪标记与完成状态语义，以及标签创建结果；
- 开发与验证指引的位置，哪些入口已核对、哪些命令已实测、哪些尚未验证；
- Codex / Claude 哪些项目级配置被保留、补齐或跳过，及生效验证范围；
- backup 路径（如修改了已有文件）；
- 未完成项。

后续按需求选路径：未决问题先 `grill`，需要固化或拆票时用 `to-spec`，目标与验收已明确的小任务可直接 `implement`。配置可以直接手动编辑，之后不必重跑 setup。
