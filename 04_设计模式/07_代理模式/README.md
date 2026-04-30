# 代理模式

## 核心定义

代理模式为目标对象提供一个代理对象，通过代理对象控制对目标对象的访问，并在调用前后增强逻辑。

## 适用场景

- Spring AOP
- 事务管理
- 权限校验
- 日志埋点
- RPC 远程调用代理
- 缓存代理

## 静态代理示例

```java
public interface UserService {
    void createUser();
}

public class UserServiceProxy implements UserService {
    private final UserService target;

    public UserServiceProxy(UserService target) {
        this.target = target;
    }

    public void createUser() {
        System.out.println("before");
        target.createUser();
        System.out.println("after");
    }
}
```

## 动态代理重点

- JDK 动态代理：基于接口，核心是 `InvocationHandler`
- CGLIB 动态代理：基于继承生成子类，不能代理 `final` 类和 `final` 方法
- Spring AOP 默认根据目标类是否有接口选择代理方式

## 面试重点

- `@Transactional` 依赖代理，所以同类方法内部调用会导致事务失效
- AOP 切面、权限、日志都是代理模式的典型应用
- RPC 客户端调用远程服务时，本地接口代理会封装网络通信细节

## 优缺点

优点是在不改目标类的情况下增强功能，符合开闭原则。缺点是调用链变长，代理失效场景需要特别理解。

## 面试话术

代理模式的核心是控制和增强目标对象访问。Spring AOP 就是典型应用，事务、日志、权限都可以通过代理在方法前后织入逻辑。使用时要注意代理失效，比如同类内部方法调用绕过代理，`private` 方法和 `final` 方法也无法被正常增强。

