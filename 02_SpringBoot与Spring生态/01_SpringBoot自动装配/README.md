# Spring Boot 自动装配 ⭐

## 项目应用

所有项目均基于 Spring Boot 2.x 自动装配；`midjourney-proxy` 通过精准 `ComponentScan` 优化启动时间。

## 核心考点

- `@SpringBootApplication` 注解三件套：`@ComponentScan` + `@EnableAutoConfiguration` + `@Configuration`
- 自动装配加载机制：Spring Boot 2.x `META-INF/spring.factories` → Spring Boot 3.x `AutoConfiguration.imports`
- `@Conditional` 系列条件装配：`@ConditionalOnClass`、`@ConditionalOnProperty`、`@ConditionalOnMissingBean`
- 自定义 Starter 套路：自动配置类 + `spring.factories` + 暴露 `@ConfigurationProperties`
- Bean 生命周期：实例化 → 属性赋值 → `Aware` 接口 → `BeanPostProcessor.before` → `@PostConstruct` / `InitializingBean.afterPropertiesSet` → `BeanPostProcessor.after` → 使用 → `@PreDestroy` / `DisposableBean.destroy`

## 面试话术

> 在 midjourney-proxy 中，我们通过精准配置 `@ComponentScan` 排除了无关的 Bean 初始化，将启动时间从 40+ 秒降到 20 秒以内。复杂项目里**自动装配虽然方便，但 Bean 数量膨胀会显著拖慢启动**，所以我们做了 `basePackages` 收敛，并通过 `@ConditionalOnProperty` 关闭测试环境不需要的 Bean。
