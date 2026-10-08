# Repository instructions

这是独立维护的 imbingox/skills，作为 Matt skills（mattpocock/skills）的中文增强层：Matt 原版能覆盖的流程直接用原版，本仓库只维护原版缺少或需要加强的部分。
维护和推送目标为 git@github.com:imbingox/skills.git。
导出 skills 下的两个手动入口 spec、finish。根 README.md 和 .claude-plugin/plugin.json 必须与这两个 skill 一致；使用说明集中在 README，执行细节放在各 skill 内，不另维护 docs 目录或 changelog。

- 默认中文说明，英文目录、name 和技术标识符保持稳定。
- 不与 Matt 原版 skill 同名；原版能满足的需求不新增 skill。
- spec 包装 Matt 的 to-spec 与 to-tickets：二者只能手动触发，spec 不经 Skill tool，直接定位并读取其已安装的 SKILL.md，缺失时停止并提示安装。spec 只写增量，冲突时以增量为准；增量只描述行为要求，不依赖 Matt 原文的步骤编号或结构。
- spec 先展示带具体 Before → After 示例的 Proposed Changes（含决策与否决方案、test seams、不做与待定项），确认后再生成完整 spec / 子票正文与写入，优先外部用法与兼容性，并按规模内置拆票。
- finish 是开发验收后的手动收尾入口，补上 Matt implement 不关票的缺口：核对当前交付证据后停止本任务临时服务、提交剩余修改并按项目配置关闭目标任务；不减免 review / verification，不自动扩大为 push、merge 或部署。finish 不依赖其他 skill。
- 项目 tracker 配置归业务项目所有，一般由 Matt 的 setup-matt-pocock-skills 生成。spec / finish 读取并按项目已有配置执行，不携带 provider 模板。
- 两个入口保留 disable-model-invocation: true 和 allow_implicit_invocation: false。
- 更新已有 tracker 对象前重读，保留人工编辑；不要假报发布、测试或验收成功。
- 变更后运行 python3 scripts/check-skills.py；具备 Claude CLI 时另跑 claude plugin validate . --strict。
- 保留 LICENSE 中的上游版权与许可。

AGENTS.md 是本仓库唯一的维护说明。插件版本在 .claude-plugin/plugin.json 中手动维护。
