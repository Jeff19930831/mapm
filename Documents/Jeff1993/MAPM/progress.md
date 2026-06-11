# MAPM — progress

## 2026-06-11 接力流程 v3.14 + CodeGraph/CODEMAP 分工

**目标**：重划 `checkpoint` / `con-dev` / `session-handoff` 的职责边界，并把 CodeGraph 与 durable CODEMAP 的分工写入治理规则。

**完成内容**：
1. **三流程边界**：`session-handoff` 仅同机短续接；`con-dev` 做冷启动接手和本地 CodeGraph 准备；`checkpoint` 做验证、归档、onboarding 自检和 commit，push/deploy 需明确授权。
2. **地图分工**：CodeGraph 是本地开发雷达（symbol/call graph/影响面，`.codegraph/` 不入 Git）；`docs/onboarding/CODEMAP.md` 是可提交交接地图，由 `refresh_codemap.py` / `check_onboarding.py` 维护。
3. **规则源更新**：同步更新 `agent-kit/claude/skills/{checkpoint,con-dev,session-handoff}/SKILL.md`、Codex onboarding 扩展、`collab-entry.md` v3.14、`onboarding.md` v3.14、`onboarding-compact.md`。

**验证**：
- `quick_validate.py` 通过本机 `.codex/skills` 与 `.agents/skills` 的三份新版 skill。
- `agent-kit/claude/skills/` 已回写为治理源；待运行 `scripts/agent_kit_sync.py --apply` 做跨目标同步。

## 2026-06-05 Memory Recall 搜索策略修复

**目标**：修复 con-dev / checkpoint skill 中 agentmemory 搜索策略，解决 Phase 2.5 云端记忆返回空的问题。

**根因**：单一泛查询（`"项目名 status decision credentials blocker"`）因词频分散、核心概念不突出，向量搜索相似度低于阈值，返回空。

**修复内容**：
1. **con-dev SKILL.md Phase 2.5** — 单一泛查询 → 3 次聚焦查询并行（checkpoint deploy / blocker decision / credentials server）
2. **checkpoint SKILL.md Step 2.5** — 同上策略
3. 新增「搜索 query 编写原则」：精确项目名 + 高频动作词，每次 2-3 词，不超过 4 词
4. 兜底机制：3 次全空时用 `agentmemory_memory_export` 全量检查

**验证**：
- `agentmemory_memory_recall(query="tradingcenter checkpoint")` → 命中 2 条 ✅
- `agentmemory_memory_recall(query="tradingcenter status decision credentials blocker development")` → 空 ❌（旧策略）
- commit: `1e012ac` pushed to `origin/mapm`

## 2026-06-03 治理优化 Roadmap 全部落地 (OPT-1..6)

**目标**：执行治理优化 Roadmap 全部 6 个优化点。

**完成内容**：

1. **OPT-1: agent-kit 同步器** — `scripts/agent_kit_sync.py`（25 测试全绿），manifest `skill_sync` 驱动，34 个 skill 部署到 4 目标目录，全部 SYNCED。
2. **OPT-2: Skill/ 双源清理** — deep-search 迁移到 `agent-kit/claude/skills/deep-search/SKILL.md`，废弃 `Skill/checkpoint.md`，`Skill/` 降为 README 指针，更新 collab-entry/onboarding/commands.md 引用。
3. **OPT-3: 规范重叠解决** — `项目规范.md` 降级为归档指针，独特内容提取到 5 个 `docs/sop/` runbook。
4. **OPT-4: skill 不对称确认** — Claude/Codex 扩展模式有意，在 `codex/skills.md` 添加分工说明。
5. **OPT-5: handoff 脚本确认** — 两脚本有意分工，加头部 docstring 明确职责边界。
6. **OPT-6: con-dev MCP 回退** — Phase 2.5 Memory Recall 增加 MCP tool 优先 + curl 回退。
7. **本机配置更新** — `~/CLAUDE.md` 重写（MCP servers / 治理 skill 清单 / agent-kit 同步规则）；`~/.claude/CLAUDE.md` 添加同步规则；`onboarding.md` § 7 新增 § 7.0 同步工具；`onboarding-compact.md` 添加同步规则和引用；`collab-entry.md` 更新 skill 表和安装说明。

**验证**：
- `python3 -m unittest MAPM.tests.test_agent_kit_sync MAPM.tests.test_doc_lifecycle` — 32/32 PASS
- `python3 scripts/agent_kit_sync.py` — 34/34 synced, 0 missing, 0 drift

## 2026-06-03 治理资产梳理 + agent-kit 同步器规划 + 优化 Roadmap

**目标**：全面梳理 MAPM 治理资产（规范文档 / skill / 治理脚本），识别系统性问题并形成可执行的优化规划。

**完成内容**：

1. **con-dev skill 优化合并**：`code_path` 已存在时执行 `git pull` 而非跳过；`origin/mapm` → `main` fast-forward + push。
2. **治理资产梳理**：识别 5 个优化点（OPT-1..5）。元洞察：MAPM 规范设计强但执行工具化滞后（manifest 声明空类别、Doc Lifecycle Gate 自身规范却重叠、§7.1 强约束但副本漂移）。
3. **OPT-1（agent-kit 安装副本漂移）完整规划**：
   - Spec：`MAPM/docs/superpowers/specs/2026-06-03-agent-kit-sync-design.md`（跨平台、manifest `skill_sync` 驱动，4 目标目录含 zcode，Codex frontmatter 补齐）。
   - Plan：`MAPM/docs/superpowers/plans/2026-06-03-agent-kit-sync-implementation.md`（10 任务 TDD）。
4. **优化 Roadmap**：`MAPM/docs/2026-06-03-governance-optimization-roadmap.md`（OPT-1..5 排期 + 依赖）。

**验证证据**：

- 漂移实测：7 个 Claude skill 全漂移/缺失（diff 行数记录于 spec Purpose）。
- `python3 scripts/governance_lint.py`：OK（3 warning，与本轮无关）。
- 文档落盘：roadmap 123 行 / spec 249 行 / plan 979 行。

**风险 / 后续**：

- 3 个规划文档已提交，OPT-1 实现（Task 1-10）尚未执行。
- 云端 agentmemory 服务本轮不可达，Memory Store 跳过。
- 顺手清理 plan.md Active 区 2026-05-29 遗留的 3 个已完成 `[x]` 项。

## 2026-05-29 Onboarding v3.11 小写四文档优先 + wechat-macro-kb 对齐

**目标**：

- 解决同一项目同时存在 `handoff.md` / `HANDOFF.md`、`progress.md` / `PROGRESS.md` 时 Agent 冷启动和 checkpoint 写入目标不一致的问题。
- 以 wechat-macro-kb 为首个大项目，把最新 Doc Lifecycle Gate + 联动契约规范落到当前入口文档。

**完成内容**：

1. **全局规则更新**：
   - `collab-entry.md` 升级到 v3.11。
   - `onboarding.md` 增加 v3.11 说明：小写四文档是当前写入目标，大写文件只作兼容读取 / 历史镜像。
   - `onboarding-compact.md` 增加“小写四文档优先”冷启动提示。
2. **wechat-macro-kb 对齐**：
   - `README.md` 重写为稳定短入口，移除 2026-04 过期数据表。
   - `handoff.md` 改为 Persistent / Current Takeover / Index。
   - `plan.md` 改为 Active / Next / Archived Plans。
   - Jeff1993 docs mirror 同步刷新 `wechat-macro-kb/README.md`、`wechat-macro-kb/plan.md`、`wechat-macro-kb/HANDOFF.md`、`wechat-macro-kb/PROGRESS.md`。
3. **注册表同步**：
   - `.project-status.yaml` 中 wechat-macro-kb `last_update` 更新到 2026-05-29。
   - sync required 改为小写 `README.md` / `plan.md` / `progress.md` / `handoff.md`。

**验证证据**：

- `python3 scripts/project_registry.py lint wechat-macro-kb`
- `python3 scripts/check_linkage_contract.py --project wechat-macro-kb --task 'EBC data contract / KB continuation'`

**风险 / 后续**：

- 旧大写 `HANDOFF.md` / `PROGRESS.md` 在 docs mirror 中仍保留，供跨设备历史兼容；不要再把它们当作代码仓当前入口。

## 2026-05-28 项目联动协同监督机制落地

`[CONTRACT-CHANGE: docs/contracts/ebc-auto--wechat-macro-kb.md]`

**目标**：

- 把 EBC 目录拆分导致 wechat-macro-kb 铁水/发运 stale 的事故，泛化成全局“项目联动协同”规范。
- 由 MAPM 负责数据规范、上下游 contract、impact/context gate 和 checkpoint 阻断标准，避免只改生产方或消费方一端。

**完成内容**：

1. **全局规则接入**：
   - `collab-entry.md` 升级到 v3.10，新增项目联动协同短规则。
   - `onboarding.md` 新增 § 17：联动契约定义、触发条件、执行流程、Linkage Supervisor、checkpoint 阻断条件和禁止事项。
   - `onboarding-compact.md` 增加联动契约变化的冷启动提示和 § 17 索引。
2. **EBC → KB 契约落地**：
   - 新增 `docs/contracts/ebc-auto--wechat-macro-kb.md`，记录 EBC 关键目录、Excel header、下游核心 slug、必跑验证和 2026-05-28 目录拆分事故 lore。
   - `.project-status.yaml` 登记 `ebc-auto governs wechat-macro-kb`，contract 指向上述文件。
3. **门禁脚本**：
   - 新增 `scripts/check_linkage_contract.py`，在联动任务中组合执行 `context_gate.py --enforce` 与 `project_impact.py --json`，作为 checkpoint 前的轻量监督入口。
4. **MAPM 职责同步**：
   - `MAPM/README.md` 将“数据规范 / 数据契约监督”明确纳入 MAPM 职责与能力表。
   - `MAPM/plan.md` / `MAPM/handoff.md` 同步当前接手状态。

**验证证据**：

- `python3 -m py_compile scripts/check_linkage_contract.py`
- `python3 scripts/governance_lint.py`
- `python3 scripts/project_impact.py wechat-macro-kb --json`
- `python3 scripts/check_linkage_contract.py --project wechat-macro-kb --task 'EBC directory split contract supervision'`

**风险 / 后续**：

- 当前 `governance_lint.py` 仍提示 3 个既有未引用 contract warning，与本轮 EBC 契约无关。
- 初版 linkage gate 先做本地 checkpoint 阻断；后续可再接入 pre-commit 或更强的 supervisor agent。

## 2026-05-22 Memory 使用方案落地（三层读取 + 五类 scope）

**目标**：

将云端记忆从"只写不读"升级为三层读取架构，让所有 agent 在关键时刻主动查询记忆。

**完成内容**：

1. **con-dev 增加 Memory Recall（Phase 2.5）**：
   - 在 Phase 3（读取项目上下文）前新增 Phase 2.5，搜索云端记忆补充跨设备上下文
   - 凭证类记忆（scope 含 credentials）优先展示，方便新设备快速获取服务器密码
   - Phase 5 就绪报告新增"云端记忆摘要"段
   - 规则：记忆与 handoff 矛盾时以 handoff 为准
2. **AGENTS.md 增加记忆使用规则**：
   - 读取规则：会话启动时、开始新任务前、遇到问题时、需要凭证时
   - 写入规则：checkpoint 时、重要决策时、排障解决时、凭证变更时
   - scope 四类：project / credentials / decision / troubleshoot
3. **checkpoint 增加 troubleshoot scope**：
   - 可选写入排障记录（问题 + 根因 + 解法 + 影响范围）
   - scope 列表从 3 类扩展到 4 类

**验证证据**：

- `curl http://43.133.86.33:3111/agentmemory/livez` → `{"status":"ok"}`
- `curl -X POST .../search -d '{"query":"server password credentials"}'` → score 14.64 命中凭证
- 云端记忆 28 条，覆盖 cloud-memory / MAPM / tradingcenter 三个项目

## 2026-05-21 MAPM 规范治理主项目重新梳理

**目标**：

- 把 MAPM 从“项目管理基础设施功能清单”重新梳理为 Jeff1993 的项目规范治理主项目。
- 对齐本地与仓库中的 `collab-entry`、通用 skill、`agent-kit`、独立 `mapm` 仓库和本机安装副本状态。

**完成内容**：

1. **MAPM 入口重写**：
   - `MAPM/README.md` 明确 MAPM 负责 `collab-entry.md`、`onboarding.md`、`onboarding-compact.md`、`agent-kit/`、通用 skill、项目注册表、治理脚本和跨设备同步约定。
   - 新增职责边界、当前真相源、资产地图、修改规则、能力表和验证命令。
2. **本地/仓库同步审计**：
   - 新增 `MAPM/docs/2026-05-21-mapm-source-sync-audit.md`。
   - 确认当前活跃真相源是 `jeff1993-docs/MAPM`。
   - 独立 `Jeff19930831/mapm` 仍存在，但 `main` 是脚本子集，`master` 是 2026-04 旧根仓快照，当前不作为规范治理单一真相源。
3. **项目注册表修正**：
   - `.project-status.yaml` 中 MAPM 的 `repo` 改为 `jeff1993-docs/MAPM`，独立 `mapm` 标为 legacy。
   - MAPM `sync` 新增 `governance-root`，覆盖 `collab-entry.md`、`onboarding*.md`、`AGENTS.md`、`agent-kit/`、`Skill/`、模板、contracts、SOP、collab-entry spec/plan 和治理脚本。
4. **通用 skill 源/安装副本收敛**：
   - `agent-kit/README.md` 新增“源与安装副本”合同。
   - `agent-kit/claude/skills/checkpoint/SKILL.md` 补齐 Memory Recall、MAPM 专用 collab-entry 同步、Memory Store。
   - `agent-kit/codex/skills/checkpoint-onboarding-ext.md` 补齐同等 Memory Hooks 说明。
   - 已同步安装副本到 `C:\Users\jiang\.agents\skills\checkpoint\SKILL.md` 和 `C:\Users\jiang\.codex\skills\checkpoint-onboarding-ext\SKILL.md`。
5. **Memory Hooks 安全口径修正**：
   - `collab-entry.md`、Claude/Codex checkpoint 源与本机安装副本统一为：默认写项目状态和 secret 引用，不默认写真实 secret payload。
   - 真实 payload 只有在认证、HTTPS、allowlist 和用户明确授权同时满足时才另行登记。

**验证证据**：

- `git fetch --all --prune`：远端引用已刷新。
- `git ls-remote https://github.com/Jeff19930831/mapm.git`：确认独立 `mapm` 仓库存在，`main` 与 `master` 指向不同提交。
- 临时克隆审计独立 `mapm` 的 `main` / `master`：确认 `main` 为脚本子集，`master` 为旧 MAPM 根仓快照。
- `python scripts/project_registry.py resolve MAPM`：解析到 `C:\Users\jiang\Documents\Jeff1993\MAPM`，`reason=current-device`。
- `python scripts/project_registry.py sync-list MAPM --summary`：`docs` 15 files，`governance-root` 50 files。
- `python scripts/project_registry.py lint MAPM`：通过，3 个 warning 仅为当前 MAPM 没有 `docs/runbooks/**/*.md`、`.env.example`、`config*.example.*`。
- `python scripts/governance_lint.py`：通过，4 个 warning 为既有未引用 contract。

**风险 / 后续**：

- 独立 `mapm` 仓库尚未处置，后续需要决定归档、保留为脚本包，或重新迁移为独立 canonical repo。
- 尚未新增 `agent-kit` dry-run 安装/比对脚本；目前通过手工同步源与本机安装副本。
- `cloud-memory` 仍需要 Phase 3 安全硬化：AGENTMEMORY_SECRET、HTTPS、备份。

## 2026-05-21 Cloud Memory + Checkpoint v3.8 Memory Hooks

**目标**：

- 部署云端 agentmemory 实现跨设备 AI 记忆共享。
- 将记忆调用 hook 集成到 checkpoint 流程，让每次 checkpoint 自动与云端记忆双向同步。

**完成内容**：

1. **cloud-memory 项目创建**：
   - agentmemory v0.9.21 + iii-engine v0.11.6 部署在腾讯云 Windows Server (43.133.86.33:3111)
   - 5 个 AI 工具 MCP 配置完成：Claude Code, Codex, Gemini CLI, OpenCode, ZCode
   - 完整文档：README / plan / progress / handoff（同步到 Obsidian + Jeff1993 文档仓）
   - 注册到 `.project-status.yaml`
2. **ZCode 配置体系调查**：
   - 确认 ZCode 没有独立 MCP 配置文件，共享 `~/.claude.json`
   - `.zcode\cli\config.json`（模型 provider）、`.zcode\agent\config.json`（活跃 agent 模型）
   - `.zcode\v2\acp-config\<agent>\<hash>\` 为 per-agent × per-project 隔离运行目录
3. **checkpoint 技能 v3.8 — Memory Hooks**：
   - 新增 Step 2.5 Memory Recall：每次 checkpoint 先搜索云端记忆获取跨设备上下文
   - 新增 Step 5.7 Memory Store：每次 checkpoint 写入项目状态摘要到云端
   - scope 分三类：`project:<name>` / `credentials:<name>` / `decision:<name>`
   - 私有环境允许写入 secret（服务器密码、API key）
   - 结束清单新增云端记忆检查项
4. **首次数据灌入**：
   - 写入 cloud-memory 凭证记忆（服务器 IP、密码、端口、启动方式）
   - 写入 cloud-memory 项目状态记忆
   - 首次 Memory Recall 验证通过（搜索 "cloud-memory server password" 返回凭证）

**验证证据**：

- `curl http://43.133.86.33:3111/agentmemory/livez` → `{"service":"agentmemory","status":"ok"}`
- `curl -X POST http://43.133.86.33:3111/agentmemory/search -d '{"query":"cloud-memory server password"}'` → 返回凭证记忆
- cloud-memory 文档已同步到 `Jeff1993/cloud-memory/` 并 push（commit 0fd3f25）
- checkpoint SKILL.md 已更新 Memory Recall + Memory Store 步骤

**风险 / 后续**：

- cloud-memory 服务当前未开启认证（无 AGENTMEMORY_SECRET），公网可直接访问
- 云端记忆中包含服务器密码（私有环境，用户授权）
- `.agents/` 不是 git 仓库，skill 更新无法通过 git 追踪

## 2026-05-21 Onboarding v3.7 长期运行知识 + Secret 引用同步

**目标**：

- 让功能配置方法、服务器接入、恢复步骤、密钥引用在跨设备接力时长期可见。
- 继续保持 secret payload 不进 Git，只同步引用和恢复步骤。

**完成内容**：

1. 新增长期运行知识层：
   - 项目内 `docs/runbooks/*.md` 放功能配置、服务器接入、故障恢复和 secret 引用卡片。
   - `onboarding.md` 新增 § 15，`collab-entry.md` 和 `onboarding-compact.md` 增加入口规则。
2. 新增模板和 allowlist：
   - `docs/templates/project/runbook.md`
   - `agent-kit/secrets/allowlist.yaml`（空 entries，仅登记路径和用途，不存真实值）
3. `con-dev` 规则更新：
   - 报告 runbook / example config 摘要。
   - 默认不读取全量 runbooks；只有 handoff / BOOTSTRAP / plan Active 明确指向时才读必要段落。
4. `checkpoint` 规则更新：
   - 新增 Step 5.5 长期运行知识同步。
   - 配置/服务器/secret 引用变更必须写入 runbook，并在 `progress.md` 追加 `[RUNBOOK]` / `[SECRET-REF]` 证据。
5. `.project-status.yaml:sync` 更新：
   - MAPM 与首批大项目增加 `docs/runbooks/**/*.md`、`.env.example`、`config*.example.*`。
6. Secret tracked exception:
   - `agent-kit/secrets/key.md` 经用户确认是真实 key 且系统必须保留 tracked。
   - 已在 `agent-kit/secrets/allowlist.yaml` 登记为 `classification: tracked-exception`、`risk_acceptance: user-approved`。
   - checkpoint 规则更新为精确匹配 allowlist 例外时允许继续, 但只报告路径和批准状态, 不读取/打印内容。

**验证证据**：

- `python scripts/project_registry.py lint MAPM`
- `python scripts/project_registry.py lint wechat-macro-kb`
- `python scripts/project_registry.py lint`
- `git diff --check`

**风险 / 后续**：

- tracked secret exception 是用户明确授权的便利模式, 不是默认安全最佳实践。后续任何报告仍只能写路径和状态, 不得读取或打印 `key.md` 内容。

## 2026-05-21 Onboarding v3.6 多设备路径 + 大项目同步清单

**目标**：

- 解决不同设备接力开发时不知道本地项目地址的问题。
- 解决首批大项目需要同步文件越来越多、但清单不机器可读的问题。

**完成内容**：

1. `.project-status.yaml` schema 扩展：
   - `code_paths`: 按 device / user / os 登记多设备本地路径，旧 `code_path` 保留为 fallback。
   - `sync`: 登记项目需要跨设备保持可见的 docs/code 文件集合和 required 文件。
2. 新增 `scripts/project_registry.py`：
   - `resolve <project>`：解析当前设备应使用的代码路径。
   - `sync-list <project> --summary`：展开同步清单摘要。
   - `lint [project]`：校验路径和同步清单。
3. `con-dev` 接入：
   - Claude skill 源 `agent-kit/claude/skills/con-dev/SKILL.md` 增加 Phase 2 路径解析和 sync summary。
   - Codex 镜像 `agent-kit/codex/skills/con-dev-onboarding-ext.md` 增加同等规则。
4. 首批项目登记：
   - MAPM: 当前 JEFFASUS 路径 `C:\Users\jiang\Documents\Jeff1993\MAPM`，保留旧 `D:\ClaudeCode\MAPM\` 为 reference。
   - wechat-macro-kb: 登记 Mac 主路径与 docs/code 同步清单。
5. 规则文档同步：
   - `collab-entry.md` 升级 v3.6。
   - `onboarding.md` 新增 § 14。
   - `onboarding-compact.md` 增加关键引用。
   - `MAPM/onboarding-suite` 升级 v1.1。

**验证证据**：

- `python3 scripts/project_registry.py lint MAPM`
- `python3 scripts/project_registry.py lint wechat-macro-kb`
- `python3 scripts/project_registry.py resolve MAPM`

---

## 2026-05-16 Governance 查询化与门控闭环（6 点全部完成）

**目标**：

- 把此前确认的 6 点从“方案”推进到“可执行机制”：关系可查、影响可查、checkpoint 可校验、上下文可门控、主会话可约束、文档语义可入图。

**完成内容**：

1. **治理脚本三件套落地**：
   - `scripts/governance_lint.py`：校验 `relations` 目标与 `docs/contracts/*` 结构
   - `scripts/build_governance_graph.py`：生成 `var/governance_graph.json`
   - `scripts/project_impact.py`：输出 `consumes/consumed_by/governs/governed_by` + 契约影响面
2. **主会话门控脚本落地**：
   - `scripts/context_gate.py` 新增
   - 自动判定 `fast/balanced/full`，并在 `--enforce` 下先跑治理检查；`full` 档位强制先做 impact
3. **文档语义边入图**（第 6 点补完）：
   - `build_governance_graph.py` 新增自动抽取边：
     - `links_to`（文档指向 contract）
     - `records_change`（`[CONTRACT-CHANGE: ...]`）
     - `records_adapt`（`[CONTRACT-ADAPT: ...]`）
4. **impact 输出增强**：
   - `project_impact.py` 新增：
     - `Docs linking contracts`
     - `Docs recording CONTRACT-CHANGE`
     - `Docs recording CONTRACT-ADAPT`
5. **规则文档同步**：
   - `Skill/checkpoint.md` 接入 governance lint
   - `collab-entry.md` / `onboarding.md` / `docs/contracts/README.md` 接入工具顺序与门控用法

**验证证据**：

- `python3 scripts/governance_lint.py` → `OK: governance relations/contracts passed (0 warning(s))`
- `python3 scripts/build_governance_graph.py` → `nodes=228 edges=221`
- `python3 scripts/project_impact.py wechat-macro-kb` → 正确显示 `hermes-governance` 下游与契约引用
- `python3 scripts/context_gate.py --project wechat-macro-kb --task cross-project-contract-change --enforce` → 自动判为 `full` 并执行治理检查链路

**提交记录**：

- `53f3c50` Design queryable governance for collab-entry relations
- `8ceccb1` Make collab-entry governance queryable and enforceable
- `ecc0514` Complete governance workflow with context gate and doc semantics

---

## 2026-05-15 v3.5 L4 全局辅助登记 + L5 跨项目关系层

**根因**：

- 四文档模型（README/plan/progress/handoff）覆盖单仓库、单消费方场景够用；wechat-macro-kb 这类**多消费方、跨仓库、长生命周期**项目已"漏水"（plan.md 1519 行、handoff 双份、跨项目耦合无主）。
- collab-entry 文档地图过时：`docs/specs/` / `docs/proposals/` / `docs/health-reports/` / `docs/backups/` / `docs/superpowers/` 实际存在但未登记；`docs/sop/` 在 v3.2 提到但实际未落地。
- 三个跨项目耦合痛点已多次发生：上游改下游不知 / "谁负责"模糊 / 跨仓库变更难追溯（hermes-governance ↔ wechat-macro-kb）。

**完成内容**：

1. **L4 全局辅助正名**：collab-entry.md `## 2. 文档地图` 节新增"全局辅助文档 (docs/)"表，登记 8 个目录（其中 `docs/sop/` 与 `docs/contracts/` 本次落地，其他正名）
2. **L5 跨项目关系新增**：
   - `.project-status.yaml` 扩展 `relations` 字段，类型 `consumes` / `governs`，每条边可选 `contract` 指针
   - 设计原则：**单边声明，反向派生**（consumed_by / governed_by 不写回 YAML，由 dashboard 脚本反查生成，避免双份漂移）
   - 字段约束：`project` 必须是 YAML 已存在 key、`purpose` 给人看、`contract` 可选
3. **契约文档规约（`docs/contracts/`）**：
   - 命名 `<声明方>--<对方>.md`（与 YAML 方向一致，不字母序）
   - 5 段模板：双方 / 接口表面 / 边界（谁动谁负责）/ 变更协议（轻量约定）/ Lore
   - 高门槛升级（接口 > 3 / 联动 ≥ 2 次 / 边界不直观才写契约，否则只 YAML 登记）
4. **onboarding.md § 13 新增**：8 小节，含 schema、关系类型表、模板、变更工作流（`[CONTRACT-CHANGE]` / `[CONTRACT-ADAPT]` / `[LINK]` 标记约定）、反向派生说明、与 archive 归档语义区分
5. **onboarding-compact.md**：关键引用表加行指向 § 13（不复制内容）
6. **collab-entry.md → v3.5**：版本头 + 文档地图重组 + L5 段
7. **首个契约落地**：`docs/contracts/hermes-governance--wechat-macro-kb.md`（49 行）—— hermes-governance 作为 consumer 声明，记录 MCP/HTTP/CLI 接口表面 + 边界（谁改 MCP 工具实现归 wechat-macro-kb / 谁改 profile 白名单归 hermes-governance）+ 5-13 profile-aware tool filtering Lore
8. **两个项目 relations 登记**：
   - `wechat-macro-kb.relations.consumes`: mysteel-mcp / ebc-auto / iron-ore-intel / crawl4ai-mcp
   - `hermes-governance.relations.consumes`: wechat-macro-kb (+ contract) / mysteel-crawl
   - `hermes-governance.relations.governs`: hermes-agent

**验证证据**：

- YAML 解析通过，43 项目无报错（`yaml.safe_load`）
- `relations` 字段在 wechat-macro-kb / hermes-governance 两个 entry 都存在且结构正确
- onboarding.md § 13 八小节齐全（13.1-13.8）
- collab-entry.md v3.5 版本头 + L4 表 + L5 段全部到位
- 契约文件 49 行（< 200 上限），5 节齐全
- `update-dashboard.py` + `update-overview.py` 跑 43 项目无报错（兼容新 schema）

**文件变更**（按 commit 分组）：

- **c7e3515** `[CHECKPOINT] collab-entry: v3.5 — L4 register + L5 cross-project relations`
  - 修改：`collab-entry.md` / `onboarding.md` / `onboarding-compact.md` / `.project-status.yaml`
  - 新建：`docs/sop/README.md` / `docs/contracts/README.md` / `docs/contracts/hermes-governance--wechat-macro-kb.md` / `dev-log/2026-05-15.md`（追加段）
- **3399e6f** `[CHECKPOINT] wechat-macro-kb: register Jeff1993 v3.5 cross-project relations`
  - 修改：`wechat-macro-kb/README.md`（关联项目段加契约指针）+ `wechat-macro-kb/PROGRESS.md`（顶部加 05-15 条目）
- **4d9fcf4** `[CHECKPOINT] hermes-governance: register Jeff1993 v3.5 cross-project relations`
  - 修改：`hermes-governance/README.md`（关联项目表加契约列）+ `hermes-governance/PROGRESS.md`（顶部加 05-15 条目）
  - 联动锚定：`[LINK: collab-entry@c7e3515, wechat-macro-kb@3399e6f]`
- **a164562** `[dashboard] regenerate after v3.5 relations field added`
  - 修改：`README.md`（根 dashboard）+ `项目总览.md`

**Follow-ups（不在本次范围）**：

- `update-dashboard.py` / `update-overview.py` 增加 `relations` 反向派生 + 关系矩阵渲染
- `/checkpoint` 加 lint：`relations` 目标存在、contract 文件存在、文件名大小写一致性（本次 wechat-macro-kb PROGRESS.md 大小写问题发现）
- wechat-macro-kb plan.md PRD 归档拆分（独立任务）
- wechat-macro-kb handoff.md 双份合一（Jeff1993 vs code repo `docs/` 各一份）

**spec / plan 文件**：

- spec: `docs/superpowers/specs/2026-05-15-collab-entry-v3.5-design.md` (87e723d)
- plan: `docs/superpowers/plans/2026-05-15-collab-entry-v3.5-implementation.md` (feb51c6)

---

## 2026-05-14 v3.4 行为准则 + CLAUDE.md 统一升级

**完成内容**：
- 精简 `~/CLAUDE.md`：去除与 `~/.claude/CLAUDE.md` 重复的项目管理段落（4573→2967 bytes, -35%）
- 引入 Karpathy 四原则（先想后做/极简主义/手术式修改/目标驱动）到 `~/.claude/CLAUDE.md`（540→1353 bytes）
- 行为准则融入 onboarding 三文件：
  - `onboarding-compact.md`：超简版 4 条（+434 bytes）
  - `onboarding.md`：新增 § 2.5 完整版（v3.2.1→v3.4）
  - `collab-entry.md`：v3.3→v3.4 版本记录
- 评估 Ruflo 多 Agent 编排平台：结论为不推荐（与当前减上下文目标冲突）

**验证证据**：
- 全局系统占用：7488→6735 bytes（净减 753 bytes, -10%）
- 行为准则从 Karpathy 原版 800 bytes 压缩到 ~600 bytes
- 三层递进：~/.claude/CLAUDE.md（设备级）→ onboarding-compact（跨设备超简）→ onboarding.md § 2.5（完整）

**文件变更**：
- 修改：`~/CLAUDE.md`（去重精简）
- 修改：`~/.claude/CLAUDE.md`（+行为准则）
- 修改：`~/Documents/Jeff1993/onboarding-compact.md`（+行为准则超简版）
- 修改：`~/Documents/Jeff1993/onboarding.md`（+§ 2.5, v3.4）
- 修改：`~/Documents/Jeff1993/collab-entry.md`（v3.4）

## 2026-05-13 con-dev 上下文优化

**完成内容**：
- 创建 `onboarding-compact.md`（1.4KB），替代 collab-entry.md + onboarding.md 的 22KB 每次对话加载
- 修改 `~/.claude/CLAUDE.md` 的 `@` 引用，从完整版切换到 compact 版
- 重写 `~/.claude/skills/con-dev/SKILL.md`（3.9KB，原 7.7KB），加入精准读取指令

**验证证据**：
- 全局层：22KB → 1.4KB（省 ~5.3K tokens/每次对话）
- Skill 层：7.7KB → 3.9KB（省 ~1K tokens）
- 项目层 BOOTSTRAP 模式：~43KB → ~6.7KB（省 ~9K tokens）
- 总计节省 ~15K tokens

**文件变更**：
- 新建：`~/Documents/Jeff1993/onboarding-compact.md`
- 修改：`~/.claude/CLAUDE.md`（@ 引用切换）
- 修改：`~/.claude/skills/con-dev/SKILL.md`（精准读取 + 精简）

## 2026-05-12 Onboarding v3.2 两层 Handoff 模型落地

- handoff.md 分为 🟢 常驻层 + 🟡 任务层
- docs/sop/ 全局约定 + dump_state.sh 鼓励规范
- 参考实现：wechat-macro-kb

## 2026-05-12 Onboarding Suite v1.0 设计与落地

- design.md + adoption.md + 4 模板 + 2 脚本
- 3 个新 Claude skills + 2 个扩展 + 5 个 Codex 镜像
- collab-entry.md v3.1 + onboarding.md v3.1 全局补丁
## 2026-05-29 MAPM handoff 轻量化改造

**目标**：

- 让 handoff 维持短入口，只保留接手所需的最小状态。
- 把失败尝试、session/test/diff、历史计划和重复问题分层到 progress / runbook / archive / evidence pointers。

**完成内容**：

1. 新增轻量化设计文档：`MAPM/docs/2026-05-29-handoff-lightweight-enhancement.md`。
2. 更新标准模板：`docs/templates/project/handoff.md` 加入 `不要重复` / `Evidence Pointers` / 行数预算。
3. 更新 MAPM 入口：`MAPM/handoff.md` 改为短接手入口，保留指针，不贴全文。
4. 新增脚本：
   - `scripts/handoff_draft.py`：dry-run 起草 handoff，不自动覆盖。
   - `scripts/md_health.py`：阻断过长 handoff、transcript-like 内容、过多 `不要重复` / `Evidence Pointers`。
   - `scripts/archive_md_sections.py`：继续保持 dry-run first。
5. 更新 onboarding bootstrap 规则，明确 handoff 目标 ≤100 行、硬上限 150 行。

**验证证据**：

- `python3 -m unittest MAPM.tests.test_doc_lifecycle -v`

**风险 / 后续**：

- 机器可读 envelope 仍预留未落地，后续若实现 `.mapm/handoffs/*.json`，必须只通过 `Evidence Pointers` 链接，不回灌全文。

## 2026-05-29 同设备 session-handoff skill 设计与落地

**目标**：

- 为同设备切 session 提供比 con-dev 更轻的续接方式。
- 保持跨设备重接手仍然由 con-dev 负责。

**完成内容**：

1. 新增轻量 skill：`agent-kit/claude/skills/session-handoff/SKILL.md` 与 `agent-kit/codex/skills/session-handoff.md`。
2. 新增脚本：`scripts/session_handoff_draft.py`，只读 handoff/plan/git 摘要并输出 dry-run 续接包。
3. 更新 skill 索引与安装清单，纳入 Codex skill 同步列表。
4. 更新 MAPM 能力表与 handoff 索引，明确 `session-handoff` 与 `con-dev` 的分工。

**验证证据**：

- `python3 -m unittest MAPM.tests.test_doc_lifecycle -v`

**风险 / 后续**：

- `session-handoff` 只适合同设备切换；跨设备或冷启动仍应走 `con-dev`。

### Checkpoint closure — 2026-05-29

**完成内容**：

- MAPM handoff 轻量化与 `session-handoff` 同设备续接 skill 已完成验证。
- `MAPM/plan.md` 中对应 Active 项已标记完成。

**验证证据**：

- `python3 -m unittest MAPM.tests.test_doc_lifecycle -v` → OK, 7 tests
- `python3 scripts/md_health.py --project-root MAPM --project MAPM` → no findings
- `python3 scripts/archive_md_sections.py --project-root MAPM --project MAPM` → No archival moves proposed
- `python3 scripts/handoff_draft.py --project-root MAPM --project MAPM` → dry-run, no files changed
- `python3 scripts/session_handoff_draft.py --project-root MAPM` → dry-run, no files changed
