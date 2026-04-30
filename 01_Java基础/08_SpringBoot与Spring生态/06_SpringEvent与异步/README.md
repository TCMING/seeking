# Spring Event 与异步

## 核心考点

- `ApplicationEvent` / `@EventListener` 事件驱动
- 同步事件 vs `@Async` 异步事件（注意需 `@EnableAsync`）
- `@Async` 默认用 `SimpleAsyncTaskExecutor`，**生产建议显式配置自定义线程池**
- 事件发布-订阅在业务解耦中的应用

## Spring Event 源码级主线

事件发布入口：

```java
applicationContext.publishEvent(event);
```

核心调用链：

```text
AbstractApplicationContext.publishEvent
-> ApplicationEventMulticaster.multicastEvent
-> 找到 ApplicationListener
-> invokeListener
```

关键类：

- `ApplicationEventPublisher`
- `AbstractApplicationContext`
- `ApplicationEventMulticaster`
- `SimpleApplicationEventMulticaster`
- `ApplicationListener`
- `EventListenerMethodProcessor`
- `ApplicationListenerMethodAdapter`

## @EventListener 如何生效

`@EventListener` 方法不是天然能被发现的。Spring 启动时会通过 `EventListenerMethodProcessor` 扫描 Bean 中标注 `@EventListener` 的方法，并包装成 `ApplicationListenerMethodAdapter`。

事件发布时，`SimpleApplicationEventMulticaster` 会找到匹配事件类型的 Listener 并调用。

## 同步事件与异步事件

默认情况下，Spring Event 是同步执行的。也就是说：

```text
publishEvent
-> listener 执行完成
-> publishEvent 返回
```

如果监听器耗时，会拖慢主流程。

异步方式通常有两种：

- 给监听方法加 `@Async`
- 给 `ApplicationEventMulticaster` 配置异步 `Executor`

## @Async 源码级主线

`@Async` 本质也是 AOP 代理。

关键类：

- `AsyncAnnotationBeanPostProcessor`
- `AsyncAnnotationAdvisor`
- `AnnotationAsyncExecutionInterceptor`
- `TaskExecutor`
- `ThreadPoolTaskExecutor`

调用链：

```text
Bean 初始化
-> AsyncAnnotationBeanPostProcessor 创建代理
-> 调用 @Async 方法
-> AnnotationAsyncExecutionInterceptor.invoke
-> 提交任务到 Executor
-> 线程池异步执行目标方法
```

## 高频坑

- 同类内部调用 `@Async` 方法不会异步，因为没有经过代理。
- 异步线程拿不到主线程事务上下文。
- 异步线程默认也拿不到主线程 SecurityContext。
- 生产环境不要使用无界线程策略，要配置核心线程数、队列大小和拒绝策略。

## 推荐断点

- `AbstractApplicationContext.publishEvent`
- `SimpleApplicationEventMulticaster.multicastEvent`
- `EventListenerMethodProcessor.processBean`
- `ApplicationListenerMethodAdapter.onApplicationEvent`
- `AsyncAnnotationBeanPostProcessor`
- `AnnotationAsyncExecutionInterceptor.invoke`

## 源码级面试话术

Spring Event 发布事件时会进入 `ApplicationEventMulticaster`，默认是同步广播。`@EventListener` 方法会在启动时被 `EventListenerMethodProcessor` 包装成监听器。`@Async` 不是事件机制自带的能力，而是通过 AOP 代理把方法调用提交到线程池，所以同类调用和事务上下文传播都要特别注意。
