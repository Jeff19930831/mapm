# Agent Onboarding (Compact)

> 完整版：`onboarding.md` | 协作入口：`collab-entry.md`

## 身份确认

确认：设备、用户名、工具（claude/codex/kimi）、Jeff1993 根目录、目标项目。

## 启动读取顺序

1. `onboarding-compact.md`（本文件）→ 2. 项目 `handoff.md` 的 Persistent / Current Takeover → 3. `plan.md` Active 区 → 4. `README.md` 定位 / 架构 / 运行段

只有入口明确链接时才展开 `progress*`、`archive/**`、`decisions/**`、`docs/runbooks/**`。

## 四文档职责

小写四文档优先：`README.md` / `plan.md` / `progress.md` / `handoff.md` 是当前写入目标；旧 `PROGRESS.md` / `HANDOFF.md` 只在无小写入口时兼容读取或作历史镜像。

| 文件 | 职责 |
|---|---|
| README.md | 稳定范围、架构（不写实时任务）|
| plan.md | Active / Next / Archived Plans；不写长 Completed 历史 |
| progress.md / progress/YYYY-MM.md | 已完成事实+证据（完成后才写）|
| handoff.md | Persistent / Current Takeover / Index；只回答“现在怎么接手” |
| archive/** | 旧计划、长评审、历史 checkpoint 原文 |
| docs/runbooks/** | 常见问题、部署、配置、恢复步骤和 secret 引用 |

## CodeGraph / CODEMAP

- CodeGraph：本地开发雷达，查调用链、symbol、影响面；`.codegraph/` 不入 Git。
- CODEMAP：`docs/onboarding/CODEMAP.md`，可提交交接地图；checkpoint/refresh-onboarding 刷新。
- 启动不读全 CODEMAP；找职责时 grep CODEMAP，查调用链时用 CodeGraph。

## 三种接力

| 流程 | 用途 | 边界 |
|---|---|---|
| session-handoff | 同设备切 session | 只读 handoff/plan/git 摘要；不查云、不刷新 CODEMAP、不 commit |
| con-dev | 新设备/冷启动接手 | 安全同步、读 takeover docs、可准备 CodeGraph；不改 durable docs |
| checkpoint | 收工可信状态 | 验证、归档、刷新 handoff/progress/onboarding、commit；push/deploy 需授权 |

## 写入规则

- 状态变更 → `.project-status.yaml` → 运行 `update-dashboard.py` + `update-overview.py`
- 路径/大项目文件变化 → `.project-status.yaml` 的 `code_paths` / `sync` → `python3 scripts/project_registry.py lint <项目>`
- 配置方法/服务器/secret 引用变化 → 项目 `docs/runbooks/*.md`；只写引用和恢复步骤，不写密钥值
- 联动契约变化（上游产物、下游消费、目录/schema、接口、指标、调度）→ 跑 `context_gate --enforce` / `project_impact`，同步 contract/runbook 和最小联动验证
- 日常推进 → `plan.md` 写 Active/Next，完成后移到 `progress/YYYY-MM.md`，`handoff.md` 只留当前接手摘要和链接
- 入口文档变长 → 执行 Doc Lifecycle Gate：历史归 `progress/YYYY-MM.md` / `archive/**`，重复问题归 `docs/runbooks/**`
- 收工 → `/checkpoint`（secret path check + commit；push/deploy 需明确授权）
- agent-kit 源 skill 改了 → `python3 scripts/agent_kit_sync.py --apply`
- dev-log → `dev-log/YYYY-MM-DD.md`（先扫描已有区块再合并）

## 行为准则

1. **先想后做** — 不确定就问，不静默假设；多种理解列选项
2. **极简主义** — 不加没要求的功能/抽象/配置；200 行能写成 50 行就重写
3. **手术式修改** — 只改必须改的，不顺手改周围；匹配已有风格
4. **目标驱动** — "修 bug"→写复现测试让它通过；多步任务先列步骤+验证

> 完整规则：`onboarding.md` § 2.5

## 关键引用（按需展开）

| 规则 | 位置 |
|---|---|
| Checkpoint 完整规则 | `onboarding.md` § 6 |
| 解析规则（resolver） | `onboarding.md` § 4 |
| agent-kit 同步工具 | `onboarding.md` § 7.0 |
| 新设备流程 | `onboarding.md` § 11 或 `/con-dev +<项目>` |
| 大项目附加层 | `onboarding.md` § 12 |
| Secret 边界 | `onboarding.md` § 8 |
| 冲突恢复 | `onboarding.md` § 9 |
| 跨项目关系 / 契约 | `onboarding.md` § 13 |
| 多设备路径 / 同步清单 | `onboarding.md` § 14 |
| 长期配置 / Secret 引用 | `onboarding.md` § 15 |
| Doc Lifecycle Gate | `onboarding.md` § 16 |
| 项目联动协同与监督 | `onboarding.md` § 17 |
| Skill 清单 | `collab-entry.md` § 9 |
| SOP（GitHub/初始化/工具） | `docs/sop/` |
