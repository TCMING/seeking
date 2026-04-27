# Spring MVC 分层架构

## 项目应用

所有项目的 Controller / Service / DAO 分层。

## 核心考点

- `DispatcherServlet` 请求处理流程：`HandlerMapping` → `HandlerAdapter` → `Controller` → `ViewResolver`
- `@RequestMapping` 路由匹配优先级
- 参数绑定与数据校验：`@Valid`、`@Validated`、Hibernate Validator、分组校验
- 统一异常处理：`@ControllerAdvice` + `@ExceptionHandler`，区分业务异常 / 系统异常 / 参数异常
- 统一响应封装：`ResponseEntity` / 全局 `Result<T>` 模型
- 拦截器（`HandlerInterceptor`）vs 过滤器（`Filter`）：执行顺序、作用范围（Filter 在 Servlet 容器层，Interceptor 在 Spring 层）
