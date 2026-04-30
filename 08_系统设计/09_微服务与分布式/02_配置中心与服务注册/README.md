# 配置中心与服务注册

## 项目应用

iQiyi `config-client` + `Nacos` 做配置管理与服务注册。

## 核心考点

- Nacos 三大能力：配置管理、服务发现、健康检查
- 配置热更新：长轮询（客户端发起 + 服务端 hold 30s）vs 推送
- Nacos AP / CP 模式切换（基于 Raft / Distro 协议）
- 命名空间（环境隔离）+ Group（业务隔离）+ Data ID 三层模型
- Nacos vs Apollo vs Spring Cloud Config：Nacos 一站式（配置 + 注册）、Apollo 治理能力强、Config 偏简单
