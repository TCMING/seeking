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

## 源码级主线

Spring Boot 启动入口通常是：

```java
SpringApplication.run(Application.class, args);
```

核心调用链：

```text
SpringApplication.run
-> SpringApplication.prepareEnvironment
-> SpringApplication.createApplicationContext
-> SpringApplication.prepareContext
-> SpringApplication.refreshContext
-> AbstractApplicationContext.refresh
```

真正进入 Spring 容器生命周期的是 `AbstractApplicationContext.refresh()`。这是 Spring 源码里最重要的模板方法之一。

## refresh() 核心步骤

```text
prepareRefresh
obtainFreshBeanFactory
prepareBeanFactory
postProcessBeanFactory
invokeBeanFactoryPostProcessors
registerBeanPostProcessors
initMessageSource
initApplicationEventMulticaster
onRefresh
registerListeners
finishBeanFactoryInitialization
finishRefresh
```

面试重点不是背全方法名，而是理解三段：

- BeanDefinition 加载：把类、XML、配置转换成 BeanDefinition。
- BeanFactory 后置处理：扩展 BeanDefinition，例如配置类解析、自动装配导入。
- 单例 Bean 实例化：创建非懒加载单例 Bean，并执行完整生命周期。

## 自动装配源码入口

`@SpringBootApplication` 包含：

```java
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan
```

`@EnableAutoConfiguration` 通过 `@Import(AutoConfigurationImportSelector.class)` 导入自动配置。

关键类：

- `AutoConfigurationImportSelector`
- `ImportCandidates`
- `AutoConfiguration.imports`
- `SpringFactoriesLoader`，主要用于 Spring Boot 2.x 时代的 `spring.factories`
- `ConditionEvaluator`
- `OnClassCondition`
- `OnBeanCondition`
- `OnPropertyCondition`

Spring Boot 2.x 主要从 `META-INF/spring.factories` 加载自动配置类。Spring Boot 3.x 改为优先使用 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`。

## 条件装配源码理解

`@ConditionalOnClass`、`@ConditionalOnMissingBean`、`@ConditionalOnProperty` 本质都是条件判断。Spring 在解析配置类时，会通过 `ConditionEvaluator` 判断当前配置类或 Bean 方法是否应该生效。

典型例子：

```java
@ConditionalOnMissingBean
public MyService myService() {
    return new DefaultMyService();
}
```

源码含义是：如果容器里已经有用户自定义的 `MyService`，自动配置里的默认 Bean 就不会注册。这就是 Spring Boot “约定优于配置，但允许用户覆盖默认实现”的核心机制。

## Bean 生命周期源码链路

创建 Bean 的关键类：

- `DefaultListableBeanFactory`
- `AbstractBeanFactory`
- `AbstractAutowireCapableBeanFactory`
- `BeanPostProcessor`
- `InstantiationAwareBeanPostProcessor`

核心调用链：

```text
getBean
-> doGetBean
-> createBean
-> doCreateBean
-> createBeanInstance
-> populateBean
-> initializeBean
-> applyBeanPostProcessorsBeforeInitialization
-> invokeInitMethods
-> applyBeanPostProcessorsAfterInitialization
```

`BeanPostProcessor` 是 Spring 扩展能力的核心。AOP、`@Autowired`、`@Async`、`@ConfigurationProperties` 等能力都依赖各种后置处理器参与 Bean 创建过程。

## 推荐断点

- `SpringApplication.run`
- `AbstractApplicationContext.refresh`
- `PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors`
- `ConfigurationClassPostProcessor.processConfigBeanDefinitions`
- `AutoConfigurationImportSelector.selectImports`
- `AbstractAutowireCapableBeanFactory.doCreateBean`

## 源码级面试话术

Spring Boot 自动装配不是简单扫描所有 jar，而是从约定位置加载候选自动配置类，再结合 `@Conditional` 条件判断是否注册。真正把自动配置接入容器的是 `AutoConfigurationImportSelector`，它通过 `@Import` 参与配置类解析流程。最终自动配置类里的 `@Bean` 方法会转成 BeanDefinition，在 `refresh()` 的后半段创建成单例 Bean。
