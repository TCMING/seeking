# 消息队列常见问题

## 核心考点

- **消息重复消费**：网络抖动、消费 ACK 失败、Rebalance → **业务侧幂等**（去重表、Redis SETNX、状态机）
- **消息丢失**：发送丢、Broker 丢、消费丢 → 三段保障
- **消息堆积**：扩 Consumer 实例 / 增加 Queue 数量（Topic 配置）/ 临时降级丢弃非核心消息 / 死信队列处理
- **顺序消费**：同业务 ID 路由到同一 Queue + 消费端串行处理
- RocketMQ vs Kafka 对比：RocketMQ 事务消息和延迟消息更友好，Kafka 吞吐更高、生态更广
