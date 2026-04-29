# IO 模型与 Netty

## 项目应用

`ibrain-base` 中 Dubbo 2.7.18 底层基于 Netty；`midjourney-proxy` 中 JDA 也是基于 Netty 维持 Discord 长连接。

## 核心考点

- 五种 IO 模型：BIO、NIO、IO 多路复用（select/poll/epoll）、信号驱动 IO、AIO
- Reactor 模式：单 Reactor 单线程 / 单 Reactor 多线程 / 主从 Reactor 多线程（Netty 默认模式）
- Netty 核心组件：`EventLoopGroup`、`Channel`、`ChannelPipeline`、`ChannelHandler`、`ByteBuf`
- TCP 粘包 / 拆包及解决方案：定长、分隔符、长度字段（`LengthFieldBasedFrameDecoder`）
- 零拷贝：`FileRegion`、`CompositeByteBuf`、`Unpooled.wrappedBuffer`
- Netty 内存管理：`PooledByteBufAllocator`、引用计数、内存泄漏检测

## LearningNotes 补充：IO 中的设计模式

JDK IO 里最常见的两个设计模式是适配器模式和装饰器模式。

## 装饰器模式

Java IO 的典型写法：

```java
InputStream inputStream =
        new BufferedInputStream(new FileInputStream("data.txt"));
```

`FileInputStream` 负责基础文件读取，`BufferedInputStream` 在外层增加缓冲能力。多个 IO 类可以层层包装，动态叠加能力，比如缓冲、字符转换、对象序列化。

面试重点：装饰器模式保持接口不变，增强对象能力；它比继承更适合组合多种能力。

## 适配器模式

IO 中也有接口转换场景，例如字节流和字符流之间的转换：

```java
Reader reader = new InputStreamReader(inputStream);
```

`InputStreamReader` 把字节输入流适配成字符读取接口，屏蔽编码转换细节。

## BIO / NIO 源码阅读重点

- BIO：一个连接通常对应一个线程，阻塞读写简单但高并发成本高。
- NIO：`Channel`、`Buffer`、`Selector` 三件套，适合大量连接和少量活跃请求。
- Netty：对 NIO 进行封装，核心是 Reactor 线程模型、Pipeline 责任链和 ByteBuf 内存管理。

## 推荐断点

- `FileInputStream.read`
- `BufferedInputStream.read`
- `InputStreamReader.read`
- `Selector.select`
- `SocketChannel.read`
- `NioEventLoop.run`
- `DefaultChannelPipeline.fireChannelRead`

## 源码级面试话术

Java IO 里 `BufferedInputStream` 包装 `FileInputStream` 是装饰器模式，目的是在不改变原接口的情况下增强缓冲能力。`InputStreamReader` 是适配器模式，它把字节流转换成字符流。Netty 则把 NIO 的 Selector、Channel、Buffer 封装成 Reactor 线程模型和 Pipeline 责任链，降低直接使用 NIO 的复杂度。

## 参考来源

- [LearningNotes - Java 并发基础知识](https://github.com/francistao/LearningNotes/blob/master/Part2/JavaConcurrent/Java%E5%B9%B6%E5%8F%91%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86.md)
