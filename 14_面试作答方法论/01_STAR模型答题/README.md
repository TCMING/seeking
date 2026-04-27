# STAR 模型答题

技术问题尤其是项目经验类，按 **Situation（背景）→ Task（任务）→ Action（动作）→ Result（结果）** 结构作答：

> **示例（分布式锁）**：
>
> - **Situation**：midjourney-proxy 是 Discord MJ 的代理服务，业务方会重复提交绘图任务；
> - **Task**：保证任务幂等，避免重复消耗成本和混乱回调；
> - **Action**：用 Redisson 分布式锁锁住「任务唯一 ID」，配合状态机校验，结合 Watchdog 续期；
> - **Result**：上线后重复任务问题归零，幂等性保障稳定。
