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

## 源码级主线

Spring Security 的入口不是 Controller，也不是 Interceptor，而是 Servlet Filter。

核心链路：

```text
Servlet 容器 FilterChain
-> DelegatingFilterProxy
-> FilterChainProxy
-> SecurityFilterChain
-> 多个 Security Filter
-> DispatcherServlet
```

`DelegatingFilterProxy` 是 Servlet Filter，它把请求委托给 Spring 容器里的 `springSecurityFilterChain` Bean。这个 Bean 通常是 `FilterChainProxy`。

## 关键类

- `DelegatingFilterProxy`
- `FilterChainProxy`
- `SecurityFilterChain`
- `SecurityContextHolderFilter`
- `UsernamePasswordAuthenticationFilter`
- `BasicAuthenticationFilter`
- `BearerTokenAuthenticationFilter`
- `ExceptionTranslationFilter`
- `AuthorizationFilter`
- `AuthenticationManager`
- `AuthenticationProvider`
- `SecurityContextHolder`

## 认证源码流程

以用户名密码登录为例：

```text
UsernamePasswordAuthenticationFilter
-> attemptAuthentication
-> AuthenticationManager.authenticate
-> ProviderManager.authenticate
-> AuthenticationProvider.authenticate
-> UserDetailsService.loadUserByUsername
-> 认证成功后写入 SecurityContext
```

认证结果会封装成 `Authentication`，并存入 `SecurityContextHolder`。

## 授权源码流程

Spring Security 6 中授权核心通常落在：

```text
AuthorizationFilter
-> AuthorizationManager.check
-> AuthorizationDecision
```

旧版本常见链路里会看到 `FilterSecurityInterceptor`。

授权判断依赖当前请求、当前用户 `Authentication`、权限集合和配置规则。

## SecurityContext 的线程绑定

`SecurityContextHolder` 默认使用 `ThreadLocal` 保存当前用户上下文。

这解释了几个问题：

- 普通业务代码可以通过 `SecurityContextHolder.getContext()` 取当前用户。
- 异步线程默认拿不到主线程的认证上下文。
- 如果使用线程池，需要考虑上下文传递或手动设置。

## CAS 源码理解

CAS 场景通常涉及：

- CAS Server：统一认证中心。
- Service Ticket：登录成功后返回给业务系统的票据。
- CAS Client Filter：业务系统侧拦截和验票。
- Spring Security：验票成功后建立本地认证上下文。

核心流程：

```text
访问业务系统
-> 未登录，重定向 CAS Server
-> CAS 登录成功，带 ticket 回调业务系统
-> 业务系统调用 CAS Server 验票
-> 验票成功后创建 Authentication
-> 写入 SecurityContext
```

## 推荐断点

- `DelegatingFilterProxy.doFilter`
- `FilterChainProxy.doFilterInternal`
- `UsernamePasswordAuthenticationFilter.attemptAuthentication`
- `ProviderManager.authenticate`
- `DaoAuthenticationProvider.retrieveUser`
- `ExceptionTranslationFilter.doFilter`
- `AuthorizationFilter.doFilter`

## 源码级面试话术

Spring Security 是基于 Servlet Filter 链工作的，请求进入 Controller 前就已经完成认证和授权。`DelegatingFilterProxy` 负责把 Servlet 容器里的 Filter 调用委托给 Spring Bean，真正执行的是 `FilterChainProxy`。认证成功后会生成 `Authentication` 并放入 `SecurityContextHolder`，后续授权和业务代码都从这里获取当前用户。
