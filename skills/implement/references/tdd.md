# 行为测试与 TDD

写测试前读取；Implementer 写测试和 Reviewer 审查测试时共用。改编自 Matt 的 tdd skill。

## 好测试

测试经 public interface 验证行为，读起来像一条规格：“有效购物车可以结账”。内部重构不改变行为时，测试不应失败。

```ts
// 好：观察调用方可见的结果
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

## 反模式

- **绑定实现**：mock 内部协作者、测 private 方法、断言调用次数 / 顺序，或绕过 interface 验证（直接查数据库而不是通过读取接口）。信号：行为没变，重构后测试却失败。
- **同义反复**：断言按实现的方式重算期望值，永远不会和代码不一致。期望值来自独立来源：已知字面量、手算样例或 spec。
- **水平切片**：先写完所有测试再写实现。这样测到的是想象中的形状而非真实行为，测试结构也在理解实现之前就被固定。改为垂直切片：一条测试 → 一段最小实现 → 下一条，每条都是 tracer bullet，吸收上一轮的发现。

```ts
// 坏：期望值照抄实现
const expected = items.reduce((sum, i) => sum + i.price, 0);
expect(calculateTotal(items)).toBe(expected);

// 好：独立字面量
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
```

## Mock 的边界

只在系统边界 mock：外部 API、时间 / 随机数，必要时数据库和文件系统（优先测试库和临时目录）。不 mock 自己控制的模块和内部协作者。
边界处接收依赖而不是在内部创建，例如传入 `paymentClient` 而不是在函数里 `new StripeClient(...)`。为每个外部操作提供具体函数，而不是一个通用的 `fetch(endpoint, options)`，这样每个 mock 只返回一种形状。

## 循环规则

- 先红后绿：先看到测试因目标行为缺失而失败，再写刚好让它通过的代码；不预写后续测试才需要的功能。
- 一次一个切片：一个 seam、一条测试、一段最小实现。
- 使用 spec 的 Testing Decisions 已约定的 seam；需要新 seam 时尽量放在高层，并在交付报告中说明。
- 重构不在红绿循环内进行；需要时在测试全绿后单独做，且不超出本次范围。
