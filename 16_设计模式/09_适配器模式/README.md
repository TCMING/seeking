# 适配器模式

## 核心定义

适配器模式把一个类的接口转换成客户端期望的另一个接口，让原本接口不兼容的类可以一起工作。

## 适用场景

- 对接第三方接口
- 老系统接口改造
- 多模型供应商统一接口
- 不同支付渠道统一参数
- DTO、VO、Entity 转换

## 示例

```java
public interface ModelClient {
    String chat(String prompt);
}

public class ThirdPartyModelApi {
    public String invoke(String text) {
        return "response: " + text;
    }
}

public class ThirdPartyModelAdapter implements ModelClient {
    private final ThirdPartyModelApi api;

    public ThirdPartyModelAdapter(ThirdPartyModelApi api) {
        this.api = api;
    }

    public String chat(String prompt) {
        return api.invoke(prompt);
    }
}
```

## 面试重点

- 适配器重点是接口转换，不是增强功能
- 常用于屏蔽第三方 API 差异
- 适配层可以做参数转换、异常转换、返回值转换
- 适配器过多时要警惕领域模型混乱

## 和装饰器模式的区别

适配器改变接口形态，让不兼容接口能使用。装饰器保持接口不变，在原能力上叠加新能力。

## 项目落地

在多模型接入中，不同模型厂商的请求参数、认证方式、响应结构都不一样。可以为每个厂商写一个 Adapter，对外统一成 `ModelClient`，业务层只依赖统一接口。

## 面试话术

适配器模式适合对接外部系统。比如第三方模型接口的参数和返回结构各不相同，我会在适配层完成请求转换、响应转换和异常转换，对业务层暴露统一接口，这样业务代码不会被供应商 API 细节污染。

