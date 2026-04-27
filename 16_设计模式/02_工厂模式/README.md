# 工厂模式

## 核心定义

工厂模式把对象创建逻辑从业务代码中抽离出来，由工厂根据条件返回不同实现。

## 适用场景

- 不同支付渠道：支付宝、微信、银行卡
- 不同消息发送器：短信、邮件、站内信
- 不同模型供应商：OpenAI、通义、文心、Claude
- 不同文件解析器：PDF、Word、Excel、Markdown

## 简单示例

```java
public interface Sender {
    void send(String message);
}

public class SmsSender implements Sender {
    public void send(String message) {
        System.out.println("sms: " + message);
    }
}

public class EmailSender implements Sender {
    public void send(String message) {
        System.out.println("email: " + message);
    }
}

public class SenderFactory {
    public static Sender create(String type) {
        if ("sms".equals(type)) {
            return new SmsSender();
        }
        if ("email".equals(type)) {
            return new EmailSender();
        }
        throw new IllegalArgumentException("unsupported type: " + type);
    }
}
```

## Spring 项目写法

在 Spring 中更推荐使用 `Map<String, Bean>` 自动收集实现类：

```java
@Service
public class SenderFactory {
    private final Map<String, Sender> senderMap;

    public SenderFactory(Map<String, Sender> senderMap) {
        this.senderMap = senderMap;
    }

    public Sender get(String type) {
        Sender sender = senderMap.get(type);
        if (sender == null) {
            throw new IllegalArgumentException("unsupported type: " + type);
        }
        return sender;
    }
}
```

## 面试重点

- 简单工厂不是 GoF 设计模式，但面试和项目里非常常用
- 工厂方法把创建逻辑下放到子类
- 抽象工厂用于创建一组相关对象
- 工厂可以减少 `new` 散落在业务代码里的问题

## 优缺点

优点是创建逻辑集中、调用方依赖接口、扩展实现更清晰。缺点是实现类和工厂类数量可能增加，简单场景过度使用会让代码绕。

## 面试话术

工厂模式主要解决对象创建和业务使用耦合的问题。比如多模型接入场景下，业务方只关心 `ModelClient` 接口，具体用 OpenAI 还是其他模型由工厂根据模型类型返回，这样新增供应商时主要新增实现类和注册配置，不需要到处改业务分支。

