# Jeff1993 协作入口（collab-entry）

> 版本: v3.2.1 / 2026-05-12
> 目的：所有设备、所有 Agent 接力开发的人工统一入口。根目录 `README.md` 仍是自动生成的项目 dashboard，不作为人工规则入口。
> v3.1 改动: 新增大型项目附加层 (`docs/onboarding/`) 入口与 5 个相关 skill (§ 9)。
> v3.2 改动: handoff.md 两层模型（🟢 常驻层 + 🟡 任务层）；docs/sop/ 全局约定；dump_state.sh 鼓励规范。详见 onboarding.md § 3 & § 6。
> v3.2.1 改动: 修正 Codex skill 安装格式为目录式 `~/.codex/skills/<name>/SKILL.md`。

## 0. 新 Agent 先读这 5 步

1. 读取本文，确认全局规则和文档地图。
2. 读取 [`onboarding.md`](onboarding.md)，确认身份、写入规则、checkpoint、init、secret 边界。
3. 通过根 [`README.md`](README.md) 或 `.project-status.yaml` 找到目标项目目录。
4. 在项目目录:
   - **若存在 `docs/onboarding/BOOTSTRAP.md`** (大项目附加层): 优先读 `handoff.md` + `BOOTSTRAP.md`, 按 BOOTSTRAP § 3 场景跳转表按需展开。**不读全 CODEMAP/decisions**。Token 预算 ≤ 5KB。
   - **否则** (小项目, 默认): 若存在 `scripts/dump_state.sh` 先运行它；读 `handoff.md` **🟢 常驻层**（设施全貌）→ **🟡 任务层**（当前接力）→ `plan.md` → `README.md`；若不存在小写文件，则兼容读取 `HANDOFF.md` / `PROGRESS.md`。
5. 开始工作前检查 Git/Obsidian 冲突；结束时执行 `/checkpoint`。

## 1. 当前同步模型

- **Obsidian Sync**：负责让 Jeff1993 Markdown 文档在多设备间快速可见。
- **Git / GitHub**（`jeff1993-docs`）：负责 checkpoint、版本历史、回滚和跨设备冲突处理。
- **代码仓库**：每个项目独立 Git 仓库，在新设备上需要单独 `git clone`（见 § 4）。
- **规则**：Obsidian 让文件到达；Git checkpoint 记录可信状态。

## 2. 文档地图

### 全局文档

| 文件 | 职责 |
|---|---|
| `collab-entry.md` | 人和 Agent 的统一入口（本文件）|
| `onboarding.md` | 新 Agent 接入规则、写入规则、同步/secret 边界、新设备流程 |
| `README.md` | 自动生成的 General dashboard；不要在 AUTO 区手写规则 |
| `项目规范.md` | 长版规范；应指向本入口和四文档模型 |
| `项目总览.md` | 项目总览文档 |
| `定时任务总览.md` | 全局定时任务汇总 |
| `agent-kit/` | skills / prompts / configs / secrets / bootstrap 的同步合同 |
| `Skill/` | Agent 技能定义（`checkpoint.md`、`deep-search.md` 等）|
| `agent-kit/claude/skills/` | Claude Code skill 跨设备同步目录（`con-dev`、`checkpoint` 等）|
| `dev-log/` | 每日全局开发日志（`YYYY-MM-DD.md`），位于 Jeff1993 根目录 |
| `docs/templates/project/` | 四文档标准模板（`handoff.md`、`plan.md`、`progress.md`、`README.md`）|
| `docs/` | 模板、规格、健康报告、备份等辅助文档 |

### 每项目四文档 (基线, 所有项目)

| 文件 | 职责 | 更新时机 |
|---|---|---|
| `README.md` | 稳定范围、方向、架构、运行方式、链接 | 项目范围/功能/设置发生稳定变化 |
| `plan.md` | 当前目标、下一步、未完成任务、验收标准 | 工作开始、计划变化、checkpoint 完成任务后 |
| `progress.md` | 已完成事实、验证证据、checkpoint/commit 记录 | 每次 checkpoint |
| `handoff.md` | 给下一位 Agent/下一台设备的最短接力状态 | 每次 checkpoint 或中断前 |

兼容期至 **2026-06-30**：旧项目的 `PROGRESS.md` / `HANDOFF.md` 继续有效；之后统一迁移为小写。

### 大项目附加层 (LOC ≥ 10K 或源文件 ≥ 20 启用)

| 文件 | 作者 | 职责 |
|---|---|---|
| `docs/onboarding/BOOTSTRAP.md` | 模型起草 + 用户审改 | Agent 启动首读, 含场景跳转表 |
| `docs/onboarding/CODEMAP.md` | 脚本表 + 模型一行职责 | 全模块结构 + 大模块清单 |
| `docs/onboarding/module-cards/*.md` | 模型起草 + 用户审 | LOC > 1000 模块的 5 段名片 |
| `docs/onboarding/decisions/*.md` | 模型起草 (决策时) + 用户审 | ADR 架构决策记录 |
| `docs/onboarding/decisions/INDEX.md` | 脚本 | ADR 索引 (自动) |

启用方式: 在项目根跑 `/init-onboarding` (Claude) 或 prompt "初始化 onboarding" (Codex)。
完整设计: [`MAPM/onboarding-suite/docs/design.md`](MAPM/onboarding-suite/docs/design.md)。

## 3. 项目状态枚举

| 状态 | 含义 |
|---|---|
| `规划中` | 尚未启动，处于构想/设计阶段 |
| `进行中` | 有人在活跃开发 |
| `运行中` | 有定时任务/自动化在持续运行 |
| `维护中` | 无活跃开发，偶发维护 |
| `已完成` | 目标达成，无需维护 |
| `已合并` | 并入其他项目，见 `archive` 字段 |
| `已归档` | 不再活跃，移入归档目录 |

## 3.1 Owner 枚举

| 值 | 含义 |
|---|---|
| `claude` | Claude（任意设备）|
| `codex` | Codex（任意设备）|
| `kimi` | Kimi / ZCode |
| `unassigned` | 暂无负责 Agent |

> Owner 按工具区分，不区分设备。设备信息通过 Agent 启动时的身份确认（见 `onboarding.md § 1`）体现。

## 4. 新设备 / 新 Agent 初始化

详见 [`onboarding.md § 11`](onboarding.md#11-新设备继续老项目流程)。

**自动化方式（推荐）**：安装好 Claude Code 和 `/con-dev` skill 后，直接运行：

```
/con-dev +<项目名>
```

skill 会自动完成全部五阶段：`git pull` → 解析 YAML → clone 代码仓库 → 读取 handoff/plan → 环境检测 → 输出就绪报告。

**手动快速路径（无 skill 时）：**
1. 确认 Jeff1993 已通过 Obsidian Sync 同步到新设备，然后 `git pull`
2. 读 `.project-status.yaml` → 目标项目 `handoff.md`
3. 根据 `code_path` 和 `repo` 字段 clone 代码仓库，运行验证命令

## 5. Checkpoint 协议入口

详见 [`onboarding.md § 6`](onboarding.md#6-checkpoint-规则) 和 [`Skill/checkpoint.md`](Skill/checkpoint.md)。

**要点**：
- 默认 commit 前缀：`[CHECKPOINT] YYYY-MM-DD <项目名>: <摘要>`
- 如配置了远程仓库（`origin`），安全检查通过后必须 `git push`
- dev-log 写入规则：先扫描当天文件是否已有同项目区块，有则合并，无则追加

### dev-log 归档策略

当前按天一个文件（`dev-log/YYYY-MM-DD.md`）。文件积累超过 90 个后，按月迁移到子目录（如 `dev-log/2026-05/`）。

## 6. Secret 同步规则

详见 [`onboarding.md § 8`](onboarding.md#8-secret-同步风险确认)。

核心边界：secret payload 不得进入 Git；`git ls-files` 命中即中止 checkpoint。

## 7. 冲突恢复

详见 [`onboarding.md § 9`](onboarding.md#9-并发与冲突)。

高冲突文件：`collab-entry.md`、`onboarding.md`、项目 `plan/progress/handoff`、`.project-status.yaml`。

## 8. 接力完成标准

一次接力结束时，应能回答：

- 当前目标是什么？
- 已完成什么，有什么验证证据？
- 下一步是谁都能执行吗？
- 是否有阻塞或风险？
- 是否已经 checkpoint 并留下可追踪 commit/report？

## 9. Skill 清单 (跨工具)

由 [`agent-kit/`](agent-kit/) 维护, 跨设备通过 jeff1993-docs git 同步。

### Claude Code (skills/<name>/SKILL.md)

| skill | 作用 | 触发 |
|---|---|---|
| `con-dev` | 跨设备/新会话接力 | `/con-dev +<项目>` |
| `checkpoint` | 收工 (含 onboarding 自检) | `/checkpoint` |
| `init-onboarding` | 一次性接入大型附加层 | `/init-onboarding [--small\|--large\|--upgrade]` |
| `adr` | 起草决策记录 | `/adr [<slug>]` |
| `refresh-onboarding` | 中途轻量刷新 | `/refresh-onboarding` |
| `init-agent` | 新设备 Agent 初始化 | `/init-agent` |

源: [`agent-kit/claude/skills/`](agent-kit/claude/skills/)
本机安装: `cp <src> ~/.claude/skills/<name>/SKILL.md`

### Codex (skills/<name>/SKILL.md)

行为与 Claude 同, 通过 prompt 触发。源: [`agent-kit/codex/skills/`](agent-kit/codex/skills/)

**当前 Codex 只自动识别目录式 skill**：`~/.codex/skills/<name>/SKILL.md`。根目录 `~/.codex/skills/<name>.md` 仅作源/通用 Markdown 复用, 不会出现在当前 Codex Skills 列表中。

本机安装: `mkdir -p ~/.codex/skills/<name> && cp <src>.md ~/.codex/skills/<name>/SKILL.md`（若源文件无 frontmatter, 安装脚本需补齐 `name` / `description`）。

清单和安装步骤见 [`agent-kit/codex/skills.md`](agent-kit/codex/skills.md)；详细约束见 [`onboarding.md § 7.1`](onboarding.md#71-codex-skill-安装格式强约束)。

### 其他 CLI (Gemini / Kimi / 通用)

通用 markdown skill 文件复用 codex 版本。通过项目 `AGENTS.md` 注入启动协议。
详见 [`MAPM/onboarding-suite/docs/adoption.md`](MAPM/onboarding-suite/docs/adoption.md)。
