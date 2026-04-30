# 策略模式

## 核心定义

策略模式把一组可互换的算法或业务规则封装成独立策略，运行时根据条件选择具体策略。

## 适用场景

- 支付渠道选择
- 优惠券计算
- 风控规则执行
- 多模型路由
- 不同业务类型的审核逻辑

## 示例

```java
public interface DiscountStrategy {
    int calculate(int originPrice);
}

public class VipDiscountStrategy implements DiscountStrategy {
    public int calculate(int originPrice) {
        return (int) (originPrice * 0.8);
    }
}

public class NewUserDiscountStrategy implements DiscountStrategy {
    public int calculate(int originPrice) {
        return originPrice - 100;
    }
}
```

配合上下文使用：

```java
public class DiscountContext {
    private final DiscountStrategy strategy;

    public DiscountContext(DiscountStrategy strategy) {
        this.strategy = strategy;
    }

    public int calculate(int originPrice) {
        return strategy.calculate(originPrice);
    }
}
```

## Spring 项目写法

```java
public interface PayStrategy {
    String type();

    void pay();
}

@Service
public class PayStrategyFactory {
    private final Map<String, PayStrategy> strategyMap;

    public PayStrategyFactory(List<PayStrategy> strategies) {
        this.strategyMap = strategies.stream()
                .collect(Collectors.toMap(PayStrategy::type, Function.identity()));
    }

    public PayStrategy get(String type) {
        return Optional.ofNullable(strategyMap.get(type))
                .orElseThrow(() -> new IllegalArgumentException("unsupported pay type"));
    }
}
```

## 面试重点

- 策略模式常用于消除大量 `if else`
- 和工厂模式经常一起使用：工厂负责选择策略，策略负责执行逻辑
- 策略适合横向扩展，不适合策略之间强依赖的流程编排

## 优缺点

优点是每种算法独立、扩展方便、单元测试清晰。缺点是策略数量多时需要做好命名、注册和兜底处理。

## 面试话术

策略模式适合处理同一类业务下多种可替换实现。比如模型路由场景中，不同模型供应商的调用、参数转换、异常处理都不一样，我会抽象统一接口，每个供应商实现一个策略，再通过工厂或配置选择具体策略，避免主流程里堆大量分支。

