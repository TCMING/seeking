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
