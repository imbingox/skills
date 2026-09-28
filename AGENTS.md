# Repository instructions

这是独立维护的 imbingox/skills 工程工作流技能集。借鉴 Matt 的方法并保留必要来源，不以同步其完整技能集为目标。
维护和推送目标为 git@github.com:imbingox/skills.git。
导出 skills 下的五个手动工作流入口 setup、grill、to-spec、implement、diagnosing-bugs，以及可自动或手动调用的写作参考 writing-for-agents。
根 README.md 和 .claude-plugin/plugin.json 必须与这六个 skill 一致；使用说明集中在 README，执行细节放在各 skill 内，不另维护 docs 目录或 changelog。

- 默认中文说明，英文目录、name 和技术标识符保持稳定。
- setup 是 run once per repo 的 bootstrap：项目 tracker/domain 必配，用户级 CLI statusline 只做幂等检查与缺失补齐。
- to-spec 内置按需拆票；Proposed Changes 优先外部用法与兼容性。
- diagnosing-bugs 是独立诊断入口，沿用六阶段闭环；codebase-design 按需内置到设计与实施流程，不导出独立入口。
- 必要纪律内置到入口或该入口的 references 内，不自动恢复已移除的 skill。
- 每个 skill 单独安装也必须能用；相对资源链接不能越过该 skill 的目录去依赖兄弟目录或仓库根文件。
- 项目 tracker 配置归业务项目所有，旧 docs/agents 文件继续读取，不强制 schema 迁移。
- 五个工作流入口保留 disable-model-invocation: true 和 allow_implicit_invocation: false；writing-for-agents 不设置前者，allow_implicit_invocation 为 true。原有入口不能硬依赖该可选参考。
- 更新已有 tracker 对象前重读，保留人工编辑；不要假报发布、测试或验收成功。
- 变更后运行 python3 scripts/check-skills.py；具备 Claude CLI 时另跑 claude plugin validate . --strict。
- 保留 LICENSE 中的上游版权与许可。没有实际使用需求，不恢复旧路由器或全量 skills。

AGENTS.md 是本仓库唯一的维护说明。插件版本在 .claude-plugin/plugin.json 中手动维护。
