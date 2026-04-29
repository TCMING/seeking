# JVM ⭐

## 项目应用

所有线上服务均涉及 JVM 调优、OOM 排查、GC 优化。

## 核心考点

### 内存模型

堆（新生代 Eden + S0/S1、老年代）、栈、方法区（元空间）、程序计数器、本地方法栈

### 垃圾回收算法

标记-清除、标记-整理、复制算法（新生代）、分代收集

### 垃圾收集器

- CMS：老年代并发收集，三色标记 + 增量更新，缺点是浮动垃圾、内存碎片
- G1：分 Region、并发标记 + 复制算法，可控停顿（`-XX:MaxGCPauseMillis`）
- ZGC / Shenandoah（JDK 11+）：低延迟、染色指针、亚毫秒级停顿

### JVM 调优常用参数

- `-Xms` / `-Xmx`：堆初始 / 最大值，建议设置一致避免动态扩容
- `-Xmn`：新生代大小
- `-XX:MetaspaceSize` / `-XX:MaxMetaspaceSize`：元空间
- `-XX:+HeapDumpOnOutOfMemoryError`：OOM 时自动 dump

### OOM 排查实战四步法

1. 通过监控（GC 频率、堆使用率、线程数）定位 OOM 类型
2. `jmap -dump:format=b,file=heap.hprof <pid>` 或线上预设的 `HeapDumpOnOutOfMemoryError`
3. MAT / VisualVM / `jhat` 分析支配树（Dominator Tree），找到内存占用 Top 对象
4. 结合代码定位泄漏点（常见：`ThreadLocal` 未清理、静态集合无限增长、连接未关闭、缓存无淘汰策略）

### 类加载机制

双亲委派模型（启动类加载器 → 扩展类加载器 → 应用类加载器）、打破双亲委派的场景（SPI、Tomcat WebappClassLoader、OSGi、热部署）

## LearningNotes 补充：类加载源码级主线

JVM 把 Class 文件加载到内存，并转换成 JVM 可直接使用的 Java 类型，这个过程叫类加载。

类生命周期：

```text
加载 Loading
-> 验证 Verification
-> 准备 Preparation
-> 解析 Resolution
-> 初始化 Initialization
-> 使用 Using
-> 卸载 Unloading
```

其中验证、准备、解析统称为连接 Linking。

## 加载阶段

加载阶段做三件事：

- 通过类全限定名获取二进制字节流。
- 将字节流的静态存储结构转换成方法区运行时数据结构。
- 在堆中生成 `java.lang.Class` 对象，作为访问入口。

面试要点：类加载器参与的是“获取字节流”这个动作，所以可以从文件、网络、加密包、动态生成字节码等来源加载类。

## 验证阶段

验证阶段保证 Class 字节流符合 JVM 要求，不危害虚拟机安全。通常包括：

- 文件格式验证
- 元数据验证
- 字节码验证
- 符号引用验证

## 准备阶段

准备阶段为类变量分配内存并设置零值。

注意：

```java
public static int count = 10;
```

准备阶段 `count` 是 `0`，初始化阶段才变成 `10`。

## 解析阶段

解析阶段把常量池中的符号引用转换为直接引用，主要针对：

- 类或接口
- 字段
- 类方法
- 接口方法

## 初始化阶段

初始化阶段执行类构造器 `<clinit>()`，也就是静态变量赋值和静态代码块的合并结果。

常见触发初始化的场景：

- `new` 对象
- 访问或设置静态字段
- 调用静态方法
- 反射调用
- 初始化子类前先初始化父类
- JVM 启动类

## 双亲委派模型

类加载器层级：

- Bootstrap ClassLoader
- Extension ClassLoader，JDK 9 后模块化机制下概念变化
- Application ClassLoader
- 自定义 ClassLoader

双亲委派流程：

```text
先委托父加载器加载
-> 父加载器无法加载
-> 子加载器再尝试加载
```

核心收益：

- 避免核心类被重复加载。
- 保护 JDK 核心类库，例如自定义 `java.lang.String` 不应替换 JDK 的 `String`。

## 推荐断点

- `ClassLoader.loadClass`
- `ClassLoader.findClass`
- `URLClassLoader.findClass`
- `Class.forName`
- 自定义 ClassLoader 的 `findClass`

## 源码级面试话术

类加载包括加载、验证、准备、解析、初始化几个阶段。加载阶段只是把字节流变成 Class 元数据和 `Class` 对象；准备阶段给静态变量赋零值；初始化阶段才执行静态赋值和静态代码块。双亲委派的核心是先让父加载器尝试加载，避免核心类被篡改和重复加载。

## 面试话术

> 我们 ibrain-prompt 服务上线后曾经出现过 Full GC 频繁，CPU 飙高的问题。先通过监控发现老年代使用率持续高位，然后 dump 堆，用 MAT 分析支配树，定位到一个本地缓存没有设置过期策略，长时间运行后内存堆积。修复后用 G1 收集器替代 CMS，并设置 `-XX:MaxGCPauseMillis=200`，P99 GC 停顿稳定在 200ms 以内。

## 参考来源

- [LearningNotes - JVM 类加载机制](https://github.com/francistao/LearningNotes/blob/master/Part2/JVM/JVM%E7%B1%BB%E5%8A%A0%E8%BD%BD%E6%9C%BA%E5%88%B6.md)
