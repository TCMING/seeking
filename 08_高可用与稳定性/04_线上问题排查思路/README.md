# 线上问题排查思路

## 核心考点（系统化套路）

### CPU 飙高

`top` → `top -Hp <pid>` 找高 CPU 线程 → `printf '%x\n' <tid>` → `jstack <pid> | grep <hex_tid> -A 20`

### 内存溢出

监控 → dump → MAT 支配树 → 定位代码

### 接口慢

链路追踪（SkyWalking）→ 慢 SQL（`EXPLAIN`）→ 外部依赖（重试 / 超时）→ GC 影响

### 线程池打满

`jstack` 看线程状态分布、是否大量 `WAITING` / `TIMED_WAITING`、是否被外部 IO 阻塞

### 死锁

`jstack` 自带死锁检测；预防——加锁顺序一致、用 `tryLock` + 超时
