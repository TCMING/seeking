# XXL-Job

## 项目应用

`ibrain-base`、`ibrain-prompt`、`ibrain-gpt-backend`、`midjourney-proxy` 均使用 XXL-Job。

## 核心考点

- 架构：调度中心（Admin）+ 执行器（Executor）解耦
- 调度策略：CRON、固定速率、固定延迟
- 路由策略：`FIRST`、`LAST`、`ROUND`、`RANDOM`、`LEAST_FREQUENTLY_USED`、`LEAST_RECENTLY_USED`、`FAILOVER`、`SHARDING_BROADCAST`
- 阻塞处理策略：`SERIAL_EXECUTION`（单机串行）、`DISCARD_LATER`、`COVER_EARLY`
- 任务超时与失败重试
- 分片广播任务处理大数据量（按分片 ID 取模分配）
