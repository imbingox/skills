# Implement

## What it does

读取 spec / ticket 与依赖，按 public seam 逐条测试和实现，完成后分别检查 Standards 与 Spec。
不再需要独立测试或评审 skill。

## When to reach for it

需求已确认，且本次要做的切片前置条件已满足时。

## Common questions

不把父 spec 当成一次包办所有子票的授权，不把 ready-for-agent 当作解除 blocker。
支持没有 Proposed Changes 标题的旧 spec；自审包含本次未提交改动与新文件。
不会替用户提交无关工作，不自动 push、merge、关闭票或执行生产操作。

## It's working if

外部行为和兼容承诺与 spec 一致，有真实验证证据，并清楚报告未完成或未验证部分。
