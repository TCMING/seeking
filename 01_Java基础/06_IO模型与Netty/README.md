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
