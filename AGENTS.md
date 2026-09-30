# Repository instructions

这是独立维护的 imbingox/skills 工程工作流技能集。借鉴 Matt 的方法并保留必要来源，不以同步其完整技能集为目标。
维护和推送目标为 git@github.com:imbingox/skills.git。
导出 skills 下的六个手动工作流入口 setup、grill、to-spec、implement、fast-implement、diagnosing-bugs，以及可自动或手动调用的写作参考 writing-for-agents。
根 README.md 和 .claude-plugin/plugin.json 必须与这七个 skill 一致；使用说明集中在 README，执行细节放在各 skill 内，不另维护 docs 目录或 changelog。

- 默认中文说明，英文目录、name 和技术标识符保持稳定。
- setup 是 run once per repo 的 bootstrap：项目 tracker/domain 必配，CLI statusline 在项目级幂等检查与缺失补齐，不写用户目录。
- 新项目默认使用 open / ready / closed 的个人工作流；远程 tracker 只需一个 ready 标签，已有状态和标签映射继续沿用，不强制迁移。
- 开发与验证约定随代码演进：setup 初始化指引，实施时核对实际脚本并随技术栈 / 命令变化维护原说明及受影响的已有 CI，不另建命令注册表。
- 中断续跑复用原 issue / 本地票的简短记录；不另建进度体系，不把历史记录当作当前验证结果，也不扩大 tracker 写入权限。
- to-spec 内置按需拆票；Proposed Changes 优先外部用法与兼容性。
- diagnosing-bugs 是独立诊断入口，沿用六阶段闭环；codebase-design 按需内置到设计与实施流程，不导出独立入口。
- 必要纪律放在入口、其 references 或明确声明的依赖资源中，不自动恢复已移除的 skill。
- 允许 skill 之间声明依赖并复用资源，不要求每个 skill 单独安装即可运行；依赖须在入口和 README 中说明，按实际安装方式定位资源，缺失时明确提示，不假定仓库根文件会随 skill 安装。
- 项目 tracker 配置归业务项目所有，旧 docs/agents 文件继续读取，不强制 schema 迁移。
- tracker 的 provider 模板和操作命令只放在 setup；to-spec / implement 只按项目配置执行，不各自携带模板。
- implement 的 Parent 自动编排是实际使用需求，精简时保留；在调用时的当前分支和工作区集成，只为子任务创建独立 worktree，不另建父级分支或 worktree。只用当前 harness 的 sub-agent，确有需求再接入其他编排后端。
- fast-implement 用于目标明确、影响局部的小任务，无需 issue / spec / setup，由当前 agent 自查并验证，不管理 issue 生命周期；依赖 implement 的实现与验证参考，不自动调用其他手动入口，不减免项目要求的独立 review 或完成条件。
- 六个工作流入口保留 disable-model-invocation: true 和 allow_implicit_invocation: false；writing-for-agents 不设置前者，allow_implicit_invocation 为 true。工作流入口不能硬依赖该可选参考。
- 更新已有 tracker 对象前重读，保留人工编辑；不要假报发布、测试或验收成功。
- 变更后运行 python3 scripts/check-skills.py；具备 Claude CLI 时另跑 claude plugin validate . --strict。
- 保留 LICENSE 中的上游版权与许可。没有实际使用需求，不恢复旧路由器或全量 skills。

AGENTS.md 是本仓库唯一的维护说明。插件版本在 .claude-plugin/plugin.json 中手动维护。
