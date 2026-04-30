# 多模型路由与适配怎么设计？

## 作答要点

- **抽象统一接口**：`InferenceService.invoke(ChatRequest) → ChatResponse`
- **工厂模式**：按 `modelType` 选具体实现（Azure / 通义 / Gemini / Bedrock / Kimi）
- **适配器模式**：每个厂商一个适配器封装鉴权、请求组装、响应解析
- **路由策略**：模型可用性、成本、配额、灰度、A/B 实验
- **降级链**：主模型失败 → 备模型 → 静态兜底

> 已接入 Azure、AWS Claude、通义、Gemini、豆包、Kimi、GLM、七牛等 10+ 模型/平台。新增模型零侵入：实现接口 + 注册工厂即可。
