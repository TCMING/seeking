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
