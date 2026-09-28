# Domain Modeling

在设计讨论中主动澄清领域模型，不只是读取 glossary。沿用项目的 domain 配置、已有位置和格式；以下模板只在没有既有约定时使用。

## 主动澄清

- 对照 glossary 指出冲突：例如原定义中 cancellation 指整单取消，当前讨论却允许部分取消，先区分现状与期望。
- 遇到含混词主动提出精确名称：例如 account 究竟指 Customer 还是 User？不同概念不能用同一个词糊过去。
- 用具体场景检验概念关系：一张 Order 能有多个 Invoice 吗？部分发货后还能取消哪些内容？只追问当前范围内有实质影响的问题。
- 用代码核对事实；代码与用户描述不一致时展示差异，不擅自把现状或猜测写成最终定义。
- 术语一旦确认就及时记录，不等会话结束再凭记忆批量补写；仍未决的选项不冒充已确认 glossary。

## 布局与 context 选择

先读项目配置；有 `CONTEXT-MAP.md` 时从 map 定位当前话题所属 context。归属不清再问用户。
只有根目录 `CONTEXT.md` 时按单 context；两者都没有时，在首个术语确认后按约定位置创建 glossary，默认根目录 `CONTEXT.md`。

```text
单 context                    多 context
CONTEXT.md                    CONTEXT-MAP.md
docs/adr/                     docs/adr/              # 系统级决策
                              src/ordering/
                                CONTEXT.md
                                docs/adr/            # 局部决策
                              src/billing/
                                CONTEXT.md
                                docs/adr/
```

按需创建，不为套模板建立空 context、空 ADR 或迁移现有目录。

## CONTEXT.md 模板

```markdown
# Ordering

接收并跟踪客户订单的领域上下文。

## Language

**Order**：客户提出的一组购买请求，是本上下文跟踪履约的业务单位。
_Avoid_: Purchase, transaction

**Customer**：提出订单的个人或组织。
_Avoid_: Client, buyer, account
```

- 一个概念选一个已确认的 canonical term，把容易混用的同义词列在 `_Avoid_`，不机械禁止它们在别的 context 表达不同概念。
- 定义通常一两句，解释“是什么”，不写操作步骤。
- 只收录该项目 context 的领域概念；timeout、utility、通用错误类型等编程知识不属于 glossary。
- 自然形成多个概念群时可加子标题，单一内聚领域用平铺列表即可。
- 不放实现细节、spec、临时笔记、验收进度或数据库技术选型；示例概念不是要求项目采用的业务模型。

## CONTEXT-MAP.md 模板

Map 是 context 位置与关系索引，不是模块文件清单。以下链接是业务项目的产物示例，应替换为该项目真实路径。

```markdown
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md)：接收和跟踪客户订单。
- [Billing](./src/billing/CONTEXT.md)：生成账单并处理付款。
- [Fulfillment](./src/fulfillment/CONTEXT.md)：管理仓库拣货和发运。

## Relationships

- Ordering → Fulfillment：发布 OrderPlaced，驱动拣货。
- Fulfillment → Billing：发布 ShipmentDispatched，触发账单生成。
- Ordering ↔ Billing：共享已约定的 CustomerId 与 Money 含义。
```

只记录已核实或已确认的关系，不凭模板发明事件、共享类型或通信方式。

## ADR

仅当决策同时难逆转、缺少背景会令人意外、确实比较过替代方案时提出 ADR。经用户同意后记录；已有本次明确授权不重复确认。
适合记录的例子：跨 context 的通信方式、数据归属、难以替换的技术选型、刻意偏离常规的方案，以及代码看不出的业务约束。
常规库选择、易逆转的局部实现、没有真实替代方案的显然选择通常不值得创建 ADR。

没有项目模板时保持简短：

```markdown
# 订单与计费通过领域事件协作

订单必须在计费服务短暂不可用时继续被接收。我们选择发布领域事件而非同步调用计费，以降低可用性耦合；代价是计费状态最终一致，需要处理重复事件。
```

一段话说明背景、决策和原因即可。只有确有价值时才增加 Status、Considered Options 或 Consequences，不为填模板扩写。
沿用已有编号与路径；缺少约定时使用 `docs/adr/0001-slug.md`，写入前读取该目录最大编号并递增。多 context 下按决策影响范围选择系统级或局部 ADR，不改写旧决策来掩盖变化。
