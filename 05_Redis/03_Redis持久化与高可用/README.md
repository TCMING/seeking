# Redis 持久化与高可用

## 核心考点

- RDB 快照（fork 子进程，数据紧凑）vs AOF 日志（追加写，恢复慢但更安全）
- AOF 重写：`bgrewriteaof`，避免无限增长
- 主从复制：全量同步（RDB）+ 增量同步（缓冲区）
- 哨兵模式：自动故障转移、主观下线 vs 客观下线
- Cluster 分片：16384 槽位、Gossip 协议、不支持跨槽事务
- 内存淘汰策略：`noeviction`、`allkeys-lru`、`volatile-lru`、`allkeys-lfu` 等
