# Spring Security 与 CAS ⭐

## 项目应用

`ibrain-prompt` 多租户鉴权；`ibrain-gpt-backend` 三层访问控制（用户级、应用级、接口级）。

## 核心考点

- Spring Security 核心：`Authentication`、`Authorization`、`SecurityContext`、`FilterChain`
- 关键过滤器：`UsernamePasswordAuthenticationFilter`、`BasicAuthenticationFilter`、`FilterSecurityInterceptor`
- CAS 单点登录流程：浏览器 → CAS Server 登录 → 回调带 ST → 应用验票 → 建本地 Session
- `UserDetailsService` 自定义认证逻辑
- RBAC + `@PreAuthorize` / `@Secured`
- API Token 鉴权与 Session 鉴权的取舍：无状态、跨域、移动端友好
- 多租户隔离：Schema 隔离、Row-Level（`tenant_id` 列）、Token 隔离

## 面试话术

> 在 ibrain-prompt 中，我们基于 CAS + Spring Security 实现了多租户鉴权体系。CAS 负责 SSO 认证，Spring Security 负责授权与接口级拦截，同时通过 API Token 支撑服务间调用。在 ibrain-gpt-backend 中进一步细化到**用户级、应用级、接口级三层访问控制**，超限响应时间控制在 5ms 以内。
