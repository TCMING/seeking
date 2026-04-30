# 单例模式

## 核心定义

单例模式保证一个类在 JVM 进程内只有一个实例，并提供一个全局访问入口。

## 适用场景

- 全局配置管理
- 线程池、连接池、缓存管理器
- ID 生成器、限流器
- Spring 默认单例 Bean

## 常见实现

### 饿汉式

```java
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();

    private Singleton() {
    }

    public static Singleton getInstance() {
        return INSTANCE;
    }
}
```

优点是线程安全，实现简单；缺点是类加载时就创建对象，可能造成资源浪费。

### 双重检查锁

```java
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {
    }

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

`volatile` 的作用是禁止指令重排，避免其他线程拿到未初始化完成的对象。

## 面试重点

- 单例是否线程安全
- 双重检查锁为什么需要 `volatile`
- 反射和反序列化可能破坏单例
- Spring 单例 Bean 是容器级单例，不等同于设计模式里的 JVM 全局单例

## 项目落地

在 Spring 项目里通常不手写单例，而是把无状态服务交给 Spring 容器管理。对于本地缓存、配置中心客户端、线程池等全局资源，也常用单例思路统一管理生命周期。

## 面试话术

单例模式适合管理全局唯一资源。实际项目里我一般优先使用 Spring 的单例 Bean，由容器负责创建和生命周期管理。如果需要手写单例，会注意线程安全、`volatile` 防止指令重排，以及反射和序列化破坏单例的问题。