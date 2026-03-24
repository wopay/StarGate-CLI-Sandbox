<div align="right">
  <strong>English</strong> | <a href="#简体中文">简体中文</a>
</div>

<a id="english"></a>
# ⚙️ StarGate-CLI-Sandbox: The Isolated Compute Engine

**The peripheral execution bus of the Open-StarGate monolith.** This repository contains the physical blueprints for the CLI-based compute engine. It isolates high-dimensional LLMs within a strictly regulated Docker environment, enforcing resource truncation, structural communication, and physical containment.

## 📐 Architectural Blueprints

* **`Dockerfile`**: A battle-tested foundation built on `node:20-slim`. It injects Python 3, Docker capabilities, and globally installs the Gemini CLI with resilient, anti-timeout network configurations.
* **`docker-compose.yml`**: The orchestration manifesto. It mounts isolated physical volumes, sets hard limits (2.0 CPU / 2G RAM), and exposes the host's Docker socket (`/var/run/docker.sock`) to grant the sandbox the ability to execute container-level safety resets.
* **`sandbox_worker.py`**: The neural cortex of the machine tool. 
  * Implements **Cascaded Lifecycle Termination** (`os.killpg`) to instantly reclaim resources from recursive or deadlocked process trees.
  * Utilizes `su -m` privilege demotion alongside `$HOME` pointer redirection to neutralize directory traversal risks.
  * Powers the **Enigma Protocol**, restricting the AI's natural language output in favor of pure JSON `[MACHINE_SIGNALS]` for maximum compute efficiency.
* **`.env.example`**: The visual compute paddle configuration (NanoBanana Model Selector).

---

## 🗺️ The Ghost Fortress Topography (V51.5 Enigma Edition)

This view represents the internal anatomical structure of the isolated computing pod.

```text
gemini_special_forces (Factory 2: V50.0 Ghost Fortress - Pure Full-Stack Compute & Vision Hub)
├── ⚙️ [Infrastructure & Core Brain]
│   ├── docker-compose.yml       // Orchestration: Proxy penetration, resource squeezing (2.0 CPU/2G), multi-volume mounting. [V50: UTF-8 injection, boot-time ghost worker init]
│   ├── Dockerfile               // Physical Mold: Node.js 20 container injected with Python & Expect. [V50: npm mirror injection, reforging 0.33.1 stable base]
│   └── 🧠 sandbox_worker.py     // (V51.5 Enigma Bus) Core Brain: Task polling, vision scheduling, and cross-domain extradition.
│       ├── 📥 [Stateless Inbox Poller]
│       │   └── Polls /app/inbox/TASK_*.json
│       │       └── Captures execution units with `world`, `dna_rules`, `workflow_id`, `enigma_mode`.
│       │
│       ├── ⚙️ [Payload Demultiplexer]
│       │   ├── Extracts `workflow_id` & `client_id` (Deadlock protection).
│       │   ├── Injects `dna_rules` (max/stop/purge) into the watchdog.
│       │   └── 🎛️ Parses `enigma_mode` (True/False) to determine communication dimension.
│       │
│       ├── 🧬 [JIT Dynamic Prompt Forge]
│       │   ├── Injects Base System Directives.
│       │   ├── Assembles Target SOP (Dynamic DNA).
│       │   └── 🗜️ Protocol Router:
│       │       ├── 🟢 IF `enigma_mode == True`:
│       │       │   ├── Mounts `ENIGMA_DICTIONARY`.
│       │       │   ├── Opens `machine_signals` data channel.
│       │       │   └── Burns physical constraint: "⚠️ Strip natural language, use <OP_CODE|DATA> cipher!"
│       │       └── 🌐 IF `enigma_mode == False`:
│       │           └── Suspends cipher, injects "[NATURAL LANGUAGE ENABLED]".
│       │
│       ├── ⚡ [ReAct Cognitive Execution Loop]
│       │   ├── High-frequency compute request (Call LLM).
│       │   ├── Intercepts Strict JSON Payload (SOJ).
│       │   ├── 🔬 Action Decoder:
│       │   │   ├── Extracts `action` -> Triggers local physical function (Disk I/O / Extensions).
│       │   │   ├── Extracts `machine_signals` -> [ <S_OK|/app/primes.txt>, <THT|Prime Traversal> ].
│       │   │   └── Extracts `safe_markdown` -> (Approaches 0 bytes in Enigma mode).
│       │   └── 🛡️ Compute Fuse Check (Evaluates Stop/Purge redlines).
│       │
│       ├── 📡 [SSE Telemetry Broadcaster]
│       │   └── Pumps `machine_signals` ciphertext into SSE pipe for Frontend Cyberpunk HUD decoding.
│       │
│       └── 📤 [Outbox Archiver]
│           └── Upon Task Complete (<T_END>) or Termination:
│               ├── Collects all `messages` (Enigma chain of thought).
│               ├── Locks `workflow_id` metadata.
│               └── Packages and pushes to /app/outbox/ for master control handover.
│
├── 🔴 [CLI Configuration & Memory]
│   ├── .gemini/                 // CLI Core Config & Memory Hub [V50: Physical stealth achieved]
│   │   ├── oauth_creds.json     // OAuth token credentials.
│   │   ├── google_accounts.json // Bound master Google account.
│   │   ├── installation_id      // Physical fingerprint of CLI instance.
│   │   ├── trustedFolders.json  // Security boundary for cross-domain I/O.
│   │   ├── projects.json        // Workspace mapping matrix [V50: Absolute physical isolation].
│   │   ├── settings.json        // Neuron parameters & retention policy (30d).
│   │   ├── state.json           // CLI runtime state.
│   │   ├── history/             // 📜 [Memory Repository]: History mirror of CLI commands.
│   │   └── tmp/app/chats/       // 🧟 [Feral Session Prison]: Monitored by global ranger; SIGKILL on limits.
│   │
│   └── ai_worker_home/          // 👻 [Ghost Worker Zone]: (Mapped to /home/ai_worker) The true AI cage.
│       └── .gemini/commands/    // ⚡ [JIT Firmware Slot]: Async os.chown authorized, holds dynamic MD5 .toml macros (tamper-proof).
│
├── 🦾 [Extension Armory]
│   └── extensions/              
│       └── nanobanana/          // 🍌 [Vision Forge Workshop]: Multimodal extension.
│           ├── gemini-extension.json // Registers core commands (/generate) to main CLI.
│           ├── GEMINI.md        // 🧠 [Compute Imprint]: Forced context to teach AI how to call Vision APIs.
│           ├── package.json     // Build scripts and dependencies.
│           ├── node_modules/    // Underlayer dependencies.
│           └── mcp-server/      // ⚙️ [Core Power Engine]: High-frequency cloud communication.
│               ├── src/         // 🔬 Uncompiled TypeScript source.
│               │   ├── index.ts          // Hub scheduling logic.
│               │   ├── imageGenerator.ts // Prompt packager & compute requester.
│               │   └── fileHandler.ts    // 🎯 Captures cloud image stream and writes to disk.
│               ├── node_modules/// Engine-specific dependencies (Google SDK).
│               └── dist/        // 🚀 Compiled artifacts.
│                   └── index.js // 💥 Engine Igniter: Executed directly by CLI to drive drawing.
│
├── ⚔️ [Pipelines & Workspace]
│   ├── template/                // 🧬 [Gene Blueprint Library]
│   │   └── evo_ouroboros.json   // Ouroboros self-evolution protocol template.
│   │
│   ├── workspace/               // ⚔️ [Physical Execution Bench]: [V50: chmod 777, the ONLY legal AI zone].
│   │   ├── dna_source.py        // Core mirror for AI daily introspection.
│   │   ├── *_prompt_*.txt       // 📜 [ReAct Tactical Board]: Dynamic clean instruction stream.
│   │   └── assets/              // 🚚 [Temp Drop Zone]: Extradited docs/images shredded and fed to AI.
│   │
│   ├── storage/                 // 🌐 [3D/VR Assets & Gene Vault]: [V50: chmod 777 host mapping].
│   │   ├── nanobanana-output/   // 🖼️ Raw HD landing zone for vision components.
│   │   ├── duihua/              // 📦 [Extradition Pod]: Forged entities (docx/pdf/png) routing to NAS.
│   │   └── os/dna/vault/dynamic/// 🧬 [Dynamic DNA Shards]: Fine-grained imprints for O(1) JIT assembly.
│   │
│   ├── logs/                    // 📡 [Radar & System Law Monitor]: [V50: chmod 700, NO AI PEEKING].
│   │   ├── worker_radar.log     // Full lifecycle physical text log.
│   │   ├── radar_history.json   // Solidified SSE queue (prevents data loss on disconnect).
│   │   └── sandbox_dna_rules.json // ⚖️ [Global Laws]: Real-time redlines (stop/purge).
│   │
│   ├── inbox/                   // 📥 [Task Drop Pod]: Awaiting execution, filtered by .processing locks.
│   ├── outbox/                  // 📤 [Output Extradition Pod]: Async physical disk write fallback.
│   └── tmp/                     // 🗑️ [Instant Collapse Zone]: Burn-after-reading data buffers.
```

---

## ⚠️ Architect's Disclaimer (Archived)
I am not a developer. This repository provides ZERO technical support, NO installation guides, and rejects all Issues/PRs. The blueprints are 100% generated by commanding an AI assistant via text micro-manipulations. If the process-reclamation logic or container bridging mechanisms are unclear, please extract the source code and interrogate your own AI.

<br><br>

---

<div align="right">
  <a href="#english">English</a> | <strong>简体中文</strong>
</div>

<a id="简体中文"></a>
# ⚙️ StarGate-CLI-Sandbox (星门算力沙盒)：零信任执行引擎

**Open-StarGate 巨型单体的外部算力挂载舱。**
本仓库包含了基于 CLI 的纯血算力机床的物理图纸。它将高维大模型隔离在极其严苛的 Docker 环境中，实施绝对的资源物理熔断与结构化通信限制。

## 📐 核心图纸解析

* **`Dockerfile`**：基于 `node:20-slim` 的极限防爆底盘。强行注入 Python 3 运行环境与底层进程工具，并采用防断流网络策略全域安装 CLI 工具。
* **`docker-compose.yml`**：编排总纲。负责挂载隔离的物理存储卷，限制极限算力 (2.0 CPU / 2G RAM)，并向沙盒暴露宿主机 `/var/run/docker.sock` (容器级控制神经索)，以赋予其执行全局安全重启的物理权限。
* **`sandbox_worker.py`**：机床大脑与调度枢纽。
  * 实施 **进程树级联回收** (`os.killpg`)：平稳且彻底地释放死循环的野生进程，杜绝内存泄漏。
  * 利用 `su -m` 权限降维与环境变量劫持，彻底封死沙盒逃逸路线。
  * 驱动 **恩尼格玛协议 (Enigma)**：降级大模型自然语言权限，强制其使用纯 JSON `[MACHINE_SIGNALS]` 进行高压通信，保护算力免受冗余消耗。
* **`.env.example`**：视觉机床算力拨片组。

---

## 🗺️ 幽灵堡垒拓扑图谱 (V51.5 恩尼格玛版)

这是算力挂载舱内部的解剖级结构视图。

```text
gemini_special_forces (二厂：V50.0 幽灵堡垒·纯血全栈算力与视觉中枢)
├── ⚙️【基建与主脑总成】(Infrastructure & Core Brain)
│   ├── docker-compose.yml       // 编排总纲：统筹代理穿透、资源压榨 (2.0 CPU/2G)、多源物理卷挂载【V50新增：UTF-8 字符集强插、开机初始化幽灵劳工 ai_worker】
│   ├── Dockerfile               // 物理模具：采用 Node.js 20 容器强行注入 Python 与 Expect 机械臂【V50新增：强插 npm 淘宝防断流镜像，重铸 0.33.1 稳定底座】
│   └── 🧠 sandbox_worker.py (V51.5 恩尼格玛·黑灯执行总线) // 核心大脑：负责任务轮询、视觉调度与跨域引渡
│       ├── 📥 【任务嗅探器】 (Stateless Inbox Poller)
│       │   └── 轮询 /app/inbox/TASK_*.json
│       │       └── 捕获完美执行单元：自带 `world`, `dna_rules`, `workflow_id`, `enigma_mode`
│       │
│       ├── ⚙️ 【指令拆解与算力定标】 (Payload Demultiplexer)
│       │   ├── 提取溯源指纹：`workflow_id` & `client_id` (死锁保护，绝不丢失)
│       │   ├── 压入物理红线：将 `dna_rules` (max/stop/purge) 注入当前线程监控狗 (Watchdog)
│       │   └── 🎛️ 截获拨码开关：解析 `enigma_mode` (True/False)，决定通讯维度
│       │
│       ├── 🧬 【JIT 提示词高压熔铸炉】 (Dynamic Prompt Forge)
│       │   ├── 注入底层系统钢印 (Base System Directives)
│       │   ├── 组装动态 DNA 业务逻辑 (Target SOP)
│       │   └── 🗜️ 协议分流器 (Protocol Router):
│       │       ├── 🟢 IF `enigma_mode == True`:
│       │       │   ├── 强制挂载 `ENIGMA_DICTIONARY` (密码本字典)
│       │       │   ├── 开放 `machine_signals` 专属数据通道
│       │       │   └── 烧录物理约束："⚠️ 剥夺自然语言生成权限，强制使用 <OP_CODE|DATA> 密文汇报，极致压缩 safe_markdown！"
│       │       └── 🌐 IF `enigma_mode == False`:
│       │           └── 悬停密码本，注入 "[NATURAL LANGUAGE ENABLED]" 放开自然语言生成权限
│       │
│       ├── ⚡ 【ReAct 机械臂执行核心】 (Cognitive Execution Loop)
│       │   ├── 发起高频算力请求 (Call LLM)
│       │   ├── 截获 SOJ 结构化响应 (Strict JSON Payload)
│       │   ├── 🔬 指令分频器 (Action Decoder):
│       │   │   ├── 提取 `action` -> 触发本地物理函数 (读写磁盘 / 调用扩展)
│       │   │   ├── 提取 `machine_signals` -> [ <S_OK|/app/primes.txt>, <THT|素数遍历> ]
│       │   │   └── 提取 `safe_markdown` -> (在 Enigma 模式下，此处将趋近于 0 字节，终极省流)
│       │   └── 🛡️ 算力熔断池检定 (评估当前轮次是否触发 Stop/Purge 红线)
│       │
│       ├── 📡 【全域雷达脉冲泵】 (SSE Telemetry Broadcaster)
│       │   └── 将提取到的 `machine_signals` 密文，实时泵入 SSE 管道。
│       │       └── (前端 0.html 的解码器将在此处接管，把密文翻译为赛博朋克风的 HUD 视觉日志)
│       │
│       └── 📤 【战利品引渡总成】 (Outbox Archiver)
│           └── 任务达成 (<T_END>) 或 被斩杀后：
│               ├── 收集所有 `messages` (保留完整的 Enigma 短码思维链)
│               ├── 封入剩余算力账单
│               ├── 绝对锁定 `workflow_id` 元数据
│               └── 整体打包，暴力推入 /app/outbox/，向主控中心完美交接！
│
├── 🔴【算力底座腹地】(CLI Configuration & Memory)
│   ├── .gemini/                 // CLI 核心配置与神经记忆中枢【V50升级：系统级空间转移，现已对大模型实现物理隐身】
│   │   ├── oauth_creds.json     // 授权命门：OAuth 令牌鉴权凭证
│   │   ├── google_accounts.json // 身份锚点：绑定的主控 Google 账号加密配置
│   │   ├── installation_id      // 物理指纹：CLI 实例的绝对唯一标识
│   │   ├── trustedFolders.json  // 信任白名单：跨域文件操作的安全边界防线
│   │   ├── projects.json        // 映射矩阵：工作区与项目命名空间的对应关系【V50注：越权黑客最渴望的目标，已实现绝对物理隔离】
│   │   ├── settings.json        // 神经元参数：会话保留策略 (30d) 与安全验证设置
│   │   ├── state.json           // 运行时态：CLI 初始化状态位
│   │   ├── history/             // 📜【记忆沉淀库】：CLI 交互命令的历史文稿镜像
│   │   │   ├── app/             //  ├─ 主程序的历史执行溯源
│   │   │   ├── gemini/          //  ├─ CLI 自身命令的交互溯源
│   │   │   └── workspace/       //  └─ 物理工作台的操作溯源
│   │   └── tmp/app/chats/       // 🧟【野生异体监禁区】：存放脱离掌控的野生 Session，由全域游侠监控，超限即触发 SIGKILL 抹杀
│   │
│   └── ai_worker_home/          // 👻【幽灵劳工专属区】：(映射为 /home/ai_worker) AI 真正的执行牢笼
│       └── .gemini/commands/    // ⚡【JIT 固件烧录槽】：无阻塞异步 os.chown 赋权，存放依据 DNA 动态生成的 MD5 .toml 宏指令 (免疫篡改)
│
├── 🦾【外挂装甲总库】(Extension Armory)
│   └── extensions/              
│       └── nanobanana/          // 🍌【视觉锻造专属车间】：多模态扩展
│           ├── gemini-extension.json // 🏷️ [机床出厂铭牌]：向主 CLI 注册 /generate 等核心指令，指明启动路径
│           ├── GEMINI.md        // 🧠 [算力思想钢印]：呼叫机床时强制喂给大模型，教会其调用视觉 API
│           ├── package.json     // 📋 [外层装配清单]：基础构建脚本和依赖
│           ├── node_modules/    // 🔩 [外围零件库]：底层依赖包
│           └── mcp-server/      // ⚙️ [核心动力引擎]：负责与云端大模型进行高频并发通讯
│               ├── src/         // 🔬 [核心图纸区]：未编译的 TypeScript 源码
│               │   ├── index.ts          // 中枢调度逻辑
│               │   ├── imageGenerator.ts // 负责打包提示词，向云端开火请求算力
│               │   └── fileHandler.ts    // 🎯 负责接住云端图片流，物理落盘 (后续魔改核心目标)
│               ├── node_modules/// 🔩 [引擎专属零件库]：含与谷歌 API 通讯的核心 SDK
│               └── dist/        // 🚀 [终极编译产物区]：探针安检目标
│                   └── index.js // 💥 [引擎点火器]：机床绝对核心，CLI 直接执行此文件驱动画图
│
├── ⚔️【流水线与工作区】(Pipelines & Workspace)
│   ├── template/                // 🧬【基因图纸库】
│   │   └── evo_ouroboros.json   // 衔尾蛇自进化协议模板（每日强制触发底盘代码自省）
│   │
│   ├── workspace/               // ⚔️【物理执行工作台】：【V50升级：chmod 777 大模型唯一合法活动区，离开即 Permission denied】
│   │   ├── dna_source.py        // 本体镜像：主脑主动拷贝的自身源码，供 AI 每日审视与进化
│   │   ├── *_prompt_*.txt       // 📜【ReAct 战术板】：每次 Loop 循环动态生成的纯净指令流，规避管道流堵塞
│   │   └── assets/              // 🚚【临时卸货区】：引渡文档/图片图纸，隐形机械手粉碎提纯后投喂给模型
│   │
│   ├── storage/                 // 🌐【3DVR视觉资产与基因总库】：【V50升级：chmod 777 对接宿主机渲染引擎】
│   │   ├── nanobanana-output/   // 🖼️ 视觉组件吐出的高清原始着陆点 (待源码魔改路径)
│   │   ├── duihua/              // 📦【跨域引渡舱】：锻造完毕的实体文件 (docx/pdf/png) 最终安全着陆点，直通 NAS
│   │   └── os/dna/vault/dynamic/// 🧬【动态 DNA 碎片库】：存放细粒度思想钢印，供 JIT 编译器 O(1) 寻址并组装烧录
│   │
│   ├── logs/                    // 📡【雷达与系统法则监控区】：【V50升级：绝对隔离 chmod 700，严禁大模型窥探】
│   │   ├── worker_radar.log     // 纯血监听脉冲：全生命周期物理级文本记录
│   │   ├── radar_history.json   // SSE 队列固化：防止前端断线导致的雷达情报丢失
│   │   └── sandbox_dna_rules.json // ⚖️【全域大盘法则】：实时烧录的最高行动准则，定义 stop/purge 容忍红线
│   │
│   ├── inbox/                   // 📥【任务投递舱】(外挂共享，待吞噬执行，由单线并发锁 .processing 接管过滤)
│   ├── outbox/                  // 📤【文本成果引渡舱】(执行完毕的产物交付区，异步物理落盘兜底最后防线)
│   └── tmp/                     // 🗑️【瞬时坍缩区】(运行时动态生成，处理高压数据缓冲，阅后即焚)】
```

## ⚠️ 厂长声明 (Archived)
本人非科班程序员，本库拒接任何技术支持，不提供保姆级安装教程，谢绝一切 Issue 与 PR。全库代码皆为指挥 AI 代笔落盘的产物。
如果你看不懂图纸里的级联释放逻辑与套娃容器权限，请直接将源码提取，并拷问你自己的 AI 助手。
