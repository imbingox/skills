# Skill mechanics

仅在目标文档是 skill 时读取。通用写作方法由 [SKILL.md](SKILL.md) 定义。

## 调用方式

- **可自动调用**：description 面向模型，写清能力与适用条件；不设置 `disable-model-invocation: true`，Codex 的 `policy.allow_implicit_invocation` 为 `true`。用户仍可手动调用，自动选择是否发生由客户端和模型决定。
- **仅手动调用**：设置 `disable-model-invocation: true`，Codex 的 `policy.allow_implicit_invocation: false`。description 写给选择入口的用户，不加入自动触发清单。其他 skill 不应自动调用它。

沿用用户明确要求与项目策略；修改内容不意味着可以顺手改变调用方式。每个新增自动入口都增加发现成本，只有独立适用场景值得时才拆出。

## 包结构与引用

目录名与 frontmatter 的 name 保持一致。SKILL.md 保留必要步骤和读取条件；实际需要的参考、脚本和元数据随包提供。
沿用项目的安装约定：要求独立安装时，必要资源随当前 skill 提供；允许依赖其他 skill 时，在入口和安装说明中列明依赖、读取条件及资源定位方式。不要假定安装后仍保留仓库中的相邻目录布局，或仓库根文件会随 skill 安装；依赖缺失时明确提示所需资源，不假装已读取。
可选辅助 skill 不得成为未声明的硬依赖；它未安装时，核心流程仍应可执行。

## 拆分与路由

按场景拆参考文件，按确有价值的独立触发场景拆入口。不要将每个参考都变成自动 skill。
只有手动入口数量造成实际选择困难时才考虑 router；router 可以帮助用户选择，但不能绕过手动入口的调用策略。

## 验证

检查 frontmatter、调用策略与安装清单一致，资源在声明的安装方式下可访问；有依赖时核对依赖齐全与缺失时的行为。用请求示例检查 description 是否准确区分适用与无关任务；静态校验不证明安装后资源可达性、自动触发率或执行效果。
