# 内容安全 / WAF 怎么做？

## 作答要点

- **双向检测**：输入审核（避免恶意 prompt）+ 输出审核（避免违规生成）
- **流式输出审核**：分片送审 + 滑动窗口聚合（避免上下文割裂误判）
- **主链路隔离**：审核异步化 / 超时兜底，**不能因审核挂掉影响主流程**
- **观察 vs 拦截模式**：灰度时观察记录、稳定后切拦截
- 参考 OWASP LLM Top 10：Prompt Injection、Data Leakage、Insecure Output Handling
