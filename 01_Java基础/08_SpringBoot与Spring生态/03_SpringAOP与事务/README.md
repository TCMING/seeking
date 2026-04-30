# Spring AOP 与事务 ⭐

## 项目应用

`ibrain-prompt` 接口耗时埋点、统一鉴权切面；`ibrain-base` 多数据源切换 AOP；`@Transactional` 全项目使用。

## 核心考点

### AOP

- AOP 实现：JDK 动态代理（接口）vs CGLIB（子类继承），Spring AOP 默认根据是否实现接口选择
- 通知类型：`@Before`、`@After`、`@AfterReturning`、`@AfterThrowing`、`@Around`
- 切点表达式：`execution()`、`@annotation()`、`within()`

### @Transactional 七种传播机制（高频考点）

- `REQUIRED`（默认）：有事务加入，没事务新建
- `REQUIRES_NEW`：挂起当前事务，新建独立事务
- `NESTED`：嵌套事务（基于 SavePoint）
- `SUPPORTS`、`NOT_SUPPORTED`、`MANDATORY`、`NEVER`

### 事务失效场景（必背）

1. 方法非 public
2. 同类内部方法调用（绕过代理）
3. 异常被 catch 没抛出
4. 抛出 checked exception 但未配置 `rollbackFor`
5. 数据库引擎不支持事务（如 MyISAM）
6. 多线程调用（事务上下文绑定 `ThreadLocal`）

### 隔离级别

`READ_UNCOMMITTED`、`READ_COMMITTED`、`REPEATABLE_READ`（MySQL 默认，通过 MVCC + Next-Key Lock 解决幻读）、`SERIALIZABLE`

## AOP 源码级主线

Spring AOP 的核心不是注解本身，而是 Bean 创建过程中生成代理对象。

关键类：

- `AnnotationAwareAspectJAutoProxyCreator`
- `AbstractAutoProxyCreator`
- `ProxyFactory`
- `JdkDynamicAopProxy`
- `CglibAopProxy`
- `ReflectiveMethodInvocation`
- `MethodInterceptor`

核心流程：

```text
Bean 创建
-> BeanPostProcessor.postProcessAfterInitialization
-> AbstractAutoProxyCreator.wrapIfNecessary
-> 找到适用于当前 Bean 的 Advisor
-> ProxyFactory 创建代理
-> JDK 动态代理或 CGLIB 代理
```

`AnnotationAwareAspectJAutoProxyCreator` 本身是一个 `BeanPostProcessor`，它在 Bean 初始化后判断当前 Bean 是否需要被 AOP 增强。如果需要，就返回代理对象替代原始对象放入容器。

## AOP 调用链源码

代理方法被调用时：

```text
JdkDynamicAopProxy.invoke
或 CglibAopProxy.DynamicAdvisedInterceptor.intercept
-> 获取当前方法的拦截器链
-> ReflectiveMethodInvocation.proceed
-> 按顺序执行 MethodInterceptor
-> 调用目标方法
```

`@Around`、`@Before`、`@After` 等通知最终都会被适配成不同的 `MethodInterceptor`。

## 为什么同类调用 AOP 失效

```java
public void a() {
    this.b();
}

@Transactional
public void b() {
}
```

`this.b()` 调用的是当前对象本身，不经过 Spring 容器里的代理对象，所以事务、AOP、`@Async` 都不会生效。

解决方式：

- 把 `b()` 移到另一个 Spring Bean。
- 通过代理对象调用。
- 使用 `AopContext.currentProxy()`，但需要开启 `exposeProxy`，不建议滥用。

## 事务源码级主线

`@Transactional` 的核心是 AOP 拦截器：

- `TransactionInterceptor`
- `TransactionAspectSupport`
- `PlatformTransactionManager`
- `DataSourceTransactionManager`
- `JpaTransactionManager`
- `TransactionSynchronizationManager`

核心调用链：

```text
代理方法调用
-> TransactionInterceptor.invoke
-> TransactionAspectSupport.invokeWithinTransaction
-> createTransactionIfNecessary
-> 调用目标方法
-> commitTransactionAfterReturning
或 completeTransactionAfterThrowing
```

## 事务上下文如何绑定

Spring 事务上下文主要通过 `TransactionSynchronizationManager` 保存在线程本地变量里。

这解释了两个高频问题：

- 多线程中事务不传播，因为事务上下文绑定在当前线程。
- `@Async` 方法里的数据库操作不会自动加入外层事务，因为它运行在另一个线程。

## 回滚规则源码理解

默认情况下：

- `RuntimeException` 和 `Error` 会回滚。
- checked exception 不回滚，除非配置 `rollbackFor`。

对应源码逻辑在 `RuleBasedTransactionAttribute.rollbackOn()` 附近。

## 推荐断点

- `AbstractAutoProxyCreator.wrapIfNecessary`
- `AnnotationAwareAspectJAutoProxyCreator.findCandidateAdvisors`
- `JdkDynamicAopProxy.invoke`
- `CglibAopProxy.DynamicAdvisedInterceptor.intercept`
- `ReflectiveMethodInvocation.proceed`
- `TransactionInterceptor.invoke`
- `TransactionAspectSupport.invokeWithinTransaction`
- `DataSourceTransactionManager.doBegin`
- `AbstractPlatformTransactionManager.processCommit`
- `AbstractPlatformTransactionManager.processRollback`

## 源码级面试话术

Spring AOP 是在 Bean 初始化后通过 `BeanPostProcessor` 判断是否需要创建代理对象。事务本质就是一个 AOP 增强，`@Transactional` 方法被调用时会进入 `TransactionInterceptor`，先开启事务，再执行目标方法，最后根据异常类型决定提交还是回滚。同类调用失效的根因是没有经过代理对象。
