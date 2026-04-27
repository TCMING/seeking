# 知识点与项目映射速查

| 知识点                   | 项目                                           | 具体应用                     | 高频度 |
| --------------------- | -------------------------------------------- | ------------------------ | --- |
| CompletableFuture     | ibrain-base、ibrain-prompt                    | 流式推理异步编排、工作流超时控制         | ⭐⭐⭐ |
| 线程池                   | ibrain-base、luffy                            | 自定义线程池、任务执行池             | ⭐⭐⭐ |
| JVM 调优 / GC           | 全项目                                          | OOM 排查、Full GC 优化        | ⭐⭐⭐ |
| Netty / IO 模型         | ibrain-base、midjourney-proxy                 | Dubbo 底层、JDA 长连接         | ⭐⭐  |
| SseEmitter            | ibrain-base、ibrain-prompt、ibrain-gpt-backend | 流式推理 / 对话 / 工作流输出        | ⭐⭐⭐ |
| AOP & 事务              | 全项目                                          | 切面埋点、`@Transactional` 传播 | ⭐⭐⭐ |
| Spring Security + CAS | ibrain-prompt、ibrain-gpt-backend             | 多租户鉴权、三层访问控制             | ⭐⭐  |
| JPA + ShardingSphere  | ibrain-prompt、ibrain-gpt-backend             | 读写分离、分库分表                | ⭐⭐⭐ |
| Redis 多级缓存            | ibrain-base、全项目                              | Caffeine + Redis         | ⭐⭐⭐ |
| Redis 分布式锁            | midjourney-proxy、luffy                       | 任务幂等、调度并发控制              | ⭐⭐⭐ |
| Redisson              | midjourney-proxy                             | 分布式锁 + Watchdog 续期       | ⭐⭐  |
| RocketMQ              | ibrain-base、ibrain-gpt-backend               | 成本消息、异步解耦                | ⭐⭐  |
| Hystrix 熔断降级          | ibrain-prompt                                | 推理链路熔断、超时降级              | ⭐⭐⭐ |
| 限流                    | ibrain-gpt-backend、ibrain-prompt             | 接口/用户/应用级三层限流            | ⭐⭐⭐ |
| 幂等设计                  | midjourney-proxy                             | 异步任务幂等提交                 | ⭐⭐  |
| XXL-Job               | 全项目                                          | 定时调度、分片广播                | ⭐⭐  |
| SkyWalking            | ibrain-base、ibrain-gpt-backend               | 分布式链路追踪                  | ⭐⭐  |
| Log4j2 + MDC          | ibrain-base、ibrain-gpt-backend               | 异步日志、链路上下文               | ⭐⭐  |
| Dubbo RPC             | ibrain-base                                  | 服务间 RPC                  | ⭐⭐  |
| Nacos                 | ibrain-base、ibrain-prompt                    | 配置中心 + 服务注册              | ⭐⭐  |
| DAG 工作流               | ibrain-prompt                                | 多节点编排引擎（项目亮点）            | ⭐⭐⭐ |
| 多模型路由                 | ibrain-base                                  | 工厂 + 适配器，10+ 模型接入（项目亮点）  | ⭐⭐⭐ |
| Tool Calling / MCP    | ibrain-gpt-backend                           | 工具调用 + 插件扩展（项目亮点）        | ⭐⭐  |
| WebFlux               | luffy                                        | 高并发调度响应式处理               | ⭐   |

> **图例**：⭐⭐⭐ 必背高频；⭐⭐ 重点掌握；⭐ 加分项。
