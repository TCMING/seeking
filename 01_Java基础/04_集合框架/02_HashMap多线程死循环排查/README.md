# HashMap 多线程死循环与 CPU 飙高排查

这个问题在面试里通常会被问成两层：

1. `HashMap` 为什么在多线程下不安全。
2. 如果线上出现 CPU 飙高，怎么定位是不是 `HashMap` 相关问题。

## 现象

常见表现不是直接报错，而是：

- CPU 持续升高
- 某个线程长期占用 CPU
- `jstack` 里同一批线程反复停在集合相关方法
- 接口响应变慢，甚至超时

## 快速结论

- JDK 7 经典问题是并发 `resize` 后链表可能成环，`get()` 进入死循环。
- JDK 8 已经修正了这一类经典头插导致的成环问题，但 `HashMap` 仍然不是线程安全的。
- 只要存在并发写入，仍然可能出现数据错乱、查询异常、频繁扩容和 CPU 飙高。

## 怎么定位

### 1. 先找高 CPU 线程

```bash
top -H -p <pid>
```

或者用任务管理器、`jcmd`、`jstack` 结合线程 ID 观察。

### 2. 连续抓 3 次线程栈

```bash
jstack -l <pid> > dump1.txt
jstack -l <pid> > dump2.txt
jstack -l <pid> > dump3.txt
```

间隔 5 到 10 秒。如果同一个线程栈一直没变，说明它可能卡在同一个热循环里。

### 3. 观察是否反复落在 HashMap 相关方法

重点看这些栈帧：

- `java.util.HashMap.putVal`
- `java.util.HashMap.getNode`
- `java.util.HashMap.resize`
- `java.util.HashMap.treeifyBin`
- `java.util.HashMap$HashIterator.nextNode`

### 4. 用采样工具确认热点

可选工具：

- `async-profiler`
- JFR
- Arthas `profiler`

如果采样显示绝大部分 CPU 消耗在 `HashMap` 相关路径，基本就能锁定方向。

## 常见根因

### 并发写 HashMap

这是第一嫌疑。多个线程同时 `put`、`remove`、`resize`，会导致：

- 桶内节点顺序混乱
- 节点丢失
- 结构损坏
- 扩容时重复搬迁

### key 的 hashCode / equals 不稳定

如果 key 是可变对象，放入 Map 后字段被修改，后续查找会异常，极端情况下会出现大量无效遍历。

### 频繁扩容和高冲突

Map 初始容量太小，或者 key 的 hash 分布太差，会导致频繁扩容和桶内冲突，CPU 明显上升。

### 实际问题不在 HashMap

有些业务线程栈里会出现 `HashMap`，但真正的循环在业务重试、自旋锁、任务队列轮询里。必须结合多次栈和采样看。

## JDK 7 和 JDK 8 的区别

### JDK 7

并发 `resize` 时，链表迁移使用头插法，极端情况下会形成环，后续 `get()` 可能一直遍历不出去。

### JDK 8

扩容迁移不再是 JDK 7 那种经典头插成环模型，已经缓解了这个历史问题，但 `HashMap` 仍然不是线程安全类。

换句话说：

- 经典死循环 bug 基本被修掉了
- 并发误用问题没有被修掉

## 面试回答模板

你可以这样说：

> 我先通过 `top -H` 找到高 CPU 线程，再连续抓 `jstack`，看同一个线程是否一直停在 `HashMap.putVal`、`resize` 或 `getNode`。如果是，就重点怀疑并发写 `HashMap`、key 设计不稳定或频繁扩容。JDK 8 已经修正了 JDK 7 的经典成环问题，但 `HashMap` 依然不是线程安全的，所以多线程写入仍可能把结构打坏，最终表现为 CPU 飙高。

## 处理方式

- 并发场景改用 `ConcurrentHashMap`
- 复合操作外层加锁
- 预估容量，减少扩容
- 使用不可变 key
- 如果是高冲突 key，重新设计 hash 或分桶方式

## 推荐断点

- `HashMap.putVal`
- `HashMap.getNode`
- `HashMap.resize`
- `HashMap.treeifyBin`
- `ConcurrentHashMap.putVal`

