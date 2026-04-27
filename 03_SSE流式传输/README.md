# SSE 流式传输 ⭐

## 项目应用

`ibrain-base` 流式推理输出；`ibrain-prompt` 推理与工作流流式返回；`ibrain-gpt-backend` 对话流式接口。

## 核心考点

- `SseEmitter` 生命周期：创建 → `send()` → `complete()` / `completeWithError()` / 超时
- SSE vs WebSocket：单向推送 vs 双向通信、HTTP/1.1 复用 vs 独立协议、轻量易接入 vs 全双工
- 线程安全：`SseEmitter` 非线程安全，多线程写入需同步或单线程消费
- 超时处理：`new SseEmitter(timeoutMs)` 设置；配合 `onTimeout` 回调释放资源
- 错误处理：`onError` / `onCompletion` 必须释放上下文（线程、连接、`MDC`）
- 前端消费：`EventSource` API 自动重连；浏览器 6 个并发连接限制
- OpenAI / Claude SSE 协议事件约定：`data: {...}\n\n`、`data: [DONE]`、`event: xxx`

## 面试话术

> 我们在 ibrain-base 基于 `SseEmitter + CompletableFuture` 实现了流式推理链路：模型增量 token 通过 `SseEmitter.send()` 推送到前端，超时通过 `orTimeout()` 兜底，`onError` 回调里释放上下文资源。在 ibrain-prompt 中还做了 OpenAI 流式 chunk 到 Claude SSE 协议事件的协议转换，**屏蔽不同模型的流式差异**，业务接入方拿到的始终是统一格式。
