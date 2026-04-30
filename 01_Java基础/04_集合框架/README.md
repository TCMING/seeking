# 集合框架

## 项目应用

所有项目高频使用，热点缓存键计算、并发安全计数器等。

## 核心考点

- `HashMap`：JDK 1.8 数组 + 链表 + 红黑树（链表长度 > 8 且数组长度 ≥ 64 才树化），扩容机制（2 倍扩容、`tableSizeFor` 取最近的 2^n）、线程不安全（多线程扩容死链问题，1.8 已修复死链但仍可能数据丢失）
- `ConcurrentHashMap`：JDK 1.7 分段锁 → 1.8 CAS + `synchronized` 锁桶头节点
- `ArrayList` 扩容（1.5 倍）vs `LinkedList`（双向链表，随机访问慢但插入快）
- `TreeMap` 红黑树实现，按 key 排序，常用于范围查询
- 并发容器选型：`ConcurrentHashMap`、`CopyOnWriteArrayList`（读多写少）、`BlockingQueue`（生产者-消费者）

## LearningNotes 补充：集合框架源码阅读主线

Java 集合框架可以按五条线阅读：

- `Collection`：List、Set、Queue 的共同抽象。
- `Map`：key-value 映射结构，和 `Collection` 是并列体系。
- 迭代器：`Iterator`、`ListIterator`、早期的 `Enumeration`。
- 抽象骨架类：`AbstractCollection`、`AbstractList`、`AbstractSet`、`AbstractMap`。
- 工具类：`Arrays`、`Collections`。

源码阅读时要注意一个设计点：JDK 集合大量使用“抽象骨架类”。例如 `AbstractList` 帮子类实现通用逻辑，具体集合只覆盖关键方法。这是适配器思想在集合框架中的体现，能减少实现类重复代码。

## HashMap 源码级重点

HashMap 面试不要只说“数组 + 链表 + 红黑树”，还要能说清楚这些源码问题：

- 为什么容量必须是 2 的幂：`(n - 1) & hash` 等价于取模且效率更高，同时能让桶分布更均匀。
- 为什么默认负载因子是 `0.75`：在空间利用率和查询性能之间折中。
- `put` 做了什么：计算 hash、定位桶、遍历桶内节点、覆盖旧值或插入新节点、必要时扩容。
- `get` 做了什么：计算 hash、定位桶、比较 hash 和 key，命中后返回 value。
- 为什么扩容成本高：扩容会重新分配数组并迁移节点，生产环境大 Map 应预估容量。
- `containsKey` 和 `containsValue` 性能不同：前者按 hash 定位桶，后者通常需要全表扫描。
- 为什么线程不安全：并发写入、扩容、链表或树结构调整都可能造成数据错乱。

## JDK 7 与 JDK 8 差异

LearningNotes 的 HashMap 源码笔记偏 JDK 7 风格，核心结构是数组 + 单链表。现在面试通常问 JDK 8，需要补充：

- JDK 8 引入红黑树，链表过长时树化，降低极端冲突下的查询复杂度。
- 树化条件不是只看链表长度，还要求数组容量达到阈值，否则优先扩容。
- JDK 8 扩容迁移利用高位 hash 判断节点留在原索引还是移动到 `oldIndex + oldCap`。

## 推荐断点

- `HashMap.putVal`
- `HashMap.getNode`
- `HashMap.resize`
- `HashMap.treeifyBin`
- `ConcurrentHashMap.putVal`
- `ArrayList.grow`
- `LinkedList.linkLast`

## 专题扩展

- [HashMap 多线程死循环与 CPU 飙高排查](./02_HashMap多线程死循环排查/README.md)

## 源码级面试话术

HashMap 的核心是通过 hash 定位桶，再在桶内比较 key。容量保持 2 的幂，是为了用位运算代替取模。扩容时会重新分配数组并迁移节点，所以如果能预估数据量，最好初始化容量。JDK 8 在链表过长时引入红黑树，但树化还受到数组容量限制，并不是一冲突就树化。

## 参考来源

- [LearningNotes - Java 集合框架](https://github.com/francistao/LearningNotes/blob/master/Part2/JavaSE/Java%E9%9B%86%E5%90%88%E6%A1%86%E6%9E%B6.md)
- [LearningNotes - HashMap 源码剖析](https://github.com/francistao/LearningNotes/blob/master/Part2/JavaSE/HashMap%E6%BA%90%E7%A0%81%E5%89%96%E6%9E%90.md)
