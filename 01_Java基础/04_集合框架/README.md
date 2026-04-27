# 集合框架

## 项目应用

所有项目高频使用，热点缓存键计算、并发安全计数器等。

## 核心考点

- `HashMap`：JDK 1.8 数组 + 链表 + 红黑树（链表长度 > 8 且数组长度 ≥ 64 才树化），扩容机制（2 倍扩容、`tableSizeFor` 取最近的 2^n）、线程不安全（多线程扩容死链问题，1.8 已修复死链但仍可能数据丢失）
- `ConcurrentHashMap`：JDK 1.7 分段锁 → 1.8 CAS + `synchronized` 锁桶头节点
- `ArrayList` 扩容（1.5 倍）vs `LinkedList`（双向链表，随机访问慢但插入快）
- `TreeMap` 红黑树实现，按 key 排序，常用于范围查询
- 并发容器选型：`ConcurrentHashMap`、`CopyOnWriteArrayList`（读多写少）、`BlockingQueue`（生产者-消费者）
