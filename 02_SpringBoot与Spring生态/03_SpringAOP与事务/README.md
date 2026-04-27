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
