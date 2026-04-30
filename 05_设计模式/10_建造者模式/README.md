# 建造者模式

## 核心定义

建造者模式把复杂对象的构建过程拆分出来，通过链式方法逐步设置参数，最后生成对象。

## 适用场景

- 构造参数很多
- 参数可选项多
- 对象创建需要校验
- 请求对象、配置对象、DTO 构建
- Lombok `@Builder`

## 示例

```java
public class ChatRequest {
    private final String model;
    private final String prompt;
    private final double temperature;

    private ChatRequest(Builder builder) {
        this.model = builder.model;
        this.prompt = builder.prompt;
        this.temperature = builder.temperature;
    }

    public static class Builder {
        private String model;
        private String prompt;
        private double temperature = 0.7;

        public Builder model(String model) {
            this.model = model;
            return this;
        }

        public Builder prompt(String prompt) {
            this.prompt = prompt;
            return this;
        }

        public Builder temperature(double temperature) {
            this.temperature = temperature;
            return this;
        }

        public ChatRequest build() {
            return new ChatRequest(this);
        }
    }
}
```

使用：

```java
ChatRequest request = new ChatRequest.Builder()
        .model("gpt")
        .prompt("hello")
        .temperature(0.8)
        .build();
```

## 面试重点

- 解决构造参数过多、可读性差的问题
- 可以在 `build()` 里统一做参数校验
- 和工厂模式不同：工厂关注创建哪一种对象，建造者关注如何一步步构建复杂对象
- Lombok `@Builder` 是项目中常见写法

## 优缺点

优点是创建过程清晰，适合可选参数多的复杂对象。缺点是类代码量增加，简单对象没有必要使用。

## 面试话术

建造者模式适合构造复杂请求对象。比如模型调用请求包含模型名、prompt、温度、最大 token、工具列表等大量可选参数，用构造函数会很难读，用 Builder 可以链式设置参数，并在 `build()` 阶段统一校验必填字段。

