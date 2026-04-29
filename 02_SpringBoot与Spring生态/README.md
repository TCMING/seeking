# Spring Boot 与 Spring 生态源码级学习路线

学习 Spring 不能只停留在注解使用层。面试深入到源码时，核心是能把“一个注解或一次请求”还原成框架内部调用链。

## 建议源码阅读顺序

1. Spring 容器启动：`SpringApplication.run` -> `refreshContext` -> `AbstractApplicationContext.refresh`
2. Bean 创建：`DefaultListableBeanFactory` -> `AbstractAutowireCapableBeanFactory` -> Bean 生命周期
3. 自动装配：`@SpringBootApplication` -> `AutoConfigurationImportSelector` -> 条件装配
4. MVC 请求链路：`DispatcherServlet` -> `HandlerMapping` -> `HandlerAdapter` -> 参数解析 -> 返回值处理
5. AOP 代理：`AnnotationAwareAspectJAutoProxyCreator` -> `ProxyFactory` -> JDK/CGLIB
6. 事务：`TransactionInterceptor` -> `PlatformTransactionManager` -> commit/rollback
7. Security：`DelegatingFilterProxy` -> `FilterChainProxy` -> Security Filter Chain
8. Event/Async：`ApplicationEventMulticaster`、`AsyncAnnotationBeanPostProcessor`

## 源码学习方法

- 先找入口类，再看模板方法，再看扩展点。
- 优先看接口和抽象类：Spring 大量使用模板方法、策略模式、责任链模式。
- 带着问题看源码，例如“为什么同类调用事务失效”“Controller 参数怎么绑定”“自动装配类从哪里加载”。
- 本地调试时建议从最小 Spring Boot Demo 开始，断点不要一开始打太多。

## 高频源码问题

- Spring Boot 启动过程做了什么？
- Bean 生命周期完整流程是什么？
- 自动装配如何加载候选配置类？
- `@ConditionalOnMissingBean` 为什么能控制默认 Bean？
- `DispatcherServlet` 如何找到 Controller？
- `@RequestBody` 和 `@ResponseBody` 是谁处理的？
- Spring AOP 为什么同类方法调用会失效？
- `@Transactional` 的事务何时开启、提交、回滚？
- Spring Security 的过滤器链如何生效？
- `@Async` 为什么必须走代理？

