# RocketMQ ⭐

## 项目应用

`ibrain-base` 成本消息、异步事件；`ibrain-gpt-backend` 异步解耦。

## 核心考点

- 核心概念：Producer、Consumer、Broker、NameServer、Topic、Queue
- 消息可靠性三段：发送端重试 + 同步 / 异步发送、Broker 同步 / 异步刷盘 + 主从复制、消费端 ACK + 重试队列
- 顺序消息：局部有序（同一 MessageQueue）vs 全局有序（单 Queue 性能差）
- 延迟消息（RocketMQ 18 个固定 level）vs 任意时间定时消息（5.x 支持）
- 事务消息：half message + 二次确认 + 回查机制
- 消费模式：集群消费 vs 广播消费
