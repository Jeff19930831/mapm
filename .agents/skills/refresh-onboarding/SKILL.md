---
name: refresh-onboarding
description: 中途轻量刷新 onboarding 文档体系。
---

# refresh-onboarding (Codex)

> 等同 Claude `/refresh-onboarding` skill。中途轻量刷新 onboarding 文档体系。
> Codex 通过 prompt 触发: "刷新 onboarding" / "看下 onboarding 健康"。

## 触发关键词
- "刷新 onboarding"
- "刷新 codemap"
- "看下 onboarding 健康"
- "refresh onboarding"

## 前置
- 项目根有 `docs/onboarding/`, 否则提示先 init-onboarding

## Doc Lifecycle Gate

refresh-onboarding 不直接改四文档, 但要检查 onboarding 产物是否保持边界:

- BOOTSTRAP 只做静态入口和场景跳转, 不复制 progress/archive/ADR 正文。
- CODEMAP 是结构地图, 不写当前任务状态。
- module-card 写长期模块知识和陷阱, 不写当前任务流水。
- ADR 写历史原因, handoff 只应链接。
- 若入口文档膨胀, 报告建议: 完成事实进 `progress/YYYY-MM.md`, 旧计划/长评审进 `archive/**`, 重复问题进 `docs/runbooks/**`。

## 流程

### Step 1 — refresh_codemap
```bash
python3 scripts/refresh_codemap.py
```

### Step 2 — check_onboarding
```bash
python3 scripts/check_onboarding.py
```

### Step 3 — 起草修复

对每个 FAIL 项:

| 检查项 | 模型动作 |
|---|---|
| codemap_missing_role | 读对应文件首末, 写一句话职责, Edit CODEMAP.md |
| module_card_missing | 读对应大文件, 按 5 段模板起草 module-card |
| adr_index_stale | `python3 scripts/check_onboarding.py --rebuild-index` |
| bootstrap_jump_dead | 提示用户改 (不自动) |

### Step 4 — WARN 处理
- codemap_freshness: Step 1 已重跑, 应转 OK
- module_card_stale: 提示用户 (不自动重写)
- module_card_orphan: 询问是否删除孤儿
- adr_module_link_dead: 提示检查

### Step 5 — 批量预览
打包所有起草/修改, 用户 y → 落盘 (不 commit)

### Step 6 — 收尾
```
✓ refresh-onboarding 完成
  下一步: 用 checkpoint 把改动 commit
```

## 与 checkpoint 的区别
- checkpoint = refresh-onboarding + 四文档同步 + dev-log + secret gate + commit + push
- refresh-onboarding = 仅 onboarding 同步, 不动 git

## 边界
- 不改 BOOTSTRAP.md (用户手写)
- 不删已有 ADR/cards
- 不 git 操作
