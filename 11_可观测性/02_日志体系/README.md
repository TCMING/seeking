# 日志体系

## 项目应用

`ibrain-base`、`ibrain-gpt-backend` 使用 Log4j2。

## 核心考点

- Log4j2 vs Logback：Log4j2 异步日志（`AsyncLogger`，基于 Disruptor 无锁队列）性能显著优于 Logback
- 日志级别动态调整：Spring Boot Actuator `loggers` 端点
- MDC：链路追踪上下文传递；跨线程要用 `TransmittableThreadLocal` 解决 `ThreadLocal` 不传递问题
- 敏感信息脱敏：密码、Token、手机号、身份证
- Log4Shell（CVE-2021-44228）警示：版本管理与漏洞响应
