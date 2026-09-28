# Domain 文档布局

Setup 只确认领域文档的位置和组织方式，记录到业务 repo 已有 domain 配置，缺失时默认 `docs/agents/domain.md`；实际术语与决策在讨论中确认后才写入。
已有路径、格式和 context 划分优先，不强制迁移。以下是没有既有约定时的示例，不要求生成空目录或文件。

## Single context

多数项目使用一个领域词汇表：

```text
/
├── CONTEXT.md
├── docs/
│   ├── agents/domain.md
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

`docs/agents/domain.md` 示例：

```markdown
# Domain documentation

- Layout: single context
- Glossary: CONTEXT.md（首个术语确认后创建）
- ADRs: docs/adr/（首个需要记录的决策确认后创建）
- ADR numbering: 四位递增编号 + slug；读取当前最大编号后递增，不覆盖旧文件
- Glossary scope: 领域术语、定义与应避免的同义词；不记录实现方案或任务进度
- Existing conventions: 沿用已有术语和文档格式
```

## Multiple contexts

若根目录已有 `CONTEXT-MAP.md`，先读取它定位各 context。只有项目确实存在不同领域语言 / 职责边界时才使用多 context，不因目录多或采用 monorepo 就自动拆分。

```text
/
├── CONTEXT-MAP.md
├── docs/
│   ├── agents/domain.md
│   └── adr/                     # 系统级决策
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/            # Ordering 内部决策
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/            # Billing 内部决策
```

`docs/agents/domain.md` 示例：

```markdown
# Domain documentation

- Layout: multiple contexts
- Context map: CONTEXT-MAP.md
- Contexts:
  - Ordering: src/ordering/CONTEXT.md; ADRs: src/ordering/docs/adr/
  - Billing: src/billing/CONTEXT.md; ADRs: src/billing/docs/adr/
- System-wide ADRs: docs/adr/
- ADR numbering: 每个 ADR 目录独立递增，沿用已有编号约定
- Topic routing: 先按 map 定位所属 context；归属不清时询问，不把不同 context 的词义强行合并
- Creation: glossary / ADR 按需创建，不预建空文档
```

Map 说明各 context 在哪里及如何交互；各 `CONTEXT.md` 只解释该 context 的语言。跨 context 的决策记录在项目约定的系统级位置，局部决策放所属 context。
配置中要区分“已有文件”和“约定将来创建的位置”，不能把只记录了路径说成内容已经创建。
