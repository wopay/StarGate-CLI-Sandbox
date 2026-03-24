<div align="right">
  <strong>English</strong> | <a href="#简体中文">简体中文</a>
</div>

<a id="english"></a>
# ⚙️ StarGate-CLI-Sandbox: The Isolated Compute Engine

**The precise execution bus of the Open-StarGate architecture.** This repository contains the operational blueprints for the CLI-based compute engine. It isolates high-dimensional LLMs within a strictly regulated, high-cleanliness Docker environment, focusing on deterministic execution, resource management, and structural communication.

## 📐 Architectural Blueprints

* **`Dockerfile`**: A stable foundation built on `node:20-slim`. It integrates Python 3, operational tools, and globally installs the Gemini CLI with resilient, anti-timeout network configurations.
* **`docker-compose.yml`**: The orchestration configuration. It mounts isolated physical volumes, sets resource limits (2.0 CPU / 2G RAM), and exposes the host's Docker socket (`/var/run/docker.sock`) to grant the sandbox the ability to execute container-level safety resets.
* **`sandbox_worker.py`**: The core dispatcher and execution bus. 
  * Implements **Deterministic Lifecycle Reclamation** (`os.killpg`) to gracefully and thoroughly reclaim resources from unresponsive or recursive process trees.
  * Utilizes `su -m` privilege demotion alongside `$HOME` pointer redirection, adhering to the **Principle of Least Privilege** to prevent directory traversal risks.
  * Powers the **Universal Machine Language (UML) Protocol**, prioritizing highly compressed JSON `[MACHINE_SIGNALS]` over natural language to maximize compute efficiency and ensure deterministic parsing.
* **`.env.example`**: The multimodal compute and vision extension configuration (NanoBanana Model Selector).

---

## 🗺️ The Isolated Fortress Topography (V51.5 UML Edition)

This view represents the internal anatomical structure of the isolated computing pod.

```text
stargate_execution_node (Factory 2: V50.0 Isolated Fortress - Full-Stack Compute Hub)
├── ⚙️ [Infrastructure & Core Dispatcher]
│   ├── docker-compose.yml       // Orchestration: Network proxying, resource management (2.0 CPU/2G), multi-volume mounting. [V50: UTF-8 standard, background service account init]
│   ├── Dockerfile               // Build Foundation: Node.js 20 container integrated with Python & operational tools.
│   └── 🧠 sandbox_worker.py     // (V51.5 UML Bus) Core Dispatcher: Task polling, vision scheduling, and cross-domain routing.
│       ├── 📥 [Stateless Inbox Poller]
│       │   └── Polls /app/inbox/TASK_*.json
│       │       └── Captures execution units with `world`, `dna_rules`, `workflow_id`, `uml_mode`.
│       │
│       ├── ⚙️ [Payload Demultiplexer]
│       │   ├── Extracts `workflow_id` & `client_id` (Anomaly prevention).
│       │   ├── Injects `dna_rules` (max/stop/reclaim limits) into the system watchdog.
│       │   └── 🎛️ Parses `uml_mode` (True/False) to determine the communication protocol.
│       │
│       ├── 🧬 [JIT Dynamic Prompt Forge]
│       │   ├── Injects Base System Directives.
│       │   ├── Assembles Target SOP (Dynamic DNA).
│       │   └── 🗜️ Protocol Router:
│       │       ├── 🟢 IF `uml_mode == True`:
│       │       │   ├── Mounts `UML_DICTIONARY`.
│       │       │   ├── Opens `machine_signals` data channel.
│       │       │   └── Prioritizes structural output: "⚠️ Optimize natural language, strictly use <OP_CODE|DATA> protocol!"
│       │       └── 🌐 IF `uml_mode == False`:
│       │           └── Suspends UML rules, injects "[NATURAL LANGUAGE ENABLED]".
│       │
│       ├── ⚡ [ReAct Execution Loop]
│       │   ├── High-frequency compute request (Call LLM).
│       │   ├── Intercepts Strict JSON Payload (SOJ).
│       │   ├── 🔬 Action Decoder:
│       │   │   ├── Extracts `action` -> Triggers local operational function (Disk I/O / Extensions).
│       │   │   ├── Extracts `machine_signals` -> [ <S_OK|/app/primes.txt>, <THT|Prime Traversal> ].
│       │   │   └── Extracts `safe_markdown` -> (Approaches 0 bytes in UML mode for efficiency).
│       │   └── 🛡️ System Threshold Check (Evaluates Stop/Reclaim limits).
│       │
│       ├── 📡 [SSE Telemetry Broadcaster]
│       │   └── Transmits `machine_signals` structural data into SSE pipe for Frontend UI real-time rendering.
│       │
│       └── 📤 [Outbox Archiver]
│           └── Upon Task Complete (<T_END>) or Reset:
│               ├── Collects all `messages` (Preserving the UML chain of thought).
│               ├── Records resource consumption.
│               ├── Locks `workflow_id` metadata.
│               └── Packages and safely transmits to /app/outbox/ for master control handover.
│
├── 🔴 [CLI Configuration & Memory]
│   ├── .gemini/                 // CLI Core Config & Memory Hub [V50: State isolation achieved]
│   │   ├── oauth_creds.json     // OAuth token credentials.
│   │   ├── google_accounts.json // Bound master Google account.
│   │   ├── installation_id      // Physical fingerprint of CLI instance.
│   │   ├── trustedFolders.json  // Security boundary for cross-domain I/O.
│   │   ├── projects.json        // Workspace mapping matrix.
│   │   ├── settings.json        // System parameters & retention policy (30d).
│   │   ├── state.json           // CLI runtime state.
│   │   ├── history/             // 📜 [Audit Log]: History mirror of CLI commands.
│   │   └── tmp/app/chats/       // ♻️ [Session Buffer]: Temporary sessions, monitored and pruned to prevent memory overflow.
│   │
│   └── ai_worker_home/          // 🛡️ [Designated Workspace]: (Mapped to /home/ai_worker) The strictly bounded execution area.
│       └── .gemini/commands/    // ⚡ [JIT Configuration Slot]: Async os.chown authorized, holds dynamic MD5 .toml configurations.
│
├── 🦾 [Extension Modules]
│   └── extensions/              
│       └── nanobanana/          // 🍌 [Vision Component]: Multimodal generation extension.
│           ├── gemini-extension.json // Registers core commands (/generate) to main CLI.
│           ├── GEMINI.md        // 🧠 [Interface Guidelines]: Context instructions for Vision API usage.
│           ├── package.json     // Build scripts and dependencies.
│           ├── node_modules/    // Underlayer dependencies.
│           └── mcp-server/      // ⚙️ [Core Communication Engine]: High-frequency cloud API service.
│               ├── src/         // 🔬 Uncompiled TypeScript source.
│               │   ├── index.ts          // Service scheduling logic.
│               │   ├── imageGenerator.ts // Prompt packager & API requester.
│               │   └── fileHandler.ts    // 🎯 Captures cloud asset stream and writes to disk.
│               ├── node_modules/// Engine-specific dependencies (Google SDK).
│               └── dist/        // 🚀 Compiled artifacts.
│                   └── index.js // 💥 Service Entrypoint: Executed directly by CLI to process multimodal requests.
│
├── ⚔️ [Pipelines & Workspace]
│   ├── template/                // 🧬 [Blueprint Library]
│   │   └── evo_ouroboros.json   // Automated code review and self-optimization template.
│   │
│   ├── workspace/               // ⚔️ [Execution Bench]: [V50: chmod 777, strictly isolated active directory].
│   │   ├── dna_source.py        // Core mirror for logic inspection.
│   │   ├── *_prompt_*.txt       // 📜 [Instruction Buffer]: Dynamic clean instruction stream.
│   │   └── assets/              // 🚚 [Asset Processing Zone]: Extradited files parsed for context integration.
│   │
│   ├── storage/                 // 🌐 [Cross-Domain Mounts]: [V50: Shared storage volumes].
│   │   ├── nanobanana-output/   // 🖼️ Raw HD landing zone for vision components.
│   │   ├── duihua/              // 📦 [Archive Pod]: Generated entities (docx/pdf/png) routing to NAS.
│   │   └── os/dna/vault/dynamic/// 🧬 [Dynamic DNA Shards]: Fine-grained configurations for O(1) JIT assembly.
│   │
│   ├── logs/                    // 📡 [Telemetry & System Limits]:
│   │   ├── worker_radar.log     // Full lifecycle execution log.
│   │   ├── radar_history.json   // Solidified SSE queue (prevents data loss on disconnect).
│   │   └── sandbox_dna_rules.json // ⚖️ [Global Directives]: Real-time system limits and thresholds.
│   │
│   ├── inbox/                   // 📥 [Task Queue]: Awaiting execution, filtered by .processing status.
│   ├── outbox/                  // 📤 [Output Buffer]: Async physical disk write staging area.
│   └── tmp/                     // 🗑️ [Runtime Cleanup Zone]: Temporary buffers designed for auto-removal.
```

---

## ⚠️ Architectural Note (Archived)
This repository is a snapshot of an architectural deduction focusing on extreme hardware optimization. The codebase is designed to test structural communication protocols and strict container isolation concepts. If the resource-reclamation logic or container bridging mechanisms are unclear, please review the source code directly.

<br><br>

---

<div align="right">
  <a href="#english">English</a> | <strong>简体中文</strong>
</div>

<a id="简体中文"></a>
# ⚙️ StarGate-CLI-Sandbox (星门算力沙盒)：隔离执行引擎

**Open-StarGate 架构的高效执行总线。**
本仓库包含了基于 CLI 的算力调度环境部署图纸。它将高维大模型隔离在高度洁净且规则明确的 Docker 环境中，专注于确定性执行、资源能效管理以及结构化通信。

## 📐 核心图纸解析

* **`Dockerfile`**：基于 `node:20-slim` 的稳定运行底盘。集成 Python 3 运行环境与执行工具链，并采用优化的网络策略全局安装 CLI 工具。
* **`docker-compose.yml`**：编排总纲。负责挂载隔离的物理存储卷，限制算力资源 (2.0 CPU / 2G RAM)，并向沙盒暴露宿主机 `/var/run/docker.sock` 以赋予其执行全局安全重启的系统权限。
* **`sandbox_worker.py`**：调度核心与执行总线。
  * 实施 **确定性生命周期回收** (`os.killpg`)：平稳且彻底地释放无响应的进程树，安全回收资源并杜绝内存泄漏。
  * 遵循 **最小权限原则**，利用 `su -m` 权限降维与环境变量 `$HOME` 重定向机制，严格控制执行边界，防范目录遍历风险。
  * 驱动 **通用机械语言 (UML) 协议**：优化大模型自然语言输出，引导其使用高度压缩的 JSON `[MACHINE_SIGNALS]` 进行结构化通信，最大化算力能效与解析准确率。
* **`.env.example`**：多模态计算与视觉扩展配置参数。

---

## 🗺️ 隔离堡垒拓扑图谱 (V51.5 UML 版)

这是算力挂载舱内部的详细结构视图。

```text
stargate_execution_node (二厂：V50.0 隔离堡垒·全栈算力与视觉中枢)
├── ⚙️【基建与调度总线】(Infrastructure & Core Dispatcher)
│   ├── docker-compose.yml       // 编排总纲：统筹网络代理、资源管理 (2.0 CPU/2G)、多源物理卷挂载【V50新增：UTF-8 标准化、初始化后台服务账户 ai_worker】
│   ├── Dockerfile               // 运行底座：采用 Node.js 20 容器集成 Python 与执行工具链【V50新增：优化镜像源，构建稳定环境】
│   └── 🧠 sandbox_worker.py (V51.5 UML 执行总线) // 核心调度：负责任务轮询、组件调度与跨域数据流转
│       ├── 📥 【无状态任务嗅探器】 (Stateless Inbox Poller)
│       │   └── 轮询 /app/inbox/TASK_*.json
│       │       └── 捕获执行单元：载入 `world`, `dna_rules`, `workflow_id`, `uml_mode`
│       │
│       ├── ⚙️ 【指令拆解与定标】 (Payload Demultiplexer)
│       │   ├── 提取溯源指纹：`workflow_id` & `client_id` (异常防范追踪)
│       │   ├── 载入系统阈值：将 `dna_rules` (max/stop/reclaim) 注入监控模块
│       │   └── 🎛️ 解析模式：识别 `uml_mode` (True/False)，决定后续通讯协议
│       │
│       ├── 🧬 【JIT 提示词熔铸炉】 (Dynamic Prompt Forge)
│       │   ├── 注入底层系统指令 (Base System Directives)
│       │   ├── 组装动态业务逻辑 (Target SOP)
│       │   └── 🗜️ 协议分流器 (Protocol Router):
│       │       ├── 🟢 IF `uml_mode == True`:
│       │       │   ├── 挂载 `UML_DICTIONARY` (结构化通信字典)
│       │       │   ├── 开放 `machine_signals` 专属数据通道
│       │       │   └── 应用输出规范："⚠️ 优化自然语言生成，优先使用 <OP_CODE|DATA> 结构化输出以提升能效！"
│       │       └── 🌐 IF `uml_mode == False`:
│       │           └── 悬停结构化约束，注入 "[NATURAL LANGUAGE ENABLED]" 恢复自然文本交互
│       │
│       ├── ⚡ 【ReAct 执行核心】 (Cognitive Execution Loop)
│       │   ├── 发起算力请求 (Call LLM)
│       │   ├── 截获 SOJ 结构化响应 (Strict JSON Payload)
│       │   ├── 🔬 指令解析器 (Action Decoder):
│       │   │   ├── 提取 `action` -> 触发本地系统函数 (读写磁盘 / 调用组件)
│       │   │   ├── 提取 `machine_signals` -> [ <S_OK|/app/primes.txt>, <THT|素数遍历> ]
│       │   │   └── 提取 `safe_markdown` -> (在 UML 模式下极度精简，降低开销)
│       │   └── 🛡️ 阈值检定 (评估当前状态是否触发 Stop/Reclaim 系统限制)
│       │
│       ├── 📡 【全域通信脉冲泵】 (SSE Telemetry Broadcaster)
│       │   └── 将提取到的 `machine_signals` 数据流，实时泵入 SSE 管道供前端 UI 呈现结构化日志。
│       │
│       └── 📤 【产物安全归档】 (Outbox Archiver)
│           └── 任务结束 (<T_END>) 或 触发重置后：
│               ├── 收集所有 `messages` (保存完整的 UML 结构化思维链)
│               ├── 记录本次执行的资源消耗
│               ├── 锚定 `workflow_id` 元数据
│               └── 统一打包，安全回传至 /app/outbox/，向主控中心交接
│
├── 🔴【系统底座与记忆区】(CLI Configuration & Memory)
│   ├── .gemini/                 // CLI 核心配置与状态存储【V50升级：实现运行状态隔离】
│   │   ├── oauth_creds.json     // 鉴权凭证
│   │   ├── google_accounts.json // 绑定的主控账号配置
│   │   ├── installation_id      // 实例唯一标识
│   │   ├── trustedFolders.json  // 跨域文件操作的安全边界
│   │   ├── projects.json        // 工作区映射矩阵
│   │   ├── settings.json        // 运行参数与保留策略设置
│   │   ├── state.json           // 初始化状态位
│   │   ├── history/             // 📜【审计日志】：CLI 交互命令的历史镜像记录
│   │   │   ├── app/             //  ├─ 主程序的执行溯源
│   │   │   ├── gemini/          //  ├─ CLI 命令的交互溯源
│   │   │   └── workspace/       //  └─ 物理工作台的操作溯源
│   │   └── tmp/app/chats/       // ♻️【会话缓冲池】：存放临时任务会话，触发阈值即执行平滑清理
│   │
│   └── ai_worker_home/          // 🛡️【独立执行工作区】：被严格限制权限的系统运行边界
│       └── .gemini/commands/    // ⚡【JIT 配置挂载点】：异步赋权，存放根据参数动态生成的 .toml 指令文件
│
├── 🦾【扩展组件总库】(Extension Modules)
│   └── extensions/              
│       └── nanobanana/          // 🍌【多模态生成组件】：视觉处理扩展
│           ├── gemini-extension.json // 🏷️ [组件注册配置]：向 CLI 注册核心指令及启动路径
│           ├── GEMINI.md        // 🧠 [接口调用规范]：定义大模型调用视觉 API 的上下文约束
│           ├── package.json     // 📋 [构建清单]：依赖及脚本
│           ├── node_modules/    // 🔩 [基础依赖]：底层代码包
│           └── mcp-server/      // ⚙️ [核心通信服务]：负责与云端进行高频并发通讯
│               ├── src/         // 🔬 [源码区]：TypeScript 源码
│               │   ├── index.ts          // 中枢调度逻辑
│               │   ├── imageGenerator.ts // 负责封装请求与参数传递
│               │   └── fileHandler.ts    // 🎯 捕获云端数据流并安全落盘
│               ├── node_modules/// 🔩 [专属依赖]：含通信 SDK
│               └── dist/        // 🚀 [编译产物区]：构建后的可执行文件
│                   └── index.js // 💥 [服务入口]：由 CLI 直接调用执行请求
│
├── ⚔️【流水线与物理工作区】(Pipelines & Workspace)
│   ├── template/                // 🧬【模板库】
│   │   └── evo_ouroboros.json   // 自动化代码审查与自我优化协议模板
│   │
│   ├── workspace/               // ⚔️【执行台】：【V50升级：系统唯一授权的严格读写隔离区】
│   │   ├── dna_source.py        // 代码镜像：供审查流程参考的逻辑源码
│   │   ├── *_prompt_*.txt       // 📜【指令缓冲】：运行时动态生成的纯净任务指令，防拥堵
│   │   └── assets/              // 🚚【资产缓冲处理区】：对传入文档进行解析与提取以备调用
│   │
│   ├── storage/                 // 🌐【跨域存储挂载点】：【V50升级：对接外部存储与资产系统】
│   │   ├── nanobanana-output/   // 🖼️ 视觉组件输出的高清图像落盘区
│   │   ├── duihua/              // 📦【产物归档舱】：处理完毕的文档/图像最终存储区
│   │   └── os/dna/vault/dynamic/// 🧬【动态配置碎片库】：存放细粒度指令，供 JIT 编译器 O(1) 寻址与组装
│   │
│   ├── logs/                    // 📡【遥测与阈值监控区】
│   │   ├── worker_radar.log     // 全生命周期运行日志
│   │   ├── radar_history.json   // SSE 队列持久化：防止连接闪断导致的情报丢失
│   │   └── sandbox_dna_rules.json // ⚖️【全域运行法则】：实时同步的系统阈值与限制基准
│   │
│   ├── inbox/                   // 📥【任务输入队列】(利用 .processing 锁处理并发过滤)
│   ├── outbox/                  // 📤【产物输出队列】(执行完毕的数据安全回传防线)
│   └── tmp/                     // 🗑️【运行时缓冲清理区】(处理高压数据缓冲，用后即焚)
```

## ⚠️ 架构师说明 (Archived)
本仓库为聚焦极端硬件优化的架构推演快照。旨在验证结构化通信协议与容器级安全隔离的概念。全库代码由 AI 辅助生成，如需深入理解调度逻辑与隔离机制，建议直接查阅源码。
