# Spring Event 与异步

## 核心考点

- `ApplicationEvent` / `@EventListener` 事件驱动
- 同步事件 vs `@Async` 异步事件（注意需 `@EnableAsync`）
- `@Async` 默认用 `SimpleAsyncTaskExecutor`，**生产建议显式配置自定义线程池**
- 事件发布-订阅在业务解耦中的应用
