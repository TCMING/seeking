# 观察者模式

## 核心定义

观察者模式定义对象之间的一对多依赖，当被观察对象状态变化时，自动通知所有观察者。

## 适用场景

- 订单状态变更后发送通知、积分、优惠券
- 用户注册后触发欢迎消息和初始化任务
- Spring 事件机制
- MQ 消息订阅
- 领域事件

## 示例

```java
public interface EventListener {
    void onEvent(UserRegisteredEvent event);
}

public class SendWelcomeMessageListener implements EventListener {
    public void onEvent(UserRegisteredEvent event) {
        System.out.println("send welcome message");
    }
}
```

## Spring 事件写法

```java
public record UserRegisteredEvent(Long userId) {
}

@Component
public class UserEventListener {
    @EventListener
    public void onUserRegistered(UserRegisteredEvent event) {
        System.out.println("user registered: " + event.userId());
    }
}
```

## 面试重点

- 观察者用于解耦主流程和副作用逻辑
- Spring `ApplicationEvent` 是典型实现
- MQ 也可以看作跨进程的观察者思想
- 同步事件会影响主流程耗时，异步事件要考虑最终一致性

## 优缺点

优点是发布方和订阅方解耦，扩展新的订阅逻辑方便。缺点是调用链不直观，异步场景下要处理失败重试、幂等和顺序问题。

## 面试话术

观察者模式适合主业务完成后触发多个附加动作。比如用户注册成功后，主流程只发布注册事件，欢迎消息、积分初始化、数据同步分别订阅事件处理。这样新增订阅方不需要修改注册主流程，但要注意异步事件的失败重试和幂等。

