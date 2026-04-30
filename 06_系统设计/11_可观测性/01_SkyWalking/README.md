# SkyWalking

## 项目应用

`ibrain-base`、`ibrain-gpt-backend` 使用 SkyWalking 链路追踪。

## 核心考点

- 分布式链路追踪三要素：`TraceId`、`SpanId`、`ParentSpanId`
- Java Agent 字节码增强（ByteBuddy）实现无侵入接入
- 服务拓扑、慢接口 Top N、依赖拓扑分析
- 自定义埋点：`@Trace`、`ActiveSpan.tag()`
- SkyWalking vs Zipkin vs Jaeger：SkyWalking 中文文档好、面板丰富；Jaeger CNCF 项目；Zipkin 轻量
