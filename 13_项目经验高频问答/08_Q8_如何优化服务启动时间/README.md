# Q8: 如何优化服务启动时间？

> midjourney-proxy 启动从 40+ 秒降到 20 秒：
>
> 1. **精准 ComponentScan**：收敛 `basePackages`，排除无关 Bean；
> 2. **@ConditionalOnProperty** 关闭测试环境不需要的 Bean；
> 3. **延迟初始化**：非核心 Bean 用 `@Lazy`；
> 4. **Bean 数量审计**：通过 Spring Boot Actuator `beans` 端点排查无效 Bean。
