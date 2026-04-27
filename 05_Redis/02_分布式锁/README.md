# 分布式锁 ⭐

## 项目应用

`midjourney-proxy` Redisson 分布式锁保障任务幂等；`luffy` 避免重复调度。

## 核心考点

- Redis 分布式锁的坑：`SETNX` + `EXPIRE` 非原子 → `SET key value NX PX ms`
- **锁续期问题**：业务未完成锁已过期 → Redisson Watchdog 自动续期（默认 30s 过期 / 10s 续期）
- Redisson 高级锁：可重入锁、公平锁、读写锁、联锁（MultiLock）、信号量
- 锁释放安全：value 用 UUID + Lua 脚本保证「比对+删除」原子
- RedLock 算法及争议（Martin Kleppmann vs antirez）
- 分布式锁 vs 数据库乐观锁：性能 vs 强一致

## 面试话术

> 在 midjourney-proxy 中，我们用 Redisson 分布式锁保障异步任务的幂等提交。Redisson 的 **Watchdog 机制每 10 秒自动续期一次**，避免业务未完成锁就过期被其他请求抢走；释放锁内置 Lua 脚本做 value 比对，避免误删别人的锁。相比手写 `SET NX EX`，Redisson 把可重入、续期、释放安全这些细节都封装好了。
