# 熔断与降级 ⭐

## 项目应用

`ibrain-prompt` Hystrix 熔断隔离；`CostLimitServiceAdapter` 超时降级。

## 核心考点

- 熔断器三种状态：`Closed → Open → Half-Open`，及切换条件
- Hystrix：线程隔离 vs 信号量隔离、超时、降级、Bulkhead
- Hystrix vs Sentinel vs Resilience4j：Hystrix 已停止维护、Sentinel 国内主流、Resilience4j 函数式风格更轻
- 降级策略：默认值返回、缓存返回、简化逻辑、静态兜底页
- 超时控制：外部模型抖动时快速失败，避免线程池被打满

## 面试话术

> 在 ibrain-prompt 中，我们用 Hystrix 做推理链路的熔断隔离。**当外部模型服务响应抖动时，Hystrix 超时后快速失败，配合 `CostLimitServiceAdapter` 做降级返回**，避免慢调用拖垮主链路线程池。优化前 P99 超时率高，优化后核心链路 P99 超时率降低约 60%。
