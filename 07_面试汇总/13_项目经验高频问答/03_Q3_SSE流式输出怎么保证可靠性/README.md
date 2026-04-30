# Q3: SSE 流式输出怎么保证可靠性？

> 基于 `SseEmitter + CompletableFuture`：
>
> 1. `orTimeout()` 控制超时自动结束；
> 2. `onError` / `onCompletion` 回调释放线程、连接、`MDC` 上下文；
> 3. **自定义线程池**避免公共池耗尽；
> 4. 协议适配层兼容 OpenAI / Claude SSE，对业务方屏蔽差异；
> 5. 前端 `EventSource` 自动重连兜底网络抖动。
