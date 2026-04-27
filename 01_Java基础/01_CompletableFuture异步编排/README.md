# CompletableFuture 异步编排 ⭐

## 项目应用

`ibrain-base` 流式推理异步回传；`ibrain-prompt` 工作流节点异步执行与超时控制。

## 核心考点

- `supplyAsync` / `runAsync` 的区别与使用场景
- `thenApply` / `thenAccept` / `thenCompose` 链式调用，以及 `thenCompose` 与 `thenApply` 的差异（前者用于嵌套 Future 扁平化）
- `allOf` / `anyOf` 并发聚合
- 超时控制：`orTimeout()`、`completeOnTimeout()`（JDK 9+）
- 异常传播：`exceptionally()`、`handle()`、`whenComplete()` 的区别
- 为什么不用默认公共池 `ForkJoinPool.commonPool()`：阻塞任务会拖累整个 JVM
- `CompletableFuture` 与 `Thread` / `ExecutorService` 的对比优势：链式编排、组合能力、异常一等公民

## 面试话术

> 在 ibrain-base 的流式推理链路中，我们用 `CompletableFuture.supplyAsync` 配合**自定义线程池**发起模型调用，通过 `thenAccept` 将增量结果写入 `SseEmitter`，用 `orTimeout` 兜底外部模型响应超时。相比裸线程池，`CompletableFuture` 的链式编排让异常传播和超时兜底更清晰；用自定义线程池而非 `commonPool` 是为了避免阻塞型 IO 任务污染全局池。
