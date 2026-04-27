# 责任链模式

## 核心定义

责任链模式把多个处理器按顺序串成链，请求沿链路依次处理，每个处理器决定是否继续向后传递。

## 适用场景

- 参数校验链
- 权限校验链
- 风控规则链
- Servlet Filter、Spring Security Filter Chain
- 审批流、工单流转

## 示例

```java
public interface Handler {
    boolean handle(Request request);
}

public class LoginCheckHandler implements Handler {
    public boolean handle(Request request) {
        return request.isLogin();
    }
}

public class PermissionCheckHandler implements Handler {
    public boolean handle(Request request) {
        return request.hasPermission();
    }
}
```

执行链：

```java
public class HandlerChain {
    private final List<Handler> handlers;

    public HandlerChain(List<Handler> handlers) {
        this.handlers = handlers;
    }

    public boolean handle(Request request) {
        for (Handler handler : handlers) {
            if (!handler.handle(request)) {
                return false;
            }
        }
        return true;
    }
}
```

## 面试重点

- 责任链能把复杂校验拆成多个独立节点
- 每个节点只关心自己的职责
- 需要控制执行顺序和中断规则
- 链路过长会增加排查成本，要有日志和监控

## 项目落地

在接口请求处理里，可以把登录校验、权限校验、参数校验、频控校验拆成多个 Handler。对于 AI 场景，也可以把 prompt 安全检查、用户额度检查、模型路由检查、敏感词检查组织成责任链。

## 面试话术

责任链模式适合多步骤校验或处理。它的好处是每个处理器职责单一，新增规则只需要加一个 Handler 并配置顺序。需要注意的是，责任链要明确中断条件，并记录关键节点日志，否则线上排查会比较困难。

