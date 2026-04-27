# 大模型流式输出怎么实现？

## 作答要点

1. **协议层**：HTTP 用 SSE（轻量、单向、自动重连），多端用 WebSocket
2. **服务端**：`SseEmitter` + `CompletableFuture` + 自定义线程池；增量 token 通过 `send()` 推送；`orTimeout()` 兜底
3. **协议适配**：OpenAI `data: {...}\n\ndata: [DONE]` 与 Claude `event: message_delta` 的转换层
4. **资源管理**：`onError` / `onTimeout` / `onCompletion` 回调释放上下文、清理 `MDC`
5. **稳定性**：限流、熔断、降级到非流式响应
