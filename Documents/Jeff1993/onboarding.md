# Agent Onboarding — Jeff1993 接力开发规则

> 版本: v3.2.1 / 2026-05-12
> 首读入口：[`collab-entry.md`](collab-entry.md)
> v3.1 改动: 新增 § 12 大型项目附加层规则。
> v3.2 改动: handoff.md 两层模型（🟢 常驻层 + 🟡 任务层）；新增 docs/sop/ 全局约定；dump_state.sh 鼓励规范。
> v3.2.1 改动: 明确 Codex skill 安装必须使用目录式 `~/.codex/skills/<name>/SKILL.md`；根目录 `*.md` 仅作源/通用 Markdown, 不会被当前 Codex 自动识别。

## 1. 身份确认

每个 Agent 启动后先确认：

1. 当前设备与用户名。
2. 当前工具：`claude` / `codex` / `kimi` / 其他（见 owner 枚举）。
3. 当前 Jeff1993 根目录，例如 `C:\Users\jiang\Documents\Jeff1993` 或 `/Users/apple/Documents/Jeff1993`。
4. 目标项目目录和对应 `.project-status.yaml` 条目。

**Owner 枚举**：`claude` / `codex` / `kimi` / `unassigned`。按工具区分，不区分设备。

不要仅凭旧 `agent-onboarding-guide.md` 判断规则；该文件现在是迁移附录。

## 2. 启动读取顺序

1. 全局：`collab-entry.md`。
2. 全局：`onboarding.md`。
3. 项目：若存在 `scripts/dump_state.sh`，**先运行它**获取实时状态快照。
4. 项目：`handoff.md` **🟢 常驻层**（了解设施全貌）→ **🟡 任务层**（了解当前接力）；不存在则读 `HANDOFF.md`。
5. 项目：`plan.md`。
6. 项目：`README.md`。
7. 必要时读 `progress.md` / `PROGRESS.md` 查历史证据。

## 3. 每项目四文档职责

- `README.md`：稳定范围、背景、架构、运行方式、链接。不是实时任务列表。
- `plan.md`：当前和未来任务。未完成事项只放这里。
- `progress.md`：已完成事实和验证证据。完成后才写这里。
- `handoff.md`：**两层结构**：
  - **🟢 常驻层**（文件顶部，半永久）：运行中服务、进程、集成设施的列表 + `docs/sop/` 指针。不随任务迭代覆盖，改一次活半年。
  - **🟡 任务层**（常驻层之后，短期）：当前目标、最近完成、下一步、阻塞点。每次 checkpoint 刷新。

**docs/sop/ 目录约定**（全局）：每个常驻设施的操作步骤超过 5 行时，独立成 `docs/sop/<name>.md`。handoff 常驻层只保留指针。

**dump_state.sh 规范**（鼓励）：大型项目建议提供 `scripts/dump_state.sh`，Agent 启动时运行，输出进程/任务/数据统计/open TODOs 实时快照。

标准模板位于 [`docs/templates/project/`](docs/templates/project/)。新建项目时从模板复制。

兼容期至 **2026-06-30**：旧项目可继续使用 `PROGRESS.md` / `HANDOFF.md`；之后统一迁移为小写。

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
- `progress.md` 管"已经做完什么/证据是什么"。
- 每完成一个 plan item：
  1. 在 `plan.md` 标记完成或移入 Completed/Archived 区。
  2. 在 `progress.md` 增加 checkpoint 记录，含验证证据。
  3. 在 `handoff.md` 更新下一步。
- 不按时间周期批量归档；完成即同步，避免 plan/progress 重复或过期。

## 6. Checkpoint 规则

执行 `/checkpoint` 或等效收工时：

1. 检查 Git/Obsidian 冲突标记。
2. 更新 `plan.md`、`progress.md`、`handoff.md` **🟡 任务层**。
2b. 若本次工作引入新的常驻服务/进程/集成，同步更新 `handoff.md` **🟢 常驻层** 和对应 `docs/sop/<name>.md`。
3. 仅在稳定信息变化时更新项目 `README.md`。
4. 写入当日全局 `dev-log/YYYY-MM-DD.md`（位于 Jeff1993 根目录，不是项目子目录）：
   - 写入前先扫描是否已有 `## <项目名>` 区块；有则合并，无则追加。
5. 仅在生命周期/owner/path/status/明确迁移 `last_handoff` 时更新 `.project-status.yaml`。
6. 运行 secret gate：候选 secret payload 不得被 Git tracked（`git ls-files` 命中即中止）。
7. commit 使用 `[CHECKPOINT] YYYY-MM-DD <项目名>: <摘要>` 前缀。
8. 如配置了远程仓库（`origin`）且安全检查通过，必须执行 `git push`。

详细合同：[`Skill/checkpoint.md`](Skill/checkpoint.md)。

## 7. agent-kit 同步规则

`agent-kit/` 是跨设备通用配置合同：

- `manifest.yaml`：声明允许同步的 skills/prompts/agents/commands/rules/plugins。
- `codex/`：Codex 用户自定义 skills/agents/prompts 说明。
- `claude/`：Claude commands/rules/plugins 说明。
- `secrets/`：只放 secret 策略、allowlist 和 payload 政策；默认不放真实 payload。
- `bootstrap/`：初始化合同和脚本（`init-agent-contract.md`）。

用户级配置写入前必须备份；系统/内置 skills 默认不覆盖。

### 7.1 Codex Skill 安装格式（强约束）

当前 Codex 运行时只会自动识别目录式 skill：

```text
~/.codex/skills/<skill-name>/SKILL.md
```

不要只把 `agent-kit/codex/skills/<name>.md` 复制到 `~/.codex/skills/<name>.md` 后就认为已安装；这些根目录 `*.md` 文件可作为源文档/通用 Markdown 复用，但**不会出现在当前 Codex 的 Skills 列表中**。

安装或同步 Codex skill 时必须：

1. 为每个 skill 创建目录：`~/.codex/skills/<name>/`。
2. 将内容写入：`~/.codex/skills/<name>/SKILL.md`。
3. `SKILL.md` 顶部必须包含 YAML frontmatter，至少含 `name` 和 `description`。
4. 重启 Codex 后验证会话 Skills 列表是否出现该 skill。

例：

```bash
mkdir -p ~/.codex/skills/checkpoint-onboarding-ext
cp ~/Documents/Jeff1993/agent-kit/codex/skills/checkpoint-onboarding-ext.md   ~/.codex/skills/checkpoint-onboarding-ext/SKILL.md
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

硬规则：

- **default deny**：未在 allowlist 中的路径不复制。
- **opt-in**：不自动发现并复制 secrets。
- **no tracked payload**：payload 默认不得进入 Git；`git ls-files` 命中即中止。
- **no log values**：报告只写路径类别、计数、hash/checksum，不写内容。
- **dry-run first**：新增或修改 allowlist 后先 dry-run。
- **backups are secrets**：备份和恢复包继承同样的保密规则。

## 9. 并发与冲突

- 不回滚其他 Agent 的改动。
- 同一文件冲突时先合并意图，再写入。
- 高冲突文件：`collab-entry.md`、`onboarding.md`、项目 `plan/progress/handoff`、`.project-status.yaml`。
- 若无法判断，写入 `handoff.md` 阻塞项并停止破坏性操作。

## 10. 结束清单

- [ ] 当前任务状态已写入 `plan.md`。
- [ ] 已完成内容和证据已写入 `progress.md`。
- [ ] 下一步和阻塞已写入 `handoff.md`。
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

skill 会自动执行以下全部阶段并输出就绪报告。手动执行时参考下方各阶段。

**Skill 安装位置**：`~/.claude/skills/con-dev/SKILL.md`
**跨设备同步源**：`agent-kit/claude/skills/con-dev/SKILL.md`（随 jeff1993-docs git pull 到达）

安装步骤（新设备首次）：
```bash
mkdir -p ~/.claude/skills/con-dev
cp ~/Documents/Jeff1993/agent-kit/claude/skills/con-dev/SKILL.md ~/.claude/skills/con-dev/SKILL.md
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
| `repo` 有 GitHub 链接 | `git clone <repo_url> <code_path>` |
| `code_path` 是本地路径（无 repo）| 需从其他设备手动同步或重建 |
| `code_path` 为 `—` | 纯文档项目，无需 clone |
| `last_handoff` | 读取对应 handoff 文件 |

```bash
# 2. 克隆代码仓库（如有）
git clone https://github.com/Jeff19930831/<repo>.git <code_path>
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

### Phase 5：开始工作

```
1. 在 onboarding.md § 1 要求的身份信息中确认：工具名 + 设备 + Jeff1993 路径
2. 按 plan.md Active 区最高优先级任务开始
3. 工作结束时执行 /checkpoint（含 git push）
```

### 快速检查清单

- [ ] Jeff1993 git pull 成功，无冲突
- [ ] 目标项目 handoff.md 已读
- [ ] 代码仓库已 clone 到正确路径
- [ ] 依赖安装完成，验证命令通过
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
