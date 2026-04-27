# Dubbo RPC

## 项目应用

`ibrain-base` 使用 Dubbo 2.7.18 做 RPC 调用。

## 核心考点

- 核心架构：Provider、Consumer、Registry（Zookeeper / Nacos）、Monitor
- 通信模型：长连接 + Netty NIO
- 负载均衡：`Random`（默认）、`RoundRobin`、`LeastActive`、`ConsistentHash`
- 容错策略：`Failover`（默认重试）、`Failfast`、`Failsafe`、`Failback`、`Forking`、`Broadcast`
- SPI 机制：基于 `META-INF/dubbo` 的扩展点加载，相比 Java SPI 支持按需加载与 IoC
- Dubbo vs Spring Cloud vs gRPC 对比
