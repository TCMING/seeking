# Q7: 项目中遇到过最严重的线上问题是什么？怎么解决的？

> 一次 ibrain-prompt 服务 Full GC 频繁、CPU 飙高。
>
> - **定位**：监控发现老年代使用率高，`jmap` dump 后用 MAT 分析支配树，定位到本地缓存没有过期策略；
> - **修复**：用 Caffeine 替换原生 HashMap 缓存，设置 `maximumSize` + `expireAfterWrite`；
> - **优化**：从 CMS 切到 G1，设置 `MaxGCPauseMillis=200`；
> - **结果**：P99 GC 停顿从秒级降到 200ms 以内，CPU 使用率从 80% 回落到 30%。
