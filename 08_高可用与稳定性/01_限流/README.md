# 限流 ⭐

## 项目应用

`ibrain-gpt-backend` 日均百万级请求限流；`ibrain-prompt` 推理入口限流。

## 核心考点

- 算法：固定窗口、滑动窗口、令牌桶（Guava `RateLimiter`）、漏桶
- 单机限流（Guava）vs 分布式限流（Redis + Lua）
- 限流粒度：接口级、用户级、应用级、IP 级
- 限流响应策略：快速失败、排队等待、降级返回
- 工具：Sentinel（流量整形 + 熔断 + 系统保护一体化）
