# Spring Data JPA

## 项目应用

`ibrain-prompt`、`ibrain-gpt-backend`、`midjourney-proxy` 的数据访问层。

## 核心考点

- JPA vs MyBatis：ORM 自动映射 vs SQL 灵活控制；JPA 适合 CRUD 主导的业务，MyBatis 适合复杂查询
- `@Entity` 映射与关联关系：`@OneToMany`、`@ManyToOne`、`@JoinColumn`
- `@Query` 自定义查询（JPQL / 原生 SQL）
- **N+1 查询问题**与解决：`@EntityGraph`、`FetchType.LAZY` + `JOIN FETCH`
- `@Transactional` 在 JPA 中尤为重要：会话与事务绑定，懒加载需在事务内
- 审计字段：`@CreatedDate`、`@LastModifiedDate`、`@EnableJpaAuditing`

## 源码级主线

Spring Data JPA 的核心是：接口没有实现类，但 Spring 会在启动时为 Repository 接口创建代理对象。

关键类：

- `RepositoryFactoryBeanSupport`
- `JpaRepositoryFactoryBean`
- `JpaRepositoryFactory`
- `SimpleJpaRepository`
- `RepositoryFactorySupport`
- `QueryLookupStrategy`
- `PartTree`
- `EntityManager`

## Repository 代理创建流程

```text
@EnableJpaRepositories
-> JpaRepositoriesRegistrar
-> RepositoryBeanDefinitionRegistrarSupport
-> 注册 RepositoryFactoryBeanSupport
-> JpaRepositoryFactoryBean.afterPropertiesSet
-> JpaRepositoryFactory 创建 Repository 代理
```

最终注入到业务代码里的 Repository 通常是一个代理对象。简单 CRUD 方法由 `SimpleJpaRepository` 提供实现。

## 方法名查询源码理解

例如：

```java
User findByNameAndStatus(String name, Integer status);
```

源码会把方法名解析成查询语义：

```text
findByNameAndStatus
-> PartTree
-> Part
-> Query 创建
-> EntityManager 执行
```

这就是为什么 Spring Data JPA 可以根据方法名自动生成查询。

## @Query 执行流程

`@Query` 会绕过方法名解析，直接使用声明的 JPQL 或 SQL。

源码侧会通过 `QueryLookupStrategy` 判断：

- 是否存在 `@Query`
- 是否能从方法名推导查询
- 是否使用命名查询

## EntityManager 与事务

JPA 的一级缓存、脏检查、懒加载都依赖持久化上下文。Spring 会把 `EntityManager` 和事务绑定到当前线程。

高频现象：

- 没事务时懒加载容易触发 `LazyInitializationException`。
- 同一事务内重复查询同一个实体可能命中一级缓存。
- 修改实体字段后无需显式 update，事务提交时会通过脏检查同步到数据库。

## N+1 问题源码角度

N+1 的根因是关联对象懒加载时，每访问一个关联集合或对象都会额外发 SQL。

解决方式：

- `JOIN FETCH`
- `@EntityGraph`
- 批量抓取配置
- DTO 投影，避免加载完整实体图

## 推荐断点

- `JpaRepositoryFactoryBean.afterPropertiesSet`
- `RepositoryFactorySupport.getRepository`
- `SimpleJpaRepository.findById`
- `QueryLookupStrategy.resolveQuery`
- `PartTreeJpaQuery`
- `AbstractEntityManagerFactoryBean`

## 源码级面试话术

Spring Data JPA 会在启动阶段扫描 Repository 接口，并通过 `JpaRepositoryFactoryBean` 创建代理对象。普通 CRUD 由 `SimpleJpaRepository` 实现，方法名查询会通过 `PartTree` 解析成查询条件。JPA 的懒加载、一级缓存和脏检查依赖事务绑定的 `EntityManager`，所以事务边界对 JPA 很关键。
