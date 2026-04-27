# 缓存与数据结构 ⭐

## 项目应用

所有项目均使用 Redis；`ibrain-base` 使用 Spring Cache + Caffeine 多级缓存。

## 核心考点

- 五种基本数据结构 + 三种高级（Bitmap、HyperLogLog、GEO）及使用场景
- 缓存三大问题：
  - **穿透**：查不存在的数据 → 布隆过滤器、缓存空值
  - **击穿**：热点 key 过期瞬间 → 互斥锁、永不过期 + 异步刷新
  - **雪崩**：大量 key 同时过期 → 随机过期、多级缓存、限流降级
- 缓存一致性策略：Cache Aside（先更 DB 再删缓存）、Write Through、Write Behind
- 双删延迟策略解决主从延迟下的不一致
- Spring Cache 注解：`@Cacheable`、`@CacheEvict`、`@CachePut`
- 本地缓存（Caffeine）+ Redis 多级缓存：减少网络开销、应对热点
