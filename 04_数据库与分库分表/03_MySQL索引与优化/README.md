# MySQL 索引与优化 ⭐

## 项目应用

`ibrain-prompt` 工作流执行表 / 调用记录表加索引；`ibrain-gpt-backend` 高频对话查询的索引设计。

## 核心考点

- B+ 树索引结构：节点存键值 + 指针、叶子节点链表（范围查询友好）
- 聚簇索引（InnoDB 主键）vs 非聚簇索引；覆盖索引、回表
- 最左前缀匹配原则；联合索引的字段顺序选择
- 索引失效场景：函数操作、隐式类型转换、`OR` 跨非索引列、`LIKE '%xxx'`、`!=` / `NOT IN`
- 慢查询排查：`EXPLAIN` 关注 `type`（理想 `ref`/`range`，避免 `ALL`）、`key`、`rows`、`Extra`（`Using filesort`、`Using temporary` 是危险信号）
- 事务隔离级别与 MVCC：`READ VIEW`、`undo log`
- 锁：表锁、行锁、间隙锁、Next-Key Lock（解决幻读）
