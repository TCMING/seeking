# 模板方法模式

## 核心定义

模板方法模式在父类中定义算法骨架，把可变步骤延迟到子类实现。

## 适用场景

- 固定业务流程中某些步骤可变
- 导入任务：读取、校验、转换、入库
- 支付流程：参数校验、扣款、回调、通知
- 大模型调用流程：构造请求、调用模型、解析响应、记录日志

## 示例

```java
public abstract class AbstractImportService {
    public final void importData() {
        readFile();
        validate();
        convert();
        save();
    }

    protected abstract void readFile();

    protected void validate() {
        System.out.println("default validate");
    }

    protected abstract void convert();

    protected abstract void save();
}
```

## 面试重点

- 父类控制流程，子类只实现变化点
- 模板方法一般用 `final` 防止子类破坏流程
- 钩子方法可以让子类选择性扩展
- Spring 中很多生命周期流程有模板方法思想

## 优缺点

优点是复用主流程、统一控制顺序、减少重复代码。缺点是依赖继承，扩展层级过深时可读性会下降。

## 和策略模式的区别

模板方法强调固定流程，由继承扩展步骤。策略模式强调替换算法，由组合切换行为。简单说，模板方法解决“流程一样，部分步骤不同”，策略模式解决“同一动作，有多种算法”。

## 面试话术

模板方法适合固定主流程但步骤存在差异的场景。比如文件导入，不同文件格式的读取和转换不同，但校验、落库、结果统计流程一致，可以放到抽象父类里统一编排，子类只实现格式相关步骤。

