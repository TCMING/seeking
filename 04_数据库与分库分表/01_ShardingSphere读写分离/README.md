# ShardingSphere 读写分离 ⭐

## 项目应用

`ibrain-prompt` JPA + `HintManager` 主从路由。

## 核心考点

- 主从复制原理：Binlog 同步、异步 / 半同步 / 全同步复制
- 读写分离配置：ShardingSphere `readwrite-splitting` 规则
- `HintManager` 强制主库路由的场景：写后立即读、强一致性查询
- 主从延迟问题：监控延迟、超阈值切主库读、关键链路绕过从库
- ShardingSphere 5.x 相比 4.x 的架构变化：内核重构、规则配置统一、SQL 解析升级

## 面试话术

> 在 ibrain-prompt 中，我们用 ShardingSphere 5.1 做读写分离，JPA 作为 ORM 层。**对于写后立即读的场景，通过 `HintManager.setWriteRouteOnly()` 强制路由到主库**，避免主从延迟导致的数据不一致；同时对从库做了延迟监控，超过阈值自动切主库读取，保证可用性。
