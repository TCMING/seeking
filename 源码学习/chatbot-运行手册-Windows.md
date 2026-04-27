# Spring AI Alibaba Chatbot 运行手册（Windows）

> 目标：在 Windows 11 + PowerShell 环境下成功跑通 `spring-ai-alibaba/examples/chatbot`，完成第一阶段"自顶向下读源码"的入口。
>
> 项目路径：`D:\project\study\spring-ai-alibaba\examples\chatbot`

---

## 一、版本与依赖要求（硬性）

| 项 | 要求 | 备注 |
|---|---|---|
| JDK | **17+**（项目用了 record/`var`/Spring Boot 3.5.x） | JDK 8 直接编译失败 |
| Maven | 3.6+ | 仓库自带 `mvnw.cmd`（3.9.6），优先用它 |
| 模型 API Key | `AI_DASHSCOPE_API_KEY` | [阿里云百炼](https://bailian.console.aliyun.com/?apiKey=1&tab=api#/api) 申请 |
| 可选：Python 工具 | GraalVM Polyglot 24.2.1（`pom.xml` 里 optional） | 第一次跑可不管 |

---

## 二、第一次环境准备

### 2.1 安装 JDK 17

任选发行版（推荐 Temurin）：

- Eclipse Temurin（Adoptium）：https://adoptium.net/temurin/releases/?version=17
- Microsoft OpenJDK 17：https://learn.microsoft.com/java/openjdk/download
- Azul Zulu 17：https://www.azul.com/downloads/?version=java-17-lts&package=jdk

安装时建议：

- 选择 **Windows x64 MSI**。
- 勾选 "Set JAVA_HOME variable"。
- 安装路径用无空格的简短目录，例如 `D:\program_flies\jdk-17`。

### 2.2 申请 DashScope API Key

1. 打开 [阿里云百炼控制台](https://bailian.console.aliyun.com/?apiKey=1&tab=api#/api)。
2. 创建 API Key，复制类似 `sk-xxxxxxxxxxxx` 的字符串备用。

---

## 三、启动步骤（PowerShell）

### 3.1 切换 JDK 17（仅当前会话）

如果不想永久改系统 `JAVA_HOME`，每次开新窗口先执行：

```powershell
$env:JAVA_HOME="D:\program_flies\jdk-17"          # ← 改成你的实际路径
$env:Path="$env:JAVA_HOME\bin;$env:Path"
java -version                                      # 应输出 17.x
```

### 3.2 设置 API Key（仅当前会话）

```powershell
$env:AI_DASHSCOPE_API_KEY="你的sk-xxxxxxxxxxxx"
```

如希望永久生效：

```powershell
[Environment]::SetEnvironmentVariable("AI_DASHSCOPE_API_KEY","sk-xxx","User")
```

### 3.3 启动 Chatbot

```powershell
cd D:\project\study\spring-ai-alibaba\examples\chatbot
..\..\mvnw.cmd spring-boot:run
```

启动成功标志：

```
🎉========================================🎉
✅ Application is ready!
🚀 Chat with you agent: http://localhost:8080/chatui/index.html
🎉========================================🎉
```

浏览器访问 `http://localhost:8080/chatui/index.html` 开聊。

---

## 四、IDEA 启动方式（可选，更适合调试）

1. **File → Project Structure → Project SDK** 选 JDK 17。
2. **File → Settings → Build Tools → Maven**
   - Maven home directory：使用 `Bundled (Maven 3)`（IDEA 自带 ≥ 3.9）。
   - Runner → JRE：选择项目 SDK（JDK 17）。
3. 右上角运行配置 → 选 `ChatbotApplication`。
4. **Edit Configurations → Environment variables** 添加：
   - `AI_DASHSCOPE_API_KEY=sk-xxx`
5. 点 ▶ 启动。

---

## 五、常见报错速查

| 报错关键字 | 原因 | 解决 |
|---|---|---|
| `invalid target release: 17` | Maven 在用 JDK 8 | 检查 `java -version` 是否 17；用 `mvnw.cmd` 而不是系统 `mvn` |
| `release version 17 not supported` | 同上 | 同上 |
| `DashScope API key is required` / 401 / 403 | 未设置或 Key 失效 | 重新设置 `AI_DASHSCOPE_API_KEY` |
| `Connection refused 8080` 或端口占用 | 8080 被占 | 改 `application.yml`（项目目前没 yml 就在启动加 `--server.port=8081`）；或 `netstat -ano \| findstr 8080` 杀掉 |
| 卡在 `Downloading from sonatype-snapshots` | 网络慢 | 给 Maven 配阿里云镜像（见下） |
| `polyglot ... python-community` 找不到 | Maven 仓库未刷新 | `..\..\mvnw.cmd -U clean package -DskipTests`；或保留默认（这两个依赖是 optional，不影响主流程） |
| 控制台中文乱码 | PowerShell GBK | 启动加 `-Dfile.encoding=UTF-8`；或 `chcp 65001` |
| 浏览器打开 404 | URL 多了 / 少了 contextPath | 严格用日志里打印的 URL |

### Maven 阿里云镜像（拉包慢时配）

编辑 `~/.m2/settings.xml`（无则新建）：

```xml
<settings>
  <mirrors>
    <mirror>
      <id>aliyunmaven</id>
      <mirrorOf>*,!spring-milestones,!sonatype-snapshots</mirrorOf>
      <name>aliyun maven</name>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
  </mirrors>
</settings>
```

> 注意 `mirrorOf` 排除了 `spring-milestones` 和 `sonatype-snapshots`，因为 chatbot 的 `pom.xml` 显式声明了这两个仓库（见 `examples/chatbot/pom.xml`）。

---

## 六、跑通后的验证清单

跑通对话只是起点，验证以下点能真正打通框架：

- [ ] 让 Chatbot 执行 shell 命令（如"列出当前目录"）：触发 `ShellTool` → 进 `ShellToolAgentHook`。
- [ ] 让 Chatbot 计算（如"用 Python 算 sin(1)+cos(1)"）：触发 `PythonTool`。
- [ ] 让 Chatbot 读文件：触发 `ReadFileTool`。
- [ ] 在控制台看 `AgentStaticLoader` 输出的 PlantUML 图（启动时打印）：能直观看到 Agent 编译后的状态图。
- [ ] 打 IDEA 断点：在 `ReactAgent` 里下断点，发一条消息，跟一遍调用栈。

完成上面 5 项就可以进入"阶段 2：吃透 Agent Framework"。

---

## 七、关键源码定位

| 角色 | 文件 |
|---|---|
| Spring Boot 启动类 | `examples/chatbot/src/main/java/.../ChatbotApplication.java` |
| Agent 装配 ★ | `examples/chatbot/src/main/java/.../ChatbotAgent.java` |
| Python 工具实现 | `examples/chatbot/src/main/java/.../PythonTool.java` |
| Agent 注册到 Studio | `examples/chatbot/src/main/java/.../AgentStaticLoader.java` |
| ReactAgent 主流程 | `spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/ReactAgent.java` |
| Shell 工具 | `spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/tools/ShellTool.java` |
| 读文件工具 | `spring-ai-alibaba-agent-framework/src/main/java/com/alibaba/cloud/ai/graph/agent/extension/tools/filesystem/ReadFileTool.java` |
| 内存 Checkpoint | `spring-ai-alibaba-graph-core/src/main/java/com/alibaba/cloud/ai/graph/checkpoint/savers/MemorySaver.java` |

> 项目当前 `examples/chatbot` 没有 `application.yml`/`application.properties`，所有配置走默认 + 环境变量；如果要改端口、日志级别等，自己在 `src/main/resources/` 下新建 `application.yml` 即可（resources 目录目前不存在，需要手动创建）。
