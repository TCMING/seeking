# Java 并发工具

## 项目应用

`midjourney-proxy` 任务幂等控制；`luffy` 避免重复调度。

## 核心考点

- `synchronized`（JDK 1.6 锁升级：偏向锁 → 轻量级锁 → 重量级锁）vs `ReentrantLock`（可中断、公平锁、Condition）
- `AbstractQueuedSynchronizer` (AQS) 原理：CLH 队列 + state 变量，理解一种就能推其他（`ReentrantLock`、`CountDownLatch`、`Semaphore` 都基于 AQS）
- `CountDownLatch` / `CyclicBarrier` / `Semaphore` 的使用场景区别
- `volatile`：可见性、禁止指令重排，但**不保证原子性**
- CAS 机制与 ABA 问题（`AtomicStampedReference` 解决）
- `ThreadLocal` 内存泄漏与最佳实践（`InheritableThreadLocal` / `TransmittableThreadLocal`）

## LearningNotes 补充：并发基础源码阅读主线

并发基础可以按“线程创建、线程通信、线程池、并发工具类”四条线学习。

## 线程创建方式

- 继承 `Thread`：简单但受 Java 单继承限制。
- 实现 `Runnable`：任务和线程解耦，更适合共享任务逻辑。
- 实现 `Callable`：可以返回结果，并配合 `Future` 获取执行结果。
- 使用线程池：生产环境首选，避免频繁创建和销毁线程。

面试时要强调：`Runnable` 和 `Callable` 描述的是任务，`Thread` 描述的是执行线程，线程池描述的是线程资源管理。

## wait 与 sleep

- `sleep()` 是 `Thread` 的静态方法，不释放对象锁，时间到后进入就绪状态。
- `wait()` 是 `Object` 的方法，必须在同步块中调用，会释放对象锁，等待 `notify()` 或 `notifyAll()` 唤醒。

这类问题要从“是否释放锁”和“属于哪个类”两个角度回答。

## 线程池源码级重点

`ThreadPoolExecutor` 核心参数：

- `corePoolSize`
- `maximumPoolSize`
- `keepAliveTime`
- `workQueue`
- `threadFactory`
- `handler`

任务提交主流程：

```text
execute
-> 如果工作线程数 < corePoolSize，创建核心线程
-> 否则尝试放入 workQueue
-> 队列满且线程数 < maximumPoolSize，创建非核心线程
-> 仍无法处理，执行拒绝策略
```

源码阅读重点：

- `ctl` 同时编码线程池状态和工作线程数量。
- `Worker` 继承 AQS，用来控制线程执行和中断。
- `getTask()` 决定线程是否阻塞等待、超时回收或退出。
- `runWorker()` 是工作线程循环取任务执行的核心。

## 生产者消费者

面试至少准备三种实现：

- `synchronized` + `wait/notify`
- `ReentrantLock` + `Condition`
- `BlockingQueue`

生产环境优先考虑 `BlockingQueue`，因为它把阻塞、唤醒、并发安全封装好了。

## 推荐断点

- `Thread.start`
- `ThreadPoolExecutor.execute`
- `ThreadPoolExecutor.addWorker`
- `ThreadPoolExecutor.runWorker`
- `ThreadPoolExecutor.getTask`
- `ArrayBlockingQueue.put`
- `ArrayBlockingQueue.take`
- `ReentrantLock.lock`
- `AbstractQueuedSynchronizer.acquire`

## 源码级面试话术

线程池的核心价值是复用线程和控制并发规模。`execute()` 提交任务后，会先尝试创建核心线程，再入队，再创建非核心线程，最后才走拒绝策略。源码里的 `ctl` 同时保存线程池状态和线程数量，`runWorker()` 循环从队列取任务执行，`getTask()` 决定线程是否需要回收。

## 参考来源

- [LearningNotes - Java 并发基础知识](https://github.com/francistao/LearningNotes/blob/master/Part2/JavaConcurrent/Java%E5%B9%B6%E5%8F%91%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86.md)
