# Codebase Design：实现与审查

吸收 Matt codebase-design 的深模块原则。只在已确认 spec 和 external contract 内优化，不借设计原则重做需求。

Module 是具有 interface 和 implementation 的单位。Interface 包含调用方必须知道的参数、约束、顺序、错误、配置及性能；不只指类型签名。
Deep module 用简单 interface 承载丰富行为，带来复用能力（leverage）和变化集中性（locality），不以代码行数比例衡量 depth。
Seam 是可替换行为的位置，adapter 是在此处满足 interface 的具体实现。沿用项目已有领域命名。

## Implementer

- 将反复出现在调用方的协调逻辑收进负责它的 module，减少方法、参数和调用顺序知识；避免只有转发价值的层。
- 删除检验：删掉抽象后，复杂性是否散落回多个调用方？若复杂性反而消失，评估是否应省去这层。
- 仅在存在真实变化需要时设置 seam，不为假想 adapter 提前加抽象。第二个实际 adapter 是变化存在的有力证据。
- 接收必要依赖，避免内部硬编码创建；可行时返回结果而非隐式修改外部状态。
- 行为测试与调用方经过同一 public interface。若测试必须穿透 interface 才能验证承诺，检查 seam 是否选错。
- 内部可以有小部件、私有 seam 和内部测试；保持 external interface 简单，不把 deep module 写成巨型函数。
- 调整 module 时用新 interface 上的行为测试覆盖原承诺，避免叠加一层抽象和一套只重复内部细节的测试；删除旧测试前确认其行为覆盖已被替代。

## Reviewer

在 Standards review 中检查：调用方需掌握的知识是否减少，复杂性是否集中，是否引入无实际变化的抽象，以及测试是否观察真实行为。
在 Spec review 中检查：接口简化是否偷偷改变外部契约或兼容性。
已有设计足够清晰时不强制重构；涉及已确认契约的改动按入口规则交回 Controller，不自行批准设计变更。
