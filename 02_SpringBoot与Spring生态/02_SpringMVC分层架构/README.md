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

## 源码级主线

Spring MVC 的核心入口是 `DispatcherServlet`。它本质是一个 Servlet，所有匹配到 Spring MVC 的请求都会先进入它。

核心调用链：

```text
HttpServlet.service
-> FrameworkServlet.service
-> FrameworkServlet.processRequest
-> DispatcherServlet.doService
-> DispatcherServlet.doDispatch
```

`doDispatch()` 是 Spring MVC 请求处理的核心方法。

## doDispatch() 关键步骤

```text
getHandler
-> getHandlerAdapter
-> HandlerInterceptor.preHandle
-> HandlerAdapter.handle
-> HandlerInterceptor.postHandle
-> processDispatchResult
-> HandlerInterceptor.afterCompletion
```

理解 Spring MVC，重点看四类组件：

- `HandlerMapping`：根据请求找到处理器，也就是 Controller 方法。
- `HandlerAdapter`：负责真正调用处理器。
- `HandlerMethodArgumentResolver`：负责参数绑定。
- `HandlerMethodReturnValueHandler`：负责返回值处理。

## Controller 方法如何被找到

关键类：

- `RequestMappingHandlerMapping`
- `RequestMappingInfo`
- `HandlerMethod`

启动时，`RequestMappingHandlerMapping` 会扫描 Controller Bean，把 `@RequestMapping`、`@GetMapping`、`@PostMapping` 等注解解析成 `RequestMappingInfo`，并和具体 `HandlerMethod` 建立映射。

请求进来时，Spring MVC 根据 URL、HTTP Method、请求参数、Header、Content-Type 等条件匹配最合适的 `HandlerMethod`。

## 参数绑定源码

关键类：

- `InvocableHandlerMethod`
- `HandlerMethodArgumentResolverComposite`
- `RequestResponseBodyMethodProcessor`
- `PathVariableMethodArgumentResolver`
- `RequestParamMethodArgumentResolver`
- `ModelAttributeMethodProcessor`

例如：

- `@RequestParam` 由 `RequestParamMethodArgumentResolver` 处理。
- `@PathVariable` 由 `PathVariableMethodArgumentResolver` 处理。
- `@RequestBody` 由 `RequestResponseBodyMethodProcessor` 处理。

`@RequestBody` 的 JSON 反序列化底层依赖 `HttpMessageConverter`，常见实现是 `MappingJackson2HttpMessageConverter`。

## 返回值处理源码

关键类：

- `HandlerMethodReturnValueHandlerComposite`
- `RequestResponseBodyMethodProcessor`
- `ResponseEntityMethodProcessor`
- `ModelAndViewMethodReturnValueHandler`

`@ResponseBody` 和 `@RestController` 返回 JSON，本质也是走 `HttpMessageConverter`，把 Java 对象写入 HTTP 响应体。

## 异常处理源码

关键类：

- `HandlerExceptionResolver`
- `ExceptionHandlerExceptionResolver`
- `ResponseStatusExceptionResolver`
- `DefaultHandlerExceptionResolver`

`@ControllerAdvice` + `@ExceptionHandler` 最终由 `ExceptionHandlerExceptionResolver` 解析和执行。

## 过滤器与拦截器源码区别

`Filter` 属于 Servlet 规范，执行点在 Spring MVC 外层。Spring Security 就是通过 Filter 链生效。

`HandlerInterceptor` 属于 Spring MVC，执行点在 `DispatcherServlet.doDispatch()` 内部，已经完成 HandlerMapping 匹配。

## 推荐断点

- `DispatcherServlet.doDispatch`
- `RequestMappingHandlerMapping.getHandlerInternal`
- `RequestMappingHandlerAdapter.invokeHandlerMethod`
- `InvocableHandlerMethod.invokeForRequest`
- `HandlerMethodArgumentResolverComposite.resolveArgument`
- `HandlerMethodReturnValueHandlerComposite.handleReturnValue`
- `ExceptionHandlerExceptionResolver.doResolveHandlerMethodException`

## 源码级面试话术

Spring MVC 的请求入口是 `DispatcherServlet`，核心方法是 `doDispatch()`。它先通过 `HandlerMapping` 找到 Controller 方法，再通过 `HandlerAdapter` 调用。方法参数不是 Controller 自己解析的，而是由一组 `HandlerMethodArgumentResolver` 完成；返回值也不是直接写响应，而是由 `HandlerMethodReturnValueHandler` 和 `HttpMessageConverter` 处理。
