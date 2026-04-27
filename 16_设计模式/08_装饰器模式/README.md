# 装饰器模式

## 核心定义

装饰器模式在不改变原对象结构的情况下，动态给对象增加额外能力。

## 适用场景

- Java IO 流
- 请求对象包装
- 响应结果增强
- 缓存、日志、限流能力叠加
- 多层数据处理管道

## 示例

```java
public interface DataLoader {
    String load();
}

public class FileDataLoader implements DataLoader {
    public String load() {
        return "file data";
    }
}

public class CacheDataLoaderDecorator implements DataLoader {
    private final DataLoader delegate;

    public CacheDataLoaderDecorator(DataLoader delegate) {
        this.delegate = delegate;
    }

    public String load() {
        return "cache(" + delegate.load() + ")";
    }
}
```

## 典型框架应用

Java IO 是最经典的装饰器模式：

```java
BufferedInputStream inputStream =
        new BufferedInputStream(new FileInputStream("data.txt"));
```

`FileInputStream` 提供基础文件读取能力，`BufferedInputStream` 在外层增加缓冲能力。

## 和代理模式的区别

代理模式更强调控制访问，例如权限、事务、远程代理。装饰器模式更强调能力叠加，例如缓冲、压缩、加密、日志包装。

## 优缺点

优点是可以组合多个增强能力，比继承更灵活。缺点是层层包装后对象结构变复杂，排查调用链需要更清晰的命名和日志。

## 面试话术

装饰器模式适合给对象动态叠加能力。比如一个数据加载器先具备文件读取能力，再包装缓存、日志、压缩等能力，每层装饰器只负责一个增强点。相比继承，它避免了能力组合爆炸的问题。

