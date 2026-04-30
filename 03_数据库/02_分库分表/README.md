# 分库分表

## 项目应用

`ibrain-prompt`、`ibrain-gpt-backend`、`midjourney-proxy` 均使用 ShardingSphere 5.1.0。

## 核心考点

- 垂直分库（按业务）vs 水平分库（按数据量）
- 分片策略：取模、范围、一致性 Hash、复合分片
- 分布式主键：Snowflake（注意时钟回拨）、UUID、号段模式（Leaf）
- 跨分片查询挑战：JOIN、聚合、分页（`LIMIT 10000, 10` 的全分片扫描问题）
- **分库分表后的分页优化**：禁止深翻页、改造为流式 / 游标分页、二次查询
- 分布式事务：XA、TCC、Saga、本地消息表、Seata AT 模式
