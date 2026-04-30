# 线程池 ⭐

## 项目应用

`ibrain-base` 异步推理自定义线程池；`luffy` 调度任务执行池。

## 核心考点

- `ThreadPoolExecutor` 七大核心参数
- 任务提交后流程：核心线程 → 工作队列 → 非核心线程 → 拒绝策略
- 四种拒绝策略：`AbortPolicy`、`CallerRunsPolicy`、`DiscardPolicy`、`DiscardOldestPolicy`，及自定义拒绝策略（一般要落日志 + 报警）
- 线程池状态流转：`RUNNING → SHUTDOWN → STOP → TIDYING → TERMINATED`
- 为什么禁止 `Executors.newFixedThreadPool` / `newCachedThreadPool`：无界队列 OOM、线程数无限膨胀
- 线程池大小：CPU 密集型 `N+1`、IO 密集型 `2N`，结合压测调整
- 优雅关闭：`shutdown()` + `awaitTermination()` vs `shutdownNow()`
- 业务隔离：核心链路 / 非核心链路使用不同线程池，避免互相影响

## 易错点

线程池中**业务异常被吞**——`submit()` 返回的 `Future` 不调 `get()` 异常会丢失，需在任务里 try-catch 或包装 `UncaughtExceptionHandler`。