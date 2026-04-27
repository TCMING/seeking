# 序列化与协议

## 项目应用

`ibrain-base` 使用 Protobuf 3.25.3 做模型相关协议定义；服务间用 JSON（Jackson / Fastjson2）；Dubbo RPC 默认 Hessian。

## 核心考点

- JSON：Jackson vs Fastjson vs Gson 对比；Fastjson 历史漏洞（autoType）警示
- Protobuf：IDL 驱动、二进制紧凑、向后兼容（保留 tag、不要复用 tag、字段标 `optional`）
- Hessian / Kryo：Dubbo 与 RPC 框架常用，性能 vs 兼容性权衡
- 序列化版本兼容：`serialVersionUID` 的作用
- 序列化安全：避免反序列化漏洞，关闭未授权类型
