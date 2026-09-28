# Repository instructions

这是 imbingox/skills 的精简 fork，不再维护上游完整技能目录。
当前只导出 skills/engineering 下的 grill-with-docs、to-spec、implement，均为 user-invoked。
README、工程目录 README、docs/engineering 和 .claude-plugin/plugin.json 必须与这三个入口一致。

- 默认中文说明，英文目录、name 和技术标识符保持稳定。
- to-spec 内置按需拆票；Proposed Changes 优先外部用法与兼容性。
- 必要纪律内置到入口或该入口的 references 内，不自动恢复已移除的 skill。
- 每个 skill 单独安装也必须能用；相对资源链接不能越过该 skill 的目录去依赖兄弟目录或仓库根文件。
- 项目 tracker 配置归业务项目所有，旧 docs/agents 文件继续读取，不强制 schema 迁移。
- 每个 SKILL.md 保留 disable-model-invocation: true，agents/openai.yaml 保留 allow_implicit_invocation: false。
- 更新已有 tracker 对象前重读，保留人工编辑；不要假报发布、测试或验收成功。
- 变更后运行 python3 scripts/check-skills.py；具备 Claude CLI 时另跑 claude plugin validate . --strict。
- 保留 LICENSE 中的上游版权与许可。没有实际使用需求，不恢复旧路由器或全量 skills。

AGENTS.md 是此文件的 symlink。上游 .agents/ 与 .out-of-scope/ 中旧流程说明作为历史保留，不是此 fork 的现行维护约定。
