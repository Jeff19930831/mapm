# Agent Onboarding — Jeff1993 接力开发规则

> 版本: v3.14 / 2026-06-11
> 首读入口：[`collab-entry.md`](collab-entry.md)
> v3.1 改动: 新增 § 12 大型项目附加层规则。
> v3.2 改动: handoff.md 两层模型（🟢 常驻层 + 🟡 任务层）；新增 docs/sop/ 全局约定；dump_state.sh 鼓励规范。
> v3.2.1 改动: 明确 Codex skill 安装必须使用目录式 `~/.codex/skills/<name>/SKILL.md`；根目录 `*.md` 仅作源/通用 Markdown, 不会被当前 Codex 自动识别。
> v3.12 改动: skill 默认安装目标统一为跨工具通用目录 `~/.agents/skills/<name>/SKILL.md`；仅当目标客户端不扫描通用目录时才回退到专用目录（如 `~/.claude/skills` 或 `~/.codex/skills`）。MCP 默认写各客户端自己的官方用户级配置。
> v3.4 改动: 新增 § 2.5 行为准则（Karpathy 四原则），统一跨设备跨 Agent 编码行为规范。
> v3.5 改动: 新增 § 13 跨项目关系 (L5)，用 `.project-status.yaml:relations` + `docs/contracts/` 管理消费/治理耦合。
> v3.6 改动: 新增 § 14 项目注册表扩展，支持 `code_paths` 多设备路径和 `sync` 大项目同步清单。
> v3.7 改动: 新增 § 15 长期运行知识与 secret 引用规则，支持配置方法、服务器信息、密钥引用的长期同步。
> v3.9 改动: 新增 § 16 Doc Lifecycle Gate。入口文档只放当前接手与常驻问题雷达，历史信息归档到 progress/archive，runbook 承载常见问题处理步骤；所有 onboarding 和 skill 均遵守此规则。
> v3.10 改动: 新增 § 17 项目联动协同与监督。跨项目/跨模块产物变更必须检查上下游、contract/runbook 和验证证据，checkpoint 可阻断不完整联动。
> v3.11 改动: 明确小写四文档为当前写入目标；旧大写文件只作兼容读取或历史镜像，不得覆盖小写当前入口。
> v3.14 改动: 重划 `session-handoff` / `con-dev` / `checkpoint` 三种接力流程；CodeGraph 作为本地开发雷达，CODEMAP 作为 durable onboarding 地图；checkpoint 默认本地收口，push/deploy 需明确授权。

## 1. 身份确认

每个 Agent 启动后先确认：

1. 当前设备与用户名。
2. 当前工具：`claude` / `codex` / `kimi` / 其他（见 owner 枚举）。
3. 当前 Jeff1993 根目录，例如 `C:\Users\jiang\Documents\Jeff1993` 或 `/Users/apple/Documents/Jeff1993`。
4. 目标项目目录和对应 `.project-status.yaml` 条目；若条目含 `code_paths`，确认当前设备匹配的是哪一条。

**Owner 枚举**：`claude` / `codex` / `kimi` / `unassigned`。按工具区分，不区分设备。

不要仅凭旧 `agent-onboarding-guide.md` 判断规则；该文件现在是迁移附录。

## 2. 启动读取顺序

1. 全局：`collab-entry.md`。
2. 全局：`onboarding.md`。
3. 项目：若存在 `scripts/dump_state.sh`，**先运行它**获取实时状态快照。
4. 项目：`handoff.md` 的 Persistent / Current Takeover；不存在则读 `HANDOFF.md`。
5. 项目：`plan.md` 的 Active 区；只在需要排期时读 Next。
6. 项目：`README.md` 的定位、架构、运行段。
7. 必要时才读 `progress.md` / `PROGRESS.md` / `progress/YYYY-MM.md` / `archive/**` 查历史证据。

## 2.5 行为准则（Karpathy 四原则）

**偏向谨慎而非速度。琐碎任务用判断力，非琐碎任务严格遵循。**

### 1. 先想后做
- 不确定就问，不要静默假设
- 多种理解时列出选项，不替用户选
- 有更简单的方案就说出来
- 不懂就停，说出困惑点

### 2. 极简主义
- 不加没要求的功能、抽象、配置
- 不为不可能发生的场景加错误处理
- 200 行能写成 50 行就重写

### 3. 手术式修改
- 只改必须改的，不顺手"改进"周围代码
- 匹配已有风格
- 注意到无关死代码只提不删
- 自己造成的孤儿代码（import/变量）必须清理

### 4. 目标驱动
- "加验证" → 写测试覆盖无效输入，让它通过
- "修 bug" → 写复现测试，让它通过
- 多步任务先列计划：步骤 → 验证方式

> 来源：[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)。

## 3. 每项目四文档职责

Doc Lifecycle Gate 是四文档的新基线：入口文档回答“现在怎么接手”，历史文档回答“以前为什么这么做”，runbook 回答“常见问题怎么安全处理”。详见 § 16。

- `README.md`：稳定范围、背景、架构、运行方式、链接。不是实时任务列表。
- `plan.md`：Active / Next / Archived Plans。未完成事项和归档索引放这里；Completed 历史不要长期堆在这里。
- `progress.md` / `progress/YYYY-MM.md`：已完成事实和验证证据。旧 handoff 完成批次、checkpoint 证据、月度历史放这里。
- `handoff.md`：Persistent / Current Takeover / Index。只放项目不变量、常驻问题雷达、当前目标、下一步、阻塞、验证和关键链接；旧完成记录不得长期堆积。
- `archive/**`：旧方案、长评审、退役计划、历史 checkpoint 原文等需要追溯但不应冷启动读取的内容。

**docs/sop/ 目录约定**（全局）：跨项目通用操作规程可放 `docs/sop/<name>.md`。项目内重复问题优先放 `docs/runbooks/*.md`。handoff 只保留指针。

**docs/runbooks/ 目录约定**（项目内）：长期会反复用到的功能配置方法、服务器接入说明、故障恢复步骤、密钥引用卡片，放在项目 `docs/runbooks/*.md`。handoff / README 只保留入口链接。

**dump_state.sh 规范**（鼓励）：大型项目建议提供 `scripts/dump_state.sh`，Agent 启动时运行，输出进程/任务/数据统计/open TODOs 实时快照。

标准模板位于 [`docs/templates/project/`](docs/templates/project/)。新建项目时从模板复制。

兼容期至 **2026-06-30**：旧项目可继续读取 `PROGRESS.md` / `HANDOFF.md`；若已存在小写 `progress.md` / `handoff.md`，小写文件是当前写入目标，大写文件只作历史镜像，不得反向覆盖。

## 4. 解析规则（resolver）

### handoff

1. 若 `.project-status.yaml:last_handoff` 指向存在的文件，优先使用该文件。
2. 否则若 `handoff.md` 存在，使用 `handoff.md`。
3. 否则若 `HANDOFF.md` 存在，使用 `HANDOFF.md`。
4. 都不存在时，从 [`docs/templates/project/handoff.md`](docs/templates/project/handoff.md) 复制并创建，不要删除旧文件。

### progress

1. 若 `progress.md` 存在，使用 `progress.md`。
2. 否则若 `PROGRESS.md` 存在，使用 `PROGRESS.md`。
3. 都不存在时，从模板创建 `progress.md`。

### plan

新模型要求 `plan.md`。旧项目若没有 `plan.md`，先从 README/PROGRESS/HANDOFF 中提取当前未完成事项，创建轻量 `plan.md`。

## 5. Plan ↔ Progress 动态同步

- `plan.md` 管"要做什么/正在做什么"。
- `progress.md` / `progress/YYYY-MM.md` 管"已经做完什么/证据是什么"。
- 每完成一个 plan item：
  1. 从 `plan.md` Active 移除或移入 Archived Plans 索引。
  2. 在 `progress/YYYY-MM.md` 或 `progress.md` 增加 checkpoint 记录，含验证证据。
  3. 在 `handoff.md` 更新 Current Takeover 和 Index。
- 完成即同步，避免 plan/progress 重复或过期；长历史不要留在入口文档。

## 6. Checkpoint 规则

执行 `/checkpoint` 或等效收工时：

Checkpoint 的输出是 durable closeout：验证证据、短入口文档、可提交状态。默认是本地收口，不自动 push/deploy；publish 行为需要用户本轮明确授权或项目策略允许。

1. 检查 Git/Obsidian 冲突标记；有冲突先停止。
2. 运行最小有效验证；涉及共享行为时扩大测试范围。
3. 可选使用本地 CodeGraph 做调用链/影响面复核；`.codegraph/` 不入 Git。
4. 执行 Doc Lifecycle Gate：入口短、历史归档、重复问题 runbook 化。
5. 更新 `plan.md` Active / Next / Archived Plans、`progress/YYYY-MM.md` 或 `progress.md`、`handoff.md` Persistent / Current Takeover / Index。
6. 若本次工作引入新的常驻服务/进程/集成，同步更新 `handoff.md` Persistent Context 和对应 `docs/runbooks/<name>.md`（跨项目通用规程才放 `docs/sop/`）。
7. 若本次工作新增/修改长期配置方法、服务器接入、密钥引用或恢复步骤，同步更新项目 `docs/runbooks/*.md` 或 `agent-kit/secrets/allowlist.yaml`；只写引用和恢复步骤，默认不写真实 payload。
8. 若本次涉及联动契约变更，执行项目联动协同检查：识别上游/下游，更新 contract/runbook，运行最小联动验证；未完成则不得标记完成。
9. 若项目启用 `docs/onboarding/`，运行 `scripts/refresh_codemap.py` 和 `scripts/check_onboarding.py`；修复 `<待填>`、缺 module-card、ADR index stale 后重跑。
10. 仅在稳定信息变化时更新项目 `README.md`。
11. 写入当日全局 `dev-log/YYYY-MM-DD.md`（位于 Jeff1993 根目录，不是项目子目录）：
   - 写入前先扫描是否已有 `## <项目名>` 区块；有则合并，无则追加。
12. 仅在生命周期/owner/path/status/明确迁移 `last_handoff` 时更新 `.project-status.yaml`。
13. 运行 secret gate：列出疑似 secret payload 路径，不打印值；私有仓策略允许时为警告，否则按项目策略阻断。
14. commit 使用 `[CHECKPOINT] <项目名>: <摘要>` 前缀（可按项目习惯加入日期）。
15. `git push` / cloud deploy / production touch 只在 publish 模式或用户明确授权时执行；push 前 fetch，禁止非授权 force-push。

详细合同：[`agent-kit/claude/skills/checkpoint/SKILL.md`](agent-kit/claude/skills/checkpoint/SKILL.md)。

### 6.1 三种接力流程边界

| 流程 | 适用场景 | 写入边界 | 跨设备/云记忆 | CodeGraph / CODEMAP |
|---|---|---|---|---|
| `session-handoff` | 同设备切到新 session，需要一段可粘贴续接包 | 默认不改文件；有 `--output` 才写指定草稿 | 不查注册表、不拉云记忆 | 不初始化 CodeGraph，不刷新 CODEMAP |
| `con-dev` | 新设备/新会话接手老项目 | 读多写少；不 checkpoint、不 commit、不 push | 可同步 docs/代码仓，读取 cloud memory 摘要 | 可准备本地 CodeGraph；只按需 grep CODEMAP |
| `checkpoint` | 收工、交付、跨设备可信交接 | 更新 plan/progress/handoff/onboarding，commit | safe memory recall/store；push 需授权 | CodeGraph 做影响复核；CODEMAP 必须可提交刷新 |

## 7. agent-kit 同步规则

`agent-kit/` 是跨设备通用配置合同：

- `manifest.yaml`：声明允许同步的 skills/prompts/agents/commands/rules/plugins，以及 `skill_sync` 映射段。
- `codex/`：Codex 用户自定义 skills/agents/prompts 说明。
- `claude/`：Claude commands/rules/plugins 说明。
- `secrets/`：只放 secret 策略、allowlist 和 payload 政策；默认不放真实 payload。
- `bootstrap/`：初始化合同和脚本（`init-agent-contract.md`）。

用户级配置写入前必须备份；系统/内置 skills 默认不覆盖。

### 7.0 同步工具（自动化，优先使用）

`scripts/agent_kit_sync.py` — manifest 驱动、跨平台的 skill 同步器。

```bash
python3 scripts/agent_kit_sync.py                  # dry-run，查看漂移
python3 scripts/agent_kit_sync.py --apply          # 部署（覆盖前自动备份）
python3 scripts/agent_kit_sync.py --agent claude   # 只同步 claude 源
python3 scripts/agent_kit_sync.py --target zcode   # 只同步 zcode 目标
python3 scripts/agent_kit_sync.py --json           # 机器可读输出
```

映射由 `manifest.yaml` 的 `skill_sync` 段驱动（source_agents + targets + on_name_conflict）。改了仓库源 skill 后必须跑 `--apply` 同步安装副本。

### 7.1 Skill 安装格式（强约束）

默认优先安装到跨工具通用用户级目录：

```text
~/.agents/skills/<skill-name>/SKILL.md
```

如果目标运行时不扫描通用目录，再回退到该工具自己的目录式 skill。Codex fallback：

```text
~/.codex/skills/<skill-name>/SKILL.md
```

不要只把 `agent-kit/codex/skills/<name>.md` 复制到 `~/.codex/skills/<name>.md` 后就认为已安装；这些根目录 `*.md` 文件可作为源文档/通用 Markdown 复用，但**不会出现在当前 Codex 的 Skills 列表中**。

安装或同步 skill 时必须：

1. 为每个 skill 创建通用目录：`~/.agents/skills/<name>/`。
2. 将内容写入：`~/.agents/skills/<name>/SKILL.md`。
3. `SKILL.md` 顶部必须包含 YAML frontmatter，至少含 `name` 和 `description`。
4. 重启目标客户端后验证会话 Skills 列表是否出现该 skill。
5. 若未出现，再同步到客户端 fallback 目录（例如 Codex 的 `~/.codex/skills/<name>/SKILL.md`）并重启验证。

例：

```bash
mkdir -p ~/.agents/skills/checkpoint-onboarding-ext
cp ~/Documents/Jeff1993/agent-kit/codex/skills/checkpoint-onboarding-ext.md   ~/.agents/skills/checkpoint-onboarding-ext/SKILL.md
```

若源文件本身没有 frontmatter，安装脚本必须补齐：

```yaml
---
name: checkpoint-onboarding-ext
description: "checkpoint 时追加 Jeff1993 onboarding 自检与双仓 push 规则。"
---
```


## 8. Secret 同步风险确认

本规范允许个人私有 secret 同步，是用户明确选择的便利模式，不是安全最佳实践。

> **2026-06-03 策略变更**：私有仓库允许明文 secret payload 进入 Git。原 `no tracked payload` 硬阻断取消，secret gate 降级为知情警告（扫描 + 列清单，不中止）。`no log values` / `backups are secrets` 仍保留。

硬规则：

- **default deny**：未在 allowlist 中的路径不复制。
- **opt-in**：不自动发现并复制 secrets。
- **payload allowed (private repo)**：私有仓允许明文 payload 进入 Git；`git ls-files` 命中仅**警告列清单**，不中止（原 no tracked payload 硬阻断已取消）。
- **no log values**：报告只写路径类别、计数、hash/checksum，不写内容。
- **dry-run first**：新增或修改 allowlist 后先 dry-run。
- **backups are secrets**：备份和恢复包继承同样的保密规则。
- **reference or payload (private repo)**：可同步 secret 名称/用途/位置/恢复步骤；私有仓也允许直接同步真实值（密钥/token/密码）。代价：git 历史不可逆 + Jeff1993 多设备扩散。

允许进入 Git 的内容：

- `.env.example`、`config.example.yaml`、脱敏配置片段。
- 项目 `docs/runbooks/*.md` 中的配置步骤、服务地址、端口、环境变量名称、secret 名称。
- `agent-kit/secrets/allowlist.yaml` 中的显式路径和用途说明。

~~禁止进入 Git 的内容~~ → 私有仓已放宽为「警告但允许」（2026-06-03，以下仍是高风险项，gate 会列清单提醒）：

- `.env`、`*.key`、`id_rsa`、真实 token / cookie / credential / auth cache。
- 未脱敏的服务器密码、API key、数据库连接串。
- 包含真实 secret 的备份包和恢复包。

## 9. 并发与冲突

- 不回滚其他 Agent 的改动。
- 同一文件冲突时先合并意图，再写入。
- 高冲突文件：`collab-entry.md`、`onboarding.md`、项目 `plan/progress/handoff`、`.project-status.yaml`。
- 若无法判断，写入 `handoff.md` 阻塞项并停止破坏性操作。

## 10. 结束清单

- [ ] 当前任务状态已写入 `plan.md`。
- [ ] 已完成内容和证据已写入 `progress.md`。
- [ ] 下一步和阻塞已写入 `handoff.md`。
- [ ] 长期配置/服务器/secret 引用变更已写入 `docs/runbooks/*.md` 或 secret allowlist，且未写入 payload。
- [ ] 当日进度已写入 `dev-log/YYYY-MM-DD.md`（合并规则已执行）。
- [ ] README/YAML 只在符合条件时更新。
- [ ] secret gate、冲突检查、验证命令已运行或说明未运行原因。
- [ ] checkpoint commit 可追踪，已 `git push`（如有远程）。

## 11. 新设备继续老项目流程

> 从 [`collab-entry.md § 4`](collab-entry.md#4-新设备--新-agent-初始化) 链接至此。

### 自动化方式（推荐）

安装好 Claude Code 和 `/con-dev` skill 后，直接运行：

```
/con-dev +<项目名>
```

例如：`/con-dev +MAPM`、`/con-dev +platts-data`、`/con-dev +ebc-auto`

skill 会执行冷启动接手并输出就绪报告。它不 checkpoint、不 commit、不 push、不重写 durable docs；手动执行时参考下方各阶段。

**Skill 安装位置**：`~/.agents/skills/con-dev/SKILL.md`（优先）；若客户端不扫描通用目录，再回退到 `~/.claude/skills/con-dev/SKILL.md`
**跨设备同步源**：`agent-kit/claude/skills/con-dev/SKILL.md`（随 jeff1993-docs git pull 到达）

安装步骤（新设备首次）：
```bash
mkdir -p ~/.agents/skills/con-dev
cp ~/Documents/Jeff1993/agent-kit/claude/skills/con-dev/SKILL.md ~/.agents/skills/con-dev/SKILL.md
# 若目标客户端不扫描 ~/.agents/skills，再同步到专用目录：
# mkdir -p ~/.claude/skills/con-dev && cp ~/Documents/Jeff1993/agent-kit/claude/skills/con-dev/SKILL.md ~/.claude/skills/con-dev/SKILL.md
```

---

### Phase 1：文档环境到位

```bash
# 1. 等待 Obsidian Sync 完成（确认 Jeff1993 目录已出现在新设备）
# 2. 确认 Git 状态
cd ~/Documents/Jeff1993
git status
```

若 Jeff1993 目录存在（Obsidian 先到）但尚未关联 Git 远程：

```bash
# 方式 A：覆盖式 clone（目录为空时）
git clone https://github.com/Jeff19930831/jeff1993-docs.git ~/Documents/Jeff1993

# 方式 B：目录已有 Obsidian 文件，仅挂载 .git
cd ~/Documents/Jeff1993
git init
git remote add origin https://github.com/Jeff19930831/jeff1993-docs.git
git fetch origin
git checkout -b main --track origin/main
# 如有冲突，手动合并后提交
```

```bash
# 3. 拉取最新状态
git pull
```

### Phase 2：定位目标项目

```bash
# 1. 读取项目注册表
cat .project-status.yaml | grep -A8 "<项目名>"
```

按注册表条目确认：

| 字段 | 动作 |
|---|---|
| `code_paths` 存在 | 先按当前设备 / 用户 / OS 解析 active 路径 |
| `repo` 有 GitHub 链接 | `git clone <repo_url> <resolved_code_path>` |
| `code_path` 是本地路径（无 repo）| 作为兼容 fallback；需从其他设备手动同步或重建 |
| `code_path` 为 `—` 且无 active `code_paths` | 纯文档项目，无需 clone |
| `last_handoff` | 读取对应 handoff 文件 |

```bash
# 2. 解析当前设备路径和同步清单
python3 scripts/project_registry.py resolve "<项目名>"
python3 scripts/project_registry.py sync-list "<项目名>" --summary

# 3. 克隆代码仓库（如有）
git clone https://github.com/Jeff19930831/<repo>.git <resolved_code_path>
```

### Phase 3：读取项目上下文

按顺序读取：

```
1. handoff.md（或 HANDOFF.md）— 最近状态、下一步、阻塞
2. plan.md — 当前任务列表
3. README.md — 架构、运行方式、依赖
```

### Phase 4：环境准备

按项目 `README.md` 的安装指引完成：

```bash
# 示例（Python 项目）
cd <code_path>
uv venv && uv pip install -r requirements.txt

# 示例（Node 项目）
pnpm install

# 示例（Go 项目）
go mod download
```

运行 `handoff.md` 中的验证命令，确认环境正常。

### Phase 4.5：本地 CodeGraph 准备（可选）

若当前项目代码量大、需要查调用链/影响面，且本机已安装 CodeGraph：

```bash
codegraph --version
codegraph init -i
```

规则：

1. `.codegraph/` 是本地索引和缓存，必须忽略，不作为同步清单或 checkpoint payload。
2. con-dev 只用 CodeGraph 做即时结构查询，例如入口链路、callers/callees、blast radius。
3. con-dev 不运行 `scripts/refresh_codemap.py`；CODEMAP 是 durable onboarding 地图，只在 checkpoint/refresh-onboarding/init-onboarding 中刷新。
4. 未安装 CodeGraph 不阻断接手；报告写明使用 `rg` / CODEMAP fallback。

### Phase 5：开始工作

```
1. 在 onboarding.md § 1 要求的身份信息中确认：工具名 + 设备 + Jeff1993 路径
2. 按 plan.md Active 区最高优先级任务开始
3. 同设备中断用 session-handoff，正式收工用 /checkpoint
```

### 快速检查清单

- [ ] Jeff1993 git pull 成功，无冲突
- [ ] 目标项目 handoff.md 已读
- [ ] 代码仓库已 clone 到 `project_registry.py resolve` 给出的当前设备路径
- [ ] 若项目条目有 `sync`，同步清单 required 文件齐全
- [ ] 依赖安装完成，验证命令通过
- [ ] 若使用 CodeGraph，确认 `.codegraph/` 未进入 Git / sync 清单
- [ ] 身份确认完成（工具 + 设备 + 路径）

## 12. 大型项目附加层 (LOC ≥ 10K 或源文件 ≥ 20)

### 12.1 何时启用

满足任一条件即建议启用:
- 代码 LOC ≥ 10,000
- 源文件数 ≥ 20
- 单文件 > 1,000 LOC

启用后在项目根增加 `docs/onboarding/` 子树, **不替换四文档**, 而是叠加。

### 12.2 五件套

| 文件 | 作者 | 触发 |
|---|---|---|
| `BOOTSTRAP.md` | 模型起草, 用户审改 | 项目接入时一次, 半年改一次 |
| `CODEMAP.md` | 脚本表 + 模型一行职责 | `refresh_codemap.py` 自动 |
| `module-cards/*.md` | 模型起草, 用户审 | 大模块出现/边界变化时 |
| `decisions/*.md` (ADR) | 模型起草 (对话决策), 用户审 | 关键词检测 / `/adr` 命令 |
| `decisions/INDEX.md` | 脚本自动 | `check_onboarding.py` 自动 |

### 12.3 Agent 启动协议 (强约束)

读取顺序与 token 上限:
1. `handoff.md` (动态状态, ~1KB)
2. `docs/onboarding/BOOTSTRAP.md` (静态入口, ~2-3KB)
3. 按 BOOTSTRAP § 3 场景跳转表按需展开 `module-cards/<X>.md` 或 `decisions/<id>.md`
4. **不读全 CODEMAP / 不读全 ADR**
5. 启动总预算 **≤ 5KB**, 与项目大小解耦

### 12.3.1 CODEMAP 与 CodeGraph 分工

- `docs/onboarding/CODEMAP.md` 是 durable、可提交、可 diff 的交接地图：文件、LOC、主要 symbol、imports、一行职责。
- CodeGraph 是本地开发雷达：symbol/call graph、caller/callee、影响面查询、MCP 查询。
- `.codegraph/` 不属于 onboarding 五件套，不进入 Git、不进入 `.project-status.yaml:sync`、不作为 checkpoint payload。
- 启动/接手时优先读 BOOTSTRAP 和 handoff；不读全 CODEMAP。只有要找文件职责时 grep CODEMAP，要查调用链时用 CodeGraph。
- checkpoint / refresh-onboarding 必须保证 CODEMAP 健康；CodeGraph 缺失不阻断 checkpoint。

### 12.4 决策识别 (模型行为约定)

对话中检测到以下关键词且选择影响 ≥ 2 个模块时, 模型应主动询问起草 ADR:
`决定 | 确定 | 就这么做 | 选这个 | 否决 | 改用 | 不做 MVP | 全量做 | 最终用 X | 不要 X 改 Y`

用户 y → 写 `decisions/NNNN-<slug>.md`
用户 n → 不写, 但 dev-log 当日条目留痕

### 12.5 启用与升级

| 操作 | Claude | Codex |
|---|---|---|
| 首次启用 | `/init-onboarding` | prompt "初始化 onboarding" |
| 升级小→大 | `/init-onboarding --upgrade` | prompt "升级 onboarding" |
| 中途刷新 | `/refresh-onboarding` | prompt "刷新 onboarding" |
| 手动起 ADR | `/adr [<slug>]` | prompt "记一下这个决定" |

详细规约: [`MAPM/onboarding-suite/docs/design.md`](MAPM/onboarding-suite/docs/design.md)
跨工具接入: [`MAPM/onboarding-suite/docs/adoption.md`](MAPM/onboarding-suite/docs/adoption.md)

### 12.6 与四文档关系

- 四文档 **基线**, 永远存在 (含小项目)
- onboarding/ 是大项目的**叠加层**, 不替换四文档
- handoff.md 仍是动态接力的主入口
- BOOTSTRAP.md 是**静态全景**入口 (跳转表 + 约定)
- 两者协同: handoff 说"现在在哪", BOOTSTRAP 说"地图怎么用"

## § 13. 跨项目关系 (L5)

> v3.5 新增。承载消费方、上下游、治理者-被治理者等跨项目耦合关系。

### 13.1 何时需要登记 relation

- 项目 A 在运行时**调用 / 读取 / 消费**项目 B 的产出（API / MCP / 文件 / 表 / 命令）
- 项目 A **治理 / 维护 / 配置**项目 B（如 hermes-governance ↔ hermes-agent）

### 13.2 何时升级到 contract 文档

YAML 登记是 baseline，contract 文档是**可选叠加**。满足以下任一条件才写 contract：

- 接口数量 > 3 个（综合 MCP / HTTP / CLI / 文件 / 数据格式）
- 历史上发生过 ≥ 2 次"联动变更"
- 边界归属不直观，需要文档化

### 13.3 YAML schema

每个项目的 entry 可选添加 `relations:`：

```yaml
<project_name>:
  # 现有字段全部保留 ...
  relations:                          # 新增，可选
    consumes:                         # 我消费谁
      - project: <upstream_project>   # 必须是 .project-status.yaml 已存在的顶层 key
        purpose: <一句话说清耦合内容>
        contract: docs/contracts/<file>.md   # 可选
    governs:                          # 我治理谁
      - project: <governed_project>
        purpose: <一句话>
        contract: docs/contracts/<file>.md   # 可选
```

### 13.4 关系类型（初版仅两种）

| 类型 | 语义 | 负责方约定 |
|---|---|---|
| `consumes` | 我依赖/消费上游项目的产出 | **下游（声明方）负责适配上游变更** |
| `governs` | 我负责治理另一个项目的运行态 | **治理方（声明方）负责被治理对象的状态** |

新关系类型（`peer_with`、`forks_from` 等）按需再加，不预设。

### 13.5 Contract 文档模板

`docs/contracts/<声明方>--<对方>.md`，5 段，~100-200 行：

```markdown
# 契约: <A> ↔ <B>

> 关系类型: consumes (A → B) | governs (A → B)
> 创建: YYYY-MM-DD · 最近修订: YYYY-MM-DD

## 1. 双方
- A (声明方, consumer/governor): <project> @ <repo>
- B (对方, producer/governed): <project> @ <repo>

## 2. 接口表面
B 暴露给 A 的接口清单（MCP / HTTP / CLI / 数据格式 / 文件约定）

## 3. 边界（谁动谁负责）
| 改动类型 | 归属方 |
|---|---|
| ... | A / B |

## 4. 变更协议（轻量约定，不强制）
- B 改接口前: progress.md 加 `[CONTRACT-CHANGE: <this-file>] ...`
- A 适配后: progress.md 加 `[CONTRACT-ADAPT: <this-file>] ...`
- 双方 commit 加 `[LINK: <other-project>@<sha>]`

## 5. Lore（可选）
设计依据 / 历史 gotcha / 不应再踩的坑
```

### 13.6 变更工作流

| 触发场景 | 动作 |
|---|---|
| 新增 / 调整一条关系 | 改 `.project-status.yaml` 的 `relations`；如够复杂，新建 `docs/contracts/<file>.md` |
| 上游接口变化（producer 侧）| progress.md 加 `[CONTRACT-CHANGE: <path>] ...`；commit 加 `[LINK: <consumer-project>@<sha>]` |
| 下游适配上游变化（consumer 侧）| progress.md 加 `[CONTRACT-ADAPT: <path>] ...`；commit 加 `[LINK: <producer-project>@<sha>]` |
| `/checkpoint` 流程 | v3.5 本次**不引入**自动校验，靠人/Agent 自觉。Follow-up: 加 lint 校验 `relations` 目标与 contract 文件存在 |

### 13.7 反向派生

`consumed_by` / `governed_by` **不写回 YAML**——由 `update-dashboard.py` / `update-overview.py` 反查派生。本次 schema 先就位，脚本侧增强为 follow-up。

### 13.8 与 archive: merged_into_X 的区别

`archive: merged_into_<project>` 是**历史归档**关系，不是活耦合，不归入 `relations`。relations 只描述当前运行时仍然存在的耦合。

### 13.9 Lint 与影响面查询（落地脚本）

在 `Jeff1993` 根目录执行：

```bash
python3 scripts/context_gate.py --project <project_name> --task "<任务描述>" --enforce
python3 scripts/governance_lint.py
python3 scripts/build_governance_graph.py
python3 scripts/project_impact.py <project_name>
python3 scripts/request_explorer.py --project <project_name> --task "<复杂跨项目任务>"
```

用途：
- `context_gate.py`：主会话门控。自动判定 `fast/balanced/full`，并在 `full` 档位下强制先跑 lint/build/impact，避免直接深探索。
- `governance_lint.py`：在 checkpoint 前发现 relation 目标缺失、contract 路径错误、contract 结构缺失。
- `build_governance_graph.py`：把 `relations` 和 `contracts` 生成 `var/governance_graph.json`，供后续查询工具消费。
- `project_impact.py`：查询项目的 `consumes` / `consumed_by` / `governs` / `governed_by`，并提示 `[CONTRACT-CHANGE]`、`[CONTRACT-ADAPT]` 写法。
- `request_explorer.py`：申请 explorer 的唯一入口。内部调用 `context_gate --enforce --request-explorer`，拒绝时返回码 `2`。

### 13.10 上下文读取档位（fast / balanced / full）

默认档位：`balanced`。

| 档位 | 场景 | 读取内容 |
|---|---|---|
| `fast` | 状态确认、小改动 | `onboarding-compact.md` + handoff Persistent/Current + `plan` Active |
| `balanced` | 常规开发 | fast + README 架构段 + `.project-status.yaml` 当前项目项 + `relations` |
| `full` | 跨项目联动/治理改动 | balanced + 相关 `docs/contracts/*` + `project_impact` 输出 + 最近 checkpoint 证据 |

主会话优先先跑 `project_impact` 做轻量查询；只有在跨仓库问题仍不清晰时再派 Explore/子 Agent 进入深度探索，避免重复扫描同一批文档。
执行上，深探索申请统一走 `request_explorer.py`，不允许绕过门禁直接派 explorer。

执行顺序建议：
1. `context_gate` 判档并输出读取范围。
2. 主会话按档位读取并完成轻量查询。
3. 若仍不清晰，再派 Explore/子 Agent 做深度探索，不重复扫描已由门控输出覆盖的内容。

## § 14. 项目注册表扩展：多设备路径与同步清单

> v3.6 新增。解决跨设备接力时本地项目地址不清、以及大项目需要同步文件越来越多的问题。

### 14.1 设计原则

- 旧字段 `code_path` 继续保留，作为兼容 fallback。
- 新字段 `code_paths` 是多设备路径登记，允许同一项目在 Windows / macOS / Linux、不同 Agent 下有不同本地路径。
- 新字段 `sync` 是项目级同步清单，只声明需要跨设备保持可见的文件集合；依赖目录、缓存、构建产物、临时数据默认排除。
- `code_paths` / `sync` 都只放在 `.project-status.yaml`；不要在 handoff 里维护第二份路径表。

### 14.2 YAML schema

```yaml
<project_name>:
  # 现有字段全部保留 ...
  code_path: <legacy_or_default_path>      # 兼容旧流程
  code_paths:
    - device: <hostname_or_alias>          # 如 JEFFASUS / mac-codex / default
      user: <domain\user_or_user>          # 可选，用于同设备多用户
      os: windows|darwin|linux             # 可选
      path: <local_project_path>
      status: active                       # active 默认；reference/retired 不作为当前工作目录
      note: <一句话说明>
  sync:
    include:                               # 默认基于 docs 目录
      - README.md
      - plan.md
      - progress.md
      - handoff.md
      - docs/**/*.md
    code:                                  # 可选，基于当前设备 resolved code path
      include:
        - src/**/*.py
        - tests/**/*.py
      exclude:
        - .venv/**
        - node_modules/**
        - __pycache__/**
    required:
      - README.md
      - plan.md
      - handoff.md
```

### 14.3 解析规则

`con-dev` 和手动接力都先运行：

```bash
python3 scripts/project_registry.py resolve <project_name>
python3 scripts/project_registry.py sync-list <project_name> --summary
```

路径选择优先级：

1. `code_paths` 中匹配当前 `device` / `user` / `os` 的 active 记录。
2. `device: default` 或 `*` 的 active 记录。
3. 本机真实存在的 active 路径。
4. 旧字段 `code_path`。

`status: reference|retired|archived|disabled|remote` 只用于保留历史线索，不作为 `cd` / `git clone` 目标。

### 14.4 大项目同步清单规则

大型项目（如 `wechat-macro-kb` / `tradingcenter`）必须显式登记 `sync`，至少覆盖：

- 四文档：README / plan / progress / handoff（含旧大写兼容文件）
- `docs/onboarding/**/*.md`
- 长期运行知识：`docs/runbooks/**/*.md`、`.env.example`、`config*.example.*`
- 关键配置：实验配置、字典、schema、路由表等
- 关键源文件：当前开发会频繁跨设备接力的 `src` / `tests` / `frontend/src`

不要登记：

- `node_modules/`
- `.venv/`
- `__pycache__/`
- `dist/` / `build/`
- 大型原始数据、缓存、临时输出；这些应由项目 README 或 handoff 指向重建/下载方式

### 14.5 Checkpoint 要求

当新增设备、移动代码仓、或发现 con-dev 找错路径时：

1. 更新 `.project-status.yaml` 的 `code_paths`，保留旧路径为 `status: reference`（若仍有历史价值）。
2. 运行 `python3 scripts/project_registry.py lint <project_name>`。
3. 若大项目新增关键文件类别，同步更新 `sync.include` / `sync.code.include`。
4. 若新增或移动的文档会让入口文档变长，先执行 Doc Lifecycle Gate：入口只留当前接手信息，历史内容移入 `progress/YYYY-MM.md` 或 `archive/**`。
5. checkpoint 报告中写明 resolved path、sync summary、以及是否触发文档归档。

## § 15. 长期运行知识与 Secret 引用

> v3.7 新增。解决功能配置方法、服务器接入方式、密钥位置等长期信息跨设备接力时丢失的问题。

### 15.1 分类

| 信息类型 | 放哪里 | 是否进 Git |
|---|---|---|
| 功能配置方法、参数含义、开关说明 | 项目 `docs/runbooks/<feature>.md` | 是 |
| 服务器地址、端口、服务名、验证命令 | 项目 `docs/runbooks/<service>.md` 或全局 `docs/sop/<service>.md` | 是，避免密码 |
| 环境变量名、secret 名称、用途、存放位置 | 项目 `docs/runbooks/<secret-ref>.md` 或 `agent-kit/secrets/allowlist.yaml` | 是，只放引用 |
| `.env.example`、脱敏 config 示例 | 项目根或 `config/` | 是 |
| 真实 `.env`、私钥、token、cookie、credential、auth cache | 用户指定的私有路径 / 密码管理器 / 加密包 | 否 |

### 15.2 Runbook 模板

项目内长期知识从 [`docs/templates/project/runbook.md`](docs/templates/project/runbook.md) 复制。核心字段:

- 用途。
- 配置文件、环境变量名、脱敏示例文件。
- Secret 引用表（名称 / 用途 / 存放位置 / 恢复方式）。
- 验证命令。
- 故障恢复。
- 变更记录。

### 15.3 Secret 引用卡片规则

密钥相关文档只允许写:

- secret 名称，如 `OPENAI_API_KEY`、`TENCENT_CLOUD_SECRET_ID`。
- secret 所属系统、用途、权限范围、轮换入口。
- 存放位置的描述，例如 "1Password / 项目名 / 条目名"、"Windows Credential Manager: <target>"、"服务器上 `/opt/app/.env`，不入 Git"。
- 恢复步骤和验证命令，但命令不得 echo/print secret value。

不得写:

- 真实值。
- 可逆编码后的值。
- 完整 cookie/session/auth cache。
- 私钥正文或数据库明文连接串。

### 15.4 con-dev 行为

`con-dev` 默认不读取所有 runbooks。它只做两件事：

1. 在就绪报告里列出 `sync` 中声明的 `docs/runbooks/**/*.md` 数量和 required 缺失项。
2. 当 `handoff` / `BOOTSTRAP` / `plan Active` 明确指向某个 runbook 时，只读取该 runbook 的必要段落。

### 15.5 checkpoint 行为

checkpoint 时若本次改动涉及配置、服务器、secret、部署或常驻服务：

1. 确认项目是否已有对应 `docs/runbooks/*.md`；没有则从模板创建。
2. 写入配置方法、恢复步骤、验证命令和 secret 引用。
3. 更新 `.project-status.yaml:sync.include`，确保大项目同步 `docs/runbooks/**/*.md` 和脱敏示例配置。
4. 运行 secret gate，列出疑似真实 payload 路径；是否阻断按项目 secret 策略执行，报告不得打印值。
5. 在 `progress.md` 记录 `[RUNBOOK]` 或 `[SECRET-REF]` 变更事实和验证证据。

### 15.6 迁移提醒

若发现已 tracked 的疑似 secret 文件（如 `*key*`、`*token*`、`credentials*`），不要读取内容；先判断是否是 payload。私有仓策略允许时可警告放行；不允许时停止提交、移出 Git 跟踪、轮换密钥，并在 `progress.md` 记录处理结果。

## § 16. Doc Lifecycle Gate

> v3.9 新增。解决 `handoff.md` / `plan.md` / onboarding 文档越写越长、历史信息淹没当前接手信息的问题。

### 16.1 核心分工

- 入口文档只回答：“我现在该怎么接手？”
- 历史文档回答：“以前为什么这么做？”
- Runbook 回答：“常见问题下次怎么安全处理？”

### 16.2 文档职责

| 文档 | 保留什么 | 不放什么 |
|---|---|---|
| `handoff.md` / `HANDOFF.md` | Persistent Context、常驻问题雷达、Current Takeover、Next、Blockers、Verification、Index | 多轮完成历史、长评审、旧计划全文 |
| `plan.md` | Active Plan、Next Plan、Archived Plans 索引 | 已完成流水账、旧方案展开、长期排障 SOP |
| `progress.md` / `progress/YYYY-MM.md` | 已完成事实、验证证据、checkpoint 摘要 | 当前接手步骤、未来计划 |
| `archive/**` | 旧计划、长评审、历史 checkpoint 原文、废弃方案 | 当前必须读取的信息 |
| `docs/runbooks/**` | 重复出现的问题、配置/部署/恢复步骤、secret 引用 | 一次性任务流水账、真实 secret payload |

### 16.3 触发条件

任一条件满足就执行清理或归档：

- `handoff.md` 超过 150 行，或 Current Takeover 需要滚动才能看完。
- `plan.md` 的 Completed/History 比 Active/Next 更长。
- 同一问题在 handoff/progress/dev-log 中重复出现两次以上。
- 某个部署、配置、secret、环境或常驻服务问题可能再次发生。
- onboarding / skill 文档开始复制项目历史，而不是给出通用规则。

### 16.4 处理步骤

1. 先分类：当前接手、常驻不变量、常见问题、已完成事实、历史原因。
2. 当前接手留在 `handoff.md`；常驻不变量保留在 Persistent Context。
3. 已完成事实移入 `progress/YYYY-MM.md`；只在 handoff 留一行链接。
4. 旧计划、旧评审、历史 checkpoint 原文移入 `archive/YYYY-MM-DD-<slug>.md`。
5. 重复出现的问题写成 `docs/runbooks/<topic>.md`，handoff 只保留问题名、风险、链接。
6. `plan.md` 只保留 Active / Next / Archived Plans 三段；Archived Plans 只放链接和一句话结论。
7. 清理后运行可用的健康检查：`scripts/md_health.py`、`scripts/archive_md_sections.py --dry-run`、`project_registry.py lint <project>`、secret gate。

### 16.5 Skill / Agent 要求

- `con-dev` 只读取 handoff 的 Persistent / Current Takeover，以及 plan 的 Active；只有被这些入口明确链接时才展开 progress、archive、decisions、runbooks。
- `checkpoint` 必须在写 handoff 前检查入口文档是否膨胀；膨胀则先归档，再刷新入口。
- `init-onboarding` 和 `refresh-onboarding` 必须生成或维护上述职责边界，不得把历史长文复制进入口。
- `adr` 只把决策正文写入 decisions；handoff 只保留链接和当前影响。
- 所有 skill 都应把“入口短、历史归档、常见问题 runbook 化”作为默认写入约束。

## § 17. 项目联动协同与监督

> v3.10 新增。解决上游目录/schema/接口变化后，下游脚本、定时任务或 Agent 消费路径未同步适配的问题。

### 17.1 什么算联动契约

当一个项目、模块、脚本、服务或定时任务的输出被另一个消费者使用时，二者之间形成“联动契约”。契约包括：目录结构、文件命名、Excel/CSV/JSON schema、数据库表字段、指标 slug/口径、HTTP/MCP/CLI 参数、cron 调度、产物路径、env/config/secret 引用和报警 freshness 阈值。

### 17.2 触发条件

任务描述或 diff 命中以下任一项，就按联动任务处理：上游/下游、目录拆分、schema/字段、接口/工具签名、指标/字典、定时任务、导入/下载/解析、配置/env/secret、contract、数据停更/freshness。

### 17.3 执行流程

1. 识别生产方、消费方、产物和契约文件。
2. 运行 `python3 scripts/context_gate.py --project <project> --task "<任务>" --enforce`，再按需运行 `project_impact.py <project>`。
3. 上游产物变化时同步检查下游解析/导入/报告/MCP/bot；下游解析变化时验证真实上游样本。
4. 复杂或重复发生的耦合写入 `docs/contracts/<声明方>--<对方>.md`；长期恢复步骤写入项目 `docs/runbooks/*.md`。
5. 至少运行一个最小联动验证：schema/header 检查、fixture 测试、真实样本导入、freshness SQL 或端到端 smoke test。
6. checkpoint 时在 producer 侧 progress 写 `[CONTRACT-CHANGE: <path>]`，consumer 侧 progress 写 `[CONTRACT-ADAPT: <path>]`，handoff 只保留当前风险和 contract/runbook 指针。

### 17.4 Linkage Supervisor

复杂联动任务结束前应执行监督检查，可由 verifier/critic/linkage-supervisor 角色完成。监督只审查，不实现。输出必须覆盖：

- Status: `pass` / `fail` / `needs-work`
- Upstream / Downstream / Contract
- 是否只改了一端
- 是否验证真实产物或 fixture
- 是否更新 contract/runbook/progress/handoff
- 阻断项

### 17.5 阻断条件

出现以下情况不得宣称完成或 checkpoint：

- 识别到联动契约变更，但没有影响面检查。
- 上游产物变化，但没有下游消费验证。
- 下游解析变化，但没有真实上游样本或 fixture。
- 重复发生的联动问题没有 contract/runbook。
- 数据存在但下游 freshness stale，却只归因“上游断供”。

### 17.6 禁止事项

- 禁止只改下载/爬虫脚本，不改导入/消费脚本。
- 禁止只看文件存在，不查核心指标最新日期。
- 禁止把联动排障结论只留在聊天里。
- 禁止把 secret payload 写入 contract/runbook/progress。
