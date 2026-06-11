# MAPM Handoff

> 给下一位 Agent / 下一台设备快速接手。入口文档只回答"我现在该怎么接手"。
> 最后更新：2026-06-11

## Persistent Context

| 项 | 状态 / 约束 | Runbook / 说明 |
|---|---|---|
| MAPM 定位 | Jeff1993 项目规范治理主项目 | `MAPM/README.md` |
| 当前真相源 | 活跃源是 `jeff1993-docs/MAPM`；独立 `mapm` 是 legacy | `MAPM/docs/2026-05-21-mapm-source-sync-audit.md` |
| secret 安全 | handoff/progress 只写引用，不写 payload | `agent-kit/secrets/allowlist.yaml` |
| agent-kit 同步 | `python3 scripts/agent_kit_sync.py --apply`（34 skill, 4 目标目录） | `onboarding.md` § 7.0 |
| 规范体系 | `onboarding.md` 是权威规范；`项目规范.md` 已归档；`Skill/` 已废弃 | `docs/sop/` |
| Skill 源 | 统一在 `agent-kit/claude/skills/` + `agent-kit/codex/skills/` | `agent-kit/manifest.yaml` skill_sync 段 |
| 记忆搜索策略 | 多查询并行（2-3 词/次），禁用泛词堆叠 | con-dev + checkpoint SKILL.md |
| CodeGraph / CODEMAP | CodeGraph 是本地开发雷达；CODEMAP 是 durable 交接地图 | `onboarding.md` § 6 / § 12 |

## Current Takeover

### 当前目标

接力流程 v3.14 已落地：`session-handoff` / `con-dev` / `checkpoint` 边界重划，CodeGraph 与 CODEMAP 分工已写入治理入口和 skill 源。

### 下一步（接手开发方案）

1. **同步新版 skill 安装副本** — 在 Jeff1993 根跑 `python3 scripts/agent_kit_sync.py --apply`
2. **验证 v3.14 流程** — 新会话跑 `/con-dev +wechat-macro-kb`，并做一次 docs-only checkpoint dry-run
3. **cloud-memory Phase 3** — AGENTMEMORY_SECRET + HTTPS + 备份
4. **独立 mapm 仓库处置** — 归档/保留/迁移

### 阻塞 / 风险

- 工作区有本会话无关的未提交改动（Obsidian/其他项目）；checkpoint 只纳入 MAPM 本轮文件，勿 `git add -A`。

### 不要重复

- 不要用旧独立 `Jeff19930831/mapm` 覆盖当前 MAPM → 混淆 legacy 与活跃源
- 不要恢复 `项目规范.md` 为规范正文 → 已降级为指针，权威规范是 `onboarding.md`
- 不要自动 `--apply` 归档 Markdown → 先 dry-run 审查
- 不要把 `.codegraph/` 纳入 Git 或项目同步清单 → 它只是本地索引

## Evidence Pointers

| 类型 | 位置 |
|---|---|
| roadmap | `MAPM/docs/2026-06-03-governance-optimization-roadmap.md` |
| sync tool | 历史设计见 `MAPM/docs/superpowers/specs/2026-06-03-agent-kit-sync-design.md`；当前 checkout 未包含脚本源码 |
| sop runbooks | `docs/sop/` (5 files: new-project-init / github-conventions / agent-collaboration / dashboard-scripts / data-governance-tools) |
| config update | `~/CLAUDE.md`, `~/.claude/CLAUDE.md`, `onboarding.md` § 7.0, `onboarding-compact.md`, `collab-entry.md` |
| v3.14 rules | `collab-entry.md`, `onboarding.md`, `onboarding-compact.md`, `agent-kit/claude/skills/*` |

## Verification

```bash
PYTHONUTF8=1 python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-kit/claude/skills/checkpoint
PYTHONUTF8=1 python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-kit/claude/skills/con-dev
PYTHONUTF8=1 python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py agent-kit/claude/skills/session-handoff
```

## Index

| 文件 | 作用 |
|---|---|
| `MAPM/README.md` | MAPM 项目定位与资产地图 |
| `MAPM/plan.md` | 当前任务（Active 8 项 + Next 6 项） |
| `MAPM/progress.md` | 已完成事实（含 OPT-1..6 详情） |
