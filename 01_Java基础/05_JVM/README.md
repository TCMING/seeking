# JVM ⭐

## 项目应用

所有线上服务均涉及 JVM 调优、OOM 排查、GC 优化。

## 核心考点

### 内存模型

堆（新生代 Eden + S0/S1、老年代）、栈、方法区（元空间）、程序计数器、本地方法栈

### 垃圾回收算法

标记-清除、标记-整理、复制算法（新生代）、分代收集

### 垃圾收集器

- CMS：老年代并发收集，三色标记 + 增量更新，缺点是浮动垃圾、内存碎片
- G1：分 Region、并发标记 + 复制算法，可控停顿（`-XX:MaxGCPauseMillis`）
- ZGC / Shenandoah（JDK 11+）：低延迟、染色指针、亚毫秒级停顿

### JVM 调优常用参数

- `-Xms` / `-Xmx`：堆初始 / 最大值，建议设置一致避免动态扩容
- `-Xmn`：新生代大小
- `-XX:MetaspaceSize` / `-XX:MaxMetaspaceSize`：元空间
- `-XX:+HeapDumpOnOutOfMemoryError`：OOM 时自动 dump

### OOM 排查实战四步法

1. 通过监控（GC 频率、堆使用率、线程数）定位 OOM 类型
2. `jmap -dump:format=b,file=heap.hprof <pid>` 或线上预设的 `HeapDumpOnOutOfMemoryError`
3. MAT / VisualVM / `jhat` 分析支配树（Dominator Tree），找到内存占用 Top 对象
4. 结合代码定位泄漏点（常见：`ThreadLocal` 未清理、静态集合无限增长、连接未关闭、缓存无淘汰策略）

### 类加载机制

双亲委派模型（启动类加载器 → 扩展类加载器 → 应用类加载器）、打破双亲委派的场景（SPI、Tomcat WebappClassLoader、OSGi、热部署）

## 面试话术

> 我们 ibrain-prompt 服务上线后曾经出现过 Full GC 频繁，CPU 飙高的问题。先通过监控发现老年代使用率持续高位，然后 dump 堆，用 MAT 分析支配树，定位到一个本地缓存没有设置过期策略，长时间运行后内存堆积。修复后用 G1 收集器替代 CMS，并设置 `-XX:MaxGCPauseMillis=200`，P99 GC 停顿稳定在 200ms 以内。
