---
name: refresh-onboarding
description: >
  中途轻量刷新 onboarding 文档体系。跑 refresh_codemap + check_onboarding, FAIL 项模型自动起草修复
  → 交用户审。不 commit、不 push、不更新四文档、不写 dev-log。
  适合: 大改完代码想立刻同步文档 / 想体检看哪些文档陈旧。当用户说"刷新 onboarding"、"刷新 codemap"、
  "看下 onboarding 健康"时触发。
argument-hint: "[--auto-fix]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# refresh-onboarding — 文档新鲜度轻量同步

`/checkpoint` 的子集: 只做"onboarding 文档"的刷新与修复, 不动 git / 不写其他文档。

## 前置

- 当前工作目录是项目代码根
- 项目已启用大型附加层 (`docs/onboarding/` 存在), 否则提示先 `/init-onboarding`

## Doc Lifecycle Gate

本 skill 不刷新 handoff/plan/progress, 但必须检查 onboarding 产物是否破坏入口边界:

- BOOTSTRAP 只做静态入口和场景跳转, 不复制 progress/archive/ADR 正文。
- CODEMAP 是结构地图, 不写当前任务状态。
- module-card 写长期模块知识和陷阱, 不写当前任务流水。
- ADR 写历史原因, handoff 只应链接。
- 若发现入口文档膨胀, 报告建议: 已完成事实进 `progress/YYYY-MM.md`, 旧计划/长评审进 `archive/**`, 重复问题进 `docs/runbooks/**`。不在本 skill 内直接改四文档。

## 流程

### Step 1 — 跑 refresh_codemap

```bash
python3 scripts/refresh_codemap.py
```

刷新 CODEMAP.md 的表格 + 元数据, 保留已写的"一行职责"列。

### Step 2 — 跑 check_onboarding

```bash
python3 scripts/check_onboarding.py
```

收集所有 FAIL / WARN 项。

### Step 3 — 起草修复

对每个 FAIL 项:

#### 3.1 codemap_missing_role
- 对每个 `<待填>` 文件, Read 首 50 行 + 末 30 行 + 主要 symbol
- 写一句话 (≤ 30 字) 职责
- 直接 Edit CODEMAP.md 把 `<待填>` 替换为实际职责

#### 3.2 module_card_missing
- 对每个 LOC > 1000 且无 card 的文件:
- Read 完整文件 (大文件分段读)
- 按 module-card 模板 5 段起草
- 写到 `docs/onboarding/module-cards/<stem>.md`

#### 3.3 adr_index_stale
```bash
python3 scripts/check_onboarding.py --rebuild-index
```

#### 3.4 其他 FAIL
- bootstrap_jump_dead: 显示死链接, 提示用户改 BOOTSTRAP (不自动改, 因为这是用户手写文件)

### Step 4 — WARN 项处理

- codemap_freshness WARN → Step 1 已重跑, 应该转为 OK
- module_card_stale → 提示用户 (不自动重写, 因为可能只是代码 churn)
- module_card_orphan → 询问用户是否删除孤儿 card
- adr_module_link_dead → 提示用户检查 (可能是文件改名了)

### Step 5 — 批量预览

把所有起草 / 修改打包给用户:

```
📋 准备应用以下修改:

CODEMAP.md:
  + 5 个文件填了职责行 (path1, path2, ...)

module-cards/:
  + workflow.md (2079 LOC, 新建)
  + summarization.md (1086 LOC, 新建)

decisions/INDEX.md:
  ↻ 重生 (15 → 17 行)

确认应用? [y/n/逐条审]
```

用户 y → 文件落盘, 不 commit
用户 n → 回滚所有改动
用户"逐条审" → 进入交互式 review

### Step 6 — 收尾

```
✓ refresh-onboarding 完成
  CODEMAP: X 文件
  cards: Y (新建 M / 更新 0)
  ADR INDEX: 重生

下一步: 用 /checkpoint 把这些改动 commit (含其他工作)
```

## --auto-fix 模式

跳过 Step 5 的预览, 自动应用所有起草。仅用于完全信任模型 + 后续会用 git diff 审核的场景。

## 与 /checkpoint 的关系

- `/checkpoint` 包含 refresh-onboarding 的所有动作 + 四文档同步 + dev-log + secret gate + commit + push
- `/refresh-onboarding` 仅做 onboarding 同步, **不动 git**

适合中途想体检 / 临时刷新, 不想触发完整 checkpoint 流程时用。

## 边界

- 不修改 BOOTSTRAP.md (用户手写文件, 仅给提示)
- 不删除已有 ADR / cards (即使发现 stale)
- 不 git add / commit / push
- 不调用 dev-log 写入

## 错误处理

- 脚本失败 → 展示 stderr, 提示用户人工处理
- onboarding/ 不存在 → 立即报错, 提示 `/init-onboarding`
- 大模块文件读取失败 → 跳过该文件, 报告中标 "skipped"
